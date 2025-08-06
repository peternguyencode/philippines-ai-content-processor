#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced Interactive Menu V2 - Strategy-based AI Content Processing
Menu tương tác với 2 Strategies hoàn toàn khác nhau

Author: AI Assistant
Date: 2025-08-06
"""

import json
import os
import subprocess
import sys
from datetime import datetime
from typing import Dict, List, Optional

# Import strategy classes
try:
    from prompt_strategies import PromptStrategyFactory
except ImportError:
    print("❌ Không thể import prompt_strategies.py")
    print("Vui lòng đảm bảo file prompt_strategies.py tồn tại trong cùng thư mục.")
    sys.exit(1)


class StrategyBasedInteractiveMenu:
    """Interactive Menu với Strategy Pattern support"""

    def __init__(self):
        """Khởi tạo Interactive Menu V2"""
        self.current_strategy = "DATABASE_PIPELINE"  # Default strategy
        self.strategies = PromptStrategyFactory.get_available_strategies()
        self.strategy_info = PromptStrategyFactory.get_strategy_info()

        print("🚀 STRATEGY-BASED AI CONTENT PROCESSOR")
        print("=" * 60)
        print("Menu tương tác với 2 Strategies xử lý dữ liệu khác nhau")
        print()

        # Hiển thị strategies available
        self.display_strategies()

    def display_strategies(self):
        """Hiển thị thông tin strategies"""
        print("🎯 AVAILABLE STRATEGIES:")
        for i, strategy in enumerate(self.strategies, 1):
            info = self.strategy_info[strategy]
            current_marker = (
                " ⭐ (CURRENT)" if strategy == self.current_strategy else ""
            )
            print(f"   {i}. {strategy}{current_marker}")
            print(f"      └── {info['description']}")
            print(
                f"          📊 {info['output_fields']} fields | 🎨 Images: {info['supports_images']} | 💰 {info['cost_per_request']}"
            )
        print()

    def show_main_menu(self):
        """Hiển thị menu chính"""
        print(f"\n🎮 MAIN MENU - CURRENT: {self.current_strategy}")
        print("=" * 50)
        print("📊 DATABASE OPERATIONS:")
        print("1. 🔍 Xem database posts")
        print("2. 📈 Xem thống kê processing theo strategy")
        print("3. 🧹 Dọn dẹp bảng posts_ai")
        print()
        print("🤖 AI PROCESSING:")
        print("4. 🚀 Batch processing với strategy hiện tại")
        print("5. 🧪 Test xử lý 1 post")
        print("6. ⚡ Batch processing nhanh (no delay)")
        print("7. 🔄 Chuyển đổi strategy")
        print()
        print("🛠️ STRATEGY MANAGEMENT:")
        print("8. 📋 So sánh 2 strategies")
        print("9. 🎯 Xem chi tiết strategy hiện tại")
        print("10. 📊 Benchmark strategies")
        print()
        print("⚙️ SYSTEM:")
        print("11. 🔧 Cài đặt hệ thống")
        print("12. 📝 Xem logs")
        print("13. ℹ️ Hướng dẫn sử dụng")
        print("0. ❌ Thoát")

    def handle_menu_choice(self, choice: str):
        """Xử lý lựa chọn menu"""
        choice = choice.strip()

        if choice == "0":
            return False
        elif choice == "1":
            self.view_database_posts()
        elif choice == "2":
            self.view_strategy_stats()
        elif choice == "3":
            self.cleanup_posts_ai()
        elif choice == "4":
            self.batch_processing()
        elif choice == "5":
            self.test_single_post()
        elif choice == "6":
            self.batch_processing_fast()
        elif choice == "7":
            self.switch_strategy()
        elif choice == "8":
            self.compare_strategies()
        elif choice == "9":
            self.view_current_strategy_details()
        elif choice == "10":
            self.benchmark_strategies()
        elif choice == "11":
            self.system_settings()
        elif choice == "12":
            self.view_logs()
        elif choice == "13":
            self.show_usage_guide()
        else:
            print("❌ Lựa chọn không hợp lệ!")

        return True

    def view_database_posts(self):
        """Xem database posts"""
        print("\n📊 DATABASE POSTS")
        print("-" * 30)

        try:
            # Chạy script xem database
            result = subprocess.run(
                [
                    sys.executable,
                    "-c",
                    """
import mysql.connector
try:
    conn = mysql.connector.connect(
        host="localhost", port=3308, user="root", 
        password="baivietwp_password", database="mydb"
    )
    cursor = conn.cursor()
    
    # Thống kê posts
    cursor.execute("SELECT COUNT(*) FROM posts")
    total_posts = cursor.fetchone()[0]
    
    # Thống kê posts_ai theo strategy
    cursor.execute('''
        SELECT processing_strategy, processing_status, COUNT(*) 
        FROM posts_ai 
        WHERE processing_strategy IS NOT NULL
        GROUP BY processing_strategy, processing_status
    ''')
    ai_stats = cursor.fetchall()
    
    print(f"📊 Tổng posts: {total_posts}")
    print(f"📈 AI Processing Stats by Strategy:")
    for strategy, status, count in ai_stats:
        print(f"   {strategy} | {status}: {count}")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Lỗi: {e}")
                """,
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )

            if result.returncode == 0:
                print(result.stdout)
            else:
                print(f"❌ Lỗi: {result.stderr}")

        except Exception as e:
            print(f"❌ Lỗi chạy database query: {e}")

    def view_strategy_stats(self):
        """Xem thống kê theo strategy"""
        print(f"\n📈 THỐNG KÊ STRATEGY: {self.current_strategy}")
        print("-" * 40)

        try:
            result = subprocess.run(
                [
                    sys.executable,
                    "ai_content_processor_v2.py",
                    "stats",
                    self.current_strategy,
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )

            if result.returncode == 0:
                print(result.stdout)
            else:
                print(f"❌ Lỗi: {result.stderr}")

        except Exception as e:
            print(f"❌ Lỗi: {e}")

    def cleanup_posts_ai(self):
        """Dọn dẹp bảng posts_ai"""
        print("\n🧹 DỌNP DẸP POSTS_AI")
        print("-" * 30)

        print("Chọn loại cleanup:")
        print("1. Xóa tất cả records")
        print("2. Xóa chỉ records lỗi")
        print("3. Xóa records của strategy cụ thể")
        print("0. Hủy")

        choice = input("Chọn (0-3): ").strip()

        if choice == "0":
            return
        elif choice == "1":
            confirm = input("⚠️ Xác nhận xóa TẤT CẢ records? (yes/no): ")
            if confirm.lower() == "yes":
                self.run_cleanup_sql("DELETE FROM posts_ai")
        elif choice == "2":
            self.run_cleanup_sql(
                "DELETE FROM posts_ai WHERE processing_status = 'error'"
            )
        elif choice == "3":
            print("Strategies available:")
            for i, strategy in enumerate(self.strategies, 1):
                print(f"{i}. {strategy}")

            try:
                strategy_choice = int(
                    input(f"Chọn strategy (1-{len(self.strategies)}): ")
                )
                if 1 <= strategy_choice <= len(self.strategies):
                    target_strategy = self.strategies[strategy_choice - 1]
                    self.run_cleanup_sql(
                        f"DELETE FROM posts_ai WHERE processing_strategy = '{target_strategy}'"
                    )
                else:
                    print("❌ Lựa chọn không hợp lệ!")
            except ValueError:
                print("❌ Vui lòng nhập số!")
        else:
            print("❌ Lựa chọn không hợp lệ!")

    def run_cleanup_sql(self, sql: str):
        """Chạy SQL cleanup"""
        try:
            result = subprocess.run(
                [
                    sys.executable,
                    "-c",
                    f"""
import mysql.connector
try:
    conn = mysql.connector.connect(
        host="localhost", port=3308, user="root", 
        password="baivietwp_password", database="mydb", autocommit=True
    )
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM posts_ai")
    before_count = cursor.fetchone()[0]
    
    cursor.execute('{sql}')
    
    cursor.execute("SELECT COUNT(*) FROM posts_ai") 
    after_count = cursor.fetchone()[0]
    
    deleted = before_count - after_count
    print(f"✅ Đã xóa {{deleted}} records")
    print(f"📊 Trước: {{before_count}} | Sau: {{after_count}}")
    
    cursor.close()
    conn.close()
except Exception as e:
    print(f"❌ Lỗi: {{e}}")
                """,
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )

            if result.returncode == 0:
                print(result.stdout)
            else:
                print(f"❌ Lỗi: {result.stderr}")

        except Exception as e:
            print(f"❌ Lỗi: {e}")

    def batch_processing(self):
        """Batch processing với strategy hiện tại"""
        print(f"\n🚀 BATCH PROCESSING VỚI {self.current_strategy}")
        print("-" * 50)

        # Hiển thị strategy info
        info = self.strategy_info[self.current_strategy]
        print(f"🎯 Strategy: {info['name']}")
        print(f"📊 Description: {info['description']}")
        print(f"💰 Cost per Request: {info['cost_per_request']}")
        print()

        try:
            limit = input("Số posts tối đa (Enter = all): ").strip()
            limit = int(limit) if limit.isdigit() else None

            delay = input("Delay giữa requests (giây) [1.0]: ").strip()
            delay = float(delay) if delay else 1.0

            # Chạy AI Content Processor V2
            cmd = [
                sys.executable,
                "ai_content_processor_v2.py",
                "batch",
                self.current_strategy,
            ]
            if limit:
                cmd.append(str(limit))
            cmd.append(str(delay))

            print(f"\n🔄 Bắt đầu processing với {self.current_strategy}...")
            subprocess.run(cmd)

        except ValueError:
            print("❌ Giá trị không hợp lệ!")
        except KeyboardInterrupt:
            print("\n⚠️ Đã dừng bởi người dùng")
        except Exception as e:
            print(f"❌ Lỗi: {e}")

    def test_single_post(self):
        """Test xử lý 1 post"""
        print(f"\n🧪 TEST XỬ LÝ 1 POST VỚI {self.current_strategy}")
        print("-" * 40)

        try:
            subprocess.run(
                [
                    sys.executable,
                    "ai_content_processor_v2.py",
                    "single",
                    self.current_strategy,
                ]
            )
        except Exception as e:
            print(f"❌ Lỗi: {e}")

    def batch_processing_fast(self):
        """Batch processing nhanh (no delay)"""
        print(f"\n⚡ BATCH PROCESSING NHANH - {self.current_strategy}")
        print("-" * 50)

        try:
            limit = input("Số posts tối đa: ").strip()
            limit = int(limit) if limit.isdigit() else 5

            print(f"🚀 Xử lý {limit} posts với delay = 0...")
            subprocess.run(
                [
                    sys.executable,
                    "ai_content_processor_v2.py",
                    "batch",
                    self.current_strategy,
                    str(limit),
                    "0",
                ]
            )

        except ValueError:
            print("❌ Giá trị không hợp lệ!")
        except Exception as e:
            print(f"❌ Lỗi: {e}")

    def switch_strategy(self):
        """Chuyển đổi strategy"""
        print("\n🔄 CHUYỂN ĐỔI STRATEGY")
        print("-" * 30)

        print("Strategies available:")
        for i, strategy in enumerate(self.strategies, 1):
            current_marker = (
                " ⭐ (CURRENT)" if strategy == self.current_strategy else ""
            )
            print(f"{i}. {strategy}{current_marker}")

        try:
            choice = int(input(f"Chọn strategy (1-{len(self.strategies)}): "))
            if 1 <= choice <= len(self.strategies):
                old_strategy = self.current_strategy
                self.current_strategy = self.strategies[choice - 1]
                print(f"✅ Đã chuyển từ {old_strategy} → {self.current_strategy}")
                self.display_strategies()
            else:
                print("❌ Lựa chọn không hợp lệ!")
        except ValueError:
            print("❌ Vui lòng nhập số!")

    def compare_strategies(self):
        """So sánh 2 strategies"""
        print("\n📋 SO SÁNH 2 STRATEGIES")
        print("=" * 40)

        for strategy in self.strategies:
            info = self.strategy_info[strategy]
            current_marker = " ⭐" if strategy == self.current_strategy else ""

            print(f"\n🎯 {strategy}{current_marker}")
            print(f"   📊 Tên: {info['name']}")
            print(f"   📝 Mô tả: {info['description']}")
            print(f"   📋 Output Fields: {info['output_fields']}")
            print(f"   🎨 Hỗ trợ Images: {info['supports_images']}")
            print(f"   🎯 Target: {info['target']}")
            print(f"   💰 Chi phí: {info['cost_per_request']}")

        print(f"\n🔍 STRATEGY COMPARISON:")
        print(f"   DATABASE_PIPELINE: Premium content với SEO + Images (chậm, đắt hơn)")
        print(
            f"   CSV_PIPELINE: Fast processing cho Philippines market (nhanh, rẻ hơn)"
        )
        print(f"   → Chọn strategy phù hợp với mục đích sử dụng!")

    def view_current_strategy_details(self):
        """Xem chi tiết strategy hiện tại"""
        print(f"\n🎯 CHI TIẾT STRATEGY: {self.current_strategy}")
        print("-" * 50)

        info = self.strategy_info[self.current_strategy]

        print("📊 THÔNG TIN STRATEGY:")
        for key, value in info.items():
            print(f"   {key}: {value}")

        print(f"\n🔧 KỸ THUẬT DETAILS:")
        try:
            strategy_instance = PromptStrategyFactory.create_strategy(
                self.current_strategy
            )
            print(
                f"   System Message: {strategy_instance.get_system_message()[:100]}..."
            )
            print(f"   Max Tokens: {strategy_instance.get_max_tokens()}")
            print(f"   Temperature: {strategy_instance.get_temperature()}")
            print(f"   Database Fields: {len(strategy_instance.get_database_fields())}")

        except Exception as e:
            print(f"❌ Lỗi lấy technical details: {e}")

    def benchmark_strategies(self):
        """Benchmark 2 strategies"""
        print("\n📊 BENCHMARK STRATEGIES")
        print("-" * 40)

        print("🚧 Tính năng này sẽ:")
        print("   1. Chạy test với sample content")
        print("   2. So sánh thời gian xử lý")
        print("   3. So sánh chất lượng output")
        print("   4. So sánh chi phí")

        confirm = input("\n⚠️ Chạy benchmark? (sẽ tốn API calls) (y/n): ").lower()
        if confirm == "y":
            print("🚧 Tính năng đang phát triển...")
            # TODO: Implement benchmark logic
        else:
            print("ℹ️ Hủy benchmark")

    def system_settings(self):
        """Cài đặt hệ thống"""
        print("\n🔧 CÀI ĐẶT HỆ THỐNG")
        print("-" * 30)

        print("1. Kiểm tra kết nối database")
        print("2. Kiểm tra OpenAI API")
        print("3. Xem config hiện tại")
        print("4. Test import modules")
        print("0. Quay lại")

        choice = input("Chọn (0-4): ").strip()

        if choice == "1":
            self.test_database_connection()
        elif choice == "2":
            self.test_openai_api()
        elif choice == "3":
            self.view_current_config()
        elif choice == "4":
            self.test_import_modules()

    def test_database_connection(self):
        """Test kết nối database"""
        print("\n🔍 TESTING DATABASE CONNECTION...")

        try:
            result = subprocess.run(
                [
                    sys.executable,
                    "-c",
                    """
import mysql.connector
try:
    conn = mysql.connector.connect(
        host="localhost", port=3308, user="root", 
        password="baivietwp_password", database="mydb"
    )
    if conn.is_connected():
        print("✅ Database connection OK")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM posts")
        posts_count = cursor.fetchone()[0]
        print(f"📊 Posts count: {posts_count}")
        cursor.close()
        conn.close()
    else:
        print("❌ Database connection failed")
except Exception as e:
    print(f"❌ Error: {e}")
                """,
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )

            print(result.stdout if result.returncode == 0 else f"❌ {result.stderr}")

        except Exception as e:
            print(f"❌ Lỗi: {e}")

    def test_openai_api(self):
        """Test OpenAI API"""
        print("\n🔍 TESTING OPENAI API...")

        try:
            result = subprocess.run(
                [
                    sys.executable,
                    "-c",
                    """
from config import Config
from openai import OpenAI
try:
    client = OpenAI(api_key=Config.OPENAI_API_KEY)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello"}],
        max_tokens=5
    )
    print("✅ OpenAI API connection OK")
    print(f"📝 Response: {response.choices[0].message.content}")
except Exception as e:
    print(f"❌ OpenAI API Error: {e}")
                """,
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )

            print(result.stdout if result.returncode == 0 else f"❌ {result.stderr}")

        except Exception as e:
            print(f"❌ Lỗi: {e}")

    def view_current_config(self):
        """Xem config hiện tại"""
        print("\n📋 CURRENT CONFIG")
        print("-" * 20)

        try:
            from config import Config

            print(f"AI_MODEL: {getattr(Config, 'AI_MODEL', 'Not set')}")
            print(
                f"OPENAI_API_KEY: {'Set' if getattr(Config, 'OPENAI_API_KEY', None) else 'Not set'}"
            )
            print(f"Current Strategy: {self.current_strategy}")
        except Exception as e:
            print(f"❌ Lỗi load config: {e}")

    def test_import_modules(self):
        """Test import các modules"""
        print("\n🔍 TESTING MODULE IMPORTS...")

        modules = [
            "mysql.connector",
            "openai",
            "tqdm",
            "config",
            "prompt_strategies",
            "ai_content_processor_v2",
        ]

        for module in modules:
            try:
                __import__(module)
                print(f"✅ {module}")
            except ImportError as e:
                print(f"❌ {module}: {e}")

    def view_logs(self):
        """Xem logs"""
        print("\n📝 LOGS")
        print("-" * 20)

        # List log files
        log_files = [
            f
            for f in os.listdir(".")
            if f.startswith("ai_processing") and f.endswith(".log")
        ]

        if not log_files:
            print("ℹ️ Không tìm thấy log files")
            return

        print("📁 Log files available:")
        for i, log_file in enumerate(log_files, 1):
            print(f"{i}. {log_file}")

        try:
            choice = int(input(f"Chọn log file (1-{len(log_files)}): "))
            if 1 <= choice <= len(log_files):
                log_file = log_files[choice - 1]

                print(f"\n📄 TAIL của {log_file} (50 dòng cuối):")
                print("-" * 40)

                try:
                    with open(log_file, "r", encoding="utf-8") as f:
                        lines = f.readlines()
                        for line in lines[-50:]:
                            print(line.rstrip())
                except Exception as e:
                    print(f"❌ Lỗi đọc file: {e}")
            else:
                print("❌ Lựa chọn không hợp lệ!")
        except ValueError:
            print("❌ Vui lòng nhập số!")

    def show_usage_guide(self):
        """Hướng dẫn sử dụng"""
        print("\n📚 HƯỚNG DẪN SỬ DỤNG")
        print("=" * 40)

        print("🎯 2 STRATEGIES CHÍNH:")
        print()
        print("1️⃣ DATABASE_PIPELINE:")
        print("   • Mục đích: Premium content cho website/blog")
        print(
            "   • Output: 6 fields (ai_content, meta_title, meta_description, image_prompt, tags, notes)"
        )
        print("   • Đặc điểm: SEO optimization + Image generation")
        print("   • Chi phí: ~$0.04/post (cao hơn)")
        print("   • Tốc độ: Chậm hơn (quality over speed)")
        print()
        print("2️⃣ CSV_PIPELINE:")
        print("   • Mục đích: Fast processing cho Philippines market")
        print(
            "   • Output: 3 fields (paraphrased_content, classification, localization_notes)"
        )
        print("   • Đặc điểm: Cultural localization + Fast processing")
        print("   • Chi phí: ~$0.002/post (rẻ hơn)")
        print("   • Tốc độ: Nhanh hơn (speed over features)")
        print()
        print("🔄 WORKFLOW KHUYẾN NGHỊ:")
        print("   1. Chọn strategy phù hợp với mục đích")
        print("   2. Test với 1 post trước (option 5)")
        print("   3. Chạy batch processing (option 4)")
        print("   4. Kiểm tra kết quả (option 2)")
        print("   5. Chuyển strategy nếu cần (option 7)")
        print()
        print("💡 TIPS:")
        print("   • DATABASE_PIPELINE: Dùng cho content chất lượng cao")
        print("   • CSV_PIPELINE: Dùng cho volume processing lớn")
        print("   • Có thể chạy cả 2 strategies trên cùng data")
        print("   • Mỗi strategy có database column riêng")

    def run(self):
        """Chạy interactive menu"""
        try:
            while True:
                self.show_main_menu()
                choice = input(f"\nChọn chức năng (0-13): ").strip()

                if not self.handle_menu_choice(choice):
                    break

                input("\n📎 Nhấn Enter để tiếp tục...")

        except KeyboardInterrupt:
            print("\n👋 Tạm biệt!")
        except Exception as e:
            print(f"❌ Lỗi nghiêm trọng: {e}")


def main():
    """Main function"""
    menu = StrategyBasedInteractiveMenu()
    menu.run()


if __name__ == "__main__":
    main()
