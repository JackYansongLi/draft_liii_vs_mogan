@echo off
chcp 65001 >nul
echo ==========================================
echo LaTeX Compilation Script for main_en.tex
echo ==========================================
echo.

if "%~1"=="clean" goto clean
if "%~1"=="compile" goto compile
if "%~1"=="all" goto all
if "%~1"=="help" goto help
if "%~1"=="" goto all

echo Unknown command: %~1
goto help

:help
echo Usage: build.bat [command]
echo.
echo Commands:
echo   compile    - Compile the LaTeX document
echo   clean      - Clean auxiliary files
echo   all        - Clean and compile (default)
echo   help       - Show this help message
echo.
goto end

:clean
echo Cleaning auxiliary files...
if exist *.aux del /q *.aux
if exist *.log del /q *.log
if exist *.out del /q *.out
if exist *.toc del /q *.toc
if exist *.bbl del /q *.bbl
if exist *.blg del /q *.blg
if exist *.synctex.gz del /q *.synctex.gz
if exist *.fdb_latexmk del /q *.fdb_latexmk
if exist *.fls del /q *.fls
if exist *.nav del /q *.nav
if exist *.snm del /q *.snm
if exist *.vrb del /q *.vrb
echo Clean complete.
echo.
goto end

:compile
echo Compiling main_en.tex...
echo.

echo [1/4] First pass...
pdflatex -interaction=nonstopmode -halt-on-error main_en.tex
if errorlevel 1 (
    echo [ERROR] Compilation failed on first pass!
    goto error
)

echo.
echo [2/4] Running BibTeX...
bibtex main_en
if errorlevel 1 (
    echo [WARNING] BibTeX returned errors, continuing...
)

echo.
echo [3/4] Second pass for references...
pdflatex -interaction=nonstopmode -halt-on-error main_en.tex
if errorlevel 1 (
    echo [ERROR] Compilation failed on third pass!
    goto error
)

echo.
echo [4/4] Final pass...
pdflatex -interaction=nonstopmode -halt-on-error main_en.tex
if errorlevel 1 (
    echo [ERROR] Compilation failed on final pass!
    goto error
)

echo.
echo ==========================================
echo Compilation successful!
echo Output: main_en.pdf
echo ==========================================
goto end

:all
call :clean
call :compile
goto end

:error
echo.
echo ==========================================
echo Compilation failed!
echo Please check main_en.log for details.
echo ==========================================
exit /b 1

:end
