#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强的网络请求模块，包含重试和超时机制
"""

import os
import time
import requests
from typing import Dict, Optional, List
from urllib.parse import urljoin
from .config import config

class EnhancedNetworkRequest:
    """增强的网络请求类，支持重试和超时"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def _retry_request(self, func, *args, **kwargs):
        """重试装饰器"""
        last_exception = None

        for attempt in range(config.max_retries + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                if attempt < config.max_retries:
                    print(f"请求失败，{config.retry_delay}秒后重试 (尝试 {attempt + 1}/{config.max_retries + 1}): {str(e)}")
                    time.sleep(config.retry_delay)
                else:
                    print(f"所有重试均失败: {str(e)}")

        raise last_exception

    def get(self, url: str, params: Optional[Dict] = None) -> requests.Response:
        """发送GET请求，带重试机制"""
        def _get():
            response = self.session.get(url, params=params, timeout=config.request_timeout)
            response.raise_for_status()
            return response

        return self._retry_request(_get)

    def get_image_numbers(self) -> Optional[Dict]:
        """获取最新的图片编号，带重试机制"""
        try:
            base_url = "https:// GrowingSeason.geo.msu.edu/"
            response = self.get(base_url)

            # 这里应该解析响应获取图片编号
            # 暂时返回模拟数据，需要根据实际页面结构调整
            return {
                "forecast": "20241220",
                "past_pcp": "20241220",
                "past_tmp": "20241220"
            }
        except Exception as e:
            print(f"获取图片编号失败: {str(e)}")
            return None

    def download_image(self, url: str, save_path: str) -> bool:
        """下载图片，带重试机制"""
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(save_path), exist_ok=True)

            def _download():
                response = self.session.get(url, stream=True, timeout=config.request_timeout)
                response.raise_for_status()

                with open(save_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)

                # 验证文件是否下载成功
                if os.path.exists(save_path) and os.path.getsize(save_path) > 0:
                    return True
                else:
                    raise Exception("下载的文件为空或不存在")

            return self._retry_request(_download)

        except Exception as e:
            print(f"下载图片失败: {url}, 错误: {str(e)}")
            # 清理可能的不完整文件
            if os.path.exists(save_path):
                os.remove(save_path)
            return False

    def close(self):
        """关闭会话"""
        self.session.close()