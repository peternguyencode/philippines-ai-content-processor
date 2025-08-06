# 🤖 AI Content Processor Guide

## 🎯 **Mục tiêu:**
Xử lý nội dung posts từ bảng `posts` với AI (OpenAI), tạo nội dung tối ưu SEO và lưu vào bảng `posts_ai`.

## 📊 **Workflow:**
```
posts (raw data) → AI Processing → posts_ai (optimized content)
```

---

## 🗄️ **Database Schema:**

### **Bảng gốc: `posts`**
- `id` - Primary key
- `title` - Tiêu đề bài viết
- `content` - Nội dung thô
- `category` - Danh mục
- `tags` - Tags

### **Bảng đích: `posts_ai`** (tự động tạo)
- `id` - Auto increment primary key
- `post_id` - Foreign key → posts.id
- `title` - Tiêu đề gốc
- `ai_content` - Nội dung đã được AI xử lý
- `meta_title` - SEO title (60-70 ký tự)
- `meta_description` - SEO description (150-160 ký tự)
- `tags` - Tags được AI suggest
- `category` - Danh mục
- `ai_model` - Model AI đã sử dụng
- `ai_notes` - Ghi chú xử lý
- `processing_status` - Trạng thái (processing/completed/error)
- `created_date`, `updated_date` - Timestamps

---

## 🚀 **Cách sử dụng:**

### **1. Interactive Mode (Recommended)**
```bash
python ai_content_processor.py
```

**Menu options:**
1. Xử lý tất cả posts chưa được AI xử lý
2. Xử lý giới hạn số posts
3. Xem thống kê xử lý
4. Xử lý 1 post để test

### **2. Command Line**
```bash
# Xử lý tất cả posts
python ai_content_processor.py batch

# Xử lý 10 posts với delay 2 giây
python ai_content_processor.py batch 10 2.0

# Xem thống kê
python ai_content_processor.py stats

# Test với 1 post
python ai_content_processor.py single
```

### **3. VS Code Tasks**
- `Ctrl+Shift+P` → `Tasks: Run Task` → chọn:
  - **"AI Content Processor"** - Interactive mode
  - **"AI Process 5 Posts"** - Batch xử lý 5 posts
  - **"AI Processing Stats"** - Xem thống kê

---

## 🤖 **AI Processing Features:**

### **Content Rewriting:**
- ✅ Tối ưu SEO
- ✅ Cải thiện readability  
- ✅ Thêm keywords tự nhiên
- ✅ Cấu trúc đoạn văn ngắn gọn
- ✅ Giữ nguyên ý nghĩa chính

### **SEO Optimization:**
- ✅ Meta title (60-70 ký tự)
- ✅ Meta description (150-160 ký tự)
- ✅ Keyword suggestions
- ✅ Tag recommendations

### **AI Response Format:**
```json
{
    "ai_content": "Nội dung đã được viết lại...",
    "meta_title": "SEO-optimized title",
    "meta_description": "SEO description...",
    "suggested_tags": "tag1, tag2, tag3",
    "notes": "Processing notes"
}
```

---

## ⚙️ **Configuration:**

### **Environment Variables (.env):**
```env
OPENAI_API_KEY=your_openai_api_key
AI_MODEL=gpt-3.5-turbo
```

### **MySQL Connection:**
- Host: `localhost:3308`
- Database: `mydb`
- User: `root`
- Password: `baivietwp_password`

---

## 📈 **Monitoring & Stats:**

### **Processing Statistics:**
```bash
python ai_content_processor.py stats
```

**Output:**
- Total posts in database
- Processed posts count
- Unprocessed posts count
- Status breakdown (processing/completed/error)

### **Logging:**
- File: `ai_processing_YYYYMMDD_HHMMSS.log`
- Console output với progress bar
- Error tracking chi tiết

---

## 🛡️ **Safety Features:**

### **Duplicate Prevention:**
- ✅ UNIQUE constraint trên `post_id`
- ✅ Skip posts đã xử lý
- ✅ ON DUPLICATE KEY UPDATE

### **Error Handling:**
- ✅ API rate limiting với delay
- ✅ Fallback content nếu AI fails
- ✅ Processing status tracking
- ✅ Comprehensive logging

### **Progress Tracking:**
- ✅ Real-time progress bar
- ✅ Status updates trong database
- ✅ Interrupt handling (Ctrl+C)

---

## 🔧 **Troubleshooting:**

### **Common Issues:**

**1. OpenAI API Error:**
```bash
❌ AI processing failed: API key not found
```
**Solution:** Kiểm tra OPENAI_API_KEY trong .env

**2. MySQL Connection Error:**
```bash
❌ MySQL connection error: Access denied
```
**Solution:** Kiểm tra MySQL container đang chạy

**3. No Posts to Process:** 
```bash
ℹ️ Không có posts nào cần xử lý!
```
**Solution:** Tất cả posts đã được xử lý hoặc bảng posts rỗng

### **Performance Tuning:**
- **Delay giữa requests:** 1-3 giây (tránh rate limit)
- **Batch size:** 5-20 posts (tùy API quota) 
- **Concurrent processing:** Không recommend với OpenAI API

---

## 📊 **Current Status:**

✅ **Ready to process 86 posts:**
- Database: `mydb` 
- Source table: `posts` (86 records)
- Target table: `posts_ai` (auto-created)
- AI Model: `gpt-3.5-turbo`

---

## 🎯 **Next Steps:**

1. **Test với 1 post:**
   ```bash
   python ai_content_processor.py single
   ```

2. **Xử lý batch nhỏ:**
   ```bash
   python ai_content_processor.py batch 5 2.0
   ```

3. **Monitor progress:**
   ```bash
   python ai_content_processor.py stats
   ```

4. **Xem kết quả trong phpMyAdmin:**
   - http://localhost:8081
   - Database: `mydb`
   - Table: `posts_ai`

**Ready to transform your content with AI! 🚀**
