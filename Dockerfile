### Multi-stage Dockerfile: build frontend, run FastAPI backend
FROM node:18-alpine AS frontend
WORKDIR /app/webapp
COPY webapp/package.json webapp/package-lock.json* ./
RUN npm install --legacy-peer-deps || true
COPY webapp/ ./
RUN npm run build

FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1

# Install ffmpeg and build deps
RUN apt-get update \
 && apt-get install -y --no-install-recommends ffmpeg build-essential git ca-certificates \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt || true

# Copy app sources
COPY . /app

# Copy frontend build
COPY --from=frontend /app/webapp/dist /app/webapp/dist

EXPOSE 8000
CMD ["uvicorn", "dubsmart.api.app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
