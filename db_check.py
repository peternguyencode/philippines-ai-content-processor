#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple Database Check - Kiểm tra nhanh MySQL Database
"""

import sys

import mysql.connector


def quick_check():
    """Kiểm tra nhanh database"""
    print("🔍 QUICK DATABASE CHECK")
    print("=" * 40)

    try:
        # Kết nối MySQL
        connection = mysql.connector.connect(
            host="localhost",
            port=3308,
            user="root",
            password="baivietwp_password",
            database="mydb",
            charset="utf8mb4",
        )

        print("✅ MySQL connected!")

        cursor = connection.cursor()

        # Kiểm tra tables
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"📁 Tables: {[table[0] for table in tables]}")

        # Đếm posts
        cursor.execute("SELECT COUNT(*) FROM posts")
        total_posts = cursor.fetchone()[0]
        print(f"📄 Total posts: {total_posts}")

        if total_posts > 0:
            # 3 posts mới nhất
            cursor.execute(
                """
                SELECT id, title, status, created_date 
                FROM posts 
                ORDER BY created_date DESC 
                LIMIT 3
            """
            )
            posts = cursor.fetchall()

            print(f"\n🕒 Latest 3 posts:")
            for post in posts:
                print(f"   [{post[0]}] {post[1][:50]}... ({post[2]})")

        cursor.close()
        connection.close()
        print("\n✅ Check completed!")

    except mysql.connector.Error as e:
        print(f"❌ MySQL Error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    quick_check()
