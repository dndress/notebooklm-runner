#!/usr/bin/env bash
set -euo pipefail

# Start cron in the background for the auth-refresh job
service cron start || true

exec uvicorn main:app --host 0.0.0.0 --port 8000
