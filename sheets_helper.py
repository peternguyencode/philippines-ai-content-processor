import gspread
import time
from datetime import datetime
from typing import List, Dict, Optional, Any
from config import Config
from google.oauth2.service_account import Credentials

class SheetsHelper:
    """Lớp xử lý Google Sheets API"""
    
    def __init__(self):
        self.gc = None
        self.sheet = None
        self.worksheet = None
        self._connect()
    
    def _connect(self):
        """Kết nối đến Google Sheets"""
        try:
            # Định nghĩa scope cần thiết
            scope = [
                'https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive'
            ]
            
            # Tạo credentials từ service account
            creds = Credentials.from_service_account_file(
                Config.GOOGLE_CREDS_FILE, 
                scopes=scope
            )
            
            # Khởi tạo client
            self.gc = gspread.authorize(creds)
            
            # Mở sheet theo ID
            self.sheet = self.gc.open_by_key(Config.GOOGLE_SHEET_ID)
            self.worksheet = self.sheet.sheet1  # Sử dụng sheet đầu tiên
            
            print("✅ Kết nối Google Sheets thành công!")
            
        except Exception as e:
            print(f"❌ Lỗi kết nối Google Sheets: {str(e)}")
            raise e
    
    def get_pending_rows(self) -> List[Dict[str, Any]]:
        """Lấy danh sách các hàng chưa xử lý (status = 'pending' hoặc rỗng)"""
        try:
            # Lấy tất cả dữ liệu
            all_records = self.worksheet.get_all_records()
            
            pending_rows = []
            for i, record in enumerate(all_records, 2):  # Bắt đầu từ hàng 2 (do header ở hàng 1)
                # Sử dụng key chính xác từ header và convert sang string
                status = str(record.get('Status', '')).lower().strip()
                prompt = str(record.get('Prompt', '')).strip()
                
                # Chỉ lấy những hàng có prompt và chưa xử lý
                if prompt and (not status or status == 'pending'):
                    record['row_number'] = i
                    record['prompt'] = prompt  # Thêm key 'prompt' thống nhất
                    pending_rows.append(record)
            
            print(f"📋 Tìm thấy {len(pending_rows)} hàng cần xử lý")
            return pending_rows
            
        except Exception as e:
            print(f"❌ Lỗi đọc dữ liệu: {str(e)}")
            return []
    
    def update_row_status(self, row_number: int, status: str, **kwargs):
        """Cập nhật trạng thái và thông tin khác cho một hàng"""
        try:
            # Cập nhật status
            self.worksheet.update_cell(row_number, 2, status)  # Cột B = Status
            
            # Cập nhật các thông tin khác
            column_mapping = {
                'title': 3,         # Cột C
                'content': 4,       # Cột D
                'wp_url': 5,        # Cột E
                'image_url': 6,     # Cột F
                'meta_title': 7,    # Cột G
                'meta_desc': 8,     # Cột H
                'created_date': 9,  # Cột I
                'error_log': 10     # Cột J
            }
            
            for key, value in kwargs.items():
                if key in column_mapping and value:
                    col_num = column_mapping[key]
                    self.worksheet.update_cell(row_number, col_num, str(value))
            
            # Luôn cập nhật thời gian
            if 'created_date' not in kwargs:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.worksheet.update_cell(row_number, 9, current_time)
            
            print(f"✅ Đã cập nhật hàng {row_number}: {status}")
            
            # Delay nhỏ để tránh rate limit
            time.sleep(0.5)
            
        except Exception as e:
            print(f"❌ Lỗi cập nhật hàng {row_number}: {str(e)}")
    
    def update_error(self, row_number: int, error_message: str):
        """Cập nhật lỗi cho một hàng"""
        try:
            self.update_row_status(
                row_number, 
                'error', 
                error_log=error_message
            )
        except Exception as e:
            print(f"❌ Lỗi ghi log lỗi: {str(e)}")
    
    def batch_update(self, updates: List[Dict]):
        """Cập nhật hàng loạt để tối ưu tốc độ"""
        try:
            # Chuẩn bị dữ liệu update dạng batch
            batch_data = []
            
            for update in updates:
                row_num = update['row_number']
                data = update['data']
                
                for key, value in data.items():
                    if key == 'status':
                        batch_data.append({
                            'range': f'B{row_num}',
                            'values': [[value]]
                        })
                    # Thêm các trường khác...
            
            # Thực hiện batch update
            if batch_data:
                self.worksheet.batch_update(batch_data)
                print(f"✅ Đã cập nhật batch {len(batch_data)} ô")
            
        except Exception as e:
            print(f"❌ Lỗi batch update: {str(e)}")
    
    def create_sample_header(self):
        """Tạo header mẫu cho Google Sheet"""
        headers = [
            'Prompt', 'Status', 'Title', 'Content', 'WP_URL', 
            'Image_URL', 'Meta_Title', 'Meta_Desc', 'Created_Date', 'Error_Log'
        ]
        
        try:
            # Kiểm tra xem đã có header chưa
            first_row = self.worksheet.row_values(1)
            
            if not first_row or first_row[0] != 'Prompt':
                self.worksheet.insert_row(headers, 1)
                print("✅ Đã tạo header cho Google Sheet")
            else:
                print("ℹ️ Header đã tồn tại")
                
        except Exception as e:
            print(f"❌ Lỗi tạo header: {str(e)}")
    
    def add_sample_data(self):
        """Thêm dữ liệu mẫu để test"""
        sample_data = [
            ["Viết bài về AI trong marketing", "pending", "", "", "", "", "", "", "", ""],
            ["Hướng dẫn SEO website", "pending", "", "", "", "", "", "", "", ""],
            ["Review sản phẩm iPhone mới", "pending", "", "", "", "", "", "", "", ""]
        ]
        
        try:
            for data in sample_data:
                self.worksheet.append_row(data)
            print("✅ Đã thêm dữ liệu mẫu")
            
        except Exception as e:
            print(f"❌ Lỗi thêm dữ liệu mẫu: {str(e)}")

# Test function
if __name__ == "__main__":
    try:
        Config.validate_config()
        sheets = SheetsHelper()
        
        # Tạo header và dữ liệu mẫu
        sheets.create_sample_header()
        sheets.add_sample_data()
        
        # Test đọc dữ liệu
        pending = sheets.get_pending_rows()
        print(f"Tìm thấy {len(pending)} hàng cần xử lý")
        
    except Exception as e:
        print(f"Lỗi test: {str(e)}")
