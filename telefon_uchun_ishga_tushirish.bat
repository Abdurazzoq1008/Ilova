@echo off
chcp 65001 >nul
cd /d "%~dp0"
title Melfis Flowers - Telefon Ilovasi Serveri

echo ======================================================================
echo       🌸 MELFIS FLOWERS SAMARQAND — TELEFON ILOVASI 🌸
echo ======================================================================
echo.
echo Telefoningizdan bir xil Wi-Fi tarmog'iga ulangan holda:
echo.
echo 📱 Telefon brauzerida ushbu havolani oching:
echo.
echo        http://192.168.2.3:5000
echo.
echo (Yoki papkadagi "telefon_uchun_qr.png" QR-kodini kamerangiz bilan skanerlang)
echo.
echo ----------------------------------------------------------------------
echo Server ishlamoqda... Oynani yopmang!
echo ======================================================================
echo.

"C:\Users\Saidovs\AppData\Local\Programs\Python\Python314\python.exe" mobile_app.py
pause

