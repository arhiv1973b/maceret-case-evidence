@echo off
REM Auto-Sync Service for maceret-case-evidence
REM Runs continuously in background

setlocal enabledelayedexpansion

set SOURCE_DIR=C:\Users\arhiv\upload_archive
set LOG_FILE=C:\Users\arhiv\sync_log.txt
set CHECK_INTERVAL=300

echo [%date% %time%] Auto-sync service started >> "%LOG_FILE%"

:loop
cd /d "%SOURCE_DIR%"
git add -A 2>nul

REM Check if there are changes
git diff --staged --quiet
if %errorlevel% neq 0 (
    echo [%date% %time%] Committing changes... >> "%LOG_FILE%"
    git commit -m "Auto-sync: %date% %time%"
    
    git push origin main 2>>"%LOG_FILE%"
    if %errorlevel% neq 0 (
        echo [%date% %time%] Push failed, pulling... >> "%LOG_FILE%"
        git pull origin main --allow-unrelated-histories 2>>"%LOG_FILE%"
        git push origin main 2>>"%LOG_FILE%"
    ) else (
        echo [%date% %time%] Push successful >> "%LOG_FILE%"
    )
) else (
    echo [%date% %time%] No changes >> "%LOG_FILE%"
)

timeout /t %CHECK_INTERVAL% /nobreak >nul
goto loop
