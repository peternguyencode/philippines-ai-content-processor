#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MODULE 1: DATA INPUT/OUTPUT HANDLER
Chỉ xử lý việc đọc/ghi dữ liệu từ Google Sheets
"""

import gspread
import time
from datetime import datetime
from typing import List, Dict, Optional, Any
from google.oauth2.service_account import Credentials

class DataInputOutput:
    """Module độc lập xử lý Google Sheets I/O"""
    
    def __init__(self, sheet_id: str, creds_file: str):
        self.sheet_id = sheet_id
        self.creds_file = creds_file
        self.gc = None
        self.sheet = None
        self.worksheet = None
        self._connect()
    
    def _connect(self):
        """Kết nối Google Sheets"""
        try:
            scope = [
                'https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive'
            ]
            
            creds = Credentials.from_service_account_file(
                self.creds_file, scopes=scope
            )
            
            self.gc = gspread.authorize(creds)
            self.sheet = self.gc.open_by_key(self.sheet_id)
            self.worksheet = self.sheet.sheet1
            
            print("✅ [INPUT/OUTPUT] Kết nối Google Sheets thành công!")
            
        except Exception as e:
            print(f"❌ [INPUT/OUTPUT] Lỗi kết nối: {str(e)}")
            raise e
    
    def get_pending_tasks(self) -> List[Dict[str, Any]]:
        """
        Lấy danh sách các task cần xử lý
        Returns: List of {prompt, row_number, status}
        """
        try:
            all_records = self.worksheet.get_all_records()
            
            pending_tasks = []
            for i, record in enumerate(all_records, 2):
                status = str(record.get('Status', '')).lower().strip()
                prompt = str(record.get('Prompt', '')).strip()
                
                if prompt and (not status or status == 'pending'):
                    task = {
                        'prompt': prompt,
                        'row_number': i,
                        'status': status,
                        'original_data': record
                    }
                    pending_tasks.append(task)
            
            print(f"📋 [INPUT/OUTPUT] Tìm thấy {len(pending_tasks)} task pending")
            return pending_tasks
            
        except Exception as e:
            print(f"❌ [INPUT/OUTPUT] Lỗi đọc tasks: {str(e)}")
            return []
    
    def update_task_status(self, row_number: int, status: str):
        """Cập nhật trạng thái task"""
        try:
            self.worksheet.update_cell(row_number, 2, status)
            print(f"✅ [INPUT/OUTPUT] Row {row_number}: {status}")
            time.sleep(0.5)  # Anti rate limit
            
        except Exception as e:
            print(f"❌ [INPUT/OUTPUT] Lỗi update status: {str(e)}")
    
    def save_results(self, row_number: int, results: Dict[str, Any]):
        """Lưu kết quả xử lý vào Google Sheet"""
        try:
            # Column mapping
            updates = {
                3: results.get('title', ''),           # Cột C
                4: results.get('content_preview', ''), # Cột D  
                5: results.get('wp_url', ''),          # Cột E
                6: results.get('image_url', ''),       # Cột F
                7: results.get('meta_title', ''),      # Cột G
                8: results.get('meta_desc', ''),       # Cột H
                9: datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # Cột I
                10: results.get('error_log', '')       # Cột J
            }
            
            for col_num, value in updates.items():
                if value:
                    self.worksheet.update_cell(row_number, col_num, str(value))
                    time.sleep(0.2)
            
            print(f"✅ [INPUT/OUTPUT] Đã lưu results cho row {row_number}")
            
        except Exception as e:
            print(f"❌ [INPUT/OUTPUT] Lỗi lưu results: {str(e)}")
    
    def log_error(self, row_number: int, error_message: str):
        """Ghi log lỗi"""
        try:
            self.update_task_status(row_number, 'error')
            self.worksheet.update_cell(row_number, 10, error_message)
            print(f"❌ [INPUT/OUTPUT] Logged error for row {row_number}: {error_message}")
            
        except Exception as e:
            print(f"❌ [INPUT/OUTPUT] Lỗi ghi log: {str(e)}")

# Test module
if __name__ == "__main__":
    from config import Config
    
    # Test Data I/O module
    data_io = DataInputOutput(
        sheet_id=Config.GOOGLE_SHEET_ID,
        creds_file=Config.GOOGLE_CREDS_FILE
    )
    
    # Test đọc tasks
    tasks = data_io.get_pending_tasks()
    print(f"Found {len(tasks)} pending tasks")
    
    if tasks:
        # Test update status
        first_task = tasks[0]
        print(f"Testing with: {first_task['prompt'][:50]}...")
        # data_io.update_task_status(first_task['row_number'], 'testing')
