# 🌐 phpMyAdmin Setup Guide

## ✅ phpMyAdmin đã được cài đặt thành công!

### 🔗 **Truy cập phpMyAdmin:**
**URL:** http://localhost:8081

### 🔐 **Thông tin đăng nhập:**
- **Server:** `host.docker.internal:3308`
- **Username:** `root`
- **Password:** `baivietwp_password`

---

## 🎯 Hướng dẫn sử dụng:

### 1. **Đăng nhập:**
1. Mở trình duyệt: http://localhost:8081
2. Nhập thông tin đăng nhập ở trên
3. Click "Go" để đăng nhập

### 2. **Xem Database:**
1. Sau khi đăng nhập, click vào database `mydb` bên trái
2. Click vào table `posts` để xem dữ liệu
3. Tab "Browse" hiển thị tất cả records
4. Tab "Structure" hiển thị cấu trúc table

### 3. **Các thao tác chính:**
- **Browse:** Xem dữ liệu posts
- **Search:** Tìm kiếm posts
- **Insert:** Thêm post mới
- **Export:** Export data ra file
- **SQL:** Chạy câu lệnh SQL tùy chỉnh

### 4. **SQL Queries hữu ích:**
```sql
-- Xem tất cả posts
SELECT * FROM posts ORDER BY created_date DESC LIMIT 20;

-- Đếm posts theo status
SELECT status, COUNT(*) FROM posts GROUP BY status;

-- Tìm posts theo keyword
SELECT id, title, status FROM posts 
WHERE title LIKE '%casino%' 
ORDER BY created_date DESC;

-- Xem posts mới nhất
SELECT id, title, status, created_date 
FROM posts 
ORDER BY created_date DESC 
LIMIT 10;
```

---

## 🐳 Docker Commands:

### **Start phpMyAdmin:**
```bash
docker start phpmyadmin
```

### **Stop phpMyAdmin:**
```bash
docker stop phpmyadmin
```

### **Remove phpMyAdmin:**
```bash
docker stop phpmyadmin
docker rm phpmyadmin
```

### **View logs:**
```bash
docker logs phpmyadmin
```

---

## 🛠️ Troubleshooting:

### **Nếu không kết nối được:**
1. Kiểm tra MySQL container đang chạy:
   ```bash
   docker ps
   ```

2. Kiểm tra phpMyAdmin logs:
   ```bash
   docker logs phpmyadmin
   ```

3. Restart phpMyAdmin:
   ```bash
   docker restart phpmyadmin
   ```

### **Nếu quên mật khẩu:**
- Username: `root`
- Password: `baivietwp_password`
- Database: `mydb`

### **Nếu port 8081 bị conflict:**
```bash
docker stop phpmyadmin
docker rm phpmyadmin
docker run --name phpmyadmin -d -p 8082:80 -e PMA_HOST=host.docker.internal -e PMA_PORT=3308 -e PMA_USER=root -e PMA_PASSWORD=baivietwp_password phpmyadmin/phpmyadmin
```

---

## 🎉 **Kết quả:**
- ✅ phpMyAdmin chạy trên: http://localhost:8081
- ✅ Kết nối MySQL database: `mydb`
- ✅ Có thể xem 86 posts đã import
- ✅ Web interface trực quan, dễ sử dụng

---

## 📊 **Current Database Status:**
- **Database:** mydb
- **Table:** posts  
- **Records:** 86 posts
- **Access:** Web-based via phpMyAdmin

**Enjoy browsing your MySQL database! 🚀**
