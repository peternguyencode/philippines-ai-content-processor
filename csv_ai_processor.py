#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CSV AI Content Processor - Xử lý file CSV posts với AI
Đọc posts.csv → AI paraphrase → Phân loại → posts_ready.csv

Author: AI Assistant
Date: 2025-08-06
"""

import csv
import json
import logging
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import openai
import pandas as pd
from openai import OpenAI
from tqdm import tqdm

# Import config để lấy API key
from config import Config


class CSVAIProcessor:
    """Lớp xử lý file CSV với AI"""

    def __init__(self):
        """Khởi tạo CSV AI Processor"""
        print("🤖 Khởi tạo CSV AI Processor...")

        # Setup logging
        self.setup_logging()

        # Setup OpenAI
        self.setup_openai()

        # Tạo thư mục data nếu chưa có
        self.data_dir = Path("./data")
        self.data_dir.mkdir(exist_ok=True)

        # Statistics
        self.stats = {"total_processed": 0, "success": 0, "errors": 0, "skipped": 0}

        print("✅ CSV AI Processor khởi tạo thành công!")

    def setup_logging(self):
        """Thiết lập logging"""
        log_filename = f"csv_processing_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler(log_filename, encoding="utf-8"),
                logging.StreamHandler(sys.stdout),
            ],
        )

        self.logger = logging.getLogger(__name__)
        self.logger.info("🔍 Logging được thiết lập")

    def setup_openai(self):
        """Thiết lập OpenAI API"""
        try:
            self.client = OpenAI(api_key=Config.OPENAI_API_KEY)

            if not Config.OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY không được thiết lập trong config")

            self.logger.info("✅ OpenAI API đã được thiết lập")

        except Exception as e:
            self.logger.error(f"❌ Lỗi thiết lập OpenAI: {e}")
            sys.exit(1)

    def read_csv_file(self, csv_file_path: str) -> List[Dict[str, Any]]:
        """
        Bước 1: Đọc file posts.csv

        Args:
            csv_file_path: Đường dẫn file CSV

        Returns:
            List các posts từ CSV
        """
        try:
            self.logger.info(f"📖 Đọc file CSV: {csv_file_path}")

            # Đọc CSV với pandas
            df = pd.read_csv(csv_file_path, encoding="utf-8")

            # Kiểm tra các cột cần thiết
            required_columns = ["id", "title", "content"]
            missing_columns = [col for col in required_columns if col not in df.columns]

            if missing_columns:
                raise ValueError(f"Thiếu các cột: {missing_columns}")

            # Chuyển đổi DataFrame thành list dict
            posts = df.to_dict("records")

            self.logger.info(f"✅ Đọc thành công {len(posts)} posts từ CSV")
            return list(posts)  # Explicit conversion

        except Exception as e:
            self.logger.error(f"❌ Lỗi đọc file CSV: {e}")
            return []

    def paraphrase_content_with_ai(self, title: str, content: str) -> Dict[str, Any]:
        """
        Bước 2: Paraphrase content với OpenAI

        Args:
            title: Tiêu đề gốc
            content: Nội dung gốc

        Returns:
            Dict chứa title và content mới
        """
        try:
            # Prompt cho AI paraphrase
            prompt = f"""
            Bạn là chuyên gia content marketing và SEO cho thị trường Philippines. 
            Hãy viết lại bài viết sau đây để:
            
            1. Tạo tiêu đề mới hoàn toàn khác nhưng giữ ý nghĩa (SEO-friendly cho Philippines)
            2. Paraphrase toàn bộ nội dung với từ ngữ địa phương hóa cho Philippines
            3. Tối ưu SEO và thu hút người đọc Philippines
            4. Giữ nguyên cấu trúc và độ dài tương tự
            5. Sử dụng từ khóa phù hợp với thị trường Philippines
            
            TIÊU ĐỀ GỐC: {title}
            
            NỘI DUNG GỐC:
            {content[:3000]}...
            
            Yêu cầu output dạng JSON:
            {{
                "new_title": "Tiêu đề mới SEO-friendly cho Philippines",
                "new_content": "Nội dung đã được paraphrase và localize",
                "notes": "Ghi chú về quá trình xử lý"
            }}
            """

            response = self.client.chat.completions.create(
                model=Config.AI_MODEL or "gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "Bạn là chuyên gia content marketing và SEO cho thị trường Philippines.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=4000,
                temperature=0.7,
            )

            ai_response = response.choices[0].message.content
            if ai_response:
                ai_response = ai_response.strip()
            else:
                ai_response = "{}"

            # Parse JSON response
            try:
                result = json.loads(ai_response)
            except json.JSONDecodeError:
                # Fallback nếu AI không trả về JSON
                result = {
                    "new_title": title,
                    "new_content": content,
                    "notes": "AI response không đúng JSON format",
                }

            self.logger.info(f"✅ Paraphrase thành công: {title[:50]}...")
            return result

        except Exception as e:
            self.logger.error(f"❌ Lỗi paraphrase với AI: {e}")
            # Fallback
            return {
                "new_title": title,
                "new_content": content,
                "notes": f"AI paraphrase failed: {str(e)}",
            }

    def classify_content_with_ai(self, title: str, content: str) -> Dict[str, str]:
        """
        Bước 3: Phân loại category và keywords với AI

        Args:
            title: Tiêu đề bài viết
            content: Nội dung bài viết

        Returns:
            Dict chứa category và keywords
        """
        try:
            # Prompt cho AI phân loại
            prompt = f"""
            Bạn là chuyên gia phân loại nội dung và SEO cho thị trường Philippines.
            Hãy phân tích bài viết sau và đưa ra:
            
            1. Category phù hợp (chọn 1 trong các category sau):
               - Casino & Gaming
               - Online Betting 
               - Sports Betting
               - Slot Games
               - Live Casino
               - Promotions & Bonuses
               - Payment Methods
               - Gaming Tips
               - News & Updates
               - Mobile Gaming
            
            2. Keywords SEO (5-8 từ khóa chính, phù hợp với Philippines market)
            
            TIÊU ĐỀ: {title}
            
            NỘI DUNG: {content[:2000]}...
            
            Yêu cầu output dạng JSON:
            {{
                "category": "Category phù hợp nhất",
                "keywords": "keyword1, keyword2, keyword3, keyword4, keyword5",
                "notes": "Lý do phân loại"
            }}
            """

            response = self.client.chat.completions.create(
                model=Config.AI_MODEL or "gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "Bạn là chuyên gia phân loại nội dung và SEO cho thị trường Philippines.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=1000,
                temperature=0.3,  # Lower temperature cho consistent classification
            )

            ai_response = response.choices[0].message.content
            if ai_response:
                ai_response = ai_response.strip()
            else:
                ai_response = "{}"

            # Parse JSON response
            try:
                result = json.loads(ai_response)
            except json.JSONDecodeError:
                # Fallback classification
                result = {
                    "category": "Casino & Gaming",
                    "keywords": "casino, gaming, philippines, online, bonus",
                    "notes": "AI classification failed - used fallback",
                }

            self.logger.info(f"✅ Phân loại thành công: {result['category']}")
            return result

        except Exception as e:
            self.logger.error(f"❌ Lỗi phân loại với AI: {e}")
            # Fallback
            return {
                "category": "Casino & Gaming",
                "keywords": "casino, gaming, philippines, online, bonus",
                "notes": f"AI classification failed: {str(e)}",
            }

    def process_single_post(self, post: Dict[str, Any]) -> Dict[str, Any]:
        """
        Xử lý một post hoàn chỉnh

        Args:
            post: Dict chứa thông tin post từ CSV

        Returns:
            Dict chứa post đã xử lý
        """
        post_id = post.get("id", "unknown")
        original_title = post.get("title", "")
        original_content = post.get("content", "")

        result = {
            "id": post_id,
            "original_title": original_title,
            "title": original_title,
            "content": original_content,
            "category": "Casino & Gaming",
            "keywords": "casino, gaming, philippines",
            "success": False,
            "error": None,
        }

        try:
            self.logger.info(f"🔄 Xử lý Post ID {post_id}: {original_title[:50]}...")

            # Bước 2: Paraphrase với AI
            paraphrase_result = self.paraphrase_content_with_ai(
                original_title, original_content
            )

            new_title = paraphrase_result.get("new_title", original_title)
            new_content = paraphrase_result.get("new_content", original_content)

            # Bước 3: Phân loại với AI
            classification = self.classify_content_with_ai(new_title, new_content)

            # Cập nhật kết quả
            result.update(
                {
                    "title": new_title,
                    "content": new_content,
                    "category": classification.get("category", "Casino & Gaming"),
                    "keywords": classification.get(
                        "keywords", "casino, gaming, philippines"
                    ),
                    "success": True,
                }
            )

            self.stats["success"] += 1
            self.logger.info(f"🎉 Hoàn thành Post ID {post_id}")

        except Exception as e:
            error_msg = str(e)
            self.logger.error(f"❌ Lỗi xử lý Post ID {post_id}: {error_msg}")

            result["error"] = error_msg
            self.stats["errors"] += 1

        self.stats["total_processed"] += 1
        return result

    def write_csv_file(
        self, processed_posts: List[Dict[str, Any]], output_file: str
    ) -> bool:
        """
        Bước 4: Ghi file posts_ready.csv

        Args:
            processed_posts: List các posts đã xử lý
            output_file: Đường dẫn file output

        Returns:
            bool: True nếu thành công
        """
        try:
            self.logger.info(f"📝 Ghi file CSV: {output_file}")

            # Chuẩn bị data cho CSV
            csv_data = []
            for post in processed_posts:
                if post["success"]:
                    csv_data.append(
                        {
                            "id": post["id"],
                            "title": post["title"],
                            "content": post["content"],
                            "category": post["category"],
                            "keywords": post["keywords"],
                        }
                    )

            # Ghi file CSV với pandas
            df = pd.DataFrame(csv_data)
            df.to_csv(output_file, index=False, encoding="utf-8")

            self.logger.info(
                f"✅ Ghi thành công {len(csv_data)} posts vào {output_file}"
            )
            return True

        except Exception as e:
            self.logger.error(f"❌ Lỗi ghi file CSV: {e}")
            return False

    def process_csv_pipeline(
        self,
        input_csv: str,
        output_csv: Optional[str] = None,
        limit: Optional[int] = None,
        delay: float = 2.0,
    ) -> Dict[str, Any]:
        """
        Pipeline chính xử lý CSV

        Args:
            input_csv: Đường dẫn file CSV input
            output_csv: Đường dẫn file CSV output (optional)
            limit: Giới hạn số posts xử lý (optional)
            delay: Delay giữa các requests AI (giây)

        Returns:
            Dict chứa thống kê kết quả
        """
        print(f"\n🚀 BẮT ĐẦU CSV AI PROCESSING PIPELINE")
        print("=" * 60)

        # Reset stats
        self.stats = {"total_processed": 0, "success": 0, "errors": 0, "skipped": 0}

        # Tạo output filename nếu chưa có
        if not output_csv:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_csv = str(self.data_dir / f"posts_ready_{timestamp}.csv")

        # Bước 1: Đọc file CSV
        posts = self.read_csv_file(input_csv)

        if not posts:
            print("❌ Không thể đọc file CSV hoặc file trống!")
            return self.stats

        # Giới hạn số posts nếu có
        if limit and limit < len(posts):
            posts = posts[:limit]
            print(f"⚠️ Giới hạn xử lý {limit} posts đầu tiên")

        print(f"📊 Sẽ xử lý {len(posts)} posts")
        print(f"⏱️ Delay giữa requests: {delay} giây")
        print(f"💾 Output file: {output_csv}")

        # Bắt đầu xử lý
        start_time = time.time()
        processed_posts = []

        with tqdm(total=len(posts), desc="Processing Posts") as pbar:
            for post in posts:
                try:
                    # Xử lý post
                    result = self.process_single_post(post)
                    processed_posts.append(result)

                    # Cập nhật progress bar
                    status = "✅" if result["success"] else "❌"
                    pbar.set_postfix_str(f"{status} Post {result['id']}")
                    pbar.update(1)

                    # Delay giữa requests
                    if delay > 0:
                        time.sleep(delay)

                except KeyboardInterrupt:
                    print("\n⚠️ Bị dừng bởi người dùng")
                    break
                except Exception as e:
                    self.logger.error(f"❌ Exception trong pipeline: {e}")
                    self.stats["errors"] += 1
                    pbar.update(1)

        # Bước 4: Ghi file output
        if processed_posts:
            self.write_csv_file(processed_posts, output_csv)

        # Tính thời gian và in kết quả
        end_time = time.time()
        duration = end_time - start_time

        print(f"\n📈 KẾT QUẢ CSV PROCESSING:")
        print(f"   Tổng số posts xử lý: {self.stats['total_processed']}")
        print(f"   Thành công: {self.stats['success']}")
        print(f"   Lỗi: {self.stats['errors']}")
        print(f"   Thời gian: {duration:.2f} giây")
        if self.stats["total_processed"] > 0:
            print(f"   Tốc độ: {duration/self.stats['total_processed']:.2f} giây/post")
        print(f"   Output file: {output_csv}")

        return self.stats


def main():
    """Hàm main"""
    print("🤖 CSV AI CONTENT PROCESSOR")
    print("=" * 50)
    print("Pipeline: CSV → AI Paraphrase → Classify → CSV")
    print()

    try:
        # Khởi tạo processor
        processor = CSVAIProcessor()

        # Kiểm tra tham số dòng lệnh
        if len(sys.argv) > 1:
            input_csv = sys.argv[1]
            limit = int(sys.argv[2]) if len(sys.argv) > 2 else None
            delay = float(sys.argv[3]) if len(sys.argv) > 3 else 2.0

            # Chạy pipeline
            stats = processor.process_csv_pipeline(input_csv, limit=limit, delay=delay)

        else:
            # Chế độ tương tác
            print("🎮 CSV AI PROCESSING:")
            print("Nhập đường dẫn file CSV input:")

            while True:
                try:
                    input_csv = input("File CSV path: ").strip().strip('"')

                    if not input_csv:
                        break

                    if not Path(input_csv).exists():
                        print(f"❌ File không tồn tại: {input_csv}")
                        continue

                    # Hỏi thêm options
                    limit_input = input("Giới hạn số posts (Enter = tất cả): ").strip()
                    limit = int(limit_input) if limit_input else None

                    delay_input = input("Delay giữa requests (giây) [2.0]: ").strip()
                    delay = float(delay_input) if delay_input else 2.0

                    # Chạy pipeline
                    stats = processor.process_csv_pipeline(
                        input_csv, limit=limit, delay=delay
                    )
                    break

                except KeyboardInterrupt:
                    print("\n⚠️ Đã dừng bởi người dùng")
                    break
                except Exception as e:
                    print(f"❌ Lỗi: {e}")

        print("\n👋 Tạm biệt!")

    except KeyboardInterrupt:
        print("\n⚠️ Chương trình bị dừng")
    except Exception as e:
        print(f"❌ Lỗi nghiêm trọng: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
