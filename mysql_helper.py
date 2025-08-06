#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MySQL Helper: Xử lý import/export dữ liệu với MySQL Database
Author: AI Assistant
Date: 2025-08-05
"""

import json
import logging
import re
from datetime import datetime
from typing import Any, Dict, List, Optional

import mysql.connector
from mysql.connector import Error

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MySQLHelper:
    """Lớp xử lý kết nối và thao tác với MySQL Database"""

    def __init__(
        self,
        host="localhost",
        port=3308,
        user="root",
        password="baivietwp_password",
        database="mydb",
    ):
        """
        Khởi tạo kết nối MySQL

        Args:
            host: MySQL host
            port: MySQL port
            user: MySQL username
            password: MySQL password
            database: Database name
        """
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

        try:
            self.connect()
            self.create_posts_table()
            logger.info("✅ MySQL Helper khởi tạo thành công!")

        except Exception as e:
            logger.error(f"❌ Lỗi khởi tạo MySQL Helper: {str(e)}")
            raise

    def connect(self):
        """Tạo kết nối tới MySQL Database"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
                charset="utf8mb4",
                collation="utf8mb4_unicode_ci",
            )

            if self.connection.is_connected():
                logger.info(
                    f"✅ Kết nối MySQL thành công: {self.host}:{self.port}/{self.database}"
                )

        except Error as e:
            logger.error(f"❌ Lỗi kết nối MySQL: {str(e)}")
            raise

    def create_posts_table(self):
        """Tạo bảng posts nếu chưa tồn tại"""
        create_table_query = """
        CREATE TABLE IF NOT EXISTS posts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            source_title VARCHAR(255) DEFAULT NULL,
            status VARCHAR(50) DEFAULT 'pending',
            title TEXT NOT NULL,
            content LONGTEXT DEFAULT NULL,
            original_url TEXT DEFAULT NULL,
            image_url TEXT DEFAULT NULL,
            meta_title TEXT DEFAULT NULL,
            meta_description TEXT DEFAULT NULL,
            created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            keywords TEXT DEFAULT NULL,
            category VARCHAR(100) DEFAULT 'Casino',
            tags TEXT DEFAULT NULL,
            ai_model VARCHAR(50) DEFAULT NULL,
            notes TEXT DEFAULT NULL,
            processing_status VARCHAR(50) DEFAULT 'pending',
            
            UNIQUE KEY unique_title (title(255)),
            UNIQUE KEY unique_url (original_url(255)),
            INDEX idx_status (status),
            INDEX idx_category (category),
            INDEX idx_created_date (created_date)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """

        try:
            cursor = self.connection.cursor()
            cursor.execute(create_table_query)
            self.connection.commit()
            cursor.close()
            logger.info("✅ Bảng 'posts' đã sẵn sàng")

        except Error as e:
            logger.error(f"❌ Lỗi tạo bảng posts: {str(e)}")
            raise

    def clean_html_content(self, html_content: str) -> str:
        """Làm sạch nội dung HTML"""
        if not html_content:
            return ""

        # Remove HTML tags
        clean_text = re.sub(r"<[^>]+>", "", html_content)
        # Remove extra spaces
        clean_text = re.sub(r"\s+", " ", clean_text).strip()
        # Remove HTML entities
        clean_text = re.sub(r"&#\d+;", "", clean_text)
        # Remove special characters that might cause issues
        clean_text = clean_text.replace("\x00", "").replace("\r", "").replace("\n", " ")

        return clean_text

    def extract_keywords_from_content(self, content: str, title: str) -> str:
        """Trích xuất keywords từ content và title"""
        if not content and not title:
            return ""

        # Common casino keywords
        casino_keywords = [
            "casino",
            "bonus",
            "free",
            "sign up",
            "deposit",
            "philippines",
            "game",
            "slot",
            "win",
        ]

        text = f"{title} {content}".lower()
        found_keywords = [kw for kw in casino_keywords if kw in text]

        return ", ".join(found_keywords[:10])  # Limit to 10 keywords

    def insert_post(self, post_data: Dict[str, Any]) -> bool:
        """
        Insert một post vào database

        Args:
            post_data: Dictionary chứa dữ liệu post

        Returns:
            bool: True nếu thành công, False nếu thất bại
        """
        try:
            # Clean and prepare data
            title = post_data.get("title", "No title").strip()
            content = self.clean_html_content(post_data.get("content", ""))
            original_url = post_data.get("link", "")
            image_url = post_data.get("featured_image", "")

            # Create meta description from content
            meta_description = content[:160] + "..." if len(content) > 160 else content

            # Extract keywords
            keywords = self.extract_keywords_from_content(content, title)

            insert_query = """
            INSERT INTO posts (
                source_title, status, title, content, original_url, image_url,
                meta_title, meta_description, created_date, keywords, category,
                tags, ai_model, notes, processing_status
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            """

            values = (
                "bonus365casinoall",  # source_title
                "imported",  # status
                title,  # title
                content,  # content
                original_url,  # original_url
                image_url,  # image_url
                title,  # meta_title
                meta_description,  # meta_description
                datetime.now(),  # created_date
                keywords,  # keywords
                "Casino",  # category
                "bonus, casino, philippines, imported",  # tags
                "Manual Import",  # ai_model
                f"Imported from JSON at {datetime.now()}",  # notes
                "JSON-Imported",  # processing_status
            )

            cursor = self.connection.cursor()
            cursor.execute(insert_query, values)
            self.connection.commit()
            cursor.close()

            logger.info(f"✅ Imported: {title[:50]}...")
            return True

        except mysql.connector.IntegrityError as e:
            if "Duplicate entry" in str(e):
                logger.warning(f"⚠️ Duplicate skipped: {title[:50]}...")
                return False
            else:
                logger.error(f"❌ Integrity error: {str(e)}")
                return False

        except Error as e:
            logger.error(f"❌ Error inserting post: {str(e)}")
            return False

    def import_from_json(self, json_file: str) -> Dict[str, int]:
        """
        Import toàn bộ dữ liệu từ file JSON

        Args:
            json_file: Đường dẫn tới file JSON

        Returns:
            Dict chứa thống kê import
        """
        stats = {"total": 0, "success": 0, "duplicates": 0, "errors": 0}

        try:
            # Load JSON data
            with open(json_file, "r", encoding="utf-8") as f:
                posts = json.load(f)

            stats["total"] = len(posts)
            logger.info(f"📊 Loaded {stats['total']} posts from {json_file}")

            # Import each post
            for i, post in enumerate(posts, 1):
                try:
                    logger.info(
                        f"[{i}/{stats['total']}] Processing: {post.get('title', 'No title')[:50]}..."
                    )

                    if self.insert_post(post):
                        stats["success"] += 1
                    else:
                        stats["duplicates"] += 1

                except Exception as e:
                    logger.error(f"❌ Error processing post {i}: {str(e)}")
                    stats["errors"] += 1

            # Print final stats
            logger.info(f"\n📈 IMPORT COMPLETED:")
            logger.info(f"   Total processed: {stats['total']}")
            logger.info(f"   Successfully imported: {stats['success']}")
            logger.info(f"   Duplicates skipped: {stats['duplicates']}")
            logger.info(f"   Errors: {stats['errors']}")

        except FileNotFoundError:
            logger.error(f"❌ File not found: {json_file}")
            stats["errors"] = stats["total"] = 1

        except json.JSONDecodeError as e:
            logger.error(f"❌ Invalid JSON file: {str(e)}")
            stats["errors"] = stats["total"] = 1

        except Exception as e:
            logger.error(f"❌ Unexpected error: {str(e)}")
            stats["errors"] += 1

        return stats

    def export_to_json(self, output_file: str, limit: int = None) -> bool:
        """
        Export dữ liệu từ MySQL ra file JSON

        Args:
            output_file: Đường dẫn file JSON output
            limit: Giới hạn số bài export (None = tất cả)

        Returns:
            bool: True nếu thành công
        """
        try:
            query = "SELECT * FROM posts ORDER BY created_date DESC"
            if limit:
                query += f" LIMIT {limit}"

            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query)
            posts = cursor.fetchall()
            cursor.close()

            # Convert datetime objects to strings
            for post in posts:
                if post["created_date"]:
                    post["created_date"] = post["created_date"].isoformat()

            # Write to JSON file
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(posts, f, ensure_ascii=False, indent=2)

            logger.info(f"✅ Exported {len(posts)} posts to {output_file}")
            return True

        except Exception as e:
            logger.error(f"❌ Export error: {str(e)}")
            return False

    def get_posts_count(self) -> Dict[str, int]:
        """Lấy thống kê số lượng posts theo status"""
        try:
            cursor = self.connection.cursor()

            # Total posts
            cursor.execute("SELECT COUNT(*) as total FROM posts")
            total = cursor.fetchone()[0]

            # Posts by status
            cursor.execute(
                "SELECT status, COUNT(*) as count FROM posts GROUP BY status"
            )
            status_counts = dict(cursor.fetchall())

            cursor.close()

            return {"total": total, "by_status": status_counts}

        except Exception as e:
            logger.error(f"❌ Error getting posts count: {str(e)}")
            return {"total": 0, "by_status": {}}

    def check_connection(self) -> bool:
        """Kiểm tra kết nối MySQL"""
        try:
            if self.connection and self.connection.is_connected():
                cursor = self.connection.cursor()
                cursor.execute("SELECT 1")
                cursor.fetchone()
                cursor.close()
                return True
            else:
                return False
        except:
            return False

    def close(self):
        """Đóng kết nối MySQL"""
        try:
            if self.connection and self.connection.is_connected():
                self.connection.close()
                logger.info("✅ MySQL connection closed")
        except Exception as e:
            logger.error(f"❌ Error closing connection: {str(e)}")


# Main function for testing
if __name__ == "__main__":
    print("🔥 MYSQL HELPER TEST 🔥")
    print("=" * 50)

    try:
        # Initialize MySQL Helper
        mysql_helper = MySQLHelper()

        # Test connection
        if mysql_helper.check_connection():
            print("✅ MySQL connection is healthy")

            # Get current posts count
            stats = mysql_helper.get_posts_count()
            print(f"📊 Current posts in database: {stats['total']}")
            print(f"📊 By status: {stats['by_status']}")

            # Test import (uncomment to run)
            # print("\n🚀 Starting JSON import...")
            # import_stats = mysql_helper.import_from_json('bonus365casinoall_posts.json')
            # print(f"🎉 Import completed: {import_stats}")

        else:
            print("❌ MySQL connection failed")

    except Exception as e:
        print(f"❌ Error: {str(e)}")

    finally:
        if "mysql_helper" in locals():
            mysql_helper.close()
