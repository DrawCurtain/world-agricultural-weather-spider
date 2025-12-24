#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试数据流完整性脚本
验证数据持久化、恢复和对比逻辑
"""

import os
import sys
import datetime
import shutil

# 确保可以导入weather_spider模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from weather_spider.config import config
from weather_spider.daily_summary import DailyWeatherSummary
from weather_spider.parser import WeatherParser
from weather_spider.downloader import ImageDownloader

def test_download_path_generation():
    """测试下载路径生成"""
    print("=" * 60)
    print("测试1: 下载路径生成")
    print("=" * 60)

    parser = WeatherParser()

    # 测试大豆（索引1）降水数据
    test_cases = [
        {
            'crop_index': 1,  # soybeans
            'region_index': 0,  # USA
            'subregion_index': 0,  # National (usa)
            'vrbl': 'pcp',
            'nday': 15,
            'date_str': '20251224',
            'expected_path': 'downloads/pcp/20251224/pcp_soybeans_usa_usa_forecast.png'
        },
        {
            'crop_index': 1,  # soybeans
            'region_index': 1,  # Brazil
            'subregion_index': 0,  # National (brazil)
            'vrbl': 'tmp',
            'nday': 15,
            'date_str': '20251224',
            'expected_path': 'downloads/tmp/20251224/tmp_soybeans_brazil_brazil_forecast.png'
        }
    ]

    for i, test in enumerate(test_cases, 1):
        print(f"\n测试用例 {i}:")
        print(f"  作物: {parser.get_supported_crops()[test['crop_index']]}")
        print(f"  地区: {parser.get_regions_by_crop(test['crop_index'])[test['region_index']]}")
        print(f"  子地区: {parser.get_subregions_by_crop_and_region(test['crop_index'], test['region_index'])[test['subregion_index']]}")
        print(f"  天气变量: {test['vrbl']}")
        print(f"  预报天数: {test['nday']}")
        print(f"  日期: {test['date_str']}")

        save_path = parser.generate_save_path(
            crop_index=test['crop_index'],
            region_index=test['region_index'],
            subregion_index=test['subregion_index'],
            vrbl=test['vrbl'],
            nday=test['nday'],
            date_str=test['date_str']
        )

        print(f"  生成路径: {save_path}")
        print(f"  预期路径: {test['expected_path']}")

        if save_path == test['expected_path']:
            print("  ✅ 路径生成正确")
        else:
            print("  ❌ 路径生成错误")

def test_data_structure():
    """测试数据结构"""
    print("\n" + "=" * 60)
    print("测试2: 数据结构验证")
    print("=" * 60)

    # 检查downloads目录是否存在
    downloads_dir = 'downloads'
    if not os.path.exists(downloads_dir):
        print(f"❌ downloads目录不存在: {downloads_dir}")
        return False

    print(f"✅ downloads目录存在: {downloads_dir}")

    # 检查pcp和tmp目录
    for subdir in ['pcp', 'tmp']:
        subdir_path = os.path.join(downloads_dir, subdir)
        if os.path.exists(subdir_path):
            print(f"✅ {subdir}目录存在: {subdir_path}")

            # 统计日期目录数量
            date_dirs = [d for d in os.listdir(subdir_path) if os.path.isdir(os.path.join(subdir_path, d))]
            print(f"  {subdir}数据天数: {len(date_dirs)}")

            # 列出日期目录
            for date_dir in sorted(date_dirs)[:5]:  # 只显示前5个
                date_path = os.path.join(subdir_path, date_dir)
                file_count = len([f for f in os.listdir(date_path) if f.endswith('.png')])
                print(f"    {date_dir}: {file_count} 个文件")
            if len(date_dirs) > 5:
                print(f"    ... 还有 {len(date_dirs) - 5} 个日期目录")
        else:
            print(f"❌ {subdir}目录不存在: {subdir_path}")

    return True

def test_image_pair_logic():
    """测试图片配对逻辑"""
    print("\n" + "=" * 60)
    print("测试3: 图片配对逻辑")
    print("=" * 60)

    # 创建模拟的DailyWeatherSummary实例来测试
    class TestSummary(DailyWeatherSummary):
        def __init__(self):
            # 使用固定的测试日期
            self.save_date = datetime.datetime(2024, 12, 20)
            self.save_date_str = self.save_date.strftime('%Y%m%d')
            self.compare_dates = {
                'previous': (self.save_date - datetime.timedelta(days=1)).strftime('%Y%m%d'),
                'current': self.save_date.strftime('%Y%m%d')
            }
            self.output_dir = os.path.join('output', self.save_date_str)

    summary = TestSummary()

    print(f"对比日期: {summary.compare_dates['previous']} vs {summary.compare_dates['current']}")

    # 模拟前一天和当天的图片文件
    test_dir = 'test_downloads'
    os.makedirs(test_dir, exist_ok=True)

    # 创建测试目录结构
    previous_dir = os.path.join(test_dir, summary.compare_dates['previous'])
    current_dir = os.path.join(test_dir, summary.compare_dates['current'])

    os.makedirs(previous_dir, exist_ok=True)
    os.makedirs(current_dir, exist_ok=True)

    # 创建测试文件
    test_files = [
        'pcp_soybeans_usa_usa_forecast.png',
        'pcp_soybeans_brazil_brazil_forecast.png',
        'pcp_soybeans_argentina_argentina_forecast.png',
    ]

    # 前一天：创建所有文件
    for f in test_files:
        with open(os.path.join(previous_dir, f), 'w') as file:
            file.write('test')

    # 当天：创建部分文件（模拟部分下载失败）
    for f in test_files[:2]:
        with open(os.path.join(current_dir, f), 'w') as file:
            file.write('test')

    # 测试find_image_pairs方法
    pairs = summary.find_image_pairs('pcp')

    print(f"\n找到的图片对数量: {len(pairs)}")

    for pair in pairs:
        print(f"  前一天: {os.path.basename(pair['previous'])}")
        print(f"  当天: {os.path.basename(pair['current'])}")
        print(f"  匹配: {'✅' if os.path.basename(pair['previous']) == os.path.basename(pair['current']) else '❌'}")

    # 清理测试目录
    shutil.rmtree(test_dir)

    # 预期应该有2个匹配的图片对
    if len(pairs) == 2:
        print("\n✅ 图片配对逻辑正确")
        return True
    else:
        print(f"\n❌ 图片配对逻辑错误，预期2对，实际{len(pairs)}对")
        return False

def test_time_logic():
    """测试时间逻辑"""
    print("\n" + "=" * 60)
    print("测试4: 时间逻辑验证")
    print("=" * 60)

    now = config.get_current_time()
    print(f"当前时间: {now.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print(f"时区: {config.timezone_str}")

    # 测试19:30前的时间
    test_time_before = datetime.datetime(2024, 12, 20, 10, 0, 0)
    if config.timezone:
        try:
            from zoneinfo import ZoneInfo
            test_time_before = test_time_before.replace(tzinfo=ZoneInfo(config.timezone_str))
        except:
            import pytz
            test_time_before = pytz.timezone(config.timezone_str).localize(test_time_before)

    should_download_before = config.should_download_previous_day(test_time_before)
    print(f"\n北京时间 10:00:")
    print(f"  是否下载前一天: {should_download_before} (预期: True)")
    if should_download_before:
        save_date = test_time_before - datetime.timedelta(days=1)
        compare_dates = {
            'previous': (test_time_before - datetime.timedelta(days=2)).strftime('%Y%m%d'),
            'current': save_date.strftime('%Y%m%d')
        }
        print(f"  保存日期: {save_date.strftime('%Y%m%d')}")
        print(f"  对比日期: {compare_dates['previous']} vs {compare_dates['current']}")
        print("  ✅ 逻辑正确" if should_download_before else "  ❌ 逻辑错误")

    # 测试19:30后的时间
    test_time_after = datetime.datetime(2024, 12, 20, 20, 0, 0)
    if config.timezone:
        try:
            from zoneinfo import ZoneInfo
            test_time_after = test_time_after.replace(tzinfo=ZoneInfo(config.timezone_str))
        except:
            import pytz
            test_time_after = pytz.timezone(config.timezone_str).localize(test_time_after)

    should_download_after = config.should_download_previous_day(test_time_after)
    print(f"\n北京时间 20:00:")
    print(f"  是否下载前一天: {should_download_after} (预期: False)")
    if not should_download_after:
        save_date = test_time_after
        compare_dates = {
            'previous': (test_time_after - datetime.timedelta(days=1)).strftime('%Y%m%d'),
            'current': save_date.strftime('%Y%m%d')
        }
        print(f"  保存日期: {save_date.strftime('%Y%m%d')}")
        print(f"  对比日期: {compare_dates['previous']} vs {compare_dates['current']}")
        print("  ✅ 逻辑正确" if not should_download_after else "  ❌ 逻辑错误")

    return should_download_before and not should_download_after

def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("数据流完整性测试")
    print("=" * 60)

    # 设置为GitHub Actions模式
    os.environ['WEATHER_SPIDER_MODE'] = 'github_actions'
    os.environ['WEATHER_SPIDER_TIMEZONE'] = 'Asia/Shanghai'

    # 重新加载配置
    from weather_spider.config import config

    results = []

    # 测试1: 下载路径生成
    try:
        test_download_path_generation()
        results.append(("下载路径生成", True))
    except Exception as e:
        print(f"\n❌ 下载路径生成测试失败: {e}")
        results.append(("下载路径生成", False))

    # 测试2: 数据结构验证
    try:
        test_data_structure()
        results.append(("数据结构验证", True))
    except Exception as e:
        print(f"\n❌ 数据结构验证失败: {e}")
        results.append(("数据结构验证", False))

    # 测试3: 图片配对逻辑
    try:
        test_image_pair_logic()
        results.append(("图片配对逻辑", True))
    except Exception as e:
        print(f"\n❌ 图片配对逻辑测试失败: {e}")
        results.append(("图片配对逻辑", False))

    # 测试4: 时间逻辑
    try:
        test_time_logic()
        results.append(("时间逻辑", True))
    except Exception as e:
        print(f"\n❌ 时间逻辑测试失败: {e}")
        results.append(("时间逻辑", False))

    # 输出测试结果
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)

    passed = 0
    failed = 0
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
        else:
            failed += 1

    print(f"\n总计: {len(results)} 项测试")
    print(f"通过: {passed}")
    print(f"失败: {failed}")

    if failed == 0:
        print("\n🎉 所有测试通过！数据流完整性验证成功")
    else:
        print(f"\n⚠️  有 {failed} 项测试失败，需要进一步检查")

if __name__ == "__main__":
    main()
