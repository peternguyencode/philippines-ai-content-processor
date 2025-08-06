# 🔄 SƠ ĐỒ QUY TRÌNH WORDPRESS AUTOMATION CHI TIẾT

## 📊 TỔNG QUAN HỆ THỐNG

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   GOOGLE SHEET  │    │    AI ENGINES   │    │   WORDPRESS     │
│  (Input/Output) │    │  (Processing)   │    │   (Output)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
    ┌────▼────┐             ┌────▼────┐             ┌────▼────┐
    │ Prompts │             │ OpenAI  │             │  Posts  │
    │ Status  │             │ Gemini  │             │ Images  │
    │ Results │             │ DALL-E  │             │ SEO     │
    └─────────┘             └─────────┘             └─────────┘
```

---

## 🎯 QUY TRÌNH CHI TIẾT - 7 BƯỚC

### **BƯỚC 1: ĐỌC DỮ LIỆU TỪ GOOGLE SHEET** 📊
```
[Google Sheet] 
    ↓
[sheets_helper.py] → get_pending_rows()
    ↓
Lấy các hàng có Status = "pending"
    ↓
Trả về: List[{prompt, row_number, ...}]
```

**📍 Vị trí dữ liệu:**
- **Source**: Google Sheet ID: `1JNeybKkC9nRUXWgX6yIdhSv8roiweal2VESQtwfLHc0`
- **Cột A**: Prompt (yêu cầu viết bài)
- **Cột B**: Status (pending/processing/completed/error)
- **File xử lý**: `sheets_helper.py` - class `SheetsHelper`

---

### **BƯỚC 2: CẬP NHẬT TRẠNG THÁI PROCESSING** 🔄
```
[main.py] → process_single_row()
    ↓
[sheets_helper.py] → update_row_status(row_number, "processing")
    ↓
Google Sheet Cột B = "processing"
```

**📍 Mục đích**: Đánh dấu bài đang được xử lý, tránh trùng lặp

---

### **BƯỚC 3: SINH CONTENT VỚI AI** 🤖
```
[ai_helper.py] → generate_content(prompt)
    ↓
┌─────────────────┐    ┌─────────────────┐
│   OPENAI API    │ or │   GEMINI API    │
│  gpt-3.5-turbo  │    │ gemini-1.5-flash│
└─────────────────┘    └─────────────────┘
    ↓
Trả về: {
    title: "Tiêu đề bài viết",
    content: "Nội dung HTML",
    image_prompt: "Mô tả ảnh",
    meta_title: "SEO title",
    meta_description: "SEO desc"
}
```

**📍 AI Providers:**
- **OpenAI**: `sk-proj-VoVJ0j-tczu-...` (Primary)
- **Gemini**: `AIzaSyA_btBnjasFVLmg...` (Backup)
- **File xử lý**: `ai_helper.py` - class `AIHelper`

---

### **BƯỚC 4: SINH ẢNH COVER VỚI DALL-E** 🎨
```
[ai_helper.py] → generate_image(image_prompt)
    ↓
[DALL-E 3 API]
    ↓
Trả về: URL ảnh trên OpenAI CDN
Ví dụ: https://oaidalleapiprodscus.blob.core.windows.net/...
```

**📍 Image Generation:**
- **Engine**: DALL-E 3
- **Size**: 1024x1024
- **Quality**: Standard
- **Style**: Optimized cho blog cover

---

### **BƯỚC 5: TẠO BÀI VIẾT TRÊN WORDPRESS** 📤
```
[wp_helper.py] → create_post(title, content, "draft")
    ↓
[WordPress REST API]: https://boss3.biz/wp-json/wp/v2/posts
    ↓
Trả về: {
    id: 4624,
    link: "https://boss3.biz/?p=4624",
    title: {...},
    status: "draft"
}
```

**📍 WordPress Database:**
- **Site**: https://boss3.biz
- **API**: REST API v2
- **Auth**: Application Password
- **Tables**: wp_posts, wp_postmeta
- **File xử lý**: `wp_helper.py` - class `WPHelper`

---

### **BƯỚC 6: UPLOAD ẢNH VÀ SET FEATURED IMAGE** 🖼️
```
[wp_helper.py] → upload_image(image_url)
    ↓
Download ảnh từ OpenAI CDN
    ↓
[WordPress Media API]: /wp-json/wp/v2/media
    ↓
Upload lên: https://boss3.biz/wp-content/uploads/2025/08/
    ↓
[wp_helper.py] → set_featured_image(post_id, media_id)
```

**📍 Media Storage:**
- **Location**: WordPress wp-content/uploads/
- **Naming**: ai_generated_[timestamp].png
- **Database**: wp_posts (attachment), wp_postmeta

---

### **BƯỚC 7: CẬP NHẬT SEO META** 🏷️
```
[wp_helper.py] → update_post_meta(post_id, meta_title, meta_desc)
    ↓
[WordPress REST API]: Update post meta
    ↓
Yoast SEO fields:
- _yoast_wpseo_title
- _yoast_wpseo_metadesc
```

**📍 SEO Database:**
- **Plugin**: Yoast SEO
- **Table**: wp_postmeta
- **Fields**: Custom meta fields

---

### **BƯỚC 8: CẬP NHẬT KẾT QUẢ VÀO GOOGLE SHEET** ✅
```
[sheets_helper.py] → update_row_status(row_number, "completed", **data)
    ↓
Google Sheet columns update:
- Cột B: "completed"
- Cột C: Title
- Cột D: Content preview
- Cột E: WordPress URL
- Cột F: Image URL
- Cột G: Meta title
- Cột H: Meta description
- Cột I: Created date
```

---

## 🗃️ CẤU TRÚC DATABASE & STORAGE

### **1. Google Sheets (Input/Output Database)**
```
Spreadsheet ID: 1JNeybKkC9nRUXWgX6yIdhSv8roiweal2VESQtwfLHc0

Columns:
A: Prompt           | "Viết bài về AI marketing"
B: Status           | pending → processing → completed
C: Title            | "10 Lợi Ích AI Trong Marketing"
D: Content          | HTML content (preview)
E: WP_URL           | https://boss3.biz/?p=4624
F: Image_URL        | https://boss3.biz/wp-content/...
G: Meta_Title       | SEO optimized title
H: Meta_Description | SEO description
I: Created_Date     | 2025-08-05 11:30:25
J: Error_Log        | Error messages if any
```

### **2. WordPress Database (Output Storage)**
```
Site: https://boss3.biz
Database Tables:

wp_posts:
- ID: 4624
- post_title: "10 Lợi Ích AI Trong Marketing"
- post_content: HTML content
- post_status: draft/publish
- post_type: post

wp_postmeta:
- meta_key: _thumbnail_id (featured image)
- meta_key: _yoast_wpseo_title
- meta_key: _yoast_wpseo_metadesc

wp_posts (attachments):
- post_type: attachment
- guid: image URLs
```

### **3. AI APIs (Processing Engines)**
```
OpenAI:
- Endpoint: https://api.openai.com/v1/
- Models: gpt-3.5-turbo, dall-e-3
- Storage: Temporary (URLs expire)

Gemini:
- Endpoint: https://generativelanguage.googleapis.com/
- Model: gemini-1.5-flash
- Storage: None (text only)
```

---

## 📦 CẤU TRÚC MODULE ĐÃ TÁCH RIÊNG

### **Module 1: Data Input/Output** 📊
```
📁 sheets_helper.py
├── class SheetsHelper
├── get_pending_rows()      # Đọc prompts
├── update_row_status()     # Cập nhật trạng thái
├── update_error()          # Ghi log lỗi
└── batch_update()          # Cập nhật hàng loạt
```

### **Module 2: AI Processing** 🤖
```
📁 ai_helper.py
├── class AIHelper
├── generate_content()      # Sinh content text
├── generate_image()        # Sinh ảnh DALL-E
├── _generate_with_openai() # OpenAI engine
├── _generate_with_gemini() # Gemini engine
└── optimize_for_seo()      # SEO optimization
```

### **Module 3: WordPress Publishing** 📤
```
📁 wp_helper.py
├── class WPHelper
├── create_post()           # Tạo bài viết
├── upload_image()          # Upload ảnh
├── set_featured_image()    # Set ảnh cover
├── update_post_meta()      # Update SEO meta
├── publish_post()          # Publish bài
└── process_complete_post() # Quy trình hoàn chỉnh
```

### **Module 4: Main Workflow** 🔄
```
📁 main.py
├── class WordPressAutomation
├── process_single_row()    # Xử lý 1 bài
├── process_batch()         # Xử lý hàng loạt
└── run_interactive()       # Menu tương tác
```

### **Module 5: Configuration** ⚙️
```
📁 config.py
├── class Config
├── API keys management
├── Database connections
├── Processing parameters
└── validate_config()
```

---

## 🛡️ SAFETY & ERROR HANDLING

### **Isolation per Module:**
```
Lỗi Google Sheets ❌ → Chỉ ảnh hưởng data I/O
Lỗi AI API ❌        → Chỉ ảnh hưởng content generation  
Lỗi WordPress ❌     → Chỉ ảnh hưởng publishing
Lỗi 1 bài ❌         → Các bài khác vẫn tiếp tục
```

### **Rollback Capability:**
```
📊 Google Sheet: Status rollback to "pending"
🤖 AI: Retry with different provider
📤 WordPress: Draft posts (safe to delete)
🖼️ Images: Stored separately, can re-upload
```

---

## 🔧 CÁC ĐIỂM CÓ THỂ CHỈNH SỬA RIÊNG

### **1. Chỉ sửa Input Source (Google Sheets):**
- File: `sheets_helper.py`
- Thay đổi: Column mapping, validation rules
- Không ảnh hưởng: AI, WordPress

### **2. Chỉ sửa AI Engine:**
- File: `ai_helper.py` 
- Thay đổi: Prompts, models, providers
- Không ảnh hưởng: Database, WordPress

### **3. Chỉ sửa WordPress Output:**
- File: `wp_helper.py`
- Thay đổi: Post format, SEO, categories
- Không ảnh hưởng: Input, AI processing

### **4. Chỉ sử Performance:**
- File: `.env`
- Thay đổi: Concurrent, delays, batch size
- Không ảnh hưởng: Logic xử lý

**🎯 Mỗi module hoàn toàn độc lập, bạn có thể sửa từng phần mà không sợ ảnh hưởng phần khác!**
