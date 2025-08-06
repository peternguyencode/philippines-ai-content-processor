# 🔍 Hướng Dẫn Xem MySQL Database

## Các Cách Xem Database

### 1. Quick Check (Kiểm tra nhanh)
```bash
python db_check.py
```
**Hoặc sử dụng VS Code Task:**
- Ctrl+Shift+P → `Tasks: Run Task` → `Quick Database Check`

**Hiển thị:**
- ✅ MySQL connection status
- 📁 Danh sách tables
- 📄 Tổng số posts
- 🕒 3 posts mới nhất

---

### 2. Database Browser (Interactive)
```bash
python db_browser.py
```
**Hoặc sử dụng VS Code Task:**
- Ctrl+Shift+P → `Tasks: Run Task` → `Database Browser (Interactive)`

**Features:**
- 📊 Database summary (tổng quan)
- 📋 List posts với filter
- 🔍 Search posts theo keyword
- 💾 Export posts to JSON
- 🎮 Interactive commands

**Interactive Commands:**
```
db> summary          # Xem tổng quan
db> list 20         # List 20 posts mới nhất
db> search casino   # Tìm posts chứa "casino"
db> export 50       # Export 50 posts to JSON
db> help           # Xem help
db> quit           # Thoát
```

---

### 3. Full Database Viewer
```bash
python view_database.py
```
**Hoặc sử dụng VS Code Task:**
- Ctrl+Shift+P → `Tasks: Run Task` → `View Database`

**Features:**
- 📊 Database overview với statistics
- 📄 Latest posts display
- 🎮 Menu actions:
  1. Xem chi tiết 1 post
  2. Export 10 posts mới nhất
  3. Search posts by keyword
  4. Xem tất cả categories

---

### 4. Sử dụng MySQL Client Tools

#### A. MySQL Workbench (Recommended)
1. Download từ: https://dev.mysql.com/downloads/workbench/
2. Kết nối với:
   - Host: `localhost`
   - Port: `3308`
   - Username: `root`
   - Password: `baivietwp_password`
   - Schema: `mydb`

#### B. phpMyAdmin (Web-based)
```bash
# Run phpMyAdmin with Docker
docker run --name phpmyadmin -d --link mysql-container:db -p 8080:80 phpmyadmin/phpmyadmin
```
Truy cập: http://localhost:8080

#### C. DBeaver (Free)
1. Download từ: https://dbeaver.io/download/
2. Tạo connection với thông tin MySQL

---

### 5. Command Line MySQL Client
```bash
# Nếu có MySQL client installed
mysql -h localhost -P 3308 -u root -p

# Sau khi đăng nhập:
USE mydb;
SHOW TABLES;
SELECT COUNT(*) FROM posts;
SELECT * FROM posts LIMIT 5;
```

---

### 6. VS Code Extensions cho Database

#### A. MySQL Extension
- Extension: `cweijan.vscode-mysql-client2`
- Sau khi install, add connection với thông tin MySQL

#### B. SQLTools
- Extension: `mtxr.sqltools`
- Support nhiều database types

---

## Current Database Status

✅ **Database đang hoạt động:**
- Host: localhost:3308
- Database: mydb
- Table: posts
- Records: 86 posts
- Status: Ready for use

## Files Created

1. `db_check.py` - Quick database check
2. `db_browser.py` - Interactive database browser  
3. `view_database.py` - Full database viewer
4. VS Code Tasks đã được thêm vào `.vscode/tasks.json`

## Troubleshooting

### Nếu connection failed:
1. Kiểm tra Docker Desktop đang chạy
2. Kiểm tra MySQL container đang active:
   ```bash
   docker ps
   ```
3. Restart MySQL container nếu cần:
   ```bash
   docker restart <mysql-container-name>
   ```

### Nếu scripts báo lỗi:
1. Activate virtual environment:
   ```bash
   .venv\Scripts\activate
   ```
2. Install packages nếu thiếu:
   ```bash
   pip install mysql-connector-python
   ```
