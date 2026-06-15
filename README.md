# notebooklm-runner

FastAPI sidecar that wraps [`notebooklm-py`](https://github.com/teng-lin/notebooklm-py)
so n8n can trigger D&D session → comic PDF generation via NotebookLM with a
single HTTP POST.

Sibling of [`kaggle-runner`](https://github.com/dndress/kaggle-runner). Joins the
same external Docker network `invents-n8n-gxu2qx`.

## Endpoints

```
POST /comic              multipart: campaign, session_id, transcript -> 202 { job_id, session_id, campaign }
GET  /comic/{job_id}                                                 -> { status, error?, campaign, ... }
GET  /comic/{job_id}/pdf                                             -> application/pdf
GET  /health                                                         -> { ok, storage_state, campaigns }
```

`/comic` is fire-and-forget; the build runs in a FastAPI `BackgroundTask`
(~10–20 min). Poll `/comic/{job_id}` until `status` is `done` or `failed`,
then `GET /comic/{job_id}/pdf`.

## Campaigns

Multiple campaigns are supported. The `campaign` form field on `POST /comic`
selects which visual guide + generator prompt get pulled in. Input is
normalized to lowercase and trimmed, so `PF2E`, `pf2e`, and `  Pf2e ` all
resolve to the `pf2e` subdir.

Asset layout (one subdir per campaign):

```
assets/
├── pf2e/
│   ├── 00_PF2_Player_visual_guide.md         <- uploaded as NotebookLM source
│   └── 00_PF2_generator_prompt.md            <- passed as `instructions=`
└── drakar/
    ├── 00_drakar_player_visual_guide.md      <- uploaded as NotebookLM source
    └── 00_drakar_outline_generator_prompt.md <- passed as `instructions=`
```

File discovery inside each subdir is glob-based:

| Role | Glob | Filename can be anything matching… |
|---|---|---|
| Source (visual guide) | `*visual_guide*.md` | `00_drakar_player_visual_guide.md`, etc. |
| `instructions=` prompt | `*generator_prompt*.md` | `00_PF2_generator_prompt.md`, `00_drakar_outline_generator_prompt.md`, etc. |

Exactly **one** match for each glob must exist per subdir, otherwise the API
returns 500 with a diagnostic. To add a third campaign, drop a new lowercase
subdir under `assets/` and restart the container — no code change.

`GET /health` lists the discovered campaigns so n8n / Dokploy can verify a
deploy picked up the new files.

## Pipeline per job

1. Persist transcript to `/tmp/notebooklm-runner/{job_id}/transcript.txt`.
2. Resolve `campaign` → `(visual_guide.md, generator_prompt.md)`.
3. `notebooks.create("{CAMPAIGN} Session <session_id>")`.
4. `sources.add_file(...)` for the campaign's visual guide (style lock).
5. `sources.add_file(...)` for the transcript.
6. `artifacts.generate_slide_deck(..., slide_format=DETAILED_DECK, slide_length=DEFAULT, language="es", instructions=<generator_prompt.md>)`.
7. `artifacts.wait_for_completion(..., timeout=1800)`.
8. `artifacts.download_slide_deck(..., output_format="pdf")` → job's PDF.
9. `notebooks.delete(...)` (best-effort cleanup).

Completed jobs + their PDFs are purged after `NBLM_JOB_TTL` seconds (default 24 h).

## Authentication: `storage_state.json` capture flow

`notebooklm-py` calls Google's internal `batchexecute` RPC and needs valid
session cookies. The container does **not** ship with Playwright. Capture the
file once on a machine that has a browser, then copy it onto the VPS named
volume.

### 1. On your laptop (one-time)

```bash
pipx install 'notebooklm-py[browser]'        # full install incl. Playwright
notebooklm login                              # interactive Google login
# writes ~/.notebooklm/storage_state.json
```

### 2. Push to the VPS volume

```bash
# A) Trampoline through the running container
scp ~/.notebooklm/storage_state.json vps:/tmp/storage_state.json
ssh vps 'docker cp /tmp/storage_state.json notebooklm-runner:/data/notebooklm/storage_state.json \
        && docker exec notebooklm-runner chmod 600 /data/notebooklm/storage_state.json \
        && rm /tmp/storage_state.json \
        && docker restart notebooklm-runner'
```

```bash
# B) Helper container (use when notebooklm-runner is not up yet)
scp ~/.notebooklm/storage_state.json vps:/tmp/storage_state.json
ssh vps 'docker run --rm -v notebooklm-data:/data/notebooklm -v /tmp:/host alpine \
        sh -c "cp /host/storage_state.json /data/notebooklm/storage_state.json \
               && chmod 600 /data/notebooklm/storage_state.json" \
        && rm /tmp/storage_state.json'
```

Confirm:

```bash
curl http://notebooklm-runner:8000/health
# {"ok":true,"storage_state":true,"campaigns":["drakar","pf2e"]}
```

### 3. Keep cookies warm

A cron job inside the container runs every 6 h:

```
0 */6 * * * notebooklm auth refresh --quiet
```

If `auth refresh` ever fails, re-run step 1 on the laptop and re-copy.

## Environment variables

| Var | Default | Notes |
|---|---|---|
| `NOTEBOOKLM_HOME`   | `/data/notebooklm` | Reads `storage_state.json` here. |
| `NBLM_ASSETS_DIR`   | `/opt/nblm-assets` | Mount of `./assets`. Per-campaign subdirs inside. |
| `NBLM_LANGUAGE`     | `es`               | BCP-47 code passed to `generate_slide_deck`. |
| `NBLM_TIMEOUT`      | `1800`             | Seconds to wait for slide deck. |
| `NBLM_JOB_TTL`      | `86400`            | Seconds before completed jobs + PDFs are purged. |

`NBLM_VISUAL_GUIDE` and `NBLM_GENERATOR_PROMPT` from v0.1 are gone — file
discovery is per-campaign and glob-based now.

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

## n8n workflow shape

```
Drive Trigger (new combined transcript in PF2E/ or Drakar/ folder)
  → Set: extract session_id from filename, derive campaign from parent folder
  → Drive: Download File (binary)
  → HTTP POST notebooklm-runner:8000/comic
       (multipart: campaign + session_id + transcript)
  → Wait loop: HTTP GET /comic/{{job_id}} every 60s until status=done|failed
  → If status=done:
       HTTP GET /comic/{{job_id}}/pdf  (binary)
       Drive: upload /D&D/comics/{{campaign}}/session_{{session_id}}.pdf
       Discord webhook: post PDF (>25 MB → fall back to Drive link)
  → If status=failed: Discord error alert
```

n8n HTTP node + Execute Command timeouts must exceed ~20 min — bump both.

## Smoke tests

```bash
# Health + campaign discovery
curl http://notebooklm-runner:8000/health

# Bad campaign (expect 400 with available campaigns listed)
curl -F campaign=foo -F session_id=1 -F transcript=@/tmp/t.txt \
     http://notebooklm-runner:8000/comic

# Real job (PF2E)
curl -F campaign=pf2e -F session_id=3 -F transcript=@/tmp/session3.txt \
     http://notebooklm-runner:8000/comic
# -> { "job_id": "...", "session_id": "3", "campaign": "pf2e" }
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
- Discord 25 MB attachment cap: PDFs may exceed, fallback to Drive link untested.
- `--language es` vs in-prompt Spanish rule: verify on first run per campaign.
- `notebooklm-py` upstream breakage risk: accept "no comic this week" as the
  failure mode; rerun once the lib catches up.
