#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KHÔI PHỤC DỰ ÁN ĐƠN GIẢN TỪ BACKUP
Restore project từ backup CSV một cách đơn giản
"""

import csv
import os
import sys

import mysql.connector
from mysql.connector import Error


def restore_project_simple():
    """Khôi phục dự án đơn giản"""
    print("🔄 KHÔI PHỤC DỰ ÁN TỪ BACKUP CSV")
    print("=" * 40)

    backup_file = "c:\\Users\\Admin\\Downloads\\posts.csv"

    # Kiểm tra file backup
    if not os.path.exists(backup_file):
        print(f"❌ Không tìm thấy file: {backup_file}")
        print("📁 Vui lòng đảm bảo file posts.csv ở đúng vị trí")
        return False

    print(f"✅ Tìm thấy file backup: {backup_file}")

    # Cảnh báo
    print("⚠️  CẢNH BÁO: Thao tác này sẽ XÓA dữ liệu hiện tại!")
    confirm = input("❓ Bạn có chắc muốn khôi phục? (yes/no): ").lower().strip()

    if confirm not in ["yes", "y"]:
        print("✋ Đã hủy khôi phục")
        return False

    try:
        # Kết nối database
        print("🔌 Đang kết nối database...")
        conn = mysql.connector.connect(
            host="localhost",
            port=3308,
            user="root",
            password="baivietwp_password",
            database="mydb",
            charset="utf8mb4",
            autocommit=True,
        )

        if not conn.is_connected():
            print("❌ Không thể kết nối database")
            return False

        print("✅ Kết nối database thành công")

        cursor = conn.cursor()

        # Tạo bảng posts nếu chưa có
        print("🔧 Tạo bảng posts...")
        create_posts_sql = """
        CREATE TABLE IF NOT EXISTS posts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            source_title VARCHAR(255),
            status VARCHAR(50),
            title VARCHAR(500) NOT NULL,
            content TEXT,
            original_url TEXT,
            image_url TEXT,
            meta_title VARCHAR(255),
            meta_description TEXT,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            keywords TEXT,
            category VARCHAR(100),
            tags TEXT,
            ai_model VARCHAR(50),
            notes TEXT,
            processing_status VARCHAR(50)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
        cursor.execute(create_posts_sql)

        # Tạo bảng posts_ai
        print("🔧 Tạo bảng posts_ai...")
        create_posts_ai_sql = """
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
            UNIQUE KEY unique_post_id (post_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
        cursor.execute(create_posts_ai_sql)

        # Xóa dữ liệu cũ
        print("🗑️ Xóa dữ liệu cũ...")
        cursor.execute("DELETE FROM posts_ai")
        cursor.execute("DELETE FROM posts")
        cursor.execute("ALTER TABLE posts AUTO_INCREMENT = 1")

        # Đọc và import CSV
        print("📥 Import dữ liệu từ backup...")
        with open(backup_file, "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)

            insert_sql = """
            INSERT INTO posts (
                id, source_title, status, title, content, original_url,
                image_url, meta_title, meta_description, created_date,
                keywords, category, tags, ai_model, notes, processing_status
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            imported_count = 0
            for row in reader:
                try:
                    values = (
                        int(row["id"]),
                        row["source_title"],
                        row["status"],
                        row["title"],
                        row["content"],
                        row["original_url"],
                        row["image_url"],
                        row["meta_title"],
                        row["meta_description"],
                        row["created_date"],
                        row["keywords"],
                        row["category"],
                        row["tags"],
                        row["ai_model"],
                        row["notes"],
                        row["processing_status"],
                    )

                    cursor.execute(insert_sql, values)
                    imported_count += 1

                    if imported_count % 10 == 0:
                        print(f"   📊 Đã import {imported_count} posts...")

                except Exception as e:
                    print(f"⚠️ Lỗi import row ID {row.get('id', '?')}: {e}")
                    continue

        # Kiểm tra kết quả
        cursor.execute("SELECT COUNT(*) FROM posts")
        total_posts = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM posts_ai")
        processed_posts = cursor.fetchone()[0]

        print(f"\n📊 KẾT QUẢ IMPORT:")
        print(f"   ✅ Tổng posts: {total_posts}")
        print(f"   📝 Đã AI processing: {processed_posts}")
        print(f"   ⏳ Chưa xử lý: {total_posts - processed_posts}")

        # Sample posts
        cursor.execute("SELECT id, title, category FROM posts LIMIT 3")
        samples = cursor.fetchall()

        print(f"\n📋 Sample posts:")
        for post in samples:
            print(f"   #{post[0]}: {post[1][:50]}... [{post[2]}]")

        cursor.close()
        conn.close()

        print(f"\n🎉 KHÔI PHỤC THÀNH CÔNG!")
        print("✅ Database đã sẵn sàng")
        print("✅ Dữ liệu đã được import")

        return True

    except Error as e:
        print(f"❌ Lỗi database: {e}")
        return False
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return False


def test_ai_processor():
    """Test AI processor sau khi restore"""
    print(f"\n🧪 TESTING AI PROCESSOR...")

    try:
        import subprocess

        # Test stats command
        result = subprocess.run(
            ["python", "ai_content_processor.py", "stats"],
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode == 0 and "total_posts" in result.stdout:
            print("✅ AI Processor hoạt động bình thường")
            print("📊 Stats output:")
            for line in result.stdout.split("\n"):
                if (
                    "total_posts" in line
                    or "processed_posts" in line
                    or "unprocessed" in line
                ):
                    print(f"   {line.strip()}")
            return True
        else:
            print("❌ AI Processor có vấn đề")
            if result.stderr:
                print(f"Error: {result.stderr}")
            return False

    except Exception as e:
        print(f"⚠️ Không thể test AI Processor: {e}")
        return False


def create_startup_guide():
    """Tạo hướng dẫn khởi động"""
    guide = """# 🚀 DỰ ÁN ĐÃ ĐƯỢC KHÔI PHỤC!

## ✅ Trạng thái hiện tại:
- ✅ Database: Connected (localhost:3308)
- ✅ Posts table: Đã có dữ liệu từ backup
- ✅ Posts_ai table: Sẵn sàng AI processing

## 🎯 Cách sử dụng:

### 1. Xem thống kê:
```bash
python ai_content_processor.py stats
```

### 2. Test 1 post:
```bash
python ai_content_processor.py single
```

### 3. Batch processing:
```bash
python ai_content_processor.py batch 5 1.0
```

### 4. Interactive menu:
```bash
python ai_content_processor.py
```

## 🎉 SẴN SÀNG SỬ DỤNG!
Chạy: `python ai_content_processor.py` để bắt đầu.
"""

    try:
        with open("PROJECT_RESTORED.md", "w", encoding="utf-8") as f:
            f.write(guide)
        print("✅ Tạo hướng dẫn: PROJECT_RESTORED.md")
    except Exception as e:
        print(f"⚠️ Không thể tạo guide: {e}")


def main():
    """Main function"""
    try:
        # Khôi phục dự án
        if restore_project_simple():
            # Test AI processor
            test_ai_processor()

            # Tạo guide
            create_startup_guide()

            print(f"\n🎉 HOÀN THÀNH!")
            print("=" * 30)
            print("🚀 Chạy ngay: python ai_content_processor.py")

            # Hỏi có muốn chạy test không
            run_test = input("\n❓ Muốn chạy test ngay? (y/n): ").lower().strip()
            if run_test in ["y", "yes"]:
                os.system("python ai_content_processor.py stats")
        else:
            print("\n❌ Khôi phục thất bại!")

    except KeyboardInterrupt:
        print("\n⚠️ Đã hủy bởi người dùng")
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")


if __name__ == "__main__":
    main()
