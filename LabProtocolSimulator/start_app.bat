@echo off
echo Starting Chemical Engineering Lab Simulator...

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python 3.7 or higher.
    pause
    exit /b
)

:: Start the Streamlit app in the background
start /b cmd /c "python -m streamlit run app.py --server.port 5000"

:: Wait for the server to start (adjust sleep time as needed)
echo Waiting for server to start...
timeout /t 5 /nobreak >nul

:: Open Chrome browser at the local address
echo Opening browser...
start chrome http://localhost:5000

echo Application started. Close this window when you're done.
echo Press any key to close the application...
pause >nul

:: Find and kill the Python process
echo Stopping the application...
taskkill /f /im python.exe
echo Application stopped.
timeout /t 2 >nul