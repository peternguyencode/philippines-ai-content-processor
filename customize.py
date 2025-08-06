#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
INTERACTIVE CUSTOMIZATION TOOL
Công cụ tương tác để chỉnh sửa hệ thống WordPress Automation
"""

import os
import shutil
from datetime import datetime

def backup_file(filepath):
    """Backup file trước khi chỉnh sửa"""
    if os.path.exists(filepath):
        backup_path = f"{filepath}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.copy2(filepath, backup_path)
        print(f"✅ Đã backup: {backup_path}")
        return backup_path
    return None

def show_current_config():
    """Hiển thị cấu hình hiện tại"""
    print("\n🔧 CẤU HÌNH HIỆN TẠI:")
    print("=" * 50)
    
    try:
        from dotenv import load_dotenv
        import os
        load_dotenv()
        
        configs = {
            "AI Provider": os.getenv('DEFAULT_AI_PROVIDER', 'openai'),
            "Max Content Length": os.getenv('MAX_CONTENT_LENGTH', '2000'),
            "Concurrent Requests": os.getenv('CONCURRENT_REQUESTS', '3'),
            "Request Delay": os.getenv('REQUEST_DELAY', '2'),
            "Batch Size": os.getenv('BATCH_SIZE', '5')
        }
        
        for key, value in configs.items():
            print(f"📊 {key}: {value}")
            
    except Exception as e:
        print(f"❌ Lỗi đọc config: {e}")

def customize_ai_settings():
    """Tùy chỉnh cài đặt AI"""
    print("\n🤖 TÙY CHỈNH AI SETTINGS")
    print("=" * 40)
    
    # Đọc cấu hình hiện tại
    from dotenv import load_dotenv
    load_dotenv()
    
    current_provider = os.getenv('DEFAULT_AI_PROVIDER', 'openai')
    current_length = os.getenv('MAX_CONTENT_LENGTH', '2000')
    
    print(f"Hiện tại - Provider: {current_provider}, Max Length: {current_length}")
    
    # Tùy chọn
    print("\n1. Chuyển sang Gemini Pro (miễn phí hơn)")
    print("2. Chuyển sang OpenAI GPT (chất lượng cao)")
    print("3. Thay đổi độ dài content")
    print("4. Tùy chỉnh prompt template")
    print("0. Quay lại")
    
    choice = input("\nChọn tùy chọn: ").strip()
    
    if choice == "1":
        update_env_var("DEFAULT_AI_PROVIDER", "gemini")
        print("✅ Đã chuyển sang Gemini Pro")
    elif choice == "2":
        update_env_var("DEFAULT_AI_PROVIDER", "openai")
        print("✅ Đã chuyển sang OpenAI GPT")
    elif choice == "3":
        new_length = input(f"Nhập độ dài mới (hiện tại: {current_length}): ").strip()
        if new_length.isdigit():
            update_env_var("MAX_CONTENT_LENGTH", new_length)
            print(f"✅ Đã cập nhật độ dài: {new_length}")
    elif choice == "4":
        customize_prompt_template()

def customize_performance():
    """Tùy chỉnh hiệu suất"""
    print("\n⚡ TÙY CHỈNH HIỆU SUẤT")
    print("=" * 40)
    
    from dotenv import load_dotenv
    load_dotenv()
    
    current_concurrent = os.getenv('CONCURRENT_REQUESTS', '3')
    current_delay = os.getenv('REQUEST_DELAY', '2')
    
    print(f"Hiện tại - Concurrent: {current_concurrent}, Delay: {current_delay}s")
    
    print("\n1. Tăng tốc độ (rủi ro rate limit)")
    print("2. Giảm tải hệ thống (chậm nhưng ổn định)")
    print("3. Tùy chỉnh chi tiết")
    print("0. Quay lại")
    
    choice = input("\nChọn tùy chọn: ").strip()
    
    if choice == "1":
        update_env_var("CONCURRENT_REQUESTS", "5")
        update_env_var("REQUEST_DELAY", "1")
        print("✅ Đã tăng tốc độ: 5 concurrent, 1s delay")
    elif choice == "2":
        update_env_var("CONCURRENT_REQUESTS", "1")
        update_env_var("REQUEST_DELAY", "5")
        print("✅ Đã giảm tải: 1 concurrent, 5s delay")
    elif choice == "3":
        concurrent = input(f"Concurrent requests (1-10, hiện tại {current_concurrent}): ").strip()
        delay = input(f"Request delay giây (1-10, hiện tại {current_delay}): ").strip()
        
        if concurrent.isdigit() and 1 <= int(concurrent) <= 10:
            update_env_var("CONCURRENT_REQUESTS", concurrent)
        if delay.isdigit() and 1 <= int(delay) <= 10:
            update_env_var("REQUEST_DELAY", delay)
        print("✅ Đã cập nhật cài đặt hiệu suất")

def customize_wordpress():
    """Tùy chỉnh WordPress settings"""
    print("\n📤 TÙY CHỈNH WORDPRESS")
    print("=" * 40)
    
    print("1. Thay đổi default post status (draft/publish)")
    print("2. Tùy chỉnh categories & tags")
    print("3. Cài đặt SEO meta")
    print("4. Kiểm tra kết nối WordPress")
    print("0. Quay lại")
    
    choice = input("\nChọn tùy chọn: ").strip()
    
    if choice == "1":
        print("\nDefault post status:")
        print("- draft: Lưu nháp (an toàn)")
        print("- publish: Đăng luôn (tự động)")
        status = input("Chọn (draft/publish): ").strip().lower()
        if status in ['draft', 'publish']:
            # Cập nhật trong wp_helper.py
            print(f"✅ Sẽ đặt default status: {status}")
            print("💡 Cần chỉnh sửa thủ công trong wp_helper.py")
    elif choice == "4":
        test_wordpress_connection()

def customize_prompt_template():
    """Tùy chỉnh prompt template"""
    print("\n📝 TÙY CHỈNH PROMPT TEMPLATE")
    print("=" * 40)
    
    backup_file("ai_helper.py")
    
    print("Các template có sẵn:")
    print("1. Blog cá nhân (tone thân thiện)")
    print("2. Business formal (tone chuyên nghiệp)")
    print("3. Technical review (tone chuyên sâu)")
    print("4. News article (tone khách quan)")
    print("5. Tùy chỉnh thủ công")
    
    choice = input("\nChọn template: ").strip()
    
    templates = {
        "1": "Bạn là một blogger cá nhân, viết tone thân thiện, gần gũi với người đọc.",
        "2": "Bạn là một chuyên gia business, viết tone chuyên nghiệp, formal.",
        "3": "Bạn là một technical reviewer, viết chi tiết, chuyên sâu về kỹ thuật.",
        "4": "Bạn là một nhà báo, viết khách quan, cung cấp thông tin chính xác."
    }
    
    if choice in templates:
        print(f"✅ Đã chọn template: {templates[choice]}")
        print("💡 Cần cập nhật thủ công trong ai_helper.py, dòng 79")
    elif choice == "5":
        custom_prompt = input("Nhập system message tùy chỉnh: ")
        print(f"✅ Custom prompt: {custom_prompt}")
        print("💡 Cần cập nhật thủ công trong ai_helper.py")

def test_wordpress_connection():
    """Test kết nối WordPress"""
    print("\n🔍 KIỂM TRA WORDPRESS...")
    
    try:
        from wp_helper import WPHelper
        wp = WPHelper()
        print("✅ Kết nối WordPress thành công!")
        
        # Test tạo bài draft
        test_title = f"Test Connection - {datetime.now().strftime('%H:%M:%S')}"
        test_content = "<p>Đây là bài test kết nối. Có thể xóa.</p>"
        
        result = wp.create_post(test_title, test_content, 'draft')
        if result:
            print(f"✅ Test tạo bài thành công: {result['link']}")
        else:
            print("❌ Không thể tạo bài test")
            
    except Exception as e:
        print(f"❌ Lỗi WordPress: {e}")

def update_env_var(key, value):
    """Cập nhật biến môi trường trong file .env"""
    try:
        # Backup .env
        backup_file(".env")
        
        # Đọc file .env
        with open(".env", "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        # Tìm và cập nhật
        updated = False
        for i, line in enumerate(lines):
            if line.startswith(f"{key}="):
                lines[i] = f"{key}={value}\n"
                updated = True
                break
        
        # Nếu không tìm thấy, thêm mới
        if not updated:
            lines.append(f"{key}={value}\n")
        
        # Ghi lại file
        with open(".env", "w", encoding="utf-8") as f:
            f.writelines(lines)
        
        print(f"✅ Đã cập nhật {key}={value}")
        
    except Exception as e:
        print(f"❌ Lỗi cập nhật .env: {e}")

def run_quick_test():
    """Chạy test nhanh sau khi chỉnh sửa"""
    print("\n🧪 CHẠY TEST NHANH...")
    
    try:
        os.system("python workflow_checker.py")
    except Exception as e:
        print(f"❌ Lỗi test: {e}")

def main():
    """Main interactive menu"""
    while True:
        print("\n🎛️ WORDPRESS AUTOMATION - CUSTOMIZATION TOOL")
        print("=" * 60)
        
        show_current_config()
        
        print("\n📋 TÙY CHỈNH:")
        print("1. 🤖 AI Settings (Provider, Content Length, Prompt)")
        print("2. ⚡ Performance (Concurrent, Delay, Batch Size)")
        print("3. 📤 WordPress (Post Status, Categories, SEO)")
        print("4. 📊 Google Sheets (Column Mapping)")
        print("5. 🧪 Chạy test sau chỉnh sửa")
        print("6. 📖 Xem hướng dẫn chi tiết")
        print("0. Thoát")
        
        choice = input("\n👉 Chọn tùy chọn (0-6): ").strip()
        
        if choice == '0':
            print("👋 Tạm biệt!")
            break
        elif choice == '1':
            customize_ai_settings()
        elif choice == '2':
            customize_performance()
        elif choice == '3':
            customize_wordpress()
        elif choice == '4':
            print("💡 Xem file CUSTOMIZATION_GUIDE.md để biết chi tiết")
        elif choice == '5':
            run_quick_test()
        elif choice == '6':
            print("📖 Xem file CUSTOMIZATION_GUIDE.md để có hướng dẫn đầy đủ")
        else:
            print("❌ Tùy chọn không hợp lệ!")

if __name__ == "__main__":
    main()
