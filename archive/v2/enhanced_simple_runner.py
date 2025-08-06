#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
V2 - ENHANCED SIMPLE RUNNER
Giao diện thân thiện cho hệ thống V2 với advanced features
"""

import sys
import os
import asyncio
from typing import Optional, Dict, Any, List
from datetime import datetime
import json

# Import V2 modules
from enhanced_data_io import EnhancedDataIO, TaskData
from advanced_ai_generator import AdvancedAIGenerator, ContentRequest, ContentType
from smart_wp_publisher import SmartWPPublisher, PostData, MediaItem, MediaType
from intelligent_orchestrator import IntelligentOrchestrator, WorkflowConfig, TaskPriority

# Import config
sys.path.append('..')
from config import Config

class EnhancedSimpleRunner:
    """V2 - Enhanced Simple Runner với advanced features"""
    
    def __init__(self):
        self.config = self._load_config()
        self.workflow_config = WorkflowConfig()
        
        # Initialize orchestrator
        self.orchestrator = None
        
        print("🚀 Enhanced Simple Runner V2")
        print("=" * 40)
        print("✨ Advanced Features:")
        print("   🧠 Intelligent processing")
        print("   📈 Performance analytics")
        print("   🎯 Quality control")
        print("   🔄 Smart retry logic")
        print("   🎨 Advanced image generation")
        print("=" * 40)
    
    def _load_config(self) -> Dict[str, Any]:
        """Load enhanced configuration"""
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
            print("🔧 Please check .env file or environment variables")
            
        return config
    
    def show_main_menu(self):
        """Enhanced main menu"""
        print("\n📋 ENHANCED MAIN MENU V2:")
        print("🔍 TESTING & DIAGNOSTICS:")
        print("   1. 🏥 Full system health check")
        print("   2. 🤖 Test AI Generator V2")
        print("   3. 📝 Test WordPress Publisher V2")
        print("   4. 📊 Test Enhanced Data I/O")
        print("")
        print("🚀 PROCESSING:")
        print("   5. 🎯 Process single task (enhanced)")
        print("   6. 🧠 Intelligent batch processing")
        print("   7. ⚡ Priority processing")
        print("   8. 🎮 Interactive mode (enhanced)")
        print("")
        print("📈 ANALYTICS & CONFIG:")
        print("   9. 📊 System performance analytics")
        print("   10. ⚙️ Configure workflow settings")
        print("   11. 🔍 Task queue management")
        print("   12. 📈 Export analytics report")
        print("")
        print("   0. ❌ Exit")
        print("-" * 50)
    
    def init_orchestrator(self):
        """Initialize orchestrator if not already done"""
        if not self.orchestrator:
            try:
                print("🔄 Initializing Enhanced Orchestrator...")
                self.orchestrator = IntelligentOrchestrator(self.config, self.workflow_config)
                print("✅ Orchestrator ready!")
            except Exception as e:
                print(f"❌ Orchestrator initialization failed: {str(e)}")
                return False
        return True
    
    def system_health_check(self):
        """Comprehensive system health check"""
        print("\n🏥 COMPREHENSIVE HEALTH CHECK V2")
        print("=" * 40)
        
        if not self.init_orchestrator():
            return
        
        try:
            # Check each module
            print("🔍 Checking individual modules...")
            
            # Data I/O health
            data_health = self.orchestrator.data_io.health_check()
            data_stats = self.orchestrator.data_io.get_statistics()
            
            print(f"📊 Data I/O:")
            print(f"   Connection: {'✅' if data_health['connection'] else '❌'}")
            print(f"   Cache hit rate: {data_stats['cache_hit_rate']}")
            print(f"   Total reads: {data_stats['total_reads']}")
            print(f"   Avg response time: {data_stats['avg_response_time']:.2f}s")
            
            # AI Generator health
            ai_stats = self.orchestrator.ai_generator.get_statistics()
            
            print(f"\n🤖 AI Generator:")
            print(f"   Providers available: {ai_stats['providers_available']}")
            print(f"   Success rate: {ai_stats['success_rate']}")
            print(f"   Avg generation time: {ai_stats['avg_generation_time']:.2f}s")
            print(f"   Avg quality score: {ai_stats['avg_quality_score']:.2f}")
            
            # WordPress health
            wp_health = self.orchestrator.wp_publisher.health_check()
            wp_stats = self.orchestrator.wp_publisher.get_statistics()
            
            print(f"\n📝 WordPress Publisher:")
            print(f"   Connection: {'✅' if wp_health['connection'] else '❌'}")
            print(f"   Media upload: {'✅' if wp_health['media_upload'] else '❌'}")
            print(f"   Post creation: {'✅' if wp_health['post_creation'] else '❌'}")
            print(f"   SEO plugin: {wp_stats['seo_plugin']}")
            print(f"   Posts created: {wp_stats['posts_created']}")
            print(f"   Media uploaded: {wp_stats['media_uploaded']}")
            
            # Overall assessment
            all_good = (data_health['connection'] and 
                       ai_stats['providers_available'] > 0 and 
                       wp_health['connection'])
            
            print(f"\n🎯 OVERALL SYSTEM STATUS: {'✅ HEALTHY' if all_good else '⚠️ ISSUES DETECTED'}")
            
            if not all_good:
                print("🔧 Recommended actions:")
                if not data_health['connection']:
                    print("   - Check Google Sheets credentials and permissions")
                if ai_stats['providers_available'] == 0:
                    print("   - Verify AI API keys (OpenAI, Gemini)")
                if not wp_health['connection']:
                    print("   - Check WordPress URL and credentials")
            
        except Exception as e:
            print(f"❌ Health check failed: {str(e)}")
    
    def test_ai_generator_v2(self):
        """Test enhanced AI generator"""
        print("\n🤖 TEST AI GENERATOR V2")
        print("=" * 30)
        
        if not self.init_orchestrator():
            return
        
        try:
            ai_gen = self.orchestrator.ai_generator
            
            # Get user input
            prompt = input("👉 Enter prompt (or press Enter for default): ").strip()
            if not prompt:
                prompt = "Lợi ích của trí tuệ nhân tạo trong marketing digital hiện đại"
            
            # Select content type
            print("\n📝 Content Types:")
            print("1. Blog Post (default)")
            print("2. Product Review")
            print("3. Tutorial")
            print("4. News Article")
            print("5. Marketing Content")
            
            type_choice = input("👉 Select content type (1-5): ").strip()
            
            content_type_map = {
                '1': ContentType.BLOG_POST,
                '2': ContentType.PRODUCT_REVIEW,
                '3': ContentType.TUTORIAL,
                '4': ContentType.NEWS_ARTICLE,
                '5': ContentType.MARKETING
            }
            
            content_type = content_type_map.get(type_choice, ContentType.BLOG_POST)
            
            # Create enhanced request
            request = ContentRequest(
                prompt=prompt,
                content_type=content_type,
                target_words=600,
                keywords=["AI", "marketing", "digital"],
                tone="professional",
                include_image=True
            )
            
            print(f"\n🔄 Generating {content_type.value} content...")
            start_time = datetime.now()
            
            # Generate content
            result = ai_gen.generate_content(request)
            
            generation_time = (datetime.now() - start_time).total_seconds()
            
            print(f"\n✅ Content Generated!")
            print(f"   📝 Title: {result.title}")
            print(f"   📊 Words: {result.word_count}")
            print(f"   ⭐ Quality Score: {result.quality_score:.2f}")
            print(f"   🤖 Provider: {result.provider_used}")
            print(f"   ⏱️  Generation Time: {generation_time:.1f}s")
            print(f"   🏷️  Tags: {', '.join(result.tags)}")
            
            # Show content preview
            show_content = input("\n👀 Show content preview? (y/n): ").lower() == 'y'
            if show_content:
                content_preview = result.content[:500] + "..." if len(result.content) > 500 else result.content
                print(f"\n📄 Content Preview:\n{content_preview}")
            
            # Test image generation
            test_image = input("\n🎨 Test image generation? (y/n): ").lower() == 'y'
            if test_image:
                print("🔄 Generating image...")
                image_url = asyncio.run(ai_gen.generate_image_advanced(
                    title=result.title,
                    content_type=content_type,
                    style="professional"
                ))
                
                if image_url:
                    print(f"✅ Image generated: {image_url}")
                else:
                    print("❌ Image generation failed")
            
        except Exception as e:
            print(f"❌ AI Generator test failed: {str(e)}")
    
    def test_wp_publisher_v2(self):
        """Test enhanced WordPress publisher"""
        print("\n📝 TEST WORDPRESS PUBLISHER V2")
        print("=" * 35)
        
        if not self.init_orchestrator():
            return
        
        try:
            wp_pub = self.orchestrator.wp_publisher
            
            # Test category creation
            test_category = input("👉 Test category name (or Enter for default): ").strip()
            if not test_category:
                test_category = "Test V2 Category"
            
            cat_id = wp_pub.get_or_create_category(test_category)
            print(f"📁 Category '{test_category}' ID: {cat_id}")
            
            # Test tag creation
            test_tag = "test-v2-runner"
            tag_id = wp_pub.get_or_create_tag(test_tag)
            print(f"🏷️  Tag '{test_tag}' ID: {tag_id}")
            
            # Create test post
            create_post = input("\n👉 Create test post? (y/n): ").lower() == 'y'
            if create_post:
                post_data = PostData(
                    title=f"Enhanced Test Post V2 - {datetime.now().strftime('%H:%M:%S')}",
                    content="""
                    <h2>Enhanced WordPress Publisher V2</h2>
                    <p>This test post demonstrates the new features:</p>
                    <ul>
                        <li>🎨 <strong>Image optimization</strong> - automatic compression and resizing</li>
                        <li>🔍 <strong>SEO automation</strong> - meta tags and structured data</li>
                        <li>🏷️  <strong>Smart categorization</strong> - automatic category/tag management</li>
                        <li>📊 <strong>Performance tracking</strong> - detailed analytics</li>
                        <li>🛡️  <strong>Error handling</strong> - robust retry mechanisms</li>
                    </ul>
                    <p>All features are working correctly if you see this post!</p>
                    """,
                    excerpt="Test post showcasing Enhanced WordPress Publisher V2 features",
                    categories=[cat_id] if isinstance(cat_id, int) else [],
                    tags=["test-v2-runner", "enhanced", "wordpress"],
                    meta_title="Enhanced Test Post V2 - SEO Title",
                    meta_desc="Testing the enhanced WordPress publisher with advanced SEO and media features."
                )
                
                print("🔄 Creating enhanced post...")
                post_url = wp_pub.create_post(post_data)
                
                if post_url:
                    print(f"✅ Enhanced post created: {post_url}")
                else:
                    print("❌ Post creation failed")
            
            # Show statistics
            stats = wp_pub.get_statistics()
            print(f"\n📊 Publisher Statistics:")
            for key, value in stats.items():
                if key != 'cache_sizes':
                    print(f"   {key}: {value}")
            
        except Exception as e:
            print(f"❌ WordPress Publisher test failed: {str(e)}")
    
    def test_enhanced_data_io(self):
        """Test enhanced data I/O"""
        print("\n📊 TEST ENHANCED DATA I/O")
        print("=" * 30)
        
        if not self.init_orchestrator():
            return
        
        try:
            data_io = self.orchestrator.data_io
            
            # Test get tasks with filtering
            print("🔍 Testing task retrieval with filters...")
            
            # All pending tasks
            all_tasks = data_io.get_pending_tasks()
            print(f"📋 Total pending tasks: {len(all_tasks)}")
            
            if all_tasks:
                # Show first few tasks
                print("📝 Sample tasks:")
                for i, task in enumerate(all_tasks[:3], 1):
                    print(f"   {i}. Row {task.row_number}: {task.prompt[:50]}...")
                    print(f"      Priority: {task.priority}, Status: {task.status}")
                
                # Test priority filtering
                high_priority = data_io.get_pending_tasks(priority_filter=3)
                print(f"🎯 High priority tasks: {len(high_priority)}")
                
                # Test status update
                test_update = input("\n👉 Test status update on first task? (y/n): ").lower() == 'y'
                if test_update:
                    first_task = all_tasks[0]
                    print(f"🔄 Testing enhanced status update...")
                    
                    data_io.update_task_status(
                        first_task.row_number, 
                        'testing-v2',
                        extra_data={
                            'priority': 2,
                            'tags': 'test,v2,runner'
                        }
                    )
                    
                    print("✅ Enhanced status update completed")
                    
                    # Revert
                    data_io.update_task_status(first_task.row_number, 'pending')
                    print("🔄 Reverted to pending")
            
            # Show cache and performance stats
            stats = data_io.get_statistics()
            print(f"\n📈 Data I/O Performance:")
            for key, value in stats.items():
                print(f"   {key}: {value}")
            
        except Exception as e:
            print(f"❌ Enhanced Data I/O test failed: {str(e)}")
    
    def process_single_task_enhanced(self):
        """Process single task with enhanced features"""
        print("\n🎯 ENHANCED SINGLE TASK PROCESSING")
        print("=" * 40)
        
        if not self.init_orchestrator():
            return
        
        try:
            # Get pending tasks
            pending_tasks = self.orchestrator.data_io.get_pending_tasks()
            
            if not pending_tasks:
                print("ℹ️ No pending tasks found. Creating manual task...")
                prompt = input("👉 Enter prompt: ").strip()
                if not prompt:
                    print("❌ Prompt required")
                    return
                
                # Create temporary task
                temp_task = TaskData(
                    prompt=prompt,
                    row_number=999,
                    status='manual',
                    priority=2,
                    original_data={}
                )
                
                result = self.orchestrator.process_single_task_enhanced(temp_task)
            else:
                print(f"📋 Found {len(pending_tasks)} pending tasks")
                
                # Show task options
                print("📝 Available tasks:")
                for i, task in enumerate(pending_tasks[:5], 1):
                    print(f"   {i}. Row {task.row_number}: {task.prompt[:60]}...")
                    print(f"      Priority: {task.priority}")
                
                choice = input("\n👉 Select task (1-5) or Enter for first: ").strip()
                
                try:
                    task_index = int(choice) - 1 if choice.isdigit() else 0
                    selected_task = pending_tasks[task_index]
                except (ValueError, IndexError):
                    selected_task = pending_tasks[0]
                
                print(f"🎯 Processing: {selected_task.prompt[:100]}...")
                
                confirm = input("👉 Confirm processing? (y/n): ").lower()
                if confirm != 'y':
                    print("❌ Cancelled")
                    return
                
                result = self.orchestrator.process_single_task_enhanced(selected_task)
            
            # Display detailed results
            print(f"\n📊 ENHANCED PROCESSING RESULTS:")
            print(f"   🎯 Task ID: {result.task_id}")
            print(f"   ✅ Success: {result.success}")
            print(f"   ⏱️  Processing Time: {result.processing_time:.1f}s")
            
            if result.success:
                print(f"   ⭐ Content Quality: {result.content_quality:.2f}")
                print(f"   🤖 AI Provider: {result.provider_used}")
                print(f"   🎨 Image Generated: {'Yes' if result.image_generated else 'No'}")
                print(f"   🔗 WordPress URL: {result.wp_url}")
            else:
                print(f"   ❌ Error: {result.error_message}")
                print(f"   🔄 Retry Count: {result.retry_count}")
            
        except Exception as e:
            print(f"❌ Enhanced single task processing failed: {str(e)}")
    
    def intelligent_batch_processing(self):
        """Intelligent batch processing with advanced options"""
        print("\n🧠 INTELLIGENT BATCH PROCESSING")
        print("=" * 35)
        
        if not self.init_orchestrator():
            return
        
        try:
            # Configuration options
            print("⚙️ Batch Configuration:")
            
            max_workers = input(f"👉 Max workers (1-4, current: {self.workflow_config.max_workers}): ").strip()
            if max_workers.isdigit():
                self.workflow_config.max_workers = min(int(max_workers), 4)
            
            max_tasks = input("👉 Max tasks to process (Enter for all): ").strip()
            max_tasks = int(max_tasks) if max_tasks.isdigit() else None
            
            # Priority filter
            print("\n🎯 Priority Filter:")
            print("1. All priorities")
            print("2. High priority only (3+)")
            print("3. Normal priority only (2)")
            print("4. Low priority only (1)")
            
            priority_choice = input("👉 Select priority filter (1-4): ").strip()
            
            priority_map = {
                '2': TaskPriority.HIGH,
                '3': TaskPriority.NORMAL,
                '4': TaskPriority.LOW
            }
            
            priority_filter = priority_map.get(priority_choice)
            
            # Quality threshold
            quality_input = input(f"👉 Quality threshold (0.0-1.0, current: {self.workflow_config.quality_threshold}): ").strip()
            if quality_input:
                try:
                    self.workflow_config.quality_threshold = max(0.0, min(1.0, float(quality_input)))
                except ValueError:
                    pass
            
            # Enable/disable features
            enable_images = input("👉 Enable image generation? (y/n, current: y): ").lower()
            self.workflow_config.enable_image_generation = enable_images != 'n'
            
            print(f"\n🔄 Starting intelligent batch processing...")
            print(f"   👥 Workers: {self.workflow_config.max_workers}")
            print(f"   📊 Max tasks: {max_tasks or 'All'}")
            print(f"   🎯 Priority filter: {priority_filter.name if priority_filter else 'All'}")
            print(f"   ⭐ Quality threshold: {self.workflow_config.quality_threshold}")
            print(f"   🎨 Images: {'Enabled' if self.workflow_config.enable_image_generation else 'Disabled'}")
            
            confirm = input("\n👉 Start processing? (y/n): ").lower()
            if confirm != 'y':
                print("❌ Cancelled")
                return
            
            # Start processing
            report = self.orchestrator.process_batch_intelligent(
                priority_filter=priority_filter,
                max_tasks=max_tasks
            )
            
            # Show detailed report
            print(f"\n🎉 BATCH PROCESSING COMPLETED!")
            
        except Exception as e:
            print(f"❌ Intelligent batch processing failed: {str(e)}")
    
    def configure_workflow_settings(self):
        """Configure workflow settings"""
        print("\n⚙️ WORKFLOW CONFIGURATION")
        print("=" * 30)
        
        print(f"Current settings:")
        print(f"   Max workers: {self.workflow_config.max_workers}")
        print(f"   Max retries: {self.workflow_config.max_retries}")
        print(f"   Timeout per task: {self.workflow_config.timeout_per_task}s")
        print(f"   Quality threshold: {self.workflow_config.quality_threshold}")
        print(f"   Image generation: {self.workflow_config.enable_image_generation}")
        print(f"   SEO optimization: {self.workflow_config.enable_seo_optimization}")
        
        print(f"\n🔧 Modify settings:")
        
        # Max workers
        workers = input("👉 Max workers (1-4): ").strip()
        if workers.isdigit():
            self.workflow_config.max_workers = min(int(workers), 4)
        
        # Max retries
        retries = input("👉 Max retries (0-5): ").strip()
        if retries.isdigit():
            self.workflow_config.max_retries = min(int(retries), 5)
        
        # Timeout
        timeout = input("👉 Timeout per task (60-600s): ").strip()
        if timeout.isdigit():
            self.workflow_config.timeout_per_task = max(60, min(int(timeout), 600))
        
        # Quality threshold
        quality = input("👉 Quality threshold (0.0-1.0): ").strip()
        if quality:
            try:
                self.workflow_config.quality_threshold = max(0.0, min(1.0, float(quality)))
            except ValueError:
                pass
        
        # Boolean settings
        images = input("👉 Enable image generation? (y/n): ").lower()
        if images in ['y', 'n']:
            self.workflow_config.enable_image_generation = images == 'y'
        
        seo = input("👉 Enable SEO optimization? (y/n): ").lower()
        if seo in ['y', 'n']:
            self.workflow_config.enable_seo_optimization = seo == 'y'
        
        print(f"\n✅ Workflow configuration updated!")
        
        # Reinitialize orchestrator with new config
        self.orchestrator = None
    
    def show_performance_analytics(self):
        """Show comprehensive performance analytics"""
        print("\n📈 SYSTEM PERFORMANCE ANALYTICS")
        print("=" * 40)
        
        if not self.init_orchestrator():
            return
        
        try:
            # Get analytics from all modules
            data_stats = self.orchestrator.data_io.get_statistics()
            ai_stats = self.orchestrator.ai_generator.get_statistics()
            wp_stats = self.orchestrator.wp_publisher.get_statistics()
            orch_analytics = self.orchestrator.analytics
            
            print("📊 DATA I/O PERFORMANCE:")
            print(f"   Cache hit rate: {data_stats['cache_hit_rate']}")
            print(f"   Total reads: {data_stats['total_reads']}")
            print(f"   Total writes: {data_stats['total_writes']}")
            print(f"   Avg response time: {data_stats['avg_response_time']:.2f}s")
            print(f"   Errors: {data_stats['errors']}")
            
            print(f"\n🤖 AI GENERATOR PERFORMANCE:")
            print(f"   Success rate: {ai_stats['success_rate']}")
            print(f"   Total requests: {ai_stats['total_requests']}")
            print(f"   Avg generation time: {ai_stats['avg_generation_time']:.2f}s")
            print(f"   Avg quality score: {ai_stats['avg_quality_score']:.2f}")
            print(f"   Cache hits: {ai_stats['cache_hits']}")
            
            if ai_stats['provider_usage']:
                print(f"   Provider usage:")
                for provider, count in ai_stats['provider_usage'].items():
                    print(f"     {provider}: {count}")
            
            print(f"\n📝 WORDPRESS PUBLISHER PERFORMANCE:")
            print(f"   Posts created: {wp_stats['posts_created']}")
            print(f"   Media uploaded: {wp_stats['media_uploaded']}")
            print(f"   Categories created: {wp_stats['categories_created']}")
            print(f"   Tags created: {wp_stats['tags_created']}")
            print(f"   Total upload size: {wp_stats['total_upload_size_mb']}MB")
            print(f"   Avg upload time: {wp_stats['avg_upload_time']:.2f}s")
            print(f"   Errors: {wp_stats['errors']}")
            
            print(f"\n🧠 ORCHESTRATOR ANALYTICS:")
            print(f"   Total tasks: {orch_analytics['total_tasks']}")
            print(f"   Successful: {orch_analytics['successful_tasks']}")
            print(f"   Failed: {orch_analytics['failed_tasks']}")
            print(f"   Avg processing time: {orch_analytics['avg_processing_time']:.2f}s")
            print(f"   Avg quality score: {orch_analytics['avg_quality_score']:.2f}")
            
        except Exception as e:
            print(f"❌ Analytics display failed: {str(e)}")
    
    def run(self):
        """Main enhanced runner loop"""
        while True:
            try:
                self.show_main_menu()
                choice = input("👉 Select option (0-12): ").strip()
                
                if choice == '0':
                    print("👋 Goodbye from Enhanced Runner V2!")
                    break
                elif choice == '1':
                    self.system_health_check()
                elif choice == '2':
                    self.test_ai_generator_v2()
                elif choice == '3':
                    self.test_wp_publisher_v2()
                elif choice == '4':
                    self.test_enhanced_data_io()
                elif choice == '5':
                    self.process_single_task_enhanced()
                elif choice == '6':
                    self.intelligent_batch_processing()
                elif choice == '7':
                    print("🎯 Priority processing - Coming soon!")
                elif choice == '8':
                    print("🎮 Enhanced interactive mode - Coming soon!")
                elif choice == '9':
                    self.show_performance_analytics()
                elif choice == '10':
                    self.configure_workflow_settings()
                elif choice == '11':
                    print("🔍 Task queue management - Coming soon!")
                elif choice == '12':
                    print("📈 Export analytics - Coming soon!")
                else:
                    print("❌ Invalid choice")
                
                input("\n⏸️  Press Enter to continue...")
                
            except KeyboardInterrupt:
                print("\n👋 Interrupted! Goodbye from Enhanced Runner V2!")
                break
            except Exception as e:
                print(f"❌ Error: {str(e)}")
                input("⏸️  Press Enter to continue...")

if __name__ == "__main__":
    runner = EnhancedSimpleRunner()
    runner.run()
