#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
天气爬虫主程序入口 - 用于打包成exe
"""

import sys
import os
import contextlib

# 确保可以导入weather_spider模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from weather_spider.daily_summary import main
from weather_spider.config import config

if __name__ == "__main__":
    # 在GitHub Actions模式下，重定向stdout到stderr以避免文件命令解析错误
    if config.mode == 'github_actions':
        # 保存原始的stdout
        original_stdout = sys.stdout

        # 创建一个写入器，将所有stdout输出重定向到stderr
        class StdoutToStderr:
            def write(self, text):
                if text.strip():  # 只写入非空文本
                    sys.stderr.write(text)

            def flush(self):
                sys.stderr.flush()

            def __getattr__(self, name):
                return getattr(sys.stderr, name)

        # 重定向stdout
        sys.stdout = StdoutToStderr()

        try:
            main()
        finally:
            # 恢复原始stdout
            sys.stdout = original_stdout
    else:
        main()