#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kiểm tra kết quả cuối cùng sau khi import hoàn tất
"""

import gspread
from google.oauth2.service_account import Credentials

def check_final_results():
    """Kiểm tra kết quả cuối cùng"""
    try:
        # Thiết lập kết nối
        creds = Credentials.from_service_account_file(
            'strong-augury-467706-b4-fa91bb781d0a.json',
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        client = gspread.authorize(creds)
        spreadsheet = client.open_by_key('1JNeybKkC9nRUXWgX6yIdhSv8roiweal2VESQtwfLHc0')
        
        # Kiểm tra sheet Bonus365casinoall
        worksheet = spreadsheet.worksheet('Bonus365casinoall')
        all_values = worksheet.get_all_values()
        
        print("=== KẾT QUẢ CUỐI CÙNG ===")
        print(f"Tổng số hàng trong sheet: {len(all_values)}")
        print(f"Số bài posts (trừ header): {len(all_values) - 1}")
        
        if len(all_values) > 1:
            print("\n5 bài cuối cùng được import:")
            for i, row in enumerate(all_values[-5:], len(all_values)-4):
                if len(row) > 2 and row[2]:  # Kiểm tra có title
                    print(f"  {i}. {row[2][:60]}...")
        
        # Kiểm tra tổng từ file JSON
        import json
        with open('bonus365casinoall_posts.json', 'r', encoding='utf-8') as f:
            posts = json.load(f)
        
        print(f"\nSố bài trong file JSON gốc: {len(posts)}")
        print(f"Số bài đã import: {len(all_values) - 1}")
        
        if len(all_values) - 1 == len(posts):
            print("✅ HOÀN THÀNH! Tất cả bài đã được import thành công!")
        else:
            print(f"⚠️ Còn thiếu {len(posts) - (len(all_values) - 1)} bài")
            
    except Exception as e:
        print(f"Lỗi khi kiểm tra: {e}")

if __name__ == "__main__":
    check_final_results()
