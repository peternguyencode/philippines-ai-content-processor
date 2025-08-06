#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MySQL Database Browser - Duyệt dữ liệu MySQL một cách trực quan
"""

import json
import os
from datetime import datetime

import mysql.connector


class DatabaseBrowser:
    def __init__(self):
        self.connection = None
        self.connect()

    def connect(self):
        """Kết nối MySQL"""
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                port=3308,
                user="root",
                password="baivietwp_password",
                database="mydb",
                charset="utf8mb4",
            )
            print("✅ Connected to MySQL database!")
            return True
        except mysql.connector.Error as e:
            print(f"❌ MySQL connection failed: {e}")
            return False

    def show_summary(self):
        """Hiển thị tổng quan database"""
        print("\n📊 DATABASE SUMMARY")
        print("=" * 50)

        cursor = self.connection.cursor()

        # Total posts
        cursor.execute("SELECT COUNT(*) FROM posts")
        total = cursor.fetchone()[0]
        print(f"📄 Total Posts: {total}")

        # By status
        cursor.execute("SELECT status, COUNT(*) FROM posts GROUP BY status")
        status_counts = cursor.fetchall()
        print(f"📈 By Status:")
        for status, count in status_counts:
            print(f"   {status}: {count}")

        # By category (top 5)
        cursor.execute(
            """
            SELECT category, COUNT(*) as count 
            FROM posts 
            GROUP BY category 
            ORDER BY count DESC 
            LIMIT 5
        """
        )
        top_categories = cursor.fetchall()
        print(f"🏷️  Top 5 Categories:")
        for category, count in top_categories:
            print(f"   {category}: {count}")

        cursor.close()

    def list_posts(self, limit=10, status=None):
        """Liệt kê posts"""
        print(f"\n📋 POSTS LIST (showing {limit})")
        print("=" * 60)

        cursor = self.connection.cursor(dictionary=True)

        query = """
            SELECT id, title, status, category, created_date, processing_status
            FROM posts 
        """
        params = []

        if status:
            query += " WHERE status = %s"
            params.append(status)

        query += " ORDER BY created_date DESC LIMIT %s"
        params.append(limit)

        cursor.execute(query, params)
        posts = cursor.fetchall()

        for i, post in enumerate(posts, 1):
            title = (
                post["title"][:50] + "..." if len(post["title"]) > 50 else post["title"]
            )
            print(f"{i:2d}. [{post['id']:2d}] {title}")
            print(f"     Status: {post['status']} | Category: {post['category']}")
            print(
                f"     Created: {post['created_date']} | Processing: {post['processing_status']}"
            )
            print()

        cursor.close()
        return posts

    def search_posts(self, keyword):
        """Tìm kiếm posts"""
        print(f"\n🔍 SEARCH RESULTS for '{keyword}'")
        print("=" * 60)

        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT id, title, status, category, created_date
            FROM posts 
            WHERE title LIKE %s OR content LIKE %s OR keywords LIKE %s
            ORDER BY created_date DESC 
            LIMIT 20
        """,
            (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"),
        )

        posts = cursor.fetchall()

        if not posts:
            print("❌ No posts found!")
            return []

        for i, post in enumerate(posts, 1):
            title = (
                post["title"][:50] + "..." if len(post["title"]) > 50 else post["title"]
            )
            print(f"{i:2d}. [{post['id']:2d}] {title}")
            print(f"     Status: {post['status']} | Category: {post['category']}")
            print()

        cursor.close()
        return posts

    def export_posts(self, filename=None, limit=10):
        """Export posts to JSON"""
        if not filename:
            filename = f"posts_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT * FROM posts 
            ORDER BY created_date DESC 
            LIMIT %s
        """,
            (limit,),
        )

        posts = cursor.fetchall()

        # Convert datetime objects to strings
        for post in posts:
            for key, value in post.items():
                if isinstance(value, datetime):
                    post[key] = value.isoformat()

        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(posts, f, indent=2, ensure_ascii=False)

            print(f"✅ Exported {len(posts)} posts to: {filename}")
            print(f"📁 File size: {os.path.getsize(filename)} bytes")

        except Exception as e:
            print(f"❌ Export failed: {e}")

        cursor.close()

    def run_interactive(self):
        """Chạy interactive mode"""
        print("\n🎮 INTERACTIVE DATABASE BROWSER")
        print("Commands: summary, list [limit], search <keyword>, export [limit], quit")

        while True:
            try:
                cmd = input("\ndb> ").strip().lower()

                if cmd == "quit" or cmd == "exit":
                    break
                elif cmd == "summary":
                    self.show_summary()
                elif cmd.startswith("list"):
                    parts = cmd.split()
                    limit = int(parts[1]) if len(parts) > 1 else 10
                    self.list_posts(limit)
                elif cmd.startswith("search"):
                    keyword = " ".join(cmd.split()[1:])
                    if keyword:
                        self.search_posts(keyword)
                    else:
                        print("❌ Please provide search keyword!")
                elif cmd.startswith("export"):
                    parts = cmd.split()
                    limit = int(parts[1]) if len(parts) > 1 else 10
                    self.export_posts(limit=limit)
                elif cmd == "help":
                    print("Available commands:")
                    print("  summary - Show database overview")
                    print("  list [limit] - List posts (default: 10)")
                    print("  search <keyword> - Search posts")
                    print("  export [limit] - Export posts to JSON")
                    print("  quit - Exit browser")
                else:
                    print("❌ Unknown command. Type 'help' for available commands.")

            except KeyboardInterrupt:
                print("\n👋 Interrupted by user")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

    def close(self):
        """Đóng kết nối"""
        if self.connection:
            self.connection.close()
            print("👋 Database connection closed!")


def main():
    """Main function"""
    browser = DatabaseBrowser()

    if not browser.connection:
        return

    try:
        # Show summary first
        browser.show_summary()

        # Run interactive mode
        browser.run_interactive()

    finally:
        browser.close()


if __name__ == "__main__":
    main()
