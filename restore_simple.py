#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RESTORE TO SIMPLE VERSION - Khôi phục về phiên bản đơn giản
Tool đơn giản nhất để chạy AI Content Processing
"""

import os
import subprocess


def restore_simple_version():
    """Khôi phục về tool đơn giản ban đầu"""
    print("🔄 KHÔI PHỤC VỀ PHIÊN BẢN ĐỎN GIẢN")
    print("=" * 50)

    print("✅ Tool đơn giản nhất của bạn:")
    print("   📄 ai_content_processor.py - Tool gốc hoạt động tốt")
    print("   📄 config.py - Cấu hình OpenAI API")
    print("   📄 interactive_menu.py - Menu đơn giản")
    print()

    print("🎯 CÁCH CHẠY ĐƠN GIẢN NHẤT:")
    print("   1. python ai_content_processor.py")
    print("   2. Chọn chức năng từ menu")
    print("   3. Chạy AI processing")
    print()

    print("🚀 HOẶC CHẠY TRỰC TIẾP:")
    print("   python ai_content_processor.py batch 5 1.0")
    print("   (Xử lý 5 posts, delay 1 giây)")
    print()

    # Kiểm tra files cần thiết
    required_files = ["ai_content_processor.py", "config.py"]

    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)

    if missing_files:
        print(f"❌ THIẾU FILES: {', '.join(missing_files)}")
        return False
    else:
        print("✅ TẤT CẢ FILES CẦN THIẾT ĐÃ CÓ")

    return True


def run_simple_test():
    """Chạy test đơn giản"""
    print("\n🧪 CHẠY TEST ĐƠN GIẢN:")

    try:
        # Test import
        print("   ✓ Testing imports...")
        result = subprocess.run(
            [
                "python",
                "-c",
                "from ai_content_processor import AIContentProcessor; print('✅ Import OK')",
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )

        if result.returncode == 0:
            print("   ✅ All imports working")
        else:
            print(f"   ❌ Import error: {result.stderr}")
            return False

        # Test connection
        print("   ✓ Testing database connection...")
        result = subprocess.run(
            [
                "python",
                "-c",
                """
import mysql.connector
try:
    conn = mysql.connector.connect(host='localhost', port=3308, user='root', password='baivietwp_password', database='mydb')
    if conn.is_connected():
        print('✅ Database OK')
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM posts')
        count = cursor.fetchone()[0] 
        print(f'✅ Posts: {count}')
        conn.close()
    else:
        print('❌ Database connection failed')
except Exception as e:
    print(f'❌ Database error: {e}')
""",
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )

        print(result.stdout)
        if "Database OK" in result.stdout:
            print("   ✅ Database connection working")
        else:
            print("   ❌ Database connection failed")
            return False

        return True

    except Exception as e:
        print(f"   ❌ Test failed: {e}")
        return False


def show_simple_usage():
    """Hiển thị cách sử dụng đơn giản"""
    print("\n📖 CÁCH SỬ DỤNG ĐƠN GIẢN:")
    print("=" * 40)

    print("🎯 OPTION 1: Interactive Menu")
    print("   python ai_content_processor.py")
    print("   → Chọn từ menu 0-4")
    print()

    print("🎯 OPTION 2: Command Line")
    print("   python ai_content_processor.py batch")
    print("   python ai_content_processor.py batch 10")
    print("   python ai_content_processor.py batch 10 2.0")
    print("   python ai_content_processor.py stats")
    print("   python ai_content_processor.py single")
    print()

    print("🎯 OPTION 3: Batch Files")
    print("   run_simple.bat - Chạy interactive menu")
    print("   run_batch.bat - Chạy batch processing")
    print()

    print("📊 FILES BẠN CẦN:")
    print("   ✅ ai_content_processor.py - Main tool")
    print("   ✅ config.py - API configuration")
    print("   ✅ requirements.txt - Dependencies")
    print("   📊 MySQL database running (localhost:3308)")


def main():
    """Main function"""
    print("🚀 RESTORE SIMPLE AI CONTENT PROCESSOR")
    print("Khôi phục về tool đơn giản ban đầu")
    print("=" * 60)

    # Khôi phục về phiên bản đơn giản
    if not restore_simple_version():
        print("❌ Không thể khôi phục. Kiểm tra files.")
        return

    # Test system
    if not run_simple_test():
        print("⚠️ Có lỗi trong system. Kiểm tra lại.")

    # Show usage
    show_simple_usage()

    print("\n🎉 READY TO USE!")
    print("Chạy: python ai_content_processor.py")

    # Tùy chọn chạy ngay
    choice = input("\n🚀 Muốn chạy ngay không? (y/n): ").lower().strip()
    if choice in ["y", "yes"]:
        print("🚀 Starting AI Content Processor...")
        os.system("python ai_content_processor.py")


if __name__ == "__main__":
    main()
