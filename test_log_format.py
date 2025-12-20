#!/usr/bin/env python3
"""测试日志格式是否正确，避免GitHub Actions输出错误"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from weather_spider import daily_summary

def test_log_format():
    """测试日志格式"""
    print("Testing log format...")

    # 测试各种消息
    test_messages = [
        "创建输出目录: output/20251219",
        "开始下载20251219的天气数据",
        "下载完成: 15个文件",
        "[警告] 文件已存在",
        "完成!"
    ]

    for msg in test_messages:
        daily_summary.log(msg)

    # 检查日志文件
    if os.path.exists("debug.log"):
        with open("debug.log", "r", encoding="utf-8") as f:
            content = f.read()
            print("\n日志内容:")
            print(content)

            # 检查是否有方括号
            if "[" in content and "]" in content:
                print("\n⚠️ 警告：日志中包含方括号，可能被GitHub Actions误解")
            else:
                print("\n✅ 日志格式正确，不包含方括号")

    # 清理测试日志
    if os.path.exists("debug.log"):
        os.remove("debug.log")

if __name__ == "__main__":
    test_log_format()