#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JSON to MySQL Import Script
Chuyển đổi dữ liệu từ JSON sang MySQL Database
Author: AI Assistant
Date: 2025-08-05
"""

import json
import logging
import os
import sys

from mysql_helper import MySQLHelper

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("import_mysql.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


def main():
    """Hàm main để import JSON vào MySQL"""
    print("🔥 JSON TO MYSQL IMPORT TOOL 🔥")
    print("=" * 50)

    # Kiểm tra file JSON
    json_file = "bonus365casinoall_posts.json"
    if not os.path.exists(json_file):
        print(f"❌ File {json_file} không tồn tại!")
        return

    try:
        # Khởi tạo MySQL Helper
        print("🔌 Connecting to MySQL...")
        mysql_helper = MySQLHelper(
            host="localhost",
            port=3308,
            user="root",
            password="baivietwp_password",
            database="mydb",
        )

        # Kiểm tra kết nối
        if not mysql_helper.check_connection():
            print("❌ MySQL connection failed!")
            return

        print("✅ MySQL connected successfully!")

        # Hiển thị trạng thái hiện tại
        stats = mysql_helper.get_posts_count()
        print(f"📊 Current posts in database: {stats['total']}")
        if stats["by_status"]:
            print("📊 By status:")
            for status, count in stats["by_status"].items():
                print(f"   - {status}: {count}")

        # Xác nhận import
        confirm = input(f"\n🚀 Import data from '{json_file}'? (y/N): ").strip().lower()
        if confirm != "y":
            print("❌ Import cancelled.")
            return

        # Bắt đầu import
        print(f"\n🚀 Starting import from {json_file}...")
        import_stats = mysql_helper.import_from_json(json_file)

        # Hiển thị kết quả
        print(f"\n🎉 IMPORT COMPLETED!")
        print(f"📊 Results:")
        print(f"   Total processed: {import_stats['total']}")
        print(f"   Successfully imported: {import_stats['success']}")
        print(f"   Duplicates skipped: {import_stats['duplicates']}")
        print(f"   Errors: {import_stats['errors']}")

        # Hiển thị trạng thái sau import
        final_stats = mysql_helper.get_posts_count()
        print(f"\n📊 Final database status:")
        print(f"   Total posts: {final_stats['total']}")

        # Tùy chọn export test
        if import_stats["success"] > 0:
            export_test = (
                input("\n📤 Export 5 posts to test file? (y/N): ").strip().lower()
            )
            if export_test == "y":
                mysql_helper.export_to_json("exported_test.json", 5)
                print("✅ Test export completed: exported_test.json")

    except KeyboardInterrupt:
        print("\n⚠️ Import interrupted by user")

    except Exception as e:
        logger.error(f"❌ Critical error: %s", str(e))
        print(f"❌ Critical error: {str(e)}")

    finally:
        if "mysql_helper" in locals():
            mysql_helper.close()
            print("🔌 MySQL connection closed")


if __name__ == "__main__":
    main()
