@echo off

>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"

if '%errorlevel%' NEQ '0' (
    echo Solicitando permisos de administrador...
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
    echo Ejecutando script con permisos de administrador...
    cd ..
    
    if exist ".venv\Scripts\activate.bat" (
        call .venv\Scripts\activate.bat
        echo Entorno virtual activado.
    ) else (
        echo ADVERTENCIA: No se encontro el entorno virtual en .venv
    )
    
    python -m Windows.main
    pause
