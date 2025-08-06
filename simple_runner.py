#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MODULE 5: SIMPLE RUNNER
Giao diện đơn giản để chạy từng module hoặc toàn bộ hệ thống
"""

import sys
import os
from typing import Optional
from config import Config

# Import các modules
from module_data_io import DataInputOutput
from module_ai_generator import AIContentGenerator
from module_wp_publisher import WordPressPublisher
from module_orchestrator import WorkflowOrchestrator

class SimpleRunner:
    """Giao diện đơn giản để test và chạy system"""
    
    def __init__(self):
        self.config = self._load_config()
        print("🚀 Simple Runner khởi động...")
        print("=" * 60)
    
    def _load_config(self) -> dict:
        """Load config từ environment"""
        config = {
            'google_sheet_id': Config.GOOGLE_SHEET_ID,
            'google_creds_file': Config.GOOGLE_CREDS_FILE,
            'openai_api_key': Config.OPENAI_API_KEY,
            'gemini_api_key': Config.GEMINI_API_KEY,
            'wp_url': Config.WP_URL,
            'wp_username': Config.WP_USERNAME,
            'wp_password': Config.WP_PASSWORD
        }
        
        # Validate config
        missing = [k for k, v in config.items() if not v]
        if missing:
            print(f"❌ Missing config: {', '.join(missing)}")
            print("🔧 Hãy check file .env hoặc set environment variables")
            
        return config
    
    def show_menu(self):
        """Hiển thị menu chính"""
        print("\n📋 MENU CHÍNH:")
        print("1. 🔍 Test từng module riêng biệt")
        print("2. 🤖 Test AI Generator") 
        print("3. 📝 Test WordPress Publisher")
        print("4. 📊 Test Google Sheets I/O")
        print("5. 🚀 Chạy 1 task hoàn chỉnh")
        print("6. 🔄 Chạy batch processing")
        print("7. 🎮 Interactive mode")
        print("8. 📈 Xem thống kê hệ thống")
        print("0. ❌ Thoát")
        print("-" * 40)
    
    def test_ai_generator(self):
        """Test AI Generator module"""
        print("\n🤖 TEST AI GENERATOR")
        print("=" * 30)
        
        try:
            ai_gen = AIContentGenerator(
                openai_key=self.config['openai_api_key'] or "",
                gemini_key=self.config['gemini_api_key'] or ""
            )
            
            prompt = input("👉 Nhập prompt để test (hoặc Enter để dùng mặc định): ").strip()
            if not prompt:
                prompt = "Viết về lợi ích của trí tuệ nhân tạo trong cuộc sống"
            
            print(f"🔄 Generating content for: {prompt}")
            content = ai_gen.generate_content(prompt)
            
            print(f"✅ Generated content:")
            print(f"   📝 Title: {content.get('title', 'N/A')}")
            print(f"   📄 Content: {len(content.get('content', ''))} characters")
            print(f"   🏷️  Tags: {content.get('tags', [])}")
            
            # Test image generation
            generate_image = input("\n🎨 Generate image? (y/n): ").lower() == 'y'
            if generate_image and content.get('title'):
                print("🔄 Generating image...")
                image_url = ai_gen.generate_image(content['title'])
                if image_url:
                    print(f"✅ Image URL: {image_url}")
                else:
                    print("❌ Image generation failed")
            
        except Exception as e:
            print(f"❌ AI Generator test failed: {str(e)}")
    
    def test_wp_publisher(self):
        """Test WordPress Publisher module"""
        print("\n📝 TEST WORDPRESS PUBLISHER")
        print("=" * 35)
        
        try:
            wp_pub = WordPressPublisher(
                wp_url=self.config['wp_url'] or "",
                username=self.config['wp_username'] or "",
                password=self.config['wp_password'] or ""
            )
            
            # Test data
            test_content = {
                'title': f'Test Post từ Simple Runner - {os.environ.get("USERNAME", "User")}',
                'content': '''
                <h2>Đây là bài viết test</h2>
                <p>Bài viết này được tạo từ <strong>Simple Runner</strong> để test module WordPress Publisher.</p>
                <ul>
                    <li>✅ Test HTML formatting</li>
                    <li>🚀 Test publish functionality</li>
                    <li>📝 Test content structure</li>
                </ul>
                <p>Nếu bạn thấy bài này, nghĩa là system hoạt động tốt!</p>
                ''',
                'excerpt': 'Bài viết test từ Simple Runner module',
                'meta_title': 'Test SEO Title - Simple Runner',
                'meta_desc': 'Test SEO description cho bài viết được tạo từ Simple Runner',
                'tags': ['test', 'simple-runner', 'module']
            }
            
            confirm = input("👉 Publish test post? (y/n): ").lower()
            if confirm == 'y':
                print("🔄 Publishing test post...")
                post_url = wp_pub.create_post(test_content)
                
                if post_url:
                    print(f"✅ Test post published: {post_url}")
                else:
                    print("❌ Test post publication failed")
            else:
                print("ℹ️ Test post skipped")
            
        except Exception as e:
            print(f"❌ WordPress Publisher test failed: {str(e)}")
    
    def test_sheets_io(self):
        """Test Google Sheets I/O module"""
        print("\n📊 TEST GOOGLE SHEETS I/O")
        print("=" * 30)
        
        try:
            data_io = DataInputOutput(
                sheet_id=self.config['google_sheet_id'] or "",
                creds_file=self.config['google_creds_file'] or ""
            )
            
            # Test get pending tasks
            tasks = data_io.get_pending_tasks()
            print(f"📋 Found {len(tasks)} pending tasks")
            
            if tasks:
                print("📝 First few tasks:")
                for i, task in enumerate(tasks[:3], 1):
                    print(f"   {i}. Row {task['row_number']}: {task['prompt'][:50]}...")
                    
                # Test update status
                test_update = input("\n👉 Test update status on first task? (y/n): ").lower()
                if test_update == 'y':
                    first_task = tasks[0]
                    print(f"🔄 Testing status update on row {first_task['row_number']}")
                    data_io.update_task_status(first_task['row_number'], 'testing-simple-runner')
                    print("✅ Status updated")
                    
                    # Revert
                    data_io.update_task_status(first_task['row_number'], 'pending')
                    print("🔄 Reverted to pending")
            else:
                print("ℹ️ No pending tasks found")
            
        except Exception as e:
            print(f"❌ Sheets I/O test failed: {str(e)}")
    
    def run_single_task(self):
        """Chạy 1 task hoàn chỉnh"""
        print("\n🚀 RUN SINGLE COMPLETE TASK")
        print("=" * 35)
        
        try:
            orchestrator = WorkflowOrchestrator(self.config)
            
            # Lấy pending tasks
            pending_tasks = orchestrator.data_io.get_pending_tasks()
            
            if not pending_tasks:
                print("ℹ️ Không có pending tasks. Tạo task manual...")
                prompt = input("👉 Nhập prompt: ").strip()
                if not prompt:
                    print("❌ Cần prompt để chạy")
                    return
                
                # Tạo temp task
                temp_task = {
                    'prompt': prompt,
                    'row_number': 999,
                    'status': 'manual'
                }
                
                result = orchestrator.process_single_task(temp_task)
            else:
                print(f"📋 Có {len(pending_tasks)} tasks pending")
                print("Sẽ chạy task đầu tiên...")
                
                first_task = pending_tasks[0]
                print(f"🎯 Task: {first_task['prompt'][:100]}...")
                
                confirm = input("👉 Confirm chạy task này? (y/n): ").lower()
                if confirm != 'y':
                    print("❌ Cancelled")
                    return
                
                result = orchestrator.process_single_task(first_task)
            
            # Báo cáo kết quả
            if result['success']:
                print(f"\n✅ TASK HOÀN THÀNH!")
                print(f"   ⏱️  Thời gian: {result['processing_time']:.1f}s")
                print(f"   🔗 WordPress URL: {result['wp_url']}")
                if result.get('image_url'):
                    print(f"   🖼️  Image: {result['image_url']}")
            else:
                print(f"\n❌ TASK THẤT BẠI!")
                print(f"   ❗ Error: {result['error_message']}")
                print(f"   ⏱️  Thời gian: {result['processing_time']:.1f}s")
                
        except Exception as e:
            print(f"❌ Single task failed: {str(e)}")
    
    def run_batch_processing(self):
        """Chạy batch processing"""
        print("\n🔄 BATCH PROCESSING")
        print("=" * 25)
        
        try:
            orchestrator = WorkflowOrchestrator(self.config)
            
            # Cấu hình batch
            max_workers = int(input("👉 Số workers (1-3, default 2): ") or "2")
            max_tasks = input("👉 Giới hạn tasks (Enter = all): ").strip()
            max_tasks = int(max_tasks) if max_tasks.isdigit() else None
            
            print(f"🔄 Starting batch với {max_workers} workers...")
            if max_tasks:
                print(f"📊 Giới hạn: {max_tasks} tasks")
            
            # Chạy batch
            stats = orchestrator.process_batch(
                max_workers=max_workers,
                max_tasks=max_tasks
            )
            
            # Báo cáo chi tiết
            print(f"\n📈 CHI TIẾT KẾT QUẢ:")
            print(f"   📊 Tổng cộng: {stats['total_processed']}")
            print(f"   ✅ Thành công: {stats['successful']}")
            print(f"   ❌ Thất bại: {stats['failed']}")
            print(f"   📈 Tỷ lệ: {stats.get('success_rate', 0):.1f}%")
            print(f"   ⏱️  Thời gian: {stats.get('total_time', 0):.1f}s")
            
            if stats.get('errors'):
                print(f"\n🚨 ERRORS:")
                for error in stats['errors']:
                    print(f"   - {error['task_id']}: {error['error']}")
                    
        except Exception as e:
            print(f"❌ Batch processing failed: {str(e)}")
    
    def interactive_mode(self):
        """Chế độ interactive"""
        print("\n🎮 INTERACTIVE MODE")
        print("=" * 25)
        print("Commands:")
        print("  - Nhập prompt để tạo post ngay")
        print("  - 'batch' để chạy batch")
        print("  - 'status' để xem trạng thái")
        print("  - 'q' để thoát")
        print("-" * 40)
        
        try:
            orchestrator = WorkflowOrchestrator(self.config)
            orchestrator.process_interactive()
        except Exception as e:
            print(f"❌ Interactive mode failed: {str(e)}")
    
    def show_system_stats(self):
        """Hiển thị thống kê hệ thống"""
        print("\n📈 SYSTEM STATISTICS")
        print("=" * 25)
        
        try:
            data_io = DataInputOutput(
                sheet_id=self.config['google_sheet_id'] or "",
                creds_file=self.config['google_creds_file'] or ""
            )
            
            # Lấy tất cả records
            all_records = data_io.worksheet.get_all_records()
            
            # Thống kê
            total_rows = len(all_records)
            pending = sum(1 for r in all_records if str(r.get('Status', '')).lower().strip() in ['', 'pending'])
            processing = sum(1 for r in all_records if 'processing' in str(r.get('Status', '')).lower())
            completed = sum(1 for r in all_records if 'completed' in str(r.get('Status', '')).lower())
            error = sum(1 for r in all_records if 'error' in str(r.get('Status', '')).lower())
            
            print(f"📊 GOOGLE SHEETS STATS:")
            print(f"   📝 Total rows: {total_rows}")
            print(f"   ⏳ Pending: {pending}")
            print(f"   🔄 Processing: {processing}")
            print(f"   ✅ Completed: {completed}")
            print(f"   ❌ Error: {error}")
            
            if total_rows > 0:
                completion_rate = (completed / total_rows) * 100
                print(f"   📈 Completion rate: {completion_rate:.1f}%")
            
            # Thống kê WordPress (nếu có thể)
            try:
                wp_pub = WordPressPublisher(
                    wp_url=self.config['wp_url'] or "",
                    username=self.config['wp_username'] or "",
                    password=self.config['wp_password'] or ""
                )
                print(f"\n📝 WORDPRESS CONNECTION: ✅ OK")
            except:
                print(f"\n📝 WORDPRESS CONNECTION: ❌ Failed")
            
            # Thống kê AI
            try:
                ai_gen = AIContentGenerator(
                    openai_key=self.config['openai_api_key'] or "",
                    gemini_key=self.config['gemini_api_key'] or ""
                )
                print(f"🤖 AI SERVICES: ✅ OK")
            except:
                print(f"🤖 AI SERVICES: ❌ Failed")
                
        except Exception as e:
            print(f"❌ Stats failed: {str(e)}")
    
    def run(self):
        """Main runner loop"""
        while True:
            try:
                self.show_menu()
                choice = input("👉 Chọn option (0-8): ").strip()
                
                if choice == '0':
                    print("👋 Goodbye!")
                    break
                elif choice == '1':
                    print("🔍 Module tests - choose specific test from menu")
                elif choice == '2':
                    self.test_ai_generator()
                elif choice == '3':
                    self.test_wp_publisher()
                elif choice == '4':
                    self.test_sheets_io()
                elif choice == '5':
                    self.run_single_task()
                elif choice == '6':
                    self.run_batch_processing()
                elif choice == '7':
                    self.interactive_mode()
                elif choice == '8':
                    self.show_system_stats()
                else:
                    print("❌ Invalid choice")
                
                input("\n⏸️  Press Enter to continue...")
                
            except KeyboardInterrupt:
                print("\n👋 Interrupted! Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {str(e)}")
                input("⏸️  Press Enter to continue...")

if __name__ == "__main__":
    runner = SimpleRunner()
    runner.run()
