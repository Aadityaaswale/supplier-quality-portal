@echo off
REM ==============================================================================
REM Run Local Development Server
REM Student: AADITYA ASWALE (23102B0044)
REM ==============================================================================

cd /d "%~dp0..\backend"
echo Starting Supplier Quality Review Portal...
call venv\Scripts\activate.bat
python manage.py runserver 127.0.0.1:8000
pause
