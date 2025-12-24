#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试时区修复是否正确的脚本
"""

import os
import sys
import datetime

# 确保可以导入weather_spider模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from weather_spider.config import config

def test_timezone_logic():
    """测试时区逻辑是否正确"""
    print("=" * 60)
    print("时区修复测试")
    print("=" * 60)

    # 测试1：检查配置
    print("\n1. 检查配置:")
    print(f"   时区字符串: {config.timezone_str}")
    print(f"   时区对象: {config.timezone}")
    print(f"   运行模式: {config.mode}")

    # 测试2：获取当前时间
    print("\n2. 获取当前时间:")
    now = config.get_current_time()
    print(f"   当前时间: {now}")
    print(f"   时区信息: {now.tzinfo}")

    # 测试3：测试截止时间
    print("\n3. 测试截止时间:")
    cutoff = config.get_cutoff_time(now)
    print(f"   截止时间 (19:30): {cutoff}")

    # 测试4：测试判断逻辑
    print("\n4. 测试判断逻辑:")
    should_download = config.should_download_previous_day(now)
    print(f"   是否应该下载前一天数据: {should_download}")

    # 测试5：模拟不同时区的时间
    print("\n5. 模拟测试:")

    # 测试19:30前的时间（北京）
    test_time_before = datetime.datetime(2024, 12, 20, 10, 0, 0)  # 北京时间上午10点
    if config.timezone:
        if config.timezone_str == 'Asia/Shanghai':
            # 手动设置时区
            try:
                from zoneinfo import ZoneInfo
                test_time_before = test_time_before.replace(tzinfo=ZoneInfo('Asia/Shanghai'))
            except:
                import pytz
                test_time_before = pytz.timezone('Asia/Shanghai').localize(test_time_before)

    result_before = config.should_download_previous_day(test_time_before)
    print(f"   北京时间 10:00 - 是否下载前一天: {result_before} (应该是 True)")

    # 测试19:30后的时间（北京）
    test_time_after = datetime.datetime(2024, 12, 20, 20, 0, 0)  # 北京时间晚上8点
    if config.timezone:
        if config.timezone_str == 'Asia/Shanghai':
            try:
                from zoneinfo import ZoneInfo
                test_time_after = test_time_after.replace(tzinfo=ZoneInfo('Asia/Shanghai'))
            except:
                import pytz
                test_time_after = pytz.timezone('Asia/Shanghai').localize(test_time_after)

    result_after = config.should_download_previous_day(test_time_after)
    print(f"   北京时间 20:00 - 是否下载前一天: {result_after} (应该是 False)")

    # 测试6：检查日期逻辑
    print("\n6. 检查日期逻辑:")
    if should_download:
        save_date = now - datetime.timedelta(days=1)
        print(f"   当前判断：下载昨天数据")
        print(f"   保存日期: {save_date.strftime('%Y%m%d')}")
        compare_dates = {
            'previous': (now - datetime.timedelta(days=2)).strftime('%Y%m%d'),
            'current': save_date.strftime('%Y%m%d')
        }
    else:
        save_date = now
        print(f"   当前判断：下载今天数据")
        print(f"   保存日期: {save_date.strftime('%Y%m%d')}")
        compare_dates = {
            'previous': (now - datetime.timedelta(days=1)).strftime('%Y%m%d'),
            'current': save_date.strftime('%Y%m%d')
        }

    print(f"   对比日期: {compare_dates['previous']} vs {compare_dates['current']}")

    # 验证结果
    print("\n7. 验证结果:")
    if now.hour < 19 or (now.hour == 19 and now.minute < 30):
        expected = True
        print(f"   当前时间 {now.strftime('%H:%M')} < 19:30，预期下载前一天: {expected}")
    else:
        expected = False
        print(f"   当前时间 {now.strftime('%H:%M')} >= 19:30，预期下载前一天: {expected}")

    if should_download == expected:
        print("   ✅ 时区逻辑正确！")
    else:
        print("   ❌ 时区逻辑错误！")
        print(f"      实际结果: {should_download}")
        print(f"      预期结果: {expected}")

    print("\n" + "=" * 60)

if __name__ == "__main__":
    # 设置环境变量以测试GitHub Actions模式
    os.environ['WEATHER_SPIDER_MODE'] = 'github_actions'
    os.environ['WEATHER_SPIDER_TIMEZONE'] = 'Asia/Shanghai'

    test_timezone_logic()
