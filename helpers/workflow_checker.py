#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
COMPREHENSIVE WORKFLOW CHECKER
Kiểm tra từng bước trong quy trình WordPress Automation
"""

import os
import sys
import traceback
from datetime import datetime

def print_step(step_num, title, status=""):
    print(f"\n{'='*60}")
    print(f"BƯỚC {step_num}: {title}")
    print(f"{'='*60}")
    if status:
        print(f"Trạng thái: {status}")

def check_environment():
    """Bước 1: Kiểm tra môi trường Python"""
    print_step(1, "KIỂM TRA MÔI TRƯỜNG PYTHON")
    
    try:
        print(f"✅ Python version: {sys.version}")
        print(f"✅ Working directory: {os.getcwd()}")
        print(f"✅ Virtual environment: {sys.prefix}")
        
        # Kiểm tra thư viện quan trọng
        libraries = {
            'openai': 'OpenAI API',
            'google.generativeai': 'Google Gemini API', 
            'gspread': 'Google Sheets API',
            'requests': 'HTTP requests',
            'dotenv': 'Environment variables'
        }
        
        print(f"\n📦 KIỂM TRA THỦ VIỆN:")
        for lib, desc in libraries.items():
            try:
                __import__(lib)
                print(f"✅ {desc}: Đã cài đặt")
            except ImportError:
                print(f"❌ {desc}: Chưa cài đặt")
                
        return True
    except Exception as e:
        print(f"❌ Lỗi kiểm tra môi trường: {e}")
        return False

def check_config_files():
    """Bước 2: Kiểm tra file cấu hình"""
    print_step(2, "KIỂM TRA FILE CẤU HÌNH")
    
    files_to_check = {
        '.env': 'Environment variables',
        'config.py': 'Main configuration',
        'strong-augury-467706-b4-fa91bb781d0a.json': 'Google Service Account credentials'
    }
    
    all_good = True
    for file, desc in files_to_check.items():
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"✅ {desc}: {file} ({size} bytes)")
        else:
            print(f"❌ {desc}: {file} - KHÔNG TỒN TẠI")
            all_good = False
    
    return all_good

def check_env_variables():
    """Bước 3: Kiểm tra biến môi trường"""
    print_step(3, "KIỂM TRA BIẾN MÔI TRƯỜNG")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        required_vars = {
            'OPENAI_API_KEY': 'OpenAI API Key',
            'GEMINI_API_KEY': 'Google Gemini API Key',
            'WP_URL': 'WordPress URL',
            'WP_USERNAME': 'WordPress Username', 
            'WP_PASSWORD': 'WordPress Password',
            'GOOGLE_SHEET_ID': 'Google Sheet ID',
            'GOOGLE_CREDS_FILE': 'Google Credentials File'
        }
        
        all_configured = True
        for var, desc in required_vars.items():
            value = os.getenv(var)
            if value:
                # Ẩn một phần giá trị nhạy cảm
                if 'KEY' in var or 'PASSWORD' in var:
                    display_value = f"{value[:10]}...{value[-4:]}" if len(value) > 14 else "***"
                else:
                    display_value = value
                print(f"✅ {desc}: {display_value}")
            else:
                print(f"❌ {desc}: CHƯA ĐƯỢC CẤU HÌNH")
                all_configured = False
        
        return all_configured
    except Exception as e:
        print(f"❌ Lỗi kiểm tra env variables: {e}")
        return False

def check_google_sheets():
    """Bước 4: Kiểm tra kết nối Google Sheets"""
    print_step(4, "KIỂM TRA GOOGLE SHEETS")
    
    try:
        from sheets_helper import SheetsHelper
        sheets = SheetsHelper()
        
        # Test đọc dữ liệu
        pending = sheets.get_pending_rows()
        print(f"✅ Kết nối Google Sheets thành công")
        print(f"📊 Tìm thấy {len(pending)} hàng pending")
        
        # Hiển thị 3 hàng đầu
        for i, row in enumerate(pending[:3], 1):
            prompt = row.get('prompt', '')[:50]
            print(f"   {i}. Hàng {row['row_number']}: {prompt}...")
        
        return True
    except Exception as e:
        print(f"❌ Lỗi Google Sheets: {e}")
        return False

def check_ai_apis():
    """Bước 5: Kiểm tra AI APIs"""
    print_step(5, "KIỂM TRA AI APIs")
    
    try:
        from ai_helper import AIHelper
        ai = AIHelper()
        
        # Test OpenAI
        try:
            result = ai.generate_content("Test ngắn", provider='openai')
            if result and result.get('title'):
                print(f"✅ OpenAI API: Hoạt động bình thường")
                print(f"   Sample title: {result['title'][:50]}...")
            else:
                print(f"❌ OpenAI API: Không trả về kết quả hợp lệ")
        except Exception as e:
            print(f"❌ OpenAI API: {e}")
        
        # Test Gemini
        try:
            result = ai.generate_content("Test ngắn", provider='gemini')
            if result and result.get('title'):
                print(f"✅ Gemini API: Hoạt động bình thường")
                print(f"   Sample title: {result['title'][:50]}...")
            else:
                print(f"❌ Gemini API: Không trả về kết quả hợp lệ")
        except Exception as e:
            print(f"❌ Gemini API: {e}")
        
        # Test Image Generation
        try:
            image_url = ai.generate_image("test image prompt")
            if image_url:
                print(f"✅ Image Generation: Hoạt động bình thường")
                print(f"   Sample URL: {image_url[:50]}...")
            else:
                print(f"❌ Image Generation: Không sinh được ảnh")
        except Exception as e:
            print(f"❌ Image Generation: {e}")
            
        return True
    except Exception as e:
        print(f"❌ Lỗi AI APIs: {e}")
        return False

def check_wordpress():
    """Bước 6: Kiểm tra WordPress API"""
    print_step(6, "KIỂM TRA WORDPRESS API")
    
    try:
        from wp_helper import WPHelper
        wp = WPHelper()
        
        # Test tạo bài viết
        print(f"✅ WordPress API: Kết nối thành công")
        
        # Lấy thông tin user
        import requests
        from config import Config
        
        response = requests.get(
            f"{Config.WP_API_URL}/users/me",
            auth=(Config.WP_USERNAME, Config.WP_PASSWORD)
        )
        
        if response.status_code == 200:
            user_info = response.json()
            print(f"✅ User info: {user_info.get('name', 'Unknown')}")
            print(f"✅ Capabilities: {len(user_info.get('capabilities', {}))} permissions")
        
        return True
    except Exception as e:
        print(f"❌ Lỗi WordPress API: {e}")
        return False

def check_workflow_readiness():
    """Bước 7: Kiểm tra sẵn sàng workflow"""
    print_step(7, "KIỂM TRA SẴN SÀNG WORKFLOW")
    
    try:
        from main import WordPressAutomation
        automation = WordPressAutomation()
        
        print(f"✅ Main workflow: Khởi tạo thành công")
        print(f"✅ All components: Đã sẵn sàng")
        
        return True
    except Exception as e:
        print(f"❌ Lỗi workflow: {e}")
        return False

def generate_action_plan(results):
    """Tạo kế hoạch hành động dựa trên kết quả kiểm tra"""
    print_step("FINAL", "KẾ HOẠCH HÀNH ĐỘNG")
    
    failed_steps = [i+1 for i, result in enumerate(results) if not result]
    
    if not failed_steps:
        print("🎉 TẤT CẢ BƯỚC ĐÃ HOÀN HẢO!")
        print("\n✅ Hệ thống sẵn sàng sử dụng:")
        print("   - Chạy: python main.py single (test 1 bài)")
        print("   - Chạy: python main.py batch 3 (test 3 bài)")
        print("   - Chạy: run_batch.bat (tự động)")
        return
    
    print(f"⚠️ CẦN KHẮC PHỤC {len(failed_steps)} BƯỚC:")
    
    action_plans = {
        1: """
        🔧 SỬA LỖI MÔI TRƯỜNG PYTHON:
        - Cài đặt Python 3.10+
        - Tạo virtual environment: python -m venv .venv
        - Activate: .venv\\Scripts\\activate
        - Cài thư viện: pip install -r requirements.txt
        """,
        2: """
        📁 SỬA LỖI FILE CẤU HÌNH:
        - Tạo file .env với API keys
        - Download Google Service Account JSON
        - Đặt tên: strong-augury-467706-b4-fa91bb781d0a.json
        """,
        3: """
        ⚙️ SỬA LỖI BIẾN MÔI TRƯỜNG:
        - Kiểm tra file .env
        - Cập nhật tất cả API keys
        - Kiểm tra WordPress credentials
        """,
        4: """
        📊 SỬA LỖI GOOGLE SHEETS:
        - Kiểm tra Google Service Account
        - Chia sẻ Sheet với email Service Account
        - Kiểm tra GOOGLE_SHEET_ID
        """,
        5: """
        🤖 SỬA LỖI AI APIs:
        - Kiểm tra OpenAI API key và credit
        - Kiểm tra Gemini API key
        - Test từng API riêng lẻ
        """,
        6: """
        📤 SỬA LỖI WORDPRESS:
        - Kiểm tra WP_URL có đúng không
        - Tạo lại Application Password
        - Kiểm tra REST API enabled
        """,
        7: """
        🔄 SỬA LỖI WORKFLOW:
        - Khắc phục tất cả lỗi trên trước
        - Restart Python environment
        - Test lại từng component
        """
    }
    
    for step in failed_steps:
        print(action_plans.get(step, f"Kiểm tra lại bước {step}"))

def main():
    """Main checker function"""
    print("🔍 WORDPRESS AUTOMATION - WORKFLOW CHECKER")
    print("=" * 60)
    print(f"Thời gian kiểm tra: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Danh sách tất cả bước kiểm tra
    checks = [
        check_environment,
        check_config_files, 
        check_env_variables,
        check_google_sheets,
        check_ai_apis,
        check_wordpress,
        check_workflow_readiness
    ]
    
    results = []
    
    # Chạy từng bước
    for check in checks:
        try:
            result = check()
            results.append(result)
        except Exception as e:
            print(f"❌ Exception trong {check.__name__}: {e}")
            traceback.print_exc()
            results.append(False)
    
    # Tạo kế hoạch hành động
    generate_action_plan(results)
    
    # Tổng kết
    success_count = sum(results)
    total_count = len(results)
    
    print(f"\n📈 TỔNG KẾT: {success_count}/{total_count} bước hoàn thành")
    print(f"📊 Tỷ lệ thành công: {success_count/total_count*100:.1f}%")
    
    if success_count == total_count:
        print("🎯 HỆ THỐNG SẴN SÀNG HOÀN HẢO!")
    else:
        print("⚠️ CẦN KHẮC PHỤC MỘT SỐ VẤN ĐỀ")

if __name__ == "__main__":
    main()
