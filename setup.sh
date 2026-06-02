#!/bin/bash

echo "🎬 AI Viral Video System - Setup & Start"
echo "=========================================="
echo ""

echo "✓ Checking Python..."
python3 --version

echo "✓ Creating virtual environment..."
python3 -m venv venv

echo "✓ Activating virtual environment..."
source venv/bin/activate

echo "✓ Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "✓ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "   1. cp .env.example .env"
echo "   2. Edit .env and add your API keys"
echo "   3. Setup PostgreSQL database"
echo "   4. Run: python main.py"
echo ""
echo "🚀 To start the server now:"
echo "   source venv/bin/activate"
echo "   python main.py"
echo ""
