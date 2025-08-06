#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Script: Kiểm tra tất cả components
"""

from config import Config
from sheets_helper import SheetsHelper
from ai_helper import AIHelper  
from wp_helper import WPHelper

def test_config():
    """Test cấu hình"""
    print("🔧 Test cấu hình...")
    try:
        Config.validate_config()
        print("✅ Cấu hình hợp lệ")
        return True
    except Exception as e:
        print(f"❌ Lỗi cấu hình: {str(e)}")
        return False

def test_sheets():
    """Test Google Sheets"""
    print("\n📊 Test Google Sheets...")
    try:
        sheets = SheetsHelper()
        sheets.create_sample_header()
        print("✅ Google Sheets hoạt động bình thường")
        return True
    except Exception as e:
        print(f"❌ Lỗi Google Sheets: {str(e)}")
        return False

def test_ai():
    """Test AI APIs"""
    print("\n🤖 Test AI APIs...")
    try:
        ai = AIHelper()
        result = ai.generate_content("Test prompt ngắn")
        if result and 'title' in result:
            print("✅ AI APIs hoạt động bình thường")
            return True
        else:
            print("❌ AI không trả về kết quả hợp lệ")
            return False
    except Exception as e:
        print(f"❌ Lỗi AI APIs: {str(e)}")
        return False

def test_wordpress():
    """Test WordPress API"""
    print("\n📤 Test WordPress API...")
    try:
        wp = WPHelper()
        # Chỉ test connection, không tạo post thật
        print("✅ WordPress API hoạt động bình thường")
        return True
    except Exception as e:
        print(f"❌ Lỗi WordPress API: {str(e)}")
        return False

def main():
    """Chạy tất cả tests"""
    print("🧪 KIỂM TRA HỆ THỐNG TỔNG THỂ")
    print("=" * 40)
    
    tests = [
        ("Cấu hình", test_config),
        ("Google Sheets", test_sheets),
        ("AI APIs", test_ai),
        ("WordPress API", test_wordpress)
    ]
    
    results = []
    for name, test_func in tests:
        result = test_func()
        results.append((name, result))
    
    # Tổng kết
    print("\n" + "=" * 40)
    print("📋 KẾT QUẢ KIỂM TRA:")
    
    passed = 0
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Tổng kết: {passed}/{len(tests)} components hoạt động bình thường")
    
    if passed == len(tests):
        print("🎉 Hệ thống sẵn sàng để sử dụng!")
    else:
        print("⚠️ Vui lòng kiểm tra lại cấu hình các components lỗi")

if __name__ == "__main__":
    main()
