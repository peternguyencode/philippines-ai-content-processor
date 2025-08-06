#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test CSV AI Processor với file mẫu

Author: AI Assistant
Date: 2025-08-06
"""

from csv_ai_processor import CSVAIProcessor


def main():
    print("🧪 TEST CSV AI PROCESSOR")
    print("=" * 40)

    # Khởi tạo processor
    processor = CSVAIProcessor()

    # Test với file posts.csv
    input_csv = "./data/posts.csv"

    print(f"📁 Testing với file: {input_csv}")

    # Test với 2 posts đầu tiên và delay 5 giây để tránh rate limit
    stats = processor.process_csv_pipeline(input_csv=input_csv, limit=2, delay=5.0)

    print(f"\n✅ Test completed!")
    print(f"📊 Results: {stats}")


if __name__ == "__main__":
    main()
