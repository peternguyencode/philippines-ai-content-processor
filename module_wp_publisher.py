#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MODULE 3: WORDPRESS PUBLISHER
Chỉ xử lý việc đăng bài lên WordPress
"""

import requests
import base64
from typing import Dict, Optional, Any
import json
from urllib.parse import urljoin

class WordPressPublisher:
    """Module độc lập publish WordPress"""
    
    def __init__(self, wp_url: str, username: str, password: str):
        self.wp_url = wp_url.rstrip('/')
        self.username = username
        self.password = password
        self.api_url = f"{self.wp_url}/wp-json/wp/v2/"
        self.auth_header = self._create_auth_header()
        self._test_connection()
    
    def _create_auth_header(self) -> str:
        """Tạo Basic Auth header"""
        credentials = f"{self.username}:{self.password}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        return f"Basic {encoded_credentials}"
    
    def _test_connection(self):
        """Test kết nối WordPress"""
        try:
            response = requests.get(
                f"{self.api_url}users/me",
                headers={"Authorization": self.auth_header},
                timeout=10
            )
            
            if response.status_code == 200:
                user_data = response.json()
                print(f"✅ [WP PUBLISHER] Connected as: {user_data.get('name', 'Unknown')}")
            else:
                print(f"❌ [WP PUBLISHER] Auth failed: {response.status_code}")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"❌ [WP PUBLISHER] Connection error: {str(e)}")
    
    def upload_image(self, image_data: bytes, filename: str) -> Optional[int]:
        """
        Upload ảnh lên WordPress Media Library
        Returns: Media ID hoặc None nếu fail
        """
        try:
            headers = {
                "Authorization": self.auth_header,
                "Content-Type": "image/jpeg",
                "Content-Disposition": f'attachment; filename="{filename}"'
            }
            
            response = requests.post(
                f"{self.api_url}media",
                headers=headers,
                data=image_data,
                timeout=30
            )
            
            if response.status_code == 201:
                media_data = response.json()
                media_id = media_data['id']
                image_url = media_data['source_url']
                
                print(f"✅ [WP PUBLISHER] Uploaded image ID: {media_id}")
                print(f"   URL: {image_url}")
                return media_id
            else:
                print(f"❌ [WP PUBLISHER] Upload failed: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ [WP PUBLISHER] Upload error: {str(e)}")
            return None
    
    def create_post(self, content_data: Dict[str, Any], featured_image_id: Optional[int] = None) -> Optional[str]:
        """
        Tạo post WordPress
        Returns: Post URL hoặc None nếu fail
        """
        try:
            # Chuẩn bị data
            post_data = {
                "title": content_data.get('title', 'Untitled'),
                "content": content_data.get('content', ''),
                "excerpt": content_data.get('excerpt', ''),
                "status": "publish",
                "categories": [1],  # Default category
                "tags": self._get_tag_ids(content_data.get('tags', [])),
            }
            
            # Thêm featured image nếu có
            if featured_image_id:
                post_data["featured_media"] = featured_image_id
            
            # Thêm SEO meta (nếu có plugin hỗ trợ)
            if content_data.get('meta_title') or content_data.get('meta_desc'):
                post_data["meta"] = {
                    "_yoast_wpseo_title": content_data.get('meta_title', ''),
                    "_yoast_wpseo_metadesc": content_data.get('meta_desc', '')
                }
            
            headers = {
                "Authorization": self.auth_header,
                "Content-Type": "application/json"
            }
            
            response = requests.post(
                f"{self.api_url}posts",
                headers=headers,
                json=post_data,
                timeout=30
            )
            
            if response.status_code == 201:
                post_info = response.json()
                post_url = post_info['link']
                post_id = post_info['id']
                
                print(f"✅ [WP PUBLISHER] Created post ID: {post_id}")
                print(f"   URL: {post_url}")
                return post_url
            else:
                print(f"❌ [WP PUBLISHER] Post creation failed: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ [WP PUBLISHER] Create post error: {str(e)}")
            return None
    
    def _get_tag_ids(self, tag_names: list) -> list:
        """Chuyển đổi tag names thành IDs"""
        try:
            tag_ids = []
            
            for tag_name in tag_names:
                # Tìm tag existing
                response = requests.get(
                    f"{self.api_url}tags",
                    headers={"Authorization": self.auth_header},
                    params={"search": tag_name, "per_page": 1},
                    timeout=10
                )
                
                if response.status_code == 200:
                    tags = response.json()
                    if tags:
                        tag_ids.append(tags[0]['id'])
                        continue
                
                # Tạo tag mới nếu không tìm thấy
                new_tag_response = requests.post(
                    f"{self.api_url}tags",
                    headers={
                        "Authorization": self.auth_header,
                        "Content-Type": "application/json"
                    },
                    json={"name": tag_name},
                    timeout=10
                )
                
                if new_tag_response.status_code == 201:
                    new_tag = new_tag_response.json()
                    tag_ids.append(new_tag['id'])
                    print(f"✅ [WP PUBLISHER] Created tag: {tag_name}")
            
            return tag_ids
            
        except Exception as e:
            print(f"❌ [WP PUBLISHER] Tag processing error: {str(e)}")
            return []
    
    def publish_complete_post(self, content_data: Dict[str, Any], image_data: Optional[bytes] = None) -> Optional[str]:
        """
        Publish bài viết hoàn chỉnh (content + image)
        Returns: Post URL hoặc None nếu fail
        """
        try:
            featured_image_id = None
            
            # Upload ảnh trước (nếu có)
            if image_data:
                title_slug = content_data.get('title', 'image').lower().replace(' ', '-')
                filename = f"{title_slug}.jpg"
                featured_image_id = self.upload_image(image_data, filename)
            
            # Tạo post
            post_url = self.create_post(content_data, featured_image_id)
            
            if post_url:
                print(f"✅ [WP PUBLISHER] Published complete post: {post_url}")
                return post_url
            else:
                print("❌ [WP PUBLISHER] Failed to publish post")
                return None
                
        except Exception as e:
            print(f"❌ [WP PUBLISHER] Publish error: {str(e)}")
            return None
    
    def get_post_info(self, post_id: int) -> Optional[Dict[str, Any]]:
        """Lấy thông tin post"""
        try:
            response = requests.get(
                f"{self.api_url}posts/{post_id}",
                headers={"Authorization": self.auth_header},
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ [WP PUBLISHER] Get post info failed: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ [WP PUBLISHER] Get post info error: {str(e)}")
            return None
    
    def update_post(self, post_id: int, update_data: Dict[str, Any]) -> bool:
        """Cập nhật post existing"""
        try:
            headers = {
                "Authorization": self.auth_header,
                "Content-Type": "application/json"
            }
            
            response = requests.post(
                f"{self.api_url}posts/{post_id}",
                headers=headers,
                json=update_data,
                timeout=30
            )
            
            if response.status_code == 200:
                print(f"✅ [WP PUBLISHER] Updated post ID: {post_id}")
                return True
            else:
                print(f"❌ [WP PUBLISHER] Update failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ [WP PUBLISHER] Update error: {str(e)}")
            return False

# Test module
if __name__ == "__main__":
    from config import Config
    
    # Test WordPress Publisher
    wp_pub = WordPressPublisher(
        wp_url=Config.WP_URL or "",
        username=Config.WP_USERNAME or "",
        password=Config.WP_PASSWORD or ""
    )
    
    # Test data
    test_content = {
        'title': 'Test Post from Module',
        'content': '<p>This is a test post from the modular WordPress publisher.</p>',
        'excerpt': 'Test excerpt',
        'meta_title': 'Test SEO Title',
        'meta_desc': 'Test SEO description',
        'tags': ['test', 'module']
    }
    
    # Test tạo post
    post_url = wp_pub.create_post(test_content)
    if post_url:
        print(f"✅ Test post created: {post_url}")
    else:
        print("❌ Test post creation failed")
