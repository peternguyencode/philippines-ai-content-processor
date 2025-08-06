# 🔄 BƯỚC 2 - AI CONTENT PIPELINE - QUY TRÌNH CHI TIẾT

## 📋 TỔNG QUAN QUY TRÌNH

**Bước 2** là giai đoạn xử lý AI nội dung, chuyển đổi từ **posts gốc** → **posts_ai được tối ưu cho Philippines**

---

## 🚀 QUY TRÌNH 6 BƯỚC CHÍNH

### **BƯỚC 1: 📊 LẤY DỮ LIỆU ĐẦU VÀO**
```sql
SELECT p.id, p.title, p.content, p.category, p.tags
FROM posts p
LEFT JOIN posts_ai pa ON p.id = pa.post_id
WHERE pa.post_id IS NULL  -- Chỉ lấy posts chưa xử lý
```

**Input:** Post gốc từ bảng `posts`
- ID: 85, 86, 87... (83 posts còn lại)
- Title: "Bonus365 Slot Game - The Highest Winning Rate"
- Content: Nội dung tiếng Anh gốc
- Category: Có thể rỗng
- Tags: Có thể rỗng

---

### **BƯỚC 2: 🎯 AUTO CATEGORIZATION**
```python
def _auto_categorize_content(title, content):
    category_keywords = {
        "Bonus": ["bonus", "free", "deposit", "welcome", "promotion"],
        "Review": ["review", "rating", "experience", "opinion"],
        "Payment": ["deposit", "withdrawal", "gcash", "paymaya"],
        "GameGuide": ["how to", "guide", "tips", "strategy"],
        "News": ["news", "update", "announcement", "launch"]
    }
    # Tính điểm cho từng category dựa trên keywords
    best_category = max(category_scores, key=category_scores.get)
```

**Quá trình:**
1. Phân tích title + content (500 ký tự đầu)
2. Tính điểm cho 5 categories: Bonus, Review, Payment, GameGuide, News
3. Chọn category có điểm cao nhất
4. Fallback: "Casino" nếu không match keyword nào

**Output:** `category = "Bonus"` (ví dụ)

---

### **BƯỚC 3: 📝 PROMPT TEMPLATE SELECTION**
```python
def _get_category_prompt_template(category, site_version):
    templates = {
        "Bonus": {
            "specific_requirements": "Focus on bonus terms, Philippines bonuses, GCash/PayMaya",
            "writing_style": "Exciting, promotional, local payment advantages"
        }
    }
    version_styles = {
        1: "Professional, formal tone",
        2: "Casual, friendly approach", 
        3: "Enthusiastic, energetic writing"
    }
```

**Quá trình:**
1. Chọn template dựa trên category được detect
2. Kết hợp với version style (1-5) cho multi-site
3. Tạo ra prompt instructions phù hợp

**Output:** Template với Philippines-specific requirements

---

### **BƯỚC 4: 🇵🇭 AI CONTENT GENERATION**
```python
prompt = f"""
🇵🇭 PHILIPPINES CASINO CONTENT EXPERT - VERSION {site_version}

TARGET CATEGORY: {category}
REQUIREMENTS:
1. 🔥 DEEP REWRITE (100% unique)
2. 🇵🇭 Add Philippines info: GCash, PayMaya, BPI, Metrobank
3. 📱 Mobile-first approach
4. 💰 Include peso (₱) currency
5. 🏆 Competitive advantages vs PH casinos

OUTPUT JSON: {11 fields including ai_content, meta_title, etc}
"""
```

**AI Processing với GPT-3.5-turbo:**
1. Gửi prompt với nội dung gốc
2. AI rewrites 100% unique content
3. Add Philippines local info (GCash, PayMaya, BPI, peso)
4. Optimize for mobile users
5. Include competitive advantages
6. Return structured JSON với 11 fields

**Output JSON:**
```json
{
    "ai_content": "Completely rewritten content with PH info...",
    "auto_category": "Bonus",
    "meta_title": "SEO title 60-65 chars with PH keywords",
    "meta_description": "Meta desc 150-160 chars",
    "image_prompt": "Professional image prompt for DALL-E",
    "suggested_tags": "philippines-casino, gcash-deposit, bonus365-ph",
    "affiliate_cta": "Strong CTA for PH market",
    "local_payments": "GCash, PayMaya supported",
    "seo_keywords": "bonus365 philippines, online casino gcash",
    "version_notes": "What makes this Version 1 unique",
    "competition_angle": "Better than other PH casinos because..."
}
```

---

### **BƯỚC 5: 🎨 IMAGE GENERATION với DALL-E 3**
```python
def generate_image_with_ai(image_prompt):
    response = client.images.generate(
        model="dall-e-3",
        prompt=image_prompt,
        size="1024x1024",
        quality="standard",
        n=1
    )
    return response.data[0].url
```

**Quá trình:**
1. Sử dụng `image_prompt` từ AI output
2. Generate image 1024x1024 với DALL-E 3
3. Return URL của image được tạo
4. Add vào `ai_result["image_url"]`

**Output:** URL image chất lượng cao (ví dụ: `https://oaidalleapi...`)

---

### **BƯỚC 6: 💾 LƯU VÀO DATABASE**
```sql
INSERT INTO posts_ai (
    post_id, title, ai_content, meta_title, meta_description,
    image_url, image_prompt, tags, category, ai_model, ai_notes
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
```

**Philippines Enhanced Notes:**
```
Version: 1 | Category: Bonus
Local Payments: GCash, PayMaya, bank transfer options mentioned
SEO Keywords: bonus365 philippines, online casino gcash
Version Notes: Professional, formal tone approach
Competition: Better bonus rates, faster GCash withdrawals
```

---

## 🌐 MULTI-VERSION PROCESSING

### **Single Version Mode:**
```bash
python ai_content_processor.py single
```
- 1 post → 1 version → 1 record trong posts_ai

### **Multi-Version Mode:**
```bash
python ai_content_processor.py multi 5 2.0 3
```
- 5 posts → 3 versions each → 15 records trong posts_ai
- Version 1: Professional, formal tone
- Version 2: Casual, friendly approach  
- Version 3: Enthusiastic, energetic writing

**Mục đích:** Tạo unique content cho multi-site deployment, tránh duplicate content

---

## ⏱️ TIMING & PERFORMANCE

### **Per Operation Timing:**
```
🔄 Processing Post ID 85 (v1): ~1s
🤖 AI Content Generation: ~6s  
🎨 DALL-E 3 Image: ~20s
💾 Database Save: ~0.1s
📊 Total: ~27s per version
```

### **Cost Analysis:**
```
💰 GPT-3.5-turbo: ~$0.01 per version
🎨 DALL-E 3: ~$0.05 per image
📊 Total: ~$0.06 per version
```

### **Batch Performance:**
```
📊 83 posts × 1 version = 83 operations (~37 minutes, ~$5)
🌐 83 posts × 5 versions = 415 operations (~3 hours, ~$25)
```

---

## 🎯 OUTPUT QUALITY

### **Enhanced Content Features:**
✅ **100% Unique**: AI rewrites không duplicate  
✅ **Philippines Localized**: GCash, PayMaya, BPI, peso  
✅ **Mobile Optimized**: Filipino users dùng mobile chủ yếu  
✅ **SEO Ready**: Meta title/description optimized  
✅ **High-Quality Images**: DALL-E 3 1024x1024  
✅ **Multi-Site Ready**: 5 versions hoàn toàn khác nhau  

### **Database Schema Enhanced:**
```sql
posts_ai:
├── id (AUTO_INCREMENT)
├── post_id (FOREIGN KEY → posts.id)
├── title, ai_content (AI generated)
├── meta_title, meta_description (SEO)  
├── image_url, image_prompt (DALL-E 3)
├── tags, category (Auto-categorized)
├── ai_model, ai_notes (Philippines info)
├── processing_status (completed/error)
└── created_date, updated_date
```

---

## 🚦 STATUS TRACKING

### **Processing Status:**
- `processing`: Đang xử lý
- `completed`: Hoàn thành thành công  
- `error`: Có lỗi xảy ra

### **Real-time Monitoring:**
```bash
🇵🇭 PH AI Processing: 100%|█| 3/3 [01:15<00:00, ✅ Post 85 v1 [Bonus]]
```

### **Statistics Dashboard:**
```
📊 AI PROCESSING STATISTICS:
   total_posts: 86
   processed_posts: 3  
   unprocessed_posts: 83
   by_status: {'completed': 3}
```

---

## 🎉 KẾT QUẢ CUỐI CÙNG

**Input:** 83 posts tiếng Anh gốc từ bonus365casinoall  
**Output:** 83-415 articles Philippines-optimized với:
- Unique content cho multi-site
- GCash/PayMaya integration
- High-quality DALL-E 3 images  
- SEO-ready meta data
- Mobile-first optimization
- Auto-categorization  

**🎯 Ready for deployment across multiple Philippines casino sites!**
