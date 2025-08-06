#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DEMO: Pandas + AI Paraphrase - Minh họa cách hoạt động

Chạy file này để hiểu rõ cách pandas đọc CSV và AI paraphrase
"""

import json
from datetime import datetime

import pandas as pd


def demo_pandas_basics():
    """Demo cơ bản về pandas"""
    print("🐼 DEMO PANDAS - Thư viện xử lý dữ liệu Python")
    print("=" * 60)

    # 1. Tạo DataFrame từ dictionary (giả lập CSV data)
    sample_data = {
        "id": [1, 2, 3],
        "title": [
            "Cách chơi baccarat online hiệu quả",
            "Tips slot machine thắng lớn",
            "Hướng dẫn poker cho người mới",
        ],
        "content": [
            "Baccarat là trò chơi casino phổ biến. Người chơi cần hiểu quy tắc cơ bản.",
            "Slot machine có nhiều loại. Chọn máy phù hợp rất quan trọng.",
            "Poker cần kỹ năng và chiến thuật. Học từ cơ bản đến nâng cao.",
        ],
        "created_date": ["2025-08-05", "2025-08-05", "2025-08-05"],
    }

    # 2. Tạo DataFrame (giống như đọc CSV)
    df = pd.DataFrame(sample_data)

    print("📊 PANDAS DataFrame (giống như đọc CSV):")
    print(df)
    print()

    print(f"📈 Thống kê:")
    print(f"   Số rows: {len(df)}")
    print(f"   Số columns: {len(df.columns)}")
    print(f"   Columns: {list(df.columns)}")
    print()

    # 3. Truy cập dữ liệu
    print("🔍 TRUY CẬP DỮ LIỆU:")
    for index, row in df.iterrows():
        print(f"   Row {index+1}:")
        print(f"     ID: {row['id']}")
        print(f"     Title: {row['title'][:30]}...")
        print(f"     Content: {row['content'][:40]}...")
        print()

    return df


def demo_ai_paraphrase_simulation():
    """Demo giả lập AI paraphrase (không gọi API thật)"""
    print("🤖 DEMO AI PARAPHRASE - Giả lập ChatGPT")
    print("=" * 60)

    original_posts = [
        {
            "title": "Cách chơi baccarat online hiệu quả",
            "content": "Baccarat là trò chơi casino phổ biến. Người chơi cần hiểu quy tắc cơ bản.",
        },
        {
            "title": "Tips slot machine thắng lớn",
            "content": "Slot machine có nhiều loại. Chọn máy phù hợp rất quan trọng.",
        },
    ]

    # Giả lập AI response (thực tế sẽ gọi ChatGPT API)
    ai_responses = [
        {
            "new_title": "Master Baccarat Strategies for Philippines Online Casino Players",
            "new_content": "Discover the most effective baccarat gaming techniques specifically designed for Filipino casino enthusiasts. Understanding fundamental rules is essential for maximizing your winning potential.",
            "notes": "Content localized for Philippines market with SEO optimization",
        },
        {
            "new_title": "Ultimate Slot Gaming Guide Philippines",
            "new_content": "Explore comprehensive slot machine strategies tailored for Philippines online casino market. Selecting the right slot games is crucial for Filipino players seeking maximum returns.",
            "notes": "Optimized for Philippines slot gaming audience",
        },
    ]

    print("🔄 QUÁN TRÌNH AI PARAPHRASE:")
    for i, (original, ai_result) in enumerate(zip(original_posts, ai_responses)):
        print(f"\n📝 POST #{i+1}:")
        print(f"   ORIGINAL TITLE: {original['title']}")
        print(f"   AI NEW TITLE:   {ai_result['new_title']}")
        print(f"   ORIGINAL CONTENT: {original['content']}")
        print(f"   AI NEW CONTENT:   {ai_result['new_content'][:80]}...")
        print(f"   AI NOTES: {ai_result['notes']}")
        print("   " + "-" * 50)

    return ai_responses


def demo_complete_workflow():
    """Demo quy trình hoàn chỉnh: Pandas + AI Paraphrase"""
    print("🚀 DEMO COMPLETE WORKFLOW - Pandas + AI")
    print("=" * 60)

    # BƯỚC 1: Pandas đọc CSV (giả lập)
    print("📊 BƯỚC 1: PANDAS ĐỌC CSV")
    original_df = demo_pandas_basics()

    # BƯỚC 2: AI Paraphrase (giả lập)
    print("🤖 BƯỚC 2: AI PARAPHRASE")
    ai_results = demo_ai_paraphrase_simulation()

    # BƯỚC 3: Kết hợp kết quả
    print("🔗 BƯỚC 3: KẾT HỢP KẾT QUẢ")

    # Tạo data mới với AI paraphrase
    processed_data = []
    for index, row in original_df.iterrows():
        if index < len(ai_results):  # Chỉ demo 2 posts đầu
            ai_result = ai_results[index]
            processed_data.append(
                {
                    "id": row["id"],
                    "original_title": row["title"],
                    "title": ai_result["new_title"],  # ← AI paraphrased
                    "content": ai_result["new_content"],  # ← AI paraphrased
                    "category": "Live Casino",  # ← AI classified
                    "keywords": "baccarat philippines, online casino",  # ← AI generated
                    "created_date": row["created_date"],
                    "processing_notes": ai_result["notes"],
                }
            )
        else:
            # Giữ nguyên những posts không xử lý
            processed_data.append(
                {
                    "id": row["id"],
                    "original_title": row["title"],
                    "title": row["title"],
                    "content": row["content"],
                    "category": "Casino & Gaming",
                    "keywords": "casino, gaming",
                    "created_date": row["created_date"],
                    "processing_notes": "Not processed in demo",
                }
            )

    # BƯỚC 4: Pandas tạo DataFrame mới
    final_df = pd.DataFrame(processed_data)

    print("✅ BƯỚC 4: KẾT QUẢ CUỐI CÙNG")
    print("DataFrame sau khi xử lý:")
    print(final_df[["id", "original_title", "title", "category"]])
    print()

    # BƯỚC 5: Pandas xuất CSV (giả lập)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"posts_ready_demo_{timestamp}.csv"

    print(f"💾 BƯỚC 5: XUẤT CSV")
    print(f"Sẽ xuất ra file: {output_file}")
    print("(Trong demo này không thực sự tạo file)")

    # final_df.to_csv(output_file, index=False)  # Uncommnet để thực sự tạo file

    return final_df


def show_real_vs_demo():
    """So sánh code demo vs code thật"""
    print("\n🔍 SO SÁNH: DEMO vs THỰC TẾ")
    print("=" * 60)

    print("📋 DEMO CODE (đơn giản):")
    print(
        """
# Demo giả lập
df = pd.DataFrame(sample_data)           # Tạo data giả
ai_result = {'new_title': '...'}         # AI response giả
final_df = pd.DataFrame(processed_data)  # Kết quả demo
"""
    )

    print("🚀 PRODUCTION CODE (thực tế):")
    print(
        """
# Code thực tế trong csv_ai_processor.py
df = pd.read_csv('./data/posts.csv')     # Đọc CSV thật
response = client.chat.completions.create(...)  # Gọi ChatGPT API thật
ai_result = json.loads(response.choices[0].message.content)  # Parse JSON
final_df.to_csv(output_file, index=False)  # Xuất CSV thật
"""
    )

    print("💡 ĐIỂM KHÁC BIỆT:")
    print("   Demo: Dữ liệu giả lập, không gọi API, không tạo file")
    print("   Thực tế: Đọc CSV thật, gọi ChatGPT API, tạo file output")
    print("   Nhưng logic xử lý giống hệt nhau!")


def main():
    """Hàm main demo"""
    print("🎯 PANDAS + AI PARAPHRASE DEMO")
    print("Hiểu cách hệ thống hoạt động mà không cần API keys")
    print("=" * 70)

    try:
        # Chạy demo hoàn chỉnh
        final_df = demo_complete_workflow()

        # So sánh với code thực tế
        show_real_vs_demo()

        print("\n🎉 DEMO HOÀN TẤT!")
        print("Bây giờ bạn đã hiểu:")
        print("   🐼 Pandas: Đọc/xuất CSV dễ dàng")
        print("   🤖 AI Paraphrase: ChatGPT viết lại content")
        print("   🔗 Kết hợp: Tạo hệ thống xử lý content tự động")
        print("\nMuốn chạy thực tế? → python interactive_menu.py")

    except Exception as e:
        print(f"❌ Lỗi demo: {e}")


if __name__ == "__main__":
    main()
