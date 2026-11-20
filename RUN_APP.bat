@echo off
title Buddy ^& Kitty - Living AI Digital Pet Game
cd /d "%~dp0"

echo ==========================================================
echo       BUDDY ^& KITTY -- Living AI Digital Pet Game
echo ==========================================================
echo.
echo Starting application...

REM Check if Python is available
where python >nul 2>nul
if %errorlevel% equ 0 (
    echo [OK] Python detected. Starting local server...
    start "" http://localhost:8000
    python server.py
) else (
    echo [NOTE] Python not found in PATH. Opening game directly in your browser...
    start "" index.html
    echo.
    echo Game launched in browser!
    pause
)
