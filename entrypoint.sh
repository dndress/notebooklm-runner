#!/usr/bin/env bash
set -euo pipefail

# Start cron daemon for the auth-refresh job. `service cron start`
# is unreliable on slim images (no init), so invoke the binary directly —
# it daemonizes by default.
cron || true

exec uvicorn main:app --host 0.0.0.0 --port 8000
