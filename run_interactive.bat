@echo off
echo 🎮 WORDPRESS AUTOMATION INTERACTIVE MODE 🎮
echo ==========================================

REM Kích hoạt môi trường Python
cd /d "D:\duanmoi"
call .venv\Scripts\activate.bat

REM Chạy chế độ tương tác
python main.py

pause
