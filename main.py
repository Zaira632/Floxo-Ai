from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional
import asyncio
import logging
from datetime import datetime
from config import API_HOST, API_PORT, DEBUG
from services.video_generator import VideoGeneratorService
from services.uploader import UploaderService
from db.models import VideoJob

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Viral Video System",
    description="Generate and upload 3D viral videos automatically",
    version="1.0.0"
)

# Services
video_service = VideoGeneratorService()
uploader_service = UploaderService()


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
    
    Flow:
    1. Generate script from idea
    2. Generate 3D video using Kling AI / Luma AI
    3. Add voiceover (ElevenLabs)
    4. Add trending music
    5. Add captions & effects
    6. Auto-upload to platforms
    """
    try:
        logger.info(f"Received video request: {request.idea}")
        
        # Create job in database
        job = VideoJob(
            idea=request.idea,
            title=request.title or request.idea[:50],
            status="processing",
            platforms=request.platforms,
            created_at=datetime.now()
        )
        # Save job (implemented in DB layer)
        
        # Start async video generation
        background_tasks.add_task(
            process_video,
            job.id,
            request,
            auto_upload=request.auto_upload
        )
        
        return {
            "job_id": job.id,
            "status": "queued",
            "message": "Video generation started. Check status with job_id"
        }
    
    except Exception as e:
        logger.error(f"Error creating video job: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/status/{job_id}")
async def get_status(job_id: str):
    """Check video generation progress"""
    try:
        job = VideoJob.get_by_id(job_id)  # DB fetch
        
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        return VideoStatusResponse(
            job_id=job.id,
            status=job.status,
            progress=job.progress,
            video_url=job.video_url,
            upload_links=job.upload_links,
            created_at=job.created_at
        )
    
    except Exception as e:
        logger.error(f"Error fetching status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/videos")
async def list_videos(limit: int = 20, offset: int = 0):
    """List all generated videos"""
    try:
        videos = VideoJob.get_all(limit=limit, offset=offset)
        return {"total": len(videos), "videos": videos}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Background Task
async def process_video(job_id: str, request: VideoIdeaRequest, auto_upload: bool):
    """Main video generation pipeline"""
    try:
        logger.info(f"Starting video processing for job {job_id}")
        
        # Step 1: Generate Script
        logger.info("Step 1: Generating script from idea...")
        script = await video_service.generate_script(request.idea)
        
        # Step 2: Generate 3D Video
        logger.info("Step 2: Generating 3D video with Kling AI...")
        video_path = await video_service.generate_video_kling(script)
        
        # Step 3: Add Voiceover
        logger.info("Step 3: Adding voiceover...")
        voiceover_path = await video_service.add_voiceover(script, video_path)
        
        # Step 4: Add Music & Effects
        logger.info("Step 4: Adding music and effects...")
        final_video = await video_service.add_music_and_effects(voiceover_path)
        
        # Step 5: Add Captions
        logger.info("Step 5: Adding viral captions...")
        final_video_with_captions = await video_service.add_captions(final_video, script)
        
        # Update job status
        job = VideoJob.get_by_id(job_id)
        job.video_path = final_video_with_captions
        job.status = "completed"
        job.progress = 100
        job.save()
        
        # Step 6: Auto-Upload
        if auto_upload:
            logger.info("Step 6: Auto-uploading to platforms...")
            upload_results = await uploader_service.upload_to_all_platforms(
                final_video_with_captions,
                request.title,
                request.description,
                request.tags,
                request.platforms
            )
            job.upload_links = upload_results
            job.save()
            logger.info(f"Upload completed: {upload_results}")
        
        logger.info(f"Video processing completed for job {job_id}")
    
    except Exception as e:
        logger.error(f"Error processing video: {str(e)}")
        job = VideoJob.get_by_id(job_id)
        job.status = "failed"
        job.error = str(e)
        job.save()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=API_HOST,
        port=API_PORT,
        reload=DEBUG
    )
