import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
LUMA_AI_KEY = os.getenv("LUMA_AI_KEY", "")
KLING_AI_KEY = os.getenv("KLING_AI_KEY", "")
RUNWAY_ML_KEY = os.getenv("RUNWAY_ML_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")

# Social Media Credentials
TIKTOK_ACCESS_TOKEN = os.getenv("TIKTOK_ACCESS_TOKEN", "")
INSTAGRAM_ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN", "")
YOUTUBE_CREDENTIALS = os.getenv("YOUTUBE_CREDENTIALS", "")

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/viral_videos")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

# API Config
API_HOST = "0.0.0.0"
API_PORT = 8000
DEBUG = os.getenv("DEBUG", "False") == "True"

# Video Settings
VIDEO_DURATION = 60  # 1 minute
VIDEO_FPS = 30
VIDEO_RESOLUTION = "1080x1920"  # Vertical for TikTok/Instagram
AUDIO_SAMPLE_RATE = 44100

# AI Models (Best providers)
SCRIPT_GENERATOR = "claude-3-sonnet"  # Best for storytelling
VIDEO_GENERATOR = "kling-ai"  # Best 3D quality (alternatives: luma-ai, runway-ml)
VOICEOVER_GENERATOR = "elevenlabs"  # Best voice quality
MUSIC_API = "epidemic-sound"  # Best royalty-free music

# Upload Settings
UPLOAD_PLATFORMS = ["tiktok", "instagram", "youtube"]
AUTO_UPLOAD = True
SCHEDULE_UPLOAD = False
