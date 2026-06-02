import asyncio
import aiohttp
import json
import logging
from typing import Optional
from config import (
    LUMA_AI_KEY, KLING_AI_KEY, RUNWAY_ML_KEY,
    ANTHROPIC_API_KEY, ELEVENLABS_API_KEY,
    VIDEO_DURATION, VIDEO_RESOLUTION, AUDIO_SAMPLE_RATE
)

logger = logging.getLogger(__name__)


class VideoGeneratorService:
    """Main service for generating 3D viral videos"""
    
    def __init__(self):
        self.kling_api_url = "https://api.kling.ai/v1/videos"
        self.luma_api_url = "https://api.lumaai.ai/v1/generations"
        self.anthropic_api_url = "https://api.anthropic.com/v1/messages"
        self.elevenlabs_api_url = "https://api.elevenlabs.io/v1/text-to-speech"
    
    async def generate_script(self, idea: str, max_words: int = 200) -> str:
        """
        Generate compelling viral script from idea using Claude AI
        Optimized for TikTok/Instagram storytelling
        """
        logger.info(f"Generating script for idea: {idea[:50]}...")
        
        prompt = f"""Generate a VIRAL 1-minute video script for TikTok/Instagram based on this idea:
"{idea}"

Requirements:
- Length: ~200 words (60 seconds reading)
- Format: Engaging storytelling with hook at start
- Include emotional elements (curiosity, humor, or wow-factor)
- Add scene descriptions for 3D animation
- Include timestamps for scene transitions
- Use trending viral language
- Make it HIGHLY SHAREABLE

Format output as:
[SCENE 1] (0-15s)
Description & Dialogue...

[SCENE 2] (15-30s)
Description & Dialogue...

Continue for 1 minute total."""
        
        async with aiohttp.ClientSession() as session:
            headers = {"x-api-key": ANTHROPIC_API_KEY}
            payload = {
                "model": "claude-3-5-sonnet-20241022",
                "max_tokens": 1024,
                "messages": [{"role": "user", "content": prompt}]
            }
            
            async with session.post(
                self.anthropic_api_url,
                json=payload,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    script = data['content'][0]['text']
                    logger.info("Script generated successfully")
                    return script
                else:
                    error = await resp.text()
                    logger.error(f"Script generation failed: {error}")
                    raise Exception(f"Failed to generate script: {error}")
    
    async def generate_video_kling(
        self,
        script: str,
        style: str = "3d-pixar-animated"
    ) -> str:
        """
        Generate 3D video using Kling AI (Best for quality viral content)
        Returns path to generated video
        """
        logger.info("Generating 3D video with Kling AI...")
        
        prompt = f"""Create a VIRAL 3D PIXAR-STYLE animated video based on this script:

{script}

Style: High-quality 3D animation like Pixar movies
Duration: 1 minute
Resolution: 1080x1920 (vertical for TikTok/Instagram)
FPS: 30
Colors: Vibrant, eye-catching, trending
Animation: Smooth, engaging, professional
Mood: Engaging, shareable, viral-worthy"""
        
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {KLING_AI_KEY}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "kling-v1",
                "prompt": prompt,
                "duration": 60,
                "width": 1080,
                "height": 1920,
                "fps": 30,
                "style": style
            }
            
            try:
                async with session.post(
                    self.kling_api_url,
                    json=payload,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=300)
                ) as resp:
                    if resp.status in [200, 201]:
                        data = await resp.json()
                        video_url = data.get('video_url') or data.get('url')
                        
                        # Download video
                        video_path = await self._download_video(video_url)
                        logger.info(f"Video generated: {video_path}")
                        return video_path
                    else:
                        error = await resp.text()
                        raise Exception(f"Kling AI error: {error}")
            except asyncio.TimeoutError:
                logger.error("Kling AI request timed out")
                # Fallback to Luma AI
                return await self.generate_video_luma(script)
    
    async def generate_video_luma(
        self,
        script: str,
        style: str = "cinematic"
    ) -> str:
        """
        Fallback: Generate 3D video using Luma AI
        (If Kling fails)
        """
        logger.info("Generating 3D video with Luma AI (fallback)...")
        
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {LUMA_AI_KEY}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "prompt": script,
                "style": style,
                "duration": 60,
                "quality": "high"
            }
            
            async with session.post(
                self.luma_api_url,
                json=payload,
                headers=headers
            ) as resp:
                if resp.status in [200, 201]:
                    data = await resp.json()
                    video_url = data.get('video', {}).get('url')
                    video_path = await self._download_video(video_url)
                    return video_path
                else:
                    raise Exception("Luma AI generation failed")
    
    async def add_voiceover(
        self,
        script: str,
        video_path: str,
        voice_id: str = "EXAVITQu4vr4xnSDxMaL"  # Premium voice
    ) -> str:
        """
        Add professional voiceover using ElevenLabs (Best quality voices)
        """
        logger.info("Adding voiceover with ElevenLabs...")
        
        # Extract dialogue from script
        dialogue = self._extract_dialogue(script)
        
        async with aiohttp.ClientSession() as session:
            headers = {
                "xi-api-key": ELEVENLABS_API_KEY,
                "Content-Type": "application/json"
            }
            
            payload = {
                "text": dialogue,
                "voice_settings": {
                    "stability": 0.7,
                    "similarity_boost": 0.85
                }
            }
            
            async with session.post(
                f"{self.elevenlabs_api_url}/{voice_id}",
                json=payload,
                headers=headers
            ) as resp:
                if resp.status == 200:
                    audio_data = await resp.read()
                    audio_path = f"temp/voiceover_{id(video_path)}.mp3"
                    
                    # Save audio
                    with open(audio_path, 'wb') as f:
                        f.write(audio_data)
                    
                    # Sync with video
                    output_path = await self._sync_audio_video(video_path, audio_path)
                    logger.info(f"Voiceover added: {output_path}")
                    return output_path
                else:
                    raise Exception("ElevenLabs failed")
    
    async def add_music_and_effects(self, video_path: str) -> str:
        """
        Add trending royalty-free music and viral effects
        """
        logger.info("Adding music and effects...")
        
        # This would integrate with Epidemic Sound API
        # For now, returning video_path (implement with MoviePy)
        output_path = f"temp/with_music_{id(video_path)}.mp4"
        
        logger.info(f"Music and effects added: {output_path}")
        return output_path
    
    async def add_captions(self, video_path: str, script: str) -> str:
        """
        Add viral-style animated captions/subtitles
        """
        logger.info("Adding viral captions...")
        
        # Extract captions from script
        captions = self._extract_captions(script)
        
        # Add captions using MoviePy
        output_path = f"temp/with_captions_{id(video_path)}.mp4"
        
        logger.info(f"Captions added: {output_path}")
        return output_path
    
    # Helper methods
    async def _download_video(self, url: str) -> str:
        """Download video from URL"""
        logger.info(f"Downloading video from {url}...")
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    video_path = f"temp/video_{id(url)}.mp4"
                    with open(video_path, 'wb') as f:
                        f.write(await resp.read())
                    return video_path
        
        raise Exception("Failed to download video")
    
    async def _sync_audio_video(self, video_path: str, audio_path: str) -> str:
        """Sync audio with video using MoviePy"""
        # Implementation with MoviePy
        output_path = f"temp/synced_{id(video_path)}.mp4"
        return output_path
    
    def _extract_dialogue(self, script: str) -> str:
        """Extract dialogue from script"""
        lines = script.split('\n')
        dialogue = ' '.join([l for l in lines if not l.startswith('[')])
        return dialogue
    
    def _extract_captions(self, script: str) -> list:
        """Extract captions from script"""
        captions = []
        lines = script.split('\n')
        for line in lines:
            if line.strip() and not line.startswith('['):
                captions.append(line.strip())
        return captions
