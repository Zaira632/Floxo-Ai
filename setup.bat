@echo off
echo 🎬 AI Viral Video System - Startup Script
echo =========================================
echo.

echo ✓ Checking Python...
python --version

echo ✓ Creating virtual environment...
python -m venv venv

echo ✓ Activating virtual environment...
call venv\Scripts\activate

echo ✓ Installing dependencies...
pip install -r requirements.txt

echo.
echo ✓ Setup complete!
echo.
echo 📝 Next steps:
echo   1. Copy .env.example to .env
echo   2. Add your API keys to .env
echo   3. Setup PostgreSQL database
echo   4. Run: python main.py
echo.
echo 🚀 To start the server, run:
echo   python main.py
echo.
echo 📖 Visit http://localhost:8000/docs for API documentation
echo.
pause
