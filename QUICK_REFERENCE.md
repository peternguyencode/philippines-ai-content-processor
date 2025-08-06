# 🚀 **QUICK REFERENCE - CÁC LỆNH CHẠY HỆ THỐNG**

## 📊 **HIỆN TRẠNG**
- **Database**: 86 posts gốc → 1 đã xử lý → **85 posts còn lại**
- **CSV File**: 86 posts ready for processing
- **Backup**: ✅ Complete backup created
- **Systems**: ✅ Both pipelines tested & working

---

## 🎯 **LỆNH NHANH - DATABASE PIPELINE**

### **Test & Stats**
```bash
python ai_content_processor.py single    # Test 1 post
python ai_content_processor.py stats     # Xem thống kê
```

### **Production Batch**
```bash  
# 5 posts (safe test)
python ai_content_processor.py batch 5 45.0

# 10 posts  
python ai_content_processor.py batch 10 45.0

# Full batch (85 posts remaining)
python ai_content_processor.py batch 85 45.0
```

**Output:** MySQL `posts_ai` table + DALL-E 3 images  
**Time:** ~45 giây/post | **Cost:** ~$0.04/post

---

## 📝 **LỆNH NHANH - CSV PIPELINE**

### **Test & Small Batch**
```bash
python test_csv_processor.py                     # Test 2 posts
python csv_ai_processor.py ./data/posts.csv 10 5.0  # 10 posts
```

### **Production Batch**
```bash
python run_full_batch.py                         # Full 86 posts
# OR
python csv_ai_processor.py ./data/posts.csv 86 5.0
```

**Output:** `./data/posts_ready_[timestamp].csv`  
**Time:** ~15 giây/post | **Cost:** ~$0.002/post

---

## ⚡ **VS CODE TASKS** 
`Ctrl+Shift+P` → "Tasks: Run Task" → Choose:

### **Database Tasks**
- **AI Process 5 Posts** (45s delay)
- **AI Process 3 Posts (Safe)** (50s delay)

### **CSV Tasks**  
- **CSV Test Processing** (2 posts)
- **CSV Small Batch** (10 posts)
- **CSV Full Batch** (86 posts)

---

## 🔍 **MONITORING**

### **Database**
```bash
# Web interface
http://localhost:8081

# Command stats
python ai_content_processor.py stats
```

### **CSV**
```bash
# Check output files
dir ./data/posts_ready_*.csv

# View logs  
type csv_processing_*.log
```

---

## 🎯 **RECOMMENDED NEXT STEPS**

### **Step 1: Choose Pipeline**
```bash
# High-quality với images (expensive)
python ai_content_processor.py batch 5 45.0

# Fast paraphrase (cheap)  
python csv_ai_processor.py ./data/posts.csv 5 5.0
```

### **Step 2: Production Run**
```bash
# Database: 85 posts, ~64 phút, ~$3.40
python ai_content_processor.py batch 85 45.0

# CSV: 86 posts, ~22 phút, ~$0.17  
python run_full_batch.py
```

---

## 🛡️ **BACKUP & SAFETY**

### **Current Backup**
```
d:\backups\duanmoi_backup_20250806_090921\
- Full project files ✅
- Database SQL dump ✅  
- ZIP archive (468 KB) ✅
```

### **New Backup Before Production**
```bash
# Quick backup database only
mysqldump -h localhost -P 3308 -u root -pbaivietwp_password mydb > backup_before_batch.sql
```

---

**🚀 Tất cả hệ thống ready! Chọn pipeline và bắt đầu processing! ✨**
