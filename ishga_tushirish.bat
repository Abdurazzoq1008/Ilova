@echo off
chcp 65001 >nul
cd /d "%~dp0"
title Gul Do'koni Ilovasi

echo ======================================================
echo    🌸 GUL DO'KONI ILOVASI ISHGA TUSHIRILMOQDA...
echo ======================================================
echo.

set "PY_EXE=C:\Users\Saidovs\AppData\Local\Programs\Python\Python314\python.exe"

if exist "%PY_EXE%" (
    "%PY_EXE%" main.py
) else (
    python main.py
)

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ------------------------------------------------------
    echo [XATOLIK] Ilova ishlashida xatolik yuz berdi!
    echo Iltimos, yuqoridagi xatoni o'qing.
    echo ------------------------------------------------------
    pause
)
