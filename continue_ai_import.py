#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tiếp tục import các bài còn lại với AI processing
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
Rewrite this casino/bonus article for Filipino players. Make it professional, engaging, and trustworthy.

Goals:
- Keep all key information and casino terms
- Improve readability and flow
- Add compelling calls-to-action
- 800-1000 words target
- Professional tone for Philippines market
- Include safety and trust elements

Title: {title}

Original content:
{clean_content[:2000]}

Rewritten content:
"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert casino content writer for the Philippines market. Create trustworthy, engaging content that helps users while driving conversions."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
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

def continue_import():
    """Tiếp tục import các bài còn lại"""
    
    # Setup
    openai_client = setup_openai()
    if not openai_client:
        return
    
    spreadsheet = setup_google_sheets()
    if not spreadsheet:
        return
    
    # Load data
    try:
        with open('bonus365casinoall_posts.json', 'r', encoding='utf-8') as f:
            posts = json.load(f)
        print(f"Loaded {len(posts)} posts")
    except Exception as e:
        print(f"Error loading JSON: {e}")
        return

    # Get existing sheet
    try:
        worksheet = spreadsheet.worksheet('bonus365casinoall_AI')
        print("✅ Found existing AI sheet")
    except:
        print("❌ AI sheet not found. Run full_import_with_ai.py first")
        return
    
    # Check what's already imported
    existing_titles = get_existing_titles(worksheet)
    remaining_posts = [p for p in posts if p.get('title', '').strip() not in existing_titles]
    
    print(f"Already imported: {len(existing_titles)}")
    print(f"Remaining to import: {len(remaining_posts)}")
    
    if not remaining_posts:
        print("✅ All posts already imported!")
        return
    
    # Continue import
    imported = 0
    total = len(remaining_posts)
    
    print(f"\n🚀 Continuing AI-enhanced import of {total} remaining posts...")
    
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
                'bonus365casinoall_AI',  # Source_Title
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
                'AI enhanced continuation',
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
                        print(f"⚠️ Rate limit, waiting 15s... (retry {retry_count}/{max_retries})")
                        time.sleep(15)
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
                print("Waiting 6 seconds...")
                time.sleep(6)
                
        except KeyboardInterrupt:
            print(f"\n⚠️ Stopped by user. Imported {imported}/{total}")
            break
        except Exception as e:
            print(f"❌ Error with post {i}: {e}")
            continue
    
    print(f"\n🎉 COMPLETED! Imported {imported}/{total} additional AI-enhanced posts")
    print(f"Total posts in sheet: {len(existing_titles) + imported}")
    print("All content enhanced by ChatGPT!")

if __name__ == "__main__":
    print("=== CONTINUE AI-ENHANCED IMPORT ===")
    continue_import()
    print("Script finished!")
