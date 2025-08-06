#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Database Viewer - Xem dữ liệu MySQL Database
Author: AI Assistant
Date: 2025-08-05
"""

import json
from datetime import datetime

from mysql_helper import MySQLHelper


def view_database():
    """Xem tổng quan database"""
    print("🔍 DATABASE VIEWER")
    print("=" * 50)

    try:
        # Kết nối MySQL
        mysql = MySQLHelper()

        if not mysql.check_connection():
            print("❌ Không thể kết nối MySQL!")
            return

        print("✅ MySQL connected successfully!")

        # Lấy thống kê tổng quan
        stats = mysql.get_posts_count()
        print(f"\n📊 DATABASE OVERVIEW:")
        print(f"   Total posts: {stats['total']}")

        if stats.get("by_status"):
            print("   By status:")
            for status, count in stats["by_status"].items():
                print(f"     - {status}: {count}")

        if stats["total"] > 0:
            # Hiển thị 5 posts gần nhất
            print(f"\n📄 LATEST 5 POSTS:")
            cursor = mysql.connection.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT id, title, status, created_date, category 
                FROM posts 
                ORDER BY created_date DESC 
                LIMIT 5
            """
            )
            posts = cursor.fetchall()
            cursor.close()

            for i, post in enumerate(posts, 1):
                print(f"   {i}. [{post['id']}] {post['title'][:60]}...")
                print(
                    f"      Status: {post['status']} | Category: {post['category']} | Created: {post['created_date']}"
                )
                print()

        # Menu actions
        while True:
            print("\n🎮 ACTIONS:")
            print("1. Xem chi tiết 1 post")
            print("2. Export 10 posts mới nhất")
            print("3. Search posts by keyword")
            print("4. Xem tất cả categories")
            print("0. Thoát")

            choice = input("\nChọn action (0-4): ").strip()

            if choice == "0":
                break
            elif choice == "1":
                view_post_detail(mysql)
            elif choice == "2":
                export_recent_posts(mysql)
            elif choice == "3":
                search_posts(mysql)
            elif choice == "4":
                view_categories(mysql)
            else:
                print("❌ Lựa chọn không hợp lệ!")

        mysql.close()
        print("👋 Database viewer closed!")

    except Exception as e:
        print(f"❌ Error: {str(e)}")


def view_post_detail(mysql):
    """Xem chi tiết 1 post"""
    try:
        post_id = input("Nhập ID post cần xem: ").strip()
        if not post_id.isdigit():
            print("❌ ID phải là số!")
            return

        cursor = mysql.connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM posts WHERE id = %s", (post_id,))
        post = cursor.fetchone()
        cursor.close()

        if not post:
            print(f"❌ Không tìm thấy post với ID {post_id}")
            return

        print(f"\n📄 POST DETAIL - ID: {post['id']}")
        print("=" * 60)
        print(f"Title: {post['title']}")
        print(f"Status: {post['status']}")
        print(f"Category: {post['category']}")
        print(f"Created: {post['created_date']}")
        print(f"Source: {post['source_title']}")
        print(f"Original URL: {post['original_url']}")
        print(f"Image URL: {post['image_url']}")
        print(f"Keywords: {post['keywords']}")
        print(f"Tags: {post['tags']}")
        print(f"Processing Status: {post['processing_status']}")
        print(f"AI Model: {post['ai_model']}")
        print(f"Notes: {post['notes']}")
        print(f"\nContent Preview:")
        print(
            post["content"][:500] + "..."
            if len(post["content"]) > 500
            else post["content"]
        )

    except Exception as e:
        print(f"❌ Error viewing post: {str(e)}")


def export_recent_posts(mysql):
    """Export 10 posts mới nhất"""
    try:
        filename = f"recent_posts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        success = mysql.export_to_json(filename, 10)

        if success:
            print(f"✅ Exported 10 recent posts to: {filename}")
        else:
            print("❌ Export failed!")

    except Exception as e:
        print(f"❌ Export error: {str(e)}")


def search_posts(mysql):
    """Tìm kiếm posts theo keyword"""
    try:
        keyword = input("Nhập keyword để search: ").strip()
        if not keyword:
            print("❌ Keyword không được rỗng!")
            return

        cursor = mysql.connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT id, title, status, created_date 
            FROM posts 
            WHERE title LIKE %s OR content LIKE %s OR keywords LIKE %s
            ORDER BY created_date DESC 
            LIMIT 10
        """,
            (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"),
        )
        posts = cursor.fetchall()
        cursor.close()

        if not posts:
            print(f"❌ Không tìm thấy posts chứa keyword '{keyword}'")
            return

        print(f"\n🔍 SEARCH RESULTS for '{keyword}' ({len(posts)} found):")
        print("=" * 60)
        for i, post in enumerate(posts, 1):
            print(f"{i}. [{post['id']}] {post['title'][:50]}...")
            print(f"   Status: {post['status']} | Created: {post['created_date']}")
            print()

    except Exception as e:
        print(f"❌ Search error: {str(e)}")


def view_categories(mysql):
    """Xem tất cả categories"""
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            """
            SELECT category, COUNT(*) as count 
            FROM posts 
            GROUP BY category 
            ORDER BY count DESC
        """
        )
        categories = cursor.fetchall()
        cursor.close()

        print(f"\n📂 CATEGORIES ({len(categories)} total):")
        print("=" * 40)
        for category, count in categories:
            print(f"   {category}: {count} posts")

    except Exception as e:
        print(f"❌ Error viewing categories: {str(e)}")


if __name__ == "__main__":
    view_database()
