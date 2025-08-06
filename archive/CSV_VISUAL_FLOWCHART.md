# 🎨 **VISUAL FLOWCHART - CSV AI PROCESSING**

```
┌─────────────────────────────────────────────────────────────────────┐
│                    🚀 CSV AI PROCESSING PIPELINE                    │
└─────────────────────────────────────────────────────────────────────┘

📂 INPUT FILE
┌──────────────────┐
│   posts.csv      │  ← 86 posts gốc
│  ┌─────────────┐ │
│  │id │title    │ │
│  │1  │Cách chơi│ │
│  │2  │Slot tips│ │
│  │...│   ...   │ │
│  └─────────────┘ │
└──────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        BƯỚC 1: ĐỌC CSV                             │
│  📊 pandas.read_csv('./data/posts.csv')                            │
│  ✅ Load 86 posts vào DataFrame                                     │
└─────────────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────────┐
│                 BƯỚC 2: AI PARAPHRASE LOOP                         │
│                      🧠 GPT-3.5-TURBO                              │
└─────────────────────────────────────────────────────────────────────┘
         │
         ▼
    ┌─────────────┐      ┌─────────────────────────────────────────┐
    │ POST #1     │ ──→  │          🤖 AI PROMPT 1                │
    │Title: "Cách │      │  "Bạn là chuyên gia content marketing  │
    │ chơi bacc.."│      │   và SEO cho thị trường Philippines.   │
    │Content: ... │      │   Hãy viết lại bài viết..."           │
    └─────────────┘      │                                         │
         │               │  INPUT: Original title + content       │
         │               │  OUTPUT: JSON {new_title, new_content} │
         ▼               └─────────────────────────────────────────┘
    ┌─────────────┐                           │
    │ RESULT #1   │ ←─────────────────────────┘
    │Title: "Master│
    │Baccarat Phil"│
    │Content: "Bacc│
    │strategies.." │
    └─────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────────┐
│                BƯỚC 3: AI CLASSIFY LOOP                            │
│                     🏷️ GPT-3.5-TURBO                               │
└─────────────────────────────────────────────────────────────────────┘
         │
         ▼
    ┌─────────────┐      ┌─────────────────────────────────────────┐
    │ POST #1     │ ──→  │          🤖 AI PROMPT 2                │
    │New Title:   │      │  "Bạn là chuyên gia phân loại nội dung │
    │"Master Bacc"│      │   và SEO cho thị trường Philippines.   │ 
    │New Content: │      │   Category chọn 1 trong 10..."         │
    │"Strategies" │      │                                         │
    └─────────────┘      │  INPUT: New title + content            │
         │               │  OUTPUT: JSON {category, keywords}     │
         ▼               └─────────────────────────────────────────┘
    ┌─────────────┐                           │
    │ FINAL #1    │ ←─────────────────────────┘
    │Category:    │
    │"Live Casino"│
    │Keywords:    │
    │"baccarat ph"│
    └─────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   BƯỚC 4: LƯU CSV OUTPUT                           │
│  💾 posts_ready_timestamp.csv                                      │
└─────────────────────────────────────────────────────────────────────┘
         │
         ▼
📂 OUTPUT FILE  
┌──────────────────────────────────────────────────────────────────┐
│              posts_ready_20250806_103045.csv                    │
│ ┌─────┬─────────────┬──────────────┬─────────────┬─────────────┐ │
│ │ id  │original_tit │ title        │ category    │ keywords    │ │ 
│ │ 1   │Cách chơi..  │Master Bacc.. │Live Casino  │baccarat ph..│ │
│ │ 2   │Slot tips..  │Ultimate Sl.. │Slot Games   │slot phil..  │ │
│ │ 86  │...         │...           │...          │...          │ │
│ └─────┴─────────────┴──────────────┴─────────────┴─────────────┘ │
└──────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                         📊 STATISTICS                              │
│  ⏱️  Total Time: ~22 minutes (86 posts × 15s/post)                 │
│  💰  Total Cost: ~$0.17 (86 posts × $0.002/post)                   │
│  ✅  Success Rate: 100% (smart fallback system)                    │
│  🎯  Output Quality: Localized cho Philippines market              │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🧠 **CHI TIẾT 2 PROMPT AI THÔNG MINH**

### **PROMPT 1: PARAPHRASE (Thông minh nhất)**
```
┌─────────────────────────────────────────────────────────────────────┐
│                     🤖 AI PARAPHRASE PROMPT                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ SYSTEM ROLE:                                                        │
│ "Bạn là chuyên gia content marketing và SEO cho thị trường         │
│  Philippines."                                                      │
│                                                                     │
│ USER PROMPT:                                                        │
│ "Bạn là chuyên gia content marketing và SEO cho thị trường         │
│  Philippines. Hãy viết lại bài viết sau đây để:                   │
│                                                                     │
│  1. Tạo tiêu đề mới hoàn toàn khác nhưng giữ ý nghĩa              │
│     (SEO-friendly cho Philippines)                                  │
│  2. Paraphrase toàn bộ nội dung với từ ngữ địa phương hóa         │
│     cho Philippines                                                 │
│  3. Tối ưu SEO và thu hút người đọc Philippines                   │
│  4. Giữ nguyên cấu trúc và độ dài tương tự                        │
│  5. Sử dụng từ khóa phù hợp với thị trường Philippines            │
│                                                                     │
│  TIÊU ĐỀ GỐC: [original_title]                                     │
│  NỘI DUNG GỐC: [first_3000_chars_of_content]...                   │
│                                                                     │
│  Yêu cầu output dạng JSON:                                         │
│  {                                                                  │
│      'new_title': 'Tiêu đề mới SEO-friendly cho Philippines',     │
│      'new_content': 'Nội dung đã được paraphrase và localize',    │
│      'notes': 'Ghi chú về quá trình xử lý'                        │
│  }                                                                  │
│                                                                     │
│ CONFIG:                                                             │
│  - Model: gpt-3.5-turbo                                           │
│  - Max tokens: 4000                                                │
│  - Temperature: 0.7 (balanced creativity)                         │
└─────────────────────────────────────────────────────────────────────┘
```

### **PROMPT 2: CLASSIFY**
```
┌─────────────────────────────────────────────────────────────────────┐
│                    🏷️ AI CLASSIFY PROMPT                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ SYSTEM ROLE:                                                        │
│ "Bạn là chuyên gia phân loại nội dung và SEO cho thị trường       │
│  Philippines."                                                      │
│                                                                     │
│ USER PROMPT:                                                        │
│ "Bạn là chuyên gia phân loại nội dung và SEO cho thị trường       │
│  Philippines. Hãy phân tích bài viết sau và đưa ra:              │
│                                                                     │
│  1. Category phù hợp (chọn 1 trong các category sau):             │
│     - Casino & Gaming                                               │
│     - Online Betting                                                │
│     - Sports Betting                                                │
│     - Slot Games                                                    │
│     - Live Casino                                                   │
│     - Promotions & Bonuses                                          │
│     - Payment Methods                                               │
│     - Gaming Tips                                                   │
│     - News & Updates                                                │
│     - Mobile Gaming                                                 │
│                                                                     │
│  2. Keywords SEO (5-8 từ khóa chính, phù hợp với Philippines      │
│     market)                                                         │
│                                                                     │
│  TIÊU ĐỀ: [paraphrased_title]                                      │
│  NỘI DUNG: [first_2000_chars_of_paraphrased_content]...           │
│                                                                     │
│  Yêu cầu output dạng JSON:                                         │
│  {                                                                  │
│      'category': 'Category phù hợp nhất',                         │
│      'keywords': 'keyword1, keyword2, keyword3, keyword4',        │
│      'notes': 'Lý do phân loại'                                    │
│  }                                                                  │
│                                                                     │
│ CONFIG:                                                             │
│  - Model: gpt-3.5-turbo                                           │
│  - Max tokens: 1000                                                │
│  - Temperature: 0.3 (consistent classification)                   │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🎯 **VÍ DỤ THỰC TẾ**

### **INPUT:**
```
Title: "Cách chơi baccarat online hiệu quả"
Content: "Baccarat là một trong những trò chơi casino phổ biến nhất..."
```

### **SAU AI PARAPHRASE:**
```json
{
  "new_title": "Master Baccarat Strategies for Philippines Online Casino Players",
  "new_content": "Discover the most effective baccarat gaming techniques specifically designed for Filipino casino enthusiasts. Learn professional strategies that work best in Philippines online casino environment...",
  "notes": "Content localized for Philippines market with SEO optimization"
}
```

### **SAU AI CLASSIFY:**  
```json
{
  "category": "Live Casino",
  "keywords": "baccarat philippines, live casino games, online baccarat strategy, filipino casino players, baccarat tips philippines",
  "notes": "Classified as Live Casino due to baccarat focus with Philippines localization"
}
```

### **FINAL OUTPUT CSV ROW:**
```
1,"Cách chơi baccarat online hiệu quả","Master Baccarat Strategies for Philippines Online Casino Players","Discover the most effective baccarat gaming techniques...","Live Casino","baccarat philippines, live casino games, online baccarat strategy","2025-08-06","AI paraphrase + classify successful"
```

🎉 **ĐÂY LÀ QUY TRÌNH AI XỬ LÝ CSV THÔNG MINH VÀ HIỆU QUẢ NHẤT!**
