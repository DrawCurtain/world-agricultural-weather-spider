import sys
import os
import datetime

# 将weather_spider目录的父目录添加到Python路径
sys.path.append(os.path.dirname(__file__))

from weather_spider.daily_summary import DailyWeatherSummary

# 创建测试脚本验证日期逻辑
def test_date_logic():
    print("=== 测试日期逻辑 ===")
    
    # 创建DailyWeatherSummary实例
    summary = DailyWeatherSummary()
    
    # 获取当前实际时间
    now = datetime.datetime.now()
    print(f"当前实际时间: {now}")
    
    # 显示日期逻辑相关信息
    print(f"比较日期: previous={summary.compare_dates['previous']}, current={summary.compare_dates['current']}")
    print(f"保存日期: {summary.save_date}")
    print(f"保存日期字符串: {summary.save_date_str}")
    print(f"保存目录: {summary.output_dir}")
    
    # 显示下载目标日期
    print(f"下载目标日期: {summary.compare_dates['current']}")
    
    # 测试不同时间点的逻辑
    print("\n=== 测试不同时间点的逻辑 ===")
    
    # 测试19:29（七点半前）
    test_time_early = now.replace(hour=19, minute=29, second=0, microsecond=0)
    print(f"测试时间点1（19:29）: {test_time_early}")
    
    if test_time_early < test_time_early.replace(hour=19, minute=30, second=0, microsecond=0):
        expected_save_date = test_time_early - datetime.timedelta(days=1)
        expected_previous = test_time_early - datetime.timedelta(days=2)
        expected_current = expected_save_date
        print(f"  七点半前，预期保存日期: {expected_save_date.strftime('%Y%m%d')}")
        print(f"  七点半前，预期比较日期: previous={expected_previous.strftime('%Y%m%d')}, current={expected_current.strftime('%Y%m%d')}")
    
    # 测试19:31（七点半后）
    test_time_late = now.replace(hour=19, minute=31, second=0, microsecond=0)
    print(f"测试时间点2（19:31）: {test_time_late}")
    
    if test_time_late >= test_time_late.replace(hour=19, minute=30, second=0, microsecond=0):
        expected_save_date = test_time_late
        expected_previous = test_time_late - datetime.timedelta(days=1)
        expected_current = expected_save_date
        print(f"  七点半后，预期保存日期: {expected_save_date.strftime('%Y%m%d')}")
        print(f"  七点半后，预期比较日期: previous={expected_previous.strftime('%Y%m%d')}, current={expected_current.strftime('%Y%m%d')}")

if __name__ == "__main__":
    test_date_logic()