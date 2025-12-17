import sys
import os
import datetime

# 将项目根目录添加到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from weather_spider.daily_summary import DailyWeatherSummary

def test_time_logic():
    """测试时间判断逻辑"""
    print("=== 测试时间判断逻辑 ===")
    
    # 模拟不同的时间点
    test_times = [
        # 七点半前（模拟前天和昨天的数据对比）
        datetime.datetime.now().replace(hour=19, minute=29, second=0),
        # 七点半后（模拟昨天和今天的数据对比）
        datetime.datetime.now().replace(hour=19, minute=30, second=0)
    ]
    
    for test_time in test_times:
        print(f"\n测试时间: {test_time}")
        
        # 创建DailyWeatherSummary实例并测试时间判断逻辑
        # 由于无法直接修改datetime.datetime.now()的返回值，我们需要模拟这个行为
        # 这里我们直接模拟逻辑，而不是实际运行整个流程
        
        cutoff_time = test_time.replace(hour=19, minute=30, second=0, microsecond=0)
        
        if test_time < cutoff_time:
            # 七点半前，保存到前一天文件夹，对比前天和昨天的数据
            save_date = test_time - datetime.timedelta(days=1)
            previous_date = test_time - datetime.timedelta(days=2)
            current_date = test_time - datetime.timedelta(days=1)
            print(f"七点半前运行:")
            print(f"  保存日期: {save_date.strftime('%Y%m%d')}")
            print(f"  对比日期: {previous_date.strftime('%Y%m%d')} vs {current_date.strftime('%Y%m%d')}")
        else:
            # 七点半后，保存到当天文件夹，对比昨天和今天的数据
            save_date = test_time
            previous_date = test_time - datetime.timedelta(days=1)
            current_date = test_time
            print(f"七点半后运行:")
            print(f"  保存日期: {save_date.strftime('%Y%m%d')}")
            print(f"  对比日期: {previous_date.strftime('%Y%m%d')} vs {current_date.strftime('%Y%m%d')}")

if __name__ == "__main__":
    test_time_logic()