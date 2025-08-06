#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script nhập TOÀN BỘ dữ liệu từ JSON file vào Google Sheets riêng biệt
Tự động tạo sheet mới với tên dựa trên file JSON
Bao gồm: title, content, link, featured_image - không tạo prompt
"""

import json
import sys
import os
from pathlib import Path
import re
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

# Thêm thư mục hiện tại vào sys.path
sys.path.append(str(Path.cwd()))

try:
    from config import Config
    
    def clean_html_content(html_content):
        """Làm sạch nội dung HTML"""
        if not html_content:
            return ""
        
        # Giữ nguyên HTML nhưng làm sạch
        clean_content = html_content.strip()
        # Loại bỏ các ký tự không mong muốn
        clean_content = re.sub(r'\t+', '', clean_content)
        clean_content = re.sub(r'\n+', '\n', clean_content)
        
        return clean_content
    
    def extract_keywords_from_content(title, content):
        """Trích xuất từ khóa từ title và content"""
        text = f"{title} {content}".lower()
        keywords = []
        
        # Danh sách từ khóa phổ biến
        keyword_patterns = [
            'free bonus', 'casino bonus', 'sign up bonus', 'no deposit',
            'online casino', '100 bonus', 'registration', 'gcash',
            'masaya', 'philippines', 'deposit', 'cashback', 'casino',
            'betting', 'gambling', 'slots', 'games'
        ]
        
        for pattern in keyword_patterns:
            if pattern in text:
                keywords.append(pattern)
        
        return ', '.join(keywords[:8])  # Giới hạn 8 từ khóa
    
    def create_meta_description(title, content):
        """Tạo meta description từ content"""
        if not content:
            return f"Tìm hiểu về {title}. Hướng dẫn chi tiết và cập nhật mới nhất."
        
        # Lấy text từ HTML
        clean_text = re.sub(r'<[^>]+>', '', content)
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()
        
        # Lấy 150 ký tự đầu
        if len(clean_text) > 150:
            meta_desc = clean_text[:147] + "..."
        else:
            meta_desc = clean_text
        
        return meta_desc
    
    def create_or_get_worksheet(json_filename):
        """Tạo hoặc lấy worksheet dựa trên tên file JSON"""
        
        # Tạo tên sheet từ filename (loại bỏ _posts.json)
        sheet_name = json_filename.replace('_posts.json', '').replace('.json', '')
        sheet_name = sheet_name.replace('_', ' ').title()  # Viết hoa chữ cái đầu
        
        print(f"🔄 Tạo/tìm sheet: '{sheet_name}'")
        
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
        
        # Kiểm tra xem sheet đã tồn tại chưa
        try:
            worksheet = spreadsheet.worksheet(sheet_name)
            print(f"✅ Tìm thấy sheet '{sheet_name}' đã tồn tại")
        except gspread.WorksheetNotFound:
            # Tạo sheet mới
            worksheet = spreadsheet.add_worksheet(title=sheet_name, rows=1000, cols=15)
            print(f"✅ Đã tạo sheet mới: '{sheet_name}'")
            
            # Tạo header cho sheet mới
            headers = [
                'Source_Title', 'Status', 'Title', 'Content', 'Original_URL', 
                'Image_URL', 'Meta_Title', 'Meta_Desc', 'Import_Date', 'Keywords',
                'Category', 'Tags', 'Author', 'Notes', 'Custom_Field'
            ]
            worksheet.insert_row(headers, 1)
            print(f"📋 Đã tạo header cho sheet '{sheet_name}'")
        
        return worksheet, sheet_name
    
    # Lấy tên file JSON từ tham số hoặc mặc định
    if len(sys.argv) > 1:
        json_file = sys.argv[1]
    else:
        json_file = "bonus365casinoall_posts.json"
    if not os.path.exists(json_file):
        print(f"❌ File {json_file} không tồn tại!")
        sys.exit(1)
    
    print(f"📁 Đọc dữ liệu từ {json_file}...")
    
    with open(json_file, 'r', encoding='utf-8') as f:
        posts_data = json.load(f)
    
    print(f"📊 Tìm thấy {len(posts_data)} bài viết trong file JSON")
    
    # Xử lý dữ liệu
    processed_data = []
    valid_posts = 0
    
    for i, post in enumerate(posts_data, 1):
        title = post.get('title', '').strip()
        content = post.get('content', '').strip()
        link = post.get('link', '').strip()
        featured_image = post.get('featured_image', '').strip()
        
        # Chỉ xử lý post có title
        if title and len(title) > 5:
            # Làm sạch content
            clean_content = clean_html_content(content)
            
            # Tạo keywords và meta description
            keywords = extract_keywords_from_content(title, content)
            meta_desc = create_meta_description(title, content)
            
            processed_data.append({
                'title': title,
                'content': clean_content,
                'wp_url': link,
                'image_url': featured_image,
                'keywords': keywords,
                'meta_title': f"{title} | Casino Guide",
                'meta_desc': meta_desc,
                'status': 'completed',  # Đánh dấu là đã có sẵn data
                'source': 'bonus365casino_import'
            })
            valid_posts += 1
            
            # Giới hạn để test trước
            if valid_posts >= 30:  # Tăng lên 30 bài
                break
    
    print(f"✅ Đã xử lý {len(processed_data)} bài viết hợp lệ")
    
    # Hiển thị preview
    if processed_data:
        print(f"\n📋 PREVIEW TOÀN BỘ DỮ LIỆU (3 bài đầu):")
        print("-" * 80)
        
        for i, data in enumerate(processed_data[:3], 1):
            print(f"\n🔹 Bài {i}:")
            print(f"   📰 Title: {data['title']}")
            print(f"   🔗 WP_URL: {data['wp_url']}")
            print(f"   🖼️ Image: {data['image_url']}")
            print(f"   📝 Content: {data['content'][:100]}...")
            print(f"   🏷️ Keywords: {data['keywords']}")
            print(f"   📄 Meta Desc: {data['meta_desc'][:80]}...")
            print(f"   ✅ Status: {data['status']}")
    
    # Hỏi xác nhận
    user_input = input(f"\n❓ Bạn có muốn nhập {len(processed_data)} bài viết ĐẦY DỦ THÔNG TIN này vào Google Sheets? (y/n): ")
    
    if user_input.lower() in ['y', 'yes', 'có']:
        print("\n🔄 Đang kết nối Google Sheets...")
        
        # Khởi tạo SheetsHelper
        sheets_helper = SheetsHelper()
        
        # Tạo header nếu chưa có
        sheets_helper.create_sample_header()
        
        print("📤 Đang nhập TOÀN BỘ dữ liệu...")
        success_count = 0
        
        for i, data in enumerate(processed_data, 1):
            try:
                # Nhập với TOÀN BỘ thông tin có sẵn
                row_data = [
                    f"Import: {data['title']}",  # Cột A: Prompt (đánh dấu là import)
                    data['status'],              # Cột B: Status = completed
                    data['title'],               # Cột C: Title (có sẵn)
                    data['content'],             # Cột D: Content (có sẵn)
                    data['wp_url'],              # Cột E: WP_URL (có sẵn)
                    data['image_url'],           # Cột F: Image_URL (có sẵn)
                    data['meta_title'],          # Cột G: Meta_Title (có sẵn)
                    data['meta_desc'],           # Cột H: Meta_Desc (có sẵn)
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # Cột I: Created_Date
                    f"Source: {data['source']}, Keywords: {data['keywords']}"  # Cột J: Ghi chú
                ]
                
                sheets_helper.worksheet.append_row(row_data)
                success_count += 1
                
                # Hiển thị tiến trình
                if i % 5 == 0:
                    print(f"   ✅ Đã nhập {i}/{len(processed_data)} bài viết đầy đủ...")
                
            except Exception as e:
                print(f"   ❌ Lỗi nhập bài {i}: {str(e)}")
        
        print(f"\n🎉 HOÀN THÀNH NHẬP DỮ LIỆU ĐẦY ĐỦ!")
        print(f"   ✅ Đã nhập thành công: {success_count}/{len(processed_data)} bài viết")
        print(f"   📊 Mỗi bài đều có: Title, Content, URL, Image, Meta tags")
        print(f"   🔄 Status: completed (không cần AI xử lý thêm)")
        
        # Hiển thị thống kê
        print(f"\n📈 THỐNG KÊ DỮ LIỆU NHẬP:")
        with_content = sum(1 for d in processed_data if d['content'])
        with_images = sum(1 for d in processed_data if d['image_url'])
        with_urls = sum(1 for d in processed_data if d['wp_url'])
        
        print(f"   📝 Có nội dung: {with_content}/{len(processed_data)}")
        print(f"   🖼️ Có hình ảnh: {with_images}/{len(processed_data)}")
        print(f"   🔗 Có URL: {with_urls}/{len(processed_data)}")
        
        print(f"\n🎯 LƯU Ý:")
        print(f"   - Tất cả bài viết đã có status = 'completed'")
        print(f"   - Không cần chạy AI processing thêm")
        print(f"   - Có thể publish trực tiếp lên WordPress")
        
    else:
        print("❌ Đã hủy việc nhập dữ liệu.")
        
        # Tạo file backup
        backup_file = f"full_bonus365_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(processed_data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Đã lưu dữ liệu đầy đủ vào: {backup_file}")

except Exception as e:
    print(f"❌ LỖI: {str(e)}")
    print(f"📍 Chi tiết lỗi: {type(e).__name__}")
    
    import traceback
    print(f"🔍 Traceback:")
    traceback.print_exc()
