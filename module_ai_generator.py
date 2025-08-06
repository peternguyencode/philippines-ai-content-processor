#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MODULE 2: AI CONTENT GENERATOR
Chỉ xử lý việc tạo nội dung bằng AI
"""

import openai
import google.generativeai as genai
import requests
import time
from typing import Dict, Optional, Any
import json

class AIContentGenerator:
    """Module độc lập tạo nội dung AI"""
    
    def __init__(self, openai_key: str, gemini_key: str):
        self.openai_key = openai_key
        self.gemini_key = gemini_key
        self.openai_client = None
        self.gemini_model = None
        self._setup_ai_clients()
    
    def _setup_ai_clients(self):
        """Thiết lập clients AI"""
        try:
            # Setup OpenAI
            self.openai_client = openai.OpenAI(api_key=self.openai_key)
            
            # Setup Gemini
            genai.configure(api_key=self.gemini_key)
            self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
            
            print("✅ [AI GENERATOR] Đã setup AI clients!")
            
        except Exception as e:
            print(f"❌ [AI GENERATOR] Lỗi setup: {str(e)}")
            raise e
    
    def generate_content(self, prompt: str, use_gemini_backup: bool = False) -> Dict[str, Any]:
        """
        Tạo nội dung từ prompt
        Returns: {title, content, meta_title, meta_desc, tags, excerpt}
        """
        try:
            enhanced_prompt = f"""
            Bạn là một chuyên gia viết content tiếng Việt. Tạo một bài viết blog chất lượng cao từ yêu cầu sau:
            
            YÊU CẦU: {prompt}
            
            Hãy trả về JSON với format chính xác sau:
            {{
                "title": "Tiêu đề bài viết hấp dẫn (60-80 ký tự)",
                "content": "Nội dung chi tiết với HTML tags (tối thiểu 800 từ)",
                "meta_title": "SEO title (50-60 ký tự)",
                "meta_desc": "SEO description (150-160 ký tự)",
                "tags": ["tag1", "tag2", "tag3"],
                "excerpt": "Tóm tắt ngắn (100-150 từ)"
            }}
            
            LƯU Ý:
            - Nội dung phải chuyên nghiệp, có cấu trúc rõ ràng
            - Sử dụng HTML tags: <h2>, <h3>, <p>, <strong>, <ul>, <li>
            - Keyword tự nhiên, không spam
            - Phong cách gần gũi người Việt
            """
            
            # Thử OpenAI trước
            if not use_gemini_backup:
                try:
                    return self._generate_with_openai(enhanced_prompt)
                except Exception as e:
                    print(f"⚠️ [AI GENERATOR] OpenAI failed: {str(e)}, switching to Gemini...")
                    use_gemini_backup = True
            
            # Fallback hoặc chọn Gemini
            if use_gemini_backup:
                return self._generate_with_gemini(enhanced_prompt)
                
        except Exception as e:
            print(f"❌ [AI GENERATOR] Lỗi tạo content: {str(e)}")
            return self._get_fallback_content(prompt)
    
    def _generate_with_openai(self, prompt: str) -> Dict[str, Any]:
        """Tạo content với OpenAI"""
        response = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Bạn là chuyên gia viết content tiếng Việt chuyên nghiệp."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.7
        )
        
        content_text = response.choices[0].message.content.strip()
        
        # Parse JSON
        try:
            if content_text.startswith('```json'):
                content_text = content_text.replace('```json', '').replace('```', '').strip()
            
            content_data = json.loads(content_text)
            print("✅ [AI GENERATOR] OpenAI content generated successfully!")
            return content_data
            
        except json.JSONDecodeError:
            print("⚠️ [AI GENERATOR] JSON parse failed, using raw content")
            return self._parse_raw_content(content_text)
    
    def _generate_with_gemini(self, prompt: str) -> Dict[str, Any]:
        """Tạo content với Gemini"""
        response = self.gemini_model.generate_content(prompt)
        content_text = response.text.strip()
        
        # Parse JSON
        try:
            if content_text.startswith('```json'):
                content_text = content_text.replace('```json', '').replace('```', '').strip()
            
            content_data = json.loads(content_text)
            print("✅ [AI GENERATOR] Gemini content generated successfully!")
            return content_data
            
        except json.JSONDecodeError:
            print("⚠️ [AI GENERATOR] JSON parse failed, using raw content")
            return self._parse_raw_content(content_text)
    
    def _parse_raw_content(self, raw_text: str) -> Dict[str, Any]:
        """Parse raw content khi JSON fail"""
        lines = raw_text.split('\n')
        
        return {
            'title': lines[0][:80] if lines else 'Tiêu đề mặc định',
            'content': raw_text,
            'meta_title': lines[0][:60] if lines else 'SEO Title',
            'meta_desc': lines[1][:160] if len(lines) > 1 else 'SEO Description',
            'tags': ['ai', 'content', 'blog'],
            'excerpt': lines[1][:150] if len(lines) > 1 else 'Tóm tắt bài viết'
        }
    
    def _get_fallback_content(self, prompt: str) -> Dict[str, Any]:
        """Content dự phòng khi AI fail"""
        return {
            'title': f'Bài viết về: {prompt[:50]}...',
            'content': f'<p>Nội dung được tạo từ yêu cầu: <strong>{prompt}</strong></p><p>Đây là nội dung dự phòng khi AI không khả dụng.</p>',
            'meta_title': f'SEO: {prompt[:50]}',
            'meta_desc': f'Bài viết chuyên sâu về {prompt[:100]}...',
            'tags': ['blog', 'content'],
            'excerpt': f'Tóm tắt về {prompt[:100]}...'
        }
    
    def generate_image(self, title: str, style: str = "professional") -> Optional[str]:
        """
        Tạo ảnh với DALL-E
        Returns: URL ảnh hoặc None nếu fail
        """
        try:
            image_prompt = f"""
            Create a professional blog featured image for an article titled: "{title}"
            
            Style: {style}, clean, modern, Vietnamese blog style
            No text overlay, high quality, 1200x630 pixels aspect ratio
            Colors: professional, eye-catching but not overwhelming
            """
            
            response = self.openai_client.images.generate(
                model="dall-e-3",
                prompt=image_prompt,
                size="1792x1024",
                quality="standard",
                n=1
            )
            
            image_url = response.data[0].url
            print(f"✅ [AI GENERATOR] Generated image: {image_url}")
            return image_url
            
        except Exception as e:
            print(f"❌ [AI GENERATOR] Lỗi tạo ảnh: {str(e)}")
            return None
    
    def download_image(self, image_url: str, filename: str) -> Optional[bytes]:
        """Download ảnh từ URL"""
        try:
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()
            
            print(f"✅ [AI GENERATOR] Downloaded image: {filename}")
            return response.content
            
        except Exception as e:
            print(f"❌ [AI GENERATOR] Lỗi download ảnh: {str(e)}")
            return None

# Test module
if __name__ == "__main__":
    from config import Config
    
    # Test AI Generator
    ai_gen = AIContentGenerator(
        openai_key=Config.OPENAI_API_KEY or "",
        gemini_key=Config.GEMINI_API_KEY or ""
    )
    
    # Test tạo content
    test_prompt = "Viết về lợi ích của AI trong marketing"
    content = ai_gen.generate_content(test_prompt)
    
    print("Generated content keys:", list(content.keys()))
    print("Title:", content.get('title', 'N/A'))
    print("Content preview:", content.get('content', '')[:200] + "...")
    
    # Test tạo ảnh
    if content.get('title'):
        image_url = ai_gen.generate_image(content['title'])
        if image_url:
            print(f"Image URL: {image_url}")
