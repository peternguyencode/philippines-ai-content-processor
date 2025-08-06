#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script import toàn bộ dữ liệu với AI processing
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
    print("✅ OpenAI API ready")
    return client

def process_content_with_ai(client, content, title):
    """Xử lý content bằng ChatGPT"""
    try:
        clean_content = clean_html_content(content)
        
        if len(clean_content) < 100:
            return clean_content
        
        prompt = f"""
Rewrite and enhance this casino/bonus content for Filipino players. Make it more engaging, professional, and conversion-focused.

Requirements:
- Keep all important information and keywords
- Improve readability and structure  
- Add compelling call-to-actions
- Target length: 800-1000 words
- Professional tone for Filipino audience
- Focus on benefits and user experience
- Include trust signals and safety aspects

Title: {title}

Content to enhance:
{clean_content[:2000]}

Enhanced content:
"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional casino content writer specializing in the Philippines market. Create compelling, trustworthy content that converts while being helpful to users."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1600,
            temperature=0.6
        )
        
        ai_content = response.choices[0].message.content.strip()
        print(f"✅ AI enhanced ({len(ai_content)} chars)")
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
        print(f"Google Sheets error: {e}")
        return None

def create_or_get_worksheet(spreadsheet, sheet_name):
    """Tạo hoặc lấy worksheet"""
    try:
        worksheet = spreadsheet.worksheet(sheet_name)
        print(f"✅ Found sheet '{sheet_name}'")
        return worksheet
    except gspread.WorksheetNotFound:
        print(f"Creating sheet: '{sheet_name}'")
        worksheet = spreadsheet.add_worksheet(title=sheet_name, rows=1000, cols=15)
        
        headers = [
            'Source_Title', 'Status', 'Title', 'Content', 'Original_URL', 
            'Image_URL', 'Meta_Title', 'Meta_Desc', 'Import_Date', 
            'Keywords', 'Category', 'Tags', 'Author', 'Notes', 'Custom_Field'
        ]
        worksheet.append_row(headers)
        print(f"✅ Created '{sheet_name}' with headers")
        return worksheet

def extract_keywords_from_content(content, title=""):
    """Trích xuất keywords"""
    if not content and not title:
        return ""
    
    text = f"{title} {content}".lower()
    
    keywords = [
        'casino', 'bonus', 'free spins', 'jackpot', 'slot', 'poker', 
        'blackjack', 'roulette', 'baccarat', 'gaming', 'bet', 'win',
        'deposit', 'withdraw', 'promotion', 'offer', 'deal', 'philippines',
        'gcash', 'maya', 'signup', 'register', 'no deposit', 'free', 'money',
        'masaya', '365', 'login', 'app', 'mobile', 'safe', 'secure'
    ]
    
    found = [kw for kw in keywords if kw in text]
    return ", ".join(found[:10])

def get_existing_titles(worksheet):
    """Lấy titles đã có để tránh trùng lặp"""
    try:
        titles = worksheet.col_values(3)
        return titles[1:] if len(titles) > 1 else []
    except:
        return []

def full_import_with_ai(json_file):
    """Import toàn bộ với AI processing"""
    
    # Setup
    openai_client = setup_openai()
    if not openai_client:
        return
    
    spreadsheet = setup_google_sheets()
    if not spreadsheet:
        return
    
    # Load data
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            posts = json.load(f)
        print(f"Loaded {len(posts)} posts from {json_file}")
    except Exception as e:
        print(f"Error loading {json_file}: {e}")
        return

    # Create sheet
    sheet_name = json_file.replace('.json', '').replace('_posts', '').replace('_', '') + "_AI"
    worksheet = create_or_get_worksheet(spreadsheet, sheet_name)
    
    # Check existing
    existing_titles = get_existing_titles(worksheet)
    remaining_posts = [p for p in posts if p.get('title', '').strip() not in existing_titles]
    
    print(f"Existing: {len(existing_titles)}, New to import: {len(remaining_posts)}")
    
    if not remaining_posts:
        print("All posts already imported!")
        return
    
    # Import with AI
    imported = 0
    total = len(remaining_posts)
    
    print(f"\n🚀 Starting AI-enhanced import of {total} posts...")
    
    for i, post in enumerate(remaining_posts, 1):
        try:
            title = post.get('title', 'No title')
            print(f"\n[{i}/{total}] {title[:60]}...")
            
            # AI enhancement
            original_content = post.get('content', '')
            print("🤖 AI enhancing...")
            ai_content = process_content_with_ai(openai_client, original_content, title)
            
            # Prepare row
            row_data = [
                sheet_name,          # Source_Title
                'ai-enhanced',       # Status
                title,              # Title
                ai_content,         # Content (AI enhanced)
                post.get('link', ''), # Original_URL
                post.get('featured_image', ''),  # Image_URL
                title,              # Meta_Title
                ai_content[:160] + "..." if len(ai_content) > 160 else ai_content,
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                extract_keywords_from_content(ai_content, title),
                'Casino',
                'bonus, casino, ai-enhanced, philippines',
                'ChatGPT-3.5',
                f'AI enhanced from {json_file}',
                'OpenAI-Enhanced'
            ]
            
            # Import with retry
            retry_count = 0
            max_retries = 3
            
            while retry_count < max_retries:
                try:
                    worksheet.append_row(row_data)
                    imported += 1
                    print(f"✅ Imported {i}/{total}")
                    break
                    
                except Exception as e:
                    retry_count += 1
                    if "quota" in str(e).lower() or "429" in str(e):
                        print(f"⚠️ Rate limit, waiting 20s... (retry {retry_count}/{max_retries})")
                        time.sleep(20)
                    else:
                        print(f"❌ Error: {e}")
                        if retry_count < max_retries:
                            print(f"Retrying... ({retry_count}/{max_retries})")
                            time.sleep(5)
                        else:
                            print("Skipping after max retries")
                            break
            
            # Delay between posts
            if i < total:
                print("Waiting 8 seconds...")
                time.sleep(8)
                
        except KeyboardInterrupt:
            print(f"\n⚠️ Stopped by user. Imported {imported}/{total}")
            break
        except Exception as e:
            print(f"❌ Error with post {i}: {e}")
            continue
    
    print(f"\n🎉 COMPLETED! Imported {imported}/{total} AI-enhanced posts")
    print(f"Sheet: '{sheet_name}' in Google Sheets")
    print("All content has been enhanced by ChatGPT for better quality!")

if __name__ == "__main__":
    print("=== FULL IMPORT WITH AI ENHANCEMENT ===")
    
    json_file = input("Enter JSON filename (default: bonus365casinoall_posts.json): ").strip()
    if not json_file:
        json_file = "bonus365casinoall_posts.json"
    
    confirm = input(f"Import all posts from '{json_file}' with AI enhancement? (y/N): ").strip().lower()
    if confirm == 'y':
        print(f"Starting full AI-enhanced import...")
        full_import_with_ai(json_file)
    else:
        print("Cancelled.")
    
    print("Script finished!")
