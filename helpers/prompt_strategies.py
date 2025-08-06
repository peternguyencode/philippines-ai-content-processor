#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PROMPT STRATEGIES - 2 Chiến lược xử lý dữ liệu hoàn toàn khác nhau
Strategy Pattern cho AI Content Processing

Author: AI Assistant
Date: 2025-08-06
"""

import json
import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from openai import OpenAI

from config import Config


class PromptStrategy(ABC):
    """Base class cho tất cả Prompt Strategies"""

    def __init__(self):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.logger = logging.getLogger(__name__)

    @abstractmethod
    def get_strategy_name(self) -> str:
        """Trả về tên strategy"""
        pass

    @abstractmethod
    def prepare_prompt(self, content: str, title: str, **kwargs) -> str:
        """Chuẩn bị prompt cho strategy này"""
        pass

    @abstractmethod
    def process_ai_response(self, response: str) -> Dict[str, Any]:
        """Xử lý response từ AI theo strategy này"""
        pass

    @abstractmethod
    def get_database_fields(self) -> Dict[str, str]:
        """Trả về mapping fields cho database"""
        pass

    def execute_strategy(self, content: str, title: str, **kwargs) -> Dict[str, Any]:
        """Execute strategy chính"""
        try:
            # 1. Prepare prompt theo strategy
            prompt = self.prepare_prompt(content, title, **kwargs)

            # 2. Call OpenAI với prompt đã chuẩn bị
            response = self.client.chat.completions.create(
                model=kwargs.get("model", Config.AI_MODEL or "gpt-3.5-turbo"),
                messages=[
                    {"role": "system", "content": self.get_system_message()},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=self.get_max_tokens(),
                temperature=self.get_temperature(),
            )

            ai_response = response.choices[0].message.content
            if ai_response:
                ai_response = ai_response.strip()
            else:
                ai_response = ""

            # 3. Process response theo strategy
            result = self.process_ai_response(ai_response)

            # 4. Add metadata
            result["strategy"] = self.get_strategy_name()
            result["model_used"] = kwargs.get(
                "model", Config.AI_MODEL or "gpt-3.5-turbo"
            )

            return result

        except Exception as e:
            self.logger.error(
                f"❌ Lỗi execute strategy {self.get_strategy_name()}: {e}"
            )
            return self.get_fallback_result(content, title, str(e))

    @abstractmethod
    def get_system_message(self) -> str:
        """System message cho strategy này"""
        pass

    @abstractmethod
    def get_max_tokens(self) -> int:
        """Max tokens cho strategy này"""
        pass

    @abstractmethod
    def get_temperature(self) -> float:
        """Temperature cho strategy này"""
        pass

    @abstractmethod
    def get_fallback_result(
        self, content: str, title: str, error: str
    ) -> Dict[str, Any]:
        """Fallback result khi có lỗi"""
        pass


class DatabasePromptStrategy(PromptStrategy):
    """STRATEGY 1: Database Pipeline - Premium SEO + Images"""

    def get_strategy_name(self) -> str:
        return "DATABASE_PIPELINE"

    def get_system_message(self) -> str:
        return "Bạn là chuyên gia content marketing và SEO chuyên nghiệp, tập trung vào chất lượng cao và tối ưu SEO."

    def get_max_tokens(self) -> int:
        return 2000

    def get_temperature(self) -> float:
        return 0.7

    def prepare_prompt(self, content: str, title: str, **kwargs) -> str:
        """Prompt cho Database Strategy - Focus SEO + Images"""
        category = kwargs.get("category", "")

        prompt = f"""
        🎯 NHIỆM VỤ: PREMIUM CONTENT PROCESSING cho Website/Blog
        
        Bạn là chuyên gia content marketing và SEO. Hãy viết lại bài viết sau đây để:
        ✅ Tối ưu SEO và thu hút người đọc
        ✅ Giữ nguyên ý nghĩa chính nhưng diễn đạt hay hơn  
        ✅ Thêm keywords tự nhiên liên quan đến chủ đề
        ✅ Cấu trúc rõ ràng với đoạn văn ngắn
        ✅ Tạo image prompt chất lượng cao
        
        📊 INPUT DATA:
        Tiêu đề gốc: {title}
        Danh mục: {category}
        
        Nội dung gốc:
        {content[:2000]}...
        
        📋 YÊU CẦU OUTPUT JSON (6 FIELDS):
        {{
            "ai_content": "Nội dung đã được viết lại với SEO optimization",
            "meta_title": "Tiêu đề SEO (60-70 ký tự)",
            "meta_description": "Mô tả SEO (150-160 ký tự)",
            "image_prompt": "Professional image prompt for DALL-E 3 (English, detailed)",
            "suggested_tags": "tag1, tag2, tag3, tag4, tag5",
            "notes": "Ghi chú về quá trình xử lý và chiến lược SEO"
        }}
        
        🎨 IMAGE PROMPT REQUIREMENTS:
        - Tiếng Anh, chi tiết
        - Professional, high-quality
        - Liên quan trực tiếp đến nội dung
        - Suitable for DALL-E 3 generation
        """
        return prompt

    def process_ai_response(self, response: str) -> Dict[str, Any]:
        """Xử lý response cho Database Strategy"""
        try:
            # Parse JSON từ AI
            ai_result = json.loads(response)

            # Validate required fields cho Database Strategy
            required_fields = [
                "ai_content",
                "meta_title",
                "meta_description",
                "image_prompt",
                "suggested_tags",
                "notes",
            ]

            for field in required_fields:
                if field not in ai_result:
                    ai_result[field] = f"Missing {field}"

            # Additional processing cho Database Strategy
            ai_result["processing_type"] = "premium_seo"
            ai_result["supports_images"] = True
            ai_result["output_format"] = "6_fields"

            return ai_result

        except json.JSONDecodeError:
            # Fallback parsing cho Database Strategy
            return {
                "ai_content": response,
                "meta_title": "Fallback Title",
                "meta_description": "Fallback Description",
                "image_prompt": "Professional business image",
                "suggested_tags": "business, content",
                "notes": "AI response không đúng JSON format - Database Strategy",
                "processing_type": "premium_seo",
                "supports_images": True,
                "output_format": "6_fields",
            }

    def get_database_fields(self) -> Dict[str, str]:
        """Database fields mapping cho Database Strategy"""
        return {
            "ai_content": "ai_content",
            "meta_title": "meta_title",
            "meta_description": "meta_description",
            "image_prompt": "image_prompt",
            "suggested_tags": "tags",
            "notes": "ai_notes",
        }

    def get_fallback_result(
        self, content: str, title: str, error: str
    ) -> Dict[str, Any]:
        """Fallback cho Database Strategy"""
        return {
            "ai_content": content,
            "meta_title": title[:70],
            "meta_description": content[:160] + "...",
            "image_prompt": "Professional business content image",
            "suggested_tags": "business, content",
            "notes": f"Database Strategy failed: {error}",
            "processing_type": "premium_seo",
            "supports_images": True,
            "output_format": "6_fields",
            "strategy": "DATABASE_PIPELINE",
        }


class CSVPromptStrategy(PromptStrategy):
    """STRATEGY 2: CSV Pipeline - Fast Philippines Localization"""

    def get_strategy_name(self) -> str:
        return "CSV_PIPELINE"

    def get_system_message(self) -> str:
        return "You are a Philippines content localization expert, focusing on fast processing and cultural adaptation."

    def get_max_tokens(self) -> int:
        return 1000  # Ít hơn Database Strategy

    def get_temperature(self) -> float:
        return 0.5  # Conservative hơn Database Strategy

    def prepare_prompt(self, content: str, title: str, **kwargs) -> str:
        """Prompt cho CSV Strategy - Focus Philippines + Fast"""

        prompt = f"""
        🇵🇭 MISSION: PHILIPPINES CONTENT LOCALIZATION
        
        You are a content localization expert for Philippines market. Transform this content to:
        ✅ Adapt to Philippines culture and market
        ✅ Keep it natural and engaging for Filipino readers
        ✅ Fast processing - concise but effective
        ✅ Focus on paraphrasing and classification
        
        📊 INPUT:
        Original Title: {title}
        
        Original Content:
        {content[:1500]}...
        
        📋 REQUIRED JSON OUTPUT (3 FIELDS ONLY):
        {{
            "paraphrased_content": "Content adapted for Philippines market",
            "classification": "Category classification (Business/Tech/Lifestyle/etc)",
            "localization_notes": "Brief notes about Philippines adaptation"
        }}
        
        🎯 FOCUS:
        - Philippines market adaptation
        - Cultural relevance
        - Fast processing
        - 3 fields only (no SEO, no images)
        """
        return prompt

    def process_ai_response(self, response: str) -> Dict[str, Any]:
        """Xử lý response cho CSV Strategy"""
        try:
            # Parse JSON từ AI
            ai_result = json.loads(response)

            # Validate required fields cho CSV Strategy
            required_fields = [
                "paraphrased_content",
                "classification",
                "localization_notes",
            ]

            for field in required_fields:
                if field not in ai_result:
                    ai_result[field] = f"Missing {field}"

            # Additional processing cho CSV Strategy
            ai_result["processing_type"] = "philippines_localization"
            ai_result["supports_images"] = False
            ai_result["output_format"] = "3_fields"
            ai_result["target_market"] = "Philippines"

            return ai_result

        except json.JSONDecodeError:
            # Fallback parsing cho CSV Strategy
            return {
                "paraphrased_content": response,
                "classification": "General",
                "localization_notes": "AI response không đúng JSON format - CSV Strategy",
                "processing_type": "philippines_localization",
                "supports_images": False,
                "output_format": "3_fields",
                "target_market": "Philippines",
            }

    def get_database_fields(self) -> Dict[str, str]:
        """Database fields mapping cho CSV Strategy"""
        return {
            "paraphrased_content": "ai_content",
            "classification": "category",
            "localization_notes": "ai_notes",
        }

    def get_fallback_result(
        self, content: str, title: str, error: str
    ) -> Dict[str, Any]:
        """Fallback cho CSV Strategy"""
        return {
            "paraphrased_content": content,
            "classification": "General",
            "localization_notes": f"CSV Strategy failed: {error}",
            "processing_type": "philippines_localization",
            "supports_images": False,
            "output_format": "3_fields",
            "target_market": "Philippines",
            "strategy": "CSV_PIPELINE",
        }


class PromptStrategyFactory:
    """Factory để tạo ra các strategies"""

    _strategies = {
        "DATABASE_PIPELINE": DatabasePromptStrategy,
        "CSV_PIPELINE": CSVPromptStrategy,
    }

    @classmethod
    def create_strategy(cls, strategy_name: str) -> PromptStrategy:
        """Tạo strategy instance"""
        if strategy_name not in cls._strategies:
            raise ValueError(
                f"Unknown strategy: {strategy_name}. Available: {list(cls._strategies.keys())}"
            )

        return cls._strategies[strategy_name]()

    @classmethod
    def get_available_strategies(cls) -> list:
        """Lấy danh sách strategies có thể dùng"""
        return list(cls._strategies.keys())

    @classmethod
    def get_strategy_info(cls) -> Dict[str, Dict]:
        """Thông tin chi tiết về từng strategy"""
        return {
            "DATABASE_PIPELINE": {
                "name": "Database Pipeline",
                "description": "Premium SEO optimization + Image generation",
                "output_fields": 6,
                "supports_images": True,
                "target": "Website/Blog premium content",
                "cost_per_request": "~$0.04",
            },
            "CSV_PIPELINE": {
                "name": "CSV Pipeline",
                "description": "Fast Philippines localization",
                "output_fields": 3,
                "supports_images": False,
                "target": "Philippines market adaptation",
                "cost_per_request": "~$0.002",
            },
        }


def demo_strategies():
    """Demo để test 2 strategies"""
    print("🎯 DEMO: 2 PROMPT STRATEGIES")
    print("=" * 50)

    # Sample data
    sample_title = "Cách tăng doanh thu kinh doanh online"
    sample_content = """
    Kinh doanh online ngày nay đang trở thành xu hướng chính của nhiều doanh nghiệp. 
    Để thành công trong lĩnh vực này, bạn cần phải hiểu rõ về thị trường, khách hàng và chiến lược marketing phù hợp.
    Việc xây dựng website chuyên nghiệp, tối ưu SEO và sử dụng mạng xã hội hiệu quả là những yếu tố then chốt.
    """

    for strategy_name in PromptStrategyFactory.get_available_strategies():
        print(f"\n🔥 TESTING STRATEGY: {strategy_name}")
        print("-" * 30)

        try:
            # Tạo strategy
            strategy = PromptStrategyFactory.create_strategy(strategy_name)

            # Hiển thị thông tin strategy
            print(f"📊 Strategy: {strategy.get_strategy_name()}")
            print(f"🎨 Max Tokens: {strategy.get_max_tokens()}")
            print(f"🌡️ Temperature: {strategy.get_temperature()}")

            # Test prompt preparation
            prompt = strategy.prepare_prompt(
                sample_content, sample_title, category="Business"
            )
            print(f"📝 Prompt Length: {len(prompt)} characters")
            print(f"📋 Database Fields: {len(strategy.get_database_fields())} fields")

            print(f"✅ Strategy {strategy_name} OK!")

        except Exception as e:
            print(f"❌ Error testing {strategy_name}: {e}")

    # Hiển thị thông tin strategies
    print(f"\n📊 STRATEGY INFORMATION:")
    print("-" * 30)
    for name, info in PromptStrategyFactory.get_strategy_info().items():
        print(f"\n🎯 {name}:")
        for key, value in info.items():
            print(f"   {key}: {value}")


if __name__ == "__main__":
    demo_strategies()
