@echo off
echo 🔧 SETUP SAMPLE DATA 🔧
echo =======================

REM Kích hoạt môi trường Python
cd /d "D:\duanmoi"
call .venv\Scripts\activate.bat

REM Thiết lập dữ liệu mẫu
python main.py setup

echo.
echo ✅ Đã thiết lập dữ liệu mẫu! Kiểm tra Google Sheet.
pause
