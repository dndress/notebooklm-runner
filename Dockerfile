FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    NOTEBOOKLM_HOME=/data/notebooklm

WORKDIR /app

# Install cron for keep-warm refresh
RUN apt-get update && apt-get install -y --no-install-recommends cron \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY main.py entrypoint.sh ./
RUN chmod +x /app/entrypoint.sh

# Cron: refresh notebooklm cookies every hour so storage_state stays warm.
# CRITICAL: cron runs with a minimal PATH that does NOT include /usr/local/bin
# where pip installs CLIs. Without an absolute path here, the job silently fails
# with "notebooklm: not found" and cookies age out on Google's natural lifecycle.
# Bumped to hourly (was every 6h) for safety margin against fingerprint-flag invalidation.
RUN echo "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin" \
    > /etc/cron.d/notebooklm-refresh \
    && echo "0 * * * * root NOTEBOOKLM_HOME=/data/notebooklm /usr/local/bin/notebooklm auth refresh --quiet >> /var/log/cron.log 2>&1" \
    >> /etc/cron.d/notebooklm-refresh \
    && chmod 0644 /etc/cron.d/notebooklm-refresh

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://localhost:8000/health',timeout=3).status==200 else 1)"

ENTRYPOINT ["/app/entrypoint.sh"]
