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

            issues = []
            # 检查是否有方括号
            if "[" in content and "]" in content:
                issues.append("方括号")
            # 检查是否有管道符
            if " | " in content:
                issues.append("管道符")
            # 检查是否使用了正确的分隔符
            if " - " not in content:
                issues.append("缺少正确的分隔符")

            if issues:
                print(f"\nWarning: Log contains problematic characters: {', '.join(issues)}")
                return False
            else:
                print("\nSuccess: Log format is correct")
                return True

    # 清理测试日志
    if os.path.exists("debug.log"):
        os.remove("debug.log")

    return True

if __name__ == "__main__":
    success = test_log_format()
    sys.exit(0 if success else 1)