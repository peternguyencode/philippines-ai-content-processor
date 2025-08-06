#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test AI Content Generation - Không cần Google Sheets hay WordPress
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ai_helper import AIHelper

def test_ai_content():
    """Test sinh content với AI"""
    print("🤖 TEST AI CONTENT GENERATION")
    print("=" * 40)
    
    try:
        ai = AIHelper()
        
        # Test prompt
        test_prompt = "Viết bài về lợi ích của AI trong marketing cho doanh nghiệp nhỏ"
        
        print(f"📝 Prompt: {test_prompt}")
        print("\n🔄 Đang sinh content...")
        
        # Sinh content
        result = ai.generate_content(test_prompt)
        
        if result:
            print(f"\n✅ THÀNH CÔNG!")
            print(f"Title: {result.get('title', 'N/A')}")
            print(f"Content preview: {result.get('content', '')[:200]}...")
            print(f"Image prompt: {result.get('image_prompt', 'N/A')}")
            print(f"Meta title: {result.get('meta_title', 'N/A')}")
            print(f"Meta desc: {result.get('meta_description', 'N/A')}")
            
            # Test sinh ảnh
            if result.get('image_prompt'):
                print(f"\n🎨 Đang sinh ảnh...")
                image_url = ai.generate_image(result['image_prompt'])
                if image_url:
                    print(f"✅ Ảnh đã sinh: {image_url}")
                else:
                    print("❌ Không sinh được ảnh")
        else:
            print("❌ Không sinh được content")
            
    except Exception as e:
        print(f"❌ Lỗi: {str(e)}")

if __name__ == "__main__":
    test_ai_content()
