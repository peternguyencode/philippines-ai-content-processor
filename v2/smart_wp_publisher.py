#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
V2 - MODULE 3: SMART WORDPRESS PUBLISHER
Cải tiến: Media optimization, SEO automation, Multi-site support, Content scheduling
"""

import requests
import base64
from typing import Dict, Optional, Any, List, Tuple, Union
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from urllib.parse import urljoin, urlparse
import json
import time
import hashlib
from PIL import Image
import io
import mimetypes
from enum import Enum

class PostStatus(Enum):
    DRAFT = "draft"
    PUBLISHED = "publish"
    PRIVATE = "private"
    SCHEDULED = "future"

class MediaType(Enum):
    IMAGE = "image"
    VIDEO = "video"
    DOCUMENT = "document"

@dataclass
class MediaItem:
    """Enhanced media item structure"""
    file_data: bytes
    filename: str
    media_type: MediaType
    alt_text: str = ""
    caption: str = ""
    title: str = ""
    optimize: bool = True
    
@dataclass
class PostData:
    """Enhanced post data structure"""
    title: str
    content: str
    excerpt: str = ""
    status: PostStatus = PostStatus.PUBLISHED
    categories: List[int] = None
    tags: List[str] = None
    featured_media: Optional[MediaItem] = None
    meta_title: str = ""
    meta_desc: str = ""
    custom_meta: Dict[str, Any] = None
    scheduled_date: Optional[datetime] = None
    author_id: Optional[int] = None
    
    def __post_init__(self):
        if self.categories is None:
            self.categories = []
        if self.tags is None:
            self.tags = []
        if self.custom_meta is None:
            self.custom_meta = {}

class SmartWPPublisher:
    """V2 - Smart WordPress Publisher với advanced features"""
    
    def __init__(self, wp_url: str, username: str, password: str):
        self.wp_url = wp_url.rstrip('/')
        self.username = username
        self.password = password
        self.api_url = f"{self.wp_url}/wp-json/wp/v2/"
        self.auth_header = self._create_auth_header()
        
        # Cache for categories, tags, users
        self._category_cache = {}
        self._tag_cache = {}
        self._user_cache = {}
        
        # Performance tracking
        self.stats = {
            'posts_created': 0,
            'media_uploaded': 0,
            'categories_created': 0,
            'tags_created': 0,
            'total_upload_size': 0,
            'avg_upload_time': 0.0,
            'errors': 0
        }
        
        # SEO plugin detection
        self.seo_plugin = self._detect_seo_plugin()
        
        self._test_connection()
    
    def _create_auth_header(self) -> str:
        """Create Basic Auth header"""
        credentials = f"{self.username}:{self.password}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        return f"Basic {encoded_credentials}"
    
    def _test_connection(self):
        """Enhanced connection test với detailed info"""
        try:
            # Test basic connectivity
            response = requests.get(
                f"{self.api_url}users/me",
                headers={"Authorization": self.auth_header},
                timeout=10
            )
            
            if response.status_code == 200:
                user_data = response.json()
                self._user_cache['me'] = user_data
                
                print(f"✅ [WP PUBLISHER V2] Connected as: {user_data.get('name', 'Unknown')}")
                print(f"   👤 Role: {', '.join(user_data.get('roles', []))}")
                print(f"   🌐 Site: {self.wp_url}")
                
                # Test media upload permissions
                self._test_media_permissions()
                
            else:
                print(f"❌ [WP PUBLISHER V2] Auth failed: {response.status_code}")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"❌ [WP PUBLISHER V2] Connection error: {str(e)}")
    
    def _test_media_permissions(self):
        """Test media upload permissions"""
        try:
            response = requests.get(
                f"{self.api_url}media",
                headers={"Authorization": self.auth_header},
                params={"per_page": 1},
                timeout=5
            )
            
            if response.status_code == 200:
                print(f"✅ [WP PUBLISHER V2] Media access confirmed")
            else:
                print(f"⚠️ [WP PUBLISHER V2] Limited media access: {response.status_code}")
                
        except Exception as e:
            print(f"⚠️ [WP PUBLISHER V2] Media test failed: {str(e)}")
    
    def _detect_seo_plugin(self) -> str:
        """Detect installed SEO plugin"""
        try:
            # Test for Yoast SEO
            response = requests.get(
                f"{self.wp_url}/wp-json/yoast/v1/",
                headers={"Authorization": self.auth_header},
                timeout=5
            )
            
            if response.status_code == 200:
                print(f"✅ [WP PUBLISHER V2] Yoast SEO detected")
                return "yoast"
            
            # Test for RankMath
            response = requests.get(
                f"{self.wp_url}/wp-json/rankmath/v1/",
                headers={"Authorization": self.auth_header},
                timeout=5
            )
            
            if response.status_code == 200:
                print(f"✅ [WP PUBLISHER V2] RankMath detected")
                return "rankmath"
            
            print(f"ℹ️ [WP PUBLISHER V2] No SEO plugin detected")
            return "none"
            
        except Exception as e:
            print(f"⚠️ [WP PUBLISHER V2] SEO plugin detection failed: {str(e)}")
            return "unknown"
    
    def optimize_image(self, image_data: bytes, max_width: int = 1200, 
                      quality: int = 85) -> Tuple[bytes, str]:
        """
        Optimize image cho web performance
        Returns: (optimized_data, format)
        """
        try:
            # Load image
            img = Image.open(io.BytesIO(image_data))
            original_format = img.format or 'JPEG'
            
            # Convert RGBA to RGB nếu cần cho JPEG
            if img.mode in ('RGBA', 'P') and original_format.upper() == 'JPEG':
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1])  # Use alpha channel as mask
                img = background
            
            # Resize if too large
            if img.width > max_width:
                ratio = max_width / img.width
                new_height = int(img.height * ratio)
                img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
                print(f"🔧 [WP PUBLISHER V2] Resized image: {img.width}x{img.height}")
            
            # Save optimized
            output = io.BytesIO()
            save_format = 'JPEG' if original_format.upper() in ['JPEG', 'JPG'] else original_format
            img.save(output, format=save_format, quality=quality, optimize=True)
            
            optimized_data = output.getvalue()
            original_size = len(image_data)
            optimized_size = len(optimized_data)
            
            compression_ratio = (1 - optimized_size / original_size) * 100
            print(f"📦 [WP PUBLISHER V2] Image optimized: {compression_ratio:.1f}% reduction")
            
            return optimized_data, save_format.lower()
            
        except Exception as e:
            print(f"⚠️ [WP PUBLISHER V2] Image optimization failed: {str(e)}")
            return image_data, 'jpeg'
    
    def upload_media(self, media_item: MediaItem) -> Optional[int]:
        """
        Enhanced media upload với optimization
        """
        start_time = time.time()
        
        try:
            file_data = media_item.file_data
            filename = media_item.filename
            
            # Optimize image nếu cần
            if media_item.media_type == MediaType.IMAGE and media_item.optimize:
                file_data, format_ext = self.optimize_image(file_data)
                # Update filename extension if needed
                if not filename.lower().endswith(f'.{format_ext}'):
                    name_without_ext = filename.rsplit('.', 1)[0]
                    filename = f"{name_without_ext}.{format_ext}"
            
            # Detect content type
            content_type, _ = mimetypes.guess_type(filename)
            if not content_type:
                content_type = 'application/octet-stream'
            
            headers = {
                "Authorization": self.auth_header,
                "Content-Type": content_type,
                "Content-Disposition": f'attachment; filename="{filename}"'
            }
            
            response = requests.post(
                f"{self.api_url}media",
                headers=headers,
                data=file_data,
                timeout=60  # Increased timeout for large files
            )
            
            if response.status_code == 201:
                media_data = response.json()
                media_id = media_data['id']
                
                # Update media metadata nếu có
                if media_item.alt_text or media_item.caption or media_item.title:
                    self._update_media_metadata(media_id, media_item)
                
                upload_time = time.time() - start_time
                file_size = len(file_data)
                
                # Update stats
                self.stats['media_uploaded'] += 1
                self.stats['total_upload_size'] += file_size
                self._update_avg_upload_time(upload_time)
                
                print(f"✅ [WP PUBLISHER V2] Uploaded media ID: {media_id}")
                print(f"   📁 File: {filename} ({file_size/1024:.1f}KB)")
                print(f"   ⏱️  Time: {upload_time:.1f}s")
                print(f"   🔗 URL: {media_data['source_url']}")
                
                return media_id
                
            else:
                print(f"❌ [WP PUBLISHER V2] Media upload failed: {response.status_code}")
                print(f"Response: {response.text}")
                self.stats['errors'] += 1
                return None
                
        except Exception as e:
            print(f"❌ [WP PUBLISHER V2] Media upload error: {str(e)}")
            self.stats['errors'] += 1
            return None
    
    def _update_media_metadata(self, media_id: int, media_item: MediaItem):
        """Update media metadata (alt text, caption, etc.)"""
        try:
            update_data = {}
            
            if media_item.alt_text:
                update_data['alt_text'] = media_item.alt_text
            if media_item.caption:
                update_data['caption'] = media_item.caption
            if media_item.title:
                update_data['title'] = media_item.title
            
            if update_data:
                response = requests.post(
                    f"{self.api_url}media/{media_id}",
                    headers={
                        "Authorization": self.auth_header,
                        "Content-Type": "application/json"
                    },
                    json=update_data,
                    timeout=10
                )
                
                if response.status_code == 200:
                    print(f"✅ [WP PUBLISHER V2] Updated media metadata for ID: {media_id}")
                
        except Exception as e:
            print(f"⚠️ [WP PUBLISHER V2] Media metadata update failed: {str(e)}")
    
    def get_or_create_category(self, category_name: str) -> int:
        """Get existing category or create new one"""
        # Check cache first
        if category_name in self._category_cache:
            return self._category_cache[category_name]
        
        try:
            # Search for existing category
            response = requests.get(
                f"{self.api_url}categories",
                headers={"Authorization": self.auth_header},
                params={"search": category_name, "per_page": 1},
                timeout=10
            )
            
            if response.status_code == 200:
                categories = response.json()
                if categories:
                    cat_id = categories[0]['id']
                    self._category_cache[category_name] = cat_id
                    return cat_id
            
            # Create new category
            new_cat_response = requests.post(
                f"{self.api_url}categories",
                headers={
                    "Authorization": self.auth_header,
                    "Content-Type": "application/json"
                },
                json={"name": category_name},
                timeout=10
            )
            
            if new_cat_response.status_code == 201:
                new_cat = new_cat_response.json()
                cat_id = new_cat['id']
                self._category_cache[category_name] = cat_id
                self.stats['categories_created'] += 1
                print(f"✅ [WP PUBLISHER V2] Created category: {category_name} (ID: {cat_id})")
                return cat_id
            
            return 1  # Default category
            
        except Exception as e:
            print(f"❌ [WP PUBLISHER V2] Category processing error: {str(e)}")
            return 1
    
    def get_or_create_tag(self, tag_name: str) -> int:
        """Get existing tag or create new one"""
        # Check cache first
        if tag_name in self._tag_cache:
            return self._tag_cache[tag_name]
        
        try:
            # Search for existing tag
            response = requests.get(
                f"{self.api_url}tags",
                headers={"Authorization": self.auth_header},
                params={"search": tag_name, "per_page": 1},
                timeout=10
            )
            
            if response.status_code == 200:
                tags = response.json()
                if tags:
                    tag_id = tags[0]['id']
                    self._tag_cache[tag_name] = tag_id
                    return tag_id
            
            # Create new tag
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
                tag_id = new_tag['id']
                self._tag_cache[tag_name] = tag_id
                self.stats['tags_created'] += 1
                print(f"✅ [WP PUBLISHER V2] Created tag: {tag_name} (ID: {tag_id})")
                return tag_id
            
            return None
            
        except Exception as e:
            print(f"❌ [WP PUBLISHER V2] Tag processing error: {str(e)}")
            return None
    
    def create_post(self, post_data: PostData) -> Optional[str]:
        """
        Enhanced post creation với full SEO support
        """
        try:
            # Process categories
            category_ids = []
            for cat_name in post_data.categories if isinstance(post_data.categories[0], str) else []:
                cat_id = self.get_or_create_category(cat_name)
                if cat_id:
                    category_ids.append(cat_id)
            
            if not category_ids and post_data.categories and isinstance(post_data.categories[0], int):
                category_ids = post_data.categories
            
            if not category_ids:
                category_ids = [1]  # Default category
            
            # Process tags
            tag_ids = []
            for tag_name in post_data.tags:
                tag_id = self.get_or_create_tag(tag_name)
                if tag_id:
                    tag_ids.append(tag_id)
            
            # Upload featured media nếu có
            featured_media_id = None
            if post_data.featured_media:
                featured_media_id = self.upload_media(post_data.featured_media)
            
            # Chuẩn bị post data
            wp_post_data = {
                "title": post_data.title,
                "content": post_data.content,
                "excerpt": post_data.excerpt,
                "status": post_data.status.value,
                "categories": category_ids,
                "tags": tag_ids,
            }
            
            # Thêm featured media
            if featured_media_id:
                wp_post_data["featured_media"] = featured_media_id
            
            # Thêm scheduled date nếu có
            if post_data.scheduled_date and post_data.status == PostStatus.SCHEDULED:
                wp_post_data["date"] = post_data.scheduled_date.isoformat()
            
            # Thêm author nếu có
            if post_data.author_id:
                wp_post_data["author"] = post_data.author_id
            
            # Thêm SEO meta data
            if post_data.meta_title or post_data.meta_desc:
                wp_post_data["meta"] = self._build_seo_meta(post_data)
            
            # Thêm custom meta
            if post_data.custom_meta:
                if "meta" not in wp_post_data:
                    wp_post_data["meta"] = {}
                wp_post_data["meta"].update(post_data.custom_meta)
            
            headers = {
                "Authorization": self.auth_header,
                "Content-Type": "application/json"
            }
            
            response = requests.post(
                f"{self.api_url}posts",
                headers=headers,
                json=wp_post_data,
                timeout=30
            )
            
            if response.status_code == 201:
                post_info = response.json()
                post_url = post_info['link']
                post_id = post_info['id']
                
                self.stats['posts_created'] += 1
                
                print(f"✅ [WP PUBLISHER V2] Created post ID: {post_id}")
                print(f"   📄 Title: {post_data.title}")
                print(f"   🔗 URL: {post_url}")
                print(f"   📊 Status: {post_data.status.value}")
                if featured_media_id:
                    print(f"   🖼️  Featured Media: ID {featured_media_id}")
                print(f"   🏷️  Categories: {len(category_ids)}, Tags: {len(tag_ids)}")
                
                return post_url
                
            else:
                print(f"❌ [WP PUBLISHER V2] Post creation failed: {response.status_code}")
                print(f"Response: {response.text}")
                self.stats['errors'] += 1
                return None
                
        except Exception as e:
            print(f"❌ [WP PUBLISHER V2] Create post error: {str(e)}")
            self.stats['errors'] += 1
            return None
    
    def _build_seo_meta(self, post_data: PostData) -> Dict[str, str]:
        """Build SEO meta fields based on detected plugin"""
        seo_meta = {}
        
        if self.seo_plugin == "yoast":
            if post_data.meta_title:
                seo_meta["_yoast_wpseo_title"] = post_data.meta_title
            if post_data.meta_desc:
                seo_meta["_yoast_wpseo_metadesc"] = post_data.meta_desc
                
        elif self.seo_plugin == "rankmath":
            if post_data.meta_title:
                seo_meta["rank_math_title"] = post_data.meta_title
            if post_data.meta_desc:
                seo_meta["rank_math_description"] = post_data.meta_desc
        
        return seo_meta
    
    def _update_avg_upload_time(self, upload_time: float):
        """Update average upload time"""
        if self.stats['avg_upload_time'] == 0:
            self.stats['avg_upload_time'] = upload_time
        else:
            # Moving average
            self.stats['avg_upload_time'] = (
                self.stats['avg_upload_time'] * 0.8 + upload_time * 0.2
            )
    
    def publish_complete_post(self, title: str, content: str, image_data: bytes = None,
                            categories: List[str] = None, tags: List[str] = None,
                            meta_title: str = "", meta_desc: str = "") -> Optional[str]:
        """
        Simplified interface for backward compatibility
        """
        # Create MediaItem nếu có image
        featured_media = None
        if image_data:
            title_slug = title.lower().replace(' ', '-').replace(',', '')[:30]
            featured_media = MediaItem(
                file_data=image_data,
                filename=f"{title_slug}.jpg",
                media_type=MediaType.IMAGE,
                alt_text=title,
                title=title
            )
        
        # Create PostData
        post_data = PostData(
            title=title,
            content=content,
            categories=categories or [],
            tags=tags or [],
            featured_media=featured_media,
            meta_title=meta_title,
            meta_desc=meta_desc
        )
        
        return self.create_post(post_data)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get detailed publishing statistics"""
        total_size_mb = self.stats['total_upload_size'] / (1024 * 1024)
        
        return {
            **self.stats,
            'total_upload_size_mb': f"{total_size_mb:.2f}",
            'seo_plugin': self.seo_plugin,
            'site_url': self.wp_url,
            'cache_sizes': {
                'categories': len(self._category_cache),
                'tags': len(self._tag_cache),
                'users': len(self._user_cache)
            }
        }
    
    def health_check(self) -> Dict[str, Any]:
        """Comprehensive health check"""
        health_status = {
            'connection': False,
            'media_upload': False,
            'post_creation': False,
            'seo_plugin': self.seo_plugin,
            'response_time': 0,
            'errors': []
        }
        
        try:
            # Test connection
            start_time = time.time()
            response = requests.get(
                f"{self.api_url}users/me",
                headers={"Authorization": self.auth_header},
                timeout=10
            )
            
            health_status['response_time'] = time.time() - start_time
            
            if response.status_code == 200:
                health_status['connection'] = True
                
                # Test media permissions
                media_response = requests.get(
                    f"{self.api_url}media",
                    headers={"Authorization": self.auth_header},
                    params={"per_page": 1},
                    timeout=5
                )
                
                if media_response.status_code == 200:
                    health_status['media_upload'] = True
                
                # Test post creation permissions  
                posts_response = requests.get(
                    f"{self.api_url}posts",
                    headers={"Authorization": self.auth_header},
                    params={"per_page": 1},
                    timeout=5
                )
                
                if posts_response.status_code == 200:
                    health_status['post_creation'] = True
            
        except Exception as e:
            health_status['errors'].append(str(e))
        
        return health_status

# Test V2 module
if __name__ == "__main__":
    import sys
    sys.path.append('..')
    from config import Config
    
    print("🧪 TESTING WORDPRESS PUBLISHER V2")
    print("=" * 40)
    
    # Test smart WordPress publisher
    wp_pub = SmartWPPublisher(
        wp_url=Config.WP_URL or "",
        username=Config.WP_USERNAME or "",
        password=Config.WP_PASSWORD or ""
    )
    
    # Test health check
    health = wp_pub.health_check()
    print(f"🏥 Health Check: {health}")
    
    # Test create category
    cat_id = wp_pub.get_or_create_category("Test V2 Category")
    print(f"📁 Category ID: {cat_id}")
    
    # Test create tag
    tag_id = wp_pub.get_or_create_tag("test-v2")
    print(f"🏷️  Tag ID: {tag_id}")
    
    # Test post creation
    test_post_data = PostData(
        title=f"Test Post V2 - {datetime.now().strftime('%H:%M:%S')}",
        content="""
        <h2>Test Post từ WordPress Publisher V2</h2>
        <p>Đây là bài test với các tính năng mới:</p>
        <ul>
            <li>✅ Enhanced media optimization</li>
            <li>🚀 SEO automation</li>
            <li>📊 Performance tracking</li>
            <li>🏷️  Smart category/tag management</li>
        </ul>
        <p>Nếu thấy bài này, V2 hoạt động tốt!</p>
        """,
        excerpt="Test excerpt cho V2 publisher",
        categories=["Test V2 Category"],
        tags=["test-v2", "wordpress", "publisher"],
        meta_title="Test SEO Title V2",
        meta_desc="Test SEO description cho WordPress Publisher V2"
    )
    
    confirm = input("👉 Create test post? (y/n): ").lower()
    if confirm == 'y':
        post_url = wp_pub.create_post(test_post_data)
        if post_url:
            print(f"✅ Test post created: {post_url}")
    
    # Show statistics
    stats = wp_pub.get_statistics()
    print(f"\n📊 Publisher Statistics:")
    for key, value in stats.items():
        print(f"   {key}: {value}")
