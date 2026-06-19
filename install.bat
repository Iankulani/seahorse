@echo off
:: SeaHorse v3.0.0 - Windows Installation Script

setlocal enabledelayedexpansion

echo ============================================================
echo         SEA HORSE v3.0.0
echo         Windows Installation Script
echo ============================================================
echo.

:: Check Python
echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python 3.7+ from https://python.org/
    pause
    exit /b 1
)

for /f "tokens=2" %%a in ('python --version 2^>^&1') do set PY_VERSION=%%a
echo Python %PY_VERSION% found
echo.

:: Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip
echo.

:: Install requirements
echo Installing Python packages...
if exist requirements.txt (
    echo Installing from requirements.txt...
    python -m pip install -r requirements.txt
) else (
    echo Installing core packages...
    python -m pip install cryptography colorama requests psutil paramiko scapy python-whois qrcode pyshorteners Flask discord.py telethon slack-sdk selenium webdriver-manager dnspython pyOpenSSL
)
echo.

:: Create directories
echo Creating SeaHorse directories...
if not exist .seahorse mkdir .seahorse
cd .seahorse
mkdir payloads 2>nul
mkdir workspaces 2>nul
mkdir scans 2>nul
mkdir reports 2>nul
mkdir phishing_pages 2>nul
mkdir wordlists 2>nul
mkdir ssh_keys 2>nul
mkdir web_ui 2>nul
mkdir traffic_logs 2>nul
mkdir captured_credentials 2>nul
mkdir phishing_templates 2>nul
mkdir custom_phishing 2>nul
mkdir webhooks 2>nul
mkdir nikto_results 2>nul
mkdir time_history 2>nul
mkdir ssh_logs 2>nul
mkdir whatsapp_session 2>nul
mkdir signal_session 2>nul
cd ..
echo.

:: Verify installation
echo Verifying installation...
python requirements_check.py
echo.

echo ============================================================
echo         INSTALLATION COMPLETE!
echo         SEA HORSE v3.0.0 is ready!
echo ============================================================
echo.
echo To run SeaHorse:
echo   python seahorse.py
echo.
echo For web interface:
echo   Open http://localhost:8080
echo.
echo For help:
echo   Type 'help' in the SeaHorse terminal
echo.
echo Check dependencies:
echo   python requirements_check.py
echo.

pause