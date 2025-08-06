# 🤖 AI Content Processing Workflow - Sơ Đồ Chi Tiết

## 📊 **Tổng Quan Quy Trình**

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   posts table   │ →  │  AI Processing   │ →  │  posts_ai table │
│   (86 posts)    │    │   (OpenAI API)   │    │  (processed)    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

---

## 🔄 **Chi Tiết Workflow - Batch Processing**

### **PHASE 1: INITIALIZATION & SETUP**
```
┌─────────────────────────────────────────────────────────────────┐
│                     🚀 KHỞI TẠO SYSTEM                         │
├─────────────────────────────────────────────────────────────────┤
│ 1. Setup Logging                                               │
│    ├── File: ai_processing_YYYYMMDD_HHMMSS.log                │
│    └── Console output với timestamps                           │
│                                                                 │
│ 2. MySQL Connection                                             │
│    ├── Host: localhost:3308                                    │
│    ├── Database: mydb                                           │
│    └── Auto-create posts_ai table                              │
│                                                                 │
│ 3. OpenAI API Setup                                             │
│    ├── API Key validation                                       │
│    ├── Model: gpt-3.5-turbo                                    │
│    └── Rate limiting preparation                                │
└─────────────────────────────────────────────────────────────────┘
```

### **PHASE 2: DATA DISCOVERY**
```
┌─────────────────────────────────────────────────────────────────┐
│                   🔍 TÌM POSTS CẦN XỬ LÝ                       │
├─────────────────────────────────────────────────────────────────┤
│ Query: SELECT p.* FROM posts p                                  │
│        LEFT JOIN posts_ai pa ON p.id = pa.post_id              │
│        WHERE pa.post_id IS NULL                                 │
│        ORDER BY p.created_date DESC                             │
│        [LIMIT if specified]                                     │
│                                                                 │
│ Result: List of unprocessed posts                               │
│ ├── Current: 85 posts chưa xử lý                               │
│ ├── 1 post đã xử lý (test)                                     │
│ └── Apply limit nếu batch size được chỉ định                   │
└─────────────────────────────────────────────────────────────────┘
```

### **PHASE 3: BATCH PROCESSING LOOP**
```
┌─────────────────────────────────────────────────────────────────┐
│              🔄 VÒNG LẶP XỬ LÝ TỪNG POST                       │
├─────────────────────────────────────────────────────────────────┤
│ FOR each post in unprocessed_posts:                            │
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │            📝 XỬ LÝ 1 POST                              │   │
│   ├─────────────────────────────────────────────────────────┤   │
│   │ 1. Log: "🔄 Xử lý Post ID {id}: {title[:50]}..."       │   │
│   │                                                         │   │
│   │ 2. Update Status = 'processing'                         │   │
│   │    INSERT INTO posts_ai (post_id, processing_status)    │   │
│   │    VALUES ({id}, 'processing')                          │   │
│   │                                                         │   │
│   │ 3. 🤖 AI PROCESSING                                     │   │
│   │    ├── Prepare prompt (SEO-focused)                    │   │
│   │    ├── Call OpenAI API                                 │   │
│   │    ├── Parse JSON response                             │   │
│   │    └── Fallback if AI fails                           │   │
│   │                                                         │   │
│   │ 4. 💾 SAVE RESULT                                      │   │
│   │    INSERT/UPDATE posts_ai SET:                         │   │
│   │    ├── ai_content = processed_content                  │   │
│   │    ├── meta_title = seo_title                          │   │
│   │    ├── meta_description = seo_desc                     │   │
│   │    ├── processing_status = 'completed'                 │   │
│   │    └── updated_date = NOW()                            │   │
│   │                                                         │   │
│   │ 5. 📊 UPDATE STATS                                     │   │
│   │    ├── total_processed++                               │   │
│   │    ├── success++ OR errors++                           │   │
│   │    └── Update progress bar                             │   │
│   │                                                         │   │
│   │ 6. ⏱️ DELAY                                            │   │
│   │    time.sleep(delay_seconds)                           │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│ Exception Handling:                                             │
│ ├── KeyboardInterrupt: Graceful shutdown                       │
│ ├── API Errors: Log + continue với fallback                    │
│ └── Database Errors: Log + mark as error                       │
└─────────────────────────────────────────────────────────────────┘
```

### **PHASE 4: AI PROCESSING DETAILS**
```
┌─────────────────────────────────────────────────────────────────┐
│                  🧠 CHI TIẾT AI PROCESSING                      │
├─────────────────────────────────────────────────────────────────┤
│ Input: original_content, title, category                       │
│                                                                 │
│ 1. 📝 PROMPT ENGINEERING                                        │
│    ┌─────────────────────────────────────────────────────────┐ │
│    │ System: "Bạn là chuyên gia content marketing và SEO"   │ │  
│    │                                                         │ │
│    │ User Prompt:                                            │ │
│    │ "Viết lại bài viết để:                                 │ │
│    │  1. Tối ưu SEO và thu hút người đọc                    │ │
│    │  2. Giữ nguyên ý nghĩa chính                           │ │
│    │  3. Thêm keywords tự nhiên                              │ │
│    │  4. Cấu trúc rõ ràng                                   │ │
│    │                                                         │ │
│    │ Content: {original_content[:2000]}                      │ │
│    │                                                         │ │
│    │ Output JSON format:                                     │ │
│    │ {                                                       │ │
│    │   'ai_content': 'Rewritten content',                   │ │
│    │   'meta_title': 'SEO title (60-70 chars)',             │ │
│    │   'meta_description': 'SEO desc (150-160 chars)',      │ │
│    │   'suggested_tags': 'tag1, tag2, tag3',                │ │
│    │   'notes': 'Processing notes'                           │ │
│    │ }"                                                      │ │
│    └─────────────────────────────────────────────────────────┘ │
│                                                                 │
│ 2. 🌐 OPENAI API CALL                                          │
│    ┌─────────────────────────────────────────────────────────┐ │
│    │ client = OpenAI(api_key=Config.OPENAI_API_KEY)         │ │
│    │                                                         │ │
│    │ response = client.chat.completions.create(              │ │
│    │     model="gpt-3.5-turbo",                             │ │
│    │     messages=messages,                                  │ │
│    │     max_tokens=2000,                                    │ │
│    │     temperature=0.7                                     │ │
│    │ )                                                       │ │
│    └─────────────────────────────────────────────────────────┘ │
│                                                                 │
│ 3. 📊 RESPONSE PROCESSING                                       │
│    ┌─────────────────────────────────────────────────────────┐ │
│    │ Try: JSON.parse(response.content)                      │ │
│    │                                                         │ │
│    │ Success: Extract all fields                             │ │
│    │ ├── ai_content                                          │ │
│    │ ├── meta_title                                          │ │
│    │ ├── meta_description                                    │ │
│    │ ├── suggested_tags                                      │ │
│    │ └── notes                                               │ │
│    │                                                         │ │
│    │ Fallback (if JSON invalid):                            │ │
│    │ ├── ai_content = raw_response                           │ │
│    │ ├── meta_title = original_title[:70]                    │ │
│    │ ├── meta_description = original_content[:160]          │ │
│    │ └── notes = "JSON parse failed"                        │ │
│    └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### **PHASE 5: DATABASE OPERATIONS**
```
┌─────────────────────────────────────────────────────────────────┐
│                    💾 DATABASE OPERATIONS                       │
├─────────────────────────────────────────────────────────────────┤
│ 1. 🔄 STATUS TRACKING                                           │
│    ┌─────────────────────────────────────────────────────────┐   │
│    │ Processing Start:                                       │   │
│    │ INSERT INTO posts_ai (post_id, processing_status)       │   │
│    │ VALUES ({post_id}, 'processing')                        │   │
│    │ ON DUPLICATE KEY UPDATE                                 │   │
│    │     processing_status = 'processing',                   │   │
│    │     updated_date = CURRENT_TIMESTAMP                    │   │
│    └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│ 2. 📝 SAVE AI RESULT                                            │
│    ┌─────────────────────────────────────────────────────────┐   │
│    │ INSERT INTO posts_ai (                                  │   │
│    │     post_id, title, ai_content, meta_title,             │   │
│    │     meta_description, tags, category, ai_model,         │   │
│    │     ai_notes, processing_status                          │   │
│    │ ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)       │   │
│    │ ON DUPLICATE KEY UPDATE                                 │   │
│    │     ai_content = VALUES(ai_content),                    │   │
│    │     meta_title = VALUES(meta_title),                    │   │
│    │     meta_description = VALUES(meta_description),        │   │
│    │     tags = VALUES(tags),                                │   │
│    │     processing_status = 'completed',                    │   │
│    │     updated_date = CURRENT_TIMESTAMP                    │   │
│    └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│ 3. 🚨 ERROR HANDLING                                            │
│    ┌─────────────────────────────────────────────────────────┐   │
│    │ On Error:                                               │   │
│    │ UPDATE posts_ai SET                                     │   │
│    │     processing_status = 'error',                        │   │
│    │     ai_notes = CONCAT(ai_notes, ' | {error_msg}'),      │   │
│    │     updated_date = CURRENT_TIMESTAMP                    │   │
│    │ WHERE post_id = {post_id}                               │   │
│    └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### **PHASE 6: PROGRESS MONITORING**
```
┌─────────────────────────────────────────────────────────────────┐
│                   📊 PROGRESS MONITORING                        │
├─────────────────────────────────────────────────────────────────┤
│ 1. 📈 REAL-TIME PROGRESS BAR                                    │
│    ┌─────────────────────────────────────────────────────────┐   │
│    │ tqdm Progress Bar:                                      │   │
│    │ AI Processing: 60%|████████▌     | 12/20 [02:45<01:50]  │   │
│    │                                   ↑      ↑     ↑        │   │
│    │                              current  total  ETA        │   │
│    │                                                         │   │
│    │ Status Display:                                         │   │
│    │ ├── ✅ Post 87 (success)                               │   │
│    │ ├── ✅ Post 86 (success)                               │   │
│    │ └── ❌ Post 85 (error)                                 │   │
│    └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│ 2. 📝 DETAILED LOGGING                                          │
│    ┌─────────────────────────────────────────────────────────┐   │
│    │ Console + File Log:                                     │   │
│    │ 2025-08-05 20:22:15 - INFO - 🔄 Xử lý Post ID 87...    │   │
│    │ 2025-08-05 20:22:19 - INFO - ✅ AI xử lý thành công    │   │
│    │ 2025-08-05 20:22:19 - INFO - ✅ Lưu AI result thành công│   │
│    │ 2025-08-05 20:22:19 - INFO - 🎉 Hoàn thành Post ID 87  │   │
│    └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│ 3. 📊 STATISTICS TRACKING                                       │
│    ┌─────────────────────────────────────────────────────────┐   │
│    │ Live Stats Update:                                      │   │
│    │ {                                                       │   │
│    │   'total_processed': 12,                                │   │
│    │   'success': 11,                                        │   │
│    │   'errors': 1,                                          │   │
│    │   'skipped': 0                                          │   │
│    │ }                                                       │   │
│    └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### **PHASE 7: COMPLETION & REPORTING**
```
┌─────────────────────────────────────────────────────────────────┐
│                    🎯 KẾT QUẢ CUỐI CÙNG                        │
├─────────────────────────────────────────────────────────────────┤
│ 📈 FINAL REPORT:                                                │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ KẾT QUẢ AI PROCESSING:                                      │ │
│ │    Tổng số posts xử lý: 20                                 │ │
│ │    Thành công: 18                                          │ │
│ │    Lỗi: 2                                                  │ │
│ │    Thời gian: 85.42 giây                                   │ │
│ │    Tốc độ: 0.23 posts/giây                                 │ │
│ │                                                            │ │
│ │ 📊 Database Status:                                        │ │
│ │    posts table: 86 records                                 │ │
│ │    posts_ai table: 19 records (18 completed, 1 error)     │ │
│ │    Unprocessed: 67 posts                                   │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│ 🔍 LOG FILES CREATED:                                           │
│ ├── ai_processing_20250805_202215.log                          │ │
│ └── Console output với full details                             │
│                                                                 │
│ ✅ MySQL Connection Closed                                      │
└─────────────────────────────────────────────────────────────────┘
```

---

## ⚙️ **Configuration & Controls**

### **Rate Limiting & Performance**
```
┌─────────────────────────────────────────────────────────────────┐
│                    ⚡ PERFORMANCE CONTROLS                      │
├─────────────────────────────────────────────────────────────────┤
│ 1. Delay Between Requests: 1-3 seconds                         │
│    └── Prevents OpenAI API rate limiting                       │
│                                                                 │
│ 2. Batch Size Limits:                                          │
│    ├── Small: 5-10 posts (testing)                            │
│    ├── Medium: 20-50 posts (production)                       │
│    └── Large: Unlimited (full processing)                     │
│                                                                 │
│ 3. Error Recovery:                                              │
│    ├── Continue on API errors                                  │
│    ├── Fallback content generation                             │
│    └── Graceful keyboard interrupt handling                    │
└─────────────────────────────────────────────────────────────────┘
```

### **Command Options**
```
┌─────────────────────────────────────────────────────────────────┐
│                     🎮 USAGE OPTIONS                           │
├─────────────────────────────────────────────────────────────────┤
│ 1. Interactive Mode:                                            │
│    python ai_content_processor.py                              │
│                                                                 │
│ 2. Command Line:                                                │
│    ├── python ai_content_processor.py batch 10 2.0            │
│    ├── python ai_content_processor.py single                   │
│    └── python ai_content_processor.py stats                    │
│                                                                 │
│ 3. VS Code Tasks:                                               │
│    ├── "AI Content Processor" (interactive)                    │
│    ├── "AI Process 5 Posts" (batch 5)                         │
│    └── "AI Processing Stats" (monitoring)                      │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎯 **Current System Status**

```
📊 HIỆN TRẠNG:
├── Database: mydb (MySQL on Docker)
├── Source: posts table (86 records)
├── Processed: posts_ai table (1 completed, 85 pending)
├── AI Model: gpt-3.5-turbo
├── Ready for batch processing: ✅
└── Estimated time for full batch: ~6-8 minutes (85 posts × 4s/post)
```

**System sẵn sàng xử lý batch với workflow hoàn chỉnh! 🚀**
