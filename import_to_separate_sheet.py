#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script nhập TOÀN BỘ dữ liệu từ JSON file vào Google Sheets riêng biệt
Tự động tạo sheet mới với tên dựa trên file JSON
Ví dụ: bonus365casinoall_posts.json → sheet "Bonus365casinoall"
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
    
    def create_sheet_name_from_filename(json_filename):
        """Tạo tên sheet từ filename JSON"""
        # Loại bỏ đuôi file và các từ không cần thiết
        sheet_name = json_filename.replace('_posts.json', '').replace('.json', '')
        sheet_name = sheet_name.replace('_', ' ')
        
        # Viết hoa chữ cái đầu từng từ
        sheet_name = ' '.join(word.capitalize() for word in sheet_name.split())
        
        # Giới hạn độ dài tên sheet (Google Sheets max 100 ký tự)
        if len(sheet_name) > 50:
            sheet_name = sheet_name[:50]
        
        return sheet_name
    
    def create_or_get_worksheet(json_filename):
        """Tạo hoặc lấy worksheet dựa trên tên file JSON"""
        
        sheet_name = create_sheet_name_from_filename(json_filename)
        
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
            
            # Kiểm tra số dòng hiện tại
            current_rows = len(worksheet.get_all_records())
            print(f"📊 Sheet hiện có {current_rows} dòng dữ liệu")
            
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
    
    print("=" * 80)
    print(f"NHẬP TOÀN BỘ DỮ LIỆU TỪ {json_file.upper()}")
    print(f"SHEET RIÊNG BIỆT: {create_sheet_name_from_filename(json_file)}")
    print("=" * 80)
    
    if not os.path.exists(json_file):
        print(f"❌ File {json_file} không tồn tại!")
        print("\n📝 CÁCH SỬ DỤNG:")
        print(f"   python {os.path.basename(__file__)} [tên_file.json]")
        print("\n📝 VÍ DỤ:")
        print(f"   python {os.path.basename(__file__)} bonus365casinoall_posts.json")
        print(f"   python {os.path.basename(__file__)} other_casino_posts.json")
        print(f"   python {os.path.basename(__file__)} blog_data.json")
        sys.exit(1)
    
    print(f"📁 Đọc dữ liệu từ {json_file}...")
    
    with open(json_file, 'r', encoding='utf-8') as f:
        posts_data = json.load(f)
    
    print(f"📊 Tìm thấy {len(posts_data)} bài viết trong file JSON")
    
    # Tạo hoặc lấy worksheet riêng cho file này
    worksheet, sheet_name = create_or_get_worksheet(json_file)
    
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
                'source_title': f"Import: {title}",
                'title': title,
                'content': clean_content,
                'original_url': link,
                'image_url': featured_image,
                'keywords': keywords,
                'meta_title': f"{title} | Casino Guide",
                'meta_desc': meta_desc,
                'status': 'completed',  # Đánh dấu là đã có sẵn data
                'source': os.path.basename(json_file).replace('.json', ''),
                'category': 'Casino',
                'import_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            valid_posts += 1
            
            # Giới hạn để test trước (có thể điều chỉnh)
            if valid_posts >= 100:  # Tăng lên 100 bài
                break
    
    print(f"✅ Đã xử lý {len(processed_data)} bài viết hợp lệ")
    
    # Hiển thị preview
    if processed_data:
        print(f"\n📋 PREVIEW DỮ LIỆU SHEET '{sheet_name}' (3 bài đầu):")
        print("-" * 80)
        
        for i, data in enumerate(processed_data[:3], 1):
            print(f"\n🔹 Bài {i}:")
            print(f"   📰 Title: {data['title']}")
            print(f"   🔗 Original URL: {data['original_url']}")
            print(f"   🖼️ Image: {data['image_url'][:80]}..." if len(data['image_url']) > 80 else f"   🖼️ Image: {data['image_url']}")
            print(f"   📝 Content: {data['content'][:100]}...")
            print(f"   🏷️ Keywords: {data['keywords']}")
            print(f"   📄 Meta Desc: {data['meta_desc'][:80]}...")
            print(f"   ✅ Status: {data['status']}")
            print(f"   📅 Import Date: {data['import_date']}")
    
    # Hỏi xác nhận
    user_input = input(f"\n❓ Bạn có muốn nhập {len(processed_data)} bài viết vào sheet '{sheet_name}'? (y/n): ")
    
    if user_input.lower() in ['y', 'yes', 'có']:
        print(f"\n🔄 Đang nhập dữ liệu vào sheet '{sheet_name}'...")
        
        success_count = 0
        error_count = 0
        
        for i, data in enumerate(processed_data, 1):
            try:
                # Nhập với TOÀN BỘ thông tin theo header mới
                row_data = [
                    data['source_title'],        # Cột A: Source_Title
                    data['status'],              # Cột B: Status
                    data['title'],               # Cột C: Title
                    data['content'],             # Cột D: Content
                    data['original_url'],        # Cột E: Original_URL
                    data['image_url'],           # Cột F: Image_URL
                    data['meta_title'],          # Cột G: Meta_Title
                    data['meta_desc'],           # Cột H: Meta_Desc
                    data['import_date'],         # Cột I: Import_Date
                    data['keywords'],            # Cột J: Keywords
                    data['category'],            # Cột K: Category
                    f"Source: {data['source']}", # Cột L: Tags
                    "Auto Import",               # Cột M: Author
                    f"Imported from {json_file}",# Cột N: Notes
                    ""                           # Cột O: Custom_Field
                ]
                
                worksheet.append_row(row_data)
                success_count += 1
                
                # Hiển thị tiến trình
                if i % 10 == 0:
                    print(f"   ✅ Đã nhập {i}/{len(processed_data)} bài viết...")
                
                # Delay nhỏ để tránh rate limit
                if i % 20 == 0:
                    import time
                    time.sleep(1)
                
            except Exception as e:
                print(f"   ❌ Lỗi nhập bài {i}: {str(e)}")
                error_count += 1
        
        print(f"\n🎉 HOÀN THÀNH NHẬP DỮ LIỆU VÀO SHEET '{sheet_name}'!")
        print(f"   ✅ Thành công: {success_count}/{len(processed_data)} bài viết")
        if error_count > 0:
            print(f"   ❌ Lỗi: {error_count} bài viết")
        print(f"   📊 Sheet độc lập: '{sheet_name}'")
        print(f"   🔗 Link: https://docs.google.com/spreadsheets/d/{Config.GOOGLE_SHEET_ID}")
        
        # Hiển thị thống kê
        print(f"\n📈 THỐNG KÊ DỮ LIỆU TRONG SHEET '{sheet_name}':")
        with_content = sum(1 for d in processed_data if d['content'])
        with_images = sum(1 for d in processed_data if d['image_url'])
        with_urls = sum(1 for d in processed_data if d['original_url'])
        
        print(f"   📝 Có nội dung: {with_content}/{len(processed_data)}")
        print(f"   🖼️ Có hình ảnh: {with_images}/{len(processed_data)}")
        print(f"   🔗 Có URL: {with_urls}/{len(processed_data)}")
        
        print(f"\n🎯 LỢI ÍCH CỦA SHEET RIÊNG BIỆT '{sheet_name}':")
        print(f"   - Dữ liệu hoàn toàn độc lập với các sheet khác")
        print(f"   - Có thể xử lý riêng biệt hoặc kết hợp sau này")
        print(f"   - Dễ dàng quản lý theo từng nguồn dữ liệu")
        print(f"   - Tất cả bài viết đã có status = 'completed'")
        print(f"   - Sẵn sàng để publish hoặc xử lý thêm")
        
        print(f"\n🚀 CÁCH SỬ DỤNG TIẾP THEO:")
        print(f"   1. Truy cập Google Sheets để xem dữ liệu")
        print(f"   2. Có thể copy dữ liệu sang sheet chính để xử lý AI")
        print(f"   3. Hoặc tạo script riêng để publish từ sheet '{sheet_name}'")
        
    else:
        print("❌ Đã hủy việc nhập dữ liệu.")
        
        # Tạo file backup
        backup_file = f"backup_{os.path.basename(json_file).replace('.json', '')}_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(processed_data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Đã lưu dữ liệu đầy đủ vào: {backup_file}")
        print(f"   Bạn có thể sử dụng file này để import sau.")

except Exception as e:
    print(f"❌ LỖI: {str(e)}")
    print(f"📍 Chi tiết lỗi: {type(e).__name__}")
    
    import traceback
    print(f"🔍 Traceback:")
    traceback.print_exc()
    
    print(f"\n💡 GỢI Ý KHẮC PHỤC:")
    print(f"   1. Kiểm tra file .env có đầy đủ thông tin không")
    print(f"   2. Kiểm tra file credentials JSON có tồn tại không")
    print(f"   3. Kiểm tra quyền truy cập Google Sheets")
    print(f"   4. Thử lại với file JSON khác")
