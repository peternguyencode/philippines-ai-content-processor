# 🔥 BƯỚC 1: IMPORT DỮ LIỆU JSON VÀO MYSQL

**Mục tiêu**: Chuyển đổi quy trình import dữ liệu bài viết từ file JSON sang MySQL Database thay vì Google Sheets

## 📋 **YÊU CẦU KỸ THUẬT**

### 🐳 **Docker MySQL Container**
- **Host**: localhost
- **Port**: 3308  
- **User**: root
- **Password**: baivietwp_password
- **Database**: mydb
- **Table**: posts (tự động tạo với 15 trường)

### 📊 **Cấu trúc Database Table**
```sql
CREATE TABLE posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    source_title VARCHAR(255),
    status VARCHAR(50) DEFAULT 'imported',
    title TEXT NOT NULL,
    content LONGTEXT,
    original_url TEXT,
    image_url TEXT,
    meta_title TEXT,
    meta_description TEXT,
    created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    keywords TEXT,
    category VARCHAR(100) DEFAULT 'Casino',
    tags TEXT,
    ai_model VARCHAR(50),
    notes TEXT,
    processing_status VARCHAR(50) DEFAULT 'pending',
    
    UNIQUE KEY unique_title (title(255)),
    UNIQUE KEY unique_url (original_url(255))
)
```

## 🚀 **CÁCH SỬ DỤNG**

### **1. Import JSON qua Script Chuyên Dụng**
```powershell
# Activate environment
.\.venv\Scripts\Activate.ps1

# Chạy import script
python import_json_to_mysql.py
```

### **2. Import JSON qua Main Script**
```powershell
# Import với main script
python main.py import bonus365casinoall_posts.json

# Hoặc interactive mode
python main.py
# Chọn option 3: Import JSON vào MySQL
```

### **3. Qua VS Code Tasks**
- `Ctrl+Shift+P` → "Tasks: Run Task"
- Chọn: **"Import JSON to MySQL"**
- Hoặc: **"Import JSON via Main Script"**

### **4. Qua Debug**
- `F5` → Chọn **"Python: Import JSON to MySQL"**

## 🎯 **KẾT QUẢ ĐẠT ĐƯỢC**

### ✅ **Import Statistics**
- **Total processed**: 87 posts
- **Successfully imported**: 86 posts  
- **Duplicates skipped**: 1 post
- **Errors**: 0

### 📊 **Database Status**
- **Table**: `posts` với 86 records
- **Duplicate handling**: Tự động skip posts trùng title/URL
- **Data cleaning**: HTML content được làm sạch
- **Keywords extraction**: Tự động trích xuất keywords từ content

## 🔧 **CHỨC NĂNG CHÍNH**

### **1. Auto Table Creation**
- Tự động tạo bảng `posts` nếu chưa tồn tại
- Cấu trúc 15 trường tương tự Google Sheet
- Indexes và constraints đầy đủ

### **2. Data Processing**
```python
# HTML cleaning
clean_text = re.sub(r'<[^>]+>', '', html_content)

# Keywords extraction
keywords = extract_keywords_from_content(content, title)

# Meta description generation
meta_description = content[:160] + "..." if len(content) > 160 else content
```

### **3. Duplicate Prevention**
- **UNIQUE constraint** trên title và original_url
- **Automatic skip** với warning log
- **No data loss** - chỉ skip, không crash

### **4. Export Functionality**
```powershell
# Export tất cả posts
python main.py export exported_posts.json

# Export giới hạn 10 posts
python main.py export exported_posts.json 10
```

## 📈 **MONITORING & LOGGING**

### **Logs Generated**
- `import_mysql.log` - Chi tiết import process
- Console output với progress tracking
- Error handling với detailed messages

### **Status Tracking**
```python
# Check database status
python main.py
# Option 5: Kiểm tra trạng thái MySQL

# Kết quả:
# Total posts: 86
# By status:
#   - imported: 86
```

## 🔄 **WORKFLOW COMPARISON**

### **Trước (Google Sheets)**
```
JSON → Clean Data → Google Sheets API → 15 columns
```

### **Sau (MySQL)**  
```
JSON → Clean Data → MySQL Database → posts table (15 fields)
```

## 🎛️ **ADVANCED FEATURES**

### **1. Batch Processing**
- Process từng post với error handling
- Progress tracking với detailed logs
- Memory efficient cho large datasets

### **2. Connection Management**
```python
# Auto connection check
if not mysql_helper.check_connection():
    raise ConnectionError("MySQL connection failed!")

# Graceful close
mysql_helper.close()
```

### **3. Export Options**
- Export all hoặc limited records
- JSON format tương thích
- Datetime handling automatic

## 📋 **FILES LIÊN QUAN**

### **Core Files**
- `mysql_helper.py` - MySQL operations class
- `import_json_to_mysql.py` - Standalone import script  
- `main.py` - Updated với MySQL integration
- `bonus365casinoall_posts.json` - Source data (87 posts)

### **Config Files**
- `requirements.txt` - Added mysql-connector-python
- `.vscode/tasks.json` - New MySQL tasks
- `.vscode/launch.json` - Debug configs for MySQL

### **Output Files**
- `import_mysql.log` - Import logs
- `exported_test.json` - Test export (5 posts)
- `exported_posts.json` - Full export option

## 🎉 **THÀNH CÔNG 100%**

✅ **BƯỚC 1 HOÀN THÀNH**: JSON → MySQL Database  
✅ **86/87 posts** imported successfully  
✅ **0 errors** trong quá trình import  
✅ **Full feature** import/export/monitoring  
✅ **Production ready** với error handling

**Next Steps**: Có thể tiếp tục với BƯỚC 2 (đọc từ MySQL để xử lý AI/WordPress)
