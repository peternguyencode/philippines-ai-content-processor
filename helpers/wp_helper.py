import requests
import json
import time
import base64
from urllib.parse import urljoin
from typing import Optional, Dict, Any, List
from config import Config

class WPHelper:
    """Lớp xử lý WordPress REST API"""
    
    def __init__(self):
        self.base_url = Config.WP_API_URL
        self.auth = (Config.WP_USERNAME, Config.WP_PASSWORD)
        self.session = requests.Session()
        self.session.auth = self.auth
        
        # Test kết nối
        self._test_connection()
    
    def _test_connection(self):
        """Test kết nối đến WordPress API"""
        try:
            response = self.session.get(f"{self.base_url}/users/me")
            if response.status_code == 200:
                user_info = response.json()
                print(f"✅ Kết nối WordPress thành công! User: {user_info.get('name')}")
            else:
                print(f"⚠️ Cảnh báo kết nối WP: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Lỗi kết nối WordPress: {str(e)}")
    
    def create_post(self, title: str, content: str, status: str = 'draft') -> Optional[Dict[str, Any]]:
        """
        Tạo bài viết mới trên WordPress
        
        Args:
            title: Tiêu đề bài viết
            content: Nội dung bài viết (HTML)
            status: Trạng thái bài viết ('draft', 'publish', 'private')
        
        Returns:
            Dict chứa thông tin bài viết đã tạo hoặc None nếu lỗi
        """
        try:
            post_data = {
                'title': title,
                'content': content,
                'status': status,
                'format': 'standard'
            }
            
            response = self.session.post(
                f"{self.base_url}/posts",
                json=post_data,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 201:
                post_info = response.json()
                print(f"✅ Đã tạo bài viết: {post_info['title']['rendered']}")
                print(f"🔗 URL: {post_info['link']}")
                return post_info
            else:
                print(f"❌ Lỗi tạo bài viết: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Exception tạo bài viết: {str(e)}")
            return None
    
    def upload_image(self, image_url: str, filename: str = None) -> Optional[Dict[str, Any]]:
        """
        Upload ảnh từ URL lên WordPress Media Library
        
        Args:
            image_url: URL của ảnh cần upload
            filename: Tên file (optional)
        
        Returns:
            Dict chứa thông tin ảnh đã upload hoặc None nếu lỗi
        """
        try:
            # Download ảnh từ URL
            img_response = requests.get(image_url, timeout=30)
            if img_response.status_code != 200:
                print(f"❌ Không tải được ảnh từ URL: {image_url}")
                return None
            
            # Tạo filename nếu chưa có
            if not filename:
                filename = f"ai_generated_{int(time.time())}.png"
            
            # Chuẩn bị data để upload
            files = {
                'file': (filename, img_response.content, 'image/png')
            }
            
            headers = {
                'Content-Disposition': f'attachment; filename="{filename}"'
            }
            
            # Upload lên WordPress
            response = self.session.post(
                f"{self.base_url}/media",
                files=files,
                headers=headers
            )
            
            if response.status_code == 201:
                media_info = response.json()
                print(f"✅ Đã upload ảnh: {media_info['source_url']}")
                return media_info
            else:
                print(f"❌ Lỗi upload ảnh: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Exception upload ảnh: {str(e)}")
            return None
    
    def set_featured_image(self, post_id: int, media_id: int) -> bool:
        """
        Đặt ảnh featured cho bài viết
        
        Args:
            post_id: ID của bài viết
            media_id: ID của ảnh trong media library
        
        Returns:
            True nếu thành công, False nếu lỗi
        """
        try:
            update_data = {
                'featured_media': media_id
            }
            
            response = self.session.post(
                f"{self.base_url}/posts/{post_id}",
                json=update_data,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                print(f"✅ Đã đặt featured image cho bài {post_id}")
                return True
            else:
                print(f"❌ Lỗi đặt featured image: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Exception đặt featured image: {str(e)}")
            return False
    
    def update_post_meta(self, post_id: int, meta_title: str, meta_description: str) -> bool:
        """
        Cập nhật meta SEO cho bài viết (dành cho Yoast SEO)
        
        Args:
            post_id: ID của bài viết
            meta_title: Meta title SEO
            meta_description: Meta description SEO
        
        Returns:
            True nếu thành công, False nếu lỗi
        """
        try:
            # Cập nhật Yoast SEO meta
            meta_data = {
                'meta': {
                    '_yoast_wpseo_title': meta_title,
                    '_yoast_wpseo_metadesc': meta_description,
                    '_yoast_wpseo_focuskw': '',  # Có thể thêm focus keyword
                }
            }
            
            response = self.session.post(
                f"{self.base_url}/posts/{post_id}",
                json=meta_data,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                print(f"✅ Đã cập nhật SEO meta cho bài {post_id}")
                return True
            else:
                print(f"❌ Lỗi cập nhật SEO meta: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Exception cập nhật SEO meta: {str(e)}")
            return False
    
    def publish_post(self, post_id: int) -> bool:
        """
        Publish bài viết (chuyển từ draft sang publish)
        
        Args:
            post_id: ID của bài viết
        
        Returns:
            True nếu thành công, False nếu lỗi
        """
        try:
            update_data = {
                'status': 'publish'
            }
            
            response = self.session.post(
                f"{self.base_url}/posts/{post_id}",
                json=update_data,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                post_info = response.json()
                print(f"✅ Đã publish bài viết: {post_info['link']}")
                return True
            else:
                print(f"❌ Lỗi publish bài viết: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Exception publish bài viết: {str(e)}")
            return False
    
    def process_complete_post(self, title: str, content: str, image_url: str = None, 
                            meta_title: str = None, meta_description: str = None,
                            auto_publish: bool = False) -> Optional[Dict[str, Any]]:
        """
        Xử lý hoàn chỉnh một bài viết: tạo post, upload ảnh, set meta, publish
        
        Returns:
            Dict chứa thông tin bài viết hoàn chỉnh hoặc None nếu lỗi
        """
        try:
            # 1. Tạo bài viết draft
            post_info = self.create_post(title, content, 'draft')
            if not post_info:
                return None
            
            post_id = post_info['id']
            result = {
                'post_id': post_id,
                'post_url': post_info['link'],
                'title': post_info['title']['rendered']
            }
            
            # 2. Upload và set featured image
            if image_url:
                media_info = self.upload_image(image_url)
                if media_info:
                    media_id = media_info['id']
                    if self.set_featured_image(post_id, media_id):
                        result['featured_image'] = media_info['source_url']
                        result['media_id'] = media_id
            
            # 3. Cập nhật SEO meta
            if meta_title and meta_description:
                if self.update_post_meta(post_id, meta_title, meta_description):
                    result['meta_title'] = meta_title
                    result['meta_description'] = meta_description
            
            # 4. Publish nếu được yêu cầu
            if auto_publish:
                if self.publish_post(post_id):
                    result['status'] = 'published'
                else:
                    result['status'] = 'draft'
            else:
                result['status'] = 'draft'
            
            print(f"✅ Hoàn thành xử lý bài viết: {title}")
            return result
            
        except Exception as e:
            print(f"❌ Lỗi xử lý hoàn chỉnh bài viết: {str(e)}")
            return None
    
    def get_post_info(self, post_id: int) -> Optional[Dict[str, Any]]:
        """Lấy thông tin chi tiết của một bài viết"""
        try:
            response = self.session.get(f"{self.base_url}/posts/{post_id}")
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Không tìm thấy bài viết {post_id}")
                return None
                
        except Exception as e:
            print(f"❌ Lỗi lấy thông tin bài viết: {str(e)}")
            return None

# Test function
if __name__ == "__main__":
    try:
        Config.validate_config()
        wp = WPHelper()
        
        # Test tạo bài viết
        test_title = "Test bài viết từ Python"
        test_content = "<h2>Đây là test content</h2><p>Nội dung test từ Python script.</p>"
        
        result = wp.process_complete_post(
            title=test_title,
            content=test_content,
            meta_title="Test Meta Title",
            meta_description="Test meta description for SEO",
            auto_publish=False
        )
        
        if result:
            print(f"🎉 Test thành công! Post ID: {result['post_id']}")
        else:
            print("❌ Test thất bại!")
            
    except Exception as e:
        print(f"Lỗi test: {str(e)}")
