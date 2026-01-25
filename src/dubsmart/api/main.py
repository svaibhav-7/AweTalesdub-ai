import os
import shutil
import uuid
from fastapi import FastAPI, UploadFile, File, Form, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from dubsmart.core.pipeline import DubbingPipeline
from dubsmart.utils import get_logger

logger = get_logger(__name__)

app = FastAPI(title="Dubsmart AI API")

# Enable CORS for the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory progress tracking (use Redis/Database for production)
jobs = {}

@app.post("/dub")
async def dub_audio(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    src_lang: str = Form("auto"),
    tgt_lang: str = Form("hi")
):
    job_id = str(uuid.uuid4())
    temp_dir = f"temp/{job_id}"
    os.makedirs(temp_dir, exist_ok=True)
    
    input_path = os.path.join(temp_dir, file.filename)
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    output_path = f"output/dubbed_{job_id}_{tgt_lang}.wav"
    os.makedirs("output", exist_ok=True)
    
    jobs[job_id] = {"status": "processing", "progress": 0, "message": "Starting pipeline..."}
    
    background_tasks.add_task(run_pipeline, job_id, input_path, src_lang, tgt_lang, output_path)
    
    return {"job_id": job_id}

@app.get("/status/{job_id}")
async def get_status(job_id: str):
    if job_id not in jobs:
        return JSONResponse(status_code=404, content={"message": "Job not found"})
    return jobs[job_id]

@app.get("/download/{job_id}")
async def download_result(job_id: str):
    job = jobs.get(job_id)
    if not job or job.get("status") != "completed":
        return JSONResponse(status_code=400, content={"message": "File not ready"})
    return FileResponse(job["output_file"])

def run_pipeline(job_id: str, input_path: str, src_lang: str, tgt_lang: str, output_path: str):
    try:
        # Resolve 'auto' to None for the pipeline
        actual_src = None if src_lang == "auto" else src_lang
        
        pipeline = DubbingPipeline(src_lang=actual_src, tgt_lang=tgt_lang)
        
        # Override logger or use a callback to track progress if needed
        # For now, we'll update status at major milestones
        jobs[job_id]["progress"] = 20
        jobs[job_id]["message"] = "Transcribing & Diarizing..."
        
        # Note: The original pipeline.process doesn't have a progress callback yet
        # but we can wrap its steps if we wanted more granular tracking.
        pipeline.process(input_path, output_path)
        
        jobs[job_id]["status"] = "completed"
        jobs[job_id]["progress"] = 100
        jobs[job_id]["message"] = "Dubbing finished successfully!"
        jobs[job_id]["output_file"] = output_path
        
    except Exception as e:
        logger.error(f"Job {job_id} failed: {e}")
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["message"] = str(e)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
