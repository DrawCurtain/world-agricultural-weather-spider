#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
天气爬虫主程序入口 - 用于打包成exe
"""

import sys
import os

# 确保可以导入weather_spider模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from weather_spider.daily_summary import main

if __name__ == "__main__":
    main()