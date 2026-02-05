# Deploying Dubsmart AI (Docker)

This repository includes a Dockerfile and `docker-compose.yml` to build the React frontend and run the FastAPI backend.

Quick start:

```bash
# Build and run with docker-compose
docker compose up --build -d

# Open http://localhost:8000 in your browser
```

Development run (backend only):

```bash
pip install -r requirements.txt
uvicorn dubsmart.api.app:app --reload --host 0.0.0.0 --port 8000
```

Notes:
- The Docker image installs `ffmpeg` and Python dependencies. The image build can be large because of model libraries (Torch, Transformers). Use a machine with sufficient disk and memory.
- Output files are written to the `output/` directory (mounted into the container by `docker-compose.yml`).
