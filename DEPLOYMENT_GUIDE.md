## 🚀 **Deployment Guide - AI Viral Video System**

### **Complete Setup Instructions**

---

## **Windows Setup (Step-by-Step)**

### **1. Install Python**
- Download Python 3.10+ from https://www.python.org/
- ✅ Check "Add Python to PATH"
- Verify: Open PowerShell → `python --version`

### **2. Install PostgreSQL**
- Download from https://www.postgresql.org/
- Run installer (use default settings)
- Note username/password (default: postgres)

### **3. Create Database**
```bash
# Open PostgreSQL console
psql -U postgres

# Create database
CREATE DATABASE viral_videos;
\q
```

### **4. Clone/Setup Project**
```bash
cd Desktop
mkdir "ai viral videos"
cd "ai viral videos"

# Download all files from this project
```

### **5. Run Setup**
```bash
# Double-click setup.bat
# OR in PowerShell:
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### **6. Configure Environment**
```bash
# Copy template
copy .env.example .env

# Edit .env with your API keys
notepad .env
```

### **7. Start Server**
```bash
python main.py
```

**Access:**
- API Docs: http://localhost:8000/docs
- Web UI: http://localhost:8000/ui

---

## **Linux/Mac Setup**

### **1. Install Python & PostgreSQL**
```bash
# Mac (using Homebrew)
brew install python@3.11
brew install postgresql

# Linux (Ubuntu)
sudo apt-get install python3.11 python3.11-venv
sudo apt-get install postgresql postgresql-contrib
```

### **2. Create Database**
```bash
createdb viral_videos
```

### **3. Setup Project**
```bash
chmod +x setup.sh
./setup.sh
```

### **4. Configure & Run**
```bash
cp .env.example .env
nano .env  # Edit with your keys

python main.py
```

---

## **API Keys Setup Guide**

### **A. Kling AI (Best 3D Video Generation) ⭐**

1. Go to: https://www.klingai.com/
2. Sign up → Verify email
3. Go to Dashboard → API Keys
4. Create new API key
5. Copy and paste into `.env`:
   ```
   KLING_AI_KEY=your_key_here
   ```

**Pricing:** 
- Free tier: 10 videos/month
- Paid: $9.99+/month

---

### **B. Claude API (Script Generation)**

1. Go to: https://console.anthropic.com/
2. Sign up with email
3. Add payment method
4. Go to API Keys → Create new key
5. Copy into `.env`:
   ```
   ANTHROPIC_API_KEY=sk-ant-xxxxx
   ```

**Pricing:**
- Pay-as-you-go (~$0.003 per script)

---

### **C. ElevenLabs (Voiceover)**

1. Go to: https://elevenlabs.io/
2. Sign up → Verify email
3. Dashboard → API Keys
4. Copy key into `.env`:
   ```
   ELEVENLABS_API_KEY=xxxxx
   ```

**Pricing:**
- Free tier: 10,000 characters/month
- Paid: $5+/month

---

### **D. TikTok API**

1. Go to: https://developers.tiktok.com/
2. Sign up → Verify
3. Create Developer Account
4. Go to: https://developer.tiktok.com/console/apps
5. Create new app
6. Get Access Token (requires approval)
7. Add to `.env`:
   ```
   TIKTOK_ACCESS_TOKEN=xxxxx
   ```

**Note:** May take 24-48 hours for approval

---

### **E. Instagram API**

1. Go to: https://developers.facebook.com/
2. Create account → Verify
3. My Apps → Create App
4. Choose "Consumer" type
5. Get to App Dashboard
6. Go to Roles → Admins → Add your account
7. Get Access Token (Graph API)
8. Add to `.env`:
   ```
   INSTAGRAM_ACCESS_TOKEN=xxxxx
   ```

---

### **F. YouTube API**

1. Go to: https://console.cloud.google.com/
2. Create new project
3. Enable "YouTube Data API v3"
4. Create OAuth 2.0 credentials (Desktop app)
5. Download JSON file
6. Add path to `.env`:
   ```
   YOUTUBE_CREDENTIALS=/path/to/credentials.json
   ```

---

## **Database Setup**

### **PostgreSQL Configuration**

```bash
# Check PostgreSQL is running
pg_isready

# Connect to database
psql -U postgres -d viral_videos

# Verify tables created
\dt
```

### **Connection String Format**
```
postgresql://username:password@localhost:5432/viral_videos
```

Update in `.env`:
```
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/viral_videos
```

---

## **Testing the System**

### **1. Test API Health**
```bash
curl http://localhost:8000/
```

Expected response:
```json
{
  "status": "healthy",
  "service": "AI Viral Video Generator",
  "version": "1.0.0"
}
```

### **2. Generate Test Video**
```bash
curl -X POST http://localhost:8000/generate-video \
  -H "Content-Type: application/json" \
  -d '{
    "idea": "A funny cat video",
    "platforms": ["tiktok"],
    "auto_upload": false
  }'
```

### **3. Check Status**
```bash
curl http://localhost:8000/status/{job_id}
```

---

## **Troubleshooting**

### **Issue: "ModuleNotFoundError: No module named 'fastapi'"**
```bash
# Solution: Install dependencies again
pip install -r requirements.txt
```

### **Issue: "Database connection refused"**
```bash
# Solution: Start PostgreSQL
# Windows: Services → PostgreSQL → Start
# Mac: brew services start postgresql
# Linux: sudo systemctl start postgresql
```

### **Issue: "Invalid API key"**
- Check `.env` file has correct key
- Verify API is enabled in provider dashboard
- Check rate limits haven't been exceeded

### **Issue: Upload fails to TikTok/Instagram**
- Verify API token is current (tokens expire)
- Check account hasn't been banned
- Ensure video format is supported

---

## **Production Deployment**

### **Deploy to Heroku**

1. Install Heroku CLI
2. Create `Procfile`:
   ```
   web: uvicorn main:app --host=0.0.0.0 --port=${PORT}
   ```

3. Deploy:
   ```bash
   heroku login
   heroku create your-app-name
   git push heroku main
   ```

### **Deploy to AWS/DigitalOcean**

1. Use Docker:
   ```dockerfile
   FROM python:3.11
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD ["python", "main.py"]
   ```

2. Run on server:
   ```bash
   docker build -t viral-video-system .
   docker run -p 8000:8000 viral-video-system
   ```

---

## **Performance Optimization**

### **For High Volume**

1. **Use Redis for caching**
   ```
   REDIS_URL=redis://localhost:6379
   ```

2. **Add Celery for async tasks**
   ```bash
   pip install celery
   ```

3. **Use GPU acceleration**
   - Deploy on GPU-enabled instance
   - Configure Kling AI for faster rendering

4. **Load balancing**
   - Deploy multiple instances
   - Use nginx for routing

---

## **Monitoring & Logging**

### **Check Logs**
```bash
# Real-time logs
tail -f logs/system.log

# All errors
grep ERROR logs/system.log

# Specific job
grep {job_id} logs/system.log
```

### **Performance Monitoring**
```bash
# Monitor API usage
watch curl http://localhost:8000/stats

# Database queries
psql viral_videos -c "SELECT COUNT(*) FROM video_jobs;"
```

---

## **Support Resources**

- **Kling AI Docs**: https://www.klingai.com/docs
- **Claude API Docs**: https://docs.anthropic.com/
- **ElevenLabs Docs**: https://docs.elevenlabs.io/
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **PostgreSQL Docs**: https://www.postgresql.org/docs/

---

## **Final Checklist**

- [ ] Python 3.10+ installed
- [ ] PostgreSQL installed & running
- [ ] All API keys added to `.env`
- [ ] Virtual environment activated
- [ ] Dependencies installed
- [ ] Database created
- [ ] Server starts without errors
- [ ] API responds at localhost:8000
- [ ] Web UI loads at localhost:8000/ui
- [ ] Test video generates successfully

---

**Your system is ready! 🚀**

Generate your first viral video now! 🎬✨
