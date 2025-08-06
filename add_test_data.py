#!/usr/bin/env python3
from sheets_helper import SheetsHelper

sheets = SheetsHelper()

# Thêm bài test
test_prompt = "Viết bài về lợi ích của công nghệ blockchain trong tài chính"
sheets.worksheet.append_row([test_prompt, 'pending', '', '', '', '', '', '', '', ''])

print(f"✅ Đã thêm bài test: {test_prompt}")
print("📋 Danh sách bài pending:")

# Kiểm tra pending rows
pending = sheets.get_pending_rows()
for row in pending:
    print(f"- Hàng {row['row_number']}: {row['prompt'][:50]}...")
