# 🧠 **GIẢI THÍCH PROMPT AI VÀ JSON OUTPUT CHI TIẾT**

## 🤖 **PROMPT LÀ GÌ?**

### **📝 Định nghĩa:**
**PROMPT** = Câu hỏi/yêu cầu bạn gửi cho ChatGPT để AI hiểu cần làm gì.

### **🔄 QUY TRÌNH:**
```
You (PROMPT) → ChatGPT → Response (JSON)
```

---

## 📋 **PROMPT THỰC TẾ TRONG HỆ THỐNG**

### **🎯 PROMPT HIỆN TẠI (CSV Pipeline):**
```
Bạn là chuyên gia content marketing và SEO cho thị trường Philippines. 
Hãy viết lại bài viết sau đây để:

1. Tạo tiêu đề mới hoàn toàn khác nhưng giữ ý nghĩa (SEO-friendly cho Philippines)
2. Paraphrase toàn bộ nội dung với từ ngữ địa phương hóa cho Philippines
3. Tối ưu SEO và thu hút người đọc Philippines
4. Giữ nguyên cấu trúc và độ dài tương tự
5. Sử dụng từ khóa phù hợp với thị trường Philippines

TIÊU ĐỀ GỐC: [title]
NỘI DUNG GỐC: [content]

Yêu cầu output dạng JSON:
{
    "new_title": "Tiêu đề mới SEO-friendly cho Philippines",
    "new_content": "Nội dung đã được paraphrase và localize",
    "notes": "Ghi chú về quá trình xử lý"
}
```

### **🎯 PROMPT DATABASE PIPELINE:**
```
Bạn là một chuyên gia content marketing và SEO. Hãy viết lại bài viết sau đây để:
1. Tối ưu SEO và thu hút người đọc
2. Giữ nguyên ý nghĩa chính nhưng diễn đạt hay hơn
3. Thêm keywords tự nhiên liên quan đến chủ đề
4. Cấu trúc rõ ràng với đoạn văn ngắn

Tiêu đề gốc: [title]
Danh mục: [category]
Nội dung gốc: [content]

Yêu cầu output dạng JSON:
{
    "ai_content": "Nội dung đã được viết lại",
    "meta_title": "Tiêu đề SEO (60-70 ký tự)",
    "meta_description": "Mô tả SEO (150-160 ký tự)",
    "image_prompt": "Mô tả hình ảnh phù hợp cho bài viết (tiếng Anh)",
    "suggested_tags": "tag1, tag2, tag3",
    "notes": "Ghi chú về quá trình xử lý"
}
```

---

## 🎯 **JSON OUTPUT LÀ GÌ?**

### **📊 JSON = Định dạng dữ liệu cấu trúc**
```json
{
    "key1": "value1",
    "key2": "value2"
}
```

### **🔍 VÍ DỤ THỰC TẾ:**

**INPUT (Bài viết gốc):**
```
Title: "Cách chơi baccarat online"
Content: "Baccarat là trò chơi casino phổ biến..."
```

**PROMPT gửi cho ChatGPT:**
```
Viết lại bài này cho Philippines market...
Yêu cầu output JSON: {"new_title": "...", "new_content": "...", "notes": "..."}
```

**OUTPUT từ ChatGPT (JSON):**
```json
{
    "new_title": "Master Baccarat Strategies for Philippines Players",
    "new_content": "Discover the most effective baccarat gaming techniques specifically designed for Filipino casino enthusiasts...",
    "notes": "Content localized for Philippines market with SEO optimization"
}
```

### **⚙️ XỬ LÝ JSON trong Code:**
```python
# ChatGPT trả về JSON string
ai_response = '{"new_title": "Master Baccarat...", "new_content": "..."}'

# Parse JSON thành Python dict
import json
result = json.loads(ai_response)

# Truy cập dữ liệu
new_title = result["new_title"]
new_content = result["new_content"]
notes = result["notes"]
```

---

## 🎨 **CÁC LOẠI PROMPT KHÁC NHAU**

### **1. PROMPT TẠO NỘI DUNG:**
```
Viết bài viết về [topic] với tone [professional/casual]
Output: {"content": "...", "title": "..."}
```

### **2. PROMPT PHÂN LOẠI:**
```
Phân loại bài viết này thuộc category nào: [categories]
Output: {"category": "...", "confidence": "..."}
```

### **3. PROMPT TẠO HÌNH ẢNH:**
```
Tạo prompt DALL-E cho bài viết về [topic]
Output: {"image_prompt": "...", "style": "..."}
```

### **4. PROMPT SEO:**
```
Tối ưu SEO cho bài viết này cho keyword [keyword]
Output: {"meta_title": "...", "meta_description": "...", "keywords": "..."}
```

---

## 💡 **TẠI SAO DÙNG JSON OUTPUT?**

### **✅ ƯU ĐIỂM:**
1. **Cấu trúc rõ ràng**: Dễ parse và xử lý
2. **Nhiều thông tin**: Một lần gọi API, nhận nhiều kết quả
3. **Consistency**: Format luôn giống nhau
4. **Error handling**: Dễ kiểm tra missing fields

### **❌ NHƯỢC ĐIỂM:**
- AI đôi khi không trả về đúng JSON format
- Cần có fallback handling

---

## 🛠️ **CUSTOMIZABLE PROMPT SYSTEM**

### **💡 Ý TƯỞNG:**
Cho phép user tự định nghĩa PROMPT và JSON output format.

### **📝 CẤU TRÚC PROMPT FILE:**
```json
{
    "name": "Philippines Casino Content",
    "description": "Paraphrase for Philippines market",
    "system_role": "Bạn là chuyên gia content marketing cho thị trường Philippines",
    "user_prompt": "Viết lại bài viết sau để tối ưu cho Philippines:\n\nTiêu đề: {title}\nNội dung: {content}\n\nYêu cầu output JSON:\n{output_format}",
    "output_format": {
        "new_title": "Tiêu đề mới cho Philippines",
        "new_content": "Nội dung đã paraphrase",
        "keywords": "Keywords SEO",
        "notes": "Ghi chú xử lý"
    },
    "variables": ["title", "content"],
    "model": "gpt-3.5-turbo",
    "max_tokens": 4000,
    "temperature": 0.7
}
```

### **🎯 CÁCH SỬ DỤNG:**
```python
# Load prompt từ file
with open('prompts/philippines_casino.json', 'r') as f:
    prompt_config = json.load(f)

# Build prompt với data thực tế
user_prompt = prompt_config['user_prompt'].format(
    title=post_title,
    content=post_content,
    output_format=json.dumps(prompt_config['output_format'], indent=2)
)

# Gọi OpenAI
response = client.chat.completions.create(
    model=prompt_config['model'],
    messages=[
        {"role": "system", "content": prompt_config['system_role']},
        {"role": "user", "content": user_prompt}
    ],
    max_tokens=prompt_config['max_tokens'],
    temperature=prompt_config['temperature']
)
```

---

## 🚀 **EXAMPLES - CÁC PROMPT TEMPLATE**

### **1. BASIC REWRITE:**
```json
{
    "name": "Basic Content Rewrite",
    "output_format": {
        "new_content": "Content đã viết lại",
        "improvements": "Các cải thiện đã thực hiện"
    }
}
```

### **2. SEO OPTIMIZATION:**
```json
{
    "name": "SEO Content Optimizer",
    "output_format": {
        "optimized_content": "Content đã tối ưu SEO",
        "meta_title": "Title SEO 60-70 chars",
        "meta_description": "Description 150-160 chars",
        "focus_keywords": "keyword1, keyword2, keyword3",
        "readability_score": "Điểm đánh giá độ dễ đọc"
    }
}
```

### **3. SOCIAL MEDIA:**
```json
{
    "name": "Social Media Content",
    "output_format": {
        "facebook_post": "Content cho Facebook",
        "twitter_post": "Content cho Twitter (280 chars)",
        "instagram_caption": "Caption cho Instagram",
        "hashtags": "#hashtag1 #hashtag2 #hashtag3"
    }
}
```

---

## 🎯 **SUMMARY**

### **🤖 PROMPT:**
- **Là**: Câu hỏi/yêu cầu gửi cho ChatGPT
- **Mục đích**: Hướng dẫn AI làm gì với input
- **Quan trọng**: Prompt hay = output chất lượng cao

### **📊 JSON OUTPUT:**  
- **Là**: Định dạng dữ liệu cấu trúc từ AI
- **Ưu điểm**: Dễ parse, nhiều thông tin, consistent
- **Ví dụ**: `{"new_title": "...", "new_content": "...", "notes": "..."}`

### **🔗 QUY TRÌNH:**
```
User Input → PROMPT Template → ChatGPT → JSON Response → Parse → Use Data
```

**📝 Bây giờ tôi sẽ thêm tính năng Add PROMPT vào interactive menu!**
