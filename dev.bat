@echo off
setlocal

REM Set working directories
set BACKEND_DIR=backend
set FRONTEND_DIR=frontend

REM Help message
if "%1"=="" (
    echo Usage: dev.bat [backend ^| frontend ^| both]
    exit /b 1
)

REM Start backend
if "%1"=="backend" (
    echo Starting FastAPI backend with reload...
    pushd %BACKEND_DIR%
    start cmd /k "uvicorn app.main:app --reload --port 8001"
    popd
    exit /b
)

REM Start frontend
if "%1"=="frontend" (
    echo Starting frontend...
    pushd %FRONTEND_DIR%
    start cmd /k "npm run dev"
    popd
    exit /b
)

REM Start both
if "%1"=="both" (
    echo Starting both backend and frontend...
    pushd %BACKEND_DIR%
    start cmd /k "uvicorn app.main:app --reload --port 8001"
    popd
    pushd %FRONTEND_DIR%
    start cmd /k "npm run dev"
    popd
    exit /b
)

echo Invalid option: %1
echo Usage: dev.bat [backend ^| frontend ^| both]
exit /b 1
