@echo off
echo 🎮 WordPress Automation - Simple Runner
echo =====================================
echo.

REM Kích hoạt virtual environment
call venv\Scripts\activate.bat

REM Chạy Simple Runner
echo 🚀 Starting Simple Runner...
python simple_runner.py

REM Giữ cửa sổ mở
echo.
echo ✅ Simple Runner finished
pause
