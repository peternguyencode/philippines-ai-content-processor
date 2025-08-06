#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Content Processor V2 - Sử dụng Strategy Pattern
2 Strategies hoàn toàn khác nhau cho xử lý dữ liệu

Author: AI Assistant
Date: 2025-08-06
"""

import json
import logging
import sys
import time
from datetime import datetime
from typing import Any, Dict, List, Optional

import mysql.connector
from mysql.connector import Error
from tqdm import tqdm

from config import Config

# Import strategies
from prompt_strategies import PromptStrategy, PromptStrategyFactory


class AIContentProcessorV2:
    """AI Content Processor V2 với Strategy Pattern"""

    def __init__(self, strategy_name: str = "DATABASE_PIPELINE"):
        """
        Khởi tạo với strategy cụ thể

        Args:
            strategy_name: Tên strategy (DATABASE_PIPELINE hoặc CSV_PIPELINE)
        """
        print(f"🤖 Khởi tạo AI Content Processor V2 với {strategy_name}...")

        # Setup logging
        self.setup_logging()

        # Set strategy
        self.set_strategy(strategy_name)

        # MySQL connection
        self.connection = None
        self.connect_mysql()

        # Statistics
        self.stats = {"total_processed": 0, "success": 0, "errors": 0, "skipped": 0}

        print(
            f"✅ AI Content Processor V2 khởi tạo thành công với {self.current_strategy.get_strategy_name()}!"
        )

    def setup_logging(self):
        """Thiết lập logging"""
        log_filename = (
            f"ai_processing_v2_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        )

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler(log_filename, encoding="utf-8"),
                logging.StreamHandler(sys.stdout),
            ],
        )

        self.logger = logging.getLogger(__name__)
        self.logger.info("🔍 Logging V2 được thiết lập")

    def set_strategy(self, strategy_name: str):
        """
        Thiết lập strategy

        Args:
            strategy_name: Tên strategy
        """
        try:
            self.current_strategy = PromptStrategyFactory.create_strategy(strategy_name)
            self.strategy_name = strategy_name
            self.logger.info(f"🎯 Strategy được set: {strategy_name}")

            # Log strategy info
            info = PromptStrategyFactory.get_strategy_info()[strategy_name]
            self.logger.info(f"📊 Strategy Info: {info}")

        except Exception as e:
            self.logger.error(f"❌ Lỗi set strategy: {e}")
            raise

    def switch_strategy(self, new_strategy_name: str):
        """
        Chuyển đổi strategy trong runtime

        Args:
            new_strategy_name: Tên strategy mới
        """
        old_strategy = self.strategy_name
        self.set_strategy(new_strategy_name)
        self.logger.info(f"🔄 Chuyển strategy từ {old_strategy} → {new_strategy_name}")
        print(f"🔄 Đã chuyển từ {old_strategy} → {new_strategy_name}")

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
                self.ensure_posts_ai_table()
            else:
                raise ConnectionError("MySQL connection failed")

        except Error as e:
            self.logger.error(f"❌ MySQL connection error: {e}")
            sys.exit(1)

    def ensure_posts_ai_table(self):
        """Đảm bảo bảng posts_ai tồn tại với đầy đủ columns"""
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
            processing_strategy VARCHAR(50),
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

            # Thêm column processing_strategy nếu chưa có
            try:
                cursor.execute(
                    "ALTER TABLE posts_ai ADD COLUMN processing_strategy VARCHAR(50)"
                )
                self.logger.info("✅ Đã thêm column processing_strategy")
            except Error:
                # Column đã tồn tại
                pass

            cursor.close()
            self.logger.info("✅ Bảng 'posts_ai' đã sẵn sàng với Strategy support")

        except Error as e:
            self.logger.error(f"❌ Lỗi ensure posts_ai table: {e}")
            raise

    def get_unprocessed_posts(
        self, limit: Optional[int] = None, strategy_filter: Optional[str] = None
    ) -> List[Dict]:
        """
        Lấy posts chưa được xử lý hoặc chưa được xử lý bởi strategy cụ thể

        Args:
            limit: Giới hạn số posts
            strategy_filter: Chỉ lấy posts chưa xử lý bởi strategy này

        Returns:
            List posts chưa xử lý
        """
        try:
            cursor = self.connection.cursor(dictionary=True)

            if strategy_filter:
                # Lấy posts chưa được xử lý bởi strategy cụ thể
                sql = """
                SELECT p.id, p.title, p.content, p.category, p.tags
                FROM posts p
                LEFT JOIN posts_ai pa ON (p.id = pa.post_id AND pa.processing_strategy = %s)
                WHERE pa.post_id IS NULL
                ORDER BY p.created_date DESC
                """
                params = (strategy_filter,)
            else:
                # Lấy posts chưa được xử lý hoàn toàn
                sql = """
                SELECT p.id, p.title, p.content, p.category, p.tags
                FROM posts p
                LEFT JOIN posts_ai pa ON p.id = pa.post_id
                WHERE pa.post_id IS NULL
                ORDER BY p.created_date DESC
                """
                params = ()

            if limit:
                sql += f" LIMIT {limit}"

            cursor.execute(sql, params)
            posts = cursor.fetchall()
            cursor.close()

            strategy_info = f" bởi {strategy_filter}" if strategy_filter else ""
            self.logger.info(
                f"📊 Tìm thấy {len(posts)} posts chưa xử lý{strategy_info}"
            )
            return posts

        except Error as e:
            self.logger.error(f"❌ Lỗi lấy posts chưa xử lý: {e}")
            return []

    def process_single_post(self, post: Dict[str, Any]) -> Dict[str, Any]:
        """
        Xử lý một post với strategy hiện tại

        Args:
            post: Dict chứa thông tin post

        Returns:
            Dict chứa kết quả xử lý
        """
        post_id = post["id"]
        title = post["title"]
        content = post["content"]
        category = post.get("category", "")
        tags = post.get("tags", "")

        result = {
            "post_id": post_id,
            "success": False,
            "error": None,
            "strategy_used": self.strategy_name,
        }

        try:
            self.logger.info(
                f"🔄 Xử lý Post ID {post_id} với {self.strategy_name}: {title[:50]}..."
            )

            # Cập nhật trạng thái processing
            self.update_processing_status(post_id, "processing")

            # Xử lý với strategy hiện tại
            ai_result = self.current_strategy.execute_strategy(
                content=content, title=title, category=category, tags=tags
            )

            # Lưu kết quả
            if self.save_strategy_result(post_id, title, ai_result, category, tags):
                result["success"] = True
                result["ai_result"] = ai_result
                self.stats["success"] += 1
                self.logger.info(
                    f"🎉 Hoàn thành Post ID {post_id} với {self.strategy_name}"
                )
            else:
                raise Exception("Lỗi lưu strategy result")

        except Exception as e:
            error_msg = str(e)
            self.logger.error(f"❌ Lỗi xử lý Post ID {post_id}: {error_msg}")

            # Cập nhật trạng thái lỗi
            self.update_processing_status(post_id, "error", error_msg)

            result["error"] = error_msg
            self.stats["errors"] += 1

        self.stats["total_processed"] += 1
        return result

    def save_strategy_result(
        self,
        post_id: int,
        title: str,
        ai_result: Dict[str, Any],
        category: str = "",
        original_tags: str = "",
    ) -> bool:
        """
        Lưu kết quả strategy vào database

        Args:
            post_id: ID của post gốc
            title: Tiêu đề
            ai_result: Kết quả từ strategy
            category: Danh mục
            original_tags: Tags gốc

        Returns:
            bool: True nếu thành công
        """
        try:
            cursor = self.connection.cursor()

            # Map fields theo strategy
            field_mapping = self.current_strategy.get_database_fields()

            # Chuẩn bị dữ liệu theo strategy
            if self.strategy_name == "DATABASE_PIPELINE":
                # Database strategy có đủ fields
                ai_content = ai_result.get("ai_content", "")
                meta_title = ai_result.get("meta_title", "")
                meta_description = ai_result.get("meta_description", "")
                image_prompt = ai_result.get("image_prompt", "")
                tags = ai_result.get("suggested_tags", "") or original_tags
                ai_notes = ai_result.get("notes", "")

            elif self.strategy_name == "CSV_PIPELINE":
                # CSV strategy chỉ có 3 fields chính
                ai_content = ai_result.get("paraphrased_content", "")
                meta_title = title[:70]  # Fallback
                meta_description = (
                    ai_content[:160] + "..." if len(ai_content) > 160 else ai_content
                )
                image_prompt = ""  # CSV strategy không support images
                tags = original_tags
                ai_notes = ai_result.get("localization_notes", "")
                category = ai_result.get("classification", category)

            # Insert với ON DUPLICATE KEY UPDATE
            insert_sql = """
            INSERT INTO posts_ai (
                post_id, title, ai_content, meta_title, meta_description,
                image_url, image_prompt, tags, category, ai_model, ai_notes, 
                processing_strategy, processing_status
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                ai_content = VALUES(ai_content),
                meta_title = VALUES(meta_title),
                meta_description = VALUES(meta_description),
                image_prompt = VALUES(image_prompt),
                tags = VALUES(tags),
                category = VALUES(category),
                ai_model = VALUES(ai_model),
                ai_notes = VALUES(ai_notes),
                processing_strategy = VALUES(processing_strategy),
                processing_status = VALUES(processing_status),
                updated_date = CURRENT_TIMESTAMP
            """

            values = (
                post_id,
                title,
                ai_content,
                meta_title,
                meta_description,
                ai_result.get(
                    "image_url", ""
                ),  # Sẽ được fill sau nếu có image generation
                image_prompt,
                tags,
                category,
                ai_result.get("model_used", "gpt-3.5-turbo"),
                ai_notes,
                self.strategy_name,
                "completed",
            )

            cursor.execute(insert_sql, values)
            cursor.close()

            self.logger.info(
                f"✅ Lưu {self.strategy_name} result thành công: Post ID {post_id}"
            )
            return True

        except Error as e:
            self.logger.error(f"❌ Lỗi lưu strategy result: {e}")
            return False

    def update_processing_status(self, post_id: int, status: str, notes: str = ""):
        """Cập nhật trạng thái xử lý"""
        try:
            cursor = self.connection.cursor()

            if status == "processing":
                # Insert processing record với strategy info
                sql = """
                INSERT INTO posts_ai (post_id, title, ai_content, processing_status, ai_notes, processing_strategy)
                VALUES (%s, 'Processing...', 'Processing...', %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    processing_status = VALUES(processing_status),
                    ai_notes = VALUES(ai_notes),
                    processing_strategy = VALUES(processing_strategy),
                    updated_date = CURRENT_TIMESTAMP
                """
                cursor.execute(
                    sql,
                    (
                        post_id,
                        status,
                        f"Processing with {self.strategy_name}: {notes}",
                        self.strategy_name,
                    ),
                )
            else:
                # Update existing record
                sql = """
                UPDATE posts_ai 
                SET processing_status = %s, 
                    ai_notes = CONCAT(COALESCE(ai_notes, ''), %s),
                    processing_strategy = %s,
                    updated_date = CURRENT_TIMESTAMP
                WHERE post_id = %s
                """
                cursor.execute(
                    sql,
                    (
                        status,
                        f" | {notes}" if notes else "",
                        self.strategy_name,
                        post_id,
                    ),
                )

            cursor.close()

        except Error as e:
            self.logger.error(f"❌ Lỗi cập nhật status: {e}")

    def process_batch(
        self, limit: Optional[int] = None, delay: float = 1.0
    ) -> Dict[str, Any]:
        """
        Xử lý batch posts với strategy hiện tại

        Args:
            limit: Giới hạn số posts xử lý
            delay: Delay giữa requests (giây)

        Returns:
            Dict chứa thống kê kết quả
        """
        print(f"\n🚀 BẮT ĐẦU BATCH PROCESSING VỚI {self.strategy_name}")
        print("=" * 60)

        # Reset stats
        self.stats = {"total_processed": 0, "success": 0, "errors": 0, "skipped": 0}

        # Lấy posts chưa xử lý bởi strategy hiện tại
        posts = self.get_unprocessed_posts(limit, self.strategy_name)

        if not posts:
            print(f"ℹ️ Không có posts nào cần xử lý với {self.strategy_name}!")
            return self.stats

        # Hiển thị strategy info
        strategy_info = PromptStrategyFactory.get_strategy_info()[self.strategy_name]
        print(f"🎯 Strategy: {strategy_info['name']}")
        print(f"📊 Description: {strategy_info['description']}")
        print(f"📋 Output Fields: {strategy_info['output_fields']}")
        print(f"🎨 Supports Images: {strategy_info['supports_images']}")
        print(f"💰 Cost per Request: {strategy_info['cost_per_request']}")
        print(f"📝 Sẽ xử lý {len(posts)} posts")
        print(f"⏱️ Delay giữa requests: {delay} giây")

        # Bắt đầu xử lý
        start_time = time.time()

        with tqdm(
            total=len(posts), desc=f"AI Processing ({self.strategy_name})"
        ) as pbar:
            for post in posts:
                try:
                    # Xử lý post
                    result = self.process_single_post(post)

                    # Cập nhật progress bar
                    status = "✅" if result["success"] else "❌"
                    pbar.set_postfix_str(f"{status} Post {result['post_id']}")
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

        print(f"\n📈 KẾT QUẢ {self.strategy_name} PROCESSING:")
        print(f"   Strategy Used: {self.strategy_name}")
        print(f"   Tổng số posts xử lý: {self.stats['total_processed']}")
        print(f"   Thành công: {self.stats['success']}")
        print(f"   Lỗi: {self.stats['errors']}")
        print(f"   Thời gian: {duration:.2f} giây")
        if self.stats["total_processed"] > 0:
            print(f"   Tốc độ: {self.stats['total_processed']/duration:.2f} posts/giây")

            # Tính cost estimate
            cost_per_request = float(
                strategy_info["cost_per_request"].replace("~$", "")
            )
            estimated_cost = self.stats["success"] * cost_per_request
            print(f"   Chi phí ước tính: ~${estimated_cost:.4f}")

        return self.stats

    def get_processing_stats_by_strategy(self) -> Dict[str, Any]:
        """Lấy thống kê xử lý theo strategy"""
        try:
            cursor = self.connection.cursor(dictionary=True)

            # Thống kê tổng quan
            cursor.execute("SELECT COUNT(*) as total FROM posts")
            total_posts = cursor.fetchone()["total"]

            # Thống kê theo strategy
            cursor.execute(
                """
                SELECT processing_strategy, processing_status, COUNT(*) as count
                FROM posts_ai 
                WHERE processing_strategy IS NOT NULL
                GROUP BY processing_strategy, processing_status
            """
            )
            strategy_stats = cursor.fetchall()

            # Tổng số posts đã xử lý
            cursor.execute("SELECT COUNT(DISTINCT post_id) as processed FROM posts_ai")
            processed_posts = cursor.fetchone()["processed"]

            cursor.close()

            # Organize stats
            stats = {
                "total_posts": total_posts,
                "processed_posts": processed_posts,
                "unprocessed_posts": total_posts - processed_posts,
                "by_strategy": {},
            }

            # Group by strategy
            for item in strategy_stats:
                strategy = item["processing_strategy"]
                status = item["processing_status"]
                count = item["count"]

                if strategy not in stats["by_strategy"]:
                    stats["by_strategy"][strategy] = {}

                stats["by_strategy"][strategy][status] = count

            return stats

        except Error as e:
            self.logger.error(f"❌ Lỗi lấy stats by strategy: {e}")
            return {}

    def close(self):
        """Đóng kết nối"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            self.logger.info("✅ MySQL connection closed")


def main():
    """Hàm main với Strategy Pattern"""
    print("🤖 AI CONTENT PROCESSOR V2 - STRATEGY PATTERN")
    print("=" * 60)
    print("2 Strategies hoàn toàn khác nhau cho xử lý dữ liệu")
    print()

    # Hiển thị strategies available
    strategies = PromptStrategyFactory.get_available_strategies()
    strategy_info = PromptStrategyFactory.get_strategy_info()

    print("🎯 AVAILABLE STRATEGIES:")
    for i, strategy in enumerate(strategies, 1):
        info = strategy_info[strategy]
        print(f"   {i}. {strategy}")
        print(f"      └── {info['description']}")
        print(
            f"          📊 {info['output_fields']} fields | 🎨 Images: {info['supports_images']} | 💰 {info['cost_per_request']}"
        )

    try:
        # Chọn strategy
        print(f"\n🎮 CHỌN STRATEGY:")
        for i, strategy in enumerate(strategies, 1):
            print(f"{i}. {strategy}")
        print("0. Thoát")

        while True:
            try:
                choice = input(
                    f"\nChọn strategy (1-{len(strategies)}, 0 để thoát): "
                ).strip()

                if choice == "0":
                    return
                elif choice.isdigit() and 1 <= int(choice) <= len(strategies):
                    selected_strategy = strategies[int(choice) - 1]
                    break
                else:
                    print("❌ Lựa chọn không hợp lệ!")
            except KeyboardInterrupt:
                print("\n👋 Tạm biệt!")
                return

        # Khởi tạo processor với strategy đã chọn
        processor = AIContentProcessorV2(selected_strategy)

        print(f"\n🎮 CHỨC NĂNG VỚI {selected_strategy}:")
        print("1. Xử lý tất cả posts chưa được AI xử lý")
        print("2. Xử lý giới hạn số posts")
        print("3. Xem thống kê theo strategy")
        print("4. Xử lý 1 post để test")
        print("5. Chuyển đổi strategy")
        print("0. Thoát")

        while True:
            try:
                choice = input("\nChọn chức năng (0-5): ").strip()

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
                    stats = processor.get_processing_stats_by_strategy()
                    print(f"\n📊 THỐNG KÊ THEO STRATEGY:")
                    for key, value in stats.items():
                        print(f"   {key}: {value}")
                elif choice == "4":
                    stats = processor.process_batch(limit=1, delay=0)
                elif choice == "5":
                    print(f"\n🔄 CHUYỂN ĐỔI STRATEGY:")
                    for i, strategy in enumerate(strategies, 1):
                        marker = (
                            " (HIỆN TẠI)" if strategy == processor.strategy_name else ""
                        )
                        print(f"{i}. {strategy}{marker}")

                    try:
                        new_choice = int(
                            input(f"Chọn strategy mới (1-{len(strategies)}): ")
                        )
                        if 1 <= new_choice <= len(strategies):
                            new_strategy = strategies[new_choice - 1]
                            processor.switch_strategy(new_strategy)
                        else:
                            print("❌ Lựa chọn không hợp lệ!")
                    except ValueError:
                        print("❌ Vui lòng nhập số!")
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


if __name__ == "__main__":
    main()
