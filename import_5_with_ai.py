#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Import 5 bài đầu tiên với AI processing để test
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
Improve and optimize this casino/bonus article content for the Philippines market. 
Tasks:
1. Keep all important information and keywords
2. Improve structure and readability
3. Add engaging call-to-action
4. Length around 700-900 words
5. Write in English for Filipino audience
6. Make it more engaging and persuasive
7. Include benefits and user experience highlights

Title: {title}

Original content:
{clean_content[:1800]}

Return the improved content:
"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert casino content writer. Create engaging, high-quality content that converts readers into players while maintaining authenticity."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1400,
            temperature=0.7
        )
        
        ai_content = response.choices[0].message.content.strip()
        print(f"✅ AI enhanced content ({len(ai_content)} chars)")
        return ai_content
        
    except Exception as e:
        print(f"⚠️ AI error: {e}")
        return clean_html_content(content)

def clean_html_content(html_content):
    """Làm sạch nội dung HTML"""
    if not html_content:
        return ""
    
    clean_text = re.sub(r'<[^>]+>', '', html_content)
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()
    clean_text = re.sub(r'&#\d+;', '', clean_text)
    
    return clean_text

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
        print(f"Lỗi Google Sheets: {e}")
        return None

def create_or_get_worksheet(spreadsheet, sheet_name):
    """Tạo hoặc lấy worksheet"""
    try:
        worksheet = spreadsheet.worksheet(sheet_name)
        print(f"✅ Found sheet '{sheet_name}'")
        return worksheet
    except gspread.WorksheetNotFound:
        print(f"Creating new sheet: '{sheet_name}'")
        worksheet = spreadsheet.add_worksheet(title=sheet_name, rows=1000, cols=15)
        
        headers = [
            'Source_Title', 'Status', 'Title', 'Content', 'Original_URL', 
            'Image_URL', 'Meta_Title', 'Meta_Desc', 'Import_Date', 
            'Keywords', 'Category', 'Tags', 'Author', 'Notes', 'Custom_Field'
        ]
        worksheet.append_row(headers)
        print(f"✅ Created sheet '{sheet_name}' with headers")
        return worksheet

def extract_keywords_from_content(content, title=""):
    """Trích xuất keywords từ nội dung"""
    if not content and not title:
        return ""
    
    text = f"{title} {content}".lower()
    
    casino_keywords = [
        'casino', 'bonus', 'free spins', 'jackpot', 'slot', 'poker', 
        'blackjack', 'roulette', 'baccarat', 'gaming', 'bet', 'win',
        'deposit', 'withdraw', 'promotion', 'offer', 'deal', 'philippines',
        'gcash', 'maya', 'signup', 'register', 'no deposit', 'free', 'money'
    ]
    
    found_keywords = [kw for kw in casino_keywords if kw in text]
    return ", ".join(found_keywords[:8])

def import_first_5_with_ai():
    """Import 5 bài đầu tiên với AI processing"""
    
    # Setup
    openai_client = setup_openai()
    if not openai_client:
        return
    
    spreadsheet = setup_google_sheets()
    if not spreadsheet:
        return
    
    # Đọc dữ liệu
    try:
        with open('bonus365casinoall_posts.json', 'r', encoding='utf-8') as f:
            posts = json.load(f)
        print(f"Loaded {len(posts)} posts")
    except Exception as e:
        print(f"Error reading JSON: {e}")
        return

    # Tạo sheet mới cho AI test
    sheet_name = "Bonus365AI_Test"
    worksheet = create_or_get_worksheet(spreadsheet, sheet_name)
    
    # Import 5 bài đầu tiên
    test_posts = posts[:5]
    print(f"Importing first 5 posts with AI enhancement...")
    
    for i, post in enumerate(test_posts, 1):
        try:
            title = post.get('title', 'No title')
            print(f"\n[{i}/5] Processing: {title[:50]}...")
            
            # AI processing
            original_content = post.get('content', '')
            print("🤖 ChatGPT enhancing content...")
            ai_content = process_content_with_ai(openai_client, original_content, title)
            
            # Prepare data
            row_data = [
                'Bonus365AI_Test',    # Source_Title
                'ai-enhanced',        # Status
                title,               # Title
                ai_content,          # Content (AI enhanced)
                post.get('link', ''), # Original_URL
                post.get('featured_image', ''),  # Image_URL
                title,               # Meta_Title
                ai_content[:160] + "..." if len(ai_content) > 160 else ai_content,  # Meta_Desc
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # Import_Date
                extract_keywords_from_content(ai_content, title),  # Keywords
                'Casino',            # Category
                'bonus, casino, ai-enhanced, test',  # Tags
                'ChatGPT-3.5',      # Author
                'AI enhanced test import',  # Notes
                'OpenAI'            # Custom_Field
            ]
            
            # Import to sheet
            worksheet.append_row(row_data)
            print(f"✅ Successfully imported post {i}/5")
            
            # Delay between posts
            if i < len(test_posts):
                print("Waiting 5 seconds...")
                time.sleep(5)
                
        except Exception as e:
            print(f"❌ Error with post {i}: {e}")
            continue
    
    print(f"\n🎉 Completed! Imported 5 AI-enhanced posts to sheet '{sheet_name}'")
    print("You can check the results in Google Sheets and then run the full import if satisfied.")

if __name__ == "__main__":
    print("=== IMPORT 5 POSTS WITH AI ENHANCEMENT ===")
    import_first_5_with_ai()
    print("Script completed!")
