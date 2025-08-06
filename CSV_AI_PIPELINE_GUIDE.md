# 📊 CSV AI PROCESSING PIPELINE - HƯỚNG DẪN SỬ DỤNG

## 🎯 **Tổng quan**

Pipeline này xử lý file CSV với các bài viết, sử dụng AI để:
- **Paraphrase content** và tạo tiêu đề mới SEO-friendly cho Philippines
- **Phân loại category** và **gán keywords** tự động
- **Xuất file kết quả** posts_ready.csv

## 📋 **Quy trình xử lý**

### **Bước 1: Đọc file posts.csv**
- Input: CSV với các trường `id`, `title`, `content` 
- Validation: Kiểm tra cột cần thiết
- Output: List các posts để xử lý

### **Bước 2: AI Paraphrase Content**
- **Model**: GPT-3.5-turbo hoặc GPT-4o
- **Prompt**: Content marketing và SEO cho Philippines
- **Output**: Title mới + content mới được localize

### **Bước 3: AI Classification**
- **Categories**: Casino & Gaming, Promotions & Bonuses, etc.
- **Keywords**: 5-8 từ khóa SEO phù hợp Philippines
- **Output**: Category + keywords cho từng bài

### **Bước 4: Export posts_ready.csv**
- **Fields**: `id`, `title`, `content`, `category`, `keywords`
- **Location**: `./data/posts_ready_[timestamp].csv`

## 🚀 **Cách sử dụng**

### **1. Command Line**
```bash
# Xử lý tất cả posts với delay 2 giây
python csv_ai_processor.py ./data/posts.csv

# Xử lý giới hạn 10 posts với delay 5 giây  
python csv_ai_processor.py ./data/posts.csv 10 5.0
```

### **2. Interactive Mode**
```bash
python csv_ai_processor.py
# Nhập đường dẫn file CSV khi được hỏi
```

### **3. Python Code**
```python
from csv_ai_processor import CSVAIProcessor

processor = CSVAIProcessor()
stats = processor.process_csv_pipeline(
    input_csv="./data/posts.csv",
    limit=5,
    delay=3.0
)
```

## 📊 **Test Results**

### **Performance Metrics**
- **Speed**: ~15 giây/post (bao gồm 2 AI calls + delay)
- **Success Rate**: 100% (2/2 posts test)
- **AI Models**: GPT-3.5-turbo cho content + classification

### **Sample Output**
```csv
id,title,content,category,keywords
1,"Claim Your ₱100 Free Sign Up Bonus without Deposit | Best Online Casino in Philippines","[paraphrased content...]","Promotions & Bonuses","free sign up bonus, no deposit, online casino, Philippines, bonus activation"
```

## ⚙️ **Configuration**

### **OpenAI Setup**
```python
# config.py
OPENAI_API_KEY = "your-api-key"
AI_MODEL = "gpt-3.5-turbo"  # hoặc "gpt-4o"
```

### **Categories Available**
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

## 🔧 **AI Prompts**

### **Paraphrase Prompt**
```
Bạn là chuyên gia content marketing và SEO cho thị trường Philippines. 
Hãy viết lại bài viết để:
1. Tạo tiêu đề mới hoàn toàn khác nhưng giữ ý nghĩa (SEO-friendly cho Philippines)
2. Paraphrase toàn bộ nội dung với từ ngữ địa phương hóa cho Philippines
3. Tối ưu SEO và thu hút người đọc Philippines
4. Sử dụng từ khóa phù hợp với thị trường Philippines
```

### **Classification Prompt**
```
Phân tích bài viết và đưa ra:
1. Category phù hợp (chọn từ 10 categories available)
2. Keywords SEO (5-8 từ khóa chính, phù hợp với Philippines market)
```

## 📈 **Cost Estimation**

### **OpenAI API Costs**
- **GPT-3.5-turbo**: ~$0.002/post (paraphrase + classification)
- **GPT-4o**: ~$0.02/post (nếu sử dụng)
- **Batch 86 posts**: ~$0.17 (GPT-3.5) hoặc ~$1.72 (GPT-4o)

### **Processing Time**
- **86 posts**: ~21 phút với delay 15 giây
- **Recommended delay**: 5 giây để tránh rate limiting

## 🛡️ **Error Handling**

### **Fallback Mechanisms**
- **AI fails**: Sử dụng content gốc
- **JSON parse error**: Default category "Casino & Gaming"
- **API timeout**: Retry với exponential backoff
- **File errors**: Detailed logging và error messages

### **Logging**
- **File**: `csv_processing_[timestamp].log`
- **Console**: Real-time progress với tqdm
- **Levels**: INFO cho success, ERROR cho failures

## 📁 **File Structure**
```
d:\duanmoi\
├── csv_ai_processor.py     ← Main pipeline
├── test_csv_processor.py   ← Test script  
├── config.py              ← API configuration
├── data/
│   ├── posts.csv          ← Input file
│   └── posts_ready_*.csv  ← Output files
└── logs/
    └── csv_processing_*.log
```

## 🎯 **Next Steps**

1. **Batch Processing**: Xử lý tất cả 86 posts
```bash
python csv_ai_processor.py ./data/posts.csv 86 5.0
```

2. **Quality Check**: Review output manually
3. **Integration**: Import vào database hoặc WordPress
4. **Monitoring**: Track performance và costs

---

**Pipeline sẵn sàng xử lý toàn bộ 86 posts với AI content enhancement!** 🚀✨
