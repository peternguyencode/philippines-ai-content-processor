#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
V2 - MODULE 4: INTELLIGENT WORKFLOW ORCHESTRATOR
Cải tiến: Smart routing, Error recovery, Performance optimization, Analytics
"""

import time
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Union
from concurrent.futures import ThreadPoolExecutor, as_completed, Future
import threading
from dataclasses import dataclass, field
from enum import Enum
import json
import traceback
from collections import defaultdict, deque
import queue

# Import enhanced modules
from enhanced_data_io import EnhancedDataIO, TaskData
from advanced_ai_generator import AdvancedAIGenerator, ContentRequest, ContentResult, ContentType
from smart_wp_publisher import SmartWPPublisher, PostData, MediaItem, MediaType, PostStatus

class TaskPriority(Enum):
    LOW = 1
    NORMAL = 2
    HIGH = 3
    URGENT = 4

class TaskStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRY = "retry"

@dataclass
class ProcessingResult:
    """Enhanced processing result"""
    task_id: str
    success: bool
    wp_url: str = ""
    error_message: str = ""
    processing_time: float = 0.0
    content_quality: float = 0.0
    retry_count: int = 0
    provider_used: str = ""
    image_generated: bool = False
    categories_created: int = 0
    tags_created: int = 0

@dataclass
class WorkflowConfig:
    """Workflow configuration"""
    max_workers: int = 2
    max_retries: int = 2
    retry_delay: float = 5.0
    timeout_per_task: float = 300.0
    batch_size: int = 5
    quality_threshold: float = 0.6
    enable_image_generation: bool = True
    enable_seo_optimization: bool = True
    
class IntelligentOrchestrator:
    """V2 - Intelligent Workflow Orchestrator với advanced features"""
    
    def __init__(self, config: Dict[str, Any], workflow_config: WorkflowConfig = None):
        self.config = config
        self.workflow_config = workflow_config or WorkflowConfig()
        
        # Performance analytics
        self.analytics = {
            'total_tasks': 0,
            'successful_tasks': 0,
            'failed_tasks': 0,
            'retry_tasks': 0,
            'avg_processing_time': 0.0,
            'avg_quality_score': 0.0,
            'provider_performance': defaultdict(list),
            'error_categories': defaultdict(int),
            'processing_timeline': deque(maxlen=100),
            'start_time': None,
            'end_time': None
        }
        
        # Task queue and management
        self._task_queue = queue.PriorityQueue()
        self._active_tasks = {}
        self._completed_tasks = {}
        self._failed_tasks = {}
        
        # Thread management
        self._stats_lock = threading.Lock()
        self._queue_lock = threading.Lock()
        
        # Retry management
        self._retry_queue = queue.Queue()
        self._retry_delays = {
            1: 5.0,   # First retry: 5s
            2: 15.0,  # Second retry: 15s
            3: 60.0   # Third retry: 60s
        }
        
        # Initialize modules
        self._init_enhanced_modules()
    
    def _init_enhanced_modules(self):
        """Initialize enhanced modules với error handling"""
        try:
            # Enhanced Data I/O
            self.data_io = EnhancedDataIO(
                sheet_id=self.config['google_sheet_id'],
                creds_file=self.config['google_creds_file'],
                cache_ttl=300  # 5 minutes cache
            )
            
            # Advanced AI Generator
            self.ai_generator = AdvancedAIGenerator(
                openai_key=self.config['openai_api_key'],
                gemini_key=self.config['gemini_api_key']
            )
            
            # Smart WordPress Publisher
            self.wp_publisher = SmartWPPublisher(
                wp_url=self.config['wp_url'],
                username=self.config['wp_username'],
                password=self.config['wp_password']
            )
            
            print("✅ [ORCHESTRATOR V2] All enhanced modules initialized!")
            
            # Run health checks
            self._run_health_checks()
            
        except Exception as e:
            print(f"❌ [ORCHESTRATOR V2] Module initialization failed: {str(e)}")
            raise e
    
    def _run_health_checks(self):
        """Run comprehensive health checks"""
        print("🏥 [ORCHESTRATOR V2] Running health checks...")
        
        try:
            # Data I/O health check
            data_health = self.data_io.health_check()
            print(f"   📊 Data I/O: {'✅' if data_health['connection'] else '❌'}")
            
            # AI Generator health check
            ai_stats = self.ai_generator.get_statistics()
            print(f"   🤖 AI Generator: ✅ ({ai_stats['providers_available']} providers)")
            
            # WordPress health check
            wp_health = self.wp_publisher.health_check()
            print(f"   📝 WordPress: {'✅' if wp_health['connection'] else '❌'}")
            
        except Exception as e:
            print(f"⚠️ [ORCHESTRATOR V2] Health check warning: {str(e)}")
    
    def process_single_task_enhanced(self, task_data: TaskData) -> ProcessingResult:
        """
        Enhanced single task processing với advanced error handling
        """
        task_id = f"Task-{task_data.row_number}"
        start_time = time.time()
        
        result = ProcessingResult(
            task_id=task_id,
            success=False
        )
        
        print(f"\n🚀 [ORCHESTRATOR V2] Processing {task_id}: {task_data.prompt[:50]}...")
        
        try:
            # Update status to processing
            self.data_io.update_task_status(
                task_data.row_number, 
                TaskStatus.PROCESSING.value,
                {"priority": task_data.priority}
            )
            
            # Create enhanced content request
            content_request = self._create_content_request(task_data)
            
            # Generate AI content
            print(f"🤖 [ORCHESTRATOR V2] {task_id}: Generating content...")
            content_result = self.ai_generator.generate_content(content_request)
            
            if not content_result or content_result.quality_score < self.workflow_config.quality_threshold:
                raise Exception(f"Content quality too low: {content_result.quality_score if content_result else 0:.2f}")
            
            # Generate image if enabled
            image_data = None
            if self.workflow_config.enable_image_generation:
                try:
                    print(f"🎨 [ORCHESTRATOR V2] {task_id}: Generating image...")
                    image_url = await self.ai_generator.generate_image_advanced(
                        title=content_result.title,
                        content_type=content_request.content_type,
                        style="professional"
                    )
                    
                    if image_url:
                        image_data = self.ai_generator.download_image(image_url, f"{task_id}.jpg")
                        result.image_generated = True
                        
                except Exception as img_error:
                    print(f"⚠️ [ORCHESTRATOR V2] {task_id}: Image generation failed: {str(img_error)}")
                    # Continue without image
            
            # Create enhanced post data
            post_data = self._create_post_data(content_result, image_data, task_data)
            
            # Publish to WordPress
            print(f"📝 [ORCHESTRATOR V2] {task_id}: Publishing to WordPress...")
            wp_url = self.wp_publisher.create_post(post_data)
            
            if not wp_url:
                raise Exception("WordPress publishing failed")
            
            # Save results to sheet
            sheet_results = self._create_sheet_results(content_result, wp_url, image_url if image_data else None)
            self.data_io.save_results(task_data.row_number, sheet_results)
            self.data_io.update_task_status(task_data.row_number, TaskStatus.COMPLETED.value)
            
            # Update result
            processing_time = time.time() - start_time
            result.success = True
            result.wp_url = wp_url
            result.processing_time = processing_time
            result.content_quality = content_result.quality_score
            result.provider_used = content_result.provider_used
            
            # Update analytics
            self._update_analytics(task_data, result, content_result)
            
            print(f"✅ [ORCHESTRATOR V2] {task_id} COMPLETED!")
            print(f"   ⏱️  Time: {processing_time:.1f}s")
            print(f"   ⭐ Quality: {content_result.quality_score:.2f}")
            print(f"   🔗 URL: {wp_url}")
            
            return result
            
        except Exception as e:
            processing_time = time.time() - start_time
            error_msg = str(e)
            
            print(f"❌ [ORCHESTRATOR V2] {task_id} FAILED: {error_msg}")
            
            # Log detailed error
            self.data_io.log_error(
                task_data.row_number, 
                f"{error_msg}\n\nTraceback:\n{traceback.format_exc()}", 
                "processing"
            )
            
            result.success = False
            result.error_message = error_msg
            result.processing_time = processing_time
            
            # Update analytics
            self._update_error_analytics(error_msg)
            
            return result
    
    def _create_content_request(self, task_data: TaskData) -> ContentRequest:
        """Create enhanced content request from task data"""
        
        # Detect content type from prompt
        prompt_lower = task_data.prompt.lower()
        content_type = ContentType.BLOG_POST  # Default
        
        if any(word in prompt_lower for word in ['review', 'đánh giá', 'test']):
            content_type = ContentType.PRODUCT_REVIEW
        elif any(word in prompt_lower for word in ['hướng dẫn', 'tutorial', 'cách']):
            content_type = ContentType.TUTORIAL
        elif any(word in prompt_lower for word in ['tin tức', 'news', 'báo']):
            content_type = ContentType.NEWS_ARTICLE
        elif any(word in prompt_lower for word in ['marketing', 'bán', 'sản phẩm']):
            content_type = ContentType.MARKETING
        
        # Extract keywords from prompt
        keywords = self._extract_keywords(task_data.prompt)
        
        return ContentRequest(
            prompt=task_data.prompt,
            content_type=content_type,
            target_words=800,
            language="vi",
            tone="professional",
            keywords=keywords,
            include_image=self.workflow_config.enable_image_generation,
            seo_focus=self.workflow_config.enable_seo_optimization
        )
    
    def _extract_keywords(self, prompt: str) -> List[str]:
        """Extract potential keywords from prompt"""
        # Simple keyword extraction
        words = prompt.lower().split()
        
        # Filter out common words
        stop_words = {'của', 'và', 'cho', 'về', 'trong', 'với', 'từ', 'để', 'có', 'là', 'một'}
        keywords = [word for word in words if len(word) > 3 and word not in stop_words]
        
        return keywords[:5]  # Max 5 keywords
    
    def _create_post_data(self, content_result: ContentResult, image_data: bytes, task_data: TaskData) -> PostData:
        """Create enhanced post data"""
        
        # Create featured media if image exists
        featured_media = None
        if image_data:
            title_slug = content_result.title.lower().replace(' ', '-')[:30]
            featured_media = MediaItem(
                file_data=image_data,
                filename=f"{title_slug}.jpg",
                media_type=MediaType.IMAGE,
                alt_text=content_result.title,
                title=content_result.title
            )
        
        return PostData(
            title=content_result.title,
            content=content_result.content,
            excerpt=content_result.excerpt,
            status=PostStatus.PUBLISHED,
            categories=["AI Generated"],  # Default category
            tags=content_result.tags,
            featured_media=featured_media,
            meta_title=content_result.meta_title,
            meta_desc=content_result.meta_desc,
            custom_meta={
                "ai_generated": "true",
                "generation_provider": content_result.provider_used,
                "quality_score": str(content_result.quality_score),
                "original_prompt": task_data.prompt
            }
        )
    
    def _create_sheet_results(self, content_result: ContentResult, wp_url: str, image_url: str = None) -> Dict[str, Any]:
        """Create results for sheet update"""
        return {
            'title': content_result.title,
            'content_preview': content_result.content[:200] + '...',
            'wp_url': wp_url,
            'image_url': image_url or '',
            'meta_title': content_result.meta_title,
            'meta_desc': content_result.meta_desc,
            'tags': ', '.join(content_result.tags),
            'error_log': ''
        }
    
    def process_batch_intelligent(self, priority_filter: Optional[TaskPriority] = None,
                                max_tasks: Optional[int] = None) -> Dict[str, Any]:
        """
        Intelligent batch processing với priority management
        """
        print("🧠 [ORCHESTRATOR V2] Starting intelligent batch processing...")
        
        # Reset analytics
        self.analytics['start_time'] = datetime.now()
        
        # Get pending tasks with filtering
        pending_tasks = self.data_io.get_pending_tasks(
            priority_filter=priority_filter.value if priority_filter else None,
            status_filter=['pending', '']
        )
        
        if not pending_tasks:
            print("ℹ️ [ORCHESTRATOR V2] No pending tasks found")
            return self._generate_final_report()
        
        # Apply task limit
        if max_tasks and len(pending_tasks) > max_tasks:
            pending_tasks = pending_tasks[:max_tasks]
        
        print(f"📋 [ORCHESTRATOR V2] Processing {len(pending_tasks)} tasks")
        print(f"⚙️  Config: {self.workflow_config.max_workers} workers, timeout {self.workflow_config.timeout_per_task}s")
        
        # Process with intelligent threading
        results = []
        
        with ThreadPoolExecutor(max_workers=self.workflow_config.max_workers) as executor:
            # Submit tasks
            future_to_task = {}
            
            for task in pending_tasks:
                future = executor.submit(self._process_task_with_timeout, task)
                future_to_task[future] = task
            
            # Collect results with progress tracking
            completed = 0
            for future in as_completed(future_to_task, timeout=None):
                task = future_to_task[future]
                completed += 1
                
                try:
                    result = future.result(timeout=10)  # Short timeout for getting result
                    results.append(result)
                    
                    progress = (completed / len(pending_tasks)) * 100
                    print(f"📊 [ORCHESTRATOR V2] Progress: {completed}/{len(pending_tasks)} ({progress:.1f}%)")
                    
                except Exception as e:
                    error_result = ProcessingResult(
                        task_id=f"Task-{task.row_number}",
                        success=False,
                        error_message=f"Executor error: {str(e)}"
                    )
                    results.append(error_result)
                    print(f"❌ [ORCHESTRATOR V2] Executor error for {task.row_number}: {str(e)}")
        
        # Process retry queue if any
        self._process_retry_queue()
        
        # Generate final report
        self.analytics['end_time'] = datetime.now()
        return self._generate_final_report(results)
    
    def _process_task_with_timeout(self, task: TaskData) -> ProcessingResult:
        """Process task với timeout protection"""
        try:
            # Use asyncio for timeout control
            return asyncio.run(
                asyncio.wait_for(
                    self._async_process_single_task(task),
                    timeout=self.workflow_config.timeout_per_task
                )
            )
        except asyncio.TimeoutError:
            print(f"⏰ [ORCHESTRATOR V2] Task {task.row_number} timed out")
            return ProcessingResult(
                task_id=f"Task-{task.row_number}",
                success=False,
                error_message="Task timed out"
            )
        except Exception as e:
            return ProcessingResult(
                task_id=f"Task-{task.row_number}",
                success=False,
                error_message=str(e)
            )
    
    async def _async_process_single_task(self, task: TaskData) -> ProcessingResult:
        """Async wrapper for single task processing"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.process_single_task_enhanced, task)
    
    def _process_retry_queue(self):
        """Process failed tasks in retry queue"""
        retry_count = 0
        
        while not self._retry_queue.empty() and retry_count < 10:  # Max 10 retries per batch
            try:
                task_data, attempt = self._retry_queue.get_nowait()
                
                if attempt <= self.workflow_config.max_retries:
                    delay = self._retry_delays.get(attempt, 60.0)
                    print(f"🔄 [ORCHESTRATOR V2] Retrying task {task_data.row_number} (attempt {attempt}) after {delay}s...")
                    
                    time.sleep(delay)
                    
                    result = self.process_single_task_enhanced(task_data)
                    
                    if not result.success and attempt < self.workflow_config.max_retries:
                        # Queue for another retry
                        self._retry_queue.put((task_data, attempt + 1))
                    
                    retry_count += 1
                    
            except queue.Empty:
                break
            except Exception as e:
                print(f"❌ [ORCHESTRATOR V2] Retry processing error: {str(e)}")
    
    def _update_analytics(self, task_data: TaskData, result: ProcessingResult, content_result: ContentResult):
        """Update performance analytics"""
        with self._stats_lock:
            self.analytics['total_tasks'] += 1
            
            if result.success:
                self.analytics['successful_tasks'] += 1
                
                # Update averages
                total_successful = self.analytics['successful_tasks']
                
                # Processing time
                current_avg_time = self.analytics['avg_processing_time']
                self.analytics['avg_processing_time'] = (
                    (current_avg_time * (total_successful - 1) + result.processing_time) / total_successful
                )
                
                # Quality score
                current_avg_quality = self.analytics['avg_quality_score']
                self.analytics['avg_quality_score'] = (
                    (current_avg_quality * (total_successful - 1) + result.content_quality) / total_successful
                )
                
                # Provider performance
                self.analytics['provider_performance'][result.provider_used].append({
                    'quality': result.content_quality,
                    'time': result.processing_time,
                    'timestamp': datetime.now().isoformat()
                })
            else:
                self.analytics['failed_tasks'] += 1
            
            # Timeline tracking
            self.analytics['processing_timeline'].append({
                'task_id': result.task_id,
                'success': result.success,
                'timestamp': datetime.now().isoformat(),
                'processing_time': result.processing_time
            })
    
    def _update_error_analytics(self, error_message: str):
        """Update error analytics"""
        with self._stats_lock:
            # Categorize errors
            error_lower = error_message.lower()
            
            if 'timeout' in error_lower:
                self.analytics['error_categories']['timeout'] += 1
            elif 'api' in error_lower or 'key' in error_lower:
                self.analytics['error_categories']['api_error'] += 1
            elif 'quality' in error_lower:
                self.analytics['error_categories']['quality_issue'] += 1
            elif 'wordpress' in error_lower or 'publish' in error_lower:
                self.analytics['error_categories']['wordpress_error'] += 1
            elif 'sheets' in error_lower or 'google' in error_lower:
                self.analytics['error_categories']['sheets_error'] += 1
            else:
                self.analytics['error_categories']['unknown'] += 1
    
    def _generate_final_report(self, results: List[ProcessingResult] = None) -> Dict[str, Any]:
        """Generate comprehensive final report"""
        if results:
            for result in results:
                if result.success:
                    self.analytics['successful_tasks'] += 1
                else:
                    self.analytics['failed_tasks'] += 1
        
        total_time = 0
        if self.analytics['start_time'] and self.analytics['end_time']:
            total_time = (self.analytics['end_time'] - self.analytics['start_time']).total_seconds()
        
        success_rate = 0
        if self.analytics['total_tasks'] > 0:
            success_rate = (self.analytics['successful_tasks'] / self.analytics['total_tasks']) * 100
        
        # Generate provider performance summary
        provider_summary = {}
        for provider, performances in self.analytics['provider_performance'].items():
            if performances:
                avg_quality = sum(p['quality'] for p in performances) / len(performances)
                avg_time = sum(p['time'] for p in performances) / len(performances)
                provider_summary[provider] = {
                    'tasks_completed': len(performances),
                    'avg_quality': f"{avg_quality:.2f}",
                    'avg_time': f"{avg_time:.1f}s"
                }
        
        report = {
            'summary': {
                'total_tasks': self.analytics['total_tasks'],
                'successful': self.analytics['successful_tasks'],
                'failed': self.analytics['failed_tasks'],
                'success_rate': f"{success_rate:.1f}%",
                'total_time': f"{total_time:.1f}s",
                'avg_processing_time': f"{self.analytics['avg_processing_time']:.1f}s",
                'avg_quality_score': f"{self.analytics['avg_quality_score']:.2f}"
            },
            'provider_performance': provider_summary,
            'error_breakdown': dict(self.analytics['error_categories']),
            'timeline': list(self.analytics['processing_timeline']),
            'module_stats': {
                'data_io': self.data_io.get_statistics(),
                'ai_generator': self.ai_generator.get_statistics(),
                'wp_publisher': self.wp_publisher.get_statistics()
            }
        }
        
        self._print_final_report(report)
        return report
    
    def _print_final_report(self, report: Dict[str, Any]):
        """Print formatted final report"""
        print(f"\n📊 [ORCHESTRATOR V2] FINAL REPORT")
        print("=" * 50)
        
        summary = report['summary']
        print(f"📈 SUMMARY:")
        print(f"   📝 Total Tasks: {summary['total_tasks']}")
        print(f"   ✅ Successful: {summary['successful']}")
        print(f"   ❌ Failed: {summary['failed']}")
        print(f"   📊 Success Rate: {summary['success_rate']}")
        print(f"   ⏱️  Total Time: {summary['total_time']}")
        print(f"   ⚡ Avg Processing: {summary['avg_processing_time']}")
        print(f"   ⭐ Avg Quality: {summary['avg_quality_score']}")
        
        if report['provider_performance']:
            print(f"\n🤖 PROVIDER PERFORMANCE:")
            for provider, stats in report['provider_performance'].items():
                print(f"   {provider}: {stats['tasks_completed']} tasks, Quality {stats['avg_quality']}, Time {stats['avg_time']}")
        
        if report['error_breakdown']:
            print(f"\n🚨 ERROR BREAKDOWN:")
            for error_type, count in report['error_breakdown'].items():
                print(f"   {error_type}: {count}")

# Test V2 module
if __name__ == "__main__":
    import sys
    sys.path.append('..')
    from config import Config
    
    print("🧪 TESTING INTELLIGENT ORCHESTRATOR V2")
    print("=" * 45)
    
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
    
    # Test workflow config
    workflow_config = WorkflowConfig(
        max_workers=1,
        max_retries=1,
        timeout_per_task=120.0,
        enable_image_generation=True,
        quality_threshold=0.5
    )
    
    # Test orchestrator
    orchestrator = IntelligentOrchestrator(test_config, workflow_config)
    
    # Test single task (if available)
    pending_tasks = orchestrator.data_io.get_pending_tasks(status_filter=['pending', ''])
    
    if pending_tasks:
        print(f"🎯 Testing single task processing...")
        first_task = pending_tasks[0]
        result = orchestrator.process_single_task_enhanced(first_task)
        
        print(f"\n📊 Single Task Result:")
        print(f"   Success: {result.success}")
        print(f"   Quality: {result.content_quality}")
        print(f"   Time: {result.processing_time:.1f}s")
        if result.wp_url:
            print(f"   URL: {result.wp_url}")
    else:
        print("ℹ️ No pending tasks for testing")
    
    # Show analytics
    print(f"\n📈 Analytics Summary:")
    analytics = orchestrator.analytics
    print(f"   Total: {analytics['total_tasks']}")
    print(f"   Success: {analytics['successful_tasks']}")
    print(f"   Failed: {analytics['failed_tasks']}")
