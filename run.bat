@echo off
title MediSpark AI
color 0A

echo.
echo  ============================================
echo    MediSpark AI - Launching...
echo  ============================================
echo.

:: Check if .venv exists
if not exist ".venv\Scripts\activate.bat" (
    echo  [ERROR] Virtual environment not found.
    echo  Please run install.bat first.
    pause
    exit /b 1
)

call .venv\Scripts\activate.bat

:: Check if data folder exists
if not exist "data\archive" (
    echo  [WARNING] data\archive folder not found.
    echo  Please add your Parquet dataset files to data\archive\
    echo.
)

echo  Starting MediSpark AI on http://localhost:8501
echo  Press Ctrl+C to stop the server.
echo.
streamlit run app.py
pause