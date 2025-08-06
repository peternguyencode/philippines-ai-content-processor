#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main Workflow: Tự động tạo và đăng bài WordPress từ Google Sheet với AI
Author: AI Assistant
Date: 2025-08-04
"""

import os
import sys
import time
import traceback
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any, Optional
from tqdm import tqdm

# Import các module helper
from config import Config
from sheets_helper import SheetsHelper
from mysql_helper import MySQLHelper
from ai_helper import AIHelper
from wp_helper import WPHelper

class WordPressAutomation:
    """Lớp chính điều phối toàn bộ workflow"""
    
    def __init__(self):
        """Khởi tạo các helper classes"""
        print("🚀 Khởi tạo WordPress Automation...")
        
        try:
            # Validate config trước
            Config.validate_config()
            
            # Khởi tạo các helper - có thể chọn MySQL hoặc Google Sheets
            print("🔌 Connecting to data sources...")
            
            # MySQL Helper (mới)
            self.mysql = MySQLHelper()
            
            # Google Sheets Helper (giữ lại để tương thích)
            self.sheets = SheetsHelper()
            
            # AI và WordPress helpers
            self.ai = AIHelper()
            self.wp = WPHelper()
            
            print("✅ Đã khởi tạo thành công tất cả components!")
            
        except Exception as e:
            print(f"❌ Lỗi khởi tạo: {str(e)}")
            sys.exit(1)
    
    def process_single_row(self, row_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Xử lý một hàng dữ liệu từ Google Sheet
        
        Args:
            row_data: Dữ liệu từ một hàng trong Google Sheet
        
        Returns:
            Dict chứa kết quả xử lý
        """
        row_number = row_data['row_number']
        prompt = row_data['prompt']
        
        result = {
            'row_number': row_number,
            'success': False,
            'error': None,
            'data': {}
        }
        
        try:
            print(f"\n📝 Xử lý hàng {row_number}: {prompt[:50]}...")
            
            # Cập nhật trạng thái đang xử lý
            self.sheets.update_row_status(row_number, 'processing')
            
            # Bước 1: Sinh content với AI
            print("🤖 Đang sinh content với AI...")
            ai_result = self.ai.generate_content(prompt)
            
            if not ai_result or 'title' not in ai_result:
                raise Exception("AI không sinh được content hợp lệ")
            
            title = ai_result['title']
            content = ai_result['content']
            image_prompt = ai_result.get('image_prompt', '')
            meta_title = ai_result.get('meta_title', title)
            meta_desc = ai_result.get('meta_description', '')
            
            print(f"✅ Đã sinh content: {title}")
            
            # Bước 2: Sinh ảnh cover
            image_url = None
            if image_prompt:
                print("🎨 Đang sinh ảnh cover...")
                image_url = self.ai.generate_image(image_prompt)
                if image_url:
                    print(f"✅ Đã sinh ảnh: {image_url}")
            
            # Bước 3: Đăng lên WordPress
            print("📤 Đang đăng lên WordPress...")
            wp_result = self.wp.process_complete_post(
                title=title,
                content=content,
                image_url=image_url,
                meta_title=meta_title,
                meta_description=meta_desc,
                auto_publish=False  # Tạo draft trước
            )
            
            if not wp_result:
                raise Exception("Không thể đăng bài lên WordPress")
            
            # Chuẩn bị data để cập nhật Google Sheet
            update_data = {
                'title': title,
                'content': content[:500] + "..." if len(content) > 500 else content,
                'wp_url': wp_result['post_url'],
                'image_url': wp_result.get('featured_image', ''),
                'meta_title': meta_title,
                'meta_desc': meta_desc
            }
            
            # Cập nhật thành công
            self.sheets.update_row_status(row_number, 'completed', **update_data)
            
            result['success'] = True
            result['data'] = update_data
            
            print(f"🎉 Hoàn thành hàng {row_number}: {wp_result['post_url']}")
            
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Lỗi xử lý hàng {row_number}: {error_msg}")
            
            # Ghi log lỗi vào Google Sheet
            self.sheets.update_error(row_number, error_msg)
            
            result['error'] = error_msg
        
        return result
    
    def process_batch(self, max_rows: int = None, concurrent: bool = True) -> Dict[str, Any]:
        """
        Xử lý hàng loạt các hàng từ Google Sheet
        
        Args:
            max_rows: Số hàng tối đa cần xử lý (None = tất cả)
            concurrent: Có xử lý đồng thời không
        
        Returns:
            Dict chứa thống kê kết quả
        """
        print("\n🔍 Tìm kiếm các hàng cần xử lý...")
        
        # Lấy danh sách hàng chưa xử lý
        pending_rows = self.sheets.get_pending_rows()
        
        if not pending_rows:
            print("ℹ️ Không có hàng nào cần xử lý!")
            return {'total': 0, 'success': 0, 'error': 0}
        
        # Giới hạn số hàng nếu cần
        if max_rows:
            pending_rows = pending_rows[:max_rows]
        
        print(f"📊 Sẽ xử lý {len(pending_rows)} hàng")
        
        # Thống kê kết quả
        stats = {
            'total': len(pending_rows),
            'success': 0,
            'error': 0,
            'results': []
        }
        
        # Bắt đầu xử lý
        start_time = time.time()
        
        if concurrent and len(pending_rows) > 1:
            # Xử lý đồng thời với ThreadPoolExecutor
            print(f"⚡ Xử lý đồng thời với {Config.CONCURRENT_REQUESTS} threads...")
            
            with ThreadPoolExecutor(max_workers=Config.CONCURRENT_REQUESTS) as executor:
                # Submit tất cả tasks
                future_to_row = {
                    executor.submit(self.process_single_row, row): row 
                    for row in pending_rows
                }
                
                # Theo dõi tiến trình với tqdm
                with tqdm(total=len(pending_rows), desc="Xử lý bài viết") as pbar:
                    for future in as_completed(future_to_row):
                        try:
                            result = future.result()
                            
                            if result['success']:
                                stats['success'] += 1
                            else:
                                stats['error'] += 1
                            
                            stats['results'].append(result)
                            pbar.update(1)
                            
                            # Delay nhỏ giữa các request
                            time.sleep(Config.REQUEST_DELAY)
                            
                        except Exception as e:
                            print(f"❌ Exception trong concurrent processing: {str(e)}")
                            stats['error'] += 1
                            pbar.update(1)
        else:
            # Xử lý tuần tự
            print("🔄 Xử lý tuần tự...")
            
            with tqdm(total=len(pending_rows), desc="Xử lý bài viết") as pbar:
                for row in pending_rows:
                    try:
                        result = self.process_single_row(row)
                        
                        if result['success']:
                            stats['success'] += 1
                        else:
                            stats['error'] += 1
                        
                        stats['results'].append(result)
                        pbar.update(1)
                        
                        # Delay giữa các request
                        time.sleep(Config.REQUEST_DELAY)
                        
                    except Exception as e:
                        print(f"❌ Exception trong sequential processing: {str(e)}")
                        stats['error'] += 1
                        pbar.update(1)
        
        # Tính thời gian thực hiện
        end_time = time.time()
        duration = end_time - start_time
        
        # In thống kê kết quả
        print(f"\n📈 KẾT QUA CUỐI CÙNG:")
        print(f"   Tổng số hàng xử lý: {stats['total']}")
        print(f"   Thành công: {stats['success']}")
        print(f"   Lỗi: {stats['error']}")
        print(f"   Thời gian: {duration:.2f} giây")
        print(f"   Tốc độ: {stats['total']/duration:.2f} bài/giây")
        
        return stats
    
    def import_json_to_mysql(self, json_file: str = "bonus365casinoall_posts.json") -> Dict[str, Any]:
        """
        Import dữ liệu từ JSON vào MySQL Database
        
        Args:
            json_file: Đường dẫn tới file JSON
            
        Returns:
            Dict chứa thống kê import
        """
        print(f"\n� Bắt đầu import JSON vào MySQL...")
        print(f"📁 File: {json_file}")
        
        try:
            # Kiểm tra file tồn tại
            if not os.path.exists(json_file):
                raise FileNotFoundError(f"File {json_file} không tồn tại!")
            
            # Kiểm tra kết nối MySQL
            if not self.mysql.check_connection():
                raise ConnectionError("MySQL connection failed!")
            
            # Hiển thị trạng thái hiện tại
            current_stats = self.mysql.get_posts_count()
            print(f"📊 Posts hiện tại trong database: {current_stats['total']}")
            
            # Thực hiện import
            import_stats = self.mysql.import_from_json(json_file)
            
            print(f"\n🎉 IMPORT HOÀN THÀNH!")
            print(f"📊 Kết quả:")
            print(f"   Tổng số bài xử lý: {import_stats['total']}")
            print(f"   Import thành công: {import_stats['success']}")
            print(f"   Bỏ qua (trùng lặp): {import_stats['duplicates']}")
            print(f"   Lỗi: {import_stats['errors']}")
            
            return import_stats
            
        except Exception as e:
            error_msg = f"Import failed: {str(e)}"
            print(f"❌ {error_msg}")
            return {
                'total': 0,
                'success': 0,
                'duplicates': 0,
                'errors': 1,
                'error_message': error_msg
            }
    
    def export_mysql_to_json(self, output_file: str = "exported_posts.json", limit: Optional[int] = None) -> bool:
        """
        Export dữ liệu từ MySQL ra file JSON
        
        Args:
            output_file: Tên file JSON output
            limit: Giới hạn số bài export (None = tất cả)
            
        Returns:
            bool: True nếu thành công
        """
        print(f"\n📤 Export MySQL data to JSON...")
        print(f"📁 Output file: {output_file}")
        
        try:
            if not self.mysql.check_connection():
                raise ConnectionError("MySQL connection failed!")
            
            success = self.mysql.export_to_json(output_file, limit)
            
            if success:
                print(f"✅ Export thành công: {output_file}")
            else:
                print(f"❌ Export thất bại")
            
            return success
            
        except Exception as e:
            print(f"❌ Export error: {str(e)}")
            return False
    
    def run_interactive(self):
        """Chạy chế độ tương tác"""
        print("\n🎮 CHẾ ĐỘ TƯƠNG TÁC")
        print("1. Xử lý tất cả hàng pending (Google Sheets)")
        print("2. Xử lý giới hạn số hàng (Google Sheets)")
        print("3. Import JSON vào MySQL")
        print("4. Export MySQL ra JSON")
        print("5. Kiểm tra trạng thái MySQL")
        print("6. Kiểm tra trạng thái Google Sheets")
        print("0. Thoát")
        
        while True:
            try:
                choice = input("\nChọn tùy chọn (0-6): ").strip()
                
                if choice == '0':
                    print("👋 Tạm biệt!")
                    break
                elif choice == '1':
                    stats = self.process_batch()
                    print(f"\n🎯 Đã xử lý xong {stats['success']}/{stats['total']} bài viết")
                elif choice == '2':
                    max_rows = int(input("Nhập số hàng tối đa: "))
                    stats = self.process_batch(max_rows=max_rows)
                    print(f"\n🎯 Đã xử lý xong {stats['success']}/{stats['total']} bài viết")
                elif choice == '3':
                    json_file = input("Nhập tên file JSON (default: bonus365casinoall_posts.json): ").strip()
                    if not json_file:
                        json_file = "bonus365casinoall_posts.json"
                    import_stats = self.import_json_to_mysql(json_file)
                    print(f"\n🎯 Import hoàn thành: {import_stats['success']}/{import_stats['total']} posts")
                elif choice == '4':
                    output_file = input("Nhập tên file output (default: exported_posts.json): ").strip()
                    if not output_file:
                        output_file = "exported_posts.json"
                    limit_input = input("Giới hạn số bài (Enter = tất cả): ").strip()
                    limit = int(limit_input) if limit_input else None
                    success = self.export_mysql_to_json(output_file, limit)
                    if success:
                        print(f"\n✅ Export thành công: {output_file}")
                elif choice == '5':
                    stats = self.mysql.get_posts_count()
                    print(f"\n📊 MySQL Database Status:")
                    print(f"   Total posts: {stats['total']}")
                    if stats.get('by_status'):
                        print("   By status:")
                        for status, count in stats['by_status'].items():
                            print(f"     - {status}: {count}")
                elif choice == '6':
                    pending = self.sheets.get_pending_rows()
                    print(f"\n📊 Google Sheets Status:")
                    print(f"   Pending rows: {len(pending)}")
                else:
                    print("❌ Tùy chọn không hợp lệ!")
                    
            except KeyboardInterrupt:
                print("\n⚠️ Đã dừng bởi người dùng")
                break
            except Exception as e:
                print(f"❌ Lỗi: {str(e)}")

def main():
    """Hàm main chính"""
    print("🔥 WORDPRESS CONTENT AUTOMATION WITH AI 🔥")
    print("=" * 50)
    
    try:
        # Khởi tạo automation
        automation = WordPressAutomation()
        
        # Kiểm tra tham số dòng lệnh
        if len(sys.argv) > 1:
            command = sys.argv[1].lower()
            
            if command == 'batch':
                # Xử lý batch tất cả
                max_rows = int(sys.argv[2]) if len(sys.argv) > 2 else None
                stats = automation.process_batch(max_rows=max_rows)
                
            elif command == 'import':
                # Import JSON vào MySQL
                json_file = sys.argv[2] if len(sys.argv) > 2 else "bonus365casinoall_posts.json"
                import_stats = automation.import_json_to_mysql(json_file)
                print(f"🎯 Import completed: {import_stats['success']}/{import_stats['total']} posts")
                
            elif command == 'export':
                # Export MySQL ra JSON
                output_file = sys.argv[2] if len(sys.argv) > 2 else "exported_posts.json"
                limit = int(sys.argv[3]) if len(sys.argv) > 3 else None
                success = automation.export_mysql_to_json(output_file, limit)
                print(f"🎯 Export {'successful' if success else 'failed'}")
                
            elif command == 'single':
                # Xử lý 1 bài
                stats = automation.process_batch(max_rows=1, concurrent=False)
                
            else:
                print(f"❌ Lệnh không hợp lệ: {command}")
                print("Sử dụng: python main.py [batch|import|export|single] [args...]")
                print("Examples:")
                print("  python main.py import bonus365casinoall_posts.json")
                print("  python main.py export exported_posts.json 10")
                print("  python main.py batch 5")
        else:
            # Chạy chế độ tương tác
            automation.run_interactive()
            
    except KeyboardInterrupt:
        print("\n⚠️ Chương trình bị dừng bởi người dùng")
    except Exception as e:
        print(f"❌ Lỗi nghiêm trọng: {str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    main()
