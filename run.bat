@echo off
REM Shopzy - Complete Application Startup Script (Windows)
REM This script starts all 7 microservices + API Gateway + Frontend
REM Usage: run.bat

setlocal enabledelayedexpansion

REM Colors won't work on all Windows versions, so we'll use simple output
echo.
echo ================================================================
echo   Shopzy - Microservices E-Commerce Platform
echo   Starting Complete Application
echo ================================================================
echo.

REM Check for required commands
echo Checking prerequisites...

python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed
    exit /b 1
)
echo OK: Python found

node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed
    exit /b 1
)
echo OK: Node.js found

npm --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: npm is not installed
    exit /b 1
)
echo OK: npm found

echo.
echo Starting all services...
echo.

REM Function to start a service
setlocal
set "services[0]=product-service:8001:Product Service"
set "services[1]=customer-service:8002:Customer Service"
set "services[2]=inventory-service:8003:Inventory Service"
set "services[3]=order-service:8004:Order Service"
set "services[4]=payment-service:8005:Payment Service"
set "services[5]=notification-service:8006:Notification Service"
set "services[6]=api-gateway:8000:API Gateway"

for /l %%i in (0,1,6) do (
    for /f "tokens=1,2,3 delims=:" %%a in ("!services[%%i]!") do (
        set "service_name=%%a"
        set "port=%%b"
        set "description=%%c"

        echo Starting !description! ^(Port !port!^)...

        cd services\!service_name!

        if not exist "venv" (
            echo   Creating virtual environment...
            python -m venv venv
        )

        call venv\Scripts\activate.bat

        if not exist "installed.marker" (
            echo   Installing dependencies...
            pip install -q -r requirements.txt
            type nul > installed.marker
        )

        start "Shopzy - !description!" python -m uvicorn app.main:app --host 0.0.0.0 --port !port! --reload

        cd ..\..
        timeout /t 1 /nobreak >nul
    )
)

REM Start Frontend
echo Starting Frontend (Port 5173)...
cd frontend

if not exist "node_modules" (
    echo   Installing npm dependencies...
    call npm install -q
)

start "Shopzy - Frontend" npm run dev
cd ..

timeout /t 3 /nobreak >nul

echo.
echo ================================================================
echo   All Services Started Successfully!
echo ================================================================
echo.
echo Frontend: http://localhost:5173
echo.
echo API Endpoints:
echo   - API Gateway:       http://localhost:8000/docs
echo   - Product Service:   http://localhost:8001/docs
echo   - Customer Service:  http://localhost:8002/docs
echo   - Inventory Service: http://localhost:8003/docs
echo   - Order Service:     http://localhost:8004/docs
echo   - Payment Service:   http://localhost:8005/docs
echo   - Notification Svc:  http://localhost:8006/docs
echo.
echo Press any key to exit...
pause >nul
