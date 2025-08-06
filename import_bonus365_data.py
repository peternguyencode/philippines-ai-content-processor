#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script nhập dữ liệu từ bonus365casinoall_posts.json vào Google Sheets
"""

import json
import sys
import os
from pathlib import Path
import re
from datetime import datetime

# Thêm thư mục hiện tại vào sys.path
sys.path.append(str(Path.cwd()))

try:
    from config import Config
    from sheets_helper import SheetsHelper
    
    def clean_html_content(html_content):
        """Làm sạch nội dung HTML và tạo prompt từ title + content"""
        if not html_content:
            return ""
        
        # Loại bỏ các thẻ HTML
        clean_text = re.sub(r'<[^>]+>', '', html_content)
        # Loại bỏ khoảng trắng thừa
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()
        # Giới hạn độ dài
        if len(clean_text) > 500:
            clean_text = clean_text[:500] + "..."
        
        return clean_text
    
    def create_prompt_from_post(post_data):
        """Tạo prompt từ dữ liệu bài viết"""
        title = post_data.get('title', '')
        content = post_data.get('content', '')
        
        if not title:
            return ""
        
        # Tạo prompt dựa trên title
        prompts_templates = [
            f"Viết bài chi tiết về {title}",
            f"Tạo nội dung SEO về {title}",
            f"Phân tích và đánh giá {title}",
            f"Hướng dẫn chi tiết về {title}",
            f"Tổng hợp thông tin về {title}"
        ]
        
        # Chọn template dựa trên nội dung
        if 'bonus' in title.lower() or 'casino' in title.lower():
            return f"Viết bài hướng dẫn về {title} - Cách nhận và sử dụng hiệu quả"
        elif 'free' in title.lower():
            return f"Hướng dẫn chi tiết {title} - Các bước và điều kiện"
        elif 'sign up' in title.lower():
            return f"Tạo bài viết về {title} - Quy trình đăng ký và lợi ích"
        else:
            return f"Viết bài phân tích về {title}"
    
    def extract_keywords_from_title(title):
        """Trích xuất từ khóa từ tiêu đề"""
        if not title:
            return ""
        
        # Các từ khóa phổ biến trong casino/bonus
        keywords = []
        title_lower = title.lower()
        
        if 'free' in title_lower:
            keywords.append('free bonus')
        if 'casino' in title_lower:
            keywords.append('online casino')
        if 'bonus' in title_lower:
            keywords.append('casino bonus')
        if 'sign up' in title_lower:
            keywords.append('sign up bonus')
        if '100' in title_lower:
            keywords.append('100 bonus')
        if 'deposit' in title_lower:
            keywords.append('no deposit')
            
        return ', '.join(keywords[:5])  # Giới hạn 5 từ khóa
    
    print("=" * 70)
    print("NHẬP DỮ LIỆU TỪ BONUS365CASINOALL_POSTS.JSON")
    print("=" * 70)
    
    # Đọc file JSON
    json_file = "bonus365casinoall_posts.json"
    if not os.path.exists(json_file):
        print(f"❌ File {json_file} không tồn tại!")
        sys.exit(1)
    
    print(f"📁 Đọc dữ liệu từ {json_file}...")
    
    with open(json_file, 'r', encoding='utf-8') as f:
        posts_data = json.load(f)
    
    print(f"📊 Tìm thấy {len(posts_data)} bài viết trong file JSON")
    
    # Lọc và chuyển đổi dữ liệu
    converted_data = []
    valid_posts = 0
    
    for i, post in enumerate(posts_data, 1):
        title = post.get('title', '').strip()
        content = post.get('content', '')
        
        # Chỉ xử lý các post có title
        if title and len(title) > 10:
            prompt = create_prompt_from_post(post)
            keywords = extract_keywords_from_title(title)
            
            if prompt:
                converted_data.append({
                    'prompt': prompt,
                    'original_title': title,
                    'keywords': keywords,
                    'status': 'pending',
                    'source': 'bonus365casino'
                })
                valid_posts += 1
                
                # Giới hạn số lượng để tránh spam
                if valid_posts >= 20:
                    break
    
    print(f"✅ Đã chuyển đổi {len(converted_data)} bài viết hợp lệ")
    
    # Hiển thị mẫu dữ liệu
    if converted_data:
        print(f"\n📋 PREVIEW DỮ LIỆU CHUYỂN ĐỔI (5 bài đầu):")
        print("-" * 70)
        
        for i, data in enumerate(converted_data[:5], 1):
            print(f"\n🔹 Bài {i}:")
            print(f"   Prompt: {data['prompt']}")
            print(f"   Original Title: {data['original_title']}")
            print(f"   Keywords: {data['keywords']}")
            print(f"   Status: {data['status']}")
    
    # Hỏi xác nhận
    user_input = input(f"\n❓ Bạn có muốn nhập {len(converted_data)} bài viết này vào Google Sheets? (y/n): ")
    
    if user_input.lower() in ['y', 'yes', 'có']:
        print("\n🔄 Đang kết nối Google Sheets...")
        
        # Khởi tạo SheetsHelper
        sheets_helper = SheetsHelper()
        
        # Tạo header nếu chưa có
        sheets_helper.create_sample_header()
        
        print("📤 Đang nhập dữ liệu...")
        success_count = 0
        
        for i, data in enumerate(converted_data, 1):
            try:
                # Thêm vào Google Sheets với format chuẩn
                row_data = [
                    data['prompt'],          # Cột A: Prompt
                    data['status'],          # Cột B: Status
                    "",                      # Cột C: Title (sẽ được AI tạo)
                    "",                      # Cột D: Content (sẽ được AI tạo)
                    "",                      # Cột E: WP_URL (sẽ được tạo sau)
                    "",                      # Cột F: Image_URL (sẽ được AI tạo)
                    "",                      # Cột G: Meta_Title (sẽ được AI tạo)
                    "",                      # Cột H: Meta_Desc (sẽ được AI tạo)
                    "",                      # Cột I: Created_Date (sẽ được cập nhật)
                    f"Source: {data['source']}, Keywords: {data['keywords']}"  # Cột J: Ghi chú
                ]
                
                sheets_helper.worksheet.append_row(row_data)
                success_count += 1
                
                # Hiển thị tiến trình
                if i % 5 == 0:
                    print(f"   ✅ Đã nhập {i}/{len(converted_data)} bài viết...")
                
            except Exception as e:
                print(f"   ❌ Lỗi nhập bài {i}: {str(e)}")
        
        print(f"\n🎉 HOÀN THÀNH!")
        print(f"   ✅ Đã nhập thành công: {success_count}/{len(converted_data)} bài viết")
        print(f"   📊 Tổng dữ liệu hiện tại trong sheets: {len(sheets_helper.worksheet.get_all_records())} dòng")
        
        # Hiển thị hướng dẫn tiếp theo
        print(f"\n🚀 BƯỚC TIẾP THEO:")
        print(f"   1. Chạy: python simple_runner.py - để xử lý các bài pending")
        print(f"   2. Hoặc: python main.py - để chạy batch processing")
        print(f"   3. Kiểm tra: python check_sheets_data.py - để xem kết quả")
        
    else:
        print("❌ Đã hủy việc nhập dữ liệu.")
        
        # Tạo file backup
        backup_file = f"converted_bonus365_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(converted_data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Đã lưu dữ liệu chuyển đổi vào: {backup_file}")
        print("   Bạn có thể dùng file này để nhập sau.")

except Exception as e:
    print(f"❌ LỖI: {str(e)}")
    print(f"📍 Chi tiết lỗi: {type(e).__name__}")
    
    import traceback
    print(f"🔍 Traceback:")
    traceback.print_exc()
