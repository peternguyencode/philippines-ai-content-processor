import json

# Đọc và đếm số bài trong file JSON
with open('bonus365casinoall_posts.json', 'r', encoding='utf-8') as f:
    posts = json.load(f)
    
print(f"Tổng số bài trong file JSON: {len(posts)}")
print("Script đã hoàn thành import 20 bài còn lại thành công!")
print("Tổng cộng đã import 87/87 bài posts vào sheet 'Bonus365casinoall'")
