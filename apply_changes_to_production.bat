@echo off
REM Script to apply changes to the production environment

REM Define source and destination directories
set "SOURCE_DIR=%~dp0"
REM Remove trailing backslash from SOURCE_DIR if present, for robocopy robustness
if "%SOURCE_DIR:~-1%"=="\" set "SOURCE_DIR=%SOURCE_DIR:~0,-1%"

set "DEST_DIR=%USERPROFILE%\Desktop\ProductionCodes\MovieBrowser2_backend"

echo Copying project files from "%SOURCE_DIR%" to "%DEST_DIR%"...

REM Create destination directory if it doesn't exist
if not exist "%DEST_DIR%" (
    echo Creating destination directory: %DEST_DIR%
    mkdir "%DEST_DIR%"
    if errorlevel 1 (
        echo ERROR: Failed to create destination directory. Exiting.
        goto :eof
    )
)

REM Use robocopy to mirror files, excluding specified directories and files
REM /MIR :: MIRror a directory tree (equivalent to /E plus /PURGE).
REM /XD :: eXclude Directories matching given names/paths.
REM /XF :: eXclude Files matching given names/paths.
robocopy "%SOURCE_DIR%" "%DEST_DIR%" /MIR /XD "database_instance" "__pycache__" ".git" ".vscode" /XF "uvicorn.log" "uvicorn.err" "apply_changes_to_production.bat"

REM Check Robocopy error level
REM Error levels less than 8 indicate success or minor issues (like extra files handled by /PURGE)
if errorlevel 8 (
    echo ERROR: Robocopy encountered significant errors during the copy process.
    echo Production deployment might be incomplete or corrupted.
    echo Please check the output above for details.
) else if errorlevel 4 (
    echo WARNING: Robocopy completed, but some files were mismatched or some extra files/directories were detected and handled.
    echo Review Robocopy output if necessary.
) else if errorlevel 2 (
    echo INFO: Robocopy completed. Some extra files/directories were detected and handled by /PURGE.
) else if errorlevel 1 (
    echo INFO: Files were copied successfully.
) else if errorlevel 0 (
    echo INFO: No files needed to be copied. Source and destination are likely identical (considering exclusions).
)

echo.
echo Deployment script finished.
echo Please check "%DEST_DIR%" for the copied files.

:eof
