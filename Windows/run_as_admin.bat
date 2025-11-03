@echo off

>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"

if '%errorlevel%' NEQ '0' (
    if /i "%VERBOSE%"=="True" echo Requesting administrator permissions...
    goto UACPrompt
) else ( goto gotAdmin )

:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"
    "%temp%\getadmin.vbs"
    exit /B

:gotAdmin
    if exist "%temp%\getadmin.vbs" ( del "%temp%\getadmin.vbs" )
    pushd "%CD%"
    CD /D "%~dp0"

:run
    cd ..
    
    REM Load VERBOSE from .env file
    if exist ".env" (
        for /f "tokens=1,2 delims==" %%a in ('findstr /i "^VERBOSE=" .env') do set %%a=%%b
    )
    
    if /i "%VERBOSE%"=="True" echo Running script with administrator permissions...
    
    if exist ".venv\Scripts\activate.bat" (
        call .venv\Scripts\activate.bat
        if /i "%VERBOSE%"=="True" echo Virtual environment activated.
    ) else (
        if /i "%VERBOSE%"=="True" echo WARNING: Virtual environment not found in .venv
    )
    
    python -m Windows.main
    pause
