@echo off
setlocal enabledelayedexpansion

set "SRC_DIR=%~dp0"
set "DEST_DIR=%~dp0arXiv-submission\figure"

if not exist "%DEST_DIR%" (
    mkdir "%DEST_DIR%"
    echo Created directory: %DEST_DIR%
)

set "COUNT=0"

for %%f in ("%SRC_DIR%*.pdf") do (
    if exist "%%f" (
        copy /Y "%%f" "%DEST_DIR%" >nul
        echo Copied: %%~nxf
        set /a COUNT+=1
    )
)

echo.
echo Total files copied: %COUNT%
echo Destination: %DEST_DIR%
pause
