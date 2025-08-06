import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Cấu hình chung cho toàn bộ ứng dụng"""

    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    # WordPress
    WP_URL = os.getenv("WP_URL")
    WP_USERNAME = os.getenv("WP_USERNAME")
    WP_PASSWORD = os.getenv("WP_PASSWORD")
    WP_API_URL = f"{WP_URL}/wp-json/wp/v2" if WP_URL else None

    # Google Sheets
    GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
    GOOGLE_CREDS_FILE = os.getenv("GOOGLE_CREDS_FILE", "creds.json")

    # AI Configuration
    DEFAULT_AI_PROVIDER = os.getenv("DEFAULT_AI_PROVIDER", "openai")
    IMAGE_AI_PROVIDER = os.getenv("IMAGE_AI_PROVIDER", "openai")
    AI_MODEL = os.getenv("AI_MODEL", "gpt-3.5-turbo")
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", 2000))
    IMAGE_SIZE = os.getenv("IMAGE_SIZE", "1024x1024")

    # Processing
    BATCH_SIZE = int(os.getenv("BATCH_SIZE", 5))
    CONCURRENT_REQUESTS = int(os.getenv("CONCURRENT_REQUESTS", 3))
    REQUEST_DELAY = int(os.getenv("REQUEST_DELAY", 2))

    # Google Sheet columns mapping
    SHEET_COLUMNS = {
        "prompt": "A",  # Prompt/yêu cầu viết bài
        "status": "B",  # Trạng thái xử lý
        "title": "C",  # Tiêu đề bài viết
        "content": "D",  # Nội dung bài viết
        "wp_url": "E",  # URL bài đăng trên WP
        "image_url": "F",  # URL ảnh cover
        "meta_title": "G",  # Meta title SEO
        "meta_desc": "H",  # Meta description SEO
        "created_date": "I",  # Ngày tạo
        "error_log": "J",  # Log lỗi nếu có
    }

    @classmethod
    def validate_config(cls):
        """Kiểm tra cấu hình cần thiết"""
        required_vars = [
            "OPENAI_API_KEY",
            "WP_URL",
            "WP_USERNAME",
            "WP_PASSWORD",
            "GOOGLE_SHEET_ID",
        ]

        missing_vars = []
        for var in required_vars:
            if not getattr(cls, var):
                missing_vars.append(var)

        if missing_vars:
            raise ValueError(f"Thiếu cấu hình: {', '.join(missing_vars)}")

        return True
