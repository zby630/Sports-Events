@echo off
setlocal enabledelayedexpansion
title Sports Events - Start Website

set "PROJ=C:\Users\Administrator\Documents\Codex\2026-11-02\ju\outputs\Sports-Events"
set "DD=C:\Users\Administrator\AppData\Local\Programs\DockerDesktop\Docker Desktop.exe"

echo ============================================
echo   Campus Sports Events - Start Website
echo ============================================

tasklist /FI "IMAGENAME eq Docker Desktop.exe" 2>nul | find /I "Docker Desktop.exe" >nul
if errorlevel 1 (
    echo [1/4] Starting Docker Desktop ...
    if exist "%DD%" (
        start "" "%DD%"
    ) else (
        echo Docker Desktop not found:
        echo %DD%
        pause
        exit /b 1
    )
) else (
    echo [1/4] Docker Desktop is already running.
)

echo [2/4] Waiting for Docker engine ...
set /a n=0
:waitdocker
docker info >nul 2>&1
if not errorlevel 1 goto dockerok
set /a n+=1
if !n! geq 60 (
    echo Docker engine did not start within 3 minutes.
    echo Please open Docker Desktop manually and run this file again.
    pause
    exit /b 1
)
timeout /t 3 /nobreak >nul
goto waitdocker
:dockerok
echo       Docker engine is ready.

echo [3/4] Starting containers ...
cd /d "%PROJ%"
docker compose up -d
if errorlevel 1 (
    echo Failed to start containers. Run: docker compose logs
    pause
    exit /b 1
)

echo [4/4] Waiting for website ...
set /a n=0
:waitweb
curl -s -o nul --max-time 3 http://localhost:3000/
if not errorlevel 1 goto webok
set /a n+=1
if !n! geq 60 (
    echo Website did not respond in time. Check: docker compose logs
    pause
    exit /b 1
)
timeout /t 2 /nobreak >nul
goto waitweb
:webok

start "" http://localhost:3000
echo.
echo Website : http://localhost:3000
echo Accounts: admin / teacher1 / student1
echo Password: 123456
echo.
pause
