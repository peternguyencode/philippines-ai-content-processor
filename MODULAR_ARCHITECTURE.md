# SƠ ĐỒ KIẾN TRÚC HỆ THỐNG - MODULAR BREAKDOWN

## 📐 KIẾN TRÚC 5 MODULE ĐỘC LẬP

```
🔄 WORKFLOW ORCHESTRATOR (Module 4)
├── 📊 DATA INPUT/OUTPUT (Module 1)
├── 🤖 AI CONTENT GENERATOR (Module 2)  
├── 📝 WORDPRESS PUBLISHER (Module 3)
└── 🎮 SIMPLE RUNNER (Module 5)
```

---

## 🎯 CHI TIẾT TỪNG MODULE

### MODULE 1: DATA INPUT/OUTPUT (`module_data_io.py`)
**Chức năng**: Chỉ xử lý Google Sheets I/O
```python
class DataInputOutput:
    def get_pending_tasks()      # Đọc tasks từ Sheet
    def update_task_status()     # Update trạng thái
    def save_results()           # Lưu kết quả
    def log_error()             # Ghi log lỗi
```

**🔧 CUSTOMIZATION POINTS:**
- `SHEET_COLUMNS`: Thay đổi mapping cột
- `_connect()`: Đổi Sheet ID hoặc credentials
- `get_pending_tasks()`: Thay đổi logic filter tasks
- `save_results()`: Customize format output

**🛡️ SAFETY**: Module này độc lập hoàn toàn, chỉ cần Sheet ID + credentials

---

### MODULE 2: AI CONTENT GENERATOR (`module_ai_generator.py`)
**Chức năng**: Chỉ tạo content + image bằng AI
```python
class AIContentGenerator:
    def generate_content()       # Tạo nội dung (OpenAI/Gemini)
    def generate_image()         # Tạo ảnh (DALL-E)
    def download_image()         # Download ảnh
    def _generate_with_openai()  # OpenAI implementation
    def _generate_with_gemini()  # Gemini fallback
```

**🔧 CUSTOMIZATION POINTS:**
- `enhanced_prompt`: Thay đổi prompt template
- `generate_content()`: Đổi model (gpt-4, claude, etc.)
- `generate_image()`: Đổi style, size, quality
- `_parse_raw_content()`: Customize JSON parsing

**🛡️ SAFETY**: Module độc lập, chỉ cần API keys. Có fallback tự động.

---

### MODULE 3: WORDPRESS PUBLISHER (`module_wp_publisher.py`)
**Chức năng**: Chỉ đăng bài lên WordPress
```python
class WordPressPublisher:
    def upload_image()           # Upload ảnh lên Media Library
    def create_post()            # Tạo post WordPress
    def publish_complete_post()  # Publish post + image
    def _get_tag_ids()          # Xử lý tags
    def update_post()           # Update post existing
```

**🔧 CUSTOMIZATION POINTS:**
- `create_post()`: Đổi categories, post_status, author
- `upload_image()`: Đổi image format, compression
- `_get_tag_ids()`: Custom tag processing logic
- SEO meta: Customize SEO plugin support

**🛡️ SAFETY**: Module độc lập, chỉ cần WP credentials. Test connection tự động.

---

### MODULE 4: WORKFLOW ORCHESTRATOR (`module_orchestrator.py`)
**Chức năng**: Điều phối toàn bộ workflow
```python
class WorkflowOrchestrator:
    def process_single_task()    # Xử lý 1 task: Input→AI→WP→Output  
    def process_batch()          # Batch processing với threading
    def process_interactive()    # Interactive mode
    def _init_modules()         # Khởi tạo 3 modules core
```

**🔧 CUSTOMIZATION POINTS:**
- `process_single_task()`: Thay đổi workflow steps
- `process_batch()`: Điều chỉnh threading, timeout
- Error handling: Custom retry logic
- Stats tracking: Thêm metrics mới

**🛡️ SAFETY**: Module này là conductor, cần tất cả modules khác hoạt động.

---

### MODULE 5: SIMPLE RUNNER (`simple_runner.py`)
**Chức năng**: Giao diện user-friendly
```python
class SimpleRunner:
    def test_ai_generator()      # Test riêng AI module
    def test_wp_publisher()      # Test riêng WP module  
    def test_sheets_io()         # Test riêng Sheets module
    def run_single_task()        # Chạy 1 task hoàn chỉnh
    def run_batch_processing()   # UI cho batch processing
    def interactive_mode()       # Interactive UI
    def show_system_stats()      # System statistics
```

**🔧 CUSTOMIZATION POINTS:**
- `show_menu()`: Thêm options mới
- Test functions: Custom test scenarios
- `show_system_stats()`: Thêm metrics tracking
- UI/UX: Thay đổi interface style

**🛡️ SAFETY**: Module UI thuần túy, không ảnh hưởng logic core.

---

## 🔄 SƠ ĐỒ LUỒNG DỮ LIỆU

```
INPUT: Google Sheets
    ↓ (Module 1: DataInputOutput)
PENDING TASKS: List[{prompt, row_number, status}]
    ↓ (Module 4: WorkflowOrchestrator)
PROCESSING: For each task
    ↓ (Module 2: AIContentGenerator)
CONTENT: {title, content, meta_title, meta_desc, tags, excerpt}
    ↓ (Module 2: AIContentGenerator)  
IMAGE: DALL-E URL → Downloaded bytes
    ↓ (Module 3: WordPressPublisher)
WORDPRESS: Upload image → Create post → Get URL
    ↓ (Module 1: DataInputOutput)
OUTPUT: Update Sheet với results + status
```

---

## ⚡ CHẠY HỆ THỐNG

### Option 1: Simple Runner (Recommended)
```bash
python simple_runner.py
```
→ Menu interactive, test từng module, chọn chế độ chạy

### Option 2: Direct Module Testing
```bash
# Test từng module riêng
python module_data_io.py        # Test Google Sheets
python module_ai_generator.py   # Test AI generation  
python module_wp_publisher.py   # Test WordPress
python module_orchestrator.py   # Test full workflow
```

### Option 3: Batch Scripts (Windows)
```bash
# Chạy batch processing
run_batch.bat

# Interactive mode  
run_interactive.bat

# Customization tool
customize.bat
```

---

## 🛠️ CUSTOMIZATION GUIDE

### ✅ AN TOÀN - CÓ THỂ SỬA KHÔNG SỢ HỎNG:

1. **Prompt Templates** (module_ai_generator.py):
   ```python
   enhanced_prompt = f"""
   # Thay đổi prompt này để tùy chỉnh style content
   """
   ```

2. **WordPress Settings** (module_wp_publisher.py):
   ```python
   post_data = {
       "status": "publish",     # draft, private, publish
       "categories": [1],       # Đổi category IDs
       "tags": tag_ids,
   }
   ```

3. **Column Mapping** (module_data_io.py):
   ```python
   updates = {
       3: results.get('title', ''),     # Cột C
       4: results.get('content_preview', ''), # Cột D
       # Thêm/đổi cột mapping
   }
   ```

4. **Processing Limits** (module_orchestrator.py):
   ```python
   def process_batch(self, max_workers: int = 2, max_tasks: Optional[int] = None):
       # Đổi default workers, timeout, batch size
   ```

### ⚠️ CẦN THẬN - MODULES CORE:

1. **API Authentication**: Đừng sửa authentication logic
2. **Threading Logic**: Cẩn thận với ThreadPoolExecutor
3. **Error Handling**: Giữ nguyên try-catch structure
4. **Module Initialization**: Đừng đổi `_init_modules()` 

### 🚨 NGUY HIỂM - ĐỪNG SỬA:

1. **Config Loading**: Class Config và environment variables
2. **Google Sheets API**: OAuth và service account setup  
3. **Database Structure**: Sheet columns structure cơ bản
4. **Module Dependencies**: Import relationships giữa modules

---

## 🔍 TROUBLESHOOTING BY MODULE

### Module 1 (Data I/O) Issues:
```
❌ Lỗi: "get_all_records" not found
✅ Fix: Check Google credentials file path
✅ Fix: Verify Sheet ID và permissions
```

### Module 2 (AI Generator) Issues:
```  
❌ Lỗi: OpenAI API key invalid
✅ Fix: Check .env file, OPENAI_API_KEY
✅ Fix: Try Gemini fallback
```

### Module 3 (WordPress) Issues:
```
❌ Lỗi: WordPress auth failed  
✅ Fix: Check Application Password
✅ Fix: Verify WP_URL format (no trailing slash)
```

### Module 4 (Orchestrator) Issues:
```
❌ Lỗi: Module initialization failed
✅ Fix: Test từng module riêng trước
✅ Fix: Check all API keys trong config
```

---

## 📊 MONITORING & ANALYTICS

### Real-time Stats:
- Simple Runner → Option 8: System Statistics
- Live processing progress với tqdm bars
- Thread-safe stats tracking

### Log Files:
- Module errors tự động log vào Google Sheets
- Console output với timestamp
- Success/failure rates tracking

### Performance Metrics:
- Processing time per task
- Success rate percentage  
- Concurrent processing efficiency
- API response times

---

## 🎯 KỊCH BẢN SỬ DỤNG

### Scenario 1: Daily Content Creation
```bash
python simple_runner.py
# Choose option 6: Batch Processing
# Set max_workers=2, max_tasks=5
```

### Scenario 2: Test New Content Style  
```bash
python simple_runner.py  
# Choose option 7: Interactive Mode
# Test prompts directly
```

### Scenario 3: Debug Specific Module
```bash
python simple_runner.py
# Choose option 2-4: Test individual modules
```

### Scenario 4: Custom Automation
```python
from module_orchestrator import WorkflowOrchestrator
orchestrator = WorkflowOrchestrator(config)
stats = orchestrator.process_batch(max_workers=3)
```

---

## 📈 SCALING & OPTIMIZATION

### Performance Tuning:
- Tăng `max_workers` (2-4 optimal)
- Batch size optimization  
- Image generation caching
- WordPress connection pooling

### Resource Management:
- Memory usage monitoring
- API rate limit handling
- Error recovery mechanisms
- Graceful shutdown handling

### Production Deployment:
- Cron job scheduling
- Log rotation
- Health check endpoints
- Backup strategies

---

**🎉 HỆ THỐNG MODULAR HOÀN CHỈNH!**

Mỗi module độc lập, có thể test riêng, customize an toàn, và scale theo nhu cầu. Simple Runner cung cấp interface thân thiện để điều khiển toàn bộ hệ thống mà không cần hiểu chi tiết technical.
