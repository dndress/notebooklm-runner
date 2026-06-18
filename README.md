# notebooklm-runner

FastAPI sidecar that wraps [`notebooklm-py`](https://github.com/teng-lin/notebooklm-py)
so n8n can trigger D&D session → comic PDF generation via NotebookLM with a
single HTTP POST.

Sibling of [`kaggle-runner`](https://github.com/dndress/kaggle-runner). Joins the
same external Docker network `invents-n8n-gxu2qx`.

## v0.3.0 architecture

Three pieces of context go into NotebookLM per job:

| Piece | Where it lives | Cadence |
|---|---|---|
| **player_visual_guide** | Container assets (`/opt/nblm-assets/<campaign>/*visual_guide*.md`) | Per-campaign, fixed |
| **storyboard** | Google Drive — per-session file dropped by upstream pipeline | Per-session |
| **prompt** | Google Drive — fixed Drive file ID per campaign, editable via Drive UI | Per-campaign, editable without redeploy |

The visual guide is uploaded to NotebookLM as a **Pasted text** source. The
storyboard is uploaded as the second **Pasted text** source. The prompt is
passed as the `instructions=` parameter of `generate_slide_deck`. The raw
transcript itself never reaches NotebookLM directly — n8n upstream distills it
into a storyboard first.

## Endpoints

```
POST /comic    multipart: campaign, session_id, storyboard, prompt   -> 202 { job_id, session_id, campaign }
GET  /comic/{job_id}                                                  -> { status, error?, campaign, ... }
GET  /comic/{job_id}/pdf                                              -> application/pdf
GET  /health                                                          -> { ok, storage_state, campaigns }
```

`/comic` is fire-and-forget; the build runs in a FastAPI `BackgroundTask`
(~10–20 min). Poll `/comic/{job_id}` until `status` is `done` or `failed`,
then `GET /comic/{job_id}/pdf`.

## Campaigns

Multiple campaigns supported. The `campaign` form field selects which
visual_guide subdir gets pulled in. Input is normalized to lowercase + trimmed,
so `PF2E`, `pf2e`, `  Pf2e ` all resolve to the `pf2e` subdir.

Asset layout (one subdir per campaign — only visual_guide is now in-container):

```
assets/
├── pf2e/
│   └── 00_PF2_Player_visual_guide.md   <- uploaded as Source 1
│   (00_PF2_generator_prompt.md is now vestigial — prompt comes from Drive)
└── drakar/
    └── 00_drakar_player_visual_guide.md
    (00_drakar_outline_generator_prompt.md is now vestigial)
```

The legacy `*generator_prompt*.md` files in `assets/{campaign}/` are unused as
of v0.3.0; main.py no longer reads them. Safe to delete in a follow-up commit.

Visual guide is discovered by glob `*visual_guide*.md` — exactly one match per
subdir required, or `/comic` returns HTTP 500.

`GET /health` lists discovered campaigns so n8n / Dokploy can verify a deploy
picked up changes.

## Pipeline per job

1. Persist storyboard + prompt to `/tmp/notebooklm-runner/{job_id}/`.
2. Resolve `campaign` → visual_guide path.
3. `notebooks.create("<CAMPAIGN> Session <session_id>")`.
4. `sources.add_text(...)` for the visual guide.
5. `sources.add_text(...)` for the storyboard.
6. `generate_slide_deck(..., language="es", instructions=<prompt content>, slide_format=DETAILED_DECK, slide_length=DEFAULT)`.
7. `wait_for_completion(..., timeout=1800)`.
8. `download_slide_deck(..., output_format="pdf")` → job's PDF.
9. `notebooks.delete(...)` (best-effort).

Completed jobs + their PDFs are purged after `NBLM_JOB_TTL` seconds (default 24 h).

## Authentication: `storage_state.json` capture flow

`notebooklm-py` calls Google's internal `batchexecute` RPC and needs valid
session cookies. The container does **not** ship with Playwright. Capture the
file once on a machine that has a browser, then copy it onto the VPS named
volume.

### 1. On your laptop (Windows-friendly)

```powershell
pipx install "notebooklm-py[browser]"
# Install Chromium for Playwright (Windows venv-direct path):
C:\Users\<you>\pipx\venvs\notebooklm-py\Scripts\playwright.exe install chromium
notebooklm login
# writes %USERPROFILE%\.notebooklm\storage_state.json (Linux/Mac: ~/.notebooklm/...)
```

### 2. Push to the VPS volume

```bash
# Trampoline through the running container (preferred once container is up)
ssh vps "cat > /tmp/storage_state.json" < ~/.notebooklm/storage_state.json
ssh vps 'docker cp /tmp/storage_state.json notebooklm-runner:/data/notebooklm/profiles/default/storage_state.json \
        && docker exec notebooklm-runner chmod 600 /data/notebooklm/profiles/default/storage_state.json \
        && rm /tmp/storage_state.json \
        && docker restart notebooklm-runner'
```

If scp not allowed by VPS, paste over SSH stdin as above (PowerShell uses
`Get-Content path -Raw | ssh ...`).

Confirm via a curl pod on the shared network:

```bash
docker run --rm --network invents-n8n-gxu2qx curlimages/curl \
  -s http://notebooklm-runner:8000/health
# {"ok":true,"storage_state":true,"campaigns":["drakar","pf2e"]}
```

### 3. Keep cookies warm

Cron inside the container runs hourly (was every 6h in v0.1):

```
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
0 * * * * root NOTEBOOKLM_HOME=/data/notebooklm /usr/local/bin/notebooklm auth refresh --quiet >> /var/log/cron.log 2>&1
```

Absolute path + explicit PATH header are mandatory — cron's default minimal PATH
does NOT include `/usr/local/bin`, where pip-installed CLIs live. Earlier
deploys silently failed every refresh cycle; cookies aged out on Google's
natural lifecycle.

`notebooklm auth check` reports valid even when cookies are dead — it only
checks file structure. Use `auth refresh` as the real liveness probe (it
actually hits Google).

## Environment variables

| Var | Default | Notes |
|---|---|---|
| `NOTEBOOKLM_HOME`   | `/data/notebooklm` | Reads `profiles/default/storage_state.json` under here. |
| `NBLM_ASSETS_DIR`   | `/opt/nblm-assets` | Per-campaign subdirs with visual_guide files. |
| `NBLM_LANGUAGE`     | `es`               | BCP-47 code for `generate_slide_deck`. |
| `NBLM_TIMEOUT`      | `1800`             | Seconds to wait for slide deck (30 min). |
| `NBLM_JOB_TTL`      | `86400`            | Seconds before completed jobs + PDFs are purged (24 h). |

## Dokploy / compose

```yaml
services:
  notebooklm-runner:
    build: .
    container_name: notebooklm-runner
    restart: unless-stopped
    environment:
      NOTEBOOKLM_HOME: /data/notebooklm
      NBLM_ASSETS_DIR: /opt/nblm-assets
      NBLM_LANGUAGE: es
      NBLM_TIMEOUT: "1800"
      NBLM_JOB_TTL: "86400"
    volumes:
      - notebooklm-data:/data/notebooklm
      - ./assets:/opt/nblm-assets:ro
    expose:
      - "8000"
    networks:
      - n8n-net

volumes:
  notebooklm-data:

networks:
  n8n-net:
    name: invents-n8n-gxu2qx
    external: true
```

## n8n workflow shape (v0.3.1 — with upstream transcript→storyboard agent)

Importable JSON in `n8n/{pf2e,drakar}_comic_workflow.json` (22 nodes each).

```
Drive Trigger (transcripts folder, per campaign)
  → Set: bootstrap (campaign hardcoded, session_id from filename, comic_prompt_file_id hardcoded)
  → Drive: Download Transcript (binary "transcript")
  → Extract Transcript Text (binary → JSON.data text)
  → AI Agent: Storyboard  ← Gemini 2.5 Flash sub-node (system prompt set in node UI)
       input:  JSON.data (raw transcript text)
       output: distilled storyboard text
  → Code: stash storyboard (wraps agent text as binary "storyboard" with filename session_<N>.md)
  → splits in parallel:
       Drive: Upload Storyboard (archive)  ← archive copy in /storyboards/<CAMP>/
       Drive: Download Comic Prompt        ← binary "prompt"
  → Code: merge binaries (storyboard + prompt onto one item)
  → POST /comic (multipart: campaign + session_id + storyboard + prompt)
  → Set: init loop (job_id, attempts=0)
  → Wait 60s → GET status → Code: tick → Switch
      done    → GET pdf → (Drive Upload comic PDF, Discord attach) parallel
      failed  → Discord failure
      timeout → Discord failure
      loop    → Wait 60s
  → IF: size <= 25MB (references upstream `$('GET pdf').item.binary.pdf.fileSize`)
      true  → Discord attach (binary `pdf` from GET pdf direct wire)
      false → Discord link (Drive webViewLink)
```

The transcript NEVER reaches notebooklm-runner. n8n's agent distills it first; only
the storyboard + comic prompt are POSTed to `/comic`. The storyboard is also
archived to Drive (per-campaign storyboards folder) for documentation /
later regeneration without re-running the LLM.

After import, replace placeholders + configure the agent node:

| Placeholder | Node | What to put |
|---|---|---|
| `REPLACE_<CAMP>_TRANSCRIPTS_FOLDER_ID` | Drive Trigger | Drive folder where Kaggle drops `transcript_session_<N>.txt` |
| `REPLACE_<CAMP>_COMIC_PROMPT_FILE_ID` | Set: bootstrap | Drive file ID of the per-campaign comic prompt |
| `REPLACE_<CAMP>_STORYBOARDS_FOLDER_ID` | Drive: Upload Storyboard (archive) | Drive folder where storyboards land |
| `REPLACE_<CAMP>_COMICS_FOLDER_ID` | Drive Upload (comic PDF) | Drive folder for output PDFs |
| `REPLACE_DISCORD_WEBHOOK_URL` × 3 | Discord nodes | Channel webhook URL (same for all 3) |
| **System prompt** | AI Agent: Storyboard | Edit the system message in the node UI — current value is a TODO placeholder |

Also:
- Reassign Google Drive credentials to all 5 Drive nodes (Trigger + 3 Downloads/Uploads + Upload Storyboard).
- Reassign Google Gemini credential to the `Gemini 2.5 Flash` sub-node.

Find a Drive folder/file ID by opening it in Drive — the URL ends in
`/folders/<id>` or `/file/d/<id>`.

### Transcript naming convention (locked)

n8n's bootstrap regex `(\d+)` extracts the first integer from the trigger
filename as `session_id`. Kaggle/upstream pipeline must name transcript files
so the first integer is the session number:

- `transcript_session_3.txt` → session_id `3` ✓
- `transcript_session_3_combined.txt` → session_id `3` ✓
- `combined_xyz.txt` → falls back to whole filename (ugly) — DON'T do this

## Smoke tests

```bash
# Health + campaign discovery
curl http://notebooklm-runner:8000/health

# Bad campaign (expect 400)
curl -F campaign=foo -F session_id=1 \
     -F storyboard=@/tmp/sb.md -F prompt=@/tmp/p.md \
     http://notebooklm-runner:8000/comic

# Real job
curl -F campaign=pf2e -F session_id=3 \
     -F storyboard=@/tmp/session3_storyboard.md \
     -F prompt=@/tmp/pf2e_comic_prompt.md \
     http://notebooklm-runner:8000/comic
```

## Build + run locally

```bash
docker compose build
docker compose up -d
docker logs -f notebooklm-runner
```

## Known limitations / open questions

See `notebooklm_comic_design` memory for the canonical list:

- Daily NotebookLM quota: two sessions in one day untested.
- Discord 25 MB attachment cap: link fallback wires the Drive webViewLink.
- `notebooklm-py` `add_file` is broken — using `add_text` everywhere.
- Cookies must be re-seeded periodically if Google flags the laptop→VPS shift.
