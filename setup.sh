#!/bin/bash

# Smart Election Assistant - Setup Script
# This script automates the setup process for both backend and frontend

echo "================================"
echo "Smart Election Assistant Setup"
echo "================================"
echo ""

# Check Python
echo "Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON=python3
elif command -v python &> /dev/null; then
    PYTHON=python
else
    echo "❌ Python is not installed. Please install Python 3.8+"
    exit 1
fi

echo "✅ Python found: $($PYTHON --version)"
echo ""

# Check Node.js
echo "Checking Node.js installation..."
if command -v node &> /dev/null; then
    echo "✅ Node.js found: $(node --version)"
else
    echo "❌ Node.js is not installed. Please install Node.js 16+"
    exit 1
fi

echo ""
echo "Setting up BACKEND..."
echo "===================="

# Create backend virtual environment
cd backend

echo "Creating virtual environment..."
$PYTHON -m venv venv

# Activate virtual environment
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

echo "✅ Virtual environment created"

# Install dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip > /dev/null
pip install -r requirements.txt > /dev/null
echo "✅ Dependencies installed"

# Initialize database
echo "Initializing database..."
$PYTHON -c "from app.database.db_setup import init_db; init_db()"
echo "✅ Database initialized"

echo ""
echo "Backend setup complete!"
echo "To start backend server:"
echo "  cd backend"
echo "  source venv/bin/activate  # On Windows: venv\\Scripts\\activate"
echo "  python -m uvicorn app.main:app --reload"
echo ""

# Setup Frontend
cd ../frontend

echo "================================"
echo "Setting up FRONTEND..."
echo "================================"

echo "Installing Node.js dependencies..."
npm install > /dev/null 2>&1
echo "✅ Dependencies installed"

echo ""
echo "Frontend setup complete!"
echo "To start frontend server:"
echo "  cd frontend"
echo "  npm start"
echo ""

echo "================================"
echo "Setup Complete! 🎉"
echo "================================"
echo ""
echo "Next steps:"
echo "1. Add API keys to backend/.env"
echo "2. In Terminal 1: cd backend && source venv/bin/activate && python -m uvicorn app.main:app --reload"
echo "3. In Terminal 2: cd frontend && npm start"
echo "4. Open http://localhost:3000 in your browser"
echo ""
echo "API Documentation: http://localhost:8000/docs"
echo ""
