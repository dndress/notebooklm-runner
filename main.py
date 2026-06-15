"""
notebooklm-runner: FastAPI sidecar wrapping the `notebooklm-py` library so n8n
can trigger D&D session -> comic PDF generation via NotebookLM with a simple
HTTP POST.

Endpoints:
    POST /comic                 -> upload transcript, kick off comic build, returns {job_id}
    GET  /comic/{job_id}        -> { status, error? }
    GET  /comic/{job_id}/pdf    -> application/pdf
    GET  /health                -> liveness + storage_state + campaigns

Env vars:
    NOTEBOOKLM_HOME        Path to dir holding storage_state.json (default /data/notebooklm)
    NBLM_ASSETS_DIR        Where per-campaign asset subdirs live (default /opt/nblm-assets)
    NBLM_LANGUAGE          BCP-47 lang code passed to generate_slide_deck (default "es")
    NBLM_TIMEOUT           Seconds to wait for slide deck generation (default 1800)
    NBLM_JOB_TTL           Seconds before completed jobs + temp dirs are purged (default 86400)

Asset layout (per campaign, lowercase subdir name = campaign flag value):
    /opt/nblm-assets/
        pf2e/
            00_PF2_Player_visual_guide.md
            00_PF2_generator_prompt.md
        drakar/
            00_drakar_player_visual_guide.md
            00_drakar_outline_generator_prompt.md

Files are discovered by glob: anything matching `*visual_guide*.md` is treated as
a source; anything matching `*generator_prompt*.md` is the instructions prompt.
Exactly one of each must exist per campaign subdir.
"""

from __future__ import annotations

import asyncio
import logging
import os
import shutil
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

from fastapi import BackgroundTasks, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse, JSONResponse

from notebooklm import NotebookLMClient
from notebooklm.types import SlideDeckFormat, SlideDeckLength

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
log = logging.getLogger("notebooklm-runner")

ASSETS_DIR = Path(os.environ.get("NBLM_ASSETS_DIR", "/opt/nblm-assets"))
LANGUAGE = os.environ.get("NBLM_LANGUAGE", "es")
TIMEOUT = int(os.environ.get("NBLM_TIMEOUT", "1800"))
JOB_TTL = int(os.environ.get("NBLM_JOB_TTL", "86400"))
WORK_ROOT = Path("/tmp/notebooklm-runner")
WORK_ROOT.mkdir(parents=True, exist_ok=True)

VISUAL_GUIDE_GLOB = "*visual_guide*.md"
GENERATOR_PROMPT_GLOB = "*generator_prompt*.md"


Status = Literal["queued", "running", "done", "failed"]


@dataclass
class Job:
    job_id: str
    session_id: str
    campaign: str
    status: Status = "queued"
    error: str | None = None
    pdf_path: Path | None = None
    notebook_id: str | None = None
    created_at: float = field(default_factory=time.time)
    finished_at: float | None = None


JOBS: dict[str, Job] = {}
JOB_LOCK = asyncio.Lock()


app = FastAPI(title="notebooklm-runner", version="0.2.0")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _normalize_campaign(raw: str) -> str:
    return raw.strip().lower()


def _list_campaigns() -> list[str]:
    if not ASSETS_DIR.is_dir():
        return []
    return sorted(p.name for p in ASSETS_DIR.iterdir() if p.is_dir())


def _resolve_campaign(campaign: str) -> tuple[Path, Path]:
    """Return (visual_guide_path, generator_prompt_path) for `campaign`."""
    camp = _normalize_campaign(campaign)
    camp_dir = ASSETS_DIR / camp
    if not camp_dir.is_dir():
        raise HTTPException(
            status_code=400,
            detail=f"unknown campaign '{camp}'; available: {_list_campaigns()}",
        )
    guides = sorted(camp_dir.glob(VISUAL_GUIDE_GLOB))
    prompts = sorted(camp_dir.glob(GENERATOR_PROMPT_GLOB))
    if len(guides) != 1:
        raise HTTPException(
            status_code=500,
            detail=f"campaign '{camp}': expected 1 visual_guide match, found {len(guides)}",
        )
    if len(prompts) != 1:
        raise HTTPException(
            status_code=500,
            detail=f"campaign '{camp}': expected 1 generator_prompt match, found {len(prompts)}",
        )
    return guides[0], prompts[0]


def _job_dir(job_id: str) -> Path:
    return WORK_ROOT / job_id


def _purge_expired() -> None:
    cutoff = time.time() - JOB_TTL
    stale = [jid for jid, j in JOBS.items() if j.finished_at and j.finished_at < cutoff]
    for jid in stale:
        shutil.rmtree(_job_dir(jid), ignore_errors=True)
        JOBS.pop(jid, None)


async def _build_comic(
    job: Job,
    transcript_path: Path,
    visual_guide: Path,
    generator_prompt: Path,
) -> None:
    """Run the full NotebookLM pipeline for one job."""
    job.status = "running"
    log.info(
        "job=%s campaign=%s starting comic build for session=%s",
        job.job_id, job.campaign, job.session_id,
    )
    try:
        instructions = generator_prompt.read_text(encoding="utf-8")
        pdf_out = _job_dir(job.job_id) / "comic.pdf"

        async with NotebookLMClient.from_storage() as client:
            nb = await client.notebooks.create(
                f"{job.campaign.upper()} Session {job.session_id}"
            )
            job.notebook_id = nb.id
            log.info("job=%s notebook=%s", job.job_id, nb.id)

            # NOTE: `add_file` consistently fails with SourceProcessingError on
            # NotebookLM's side for our markdown/text inputs — reproduced outside
            # FastAPI, file is clean ASCII. `add_text` (Pasted text source) works
            # via a different API path and is READY immediately. Both sources
            # here are plain text so this is a clean swap.
            vg_text = visual_guide.read_text(encoding="utf-8")
            vg_title = f"{job.campaign.upper()} Player Visual Guide"
            vg_src = await client.sources.add_text(nb.id, vg_title, vg_text)
            log.info("job=%s visual_guide source=%s status=%s",
                     job.job_id, vg_src.id, getattr(vg_src, "status", "?"))

            tx_text = transcript_path.read_text(encoding="utf-8", errors="replace")
            tx_title = f"{job.campaign.upper()} Session {job.session_id} Transcript"
            tx_src = await client.sources.add_text(nb.id, tx_title, tx_text)
            log.info("job=%s transcript source=%s status=%s size=%d bytes",
                     job.job_id, tx_src.id, getattr(tx_src, "status", "?"),
                     transcript_path.stat().st_size)

            status = await client.artifacts.generate_slide_deck(
                nb.id,
                source_ids=None,
                language=LANGUAGE,
                instructions=instructions,
                slide_format=SlideDeckFormat.DETAILED_DECK,
                slide_length=SlideDeckLength.DEFAULT,
            )
            final = await client.artifacts.wait_for_completion(
                nb.id, status.task_id, timeout=TIMEOUT
            )
            if not final.is_complete:
                raise RuntimeError(
                    f"slide deck generation status={final.status} error={final.error}"
                )

            await client.artifacts.download_slide_deck(
                nb.id, str(pdf_out), artifact_id=final.task_id, output_format="pdf"
            )

            try:
                await client.notebooks.delete(nb.id)
            except Exception as e:
                log.warning("job=%s notebook delete failed: %s", job.job_id, e)

        job.pdf_path = pdf_out
        job.status = "done"
        log.info("job=%s done -> %s", job.job_id, pdf_out)
    except Exception as e:
        log.exception("job=%s failed", job.job_id)
        job.status = "failed"
        job.error = f"{type(e).__name__}: {e}"
    finally:
        job.finished_at = time.time()
        try:
            transcript_path.unlink(missing_ok=True)
        except Exception:
            pass


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.post("/comic", status_code=202)
async def create_comic(
    background: BackgroundTasks,
    campaign: str = Form(...),
    session_id: str = Form(...),
    transcript: UploadFile = File(...),
):
    _purge_expired()
    visual_guide, generator_prompt = _resolve_campaign(campaign)
    camp = _normalize_campaign(campaign)

    job_id = uuid.uuid4().hex
    work = _job_dir(job_id)
    work.mkdir(parents=True, exist_ok=True)
    transcript_path = work / "transcript.txt"

    with transcript_path.open("wb") as f:
        while True:
            chunk = await transcript.read(1 << 20)
            if not chunk:
                break
            f.write(chunk)

    async with JOB_LOCK:
        JOBS[job_id] = Job(job_id=job_id, session_id=session_id, campaign=camp)

    background.add_task(
        _build_comic, JOBS[job_id], transcript_path, visual_guide, generator_prompt,
    )
    return {"job_id": job_id, "session_id": session_id, "campaign": camp}


@app.get("/comic/{job_id}")
async def get_status(job_id: str):
    job = JOBS.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="job not found")
    body: dict[str, Any] = {
        "job_id": job.job_id,
        "session_id": job.session_id,
        "campaign": job.campaign,
        "status": job.status,
    }
    if job.error:
        body["error"] = job.error
    return JSONResponse(body)


@app.get("/comic/{job_id}/pdf")
async def get_pdf(job_id: str):
    job = JOBS.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="job not found")
    if job.status != "done" or not job.pdf_path or not job.pdf_path.is_file():
        raise HTTPException(status_code=409, detail=f"job not ready (status={job.status})")
    return FileResponse(
        path=str(job.pdf_path),
        media_type="application/pdf",
        filename=f"{job.campaign}_session_{job.session_id}.pdf",
    )


@app.get("/health")
async def health():
    storage_ok = (Path(os.environ.get("NOTEBOOKLM_HOME", "/data/notebooklm"))
                  / "storage_state.json").is_file()
    return {
        "ok": True,
        "storage_state": storage_ok,
        "campaigns": _list_campaigns(),
    }
