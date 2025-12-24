#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置模块，用于管理爬虫的配置参数
"""

import os
import datetime
from typing import Optional

try:
    # Python 3.9+ 有内置的 zoneinfo
    from zoneinfo import ZoneInfo
    HAS_ZONEINFO = True
except (ImportError, Exception) as e:
    # 对于旧版本，使用 pytz
    try:
        import pytz
        HAS_ZONEINFO = False
    except ImportError:
        # 如果都没有，使用系统时间（不推荐，但作为备选）
        HAS_ZONEINFO = None

class WeatherSpiderConfig:
    """天气爬虫配置类"""

    def __init__(self):
        # 从环境变量或默认值获取配置
        self.timezone_str = os.getenv('WEATHER_SPIDER_TIMEZONE', 'Asia/Shanghai')
        self.mode = os.getenv('WEATHER_SPIDER_MODE', 'local')
        self.request_timeout = int(os.getenv('REQUEST_TIMEOUT', '30'))
        self.max_retries = int(os.getenv('MAX_RETRIES', '3'))
        self.retry_delay = int(os.getenv('RETRY_DELAY', '5'))

        # 日志文件始终使用 debug.log
        # 在GitHub Actions中，日志会通过artifact上传，不需要特殊处理
        self.log_file = 'debug.log'

        # 初始化时区
        self.timezone = None
        if HAS_ZONEINFO is True:
            try:
                self.timezone = ZoneInfo(self.timezone_str)
            except Exception as e:
                print(f"警告：无法初始化ZoneInfo '{self.timezone_str}': {e}")
                print("将使用系统本地时间")
        elif HAS_ZONEINFO is False:
            try:
                self.timezone = pytz.timezone(self.timezone_str)
            except Exception as e:
                print(f"警告：无法初始化pytz时区 '{self.timezone_str}': {e}")
                print("将使用系统本地时间")
        else:
            # 如果没有时区库，使用系统时间（仅作备选）
            print(f"警告：未找到时区库，使用系统本地时间")

    def get_current_time(self) -> datetime.datetime:
        """获取当前时间（考虑时区）"""
        if self.timezone:
            # 如果有时区信息，返回带时区的时间
            if HAS_ZONEINFO is True:
                # 使用 zoneinfo
                return datetime.datetime.now(self.timezone)
            elif HAS_ZONEINFO is False:
                # 使用 pytz
                return datetime.datetime.now(self.timezone)
        else:
            # 如果没有时区库，返回系统本地时间
            return datetime.datetime.now()

    def get_cutoff_time(self, current_time: datetime.datetime) -> datetime.datetime:
        """获取截止时间（北京时间19:30）"""
        # 简化逻辑：直接替换时间
        return current_time.replace(hour=19, minute=30, second=0, microsecond=0)

    def should_download_previous_day(self, current_time: datetime.datetime) -> bool:
        """判断是否应该下载前一天的数据（19:30前）"""
        # 简化逻辑：直接比较时间
        cutoff_time = self.get_cutoff_time(current_time)
        return current_time < cutoff_time

# 创建全局配置实例
config = WeatherSpiderConfig()