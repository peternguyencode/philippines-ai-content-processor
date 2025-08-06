#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script để hoàn thành import 20 bài còn lại vào Google Sheets
Với cơ chế delay và retry để tránh rate limit
"""

import json
import gspread
import time
import re
from datetime import datetime
from google.oauth2.service_account import Credentials

def setup_google_sheets():
    """Thiết lập kết nối Google Sheets"""
    try:
        # Đọc credentials từ file JSON
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
    # Giới hạn độ dài để tránh lỗi Google Sheets
    if len(clean_text) > 5000:
        clean_text = clean_text[:5000] + "..."
    
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
        'deposit', 'withdraw', 'promotion', 'offer', 'deal'
    ]
    
    found_keywords = [kw for kw in casino_keywords if kw in text]
    return ", ".join(found_keywords[:5])  # Giới hạn 5 keywords

def get_existing_titles(worksheet):
    """Lấy danh sách titles đã có trong sheet để tránh trùng lặp"""
    try:
        # Lấy tất cả dữ liệu từ cột Title (cột C)
        titles = worksheet.col_values(3)  # Cột 3 là Title
        # Bỏ qua header
        return titles[1:] if len(titles) > 1 else []
    except Exception as e:
        print(f"Lỗi khi lấy danh sách titles: {e}")
        return []

def import_remaining_posts():
    """Import 20 bài còn lại với delay để tránh rate limit"""
    
    # Đọc dữ liệu JSON
    try:
        with open('bonus365casinoall_posts.json', 'r', encoding='utf-8') as f:
            posts = json.load(f)
        
        # File này là một mảng trực tiếp, không có key 'posts'
        if not isinstance(posts, list):
            print("File JSON không phải là mảng posts")
            return
            
        print(f"Tổng số bài posts: {len(posts)}")
        
    except FileNotFoundError:
        print("Không tìm thấy file bonus365casinoall_posts.json")
        return
    except json.JSONDecodeError as e:
        print(f"Lỗi đọc file JSON: {e}")
        return

    # Thiết lập Google Sheets
    spreadsheet = setup_google_sheets()
    if not spreadsheet:
        return
    
    # Lấy worksheet "Bonus365casinoall"
    try:
        worksheet = spreadsheet.worksheet("Bonus365casinoall")
        print("Đã tìm thấy sheet 'Bonus365casinoall'")
    except gspread.WorksheetNotFound:
        print("Không tìm thấy sheet 'Bonus365casinoall'")
        return
    
    # Lấy danh sách titles đã có
    existing_titles = get_existing_titles(worksheet)
    print(f"Đã có {len(existing_titles)} bài trong sheet")
    
    # Tìm các bài chưa được import
    remaining_posts = []
    for post in posts:
        title = post.get('title', '').strip()  # title là string trực tiếp
        if title and title not in existing_titles:
            remaining_posts.append(post)
    
    print(f"Số bài còn lại cần import: {len(remaining_posts)}")
    
    if not remaining_posts:
        print("Tất cả bài đã được import!")
        return
    
    # Import từng bài với delay
    imported_count = 0
    total_remaining = len(remaining_posts)
    
    for i, post in enumerate(remaining_posts, 1):
        try:
            print(f"\n[{i}/{total_remaining}] Đang import bài: {post.get('title', 'No title')[:50]}...")
            
            # Chuẩn bị dữ liệu - cấu trúc JSON đơn giản
            title = post.get('title', '')
            content = post.get('content', '')
            clean_content = clean_html_content(content)
            
            # Lấy URL ảnh featured
            featured_image_url = post.get('featured_image', '')
            
            # Tạo dữ liệu row
            row_data = [
                'Bonus365casinoall',  # Source_Title
                'completed',          # Status
                title,               # Title
                clean_content,       # Content
                post.get('link', ''), # Original_URL
                featured_image_url,   # Image_URL
                title,               # Meta_Title
                clean_content[:160] + "..." if len(clean_content) > 160 else clean_content,  # Meta_Desc
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # Import_Date
                extract_keywords_from_content(clean_content, title),  # Keywords
                'Casino',            # Category
                'bonus, casino',     # Tags
                'AI Import',         # Author
                'Imported from bonus365casinoall_posts.json',  # Notes
                ''                   # Custom_Field
            ]
            
            # Thêm vào sheet với retry mechanism
            retry_count = 0
            max_retries = 3
            
            while retry_count < max_retries:
                try:
                    worksheet.append_row(row_data)
                    imported_count += 1
                    print(f"✓ Đã import thành công bài {i}/{total_remaining}")
                    break
                    
                except Exception as e:
                    retry_count += 1
                    if "quota" in str(e).lower() or "429" in str(e):
                        print(f"⚠️ Rate limit detected, waiting 10 seconds... (retry {retry_count}/{max_retries})")
                        time.sleep(10)
                    else:
                        print(f"❌ Lỗi import bài {i}: {e}")
                        if retry_count < max_retries:
                            print(f"Thử lại sau 5 giây... (retry {retry_count}/{max_retries})")
                            time.sleep(5)
                        else:
                            print(f"Bỏ qua bài này sau {max_retries} lần thử")
                            break
            
            # Delay giữa các bài để tránh rate limit
            if i < total_remaining:  # Không delay sau bài cuối
                print(f"Chờ 5 giây trước khi import bài tiếp theo...")
                time.sleep(5)
                
        except KeyboardInterrupt:
            print(f"\n⚠️ Người dùng dừng quá trình. Đã import {imported_count}/{total_remaining} bài.")
            break
        except Exception as e:
            print(f"❌ Lỗi không mong muốn khi xử lý bài {i}: {e}")
            continue
    
    print(f"\n🎉 Hoàn thành! Đã import thêm {imported_count}/{total_remaining} bài còn lại.")
    print(f"Tổng số bài trong sheet hiện tại: {len(existing_titles) + imported_count}")

if __name__ == "__main__":
    print("=== SCRIPT HOÀN THÀNH IMPORT DỮ LIỆU ===")
    print("Bắt đầu import 20 bài còn lại...")
    import_remaining_posts()
    print("Script hoàn thành!")
