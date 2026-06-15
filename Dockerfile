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

# Cron: refresh notebooklm cookies every 6 hours so storage_state stays warm
RUN echo "0 */6 * * * root NOTEBOOKLM_HOME=/data/notebooklm notebooklm auth refresh --quiet >> /var/log/cron.log 2>&1" \
    > /etc/cron.d/notebooklm-refresh \
    && chmod 0644 /etc/cron.d/notebooklm-refresh

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://localhost:8000/health',timeout=3).status==200 else 1)"

ENTRYPOINT ["/app/entrypoint.sh"]
