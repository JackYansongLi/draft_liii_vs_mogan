@echo off
setlocal enabledelayedexpansion

echo Cleaning LaTeX temporary files...

REM Define the file extensions to be deleted
set extensions=aux log toc lof lot fls out fmt fot cb cb2 lb bbl bcf blg run.xml fdb_latexmk synctex.gz xdv thm nav snm vrb mp tikz dvi ps eps epsi

REM Loop through each extension and delete matching files
for %%e in (%extensions%) do (
    for /f "delims=" %%f in ('dir /b *.%%e 2^>nul') do (
        del "%%f"
        echo Deleted: %%f
    )
)

REM Delete PDF files (optional - comment out if you want to keep PDFs)
for /f "delims=" %%f in ('dir /b *.pdf 2^>nul') do (
    del "%%f"
    echo Deleted: %%f
)

echo.
echo Cleanup completed!
pause
