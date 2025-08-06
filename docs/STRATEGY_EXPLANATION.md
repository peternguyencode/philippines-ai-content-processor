# 🎯 2 PROMPT STRATEGIES - HOÀN TOÀN KHÁC NHAU

## 📋 TỔNG QUAN

Hệ thống AI Content Processing hiện có **2 STRATEGIES hoàn toàn khác nhau** để xử lý dữ liệu:

### 1️⃣ DATABASE_PIPELINE Strategy
**🎯 Mục đích:** Premium content cho website/blog với SEO optimization  
**📊 Cách xử lý:** Tạo content chất lượng cao với đầy đủ metadata và hình ảnh  

### 2️⃣ CSV_PIPELINE Strategy  
**🎯 Mục đích:** Fast processing cho thị trường Philippines  
**📊 Cách xử lý:** Localization nhanh với cultural adaptation  

---

## 🔥 SO SÁNH CHI TIẾT

| Aspect | DATABASE_PIPELINE | CSV_PIPELINE |
|--------|-------------------|--------------|
| **Prompt Language** | Tiếng Việt | Tiếng Anh |
| **System Message** | SEO & Content Marketing Expert | Philippines Localization Expert |
| **Output Fields** | 6 fields | 3 fields |
| **Max Tokens** | 2,000 | 1,000 |
| **Temperature** | 0.7 (creative) | 0.5 (conservative) |
| **Processing Focus** | SEO + Image generation | Cultural adaptation |
| **Cost per Request** | ~$0.04 | ~$0.002 |
| **Speed** | Chậm hơn (quality first) | Nhanh hơn (speed first) |

---

## 🎨 OUTPUT STRUCTURE

### DATABASE_PIPELINE Output:
```json
{
    "ai_content": "Premium content với SEO optimization",
    "meta_title": "SEO title 60-70 chars",
    "meta_description": "SEO description 150-160 chars", 
    "image_prompt": "Detailed English prompt for DALL-E 3",
    "suggested_tags": "tag1, tag2, tag3, tag4, tag5",
    "notes": "Processing notes và SEO strategy"
}
```

### CSV_PIPELINE Output:
```json
{
    "paraphrased_content": "Content adapted for Philippines",
    "classification": "Category classification",
    "localization_notes": "Philippines adaptation notes"
}
```

---

## 🚀 STRATEGY WORKFLOW

### DATABASE_PIPELINE Workflow:
1. **Input:** Tiêu đề + Nội dung gốc + Category
2. **AI Processing:** 
   - SEO optimization
   - Content enhancement  
   - Meta title/description generation
   - Image prompt creation (English)
   - Tag suggestions
3. **Output:** 6-field JSON → Database
4. **Optional:** DALL-E 3 image generation
5. **Database:** Lưu vào posts_ai với strategy = "DATABASE_PIPELINE"

### CSV_PIPELINE Workflow:
1. **Input:** Tiêu đề + Nội dung gốc
2. **AI Processing:**
   - Philippines cultural adaptation
   - Content paraphrasing
   - Category classification
   - Localization notes
3. **Output:** 3-field JSON → Database/CSV
4. **Database:** Lưu vào posts_ai với strategy = "CSV_PIPELINE"

---

## 💡 KHI NÀO DÙNG STRATEGY NÀO?

### ✅ Dùng DATABASE_PIPELINE khi:
- Cần content chất lượng cao cho website/blog
- Muốn tối ưu SEO đầy đủ
- Cần hình ảnh minh họa (DALL-E 3)
- Không quan trọng chi phí và thời gian
- Target audience: General market

### ✅ Dùng CSV_PIPELINE khi:  
- Cần xử lý volume lớn nhanh chóng
- Target market: Philippines
- Ưu tiên tốc độ và chi phí thấp
- Cần cultural localization
- Không cần SEO metadata chi tiết

---

## 🛠️ CÀI ĐẶT STRATEGY

### Chạy với DATABASE_PIPELINE:
```bash
python ai_content_processor_v2.py DATABASE_PIPELINE
```

### Chạy với CSV_PIPELINE:  
```bash
python ai_content_processor_v2.py CSV_PIPELINE
```

### Interactive Menu với Strategy:
```bash
python interactive_menu_v2.py
```

---

## 📊 DATABASE STRUCTURE

Bảng `posts_ai` hỗ trợ cả 2 strategies:

```sql
posts_ai (
    processing_strategy VARCHAR(50),  -- "DATABASE_PIPELINE" or "CSV_PIPELINE"
    ai_content TEXT,                  -- Được map khác nhau tùy strategy
    meta_title VARCHAR(255),          -- Chỉ DATABASE_PIPELINE mới có đủ
    meta_description VARCHAR(300),    -- CSV_PIPELINE sẽ fallback
    image_prompt TEXT,                -- Chỉ DATABASE_PIPELINE
    tags TEXT,                        -- DATABASE_PIPELINE: từ AI, CSV_PIPELINE: original
    category VARCHAR(100),            -- DATABASE_PIPELINE: original, CSV_PIPELINE: từ classification
    ai_notes TEXT                     -- Notes khác nhau tùy strategy
)
```

---

## 🎯 STRATEGY PATTERN IMPLEMENTATION

### Factory Pattern:
```python
# Tạo strategy
strategy = PromptStrategyFactory.create_strategy("DATABASE_PIPELINE")
# hoặc 
strategy = PromptStrategyFactory.create_strategy("CSV_PIPELINE")

# Execute với strategy cụ thể
result = strategy.execute_strategy(content, title, category)
```

### Switching Strategies:
```python
processor = AIContentProcessorV2("DATABASE_PIPELINE")
# Có thể switch runtime
processor.switch_strategy("CSV_PIPELINE")
```

---

## 🔄 WORKFLOW THỰC TẾ

### Scenario 1: Premium Website Content
1. Chọn DATABASE_PIPELINE
2. Batch process với delay 1-2 giây
3. Kết quả: SEO-optimized content + images
4. Chi phí: 86 posts × $0.04 = ~$3.40

### Scenario 2: Volume Processing cho Philippines
1. Chọn CSV_PIPELINE  
2. Batch process với delay 0.5 giây
3. Kết quả: Fast localized content
4. Chi phí: 86 posts × $0.002 = ~$0.17

### Scenario 3: Dual Processing
1. Chạy DATABASE_PIPELINE trước cho 10 posts premium
2. Switch sang CSV_PIPELINE cho 76 posts còn lại
3. Kết quả: Mixed content quality tùy mục đích

---

## 🎉 KẾT LUẬN

**2 STRATEGIES = 2 CÁCH XỬ LÝ DỮ LIỆU HOÀN TOÀN KHÁC NHAU:**

- **DATABASE_PIPELINE:** Chất lượng > Tốc độ > Chi phí
- **CSV_PIPELINE:** Tốc độ > Chi phí > Tính năng

Mỗi strategy có:
- Prompt riêng biệt
- System message riêng  
- Cách xử lý response khác nhau
- Database mapping khác nhau
- Use case khác nhau

👉 **Chọn strategy phù hợp với mục đích sử dụng!**
