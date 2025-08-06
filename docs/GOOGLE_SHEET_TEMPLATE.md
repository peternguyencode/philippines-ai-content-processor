# 📊 CẤU TRÚC GOOGLE SHEET MẪU

## Cấu trúc cột (Row 1 - Header)

| Cột | Tên cột | Mô tả | Ví dụ |
|-----|---------|-------|-------|
| A | Prompt | Yêu cầu viết bài từ người dùng | "Viết bài về lợi ích của AI trong marketing" |
| B | Status | Trạng thái xử lý | pending/processing/completed/error |
| C | Title | Tiêu đề bài viết do AI sinh | "10 Lợi Ích Tuyệt Vời Của AI Trong Marketing" |
| D | Content | Nội dung bài viết (rút gọn) | "AI đang cách mạng hóa marketing..." |
| E | WP_URL | Link bài viết trên WordPress | "https://yoursite.com/ai-marketing" |
| F | Image_URL | Link ảnh cover | "https://yoursite.com/wp-content/uploads/ai-image.png" |
| G | Meta_Title | Meta title SEO | "AI Marketing: 10 Lợi Ích Không Thể Bỏ Qua" |
| H | Meta_Desc | Meta description SEO | "Khám phá 10 lợi ích tuyệt vời của AI trong marketing..." |
| I | Created_Date | Ngày tạo | "2025-08-04 14:30:25" |
| J | Error_Log | Log lỗi nếu có | "OpenAI API rate limit exceeded" |

## Dữ liệu mẫu (Row 2+)

### Row 2 - Bài viết về AI Marketing
| A | B | C | D | E | F | G | H | I | J |
|---|---|---|---|---|---|---|---|---|---|
| Viết bài về lợi ích của AI trong marketing | pending | | | | | | | | |

### Row 3 - Bài viết về SEO
| A | B | C | D | E | F | G | H | I | J |
|---|---|---|---|---|---|---|---|---|---|
| Hướng dẫn SEO website cho người mới bắt đầu | pending | | | | | | | | |

### Row 4 - Review sản phẩm
| A | B | C | D | E | F | G | H | I | J |
|---|---|---|---|---|---|---|---|---|---|
| Review chi tiết iPhone 15 Pro Max | pending | | | | | | | | |

### Row 5 - Bài viết đã xử lý thành công
| A | B | C | D | E | F | G | H | I | J |
|---|---|---|---|---|---|---|---|---|---|
| Cách kiếm tiền online 2025 | completed | 7 Cách Kiếm Tiền Online Hiệu Quả 2025 | Kiếm tiền online không còn là... | https://site.com/kiem-tien-online | https://site.com/image.png | Kiếm Tiền Online 2025: 7 Cách Hiệu Quả | Khám phá 7 cách kiếm tiền online... | 2025-08-04 10:15:30 | |

### Row 6 - Bài viết có lỗi
| A | B | C | D | E | F | G | H | I | J |
|---|---|---|---|---|---|---|---|---|---|
| Viết bài về chủ đề phức tạp | error | | | | | | | 2025-08-04 11:20:15 | OpenAI API quota exceeded |

## Cách sử dụng Google Sheet

### 1. Tạo Sheet mới
1. Truy cập https://sheets.google.com
2. Tạo sheet mới
3. Đặt tên sheet (ví dụ: "WordPress Auto Content")

### 2. Thiết lập header
- Copy dòng header vào row 1
- Hoặc chạy script `python main.py setup`

### 3. Thêm prompt
- Thêm prompt vào cột A
- Để cột B trống hoặc ghi "pending"
- Các cột khác để trống

### 4. Chia sẻ với Service Account
1. Nhấn nút "Share" 
2. Thêm email Service Account
3. Cấp quyền "Editor"

### 5. Lấy Sheet ID
- Từ URL: `https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit`
- Copy {SHEET_ID} vào file .env

## Trạng thái xử lý (Status Column)

| Trạng thái | Mô tả | Màu gợi ý |
|------------|-------|-----------|
| `pending` | Chưa xử lý | Màu vàng |
| `processing` | Đang xử lý | Màu xanh |
| `completed` | Hoàn thành | Màu xanh lá |
| `error` | Có lỗi | Màu đỏ |

## Tips sử dụng Google Sheet

### Định dạng có điều kiện (Conditional Formatting)
1. Chọn cột Status (B)
2. Format → Conditional formatting
3. Thiết lập màu cho từng trạng thái

### Filter và Sort
- Sử dụng filter để xem các bài viết theo trạng thái
- Sort theo Created_Date để xem bài mới nhất

### Validation
- Tạo dropdown cho cột Status với các giá trị hợp lệ
- Validation cho cột Prompt (không được rỗng)

### Formulas hữu ích
```
# Đếm số bài completed
=COUNTIF(B:B,"completed")

# Đếm số bài error  
=COUNTIF(B:B,"error")

# Tỷ lệ thành công
=COUNTIF(B:B,"completed")/COUNTA(B:B)-1
```

## Import dữ liệu từ CSV

Nếu bạn có danh sách prompt trong CSV:

```csv
Prompt,Status
"Viết bài về AI trong marketing",pending
"Hướng dẫn SEO website",pending
"Review iPhone 15",pending
```

1. File → Import → Upload CSV
2. Chọn "Replace current sheet" hoặc "Insert new sheet"

## Export kết quả

Để backup hoặc phân tích:
1. File → Download → Excel (.xlsx) hoặc CSV
2. Chọn sheet cần export
3. Lưu file backup định kỳ

---

💡 **Lưu ý**: 
- Luôn backup Google Sheet trước khi chạy batch lớn
- Giới hạn 1000 hàng/lần chạy để tránh quá tải
- Sử dụng filter để focus vào những bài cần xử lý
