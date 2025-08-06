@echo off
echo 🚀 CSV AI PROCESSING PIPELINE
echo ========================================
echo.
echo Chọn chế độ xử lý:
echo 1. Test mode (2 posts, delay 5s)
echo 2. Small batch (10 posts, delay 5s) 
echo 3. Full batch (86 posts, delay 5s)
echo 4. Custom mode
echo.
set /p choice="Nhập lựa chọn (1-4): "

if %choice%==1 (
    echo 🧪 Running test mode...
    python test_csv_processor.py
) else if %choice%==2 (
    echo 📊 Running small batch...
    python csv_ai_processor.py ./data/posts.csv 10 5.0
) else if %choice%==3 (
    echo 🔥 Running full batch... 
    echo ⚠️  This will take about 72 minutes and cost ~$0.17
    set /p confirm="Are you sure? (y/n): "
    if /i "%confirm%"=="y" (
        python csv_ai_processor.py ./data/posts.csv 86 5.0
    )
) else if %choice%==4 (
    set /p limit="Number of posts: "
    set /p delay="Delay between requests (seconds): "
    echo 🔄 Running custom batch...
    python csv_ai_processor.py ./data/posts.csv %limit% %delay%
) else (
    echo ❌ Invalid choice
)

echo.
pause
