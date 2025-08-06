@echo off
echo 🔥 WORDPRESS AUTOMATION BATCH RUNNER 🔥
echo ======================================

REM Kích hoạt môi trường Python
cd /d "D:\duanmoi"
call .venv\Scripts\activate.bat

REM Kiểm tra file cấu hình
if not exist ".env" (
    echo ❌ Không tìm thấy file .env! Vui lòng tạo file .env với cấu hình cần thiết.
    pause
    exit /b 1
)

if not exist "creds.json" (
    echo ❌ Không tìm thấy file creds.json! Vui lòng tải Google Service Account credentials.
    pause
    exit /b 1
)

REM Chạy chương trình chính
echo 🚀 Bắt đầu xử lý...
python main.py batch

echo.
echo ✅ Hoàn thành! Kiểm tra Google Sheet để xem kết quả.
pause
