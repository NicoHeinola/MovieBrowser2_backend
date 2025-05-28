REM Ensure this script is run from the project root directory.

REM Path to the virtual environment activation script
set "VenvActivateScript=.\.venv\Scripts\activate.bat"

REM Check if virtual environment exists
if not exist "%VenvActivateScript%" (
    echo ERROR: Virtual environment not found at %VenvActivateScript%.
    echo Please create it first using 'python -m venv venv'.
    goto :eof
)

echo Attempting to activate virtual environment...
call "%VenvActivateScript%"
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment.
    goto :eof
)
echo Virtual environment activated.

REM Set environment variables (if your app relies on them and they aren't in a .env file loaded by Python)
REM set ENVIRONMENT=development
REM set PYTHONPATH=%CD%

echo Running database migrations...
alembic upgrade head
if errorlevel 1 (
    echo ERROR: Alembic migrations failed.
    goto :eof
)

echo Running seeders...
python run_seeders.py
if errorlevel 1 (
    echo ERROR: Seeders script failed.
    goto :eof
)

echo Starting FastAPI application with Uvicorn in the background...
echo The application will run at http://localhost:8000 (or the configured host/port).
echo To stop the server, you may need to find and kill the Uvicorn/Python process (e.g., via Task Manager).

REM Start Uvicorn in the background
REM Ensure uvicorn is installed (pip install uvicorn[standard]) if not in requirements.txt
start "MovieBrowserBackend" /B pythonw -m uvicorn main:app --host 0.0.0.0 --port 8000

if errorlevel 1 (
    echo ERROR: Failed to start Uvicorn.
    goto :eof
)

echo Uvicorn server started in the background. This script will now exit.

:eof
REM Optional: Deactivate virtual environment if script is kept open or for cleanup
REM if defined VIRTUAL_ENV (
REM     echo Deactivating virtual environment...
REM     call .\venv\Scripts\deactivate.bat
REM )
