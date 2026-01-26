from fastapi import APIRouter, UploadFile, File, Form, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from .logic import jobs, create_job, run_pipeline_task

router = APIRouter()

@router.post("/dub")
async def dub_audio(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    src_lang: str = Form("auto"),
    tgt_lang: str = Form("hi")
):
    job_id = create_job(file.filename, file.file)
    background_tasks.add_task(run_pipeline_task, job_id, src_lang, tgt_lang)
    return {"job_id": job_id}

@router.get("/status/{job_id}")
async def get_status(job_id: str):
    if job_id not in jobs:
        return JSONResponse(status_code=404, content={"message": "Job not found"})
    return jobs[job_id]

@router.get("/download/{job_id}")
async def download_result(job_id: str):
    job = jobs.get(job_id)
    if not job or job.get("status") != "completed":
        return JSONResponse(status_code=400, content={"message": "File not ready"})
    return FileResponse(job["output_file"])
