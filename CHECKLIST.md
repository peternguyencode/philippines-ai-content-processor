# 📋 CHECKLIST TRIỂN KHAI WORDPRESS AUTOMATION

## ✅ 1. Chuẩn bị môi trường
- [x] Python 3.11 đã cài đặt
- [x] Virtual environment đã tạo
- [x] Thư viện Python đã cài đặt
- [ ] Kiểm tra kết nối Internet

## ✅ 2. Cấu hình API Keys

### OpenAI API
- [ ] Đăng ký tài khoản OpenAI
- [ ] Tạo API key tại https://platform.openai.com/api-keys
- [ ] Nạp credit vào tài khoản (tối thiểu $5)
- [ ] Điền OPENAI_API_KEY vào file .env

### Google Gemini API (Optional)
- [ ] Đăng ký Google AI Studio
- [ ] Tạo API key tại https://makersuite.google.com/app/apikey
- [ ] Điền GEMINI_API_KEY vào file .env

## ✅ 3. Cấu hình Google Sheets

### Tạo Google Service Account
- [ ] Truy cập https://console.cloud.google.com/
- [ ] Tạo project mới hoặc chọn project
- [ ] Enable Google Sheets API
- [ ] Enable Google Drive API
- [ ] Tạo Service Account
- [ ] Download credentials JSON
- [ ] Đổi tên file thành 'creds.json'
- [ ] Copy creds.json vào thư mục project

### Tạo Google Sheet
- [ ] Tạo Google Sheet mới
- [ ] Copy Sheet ID từ URL
- [ ] Chia sẻ Sheet với email Service Account
- [ ] Điền GOOGLE_SHEET_ID vào file .env

## ✅ 4. Cấu hình WordPress

### Chuẩn bị WordPress Site
- [ ] WordPress site đã online
- [ ] Cài đặt plugin Yoast SEO (optional)
- [ ] Kiểm tra REST API enabled

### Tạo Application Password
- [ ] Login WordPress Admin
- [ ] Vào Users → Your Profile
- [ ] Scroll xuống "Application Passwords"  
- [ ] Tạo password mới với tên "Python Automation"
- [ ] Copy username và app password
- [ ] Điền WP_USERNAME và WP_PASSWORD vào .env
- [ ] Điền WP_URL vào .env (ví dụ: https://yoursite.com)

## ✅ 5. Test hệ thống

### Chạy test tổng thể
- [ ] Chạy: `python test_system.py`
- [ ] Kiểm tra tất cả components PASS
- [ ] Nếu có lỗi, sửa cấu hình và test lại

### Test từng component
- [ ] Test Google Sheets connection
- [ ] Test AI API (sinh content mẫu)
- [ ] Test WordPress API connection  
- [ ] Test upload ảnh lên WordPress

## ✅ 6. Thiết lập dữ liệu mẫu

### Tạo dữ liệu test
- [ ] Chạy: `python main.py setup`
- [ ] Kiểm tra Google Sheet có header và data mẫu
- [ ] Thêm vài prompt test thủ công

### Test xử lý 1 bài
- [ ] Chạy: `python main.py single`
- [ ] Kiểm tra bài viết được tạo trên WordPress
- [ ] Kiểm tra ảnh cover được set
- [ ] Kiểm tra meta SEO
- [ ] Kiểm tra trạng thái cập nhật trong Sheet

## ✅ 7. Triển khai production

### Batch processing
- [ ] Thêm nhiều prompt vào Google Sheet
- [ ] Chạy: `run_batch.bat`
- [ ] Theo dõi tiến trình xử lý
- [ ] Kiểm tra kết quả trong Sheet và WordPress

### Monitoring và tối ưu
- [ ] Điều chỉnh CONCURRENT_REQUESTS phù hợp
- [ ] Điều chỉnh REQUEST_DELAY tránh rate limit
- [ ] Monitor usage quota của APIs
- [ ] Thiết lập backup cho creds.json

## ✅ 8. Bảo mật và backup

### Bảo mật
- [ ] Không commit .env và creds.json lên Git
- [ ] Giữ bí mật các API keys
- [ ] Định kỳ rotate Application Password
- [ ] Giới hạn quyền Service Account

### Backup
- [ ] Backup file .env
- [ ] Backup file creds.json  
- [ ] Backup Google Sheet ID
- [ ] Document toàn bộ quy trình

## 🎯 Sẵn sàng sử dụng!

Khi tất cả checklist đã hoàn thành:

1. **Hàng ngày**: Thêm prompt vào Google Sheet, chạy `run_batch.bat`
2. **Tương tác**: Chạy `run_interactive.bat` để control chi tiết  
3. **Monitor**: Kiểm tra Google Sheet để theo dõi trạng thái
4. **Troubleshoot**: Xem Error_Log column nếu có lỗi

---

💡 **Lưu ý quan trọng**:
- Bắt đầu với ít bài để test trước
- Monitor API usage để tránh vượt quota
- Backup dữ liệu quan trọng thường xuyên
- Giữ các API key an toàn
