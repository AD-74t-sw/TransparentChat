@echo off

>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"

if '%errorlevel%' NEQ '0' (
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
    
    REM
    set SHOW_CONSOLE=True
    if exist ".env" (
        for /f "tokens=1,2 delims==" %%a in ('findstr /i "^SHOW_CONSOLE=" .env') do set %%a=%%b
    )
    
    REM
    if exist ".venv\Scripts\python.exe" (
        if /i "%SHOW_CONSOLE%"=="False" (
            start "" ".venv\Scripts\pythonw.exe" -m Windows.main
            exit
        ) else (
            ".venv\Scripts\python.exe" -m Windows.main
            pause
        )
    ) else (
        if /i "%SHOW_CONSOLE%"=="False" (
            start "" pythonw -m Windows.main
            exit
        ) else (
            python -m Windows.main
            pause
        )
    )
