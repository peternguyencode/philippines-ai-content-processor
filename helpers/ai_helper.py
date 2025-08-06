import openai
import google.generativeai as genai
import requests
import time
import base64
from io import BytesIO
from typing import Optional, Dict, Any
from config import Config

class AIHelper:
    """Lớp xử lý AI để sinh content, title, meta và ảnh"""
    
    def __init__(self):
        self._setup_apis()
    
    def _setup_apis(self):
        """Thiết lập API keys cho các AI provider"""
        # Setup OpenAI
        if Config.OPENAI_API_KEY:
            self.openai_client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
            print("✅ Đã thiết lập OpenAI API")
        
        # Setup Gemini
        if Config.GEMINI_API_KEY:
            genai.configure(api_key=Config.GEMINI_API_KEY)
            print("✅ Đã thiết lập Gemini API")
    
    def generate_content(self, prompt: str, provider: str = None) -> Dict[str, Any]:
        """
        Sinh nội dung bài viết từ prompt
        Returns: {
            'title': str,
            'content': str,
            'image_prompt': str,
            'meta_title': str,
            'meta_description': str
        }
        """
        provider = provider or Config.DEFAULT_AI_PROVIDER
        
        try:
            # Tạo prompt chi tiết
            detailed_prompt = f"""
            Hãy viết một bài blog chất lượng cao dựa trên yêu cầu sau: "{prompt}"
            
            Yêu cầu:
            1. Tạo tiêu đề hấp dẫn (dưới 60 ký tự)
            2. Viết nội dung chi tiết, hữu ích (khoảng {Config.MAX_CONTENT_LENGTH} từ)
            3. Tạo prompt để sinh ảnh cover phù hợp
            4. Tạo meta title SEO (dưới 60 ký tự)
            5. Tạo meta description SEO (dưới 160 ký tự)
            
            Trả về theo format JSON:
            {{
                "title": "Tiêu đề bài viết",
                "content": "Nội dung bài viết đầy đủ với HTML tags",
                "image_prompt": "Mô tả ảnh để sinh bằng AI",
                "meta_title": "Meta title SEO",
                "meta_description": "Meta description SEO"
            }}
            """
            
            if provider == 'openai':
                return self._generate_with_openai(detailed_prompt)
            elif provider == 'gemini':
                return self._generate_with_gemini(detailed_prompt)
            else:
                raise ValueError(f"Provider không hỗ trợ: {provider}")
                
        except Exception as e:
            print(f"❌ Lỗi sinh content: {str(e)}")
            return self._create_error_response(str(e))
    
    def _generate_with_openai(self, prompt: str) -> Dict[str, Any]:
        """Sinh content bằng OpenAI GPT"""
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Bạn là một copywriter chuyên nghiệp, viết tiếng Việt tự nhiên và hấp dẫn."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=3000,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            
            # Parse JSON response
            import json
            try:
                if content:
                    result = json.loads(content)
                    return result
                else:
                    return self._create_error_response("No content returned")
            except json.JSONDecodeError:
                # Nếu không parse được JSON, tạo response thủ công
                if content:
                    return self._parse_text_response(content)
                else:
                    return self._create_error_response("Empty response")
                
        except Exception as e:
            print(f"❌ Lỗi OpenAI: {str(e)}")
            raise e
    
    def _generate_with_gemini(self, prompt: str) -> Dict[str, Any]:
        """Sinh content bằng Google Gemini"""
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            
            content = response.text
            
            # Parse JSON response
            import json
            try:
                result = json.loads(content)
                return result
            except json.JSONDecodeError:
                return self._parse_text_response(content)
                
        except Exception as e:
            print(f"❌ Lỗi Gemini: {str(e)}")
            raise e
    
    def _parse_text_response(self, text: str) -> Dict[str, Any]:
        """Parse response khi không có JSON format"""
        lines = text.split('\n')
        
        # Logic đơn giản để extract thông tin
        title = lines[0].strip() if lines else "Tiêu đề mặc định"
        content = text
        
        return {
            'title': title[:60],
            'content': content,
            'image_prompt': f"Professional illustration about {title}",
            'meta_title': title[:60],
            'meta_description': content[:160] + "..." if len(content) > 160 else content
        }
    
    def generate_image(self, prompt: str, provider: str = None) -> Optional[str]:
        """
        Sinh ảnh từ prompt
        Returns: URL của ảnh đã sinh
        """
        provider = provider or Config.IMAGE_AI_PROVIDER
        
        try:
            if provider == 'openai':
                return self._generate_image_openai(prompt)
            elif provider == 'gemini':
                # Gemini chưa hỗ trợ sinh ảnh, dùng OpenAI backup
                return self._generate_image_openai(prompt)
            else:
                raise ValueError(f"Image provider không hỗ trợ: {provider}")
                
        except Exception as e:
            print(f"❌ Lỗi sinh ảnh: {str(e)}")
            return None
    
    def _generate_image_openai(self, prompt: str) -> Optional[str]:
        """Sinh ảnh bằng DALL-E"""
        try:
            # Tối ưu prompt cho DALL-E
            optimized_prompt = f"""
            {prompt}, professional quality, high resolution, 
            clean design, suitable for blog cover image, 
            vibrant colors, modern style
            """
            
            response = self.openai_client.images.generate(
                model="dall-e-3",
                prompt=optimized_prompt,
                size="1024x1024",  # Fixed size for DALL-E 3
                quality="standard",
                n=1
            )
            
            image_url = response.data[0].url if response.data else None
            if image_url:
                print(f"✅ Đã sinh ảnh: {image_url}")
                return image_url
            else:
                return None
            
        except Exception as e:
            print(f"❌ Lỗi DALL-E: {str(e)}")
            return None
    
    def _create_error_response(self, error_msg: str) -> Dict[str, Any]:
        """Tạo response lỗi mặc định"""
        return {
            'title': 'Lỗi sinh content',
            'content': f'Có lỗi xảy ra: {error_msg}',
            'image_prompt': 'Error illustration',
            'meta_title': 'Lỗi',
            'meta_description': 'Có lỗi xảy ra khi sinh content'
        }
    
    def optimize_for_seo(self, title: str, content: str) -> Dict[str, str]:
        """Tối ưu SEO cho title và content"""
        try:
            seo_prompt = f"""
            Hãy tối ưu SEO cho bài viết sau:
            Tiêu đề: {title}
            Nội dung: {content[:500]}...
            
            Tạo:
            1. Meta title tối ưu SEO (dưới 60 ký tự)
            2. Meta description hấp dẫn (dưới 160 ký tự)
            3. Đề xuất từ khóa chính
            
            Trả về JSON format:
            {{
                "meta_title": "...",
                "meta_description": "...",
                "keywords": "..."
            }}
            """
            
            if Config.DEFAULT_AI_PROVIDER == 'openai':
                response = self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": seo_prompt}],
                    max_tokens=500
                )
                content = response.choices[0].message.content or ""
            else:
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(seo_prompt)
                content = response.text
            
            import json
            return json.loads(content)
            
        except Exception as e:
            print(f"❌ Lỗi tối ưu SEO: {str(e)}")
            return {
                'meta_title': title[:60],
                'meta_description': content[:160],
                'keywords': ''
            }

# Test function
if __name__ == "__main__":
    try:
        Config.validate_config()
        ai = AIHelper()
        
        # Test sinh content
        test_prompt = "Viết bài về lợi ích của AI trong marketing"
        result = ai.generate_content(test_prompt)
        
        print("📝 Kết quả sinh content:")
        print(f"Title: {result.get('title')}")
        print(f"Content length: {len(result.get('content', ''))}")
        print(f"Image prompt: {result.get('image_prompt')}")
        
        # Test sinh ảnh
        if result.get('image_prompt'):
            image_url = ai.generate_image(result['image_prompt'])
            print(f"🖼️ Image URL: {image_url}")
            
    except Exception as e:
        print(f"Lỗi test: {str(e)}")
