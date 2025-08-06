#!/usr/bin/env python3
# -*- coding: utf-8 -*-

print("🔥 TEST API KEYS")
print("=" * 30)

# Test import libraries
try:
    import openai
    print("✅ OpenAI library imported")
except ImportError as e:
    print(f"❌ OpenAI import error: {e}")

try:
    import google.generativeai as genai
    print("✅ Google Generative AI library imported")
except ImportError as e:
    print(f"❌ Gemini import error: {e}")

try:
    from dotenv import load_dotenv
    print("✅ python-dotenv imported")
except ImportError as e:
    print(f"❌ dotenv import error: {e}")

# Test environment variables
import os
load_dotenv()

openai_key = os.getenv('OPENAI_API_KEY')
gemini_key = os.getenv('GEMINI_API_KEY')

print(f"\n🔑 API KEYS STATUS:")
print(f"OpenAI Key: {'✅ Configured' if openai_key else '❌ Missing'}")
print(f"Gemini Key: {'✅ Configured' if gemini_key else '❌ Missing'}")

if openai_key:
    print(f"OpenAI Key preview: {openai_key[:20]}...")

if gemini_key:
    print(f"Gemini Key preview: {gemini_key[:20]}...")

# Test OpenAI API
if openai_key:
    try:
        from openai import OpenAI
        client = OpenAI(api_key=openai_key)
        
        # Test simple completion
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello! Please respond with just 'API working'"}],
            max_tokens=10
        )
        print(f"🤖 OpenAI Test: {response.choices[0].message.content}")
        
    except Exception as e:
        print(f"❌ OpenAI API Error: {str(e)}")

# Test Gemini API  
if gemini_key:
    try:
        import google.generativeai as genai
        genai.configure(api_key=gemini_key)
        
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Hello! Please respond with just 'API working'")
        print(f"🤖 Gemini Test: {response.text}")
        
    except Exception as e:
        print(f"❌ Gemini API Error: {str(e)}")

print("\n✅ Test completed!")
