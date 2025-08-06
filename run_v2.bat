@echo off
echo 🚀 WordPress Automation V2 - Enhanced Runner
echo ===========================================
echo.

REM Kích hoạt virtual environment
call venv\Scripts\activate.bat

echo 🔄 Entering V2 directory...
cd v2

REM Chạy Enhanced Simple Runner V2
echo ✨ Starting Enhanced Simple Runner V2...
python enhanced_simple_runner.py

REM Quay lại thư mục gốc
cd ..

REM Giữ cửa sổ mở
echo.
echo ✅ Enhanced Runner V2 finished
pause
