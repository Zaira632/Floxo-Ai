from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional
import logging
from datetime import datetime
from config import API_HOST, API_PORT, DEBUG

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Viral Video System",
    description="Generate and upload 3D viral videos automatically",
    version="1.0.0"
)


# Request Models
class VideoIdeaRequest(BaseModel):
    idea: str
    title: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[list[str]] = None
    platforms: list[str] = ["tiktok", "instagram", "youtube"]
    auto_upload: bool = True


class VideoStatusResponse(BaseModel):
    job_id: str
    status: str
    progress: int
    video_url: Optional[str] = None
    upload_links: Optional[dict] = None
    created_at: datetime


# Routes
@app.get("/")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "AI Viral Video Generator",
        "version": "1.0.0"
    }


@app.post("/generate-video")
async def generate_video(
    request: VideoIdeaRequest,
    background_tasks: BackgroundTasks
):
    """
    Main endpoint: Accept idea and generate viral video
    """
    try:
        logger.info(f"Received video request: {request.idea}")
        
        return {
            "job_id": "test-job-001",
            "status": "queued",
            "message": "Video generation started. Check status with job_id"
        }
    
    except Exception as e:
        logger.error(f"Error creating video job: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/status/{job_id}")
async def get_status(job_id: str):
    """Check video generation progress"""
    return VideoStatusResponse(
        job_id=job_id,
        status="processing",
        progress=50,
        video_url=None,
        upload_links=None,
        created_at=datetime.now()
    )


@app.get("/videos")
async def list_videos(limit: int = 20, offset: int = 0):
    """List all generated videos"""
    return {"total": 0, "videos": []}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=API_HOST,
        port=API_PORT,
        log_level="info"
    )
