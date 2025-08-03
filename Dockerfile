# ===== Builder stage =====
FROM python:3.11-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# System deps (add build tools only if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# Copy and install dependencies
COPY src/requirements.txt ./requirements.txt
RUN python -m pip install --upgrade pip wheel \
 && pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

# ===== Runtime stage =====
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_ENV=production \
    HOST=0.0.0.0 \
    PORT=8000 \
    WORKERS=2

WORKDIR /app

# Minimal OS deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# Copy wheels and install
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/*

# Copy application code
COPY src ./src
COPY .env ./.env  # optional: avoid in prod images; prefer runtime env injection

# Create non-root user
RUN useradd -m appuser
USER appuser

EXPOSE 8000

# Healthcheck (adjust endpoint)
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import sys,requests; sys.exit(0) if requests.get('http://127.0.0.1:8000/healthy', timeout=2).ok else sys.exit(1)" || exit 1

# Entrypoint (adjust module:path)
# If your app is at src/main/app.py with FastAPI instance "app":
CMD ["uvicorn", "src.main.app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
