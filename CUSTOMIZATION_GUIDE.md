# 📋 QUY TRÌNH WORDPRESS AUTOMATION - HƯỚNG DẪN CHỈNH SỬA

## 🎯 TỔNG QUAN HIỆN TẠI

**Trạng thái hệ thống**: ✅ HOÀN HẢO 100% (7/7 bước)
- ✅ Python Environment
- ✅ File cấu hình 
- ✅ Biến môi trường
- ✅ Google Sheets (4 bài pending)
- ✅ AI APIs (OpenAI + Gemini)
- ✅ WordPress API
- ✅ Main Workflow

---

## 🔧 CÁC THÀNH PHẦN CÓ THỂ CHỈNH SỬA

### 1. ⚙️ CẤU HÌNH CHUNG (File: `.env`)

**Vị trí**: `d:/duanmoi/.env`

#### AI Configuration:
```env
# Thay đổi AI provider mặc định
DEFAULT_AI_PROVIDER=openai        # openai hoặc gemini
IMAGE_AI_PROVIDER=openai          # chỉ openai (DALL-E)

# Điều chỉnh độ dài content
MAX_CONTENT_LENGTH=2000           # số từ tối đa (1000-5000)
```

#### Processing Configuration:
```env
# Tăng/giảm hiệu suất xử lý
BATCH_SIZE=5                      # số bài xử lý mỗi lần (1-20)
CONCURRENT_REQUESTS=3             # số thread đồng thời (1-10)
REQUEST_DELAY=2                   # delay giữa requests (1-5 giây)
```

**🔧 Cách chỉnh sửa:**
1. Mở file `.env` 
2. Thay đổi giá trị
3. Save và restart chương trình

---

### 2. 🤖 AI CONTENT GENERATION (File: `ai_helper.py`)

**Vị trí**: `d:/duanmoi/ai_helper.py`

#### Chỉnh sửa prompt template (dòng 39-58):
```python
detailed_prompt = f"""
Hãy viết một bài blog chất lượng cao dựa trên yêu cầu sau: "{prompt}"

Yêu cầu:
1. Tạo tiêu đề hấp dẫn (dưới 60 ký tự)
2. Viết nội dung chi tiết, hữu ích (khoảng {Config.MAX_CONTENT_LENGTH} từ)
3. Tạo prompt để sinh ảnh cover phù hợp
4. Tạo meta title SEO (dưới 60 ký tự)
5. Tạo meta description SEO (dưới 160 ký tự)

[THÊM YÊU CẦU TÙY CHỈNH CỦA BẠN Ở ĐÂY]

Trả về theo format JSON:
{{
    "title": "Tiêu đề bài viết",
    "content": "Nội dung bài viết đầy đủ với HTML tags",
    "image_prompt": "Mô tả ảnh để sinh bằng AI",
    "meta_title": "Meta title SEO",
    "meta_description": "Meta description SEO"
}}
"""
```

#### Chỉnh sửa system message (dòng 79):
```python
{"role": "system", "content": "Bạn là một copywriter chuyên nghiệp, viết tiếng Việt tự nhiên và hấp dẫn. [THÊM HƯỚNG DẪN CHI TIẾT]"}
```

**🔧 Cách chỉnh sửa:**
1. Mở `ai_helper.py`
2. Tìm function `generate_content`
3. Chỉnh sửa `detailed_prompt`
4. Save và test

---

### 3. 📤 WORDPRESS SETTINGS (File: `wp_helper.py`)

**Vị trí**: `d:/duanmoi/wp_helper.py`

#### Chỉnh sửa default post settings (dòng 35-42):
```python
post_data = {
    'title': title,
    'content': content,
    'status': status,          # 'draft' hoặc 'publish'
    'format': 'standard',      # 'standard', 'video', 'gallery', etc.
    'categories': [1],         # ID danh mục
    'tags': ['AI', 'Tech'],    # Tags tự động
    'comment_status': 'open'   # 'open' hoặc 'closed'
}
```

#### Tùy chỉnh SEO meta (dòng 189-196):
```python
meta_data = {
    'meta': {
        '_yoast_wpseo_title': meta_title,
        '_yoast_wpseo_metadesc': meta_description,
        '_yoast_wpseo_focuskw': '',           # Focus keyword
        '_yoast_wpseo_canonical': '',         # Canonical URL
        '_yoast_wpseo_meta-robots-noindex': '0',
        '_yoast_wpseo_meta-robots-nofollow': '0'
    }
}
```

**🔧 Cách chỉnh sửa:**
1. Mở `wp_helper.py`
2. Tìm function `create_post` hoặc `update_post_meta`
3. Thêm/sửa fields
4. Save và test

---

### 4. 📊 GOOGLE SHEETS MAPPING (File: `config.py`)

**Vị trí**: `d:/duanmoi/config.py` (dòng 33-44)

#### Thay đổi cấu trúc cột:
```python
SHEET_COLUMNS = {
    'prompt': 'A',          # Prompt/yêu cầu viết bài
    'status': 'B',          # Trạng thái xử lý  
    'title': 'C',           # Tiêu đề bài viết
    'content': 'D',         # Nội dung bài viết
    'wp_url': 'E',          # URL bài đăng trên WP
    'image_url': 'F',       # URL ảnh cover
    'meta_title': 'G',      # Meta title SEO
    'meta_desc': 'H',       # Meta description SEO
    'created_date': 'I',    # Ngày tạo
    'error_log': 'J',       # Log lỗi nếu có
    'category': 'K',        # THÊM CỘT MỚI: Danh mục
    'tags': 'L',            # THÊM CỘT MỚI: Tags
}
```

**🔧 Cách chỉnh sửa:**
1. Mở `config.py`
2. Thêm/sửa `SHEET_COLUMNS`
3. Cập nhật Google Sheet header tương ứng
4. Sửa code xử lý trong `sheets_helper.py`

---

### 5. 🎨 IMAGE GENERATION (File: `ai_helper.py`)

**Vị trí**: `d:/duanmoi/ai_helper.py` (dòng 161-175)

#### Tùy chỉnh image prompt:
```python
optimized_prompt = f"""
{prompt}, 
[THÊM STYLE TÙY CHỈNH]:
- professional quality, high resolution
- clean design, suitable for blog cover image  
- vibrant colors, modern style
- [THEME/STYLE CỦA BẠN]
- Vietnamese content friendly
"""
```

#### Thay đổi image settings:
```python
response = self.openai_client.images.generate(
    model="dall-e-3",                    # dall-e-2 hoặc dall-e-3
    prompt=optimized_prompt,
    size="1024x1024",                    # "256x256", "512x512", "1024x1024"
    quality="hd",                        # "standard" hoặc "hd"
    style="vivid",                       # "natural" hoặc "vivid"
    n=1
)
```

---

### 6. 🔄 WORKFLOW LOGIC (File: `main.py`)

**Vị trí**: `d:/duanmoi/main.py`

#### Thay đổi thứ tự xử lý (dòng 60-110):
```python
# THÊM BƯỚC MỚI HOẶC SỬA THỨ TỰ:

# Bước 1: Sinh content với AI
ai_result = self.ai.generate_content(prompt)

# Bước 2: [THÊM BƯỚC XỬ LÝ CONTENT]
# processed_content = self.process_content(ai_result['content'])

# Bước 3: Sinh ảnh cover
image_url = self.ai.generate_image(image_prompt) if image_prompt else None

# Bước 4: [THÊM BƯỚC XỬ LÝ ẢNH]
# processed_image = self.process_image(image_url)

# Bước 5: Đăng lên WordPress
wp_result = self.wp.process_complete_post(...)
```

#### Thêm validation rules:
```python
# THÊM VALIDATION TÙY CHỈNH:
def validate_content(self, content):
    """Kiểm tra content trước khi đăng"""
    if len(content) < 500:
        return False, "Content quá ngắn"
    if "spam_keyword" in content.lower():
        return False, "Content chứa từ khóa spam"
    return True, "OK"
```

---

## 🎛️ CÁC THAM SỐ QUAN TRỌNG CÓ THỂ ĐIỀU CHỈNH

### Performance Tuning:
```env
# Tăng tốc độ xử lý (rủi ro: rate limit)
CONCURRENT_REQUESTS=5
REQUEST_DELAY=1

# Giảm tải hệ thống (chậm hơn nhưng ổn định)
CONCURRENT_REQUESTS=1  
REQUEST_DELAY=5
```

### Content Quality:
```env
# Content dài hơn (tốn token hơn)
MAX_CONTENT_LENGTH=3000

# Content ngắn hơn (tiết kiệm token)
MAX_CONTENT_LENGTH=1000
```

### AI Provider:
```env
# Dùng Gemini (miễn phí hơn)
DEFAULT_AI_PROVIDER=gemini

# Dùng OpenAI (chất lượng cao hơn)
DEFAULT_AI_PROVIDER=openai
```

---

## 🔧 CÁC LỆNH CHỈNH SỬA THÔNG DỤNG

### Test sau khi chỉnh sửa:
```bash
# Kiểm tra toàn bộ hệ thống
python workflow_checker.py

# Test AI với prompt mới
python test_ai_only.py

# Test 1 bài viết
python main.py single

# Test batch nhỏ
python main.py batch 2
```

### Backup trước khi chỉnh sửa:
```bash
# Backup file quan trọng
copy .env .env.backup
copy ai_helper.py ai_helper.py.backup
copy wp_helper.py wp_helper.py.backup
```

---

## 📈 MONITORING & DEBUGGING

### Log files to check:
- Console output (real-time)
- Google Sheet Error_Log column
- WordPress admin logs

### Common issues:
1. **Rate limit**: Tăng `REQUEST_DELAY`
2. **Content quality**: Chỉnh sửa prompt template
3. **Image generation fail**: Kiểm tra OpenAI credit
4. **WordPress error**: Kiểm tra permissions

---

## 🎯 QUY TRÌNH CHỈNH SỬA RECOMMENDED

1. **Backup files quan trọng**
2. **Chỉnh sửa 1 component tại 1 thời điểm**
3. **Test ngay sau mỗi thay đổi**
4. **Ghi chú lại thay đổi**
5. **Rollback nếu có lỗi**

**🔧 Bạn muốn chỉnh sửa thành phần nào đầu tiên?**
