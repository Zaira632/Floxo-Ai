## 🎨 **Advanced Features Guide**

### **Customization & Pro Tips**

---

## **1. Custom Video Styles**

### **Available Styles**
```python
# In services/video_generator.py modify:

STYLES = {
    "3d-pixar": "Pixar-style 3D animation",
    "cinematic": "Cinema quality storytelling",
    "anime": "Anime-style animation",
    "realistic": "Photorealistic rendering",
    "cartoon": "Fun cartoon style",
    "motion-graphics": "Modern motion graphics",
    "stop-motion": "Stop-motion animation"
}
```

**Usage:**
```bash
POST /generate-video
{
    "idea": "Your idea",
    "style": "3d-pixar"  # Set custom style
}
```

---

## **2. Multi-Language Support**

### **Voiceover in Different Languages**
```python
# Modify ElevenLabs request:

VOICE_CONFIGS = {
    "en-US": "EXAVITQu4vr4xnSDxMaL",  # English
    "es-ES": "jHBSvCqYkqWvJn8o3i3b",  # Spanish
    "fr-FR": "qgZXPPAGjPzJGgf3TQLV",  # French
    "de-DE": "VR6AewLVsFNHj2MF0QnL",  # German
    "ja-JP": "2jABcMSFZ8bfVbHZNCnD",  # Japanese
    "zh-CN": "Xb7hH8MSUJpSbPP7z9BL",  # Mandarin
    "hi-IN": "pNInz6obpgDQGcFmZCC2",  # Hindi
}
```

---

## **3. Scheduling Videos**

### **Schedule Upload for Later**
```bash
POST /schedule-upload
{
    "idea": "Your idea",
    "scheduled_time": "2024-05-15T18:00:00Z",
    "platforms": ["tiktok", "instagram"]
}

Response:
{
    "status": "scheduled",
    "scheduled_time": "2024-05-15T18:00:00Z"
}
```

---

## **4. Batch Video Generation**

### **Generate Multiple Videos at Once**
```bash
POST /generate-batch
{
    "videos": [
        {"idea": "Funny cat video"},
        {"idea": "Motivational quote"},
        {"idea": "Cooking hack"}
    ],
    "auto_upload": true
}
```

---

## **5. Video Analytics & Optimization**

### **Get Performance Metrics**
```bash
GET /analytics/{job_id}

Response:
{
    "video_id": "vid123",
    "platforms": {
        "tiktok": {
            "views": 45000,
            "likes": 8900,
            "shares": 1200,
            "comments": 340,
            "engagement_rate": 22.3,
            "watch_time_avg": "48s"
        },
        "instagram": {
            "views": 23000,
            "likes": 5600,
            "shares": 800,
            "comments": 290,
            "engagement_rate": 27.5,
            "watch_time_avg": "52s"
        },
        "youtube": {
            "views": 12000,
            "likes": 2300,
            "shares": 150,
            "comments": 445,
            "engagement_rate": 22.1,
            "watch_time_avg": "55s"
        }
    },
    "viral_score": 8.7,  # 0-10 scale
    "trending_keywords": ["funny", "cat", "pets"],
    "recommendations": [
        "Upload during peak hours (6-8 PM)",
        "Add more trending hashtags",
        "Similar videos perform well on Instagram"
    ]
}
```

---

## **6. AI-Powered Optimization**

### **Auto-Optimize for Virality**
```python
# Modify script generation prompt to include:

prompt += """
Optimization for virality:
- Add hooks in first 3 seconds (90% of engagement happens there)
- Include emotional triggers (shock, humor, inspiration, FOMO)
- Use trending sounds/formats
- Include call-to-action at end
- Keep pacing fast (scene every 3-5 seconds)
"""
```

---

## **7. Custom Music Library**

### **Add Your Own Music**
```bash
POST /add-music-library
{
    "playlist_name": "Trending TikTok Hits",
    "music_urls": [
        "https://example.com/music1.mp3",
        "https://example.com/music2.mp3"
    ]
}
```

---

## **8. A/B Testing**

### **Generate Multiple Versions for Testing**
```bash
POST /generate-variants
{
    "idea": "Your idea",
    "num_variants": 3,
    "variations": [
        {"style": "cinematic", "music": "dramatic"},
        {"style": "cartoon", "music": "upbeat"},
        {"style": "anime", "music": "epic"}
    ]
}

Response:
{
    "variants": [
        {"id": "var1", "url": "..."},
        {"id": "var2", "url": "..."},
        {"id": "var3", "url": "..."}
    ],
    "recommendation": "var2 has highest predicted engagement"
}
```

---

## **9. Trend Analysis**

### **Get Current Trending Topics**
```bash
GET /trends?platform=tiktok

Response:
{
    "trends": [
        {
            "hashtag": "#FYP",
            "volume": 500000,
            "engagement_rate": 18.5,
            "growth": "↑ 12%"
        },
        {
            "hashtag": "#viral",
            "volume": 450000,
            "engagement_rate": 15.2,
            "growth": "↑ 8%"
        }
    ]
}
```

---

## **10. Advanced Editing**

### **Post-Generation Editing**
```bash
POST /edit-video/{job_id}
{
    "edits": [
        {"type": "crop", "dimensions": "9:16"},
        {"type": "filter", "name": "warm"},
        {"type": "speed", "multiplier": 1.2},
        {"type": "add_text", "text": "New Hook!", "position": "top"},
        {"type": "add_watermark", "url": "logo.png"}
    ]
}
```

---

## **11. Webhook Integration**

### **Get Notifications on Completion**
```bash
POST /generate-video
{
    "idea": "Your idea",
    "webhook_url": "https://yourserver.com/webhook"
}

# Your server will receive:
POST https://yourserver.com/webhook
{
    "event": "video.completed",
    "job_id": "abc123",
    "video_url": "...",
    "upload_links": {...}
}
```

---

## **12. API Rate Limiting**

### **Tier System**
```
Free Tier: 5 videos/day
Starter: 50 videos/day ($9.99/month)
Pro: 500 videos/day ($49.99/month)
Enterprise: Unlimited (Custom pricing)
```

---

## **Performance Tips**

### **1. Batch Processing**
```python
# Generate multiple videos efficiently
for ideas in batch_of_ideas:
    tasks.append(generate_video_async(idea))
results = await asyncio.gather(*tasks)
```

### **2. Cache Results**
```python
# Cache trending data, scripts, etc.
redis_client.set(f"script:{idea}", script, ex=3600)
```

### **3. Optimize Images**
```python
# Compress video before upload
ffmpeg -i input.mp4 -vf scale=1080:1920 -c:v libx264 -preset faster output.mp4
```

### **4. Use CDN**
- Upload videos to CloudFlare/AWS CloudFront
- Reduces upload time
- Better distribution

---

## **Security Best Practices**

### **1. API Key Rotation**
```bash
# Rotate API keys monthly
# Keep old keys for 24 hours as backup
```

### **2. Rate Limiting**
```python
# Add to FastAPI:
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)

@app.post("/generate-video")
@limiter.limit("5/minute")
async def generate_video(request):
    pass
```

### **3. CORS Configuration**
```python
# Restrict to your domain only
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
)
```

---

## **Troubleshooting Advanced Features**

### **High Latency?**
- Deploy to region closer to users
- Upgrade to GPU instance
- Use caching layer

### **Videos Look Worse?**
- Check Kling AI quality settings
- Increase resolution
- Use "cinematic" style instead

### **Upload Rate Limited?**
- Spread uploads across accounts
- Use schedule feature
- Implement backoff strategy

---

## **Integration Examples**

### **Discord Bot**
```python
@bot.command()
async def generate_viral(ctx, *, idea):
    response = await create_video(idea)
    await ctx.send(f"✅ Video generating: {response['job_id']}")
```

### **Telegram Bot**
```python
@dp.message_handler(commands=['create'])
async def cmd_create(message: types.Message):
    job_id = await generate_video(message.text)
    await message.reply(f"Video: {job_id}")
```

### **WhatsApp Integration**
```python
# Send video ideas via WhatsApp
# Receive upload links automatically
```

---

**Master advanced features and unlock 10/10+ results! 🚀**
