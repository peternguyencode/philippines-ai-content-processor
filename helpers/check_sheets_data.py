#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script kiểm tra dữ liệu trong Google Sheets
"""

import json
import sys
import os
from pathlib import Path

# Thêm thư mục hiện tại vào sys.path
sys.path.append(str(Path.cwd()))

try:
    from config import Config
    from sheets_helper import SheetsHelper
    
    print("=" * 60)
    print("KIỂM TRA DỮ LIỆU GOOGLE SHEETS")
    print("=" * 60)
    
    # Khởi tạo SheetsHelper
    sheets_helper = SheetsHelper()
    
    print(f"📊 Đang kết nối tới Google Sheets...")
    print(f"📋 Sheet ID: {Config.GOOGLE_SHEET_ID}")
    
    # Lấy tất cả dữ liệu
    all_data = sheets_helper.worksheet.get_all_records()
    
    print(f"\n📈 TỔNG QUAN DỮ LIỆU:")
    print(f"   - Số dòng dữ liệu: {len(all_data)}")
    
    if all_data:
        print(f"   - Các cột có sẵn: {list(all_data[0].keys())}")
        
        print(f"\n📋 DỮ LIỆU CHI TIẾT:")
        print("-" * 60)
        
        for i, row in enumerate(all_data, 1):
            print(f"\n🔹 Dòng {i}:")
            for key, value in row.items():
                if value:  # Chỉ hiển thị các cột có dữ liệu
                    print(f"   {key}: {value}")
    else:
        print("\n❌ KHÔNG CÓ DỮ LIỆU TRONG SPREADSHEET")
        print("📝 Spreadsheet hiện tại trống hoặc chỉ có header.")
        print("\n💡 ĐỀ XUẤT THÊM DỮ LIỆU MẪU:")
        print("   - Prompt: Yêu cầu viết bài")
        print("   - Status: Trạng thái (pending/completed/error)")
        print("   - Title, Content, v.v.: Sẽ được AI tự động tạo")
        
        # Gợi ý thêm dữ liệu mẫu
        sample_prompts = [
            "Viết bài về xu hướng AI trong marketing 2024",
            "Hướng dẫn tối ưu SEO website hiệu quả",
            "Top 10 công cụ productivity cho doanh nghiệp",
            "Cách đầu tư cryptocurrency an toàn cho người mới"
        ]
        
        print(f"\n📋 CÁC PROMPT MẪU KHUYẾN NGHỊ:")
        for i, prompt in enumerate(sample_prompts, 1):
            print(f"   {i}. {prompt}")
        
        user_input = input("\n❓ Bạn có muốn thêm dữ liệu mẫu này vào spreadsheet? (y/n): ")
        if user_input.lower() in ['y', 'yes', 'có']:
            print("🔄 Đang thêm dữ liệu mẫu...")
            
            # Tạo header nếu chưa có
            sheets_helper.create_sample_header()
            
            # Thêm dữ liệu mẫu
            for prompt in sample_prompts:
                try:
                    sheets_helper.worksheet.append_row([prompt, "pending", "", "", "", "", "", "", "", ""])
                except Exception as e:
                    print(f"❌ Lỗi thêm prompt '{prompt}': {str(e)}")
            
            print("✅ Đã thêm dữ liệu mẫu thành công!")
            
            # Hiển thị lại dữ liệu sau khi thêm
            print("\n📊 DỮ LIỆU SAU KHI THÊM:")
            all_data = sheets_helper.worksheet.get_all_records()
            for i, row in enumerate(all_data, 1):
                print(f"\n🔹 Dòng {i}:")
                for key, value in row.items():
                    if value:
                        print(f"   {key}: {value}")
    
    print("\n" + "=" * 60)
    print("🎯 KẾT LUẬN:")
    print("   - Google Sheets đã được kết nối thành công")
    print("   - Dữ liệu bài viết sẽ được lấy từ spreadsheet này")
    print("   - Hệ thống AI sẽ tự động tạo nội dung dựa trên dữ liệu")
    print("=" * 60)
    
except Exception as e:
    print(f"❌ LỖI: {str(e)}")
    print(f"📍 Chi tiết lỗi: {type(e).__name__}")
    
    # Cập nhật thông tin sheet ID
    cred_path = "strong-augury-467706-b4-fa91bb781d0a.json"
    if os.path.exists(cred_path):
        print(f"✅ File credentials.json tồn tại: {cred_path}")
    else:
        print(f"❌ File credentials.json không tồn tại: {cred_path}")
    
    # Kiểm tra file .env
    env_path = ".env"
    if os.path.exists(env_path):
        print(f"✅ File .env tồn tại: {env_path}")
    else:
        print(f"❌ File .env không tồn tại: {env_path}")
