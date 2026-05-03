@echo off
REM Smart Election Assistant - Setup Script (Windows)
REM This script automates the setup process for both backend and frontend

echo.
echo ================================
echo Smart Election Assistant Setup
echo ================================
echo.

REM Check Python
echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.8+
    exit /b 1
)
for /f "tokens=*" %%A in ('python --version') do echo ✅ Python found: %%A
echo.

REM Check Node.js
echo Checking Node.js installation...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed. Please install Node.js 16+
    exit /b 1
)
for /f "tokens=*" %%A in ('node --version') do echo ✅ Node.js found: %%A
echo.

echo Setting up BACKEND...
echo ====================
cd backend

echo Creating virtual environment...
python -m venv venv
echo ✅ Virtual environment created

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing Python dependencies...
pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt >nul 2>&1
echo ✅ Dependencies installed

echo Initializing database...
python -c "from app.database.db_setup import init_db; init_db()"
echo ✅ Database initialized

echo.
echo Backend setup complete!
echo To start backend server:
echo   cd backend
echo   venv\Scripts\activate
echo   python -m uvicorn app.main:app --reload
echo.

cd ..\frontend

echo ================================
echo Setting up FRONTEND...
echo ================================

echo Installing Node.js dependencies...
call npm install >nul 2>&1
echo ✅ Dependencies installed

echo.
echo Frontend setup complete!
echo To start frontend server:
echo   cd frontend
echo   npm start
echo.

echo ================================
echo Setup Complete! 🎉
echo ================================
echo.
echo Next steps:
echo 1. Add API keys to backend\.env
echo 2. In Terminal 1: cd backend ^&^& venv\Scripts\activate ^&^& python -m uvicorn app.main:app --reload
echo 3. In Terminal 2: cd frontend ^&^& npm start
echo 4. Open http://localhost:3000 in your browser
echo.
echo API Documentation: http://localhost:8000/docs
echo.
pause
