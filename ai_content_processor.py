#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Content Processor - Xử lý nội dung posts với AI
Lấy dữ liệu từ bảng 'posts' → AI processing → lưu vào bảng 'posts_ai'

Author: AI Assistant
Date: 2025-08-05
"""

import json
import logging
import os
import sys
import time
import traceback
from datetime import datetime
from typing import Any, Dict, List, Optional

import mysql.connector
import openai
from mysql.connector import Error
from tqdm import tqdm

# Import config
from config import Config


class AIContentProcessor:
    """Lớp chính xử lý nội dung posts với AI"""

    def __init__(self):
        """Khởi tạo AI Content Processor"""
        print("🤖 Khởi tạo AI Content Processor...")

        # Setup logging
        self.setup_logging()

        # MySQL connection
        self.connection = None
        self.connect_mysql()

        # OpenAI setup
        self.setup_openai()

        # Statistics
        self.stats = {"total_processed": 0, "success": 0, "errors": 0, "skipped": 0}

        print("✅ AI Content Processor khởi tạo thành công!")

    def setup_logging(self):
        """Thiết lập logging"""
        log_filename = f"ai_processing_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler(log_filename, encoding="utf-8"),
                logging.StreamHandler(sys.stdout),
            ],
        )

        self.logger = logging.getLogger(__name__)
        self.logger.info("🔍 Logging được thiết lập")

    def connect_mysql(self):
        """Kết nối MySQL Database"""
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                port=3308,
                user="root",
                password="baivietwp_password",
                database="mydb",
                charset="utf8mb4",
                autocommit=True,
            )

            if self.connection.is_connected():
                self.logger.info("✅ Kết nối MySQL thành công")
                self.create_posts_ai_table()
            else:
                raise ConnectionError("MySQL connection failed")

        except Error as e:
            self.logger.error(f"❌ MySQL connection error: {e}")
            sys.exit(1)

    def create_posts_ai_table(self):
        """Tạo bảng posts_ai nếu chưa tồn tại"""
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS posts_ai (
            id INT AUTO_INCREMENT PRIMARY KEY,
            post_id INT NOT NULL,
            title VARCHAR(500) NOT NULL,
            ai_content TEXT NOT NULL,
            meta_title VARCHAR(255),
            meta_description VARCHAR(300),
            image_url TEXT,
            image_prompt TEXT,
            tags TEXT,
            category VARCHAR(100),
            ai_model VARCHAR(50),
            ai_notes TEXT,
            processing_status ENUM('processing', 'completed', 'error') DEFAULT 'processing',
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            UNIQUE KEY unique_post_id (post_id),
            FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """

        try:
            cursor = self.connection.cursor()
            cursor.execute(create_table_sql)
            cursor.close()
            self.logger.info("✅ Bảng 'posts_ai' đã sẵn sàng")

        except Error as e:
            self.logger.error(f"❌ Lỗi tạo bảng posts_ai: {e}")
            raise

    def _auto_categorize_content(self, title: str, content: str) -> str:
        """
        🤖 AUTO CATEGORIZE content dựa trên AI analysis
        
        Args:
            title: Tiêu đề bài viết
            content: Nội dung bài viết
            
        Returns:
            str: Category được detect (Bonus/Review/Payment/GameGuide/News)
        """
        try:
            # Keywords mapping cho auto categorization
            category_keywords = {
                "Bonus": ["bonus", "free", "deposit", "welcome", "promotion", "offer", "100%", "150%", "cashback"],
                "Review": ["review", "rating", "experience", "opinion", "test", "evaluation", "compare"],
                "Payment": ["deposit", "withdrawal", "payment", "gcash", "paymaya", "bank", "method", "transfer"],
                "GameGuide": ["how to", "guide", "tips", "strategy", "play", "win", "tutorial", "steps"],
                "News": ["news", "update", "announcement", "launch", "new", "latest", "breaking"]
            }
            
            text_to_analyze = f"{title} {content[:500]}".lower()
            
            # Score cho từng category
            category_scores = {}
            for category, keywords in category_keywords.items():
                score = sum(1 for keyword in keywords if keyword in text_to_analyze)
                category_scores[category] = score
            
            # Trả về category có score cao nhất
            best_category = max(category_scores, key=category_scores.get)
            
            # Fallback nếu không match keyword nào
            if category_scores[best_category] == 0:
                return "Casino"  # Default category
                
            self.logger.info(f"🎯 Auto-categorized: {best_category} (score: {category_scores[best_category]})")
            return best_category
            
        except Exception as e:
            self.logger.error(f"❌ Lỗi auto categorize: {e}")
            return "Casino"  # Fallback

    def _get_category_prompt_template(self, category: str, site_version: int) -> Dict[str, str]:
        """
        🎨 GET PROMPT TEMPLATE cho từng category và site version
        
        Args:
            category: Danh mục (Bonus/Review/Payment/etc)
            site_version: Version site (1-5)
            
        Returns:
            Dict chứa prompt template specific
        """
        # Base templates cho từng category
        templates = {
            "Bonus": {
                "specific_requirements": "Focus on bonus terms, wagering requirements, Philippines-specific bonuses, GCash/PayMaya deposit bonuses",
                "writing_style": "Exciting, promotional, emphasizing value and local payment advantages"
            },
            "Review": {
                "specific_requirements": "Detailed analysis, pros/cons, Philippines player perspective, local banking compatibility",
                "writing_style": "Analytical, trustworthy, unbiased review with Filipino player insights"
            },
            "Payment": {
                "specific_requirements": "Deep dive into PH payment methods: GCash, PayMaya, BPI, BDO, Metrobank, UnionBank",
                "writing_style": "Informative, step-by-step, addressing Filipino banking concerns"
            },
            "GameGuide": {
                "specific_requirements": "Practical strategies, beginner-friendly for Filipino players, mobile-first approach",
                "writing_style": "Educational, encouraging, using Filipino gaming culture references"
            },
            "News": {
                "specific_requirements": "Latest updates relevant to Philippines gambling laws, new casino launches for PH market",
                "writing_style": "News-worthy, timely, with local market implications"
            }
        }
        
        # Version-specific style adjustments
        version_styles = {
            1: "Professional, formal tone",
            2: "Casual, friendly approach", 
            3: "Enthusiastic, energetic writing",
            4: "Expert, technical analysis",
            5: "Story-telling, narrative style"
        }
        
        # Get base template hoặc fallback
        base_template = templates.get(category, templates["Bonus"])
        
        # Customize theo version
        template = base_template.copy()
        template["writing_style"] += f" | Version {site_version}: {version_styles.get(site_version, 'Balanced approach')}"
        
        return template

    def setup_openai(self):
        """Thiết lập OpenAI API"""
        try:
            openai.api_key = Config.OPENAI_API_KEY

            if not openai.api_key:
                raise ValueError("OPENAI_API_KEY không được thiết lập trong config")

            self.logger.info("✅ OpenAI API đã được thiết lập")

        except Exception as e:
            self.logger.error(f"❌ Lỗi thiết lập OpenAI: {e}")
            sys.exit(1)

    def get_unprocessed_posts(self, limit: Optional[int] = None) -> List[Dict]:
        """
        Lấy danh sách posts chưa được xử lý bởi AI

        Args:
            limit: Giới hạn số posts lấy

        Returns:
            List posts chưa xử lý
        """
        try:
            cursor = self.connection.cursor(dictionary=True)

            # Query posts chưa có trong posts_ai
            sql = """
            SELECT p.id, p.title, p.content, p.category, p.tags
            FROM posts p
            LEFT JOIN posts_ai pa ON p.id = pa.post_id
            WHERE pa.post_id IS NULL
            ORDER BY p.created_date DESC
            """

            if limit:
                sql += f" LIMIT {limit}"

            cursor.execute(sql)
            posts = cursor.fetchall()
            cursor.close()

            self.logger.info(f"📊 Tìm thấy {len(posts)} posts chưa xử lý")
            return posts

        except Error as e:
            self.logger.error(f"❌ Lỗi lấy posts chưa xử lý: {e}")
            return []

    def process_content_with_ai(
        self, original_content: str, title: str, category: str = "", site_version: int = 1
    ) -> Dict[str, Any]:
        """
        🇵🇭 PHILIPPINES MULTI-SITE AI CONTENT PIPELINE
        Deep rewrite + Auto categorize + Local info + Multi-version

        Args:
            original_content: Nội dung gốc
            title: Tiêu đề bài viết
            category: Danh mục (auto-detect nếu rỗng)
            site_version: Version cho site khác nhau (1-5)

        Returns:
            Dict chứa nội dung đã xử lý với Philippines local info
        """
        try:
            # 🎯 AUTO CATEGORIZE nếu chưa có category
            if not category:
                category = self._auto_categorize_content(title, original_content)
            
            # 🚀 CHỌN PROMPT TEMPLATE theo category và site version
            prompt_template = self._get_category_prompt_template(category, site_version)
            
            # 🇵🇭 XÂY DỰNG PROMPT PHILIPPINES SPECIFIC
            prompt = f"""
            🇵🇭 PHILIPPINES CASINO CONTENT EXPERT - MULTI-SITE VERSION {site_version}
            
            MISSION: Create UNIQUE, SEO-optimized content for Philippines market with local payment methods, culture, and regulations.
            
            📋 TARGET CATEGORY: {category}
            📊 SITE VERSION: {site_version}/5 (Must be completely unique from other versions)
            
            🎯 REQUIREMENTS:
            1. 🔥 DEEP REWRITE (100% unique, no duplicate detection)
            2. 🇵🇭 Add Philippines local info: GCash, PayMaya, BPI, Metrobank, local bonuses
            3. 🎰 {prompt_template['specific_requirements']}
            4. 📱 Include mobile-first approach (Filipinos use mobile heavily)
            5. 🏆 Add competitive advantages vs other PH casinos
            6. 💰 Include peso (₱) currency mentions
            
            📝 ORIGINAL:
            Title: {title}
            Content: {original_content[:2500]}...
            
            🎨 STYLE FOR VERSION {site_version}: {prompt_template['writing_style']}
            
            📤 OUTPUT JSON:
            {{
                "ai_content": "COMPLETELY rewritten content with PH local info, payment methods, cultural references",
                "auto_category": "Auto-detected category (Bonus/Review/Payment/GameGuide/News)",
                "meta_title": "SEO title 60-65 chars with PH keywords",
                "meta_description": "Meta desc 150-160 chars with local appeal",
                "image_prompt": "Professional image prompt for {category} content (English)",
                "suggested_tags": "PH-specific tags: philippines-casino, gcash-deposit, etc",
                "affiliate_cta": "Strong CTA with urgency for PH market",
                "local_payments": "GCash, PayMaya, bank transfer options mentioned",
                "seo_keywords": "Primary keywords for PH SEO ranking",
                "version_notes": "What makes this Version {site_version} unique",
                "competition_angle": "Unique selling points vs competitors"
            }}
            """

            # Gọi OpenAI API (v1.0+ syntax)
            from openai import OpenAI

            client = OpenAI(api_key=Config.OPENAI_API_KEY)

            response = client.chat.completions.create(
                model=Config.AI_MODEL or "gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "Bạn là chuyên gia content marketing và SEO chuyên nghiệp.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=2000,
                temperature=0.7,
            )

            # Parse response
            ai_response = response.choices[0].message.content.strip()

            # Thử parse JSON response
            try:
                ai_result = json.loads(ai_response)
            except json.JSONDecodeError:
                # Nếu AI không trả về JSON đúng format, tạo fallback
                ai_result = {
                    "ai_content": ai_response,
                    "meta_title": title[:70],
                    "meta_description": original_content[:160] + "...",
                    "image_prompt": f"Professional image related to {category or 'business'}",
                    "suggested_tags": "",
                    "notes": "AI response không đúng JSON format",
                }

            self.logger.info(f"✅ AI xử lý thành công: {title[:50]}...")
            return ai_result

        except Exception as e:
            self.logger.error(f"❌ Lỗi AI processing: {e}")
            # Fallback nếu AI fails
            return {
                "ai_content": original_content,
                "meta_title": title[:70],
                "meta_description": original_content[:160] + "...",
                "image_prompt": f"Professional image related to {category or 'business'}",
                "suggested_tags": "",
                "notes": f"AI processing failed: {str(e)}",
            }

    def generate_image_with_ai(self, image_prompt: str) -> str:
        """
        Generate image URL with AI (OpenAI DALL-E)

        Args:
            image_prompt: Prompt mô tả hình ảnh

        Returns:
            str: URL hình ảnh hoặc empty string nếu failed
        """
        try:
            if not image_prompt or len(image_prompt.strip()) < 10:
                self.logger.warning("❌ Image prompt quá ngắn hoặc rỗng")
                return ""

            from openai import OpenAI

            client = OpenAI(api_key=Config.OPENAI_API_KEY)

            self.logger.info(f"🎨 Generating image: {image_prompt[:50]}...")

            response = client.images.generate(
                model="dall-e-3",
                prompt=image_prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )

            image_url = response.data[0].url
            self.logger.info(f"✅ Image generated successfully: {image_url[:50]}...")
            return image_url

        except Exception as e:
            self.logger.error(f"❌ Lỗi generate image: {e}")
            return ""

    def save_ai_result(
        self,
        post_id: int,
        title: str,
        ai_result: Dict[str, Any],
        category: str = "",
        original_tags: str = "",
        site_version: int = 1,
    ) -> bool:
        """
        💾 LƯU KẾT QUẢ AI VÀO BẢNG posts_ai với Philippines info
        
        Args:
            post_id: ID của post gốc
            title: Tiêu đề
            ai_result: Kết quả xử lý từ AI
            category: Danh mục
            original_tags: Tags gốc
            site_version: Version site (1-5)

        Returns:
            bool: True nếu thành công
        """
        try:
            cursor = self.connection.cursor()

            # 🎯 CHUẨN BỊ DỮ LIỆU với Philippines info
            auto_category = ai_result.get("auto_category", category)
            tags = ai_result.get("suggested_tags", "") or original_tags
            ai_model = Config.AI_MODEL or "gpt-3.5-turbo"
            
            # 🇵🇭 Philippines-specific fields
            local_payments = ai_result.get("local_payments", "")
            affiliate_cta = ai_result.get("affiliate_cta", "")
            seo_keywords = ai_result.get("seo_keywords", "")
            version_notes = ai_result.get("version_notes", f"Site version {site_version}")
            competition_angle = ai_result.get("competition_angle", "")

            insert_sql = """
            INSERT INTO posts_ai (
                post_id, title, ai_content, meta_title, meta_description,
                image_url, image_prompt, tags, category, ai_model, ai_notes, processing_status
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                ai_content = VALUES(ai_content),
                meta_title = VALUES(meta_title),
                meta_description = VALUES(meta_description),
                image_url = VALUES(image_url),
                image_prompt = VALUES(image_prompt),
                tags = VALUES(tags),
                category = VALUES(category),
                ai_model = VALUES(ai_model),
                ai_notes = VALUES(ai_notes),
                processing_status = VALUES(processing_status),
                updated_date = CURRENT_TIMESTAMP
            """

            # 📋 Gộp notes với Philippines info
            combined_notes = f"""
            Version: {site_version} | Category: {auto_category}
            Local Payments: {local_payments}
            SEO Keywords: {seo_keywords}
            Version Notes: {version_notes}
            Competition: {competition_angle}
            Original Notes: {ai_result.get('notes', '')}
            """.strip()

            values = (
                post_id,
                title,
                ai_result["ai_content"],
                ai_result["meta_title"],
                ai_result["meta_description"],
                ai_result.get("image_url", ""),
                ai_result.get("image_prompt", ""),
                tags,
                auto_category,
                ai_model,
                combined_notes,
                "completed",
            )

            cursor.execute(insert_sql, values)
            cursor.close()

            self.logger.info(f"✅ Saved Post ID {post_id} (v{site_version}) - {auto_category}")
            return True

        except Exception as e:
            self.logger.error(f"❌ Lỗi lưu AI result: {e}")
            return False

    def process_single_post(self, post: Dict[str, Any], site_version: int = 1) -> Dict[str, Any]:
        """
        🇵🇭 XỬ LÝ MỘT POST VỚI AI - PHILIPPINES MULTI-VERSION
        
        Args:
            post: Dict chứa thông tin post
            site_version: Version cho site khác nhau (1-5)

        Returns:
            Dict chứa kết quả xử lý
        """
        post_id = post["id"]
        title = post["title"]
        content = post["content"]
        category = post.get("category", "")
        tags = post.get("tags", "")

        result = {"post_id": post_id, "site_version": site_version, "success": False, "error": None}

        try:
            self.logger.info(f"🔄 Processing Post ID {post_id} (v{site_version}): {title[:50]}...")

            # Cập nhật trạng thái processing
            self.update_processing_status(post_id, "processing")

            # 🚀 XỬ LÝ VỚI AI - PHILIPPINES VERSION
            ai_result = self.process_content_with_ai(content, title, category, site_version)

            # 🎨 GENERATE IMAGE nếu có image_prompt
            image_url = ""
            image_prompt = ai_result.get("image_prompt", "")
            if image_prompt and len(image_prompt.strip()) > 10:
                self.logger.info(f"🎨 Generating image for Post ID {post_id} (v{site_version})...")
                image_url = self.generate_image_with_ai(image_prompt)
                if image_url:
                    ai_result["image_url"] = image_url
                    self.logger.info(f"✅ Image generated: {image_url[:50]}...")
                else:
                    self.logger.warning(f"⚠️ Image generation failed for Post ID {post_id}")

            # 💾 LƯU KẾT QUẢ với version info
            if self.save_ai_result(post_id, title, ai_result, category, tags, site_version):
                result["success"] = True
                result["category"] = ai_result.get("auto_category", category)
                result["version_notes"] = ai_result.get("version_notes", "")
                self.stats["success"] += 1
                self.logger.info(f"🎉 Completed Post ID {post_id} (v{site_version}) - {ai_result.get('auto_category', category)}")
            else:
                raise Exception("Lỗi lưu AI result")

        except Exception as e:
            error_msg = str(e)
            self.logger.error(f"❌ Lỗi xử lý Post ID {post_id} (v{site_version}): {error_msg}")

            # Cập nhật trạng thái lỗi
            self.update_processing_status(post_id, "error", error_msg)

            result["error"] = error_msg
            self.stats["errors"] += 1

        self.stats["total_processed"] += 1
        return result

    def update_processing_status(self, post_id: int, status: str, notes: str = ""):
        """Cập nhật trạng thái xử lý"""
        try:
            cursor = self.connection.cursor()

            if status == "processing":
                # Insert processing record
                sql = """
                INSERT INTO posts_ai (post_id, title, ai_content, processing_status, ai_notes)
                VALUES (%s, 'Processing...', 'Processing...', %s, %s)
                ON DUPLICATE KEY UPDATE
                    processing_status = VALUES(processing_status),
                    ai_notes = VALUES(ai_notes),
                    updated_date = CURRENT_TIMESTAMP
                """
                cursor.execute(sql, (post_id, status, notes))
            else:
                # Update existing record
                sql = """
                UPDATE posts_ai 
                SET processing_status = %s, ai_notes = CONCAT(COALESCE(ai_notes, ''), %s), updated_date = CURRENT_TIMESTAMP
                WHERE post_id = %s
                """
                cursor.execute(sql, (status, f" | {notes}" if notes else "", post_id))

            cursor.close()

        except Error as e:
            self.logger.error(f"❌ Lỗi cập nhật status: {e}")

    def process_batch(
        self, limit: Optional[int] = None, delay: float = 1.0, multi_version: bool = False, num_versions: int = 3
    ) -> Dict[str, Any]:
        """
        🇵🇭 XỬ LÝ BATCH POSTS VỚI AI - PHILIPPINES MULTI-VERSION
        
        Args:
            limit: Giới hạn số posts xử lý
            delay: Delay giữa các request (giây)
            multi_version: Có tạo nhiều version không
            num_versions: Số version tạo cho multi-site (1-5)

        Returns:
            Dict chứa thống kê kết quả
        """
        print(f"\n🚀 🇵🇭 PHILIPPINES AI CONTENT PIPELINE")
        print("=" * 60)
        
        if multi_version:
            print(f"🌐 MULTI-SITE MODE: {num_versions} versions per post")
        else:
            print("📝 SINGLE VERSION MODE")

        # Reset stats
        self.stats = {"total_processed": 0, "success": 0, "errors": 0, "skipped": 0}

        # Lấy posts chưa xử lý
        posts = self.get_unprocessed_posts(limit)

        if not posts:
            print("ℹ️ Không có posts nào cần xử lý!")
            return self.stats

        # Tính total processing với multi-version
        total_processing = len(posts) * (num_versions if multi_version else 1)
        
        print(f"📊 Posts to process: {len(posts)}")
        print(f"🔄 Total operations: {total_processing}")
        print(f"⏱️ Delay between requests: {delay}s")

        # Bắt đầu xử lý
        start_time = time.time()

        with tqdm(total=total_processing, desc="🇵🇭 PH AI Processing") as pbar:
            for post in posts:
                try:
                    # Xử lý multi-version hoặc single version
                    versions_to_process = range(1, num_versions + 1) if multi_version else [1]
                    
                    for version in versions_to_process:
                        # Xử lý post với version specific
                        result = self.process_single_post(post, version)

                        # Cập nhật progress bar
                        status = "✅" if result["success"] else "❌"
                        category_info = result.get("category", "")
                        pbar.set_postfix_str(f"{status} Post {result['post_id']} v{version} [{category_info}]")
                        pbar.update(1)

                        # Delay giữa requests
                        if delay > 0:
                            time.sleep(delay)

                except KeyboardInterrupt:
                    print("\n⚠️ Bị dừng bởi người dùng")
                    break
                except Exception as e:
                    self.logger.error(f"❌ Exception trong batch processing: {e}")
                    self.stats["errors"] += 1
                    pbar.update(1)

        # Tính thời gian và in kết quả
        end_time = time.time()
        duration = end_time - start_time

        print(f"\n📈 🇵🇭 PHILIPPINES AI PROCESSING RESULTS:")
        print(f"   Total operations: {self.stats['total_processed']}")
        print(f"   Success: {self.stats['success']}")
        print(f"   Errors: {self.stats['errors']}")
        print(f"   Duration: {duration:.2f}s")
        if self.stats["total_processed"] > 0:
            print(f"   Speed: {self.stats['total_processed']/duration:.2f} operations/s")
        
        if multi_version:
            print(f"   🌐 Multi-site versions created: {num_versions}")
            print(f"   🎯 Ready for {num_versions} different sites!")

        return self.stats

    def get_processing_stats(self) -> Dict[str, Any]:
        """Lấy thống kê xử lý"""
        try:
            cursor = self.connection.cursor(dictionary=True)

            # Thống kê tổng quan
            cursor.execute("SELECT COUNT(*) as total FROM posts")
            total_posts = cursor.fetchone()["total"]

            cursor.execute("SELECT COUNT(*) as processed FROM posts_ai")
            processed_posts = cursor.fetchone()["processed"]

            cursor.execute(
                """
                SELECT processing_status, COUNT(*) as count 
                FROM posts_ai 
                GROUP BY processing_status
            """
            )
            status_stats = cursor.fetchall()

            cursor.close()

            stats = {
                "total_posts": total_posts,
                "processed_posts": processed_posts,
                "unprocessed_posts": total_posts - processed_posts,
                "by_status": {
                    item["processing_status"]: item["count"] for item in status_stats
                },
            }

            return stats

        except Error as e:
            self.logger.error(f"❌ Lỗi lấy stats: {e}")
            return {}

    def close(self):
        """Đóng kết nối"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            self.logger.info("✅ MySQL connection closed")


def main():
    """Hàm main"""
    print("🤖 AI CONTENT PROCESSOR")
    print("=" * 40)
    print("Xử lý nội dung posts với AI")
    print("posts → AI processing → posts_ai")
    print()

    try:
        # Khởi tạo processor
        processor = AIContentProcessor()

        # Kiểm tra tham số dòng lệnh
        if len(sys.argv) > 1:
            command = sys.argv[1].lower()

            if command == "batch":
                # Batch processing
                limit = int(sys.argv[2]) if len(sys.argv) > 2 else None
                delay = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
                multi_version = sys.argv[4].lower() == "true" if len(sys.argv) > 4 else False
                num_versions = int(sys.argv[5]) if len(sys.argv) > 5 else 3
                stats = processor.process_batch(limit, delay, multi_version, num_versions)

            elif command == "multi":
                # Multi-version processing
                limit = int(sys.argv[2]) if len(sys.argv) > 2 else None
                delay = float(sys.argv[3]) if len(sys.argv) > 3 else 2.0
                num_versions = int(sys.argv[4]) if len(sys.argv) > 4 else 3
                stats = processor.process_batch(limit, delay, True, num_versions)

            elif command == "stats":
                # Hiển thị thống kê
                stats = processor.get_processing_stats()
                print(f"\n📊 AI PROCESSING STATISTICS:")
                for key, value in stats.items():
                    print(f"   {key}: {value}")

            elif command == "single":
                # Xử lý 1 post
                stats = processor.process_batch(limit=1, delay=0)

            elif command == "test-multi":
                # Test multi-version với 1 post
                stats = processor.process_batch(limit=1, delay=0, multi_version=True, num_versions=2)

            else:
                print(f"❌ Lệnh không hợp lệ: {command}")
                print("🇵🇭 PHILIPPINES AI CONTENT PROCESSOR")
                print("Usage: python ai_content_processor.py [command] [args...]")
                print("\nCommands:")
                print("  batch [limit] [delay] [multi_version] [num_versions] - Batch processing")
                print("  multi [limit] [delay] [num_versions] - Multi-version processing")
                print("  stats - Show statistics")
                print("  single - Process 1 post")
                print("  test-multi - Test multi-version with 1 post")
                print("\nExamples:")
                print("  python ai_content_processor.py batch 10 2.0 false 1")
                print("  python ai_content_processor.py multi 5 2.0 3")
                print("  python ai_content_processor.py test-multi")
                print("  python ai_content_processor.py stats")
        else:
            # Chế độ tương tác
            print("�🇭 PHILIPPINES AI CONTENT PROCESSOR - INTERACTIVE MENU")
            print("�🎮 CHỌN CHỨC NĂNG:")
            print("1. Xử lý tất cả posts (single version)")
            print("2. Xử lý giới hạn số posts (single version)")  
            print("3. 🌐 MULTI-VERSION: Tạo nhiều version cho multi-site")
            print("4. Xem thống kê xử lý")
            print("5. Test xử lý 1 post (single version)")
            print("6. 🧪 Test multi-version với 1 post")
            print("0. Thoát")

            while True:
                try:
                    choice = input("\nChọn chức năng (0-6): ").strip()

                    if choice == "0":
                        break
                    elif choice == "1":
                        delay = float(input("Delay giữa requests (giây) [1.0]: ") or "1.0")
                        stats = processor.process_batch(delay=delay)
                    elif choice == "2":
                        limit = int(input("Số posts tối đa: "))
                        delay = float(input("Delay giữa requests (giây) [1.0]: ") or "1.0")
                        stats = processor.process_batch(limit, delay)
                    elif choice == "3":
                        print("\n🌐 MULTI-VERSION PROCESSING")
                        limit = int(input("Số posts tối đa [10]: ") or "10")
                        delay = float(input("Delay giữa requests (giây) [2.0]: ") or "2.0")
                        num_versions = int(input("Số versions tạo (1-5) [3]: ") or "3")
                        if num_versions > 5:
                            num_versions = 5
                        print(f"🚀 Sẽ tạo {num_versions} versions unique cho {limit} posts")
                        confirm = input("Tiếp tục? (y/N): ").lower()
                        if confirm == 'y':
                            stats = processor.process_batch(limit, delay, True, num_versions)
                    elif choice == "4":
                        stats = processor.get_processing_stats()
                        print(f"\n📊 THỐNG KÊ:")
                        for key, value in stats.items():
                            print(f"   {key}: {value}")
                    elif choice == "5":
                        stats = processor.process_batch(limit=1, delay=0)
                    elif choice == "6":
                        print("\n🧪 TEST MULTI-VERSION")
                        num_versions = int(input("Số versions test (1-5) [2]: ") or "2")
                        stats = processor.process_batch(limit=1, delay=0, multi_version=True, num_versions=num_versions)
                    else:
                        print("❌ Lựa chọn không hợp lệ!")

                except KeyboardInterrupt:
                    print("\n⚠️ Đã dừng bởi người dùng")
                    break
                except Exception as e:
                    print(f"❌ Lỗi: {e}")

        processor.close()
        print("\n👋 Tạm biệt!")

    except KeyboardInterrupt:
        print("\n⚠️ Chương trình bị dừng")
    except Exception as e:
        print(f"❌ Lỗi nghiêm trọng: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    main()
