#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
V2 - MODULE 1: ENHANCED DATA INPUT/OUTPUT
Cải tiến: Performance, Error handling, Flexible mapping, Caching
"""

import gspread
import time
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any, Tuple
from google.oauth2.service_account import Credentials
from dataclasses import dataclass
import threading
from pathlib import Path

@dataclass
class TaskData:
    """Structured task data"""
    prompt: str
    row_number: int
    status: str
    original_data: Dict[str, Any]
    priority: int = 1
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class EnhancedDataIO:
    """V2 - Enhanced Google Sheets I/O với caching và performance optimization"""
    
    def __init__(self, sheet_id: str, creds_file: str, cache_ttl: int = 300):
        self.sheet_id = sheet_id
        self.creds_file = creds_file
        self.cache_ttl = cache_ttl
        
        # Caching system
        self._cache = {}
        self._cache_timestamps = {}
        self._cache_lock = threading.Lock()
        
        # Connection objects
        self.gc = None
        self.sheet = None
        self.worksheet = None
        
        # Column mapping - Flexible và configurable
        self.column_mapping = {
            'prompt': 1,        # A
            'status': 2,        # B  
            'title': 3,         # C
            'content_preview': 4, # D
            'wp_url': 5,        # E
            'image_url': 6,     # F
            'meta_title': 7,    # G
            'meta_desc': 8,     # H
            'created_at': 9,    # I
            'error_log': 10,    # J
            'priority': 11,     # K (NEW)
            'tags': 12,         # L (NEW)
            'category': 13      # M (NEW)
        }
        
        # Performance stats
        self.stats = {
            'total_reads': 0,
            'total_writes': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'errors': 0,
            'avg_response_time': 0
        }
        
        self._connect()
    
    def _connect(self):
        """Enhanced connection với retry logic"""
        max_retries = 3
        retry_delay = 1
        
        for attempt in range(max_retries):
            try:
                scope = [
                    'https://spreadsheets.google.com/feeds',
                    'https://www.googleapis.com/auth/drive'
                ]
                
                if not Path(self.creds_file).exists():
                    raise FileNotFoundError(f"Credentials file not found: {self.creds_file}")
                
                creds = Credentials.from_service_account_file(
                    self.creds_file, scopes=scope
                )
                
                self.gc = gspread.authorize(creds)
                self.sheet = self.gc.open_by_key(self.sheet_id)
                self.worksheet = self.sheet.sheet1
                
                # Test connection
                self.worksheet.get('A1')
                
                print(f"✅ [DATA IO V2] Connected successfully (attempt {attempt + 1})")
                return
                
            except Exception as e:
                self.stats['errors'] += 1
                if attempt == max_retries - 1:
                    print(f"❌ [DATA IO V2] Connection failed after {max_retries} attempts: {str(e)}")
                    raise e
                else:
                    print(f"⚠️ [DATA IO V2] Connection attempt {attempt + 1} failed, retrying in {retry_delay}s...")
                    time.sleep(retry_delay)
                    retry_delay *= 2
    
    def _is_cache_valid(self, cache_key: str) -> bool:
        """Check if cache is still valid"""
        if cache_key not in self._cache_timestamps:
            return False
        
        elapsed = (datetime.now() - self._cache_timestamps[cache_key]).total_seconds()
        return elapsed < self.cache_ttl
    
    def _get_from_cache(self, cache_key: str) -> Optional[Any]:
        """Get data from cache if valid"""
        with self._cache_lock:
            if self._is_cache_valid(cache_key):
                self.stats['cache_hits'] += 1
                return self._cache[cache_key]
            
            self.stats['cache_misses'] += 1
            return None
    
    def _set_cache(self, cache_key: str, data: Any):
        """Set data to cache"""
        with self._cache_lock:
            self._cache[cache_key] = data
            self._cache_timestamps[cache_key] = datetime.now()
    
    def get_pending_tasks(self, priority_filter: Optional[int] = None, 
                         status_filter: List[str] = None) -> List[TaskData]:
        """
        Enhanced get pending tasks với filtering và caching
        """
        start_time = time.time()
        cache_key = f"pending_tasks_{priority_filter}_{status_filter}"
        
        # Try cache first
        cached_data = self._get_from_cache(cache_key)
        if cached_data is not None:
            print(f"📋 [DATA IO V2] Loaded {len(cached_data)} tasks from cache")
            return cached_data
        
        try:
            all_records = self.worksheet.get_all_records()
            self.stats['total_reads'] += 1
            
            if not status_filter:
                status_filter = ['', 'pending']
            
            pending_tasks = []
            
            for i, record in enumerate(all_records, 2):  # Start from row 2
                status = str(record.get('Status', '')).lower().strip()
                prompt = str(record.get('Prompt', '')).strip()
                priority = int(record.get('Priority', 1)) if str(record.get('Priority', '')).isdigit() else 1
                
                # Apply filters
                if not prompt:
                    continue
                    
                if status not in [s.lower() for s in status_filter]:
                    continue
                    
                if priority_filter is not None and priority != priority_filter:
                    continue
                
                task = TaskData(
                    prompt=prompt,
                    row_number=i,
                    status=status,
                    priority=priority,
                    original_data=record,
                    created_at=self._parse_datetime(record.get('Created', '')),
                    updated_at=datetime.now()
                )
                
                pending_tasks.append(task)
            
            # Sort by priority (higher first), then by row number
            pending_tasks.sort(key=lambda x: (-x.priority, x.row_number))
            
            # Cache results
            self._set_cache(cache_key, pending_tasks)
            
            response_time = time.time() - start_time
            self._update_avg_response_time(response_time)
            
            print(f"📋 [DATA IO V2] Found {len(pending_tasks)} pending tasks (filtered)")
            return pending_tasks
            
        except Exception as e:
            self.stats['errors'] += 1
            print(f"❌ [DATA IO V2] Error getting tasks: {str(e)}")
            return []
    
    def _parse_datetime(self, date_str: str) -> Optional[datetime]:
        """Parse datetime string with multiple formats"""
        if not date_str:
            return None
            
        formats = [
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d",
            "%d/%m/%Y %H:%M:%S",
            "%d/%m/%Y"
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(str(date_str), fmt)
            except ValueError:
                continue
        
        return None
    
    def update_task_status(self, row_number: int, status: str, 
                          extra_data: Optional[Dict[str, Any]] = None):
        """Enhanced status update với batch operations"""
        try:
            updates = [
                {
                    'range': f'B{row_number}',  # Status column
                    'values': [[status]]
                }
            ]
            
            # Add timestamp
            updates.append({
                'range': f'I{row_number}',  # Created_at column
                'values': [[datetime.now().strftime("%Y-%m-%d %H:%M:%S")]]
            })
            
            # Add extra data if provided
            if extra_data:
                for key, value in extra_data.items():
                    if key in self.column_mapping:
                        col_letter = self._get_column_letter(self.column_mapping[key])
                        updates.append({
                            'range': f'{col_letter}{row_number}',
                            'values': [[str(value)]]
                        })
            
            # Batch update
            self.worksheet.batch_update(updates)
            self.stats['total_writes'] += len(updates)
            
            # Clear cache
            self._clear_cache()
            
            print(f"✅ [DATA IO V2] Updated row {row_number}: {status}")
            time.sleep(0.1)  # Reduced delay
            
        except Exception as e:
            self.stats['errors'] += 1
            print(f"❌ [DATA IO V2] Error updating status: {str(e)}")
    
    def save_results(self, row_number: int, results: Dict[str, Any], 
                    batch_mode: bool = False):
        """
        Enhanced save results với batch operations và validation
        """
        try:
            updates = []
            
            # Map results to columns
            result_mapping = {
                'title': 'title',
                'content_preview': 'content_preview', 
                'wp_url': 'wp_url',
                'image_url': 'image_url',
                'meta_title': 'meta_title',
                'meta_desc': 'meta_desc',
                'error_log': 'error_log',
                'tags': 'tags',
                'category': 'category'
            }
            
            for result_key, column_key in result_mapping.items():
                if result_key in results and results[result_key]:
                    value = results[result_key]
                    
                    # Special handling for different data types
                    if isinstance(value, list):
                        value = ', '.join(str(v) for v in value)
                    elif isinstance(value, dict):
                        value = json.dumps(value, ensure_ascii=False)
                    
                    # Truncate long values
                    if len(str(value)) > 1000 and result_key == 'content_preview':
                        value = str(value)[:997] + '...'
                    
                    col_num = self.column_mapping.get(column_key)
                    if col_num:
                        col_letter = self._get_column_letter(col_num)
                        updates.append({
                            'range': f'{col_letter}{row_number}',
                            'values': [[str(value)]]
                        })
            
            # Add timestamp
            col_letter = self._get_column_letter(self.column_mapping['created_at'])
            updates.append({
                'range': f'{col_letter}{row_number}',
                'values': [[datetime.now().strftime("%Y-%m-%d %H:%M:%S")]]
            })
            
            if updates:
                if batch_mode:
                    return updates  # Return for batch processing
                else:
                    self.worksheet.batch_update(updates)
                    self.stats['total_writes'] += len(updates)
                    self._clear_cache()
                    
                    print(f"✅ [DATA IO V2] Saved results for row {row_number}")
            
        except Exception as e:
            self.stats['errors'] += 1
            print(f"❌ [DATA IO V2] Error saving results: {str(e)}")
            return None
    
    def batch_save_results(self, batch_data: List[Tuple[int, Dict[str, Any]]]):
        """Batch save multiple results efficiently"""
        try:
            all_updates = []
            
            for row_number, results in batch_data:
                updates = self.save_results(row_number, results, batch_mode=True)
                if updates:
                    all_updates.extend(updates)
            
            if all_updates:
                # Split into chunks of 100 (Google Sheets limit)
                chunk_size = 100
                for i in range(0, len(all_updates), chunk_size):
                    chunk = all_updates[i:i + chunk_size]
                    self.worksheet.batch_update(chunk)
                    time.sleep(0.1)
                
                self.stats['total_writes'] += len(all_updates)
                self._clear_cache()
                
                print(f"✅ [DATA IO V2] Batch saved {len(batch_data)} results")
            
        except Exception as e:
            self.stats['errors'] += 1
            print(f"❌ [DATA IO V2] Batch save error: {str(e)}")
    
    def _get_column_letter(self, col_num: int) -> str:
        """Convert column number to letter (1=A, 2=B, etc.)"""
        result = ""
        while col_num > 0:
            col_num -= 1
            result = chr(col_num % 26 + ord('A')) + result
            col_num //= 26
        return result
    
    def _clear_cache(self):
        """Clear all cache"""
        with self._cache_lock:
            self._cache.clear()
            self._cache_timestamps.clear()
    
    def _update_avg_response_time(self, response_time: float):
        """Update average response time"""
        if self.stats['avg_response_time'] == 0:
            self.stats['avg_response_time'] = response_time
        else:
            # Moving average
            self.stats['avg_response_time'] = (
                self.stats['avg_response_time'] * 0.8 + response_time * 0.2
            )
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get performance statistics"""
        cache_hit_rate = 0
        if self.stats['cache_hits'] + self.stats['cache_misses'] > 0:
            cache_hit_rate = self.stats['cache_hits'] / (
                self.stats['cache_hits'] + self.stats['cache_misses']
            ) * 100
        
        return {
            **self.stats,
            'cache_hit_rate': f"{cache_hit_rate:.1f}%",
            'cache_size': len(self._cache),
            'connection_status': 'Connected' if self.worksheet else 'Disconnected'
        }
    
    def log_error(self, row_number: int, error_message: str, error_type: str = 'general'):
        """Enhanced error logging with categorization"""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            detailed_error = f"[{timestamp}] {error_type.upper()}: {error_message}"
            
            # Update status and error log
            self.update_task_status(row_number, 'error', {
                'error_log': detailed_error
            })
            
            print(f"❌ [DATA IO V2] Logged {error_type} error for row {row_number}: {error_message}")
            
        except Exception as e:
            print(f"❌ [DATA IO V2] Error logging failed: {str(e)}")
    
    def health_check(self) -> Dict[str, Any]:
        """Comprehensive health check"""
        health_status = {
            'connection': False,
            'read_test': False,
            'write_test': False,
            'response_time': 0,
            'errors': []
        }
        
        try:
            # Test connection
            start_time = time.time()
            test_data = self.worksheet.get('A1')
            health_status['connection'] = True
            health_status['read_test'] = True
            health_status['response_time'] = time.time() - start_time
            
        except Exception as e:
            health_status['errors'].append(f"Connection/Read test failed: {str(e)}")
        
        return health_status

# Test V2 module
if __name__ == "__main__":
    import sys
    sys.path.append('..')
    from config import Config
    
    print("🧪 TESTING DATA IO V2")
    print("=" * 30)
    
    # Test enhanced Data I/O
    data_io = EnhancedDataIO(
        sheet_id=Config.GOOGLE_SHEET_ID or "",
        creds_file=Config.GOOGLE_CREDS_FILE or "",
        cache_ttl=60  # 1 minute cache
    )
    
    # Test health check
    health = data_io.health_check()
    print(f"🏥 Health Check: {health}")
    
    # Test get tasks with filtering
    tasks = data_io.get_pending_tasks(status_filter=['pending', ''])
    print(f"📋 Found {len(tasks)} tasks")
    
    if tasks:
        # Test first task
        first_task = tasks[0]
        print(f"🎯 First task: {first_task.prompt[:50]}...")
        print(f"   Priority: {first_task.priority}")
        print(f"   Row: {first_task.row_number}")
    
    # Show statistics
    stats = data_io.get_statistics()
    print(f"\n📊 Statistics:")
    for key, value in stats.items():
        print(f"   {key}: {value}")
