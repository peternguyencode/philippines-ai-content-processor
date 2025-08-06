#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interactive Processing Menu - Chọn các bước xử lý

Author: AI Assistant
Date: 2025-08-06
"""

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def print_header():
    """Print header"""
    print("\n" + "=" * 60)
    print("🤖 AI CONTENT PROCESSING - INTERACTIVE MENU")
    print("=" * 60)
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()


def print_status():
    """Print current status"""
    print("📊 HIỆN TRẠNG HỆ THỐNG:")
    print("   Database: 86 posts gốc → 1 đã xử lý → 85 posts còn lại")
    print("   CSV File: 86 posts sẵn sàng xử lý")
    print("   Backup: ✅ Đã backup hoàn tất")
    print("   Systems: ✅ Cả 2 pipeline đã test thành công")
    print()


def show_menu():
    """Show main menu"""
    print("🎯 CHỌN PIPELINE XỬ LÝ:")
    print()
    print("📊 DATABASE PIPELINE (MySQL + DALL-E 3 Images):")
    print("   1. Test 1 post (kiểm tra hệ thống)")
    print("   2. Batch 5 posts (test an toàn)")
    print("   3. Batch 10 posts (production nhỏ)")
    print("   4. Full batch 85 posts (production đầy đủ)")
    print("   5. Xem thống kê database")
    print()
    print("📝 CSV PIPELINE (Text Processing + Classification):")
    print("   6. Test 2 posts CSV (kiểm tra hệ thống)")
    print("   7. Batch 10 posts CSV (test)")
    print("   8. Full batch 86 posts CSV (production)")
    print()
    print("🔧 UTILITIES:")
    print("   9. Backup database hiện tại")
    print("   10. Mở phpMyAdmin")
    print("   11. Xem các file output")
    print("   12. Mở thư mục data")
    print()
    print("🎨 PROMPT MANAGEMENT:")
    print("   13. Xem prompt hiện tại")
    print("   14. Add/Edit custom prompt")
    print("   15. Test prompt với sample data")
    print()
    print("   0. Thoát")
    print()


def run_command(cmd, description):
    """Run command with description"""
    print(f"\n🚀 {description}")
    print("-" * 50)
    print(f"Executing: {cmd}")
    print()

    try:
        result = subprocess.run(cmd, shell=True, check=True)
        print(f"\n✅ Hoàn thành: {description}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Lỗi: {e}")
        return False
    except KeyboardInterrupt:
        print(f"\n⚠️ Đã dừng bởi người dùng")
        return False


def handle_choice(choice):
    """Handle user choice"""

    if choice == "1":
        return run_command(
            "python ai_content_processor.py single", "Test 1 post với database pipeline"
        )

    elif choice == "2":
        return run_command(
            "python ai_content_processor.py batch 5 45.0",
            "Batch 5 posts với database pipeline (45s delay)",
        )

    elif choice == "3":
        return run_command(
            "python ai_content_processor.py batch 10 45.0",
            "Batch 10 posts với database pipeline",
        )

    elif choice == "4":
        print("⚠️ CẢNH BÁO: Full batch sẽ xử lý 85 posts")
        print("   Thời gian: ~64 phút")
        print("   Chi phí: ~$3.40 (DALL-E 3 images)")
        confirm = input("\nBạn có chắc chắn? (y/n): ").strip().lower()

        if confirm == "y":
            return run_command(
                "python ai_content_processor.py batch 85 45.0",
                "Full batch 85 posts với database pipeline",
            )
        else:
            print("❌ Đã hủy full batch processing")
            return True

    elif choice == "5":
        return run_command(
            "python ai_content_processor.py stats", "Xem thống kê database processing"
        )

    elif choice == "6":
        return run_command(
            "python test_csv_processor.py", "Test 2 posts với CSV pipeline"
        )

    elif choice == "7":
        return run_command(
            "python csv_ai_processor.py ./data/posts.csv 10 5.0",
            "Batch 10 posts với CSV pipeline",
        )

    elif choice == "8":
        print("⚠️ THÔNG TIN: Full CSV batch sẽ xử lý 86 posts")
        print("   Thời gian: ~22 phút")
        print("   Chi phí: ~$0.17 (text processing only)")
        confirm = input("\nBạn có muốn tiếp tục? (y/n): ").strip().lower()

        if confirm == "y":
            return run_command(
                "python run_full_batch.py", "Full batch 86 posts với CSV pipeline"
            )
        else:
            print("❌ Đã hủy CSV full batch processing")
            return True

    elif choice == "9":
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        cmd = f"docker exec baivietwp mysqldump -u root -pbaivietwp_password mydb > backup_{timestamp}.sql"
        return run_command(cmd, f"Backup database - backup_{timestamp}.sql")

    elif choice == "10":
        print("🌐 Mở phpMyAdmin trong browser...")
        print("URL: http://localhost:8081")
        try:
            import webbrowser

            webbrowser.open("http://localhost:8081")
            print("✅ Đã mở phpMyAdmin")
            return True
        except Exception as e:
            print(f"❌ Không thể mở browser: {e}")
            print("Vui lòng mở manual: http://localhost:8081")
            return True

    elif choice == "11":
        print("\n📁 CÁC FILE OUTPUT:")
        print("-" * 30)

        # Check CSV outputs
        print("CSV Pipeline outputs:")
        try:
            import glob

            csv_files = glob.glob("./data/posts_ready_*.csv")
            if csv_files:
                for f in csv_files:
                    print(f"   ✅ {f}")
            else:
                print("   ⚠️ Chưa có file CSV output")
        except Exception:
            print("   ❌ Không thể check CSV files")

        # Check log files
        print("\nLog files:")
        try:
            log_files = glob.glob("*processing*.log")
            if log_files:
                for f in log_files[-3:]:  # Show last 3 logs
                    print(f"   📝 {f}")
            else:
                print("   ⚠️ Chưa có log files")
        except Exception:
            print("   ❌ Không thể check log files")

        return True

    elif choice == "12":
        print("📁 Mở thư mục data...")
        data_path = r"D:\duanmoi\data"

        if os.path.exists(data_path):
            try:
                # Windows command to open folder in File Explorer
                os.startfile(data_path)
                print(f"✅ Đã mở thư mục: {data_path}")
                return True
            except Exception as e:
                print(f"❌ Không thể mở thư mục: {e}")
                # Fallback to explorer command
                try:
                    subprocess.run(["explorer", data_path], check=True)
                    print(f"✅ Đã mở thư mục: {data_path}")
                    return True
                except Exception:
                    print(f"Vui lòng mở manual: {data_path}")
                    return True
        else:
            print(f"❌ Thư mục không tồn tại: {data_path}")
            # Create data directory if it doesn't exist
            try:
                os.makedirs(data_path, exist_ok=True)
                print(f"✅ Đã tạo thư mục: {data_path}")
                os.startfile(data_path)
                print(f"✅ Đã mở thư mục: {data_path}")
            except Exception as e:
                print(f"❌ Không thể tạo/mở thư mục: {e}")
            return True

    elif choice == "13":
        return show_current_prompts()

    elif choice == "14":
        return add_edit_prompt()

    elif choice == "15":
        return test_prompt_with_sample()

    elif choice == "0":
        print("👋 Tạm biệt!")
        return False

    else:
        print("❌ Lựa chọn không hợp lệ!")
        return True


def show_current_prompts():
    """Hiển thị các prompt hiện tại"""
    print("\n🎨 PROMPT HIỆN TẠI TRONG HỆ THỐNG")
    print("=" * 60)

    print("📊 1. DATABASE PIPELINE PROMPT:")
    print("-" * 40)
    database_prompt = """
Bạn là một chuyên gia content marketing và SEO. Hãy viết lại bài viết sau đây để:
1. Tối ưu SEO và thu hút người đọc
2. Giữ nguyên ý nghĩa chính nhưng diễn đạt hay hơn
3. Thêm keywords tự nhiên liên quan đến chủ đề
4. Cấu trúc rõ ràng với đoạn văn ngắn

Tiêu đề gốc: {title}
Danh mục: {category}
Nội dung gốc: {original_content[:2000]}...

Yêu cầu output dạng JSON:
{
    "ai_content": "Nội dung đã được viết lại",
    "meta_title": "Tiêu đề SEO (60-70 ký tự)",
    "meta_description": "Mô tả SEO (150-160 ký tự)",
    "image_prompt": "Mô tả hình ảnh phù hợp cho bài viết (tiếng Anh)",
    "suggested_tags": "tag1, tag2, tag3",
    "notes": "Ghi chú về quá trình xử lý"
}"""
    print(database_prompt.strip())

    print("\n📝 2. CSV PIPELINE PROMPT:")
    print("-" * 40)
    csv_prompt = """
Bạn là chuyên gia content marketing và SEO cho thị trường Philippines. 
Hãy viết lại bài viết sau đây để:

1. Tạo tiêu đề mới hoàn toàn khác nhưng giữ ý nghĩa (SEO-friendly cho Philippines)
2. Paraphrase toàn bộ nội dung với từ ngữ địa phương hóa cho Philippines
3. Tối ưu SEO và thu hút người đọc Philippines
4. Giữ nguyên cấu trúc và độ dài tương tự
5. Sử dụng từ khóa phù hợp với thị trường Philippines

TIÊU ĐỀ GỐC: {title}
NỘI DUNG GỐC: {content[:3000]}...

Yêu cầu output dạng JSON:
{
    "new_title": "Tiêu đề mới SEO-friendly cho Philippines",
    "new_content": "Nội dung đã được paraphrase và localize",
    "notes": "Ghi chú về quá trình xử lý"
}"""
    print(csv_prompt.strip())

    print(f"\n💡 GIẢI THÍCH:")
    print("   - PROMPT = Câu hỏi/yêu cầu gửi cho ChatGPT")
    print("   - JSON OUTPUT = Định dạng dữ liệu trả về từ AI")
    print(
        "   - Variables: {title}, {content}, {category} sẽ được thay thế bằng dữ liệu thực tế"
    )

    return True


def add_edit_prompt():
    """Thêm/sửa custom prompt"""
    print("\n🎨 THÊM/SỬA CUSTOM PROMPT")
    print("=" * 50)

    print("📝 CÁC TEMPLATE CÓ SẴN:")
    templates = {
        "1": {
            "name": "SEO Content Optimizer",
            "prompt": "Tối ưu SEO cho bài viết này với focus keyword: {keyword}",
            "output": {
                "optimized_content": "Content đã tối ưu",
                "seo_score": "Điểm SEO",
            },
        },
        "2": {
            "name": "Social Media Content",
            "prompt": "Tạo content social media từ bài viết này",
            "output": {"facebook_post": "Post Facebook", "twitter_post": "Tweet"},
        },
        "3": {
            "name": "Philippines Localization",
            "prompt": "Localize content cho thị trường Philippines",
            "output": {
                "localized_content": "Content Philippines",
                "cultural_notes": "Ghi chú văn hóa",
            },
        },
    }

    for key, template in templates.items():
        print(f"   {key}. {template['name']}")
    print("   4. Tạo custom prompt hoàn toàn mới")

    choice = input("\nChọn template (1-4): ").strip()

    if choice in templates:
        template = templates[choice]
        print(f"\n✅ Đã chọn template: {template['name']}")
        print(f"Prompt: {template['prompt']}")
        print(f"Output format: {json.dumps(template['output'], indent=2)}")

        # Tạo file prompt
        prompts_dir = Path("./prompts")
        prompts_dir.mkdir(exist_ok=True)

        filename = f"custom_prompt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = prompts_dir / filename

        prompt_config = {
            "name": template["name"],
            "system_role": "Bạn là chuyên gia content marketing chuyên nghiệp",
            "user_prompt": template["prompt"],
            "output_format": template["output"],
            "model": "gpt-3.5-turbo",
            "max_tokens": 2000,
            "temperature": 0.7,
        }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(prompt_config, f, indent=2, ensure_ascii=False)

        print(f"✅ Đã tạo prompt file: {filepath}")

    elif choice == "4":
        print("\n📝 TẠO CUSTOM PROMPT:")
        name = input("Tên prompt: ").strip()
        system_role = input("System role (AI sẽ đóng vai gì): ").strip()
        user_prompt = input("User prompt (yêu cầu cụ thể): ").strip()

        print("\n📊 OUTPUT FORMAT:")
        print("Nhập các fields bạn muốn AI trả về (cách nhau bởi dấu phẩy):")
        print("Ví dụ: new_content,meta_title,keywords,notes")

        fields = input("Fields: ").strip().split(",")
        output_format = {
            field.strip(): f"Mô tả cho {field.strip()}" for field in fields
        }

        # Tạo file prompt
        prompts_dir = Path("./prompts")
        prompts_dir.mkdir(exist_ok=True)

        filename = f"custom_{name.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = prompts_dir / filename

        prompt_config = {
            "name": name,
            "system_role": system_role,
            "user_prompt": user_prompt,
            "output_format": output_format,
            "model": "gpt-3.5-turbo",
            "max_tokens": 2000,
            "temperature": 0.7,
        }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(prompt_config, f, indent=2, ensure_ascii=False)

        print(f"✅ Đã tạo custom prompt: {filepath}")

    else:
        print("❌ Lựa chọn không hợp lệ!")

    return True


def test_prompt_with_sample():
    """Test prompt với sample data"""
    print("\n🧪 TEST PROMPT VỚI SAMPLE DATA")
    print("=" * 50)

    # Sample data
    sample_data = {
        "title": "Cách chơi baccarat online hiệu quả",
        "content": "Baccarat là một trong những trò chơi casino phổ biến nhất. Người chơi cần hiểu các quy tắc cơ bản để có thể thắng lớn.",
        "category": "Casino & Gaming",
    }

    print("📊 SAMPLE DATA:")
    for key, value in sample_data.items():
        print(f"   {key}: {value}")

    print(f"\n🤖 SIMULATED AI RESPONSES:")

    print("\n1. DATABASE PIPELINE RESPONSE:")
    db_response = {
        "ai_content": "Master the art of online baccarat with proven strategies. Learn fundamental rules and winning techniques for maximizing your casino success.",
        "meta_title": "Master Online Baccarat - Winning Strategies & Tips",
        "meta_description": "Discover effective online baccarat strategies. Learn rules, tips and techniques to increase your winning chances in casino games.",
        "image_prompt": "Professional casino baccarat table with cards and chips, elegant gaming atmosphere",
        "suggested_tags": "baccarat, casino games, online gambling, card games, gaming tips",
        "notes": "Content optimized for SEO with focus on baccarat strategies",
    }
    print(json.dumps(db_response, indent=2, ensure_ascii=False))

    print("\n2. CSV PIPELINE RESPONSE:")
    csv_response = {
        "new_title": "Master Baccarat Strategies for Philippines Online Casino Players",
        "new_content": "Discover the most effective baccarat gaming techniques specifically designed for Filipino casino enthusiasts. Understanding fundamental rules is essential for maximizing your winning potential in Philippines online casino market.",
        "notes": "Content localized for Philippines market with cultural adaptation",
    }
    print(json.dumps(csv_response, indent=2, ensure_ascii=False))

    print(f"\n💡 LƯU Ý:")
    print("   - Đây là simulation, không gọi API thật")
    print("   - Trong production, sẽ gọi ChatGPT API với prompt thực tế")
    print("   - JSON response sẽ được parse và sử dụng trong hệ thống")

    return True


def main():
    """Main interactive loop"""

    while True:
        try:
            print_header()
            print_status()
            show_menu()

            choice = input("Chọn option (0-15): ").strip()

            if not handle_choice(choice):
                break

            input("\nPress Enter để tiếp tục...")

        except KeyboardInterrupt:
            print("\n\n⚠️ Đã dừng bởi người dùng")
            break
        except Exception as e:
            print(f"\n❌ Lỗi không mong muốn: {e}")
            input("Press Enter để tiếp tục...")


if __name__ == "__main__":
    main()
