
@echo off
title COGNISYS - Your PC. Understood.

cd /d "%~dp0"

echo.
echo ========================================
echo          COGNISYS INTELLIGENCE
echo ========================================
echo.

if not exist ".venv\Scripts\python.exe" (
    echo ERROR: Python virtual environment not found!
    echo Please check the .venv folder.
    pause
    exit /b 1
)

echo Starting COGNISYS...
echo.

".venv\Scripts\python.exe" -m backend.app.collector.cognisys_runner

echo.
echo COGNISYS process has ended.
pause
