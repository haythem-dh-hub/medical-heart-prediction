@echo off
title MediSpark AI - Installer
color 0A

echo.
echo  ============================================
echo    MediSpark AI - Auto Installer
echo    Massive Medical Data Analysis Platform
echo  ============================================
echo.

:: Check if py is available
py --version >nul 2>&1
if errorlevel 1 (
    echo  [ERROR] Python not found.
    echo  Please install Python 3.12+ from https://python.org
    echo  Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

echo  [1/4] Creating virtual environment...
py -m venv .venv
if errorlevel 1 (
    echo  [ERROR] Failed to create virtual environment.
    pause
    exit /b 1
)

echo  [2/4] Activating virtual environment...
call .venv\Scripts\activate.bat

echo  [3/4] Upgrading pip...
python -m pip install --upgrade pip --quiet

echo  [4/4] Installing dependencies (this may take a few minutes)...
pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo  [ERROR] Some packages failed to install.
    echo  Check your internet connection and try again.
    pause
    exit /b 1
)

echo.
echo  ============================================
echo    Installation complete!
echo    Run "run.bat" to launch the app.
echo  ============================================
echo.
pause