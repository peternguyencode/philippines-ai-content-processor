#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MODULE 4: WORKFLOW ORCHESTRATOR
Điều phối toàn bộ quy trình từ input → AI → WordPress
"""

import time
from datetime import datetime
from typing import Dict, List, Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# Import các modules riêng biệt
from module_data_io import DataInputOutput
from module_ai_generator import AIContentGenerator  
from module_wp_publisher import WordPressPublisher

class WorkflowOrchestrator:
    """Module điều phối toàn bộ workflow"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.stats = {
            'total_processed': 0,
            'successful': 0,
            'failed': 0,
            'start_time': None,
            'errors': []
        }
        
        # Khởi tạo các modules
        self._init_modules()
        
        # Thread lock cho stats
        self.stats_lock = threading.Lock()
    
    def _init_modules(self):
        """Khởi tạo tất cả modules"""
        try:
            # Module 1: Data I/O
            self.data_io = DataInputOutput(
                sheet_id=self.config['google_sheet_id'],
                creds_file=self.config['google_creds_file']
            )
            
            # Module 2: AI Generator
            self.ai_generator = AIContentGenerator(
                openai_key=self.config['openai_api_key'],
                gemini_key=self.config['gemini_api_key']
            )
            
            # Module 3: WordPress Publisher
            self.wp_publisher = WordPressPublisher(
                wp_url=self.config['wp_url'],
                username=self.config['wp_username'],
                password=self.config['wp_password']
            )
            
            print("✅ [ORCHESTRATOR] Tất cả modules đã được khởi tạo!")
            
        except Exception as e:
            print(f"❌ [ORCHESTRATOR] Lỗi khởi tạo modules: {str(e)}")
            raise e
    
    def process_single_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Xử lý 1 task hoàn chỉnh: Input → AI → WordPress → Output
        """
        task_id = f"Task-{task['row_number']}"
        prompt = task['prompt']
        row_number = task['row_number']
        
        print(f"\n🚀 [ORCHESTRATOR] Bắt đầu {task_id}: {prompt[:50]}...")
        
        results = {
            'task_id': task_id,
            'row_number': row_number,
            'success': False,
            'error_message': '',
            'wp_url': '',
            'processing_time': 0
        }
        
        start_time = time.time()
        
        try:
            # STEP 1: Update status "processing"
            self.data_io.update_task_status(row_number, 'processing')
            
            # STEP 2: Generate AI content
            print(f"🤖 [ORCHESTRATOR] {task_id}: Generating content...")
            content_data = self.ai_generator.generate_content(prompt)
            
            if not content_data.get('title'):
                raise Exception("AI không tạo được content hợp lệ")
            
            # STEP 3: Generate image (optional)
            image_data = None
            image_url = None
            
            try:
                print(f"🎨 [ORCHESTRATOR] {task_id}: Generating image...")
                image_url = self.ai_generator.generate_image(content_data['title'])
                
                if image_url:
                    image_data = self.ai_generator.download_image(
                        image_url, f"{task_id}.jpg"
                    )
            except Exception as img_error:
                print(f"⚠️ [ORCHESTRATOR] {task_id}: Image gen failed: {str(img_error)}")
                # Không dừng process, tiếp tục không có ảnh
            
            # STEP 4: Publish to WordPress
            print(f"📝 [ORCHESTRATOR] {task_id}: Publishing to WordPress...")
            wp_url = self.wp_publisher.publish_complete_post(content_data, image_data)
            
            if not wp_url:
                raise Exception("Không thể publish lên WordPress")
            
            # STEP 5: Save results to Sheet
            sheet_results = {
                'title': content_data.get('title', ''),
                'content_preview': content_data.get('content', '')[:200] + '...',
                'wp_url': wp_url,
                'image_url': image_url or '',
                'meta_title': content_data.get('meta_title', ''),
                'meta_desc': content_data.get('meta_desc', ''),
                'error_log': ''
            }
            
            self.data_io.save_results(row_number, sheet_results)
            self.data_io.update_task_status(row_number, 'completed')
            
            # Update results
            results.update({
                'success': True,
                'wp_url': wp_url,
                'content_data': content_data,
                'image_url': image_url
            })
            
            processing_time = time.time() - start_time
            results['processing_time'] = processing_time
            
            print(f"✅ [ORCHESTRATOR] {task_id} HOÀN THÀNH trong {processing_time:.1f}s")
            print(f"   📄 Post: {wp_url}")
            
            return results
            
        except Exception as e:
            error_msg = str(e)
            processing_time = time.time() - start_time
            
            print(f"❌ [ORCHESTRATOR] {task_id} THẤT BẠI: {error_msg}")
            
            # Log error
            self.data_io.log_error(row_number, error_msg)
            
            results.update({
                'success': False,
                'error_message': error_msg,
                'processing_time': processing_time
            })
            
            return results
    
    def process_batch(self, max_workers: int = 2, max_tasks: Optional[int] = None) -> Dict[str, Any]:
        """
        Xử lý batch tasks với threading
        """
        print("🔄 [ORCHESTRATOR] Bắt đầu batch processing...")
        
        # Reset stats
        self.stats = {
            'total_processed': 0,
            'successful': 0,
            'failed': 0,
            'start_time': datetime.now(),
            'errors': []
        }
        
        # Lấy danh sách tasks
        pending_tasks = self.data_io.get_pending_tasks()
        
        if not pending_tasks:
            print("ℹ️ [ORCHESTRATOR] Không có tasks pending")
            return self.stats
        
        # Giới hạn số lượng nếu có
        if max_tasks and len(pending_tasks) > max_tasks:
            pending_tasks = pending_tasks[:max_tasks]
        
        print(f"📋 [ORCHESTRATOR] Sẽ xử lý {len(pending_tasks)} tasks với {max_workers} workers")
        
        # Process với ThreadPoolExecutor
        results = []
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit tất cả tasks
            future_to_task = {
                executor.submit(self.process_single_task, task): task 
                for task in pending_tasks
            }
            
            # Collect results
            for future in as_completed(future_to_task):
                task = future_to_task[future]
                
                try:
                    result = future.result(timeout=300)  # 5 phút timeout
                    results.append(result)
                    
                    # Update stats thread-safe
                    with self.stats_lock:
                        self.stats['total_processed'] += 1
                        if result['success']:
                            self.stats['successful'] += 1
                        else:
                            self.stats['failed'] += 1
                            self.stats['errors'].append({
                                'task_id': result['task_id'],
                                'error': result['error_message']
                            })
                    
                except Exception as e:
                    error_msg = f"Executor error for {task['row_number']}: {str(e)}"
                    print(f"❌ [ORCHESTRATOR] {error_msg}")
                    
                    with self.stats_lock:
                        self.stats['total_processed'] += 1
                        self.stats['failed'] += 1
                        self.stats['errors'].append({
                            'task_id': f"Task-{task['row_number']}",
                            'error': error_msg
                        })
        
        # Tính toán thời gian
        end_time = datetime.now()
        total_time = (end_time - self.stats['start_time']).total_seconds()
        
        # Báo cáo kết quả
        print(f"\n📊 [ORCHESTRATOR] BATCH HOÀN THÀNH:")
        print(f"   ⏱️  Thời gian: {total_time:.1f}s")
        print(f"   📈 Tổng cộng: {self.stats['total_processed']}")
        print(f"   ✅ Thành công: {self.stats['successful']}")
        print(f"   ❌ Thất bại: {self.stats['failed']}")
        
        if self.stats['errors']:
            print(f"   🚨 Errors:")
            for error in self.stats['errors']:
                print(f"      - {error['task_id']}: {error['error']}")
        
        success_rate = (self.stats['successful'] / self.stats['total_processed']) * 100 if self.stats['total_processed'] > 0 else 0
        print(f"   📊 Tỷ lệ thành công: {success_rate:.1f}%")
        
        self.stats['end_time'] = end_time
        self.stats['total_time'] = total_time
        self.stats['success_rate'] = success_rate
        self.stats['results'] = results
        
        return self.stats
    
    def process_interactive(self):
        """Chế độ interactive processing"""
        print("🎮 [ORCHESTRATOR] Interactive Mode")
        print("Nhập 'q' để thoát, 'status' để xem trạng thái")
        
        while True:
            try:
                command = input("\n👉 Nhập prompt (hoặc command): ").strip()
                
                if command.lower() == 'q':
                    print("👋 Bye!")
                    break
                elif command.lower() == 'status':
                    pending = self.data_io.get_pending_tasks()
                    print(f"📋 Có {len(pending)} tasks pending")
                    continue
                elif command.lower() == 'batch':
                    print("🔄 Chạy batch processing...")
                    self.process_batch()
                    continue
                elif not command:
                    continue
                
                # Tạo task tạm thời
                temp_task = {
                    'prompt': command,
                    'row_number': 999,  # Temp row
                    'status': 'processing'
                }
                
                result = self.process_single_task(temp_task)
                
                if result['success']:
                    print(f"✅ Thành công: {result['wp_url']}")
                else:
                    print(f"❌ Thất bại: {result['error_message']}")
                    
            except KeyboardInterrupt:
                print("\n👋 Interrupted! Bye!")
                break
            except Exception as e:
                print(f"❌ Error: {str(e)}")

# Test module
if __name__ == "__main__":
    from config import Config
    
    # Test config
    test_config = {
        'google_sheet_id': Config.GOOGLE_SHEET_ID,
        'google_creds_file': Config.GOOGLE_CREDS_FILE,
        'openai_api_key': Config.OPENAI_API_KEY,
        'gemini_api_key': Config.GEMINI_API_KEY,
        'wp_url': Config.WP_URL,
        'wp_username': Config.WP_USERNAME,
        'wp_password': Config.WP_PASSWORD
    }
    
    # Test orchestrator
    orchestrator = WorkflowOrchestrator(test_config)
    
    # Test batch processing (1 task)
    stats = orchestrator.process_batch(max_workers=1, max_tasks=1)
    
    print(f"\n📊 Final Stats:")
    print(f"Success Rate: {stats.get('success_rate', 0):.1f}%")
    print(f"Total Time: {stats.get('total_time', 0):.1f}s")
