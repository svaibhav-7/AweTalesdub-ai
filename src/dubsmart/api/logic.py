import os
import shutil
import uuid
from typing import Dict, Any
from dubsmart.core.pipeline import DubbingPipeline
from dubsmart.utils import get_logger

logger = get_logger(__name__)

# In-memory progress tracking
jobs: Dict[str, Any] = {}

def create_job(filename: str, file_obj) -> str:
    job_id = str(uuid.uuid4())
    temp_dir = f"temp/{job_id}"
    os.makedirs(temp_dir, exist_ok=True)
    
    input_path = os.path.join(temp_dir, filename)
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file_obj, buffer)
    
    jobs[job_id] = {
        "status": "processing", 
        "progress": 0, 
        "message": "Starting pipeline...",
        "input_path": input_path
    }
    return job_id

def run_pipeline_task(job_id: str, src_lang: str, tgt_lang: str):
    """Run pipeline with proper error handling and progress tracking."""
    try:
        job = jobs.get(job_id)
        if not job: 
            return
        
        input_path = job["input_path"]
        output_path = f"output/dubbed_{job_id}_{tgt_lang}.wav"
        os.makedirs("output", exist_ok=True)
        
        # Resolve 'auto' to None for the pipeline
        actual_src = None if src_lang == "auto" else src_lang
        
        # Validate target language
        from dubsmart.utils.config import SUPPORTED_LANGUAGES
        if tgt_lang not in SUPPORTED_LANGUAGES:
            raise ValueError(f"Target language '{tgt_lang}' not supported. Choose from: {', '.join(SUPPORTED_LANGUAGES.keys())}")
        
        pipeline = DubbingPipeline(src_lang=actual_src, tgt_lang=tgt_lang)
        
        job["progress"] = 20
        job["message"] = "Transcribing & Diarizing..."
        logger.info(f"Job {job_id}: Transcribing audio...")
        
        # Run pipeline with error handling at each stage
        try:
            result = pipeline.process(input_path, output_path)
            
            if not result or not os.path.exists(result):
                raise RuntimeError("Pipeline completed but output file not found")
            
            job["status"] = "completed"
            job["progress"] = 100
            job["message"] = f"Dubbing finished! Saved to {os.path.basename(result)}"
            job["output_file"] = result
            logger.info(f"Job {job_id}: Completed successfully")
            
        except Exception as pipeline_err:
            logger.error(f"Job {job_id} pipeline error: {pipeline_err}")
            jobs[job_id]["status"] = "failed"
            jobs[job_id]["message"] = f"Pipeline error: {str(pipeline_err)}"
            return
        
    except Exception as e:
        logger.error(f"Job {job_id} failed: {e}")
        if job_id in jobs:
            jobs[job_id]["status"] = "failed"
            jobs[job_id]["message"] = f"Error: {str(e)[:100]}"
