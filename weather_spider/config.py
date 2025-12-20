#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置模块，用于管理爬虫的配置参数
"""

import os
import datetime
from typing import Optional

class WeatherSpiderConfig:
    """天气爬虫配置类"""

    def __init__(self):
        # 从环境变量或默认值获取配置
        self.timezone = os.getenv('WEATHER_SPIDER_TIMEZONE', 'Asia/Shanghai')
        self.mode = os.getenv('WEATHER_SPIDER_MODE', 'local')
        self.request_timeout = int(os.getenv('REQUEST_TIMEOUT', '30'))
        self.max_retries = int(os.getenv('MAX_RETRIES', '3'))
        self.retry_delay = int(os.getenv('RETRY_DELAY', '5'))

        # GitHub Actions特定配置
        if self.mode == 'github_actions':
            self.log_file = os.getenv('GITHUB_OUTPUT', 'debug.log')
        else:
            self.log_file = 'debug.log'

    def get_current_time(self) -> datetime.datetime:
        """获取当前时间（考虑时区）"""
        # 在GitHub Actions中，时区已经在workflow中设置
        # 在本地，使用系统时间
        return datetime.datetime.now()

    def get_cutoff_time(self, current_time: datetime.datetime) -> datetime.datetime:
        """获取截止时间（北京时间19:30）"""
        return current_time.replace(hour=19, minute=30, second=0, microsecond=0)

    def should_download_previous_day(self, current_time: datetime.datetime) -> bool:
        """判断是否应该下载前一天的数据（19:30前）"""
        cutoff_time = self.get_cutoff_time(current_time)
        return current_time < cutoff_time

# 创建全局配置实例
config = WeatherSpiderConfig()