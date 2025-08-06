#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch CSV Processor - Xử lý toàn bộ 86 posts với AI

Author: AI Assistant
Date: 2025-08-06
"""

import sys

from csv_ai_processor import CSVAIProcessor


def run_full_batch():
    print("🔥 FULL BATCH CSV AI PROCESSING")
    print("=" * 50)
    print("📊 Sẽ xử lý: 86 posts")
    print("⏱️  Thời gian dự kiến: ~72 phút")
    print("💰 Chi phí dự kiến: ~$0.17 (GPT-3.5-turbo)")
    print("🎯 Output: posts_ready_[timestamp].csv")
    print()

    confirm = input("Bạn có chắc chắn muốn tiếp tục? (y/n): ").strip().lower()

    if confirm != "y":
        print("❌ Đã hủy batch processing")
        return

    # Khởi tạo processor
    processor = CSVAIProcessor()

    # Chạy full batch
    stats = processor.process_csv_pipeline(
        input_csv="./data/posts.csv",
        limit=86,
        delay=5.0,  # 5 giây delay để tránh rate limiting
    )

    print(f"\n🎉 FULL BATCH HOÀN THÀNH!")
    print(f"📈 Results: {stats}")

    # Kiểm tra results
    if stats["success"] == 86:
        print("✅ Tất cả 86 posts đã được xử lý thành công!")
    else:
        print(f"⚠️  {stats['errors']} posts bị lỗi, cần kiểm tra log files")


if __name__ == "__main__":
    try:
        run_full_batch()
    except KeyboardInterrupt:
        print("\n⚠️ Đã dừng bởi người dùng")
    except Exception as e:
        print(f"❌ Lỗi nghiêm trọng: {e}")
        import traceback

        traceback.print_exc()
