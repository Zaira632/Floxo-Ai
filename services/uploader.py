import asyncio
import aiohttp
import json
import logging
from typing import Optional, Dict, List
from config import (
    TIKTOK_ACCESS_TOKEN,
    INSTAGRAM_ACCESS_TOKEN,
    YOUTUBE_CREDENTIALS
)

logger = logging.getLogger(__name__)


class UploaderService:
    """Service for uploading videos to TikTok, Instagram, and YouTube"""
    
    def __init__(self):
        self.tiktok_api_url = "https://open.tiktokapis.com/v1"
        self.instagram_api_url = "https://graph.instagram.com/v18.0"
        self.youtube_api_url = "https://www.googleapis.com/youtube/v3"
    
    async def upload_to_all_platforms(
        self,
        video_path: str,
        title: str,
        description: str,
        tags: List[str],
        platforms: List[str]
    ) -> Dict[str, str]:
        """
        Upload video to multiple platforms simultaneously
        Returns URLs of uploaded videos
        """
        logger.info(f"Starting upload to platforms: {platforms}")
        
        tasks = []
        
        if "tiktok" in platforms:
            tasks.append(self.upload_to_tiktok(video_path, title, description, tags))
        
        if "instagram" in platforms:
            tasks.append(self.upload_to_instagram(video_path, title, description, tags))
        
        if "youtube" in platforms:
            tasks.append(self.upload_to_youtube(video_path, title, description, tags))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        upload_links = {}
        for platform, result in zip(platforms, results):
            if isinstance(result, Exception):
                logger.error(f"Error uploading to {platform}: {result}")
                upload_links[platform] = f"Error: {str(result)}"
            else:
                upload_links[platform] = result
        
        return upload_links
    
    async def upload_to_tiktok(
        self,
        video_path: str,
        title: str,
        description: str,
        tags: List[str]
    ) -> str:
        """
        Upload to TikTok using Official API
        """
        logger.info("Uploading to TikTok...")
        
        try:
            with open(video_path, 'rb') as video_file:
                video_data = video_file.read()
            
            # Prepare metadata
            hashtags = ' '.join([f"#{tag}" for tag in tags[:10]])  # Max 10 hashtags
            caption = f"{description}\n{hashtags}"
            
            async with aiohttp.ClientSession() as session:
                # Upload video file
                upload_url = f"{self.tiktok_api_url}/video/upload/"
                headers = {
                    "Authorization": f"Bearer {TIKTOK_ACCESS_TOKEN}"
                }
                
                # TikTok API requires form data
                form_data = aiohttp.FormData()
                form_data.add_field('video', video_data, filename='video.mp4')
                form_data.add_field('caption', caption)
                
                async with session.post(
                    upload_url,
                    data=form_data,
                    headers=headers
                ) as resp:
                    if resp.status in [200, 201]:
                        data = await resp.json()
                        video_id = data.get('data', {}).get('video_id')
                        tiktok_url = f"https://www.tiktok.com/@yourprofile/video/{video_id}"
                        logger.info(f"TikTok upload successful: {tiktok_url}")
                        return tiktok_url
                    else:
                        error = await resp.text()
                        raise Exception(f"TikTok upload failed: {error}")
        
        except Exception as e:
            logger.error(f"TikTok upload error: {str(e)}")
            raise
    
    async def upload_to_instagram(
        self,
        video_path: str,
        title: str,
        description: str,
        tags: List[str]
    ) -> str:
        """
        Upload Reel to Instagram using Graph API
        """
        logger.info("Uploading to Instagram...")
        
        try:
            with open(video_path, 'rb') as video_file:
                video_data = video_file.read()
            
            hashtags = ' '.join([f"#{tag}" for tag in tags[:30]])
            caption = f"{description}\n\n{hashtags}"
            
            async with aiohttp.ClientSession() as session:
                # Get page ID first
                page_url = f"{self.instagram_api_url}/me/accounts"
                headers = {"Authorization": f"Bearer {INSTAGRAM_ACCESS_TOKEN}"}
                
                async with session.get(page_url, headers=headers) as resp:
                    if resp.status == 200:
                        accounts = await resp.json()
                        page_id = accounts['data'][0]['id'] if accounts['data'] else None
                        
                        if page_id:
                            # Upload as Reel (video)
                            upload_url = f"{self.instagram_api_url}/{page_id}/media"
                            
                            form_data = aiohttp.FormData()
                            form_data.add_field('media_type', 'REELS')
                            form_data.add_field('video', video_data, filename='reel.mp4')
                            form_data.add_field('caption', caption)
                            form_data.add_field('thumb_offset', '0')
                            
                            async with session.post(
                                upload_url,
                                data=form_data,
                                headers=headers
                            ) as upload_resp:
                                if upload_resp.status in [200, 201]:
                                    data = await upload_resp.json()
                                    media_id = data.get('id')
                                    instagram_url = f"https://www.instagram.com/p/{media_id}/"
                                    logger.info(f"Instagram upload successful: {instagram_url}")
                                    return instagram_url
                                else:
                                    error = await upload_resp.text()
                                    raise Exception(f"Instagram upload failed: {error}")
        
        except Exception as e:
            logger.error(f"Instagram upload error: {str(e)}")
            raise
    
    async def upload_to_youtube(
        self,
        video_path: str,
        title: str,
        description: str,
        tags: List[str]
    ) -> str:
        """
        Upload video to YouTube
        """
        logger.info("Uploading to YouTube...")
        
        try:
            # YouTube upload would use google-api-python-client
            # For async, we use a thread executor
            
            def upload_sync():
                from google_auth_oauthlib.flow import InstalledAppFlow
                from google.auth.transport.requests import Request
                from googleapiclient.discovery import build
                from googleapiclient.errors import HttpError
                from googleapiclient.http import MediaFileUpload
                import pickle
                
                # Authenticate
                SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
                
                try:
                    # Load credentials
                    with open(YOUTUBE_CREDENTIALS, 'r') as f:
                        creds_json = json.load(f)
                    
                    # Build YouTube service
                    youtube = build('youtube', 'v3')
                    
                    # Prepare upload
                    body = {
                        'snippet': {
                            'title': title[:100],
                            'description': description[:5000],
                            'tags': tags[:50],
                            'categoryId': '24'  # Entertainment
                        },
                        'status': {
                            'privacyStatus': 'public',
                            'madeForKids': False
                        }
                    }
                    
                    media = MediaFileUpload(
                        video_path,
                        mimetype='video/mp4',
                        resumable=True
                    )
                    
                    request = youtube.videos().insert(
                        part='snippet,status',
                        body=body,
                        media_body=media
                    )
                    
                    response = request.execute()
                    video_id = response['id']
                    youtube_url = f"https://www.youtube.com/watch?v={video_id}"
                    logger.info(f"YouTube upload successful: {youtube_url}")
                    return youtube_url
                
                except Exception as e:
                    raise Exception(f"YouTube upload failed: {str(e)}")
            
            # Run in thread pool
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(None, upload_sync)
            return result
        
        except Exception as e:
            logger.error(f"YouTube upload error: {str(e)}")
            raise
    
    async def schedule_upload(
        self,
        video_path: str,
        title: str,
        description: str,
        tags: List[str],
        platforms: List[str],
        schedule_time: str  # ISO format datetime
    ) -> Dict[str, str]:
        """
        Schedule video upload for later
        """
        logger.info(f"Scheduling upload for {schedule_time}")
        
        # Store in database with scheduled time
        # Implement with Celery or APScheduler
        
        return {
            "status": "scheduled",
            "scheduled_time": schedule_time,
            "platforms": platforms
        }
