@echo off
REM Helper script untuk menjalankan AWS Technical Document Generator dengan .env file (Windows)
REM Usage: run-with-env.bat

setlocal enabledelayedexpansion

echo ========================================
echo AWS Technical Document Generator
echo ========================================
echo.

REM Check if .env exists
if not exist .env (
    echo [ERROR] File .env tidak ditemukan!
    echo.
    echo Silakan copy dari template:
    echo   copy .env.example .env
    echo.
    echo Kemudian edit file .env dengan credentials Anda.
    exit /b 1
)

echo [OK] Loading configuration from .env...

REM Load .env file
for /f "usebackq tokens=1,* delims==" %%a in (.env) do (
    set "line=%%a"
    if not "!line:~0,1!"=="#" (
        set "%%a=%%b"
    )
)

REM Validate required variables
if "%AWS_ACCESS_KEY_ID%"=="" (
    echo [ERROR] AWS_ACCESS_KEY_ID tidak ditemukan di .env
    exit /b 1
)
if "%AWS_SECRET_ACCESS_KEY%"=="" (
    echo [ERROR] AWS_SECRET_ACCESS_KEY tidak ditemukan di .env
    exit /b 1
)
if "%AWS_DEFAULT_REGION%"=="" (
    echo [ERROR] AWS_DEFAULT_REGION tidak ditemukan di .env
    exit /b 1
)
if "%CUSTOMER_NAME%"=="" (
    echo [ERROR] CUSTOMER_NAME tidak ditemukan di .env
    exit /b 1
)
if "%PROJECT_NAME%"=="" (
    echo [ERROR] PROJECT_NAME tidak ditemukan di .env
    exit /b 1
)
if "%DOCUMENT_VERSION%"=="" (
    echo [ERROR] DOCUMENT_VERSION tidak ditemukan di .env
    exit /b 1
)

echo [OK] Configuration loaded successfully
echo.
echo   Customer: %CUSTOMER_NAME%
echo   Project: %PROJECT_NAME%
echo   Version: %DOCUMENT_VERSION%
echo   Region: %AWS_DEFAULT_REGION%
echo.

REM Step 1: Scan AWS resources
echo ========================================
echo Step 1: Scanning AWS resources...
echo ========================================
python scripts\scan-aws-resources.py "%AWS_ACCESS_KEY_ID%" "%AWS_SECRET_ACCESS_KEY%" "%AWS_DEFAULT_REGION%"

if errorlevel 1 (
    echo [ERROR] Scan failed
    exit /b 1
)

REM Find the latest scan file
for /f "delims=" %%i in ('dir /b /od aws-resources-*.json 2^>nul') do set SCAN_FILE=%%i

if "%SCAN_FILE%"=="" (
    echo [ERROR] Scan file tidak ditemukan
    exit /b 1
)

echo.
echo [OK] Scan completed: %SCAN_FILE%
echo.

REM Step 2: Generate document
echo ========================================
echo Step 2: Generating technical document...
echo ========================================
python scripts\generate-document.py "%SCAN_FILE%" "%CUSTOMER_NAME%" "%PROJECT_NAME%" "%DOCUMENT_VERSION%"

if errorlevel 1 (
    echo [ERROR] Document generation failed
    exit /b 1
)

echo.
echo ========================================
echo [OK] Process completed successfully!
echo ========================================

endlocal
