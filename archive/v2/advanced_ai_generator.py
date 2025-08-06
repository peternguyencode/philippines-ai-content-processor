#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
V2 - MODULE 2: ADVANCED AI CONTENT GENERATOR  
Cải tiến: Multi-provider support, Content templates, Image optimization, Quality scoring
"""

import openai
import google.generativeai as genai
import requests
import time
import json
import asyncio
import aiohttp
from typing import Dict, Optional, Any, List, Union, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import hashlib
import re
from datetime import datetime
import tempfile
import os

class AIProvider(Enum):
    OPENAI = "openai"
    GEMINI = "gemini"
    CLAUDE = "claude"  # Future support

class ContentType(Enum):
    BLOG_POST = "blog_post"
    PRODUCT_REVIEW = "product_review"
    NEWS_ARTICLE = "news_article"
    TUTORIAL = "tutorial"
    MARKETING = "marketing"

@dataclass
class ContentRequest:
    """Structured content request"""
    prompt: str
    content_type: ContentType = ContentType.BLOG_POST
    target_words: int = 800
    language: str = "vi"
    tone: str = "professional"
    keywords: List[str] = None
    include_image: bool = True
    seo_focus: bool = True
    
    def __post_init__(self):
        if self.keywords is None:
            self.keywords = []

@dataclass  
class ContentResult:
    """Structured content result"""
    title: str
    content: str
    meta_title: str
    meta_desc: str
    tags: List[str]
    excerpt: str
    word_count: int
    quality_score: float
    image_url: Optional[str] = None
    image_alt: Optional[str] = None
    provider_used: str = "unknown"
    generation_time: float = 0.0
    
class AdvancedAIGenerator:
    """V2 - Advanced AI Content Generator với multi-provider và quality control"""
    
    def __init__(self, openai_key: str, gemini_key: str, claude_key: str = None):
        self.providers = {}
        self.content_templates = self._load_content_templates()
        self.quality_thresholds = {
            'min_words': 400,
            'max_words': 3000,
            'min_quality_score': 0.6,
            'required_sections': ['title', 'content', 'meta_title', 'meta_desc']
        }
        
        # Performance tracking
        self.stats = {
            'total_requests': 0,
            'successful_generations': 0,
            'provider_usage': {},
            'avg_quality_score': 0.0,
            'avg_generation_time': 0.0,
            'cache_hits': 0
        }
        
        # Content cache
        self._content_cache = {}
        
        self._setup_providers(openai_key, gemini_key, claude_key)
    
    def _setup_providers(self, openai_key: str, gemini_key: str, claude_key: str = None):
        """Setup AI providers với error handling"""
        # Setup OpenAI
        if openai_key:
            try:
                self.providers[AIProvider.OPENAI] = openai.OpenAI(api_key=openai_key)
                print("✅ [AI GEN V2] OpenAI client initialized")
            except Exception as e:
                print(f"⚠️ [AI GEN V2] OpenAI setup failed: {str(e)}")
        
        # Setup Gemini
        if gemini_key:
            try:
                genai.configure(api_key=gemini_key)
                self.providers[AIProvider.GEMINI] = genai.GenerativeModel('gemini-1.5-flash')
                print("✅ [AI GEN V2] Gemini client initialized")
            except Exception as e:
                print(f"⚠️ [AI GEN V2] Gemini setup failed: {str(e)}")
        
        # Future: Claude support
        if claude_key and False:  # Disabled for now
            try:
                # self.providers[AIProvider.CLAUDE] = claude_client
                print("✅ [AI GEN V2] Claude client initialized")
            except Exception as e:
                print(f"⚠️ [AI GEN V2] Claude setup failed: {str(e)}")
        
        print(f"🤖 [AI GEN V2] Initialized {len(self.providers)} AI providers")
    
    def _load_content_templates(self) -> Dict[ContentType, str]:
        """Load content templates cho từng loại content"""
        return {
            ContentType.BLOG_POST: """
            Tạo một bài viết blog chuyên nghiệp về: {prompt}
            
            YÊU CẦU:
            - Tiêu đề hấp dẫn, tối ưu SEO (60-80 ký tự)
            - Nội dung chi tiết {target_words}+ từ
            - Tone: {tone}, ngôn ngữ: {language}
            - Keywords: {keywords}
            - Cấu trúc: Mở đầu → Nội dung chính → Kết luận
            - Sử dụng HTML tags: <h2>, <h3>, <p>, <strong>, <ul>, <li>
            
            ĐỊNH DẠNG JSON:
            {{
                "title": "Tiêu đề chính (60-80 ký tự)",
                "content": "Nội dung HTML đầy đủ với các thẻ",
                "meta_title": "SEO title (50-60 ký tự)", 
                "meta_desc": "SEO description (150-160 ký tự)",
                "tags": ["tag1", "tag2", "tag3", "tag4", "tag5"],
                "excerpt": "Tóm tắt hấp dẫn (100-150 từ)"
            }}
            """,
            
            ContentType.PRODUCT_REVIEW: """
            Viết đánh giá sản phẩm chi tiết về: {prompt}
            
            YÊU CẦU:
            - Đánh giá trung thực, khách quan
            - Ưu điểm, nhược điểm rõ ràng
            - So sánh với sản phẩm tương tự
            - Khuyến nghị mua/không mua
            - {target_words}+ từ
            
            [Same JSON format]
            """,
            
            ContentType.TUTORIAL: """
            Tạo hướng dẫn step-by-step về: {prompt}
            
            YÊU CẦU:
            - Các bước thực hiện rõ ràng, dễ theo dõi
            - Screenshots/hình ảnh minh họa (nếu cần)
            - Tips và troubleshooting
            - {target_words}+ từ
            
            [Same JSON format]
            """,
            
            ContentType.NEWS_ARTICLE: """
            Viết bài báo tin tức về: {prompt}
            
            YÊU CẦU:
            - Lead paragraph với 5W1H
            - Thông tin cập nhật, chính xác
            - Quotes từ các nguồn
            - Tone trung thực, khách quan
            - {target_words}+ từ
            
            [Same JSON format]
            """,
            
            ContentType.MARKETING: """
            Tạo content marketing về: {prompt}
            
            YÊU CẦU:
            - Call-to-action mạnh mẽ
            - Benefits rõ ràng cho khách hàng
            - Social proof, testimonials
            - Tone thuyết phục nhưng không spam
            - {target_words}+ từ
            
            [Same JSON format]
            """
        }
    
    def generate_content(self, request: Union[ContentRequest, str], 
                        preferred_provider: AIProvider = None) -> ContentResult:
        """
        Advanced content generation với quality control
        """
        start_time = time.time()
        self.stats['total_requests'] += 1
        
        # Convert string to ContentRequest nếu cần
        if isinstance(request, str):
            request = ContentRequest(prompt=request)
        
        # Check cache
        cache_key = self._generate_cache_key(request)
        if cache_key in self._content_cache:
            self.stats['cache_hits'] += 1
            cached_result = self._content_cache[cache_key]
            print(f"📋 [AI GEN V2] Using cached content for: {request.prompt[:50]}...")
            return cached_result
        
        # Select provider
        provider = self._select_best_provider(preferred_provider)
        if not provider:
            raise Exception("No AI providers available")
        
        try:
            # Generate content
            content_result = self._generate_with_provider(provider, request)
            
            # Quality check
            quality_score = self._calculate_quality_score(content_result, request)
            content_result.quality_score = quality_score
            
            # Retry với provider khác nếu quality thấp
            if quality_score < self.quality_thresholds['min_quality_score']:
                print(f"⚠️ [AI GEN V2] Low quality score: {quality_score:.2f}, retrying...")
                alternative_provider = self._get_alternative_provider(provider)
                if alternative_provider:
                    retry_result = self._generate_with_provider(alternative_provider, request)
                    retry_quality = self._calculate_quality_score(retry_result, request)
                    
                    if retry_quality > quality_score:
                        content_result = retry_result
                        content_result.quality_score = retry_quality
                        provider = alternative_provider
            
            # Update stats
            generation_time = time.time() - start_time
            content_result.generation_time = generation_time
            content_result.provider_used = provider.value
            
            self._update_stats(provider, quality_score, generation_time)
            
            # Cache result
            self._content_cache[cache_key] = content_result
            
            print(f"✅ [AI GEN V2] Generated content (Quality: {quality_score:.2f}, Time: {generation_time:.1f}s)")
            return content_result
            
        except Exception as e:
            print(f"❌ [AI GEN V2] Generation failed: {str(e)}")
            return self._create_fallback_content(request)
    
    def _generate_cache_key(self, request: ContentRequest) -> str:
        """Generate cache key from request"""
        key_data = {
            'prompt': request.prompt,
            'content_type': request.content_type.value,
            'target_words': request.target_words,
            'language': request.language,
            'tone': request.tone,
            'keywords': sorted(request.keywords)
        }
        key_string = json.dumps(key_data, sort_keys=True)
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def _select_best_provider(self, preferred: AIProvider = None) -> Optional[AIProvider]:
        """Select best available provider"""
        if preferred and preferred in self.providers:
            return preferred
        
        # Priority order based on performance
        priority_order = [AIProvider.OPENAI, AIProvider.GEMINI, AIProvider.CLAUDE]
        
        for provider in priority_order:
            if provider in self.providers:
                return provider
        
        return None
    
    def _get_alternative_provider(self, current: AIProvider) -> Optional[AIProvider]:
        """Get alternative provider for retry"""
        alternatives = [p for p in self.providers.keys() if p != current]
        return alternatives[0] if alternatives else None
    
    def _generate_with_provider(self, provider: AIProvider, request: ContentRequest) -> ContentResult:
        """Generate content với specific provider"""
        template = self.content_templates[request.content_type]
        
        formatted_prompt = template.format(
            prompt=request.prompt,
            target_words=request.target_words,
            language=request.language, 
            tone=request.tone,
            keywords=", ".join(request.keywords) if request.keywords else "không có"
        )
        
        if provider == AIProvider.OPENAI:
            return self._generate_with_openai(formatted_prompt, request)
        elif provider == AIProvider.GEMINI:
            return self._generate_with_gemini(formatted_prompt, request)
        else:
            raise Exception(f"Provider {provider.value} not implemented")
    
    def _generate_with_openai(self, prompt: str, request: ContentRequest) -> ContentResult:
        """Generate với OpenAI"""
        client = self.providers[AIProvider.OPENAI]
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Bạn là chuyên gia viết content tiếng Việt. Luôn trả về JSON hợp lệ."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2500,
            temperature=0.7
        )
        
        content_text = response.choices[0].message.content.strip()
        return self._parse_content_response(content_text, request)
    
    def _generate_with_gemini(self, prompt: str, request: ContentRequest) -> ContentResult:
        """Generate với Gemini"""
        model = self.providers[AIProvider.GEMINI]
        
        response = model.generate_content(prompt)
        content_text = response.text.strip()
        return self._parse_content_response(content_text, request)
    
    def _parse_content_response(self, response_text: str, request: ContentRequest) -> ContentResult:
        """Parse AI response thành ContentResult"""
        try:
            # Clean JSON from response
            if response_text.startswith('```json'):
                response_text = response_text.replace('```json', '').replace('```', '').strip()
            
            # Try to extract JSON from text
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                response_text = json_match.group(0)
            
            content_data = json.loads(response_text)
            
            # Validate required fields
            required_fields = ['title', 'content', 'meta_title', 'meta_desc', 'tags', 'excerpt']
            for field in required_fields:
                if field not in content_data:
                    content_data[field] = f"Generated {field}"
            
            # Count words
            word_count = len(re.findall(r'\w+', content_data['content']))
            
            return ContentResult(
                title=content_data['title'][:100],  # Limit length
                content=content_data['content'],
                meta_title=content_data['meta_title'][:60],
                meta_desc=content_data['meta_desc'][:160], 
                tags=content_data['tags'][:8] if isinstance(content_data['tags'], list) else [],
                excerpt=content_data['excerpt'][:200],
                word_count=word_count,
                quality_score=0.0  # Will be calculated later
            )
            
        except (json.JSONDecodeError, KeyError) as e:
            print(f"⚠️ [AI GEN V2] Parse error: {str(e)}, using fallback parser")
            return self._parse_raw_content(response_text, request)
    
    def _parse_raw_content(self, raw_text: str, request: ContentRequest) -> ContentResult:
        """Fallback parser cho raw text"""
        lines = [line.strip() for line in raw_text.split('\n') if line.strip()]
        
        title = lines[0][:80] if lines else f"Về {request.prompt}"
        content = raw_text
        word_count = len(re.findall(r'\w+', content))
        
        return ContentResult(
            title=title,
            content=f"<p>{content}</p>",
            meta_title=title[:60],
            meta_desc=lines[1][:160] if len(lines) > 1 else f"Bài viết về {request.prompt}",
            tags=['ai-generated', 'content'],
            excerpt=lines[1][:150] if len(lines) > 1 else content[:150],
            word_count=word_count,
            quality_score=0.3  # Low score for fallback
        )
    
    def _calculate_quality_score(self, result: ContentResult, request: ContentRequest) -> float:
        """Calculate content quality score (0.0 - 1.0)"""
        score = 0.0
        
        # Word count score (40%)
        target_words = request.target_words
        word_ratio = min(result.word_count / target_words, 1.0)
        word_score = 0.4 * word_ratio
        
        # Structure score (30%)
        structure_score = 0.0
        if result.title and len(result.title) > 10:
            structure_score += 0.1
        if result.content and '<h2>' in result.content:
            structure_score += 0.1  
        if result.meta_title and len(result.meta_title) > 20:
            structure_score += 0.05
        if result.meta_desc and len(result.meta_desc) > 50:
            structure_score += 0.05
        
        # Keyword presence (20%)
        keyword_score = 0.0
        if request.keywords:
            content_lower = result.content.lower()
            found_keywords = sum(1 for kw in request.keywords if kw.lower() in content_lower)
            keyword_score = 0.2 * (found_keywords / len(request.keywords))
        else:
            keyword_score = 0.2  # Full score if no keywords specified
        
        # Language and formatting (10%)
        format_score = 0.0
        if '<p>' in result.content or '<h2>' in result.content:
            format_score += 0.05
        if result.tags and len(result.tags) >= 3:
            format_score += 0.05
        
        total_score = word_score + structure_score + keyword_score + format_score
        return min(total_score, 1.0)
    
    def _create_fallback_content(self, request: ContentRequest) -> ContentResult:
        """Create fallback content when AI fails"""
        return ContentResult(
            title=f"Bài viết về {request.prompt}",
            content=f"<h2>Giới thiệu</h2><p>Nội dung về <strong>{request.prompt}</strong> đang được cập nhật.</p>",
            meta_title=f"Tìm hiểu về {request.prompt}",
            meta_desc=f"Bài viết chi tiết về {request.prompt} với thông tin hữu ích.",
            tags=['fallback', 'content'],
            excerpt=f"Khám phá thông tin về {request.prompt}...",
            word_count=50,
            quality_score=0.2,
            provider_used='fallback'
        )
    
    def _update_stats(self, provider: AIProvider, quality_score: float, generation_time: float):
        """Update performance statistics"""
        self.stats['successful_generations'] += 1
        
        # Provider usage
        if provider.value not in self.stats['provider_usage']:
            self.stats['provider_usage'][provider.value] = 0
        self.stats['provider_usage'][provider.value] += 1
        
        # Average quality score
        current_avg = self.stats['avg_quality_score']
        total_successful = self.stats['successful_generations']
        self.stats['avg_quality_score'] = (
            (current_avg * (total_successful - 1) + quality_score) / total_successful
        )
        
        # Average generation time
        current_time_avg = self.stats['avg_generation_time']
        self.stats['avg_generation_time'] = (
            (current_time_avg * (total_successful - 1) + generation_time) / total_successful
        )
    
    async def generate_image_advanced(self, title: str, content_type: ContentType = ContentType.BLOG_POST,
                                    style: str = "professional", size: str = "1792x1024") -> Optional[str]:
        """
        Advanced image generation với style templates
        """
        try:
            if AIProvider.OPENAI not in self.providers:
                return None
            
            client = self.providers[AIProvider.OPENAI]
            
            # Style-specific prompts
            style_prompts = {
                "professional": "clean, modern, business-style, high-quality stock photo aesthetic",
                "creative": "artistic, vibrant colors, creative composition, inspiring",
                "minimalist": "clean, simple, minimal design, plenty of white space",
                "tech": "futuristic, digital, technology-focused, modern interface elements",
                "lifestyle": "bright, natural lighting, lifestyle photography, relatable"
            }
            
            base_prompt = f"""
            Create a high-quality featured image for a {content_type.value} titled: "{title}"
            
            Style: {style_prompts.get(style, style)}
            Requirements:
            - No text overlay or watermarks
            - Professional composition suitable for blog header
            - Colors that work well with web design
            - High contrast and visual appeal
            - {size} aspect ratio optimized
            """
            
            response = client.images.generate(
                model="dall-e-3",
                prompt=base_prompt.strip(),
                size=size,
                quality="standard",
                n=1
            )
            
            image_url = response.data[0].url
            print(f"🎨 [AI GEN V2] Generated {style} image: {image_url}")
            return image_url
            
        except Exception as e:
            print(f"❌ [AI GEN V2] Image generation failed: {str(e)}")
            return None
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get detailed performance statistics"""
        success_rate = 0
        if self.stats['total_requests'] > 0:
            success_rate = (self.stats['successful_generations'] / self.stats['total_requests']) * 100
        
        return {
            **self.stats,
            'success_rate': f"{success_rate:.1f}%",
            'cache_size': len(self._content_cache),
            'providers_available': len(self.providers),
            'provider_list': [p.value for p in self.providers.keys()]
        }
    
    def optimize_content_for_seo(self, result: ContentResult, keywords: List[str]) -> ContentResult:
        """Post-process content for SEO optimization"""
        if not keywords:
            return result
        
        # Optimize title
        primary_keyword = keywords[0]
        if primary_keyword.lower() not in result.title.lower():
            result.title = f"{primary_keyword} - {result.title}"[:80]
        
        # Optimize meta description
        if primary_keyword.lower() not in result.meta_desc.lower():
            result.meta_desc = f"{result.meta_desc} Tìm hiểu về {primary_keyword}."[:160]
        
        # Add keywords to tags
        for keyword in keywords[:3]:  # Max 3 keyword tags
            if keyword not in result.tags:
                result.tags.append(keyword)
        
        result.tags = result.tags[:8]  # Limit total tags
        
        return result

# Test V2 module
if __name__ == "__main__":
    import sys
    import asyncio
    sys.path.append('..')
    from config import Config
    
    print("🧪 TESTING AI GENERATOR V2")
    print("=" * 35)
    
    # Test advanced AI generator
    ai_gen = AdvancedAIGenerator(
        openai_key=Config.OPENAI_API_KEY or "",
        gemini_key=Config.GEMINI_API_KEY or ""
    )
    
    # Test content generation
    test_request = ContentRequest(
        prompt="Lợi ích của trí tuệ nhân tạo trong marketing digital",
        content_type=ContentType.BLOG_POST,
        target_words=600,
        keywords=["AI marketing", "digital marketing", "automation"],
        tone="professional"
    )
    
    print(f"🔄 Generating content: {test_request.prompt}")
    result = ai_gen.generate_content(test_request)
    
    print(f"\n✅ Generation Results:")
    print(f"   📝 Title: {result.title}")
    print(f"   📊 Words: {result.word_count}")
    print(f"   ⭐ Quality: {result.quality_score:.2f}")
    print(f"   🤖 Provider: {result.provider_used}")
    print(f"   ⏱️  Time: {result.generation_time:.1f}s")
    print(f"   🏷️  Tags: {result.tags}")
    
    # Test image generation
    print(f"\n🎨 Testing image generation...")
    image_url = asyncio.run(ai_gen.generate_image_advanced(
        title=result.title,
        content_type=ContentType.BLOG_POST,
        style="professional"
    ))
    
    if image_url:
        print(f"✅ Image generated: {image_url}")
    
    # Show statistics
    stats = ai_gen.get_statistics()
    print(f"\n📊 AI Generator Statistics:")
    for key, value in stats.items():
        print(f"   {key}: {value}")
