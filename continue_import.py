#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script tiếp tục nhập dữ liệu còn lại vào sheet (khắc phục rate limit)
"""

import json
import sys
import os
from pathlib import Path
import re
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials
import time

sys.path.append(str(Path.cwd()))

try:
    from config import Config
    
    def clean_html_content(html_content):
        if not html_content:
            return ""
        clean_content = html_content.strip()
        clean_content = re.sub(r'\t+', '', clean_content)
        clean_content = re.sub(r'\n+', '\n', clean_content)
        return clean_content
    
    def extract_keywords_from_content(title, content):
        text = f"{title} {content}".lower()
        keywords = []
        keyword_patterns = [
            'free bonus', 'casino bonus', 'sign up bonus', 'no deposit',
            'online casino', '100 bonus', 'registration', 'gcash',
            'masaya', 'philippines', 'deposit', 'cashback', 'casino',
            'betting', 'gambling', 'slots', 'games'
        ]
        for pattern in keyword_patterns:
            if pattern in text:
                keywords.append(pattern)
        return ', '.join(keywords[:8])
    
    def create_meta_description(title, content):
        if not content:
            return f"Tìm hiểu về {title}. Hướng dẫn chi tiết và cập nhật mới nhất."
        clean_text = re.sub(r'<[^>]+>', '', content)
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()
        if len(clean_text) > 150:
            meta_desc = clean_text[:147] + "..."
        else:
            meta_desc = clean_text
        return meta_desc
    
    # Lấy tham số
    if len(sys.argv) > 1:
        json_file = sys.argv[1]
        skip_count = int(sys.argv[2]) if len(sys.argv) > 2 else 67
    else:
        json_file = "bonus365casinoall_posts.json"
        skip_count = 67
    
    sheet_name = "Bonus365casinoall"
    
    print("=" * 80)
    print(f"TIẾP TỤC NHẬP DỮ LIỆU VÀO SHEET '{sheet_name}'")
    print(f"BỎ QUA {skip_count} BÀI ĐÃ NHẬP, NHẬP PHẦN CÒN LẠI")
    print("=" * 80)
    
    # Đọc file JSON
    with open(json_file, 'r', encoding='utf-8') as f:
        posts_data = json.load(f)
    
    print(f"📊 Tổng {len(posts_data)} bài, bỏ qua {skip_count} bài đã nhập")
    
    # Kết nối Google Sheets
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]
    
    creds = Credentials.from_service_account_file(
        Config.GOOGLE_CREDS_FILE, 
        scopes=scope
    )
    
    gc = gspread.authorize(creds)
    spreadsheet = gc.open_by_key(Config.GOOGLE_SHEET_ID)
    worksheet = spreadsheet.worksheet(sheet_name)
    
    print(f"✅ Kết nối sheet '{sheet_name}' thành công")
    
    # Xử lý phần còn lại
    remaining_posts = posts_data[skip_count:]
    print(f"📋 Còn lại {len(remaining_posts)} bài cần nhập")
    
    processed_data = []
    for i, post in enumerate(remaining_posts):
        title = post.get('title', '').strip()
        content = post.get('content', '').strip()
        link = post.get('link', '').strip()
        featured_image = post.get('featured_image', '').strip()
        
        if title and len(title) > 5:
            clean_content = clean_html_content(content)
            keywords = extract_keywords_from_content(title, content)
            meta_desc = create_meta_description(title, content)
            
            processed_data.append({
                'source_title': f"Import: {title}",
                'title': title,
                'content': clean_content,
                'original_url': link,
                'image_url': featured_image,
                'keywords': keywords,
                'meta_title': f"{title} | Casino Guide",
                'meta_desc': meta_desc,
                'status': 'completed',
                'source': os.path.basename(json_file).replace('.json', ''),
                'category': 'Casino',
                'import_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
    
    print(f"✅ Xử lý được {len(processed_data)} bài viết hợp lệ")
    
    if processed_data:
        user_input = input(f"\n❓ Tiếp tục nhập {len(processed_data)} bài còn lại? (y/n): ")
        
        if user_input.lower() in ['y', 'yes', 'có']:
            print(f"\n🔄 Nhập với delay để tránh rate limit...")
            
            success_count = 0
            error_count = 0
            
            for i, data in enumerate(processed_data, 1):
                try:
                    row_data = [
                        data['source_title'],
                        data['status'],
                        data['title'],
                        data['content'],
                        data['original_url'],
                        data['image_url'],
                        data['meta_title'],
                        data['meta_desc'],
                        data['import_date'],
                        data['keywords'],
                        data['category'],
                        f"Source: {data['source']}",
                        "Auto Import",
                        f"Imported from {json_file}",
                        ""
                    ]
                    
                    worksheet.append_row(row_data)
                    success_count += 1
                    
                    if i % 5 == 0:
                        print(f"   ✅ Đã nhập {i}/{len(processed_data)} bài...")
                    
                    # Delay 3 giây mỗi request để tránh rate limit
                    time.sleep(3)
                    
                except Exception as e:
                    print(f"   ❌ Lỗi bài {i}: {str(e)}")
                    error_count += 1
                    time.sleep(5)  # Delay lâu hơn khi có lỗi
            
            print(f"\n🎉 HOÀN THÀNH NHẬP PHẦN CÒN LẠI!")
            print(f"   ✅ Thành công: {success_count}/{len(processed_data)}")
            if error_count > 0:
                print(f"   ❌ Lỗi: {error_count}")
            print(f"   📊 Tổng cộng sheet '{sheet_name}': ~{skip_count + success_count} bài")

except Exception as e:
    print(f"❌ LỖI: {str(e)}")
    import traceback
    traceback.print_exc()
