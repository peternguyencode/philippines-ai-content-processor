@echo off
echo 🎛️ WORDPRESS AUTOMATION - CUSTOMIZATION TOOL 🎛️
echo ================================================

REM Kích hoạt môi trường Python
cd /d "D:\duanmoi"
call .venv\Scripts\activate.bat

REM Chạy công cụ tùy chỉnh
python customize.py

pause
