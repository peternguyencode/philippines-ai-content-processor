#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script import dữ liệu với AI xử lý content bằng ChatGPT
"""

import json
import gspread
import time
import re
from openai import OpenAI
from datetime import datetime
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def setup_openai():
    """Thiết lập OpenAI API"""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ Không tìm thấy OPENAI_API_KEY trong file .env")
        return None
    
    client = OpenAI(api_key=api_key)
    print("✅ OpenAI API đã được thiết lập")
    return client

def process_content_with_ai(client, content, title):
    """Xử lý content bằng ChatGPT"""
    try:
        # Làm sạch HTML trước
        clean_content = clean_html_content(content)
        
        # Nếu content quá ngắn, không cần xử lý AI
        if len(clean_content) < 100:
            return clean_content
        
        # Prompt cho ChatGPT
        prompt = f"""
Hãy cải thiện và tối ưu nội dung bài viết sau về casino/bonus cho thị trường Philippines. 
Yêu cầu:
1. Giữ nguyên thông tin chính và từ khóa quan trọng
2. Cải thiện cấu trúc và dễ đọc hơn
3. Thêm call-to-action phù hợp
4. Độ dài khoảng 800-1200 từ
5. Viết bằng tiếng Anh, phù hợp với người Philippines

Tiêu đề: {title}

Nội dung gốc:
{clean_content[:2000]}...

Hãy trả về nội dung đã được cải thiện:
"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Bạn là một chuyên gia viết content về casino và bonus. Hãy tạo nội dung chất lượng cao, hấp dẫn và có tính thuyết phục."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.7
        )
        
        ai_content = response.choices[0].message.content.strip()
        print(f"✅ AI đã xử lý content (độ dài: {len(ai_content)} ký tự)")
        return ai_content
        
    except Exception as e:
        print(f"⚠️ Lỗi khi xử lý AI: {e}")
        print("Sẽ sử dụng content gốc đã làm sạch")
        return clean_html_content(content)

def setup_google_sheets():
    """Thiết lập kết nối Google Sheets"""
    try:
        creds = Credentials.from_service_account_file(
            'strong-augury-467706-b4-fa91bb781d0a.json',
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        
        client = gspread.authorize(creds)
        spreadsheet = client.open_by_key('1JNeybKkC9nRUXWgX6yIdhSv8roiweal2VESQtwfLHc0')
        
        return spreadsheet
    except Exception as e:
        print(f"Lỗi khi thiết lập Google Sheets: {e}")
        return None

def clean_html_content(html_content):
    """Làm sạch nội dung HTML"""
    if not html_content:
        return ""
    
    # Loại bỏ các thẻ HTML
    clean_text = re.sub(r'<[^>]+>', '', html_content)
    # Loại bỏ khoảng trắng thừa
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()
    # Loại bỏ các ký tự đặc biệt
    clean_text = re.sub(r'&#\d+;', '', clean_text)
    
    return clean_text

def extract_keywords_from_content(content, title=""):
    """Trích xuất keywords từ nội dung"""
    if not content and not title:
        return ""
    
    text = f"{title} {content}".lower()
    
    # Keywords liên quan đến casino/bonus
    casino_keywords = [
        'casino', 'bonus', 'free spins', 'jackpot', 'slot', 'poker', 
        'blackjack', 'roulette', 'baccarat', 'gaming', 'bet', 'win',
        'deposit', 'withdraw', 'promotion', 'offer', 'deal', 'philippines',
        'gcash', 'maya', 'signup', 'register', 'no deposit'
    ]
    
    found_keywords = [kw for kw in casino_keywords if kw in text]
    return ", ".join(found_keywords[:8])  # Giới hạn 8 keywords

def get_existing_titles(worksheet):
    """Lấy danh sách titles đã có trong sheet để tránh trùng lặp"""
    try:
        titles = worksheet.col_values(3)  # Cột 3 là Title
        return titles[1:] if len(titles) > 1 else []
    except Exception as e:
        print(f"Lỗi khi lấy danh sách titles: {e}")
        return []

def create_or_get_worksheet(spreadsheet, sheet_name):
    """Tạo hoặc lấy worksheet"""
    try:
        worksheet = spreadsheet.worksheet(sheet_name)
        print(f"✅ Đã tìm thấy sheet '{sheet_name}'")
        return worksheet
    except gspread.WorksheetNotFound:
        print(f"Tạo sheet mới: '{sheet_name}'")
        worksheet = spreadsheet.add_worksheet(title=sheet_name, rows=1000, cols=15)
        
        # Thêm header
        headers = [
            'Source_Title', 'Status', 'Title', 'Content', 'Original_URL', 
            'Image_URL', 'Meta_Title', 'Meta_Desc', 'Import_Date', 
            'Keywords', 'Category', 'Tags', 'Author', 'Notes', 'Custom_Field'
        ]
        worksheet.append_row(headers)
        print(f"✅ Đã tạo sheet '{sheet_name}' với headers")
        return worksheet

def import_with_ai_processing(json_file):
    """Import dữ liệu với AI xử lý content"""
    
    # Kiểm tra OpenAI API
    openai_client = setup_openai()
    if not openai_client:
        return
    
    # Đọc dữ liệu JSON
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            posts = json.load(f)
        
        if not isinstance(posts, list):
            print("File JSON không phải là mảng posts")
            return
            
        print(f"Tổng số bài posts: {len(posts)}")
        
    except FileNotFoundError:
        print(f"Không tìm thấy file {json_file}")
        return
    except json.JSONDecodeError as e:
        print(f"Lỗi đọc file JSON: {e}")
        return

    # Thiết lập Google Sheets
    spreadsheet = setup_google_sheets()
    if not spreadsheet:
        return
    
    # Tạo tên sheet từ filename
    sheet_name = json_file.replace('.json', '').replace('_posts', '').replace('_', '').title()
    worksheet = create_or_get_worksheet(spreadsheet, sheet_name)
    
    # Lấy danh sách titles đã có
    existing_titles = get_existing_titles(worksheet)
    print(f"Đã có {len(existing_titles)} bài trong sheet")
    
    # Tìm các bài chưa được import
    remaining_posts = []
    for post in posts:
        title = post.get('title', '').strip()
        if title and title not in existing_titles:
            remaining_posts.append(post)
    
    print(f"Số bài cần import và xử lý AI: {len(remaining_posts)}")
    
    if not remaining_posts:
        print("Tất cả bài đã được import!")
        return
    
    # Import từng bài với AI processing
    imported_count = 0
    total_remaining = len(remaining_posts)
    
    for i, post in enumerate(remaining_posts, 1):
        try:
            title = post.get('title', 'No title')
            print(f"\n[{i}/{total_remaining}] Đang xử lý: {title[:50]}...")
            
            # Xử lý content bằng AI
            original_content = post.get('content', '')
            print("🤖 Đang xử lý content bằng ChatGPT...")
            ai_processed_content = process_content_with_ai(openai_client, original_content, title)
            
            # Lấy URL ảnh featured
            featured_image_url = post.get('featured_image', '')
            
            # Tạo dữ liệu row
            row_data = [
                sheet_name,           # Source_Title
                'completed',          # Status
                title,               # Title
                ai_processed_content, # Content (đã được AI xử lý)
                post.get('link', ''), # Original_URL
                featured_image_url,   # Image_URL
                title,               # Meta_Title
                ai_processed_content[:160] + "..." if len(ai_processed_content) > 160 else ai_processed_content,  # Meta_Desc
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # Import_Date
                extract_keywords_from_content(ai_processed_content, title),  # Keywords
                'Casino',            # Category
                'bonus, casino, ai-enhanced',  # Tags
                'AI Enhanced',       # Author
                f'AI processed from {json_file}',  # Notes
                'ChatGPT-3.5'       # Custom_Field
            ]
            
            # Thêm vào sheet với retry mechanism
            retry_count = 0
            max_retries = 3
            
            while retry_count < max_retries:
                try:
                    worksheet.append_row(row_data)
                    imported_count += 1
                    print(f"✅ Đã import thành công bài {i}/{total_remaining}")
                    break
                    
                except Exception as e:
                    retry_count += 1
                    if "quota" in str(e).lower() or "429" in str(e):
                        print(f"⚠️ Rate limit detected, waiting 15 seconds... (retry {retry_count}/{max_retries})")
                        time.sleep(15)
                    else:
                        print(f"❌ Lỗi import bài {i}: {e}")
                        if retry_count < max_retries:
                            print(f"Thử lại sau 5 giây... (retry {retry_count}/{max_retries})")
                            time.sleep(5)
                        else:
                            print(f"Bỏ qua bài này sau {max_retries} lần thử")
                            break
            
            # Delay giữa các bài để tránh rate limit và cho phép AI xử lý
            if i < total_remaining:
                print(f"Chờ 8 giây trước khi xử lý bài tiếp theo...")
                time.sleep(8)
                
        except KeyboardInterrupt:
            print(f"\n⚠️ Người dùng dừng quá trình. Đã import {imported_count}/{total_remaining} bài.")
            break
        except Exception as e:
            print(f"❌ Lỗi không mong muốn khi xử lý bài {i}: {e}")
            continue
    
    print(f"\n🎉 Hoàn thành! Đã import và xử lý AI cho {imported_count}/{total_remaining} bài.")
    print(f"Tất cả content đã được ChatGPT cải thiện và tối ưu!")

if __name__ == "__main__":
    print("=== IMPORT DỮ LIỆU VỚI AI XỬ LÝ CONTENT ===")
    
    # Nhập tên file JSON
    json_file = input("Nhập tên file JSON (ví dụ: bonus365casinoall_posts.json): ").strip()
    if not json_file:
        json_file = "bonus365casinoall_posts.json"  # Default
    
    print(f"Bắt đầu import và xử lý AI cho file: {json_file}")
    import_with_ai_processing(json_file)
    print("Script hoàn thành!")
