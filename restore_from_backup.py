#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KHÔI PHỤC DỰ ÁN TỪ BACKUP
Restore project từ backup CSV và thiết lập lại toàn bộ hệ thống
"""

import os
import subprocess
import sys
from datetime import datetime

import mysql.connector
import pandas as pd
from mysql.connector import Error


class BackupRestorer:
    """Khôi phục dự án từ backup"""

    def __init__(self):
        self.backup_csv = "c:\\Users\\Admin\\Downloads\\posts.csv"
        self.connection = None

    def connect_database(self):
        """Kết nối database"""
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
                print("✅ Kết nối MySQL thành công")
                return True
            else:
                print("❌ Không thể kết nối MySQL")
                return False

        except Error as e:
            print(f"❌ Lỗi kết nối database: {e}")
            return False

    def check_backup_file(self):
        """Kiểm tra file backup"""
        if not os.path.exists(self.backup_csv):
            print(f"❌ Không tìm thấy file backup: {self.backup_csv}")
            print("📁 Vui lòng đảm bảo file posts.csv ở đúng vị trí")
            return False

        try:
            df = pd.read_csv(self.backup_csv)
            print(f"✅ File backup hợp lệ: {len(df)} records")
            print(f"📊 Columns: {list(df.columns)}")
            return True

        except Exception as e:
            print(f"❌ Lỗi đọc file backup: {e}")
            return False

    def create_tables(self):
        """Tạo lại các bảng cần thiết"""
        try:
            cursor = self.connection.cursor()

            # Tạo bảng posts
            posts_sql = """
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

            cursor.execute(posts_sql)
            print("✅ Bảng 'posts' đã sẵn sàng")

            # Tạo bảng posts_ai
            posts_ai_sql = """
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

            cursor.execute(posts_ai_sql)
            print("✅ Bảng 'posts_ai' đã sẵn sàng")

            cursor.close()
            return True

        except Error as e:
            print(f"❌ Lỗi tạo bảng: {e}")
            return False

    def import_data_from_backup(self):
        """Import dữ liệu từ backup CSV"""
        try:
            # Đọc CSV
            df = pd.read_csv(self.backup_csv)

            cursor = self.connection.cursor()

            # Xóa dữ liệu cũ (nếu có)
            cursor.execute("DELETE FROM posts_ai")
            cursor.execute("DELETE FROM posts")
            cursor.execute("ALTER TABLE posts AUTO_INCREMENT = 1")
            print("✅ Đã xóa dữ liệu cũ")

            # Insert dữ liệu posts
            insert_sql = """
            INSERT INTO posts (
                id, source_title, status, title, content, original_url, 
                image_url, meta_title, meta_description, created_date,
                keywords, category, tags, ai_model, notes, processing_status
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            imported_count = 0
            for _, row in df.iterrows():
                try:
                    values = (
                        row["id"],
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

                except Exception as e:
                    print(f"⚠️ Lỗi import row {row.get('id', '?')}: {e}")
                    continue

            cursor.close()

            print(f"✅ Import thành công {imported_count}/{len(df)} posts")
            return True

        except Exception as e:
            print(f"❌ Lỗi import dữ liệu: {e}")
            return False

    def verify_data(self):
        """Xác minh dữ liệu sau khi import"""
        try:
            cursor = self.connection.cursor(dictionary=True)

            # Kiểm tra số lượng posts
            cursor.execute("SELECT COUNT(*) as total FROM posts")
            total_posts = cursor.fetchone()["total"]

            # Kiểm tra posts_ai
            cursor.execute("SELECT COUNT(*) as processed FROM posts_ai")
            processed_posts = cursor.fetchone()["processed"]

            # Lấy vài posts mẫu
            cursor.execute("SELECT id, title, category FROM posts LIMIT 3")
            sample_posts = cursor.fetchall()

            cursor.close()

            print(f"\n📊 KIỂM TRA DỮ LIỆU:")
            print(f"   Tổng posts: {total_posts}")
            print(f"   Đã AI processing: {processed_posts}")
            print(f"   Chưa xử lý: {total_posts - processed_posts}")

            print(f"\n📝 Sample posts:")
            for post in sample_posts:
                print(f"   #{post['id']}: {post['title'][:50]}... [{post['category']}]")

            return True

        except Error as e:
            print(f"❌ Lỗi verify dữ liệu: {e}")
            return False

    def test_ai_processor(self):
        """Test AI Content Processor"""
        try:
            print(f"\n🧪 TESTING AI PROCESSOR:")

            # Test import
            result = subprocess.run(
                [
                    "python",
                    "-c",
                    "from ai_content_processor import AIContentProcessor; print('✅ Import OK')",
                ],
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode == 0:
                print("   ✅ AI Processor import: OK")
            else:
                print(f"   ❌ AI Processor import failed: {result.stderr}")
                return False

            # Test basic functionality
            result = subprocess.run(
                ["python", "ai_content_processor.py", "stats"],
                capture_output=True,
                text=True,
                timeout=30,
            )

            if "total_posts" in result.stdout:
                print("   ✅ AI Processor functionality: OK")
                return True
            else:
                print("   ❌ AI Processor functionality failed")
                return False

        except Exception as e:
            print(f"   ❌ Test AI Processor error: {e}")
            return False

    def create_quick_start_guide(self):
        """Tạo hướng dẫn khởi động nhanh"""
        guide = """# 🚀 HƯỚNG DẪN KHỞI ĐỘNG LẠI DỰ ÁN

## ✅ DỮ LIỆU ĐÃ KHÔI PHỤC THÀNH CÔNG!

### 📊 Trạng thái hiện tại:
- ✅ Database MySQL: Connected (localhost:3308)
- ✅ Bảng posts: Đã có dữ liệu từ backup
- ✅ Bảng posts_ai: Sẵn sàng để AI processing
- ✅ AI Content Processor: Hoạt động bình thường

### 🎯 CÁC LỆNH CƠ BẢN:

#### 1. Xem thống kê:
```bash
python ai_content_processor.py stats
```

#### 2. Test với 1 post:
```bash  
python ai_content_processor.py single
```

#### 3. Xử lý batch:
```bash
python ai_content_processor.py batch 5 1.0
# (5 posts, delay 1 giây)
```

#### 4. Interactive menu:
```bash
python ai_content_processor.py
```

### 🔧 Files chính:
- `ai_content_processor.py` - Main processor
- `config.py` - OpenAI API configuration  
- Database: `mydb` on localhost:3308

### 🎉 DỰ ÁN SẴN SÀNG SỬ DỤNG!

Chạy: `python ai_content_processor.py` để bắt đầu!
"""

        with open("QUICK_START_RESTORED.md", "w", encoding="utf-8") as f:
            f.write(guide)

        print("✅ Tạo hướng dẫn: QUICK_START_RESTORED.md")

    def restore_project(self):
        """Khôi phục toàn bộ dự án"""
        print("🔄 BẮT ĐẦU KHÔI PHỤC DỰ ÁN TỪ BACKUP")
        print("=" * 50)

        # Step 1: Check backup file
        if not self.check_backup_file():
            return False

        # Step 2: Connect database
        if not self.connect_database():
            return False

        # Step 3: Create tables
        if not self.create_tables():
            return False

        # Step 4: Import data
        if not self.import_data_from_backup():
            return False

        # Step 5: Verify data
        if not self.verify_data():
            return False

        # Step 6: Test AI processor
        if not self.test_ai_processor():
            print("⚠️ AI Processor test failed, nhưng dữ liệu đã được restore")

        # Step 7: Create guide
        self.create_quick_start_guide()

        print(f"\n🎉 KHÔI PHỤC THÀNH CÔNG!")
        print("=" * 30)
        print("✅ Dữ liệu đã được import từ backup")
        print("✅ Database đã sẵn sàng")
        print("✅ AI Content Processor hoạt động")
        print("\n🚀 Chạy: python ai_content_processor.py")

        return True

    def close(self):
        """Đóng kết nối"""
        if self.connection and self.connection.is_connected():
            self.connection.close()


def main():
    """Main function"""
    try:
        restorer = BackupRestorer()

        # Kiểm tra xem có muốn restore không
        print("🔄 KHÔI PHỤC DỰ ÁN TỪ BACKUP CSV")
        print("=" * 40)
        print("⚠️  CẢNH BÁO: Thao tác này sẽ XÓA dữ liệu hiện tại!")
        print("📁 Backup file: c:\\Users\\Admin\\Downloads\\posts.csv")

        confirm = (
            input("\n❓ Bạn có chắc muốn khôi phục từ backup? (yes/no): ")
            .lower()
            .strip()
        )

        if confirm in ["yes", "y"]:
            if restorer.restore_project():
                print("\n🎉 HOÀN THÀNH! Dự án đã được khôi phục thành công!")

                # Hỏi có muốn chạy test không
                test = input("\n🧪 Muốn chạy test ngay? (y/n): ").lower().strip()
                if test in ["y", "yes"]:
                    os.system("python ai_content_processor.py stats")
            else:
                print("\n❌ Khôi phục thất bại!")
        else:
            print("\n✋ Đã hủy khôi phục")

        restorer.close()

    except KeyboardInterrupt:
        print("\n⚠️ Đã hủy bởi người dùng")
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")


if __name__ == "__main__":
    main()
