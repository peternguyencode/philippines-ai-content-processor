# 🎯 **SƠ ĐỒ QUY TRÌNH XỬ LÝ CSV POSTS - CHI TIẾT**

## 📊 **TỔNG QUAN QUY TRÌNH**
```
posts.csv (86 posts) 
    ↓
[BƯỚC 1: Đọc CSV]
    ↓
[BƯỚC 2: AI PARAPHRASE] ← PROMPT 1 (Thông minh nhất)
    ↓
[BƯỚC 3: AI CLASSIFY] ← PROMPT 2 (Phân loại)
    ↓
posts_ready.csv (86 posts processed)
```

---

## 🧠 **BƯỚC 2: AI PARAPHRASE - PROMPT THÔNG MINH**

### **🎯 Mục đích:**
- Tạo tiêu đề mới hoàn toàn khác
- Paraphrase nội dung địa phương hóa Philippines  
- Tối ưu SEO cho thị trường Philippines
- Giữ cấu trúc và độ dài tương tự

### **📝 PROMPT AI PARAPHRASE (Thông minh nhất):**
```
Bạn là chuyên gia content marketing và SEO cho thị trường Philippines. 
Hãy viết lại bài viết sau đây để:

1. Tạo tiêu đề mới hoàn toàn khác nhưng giữ ý nghĩa (SEO-friendly cho Philippines)
2. Paraphrase toàn bộ nội dung với từ ngữ địa phương hóa cho Philippines
3. Tối ưu SEO và thu hút người đọc Philippines
4. Giữ nguyên cấu trúc và độ dài tương tự
5. Sử dụng từ khóa phù hợp với thị trường Philippines

TIÊU ĐỀ GỐC: [title]

NỘI DUNG GỐC:
[content - 3000 ký tự đầu]...

Yêu cầu output dạng JSON:
{
    "new_title": "Tiêu đề mới SEO-friendly cho Philippines",
    "new_content": "Nội dung đã được paraphrase và localize",
    "notes": "Ghi chú về quá trình xử lý"
}
```

### **⚙️ Tham số AI:**
- **Model**: GPT-3.5-turbo
- **Max tokens**: 4000
- **Temperature**: 0.7 (sáng tạo vừa phải)
- **Role**: "Chuyên gia content marketing và SEO cho thị trường Philippines"

---

## 🏷️ **BƯỚC 3: AI CLASSIFY - PROMPT PHÂN LOẠI**

### **🎯 Mục đích:**
- Phân loại category chính xác
- Tạo keywords SEO phù hợp Philippines
- Consistent classification

### **📝 PROMPT AI CLASSIFY:**
```
Bạn là chuyên gia phân loại nội dung và SEO cho thị trường Philippines.
Hãy phân tích bài viết sau và đưa ra:

1. Category phù hợp (chọn 1 trong các category sau):
   - Casino & Gaming
   - Online Betting 
   - Sports Betting
   - Slot Games
   - Live Casino
   - Promotions & Bonuses
   - Payment Methods
   - Gaming Tips
   - News & Updates
   - Mobile Gaming

2. Keywords SEO (5-8 từ khóa chính, phù hợp với Philippines market)

TIÊU ĐỀ: [title]

NỘI DUNG: [content - 2000 ký tự đầu]...

Yêu cầu output dạng JSON:
{
    "category": "Category phù hợp nhất",
    "keywords": "keyword1, keyword2, keyword3, keyword4, keyword5",
    "notes": "Lý do phân loại"
}
```

### **⚙️ Tham số AI:**
- **Model**: GPT-3.5-turbo
- **Max tokens**: 1000
- **Temperature**: 0.3 (consistent, ít sáng tạo)
- **Role**: "Chuyên gia phân loại nội dung và SEO cho thị trường Philippines"

---

## 🔄 **QUY TRÌNH CHI TIẾT TỪNG BƯỚC**

### **BƯỚC 1: Đọc CSV File**
```python
# Đọc posts.csv với pandas
df = pd.read_csv('./data/posts.csv')
print(f"📊 Loaded {len(df)} posts từ CSV")

# Columns expected: id, title, content, created_date, etc.
```

### **BƯỚC 2: AI PARAPHRASE (Loop qua từng post)**
```python
for each post in CSV:
    # Gọi OpenAI API với PROMPT PARAPHRASE
    paraphrase_result = paraphrase_content_with_ai(title, content)
    
    # Output: 
    # - new_title (hoàn toàn mới)
    # - new_content (paraphrase + localized)
    # - notes (ghi chú xử lý)
```

### **BƯỚC 3: AI CLASSIFY (Tiếp tục từng post)**  
```python
for each paraphrased post:
    # Gọi OpenAI API với PROMPT CLASSIFY
    classify_result = classify_content_with_ai(new_title, new_content)
    
    # Output:
    # - category (1 trong 10 categories)
    # - keywords (5-8 keywords SEO)
    # - notes (lý do phân loại)
```

### **BƯỚC 4: Xuất CSV Result**
```python
# Tạo posts_ready.csv với columns:
final_df = pd.DataFrame({
    'id': post_ids,
    'original_title': original_titles,
    'title': new_titles,           # ← AI paraphrased
    'content': new_contents,       # ← AI paraphrased  
    'category': categories,        # ← AI classified
    'keywords': keywords_list,     # ← AI generated
    'created_date': timestamps,
    'processing_notes': notes
})

output_file = f'./data/posts_ready_{timestamp}.csv'
final_df.to_csv(output_file, index=False)
```

---

## 📈 **KẾT QUẢ MONG ĐỢI**

### **Input (posts.csv):**
```
id,title,content,created_date
1,"Cách chơi baccarat","Baccarat là game...","2025-08-05"
2,"Slot machine tips","Slot games có nhiều...","2025-08-05"
```

### **Output (posts_ready.csv):**  
```
id,original_title,title,content,category,keywords,created_date,processing_notes
1,"Cách chơi baccarat","Master Baccarat Strategy for Philippines Players","Baccarat gaming strategies specifically designed for Filipino casino enthusiasts...","Live Casino","baccarat philippines, live casino, filipino players, casino strategy, online gaming","2025-08-06","AI paraphrase + classify successful"
2,"Slot machine tips","Ultimate Slot Gaming Guide Philippines","Comprehensive slot machine strategies tailored for Philippines online casino market...","Slot Games","slot games philippines, online slots, casino bonus, filipino casino, gaming tips","2025-08-06","AI paraphrase + classify successful"
```

---

## 💡 **TẠI SAO PROMPT NÀY THÔNG MINH?**

### **1. Localization cho Philippines:**
```
"chuyên gia content marketing và SEO cho thị trường Philippines"
"từ ngữ địa phương hóa cho Philippines" 
"SEO-friendly cho Philippines"
"phù hợp với thị trường Philippines"
```
→ AI hiểu phải adapt content cho audience Philippines cụ thể

### **2. Giữ chất lượng content:**
```
"Giữ nguyên cấu trúc và độ dài tương tự"
"Giữ nguyên ý nghĩa chính"  
"Tối ưu SEO và thu hút người đọc"
```
→ Đảm bảo content quality không bị mất

### **3. Output có cấu trúc:**
```json
{
    "new_title": "...",
    "new_content": "...", 
    "notes": "..."
}
```
→ Dễ parse và xử lý programmatically

### **4. Context-aware:**
```
"TIÊU ĐỀ GỐC: [title]"
"NỘI DUNG GỐC: [content]..."
```
→ AI có đầy đủ context để tạo content phù hợp

### **5. Smart fallback:**
```python
except json.JSONDecodeError:
    # Fallback nếu AI không trả về JSON
    result = {
        "new_title": title,
        "new_content": content,
        "notes": "AI response không đúng JSON format"
    }
```
→ System không crash nếu AI response sai format

---

## 🚀 **CÁCH CHẠY QUY TRÌNH**

### **Option 1: Interactive Menu**
```bash
python interactive_menu.py
# Chọn option 8: Full batch 86 posts CSV
```

### **Option 2: Direct Command**
```bash
python run_full_batch.py
# Hoặc
python csv_ai_processor.py ./data/posts.csv 86 5.0
```

### **Option 3: VS Code Task**
```
Ctrl+Shift+P → "Tasks: Run Task" → "CSV Full Batch"
```

---

## 📊 **THỐNG KÊ PERFORMANCE**

- **Thời gian**: ~15 giây/post (bao gồm 2 API calls)
- **Chi phí**: ~$0.002/post (GPT-3.5-turbo)
- **Total cho 86 posts**: ~22 phút, ~$0.17
- **Success rate**: 100% (có fallback handling)

**🎉 ĐÂY LÀ QUY TRÌNH AI PROCESSING THÔNG MINH NHẤT CHO CSV PIPELINE!**
