@echo off
cd /d "%~dp0"
echo Checking AI Digital Pet project files...
for %%F in (index.html style.css manifest.json icon.svg server.py js\app.js assets\buddy.svg assets\kitty.svg icons\icon-192.svg icons\icon-512.svg icons\maskable-512.svg RUN_APP.bat README.md .env.example sw.js) do (
 if exist "%%F" (echo [OK] %%F) else (echo [MISSING] %%F)
)
echo.
pause
