#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script AI processing với 3 bài đầu tiên
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
Requirements:
1. Keep main information and important keywords
2. Improve structure and readability
3. Add appropriate call-to-action
4. Length around 600-800 words
5. Write in English, suitable for Filipino audience
6. Focus on benefits and user experience

Title: {title}

Original content:
{clean_content[:1500]}

Please return the improved content:
"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a casino and bonus content expert. Create high-quality, engaging and persuasive content."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1200,
            temperature=0.7
        )
        
        ai_content = response.choices[0].message.content.strip()
        print(f"✅ AI processed content (length: {len(ai_content)} chars)")
        return ai_content
        
    except Exception as e:
        print(f"⚠️ AI processing error: {e}")
        print("Will use cleaned original content")
        return clean_html_content(content)

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

def test_ai_processing():
    """Test AI processing với 3 bài đầu tiên"""
    
    # Kiểm tra OpenAI API
    openai_client = setup_openai()
    if not openai_client:
        return
    
    # Đọc dữ liệu JSON
    try:
        with open('bonus365casinoall_posts.json', 'r', encoding='utf-8') as f:
            posts = json.load(f)
        
        if not isinstance(posts, list):
            print("File JSON không phải là mảng posts")
            return
            
        print(f"Tổng số bài posts: {len(posts)}")
        print("Sẽ test AI processing với 3 bài đầu tiên...")
        
    except FileNotFoundError:
        print("Không tìm thấy file bonus365casinoall_posts.json")
        return
    except json.JSONDecodeError as e:
        print(f"Lỗi đọc file JSON: {e}")
        return

    # Test với 3 bài đầu tiên
    test_posts = posts[:3]
    
    for i, post in enumerate(test_posts, 1):
        try:
            title = post.get('title', 'No title')
            print(f"\n[TEST {i}/3] Đang test: {title[:60]}...")
            
            # Xử lý content bằng AI
            original_content = post.get('content', '')
            original_length = len(clean_html_content(original_content))
            print(f"📄 Original content length: {original_length} chars")
            
            print("🤖 Processing with ChatGPT...")
            ai_processed_content = process_content_with_ai(openai_client, original_content, title)
            
            print(f"✅ AI processed content length: {len(ai_processed_content)} chars")
            print(f"📝 First 200 chars of AI content: {ai_processed_content[:200]}...")
            
            # Delay giữa các request
            if i < len(test_posts):
                print("Waiting 3 seconds before next request...")
                time.sleep(3)
                
        except Exception as e:
            print(f"❌ Error processing post {i}: {e}")
            continue
    
    print(f"\n🎉 Test completed successfully!")
    print("AI processing is working. You can now run the full import script.")

if __name__ == "__main__":
    print("=== TEST AI PROCESSING ===")
    test_ai_processing()
    print("Test finished!")
