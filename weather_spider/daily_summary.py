import os
import sys
import datetime
from .downloader import ImageDownloader
from .parser import WeatherParser
from .image_generator import create_image_comparison
from .config import config

# 缓存状态（从环境变量获取）
CACHE_STATUS = os.getenv('GITHUB_CACHE_STATUS', 'unknown')

def log(message, level="INFO"):
    """将日志信息写入文件并输出到控制台

    Args:
        message: 日志消息
        level: 日志级别 (INFO, WARN, ERROR, SUCCESS)
    """
    log_file = config.log_file
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 日志级别标记
    level_markers = {
        "INFO": "[INFO]",
        "WARN": "[WARN]",
        "ERROR": "[ERROR]",
        "SUCCESS": "[SUCCESS]",
    }
    marker = level_markers.get(level, "[INFO]")

    # 格式化日志
    formatted_msg = f"{marker} {message}"

    # 写入日志文件
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} {formatted_msg}\n")

    # 输出到控制台
    print(formatted_msg)

class DailyWeatherSummary:
    """每日天气数据汇总模块，用于生成今天和前一天的天气对比Word文档"""
    
    def __init__(self):
        self.downloader = ImageDownloader()
        self.parser = WeatherParser()

        # 使用配置获取当前时间
        now = config.get_current_time()

        # 判断是否应该下载前一天的数据
        if config.should_download_previous_day(now):
            # 七点半前，下载昨天的数据，保存到昨天的文件夹
            self.save_date = now - datetime.timedelta(days=1)
            self.compare_dates = {
                'previous': (now - datetime.timedelta(days=2)).strftime('%Y%m%d'),
                'current': self.save_date.strftime('%Y%m%d')
            }
        else:
            # 七点半后，下载今天的数据，保存到今天的文件夹
            self.save_date = now
            self.compare_dates = {
                'previous': (now - datetime.timedelta(days=1)).strftime('%Y%m%d'),
                'current': self.save_date.strftime('%Y%m%d')
            }

        self.save_date_str = self.save_date.strftime('%Y%m%d')
        self.output_dir = os.path.join('output', self.save_date_str)

        # 创建输出目录
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        # 打印启动信息
        log("=" * 50)
        log(f"启动时间: {now.strftime('%Y-%m-%d %H:%M:%S')}")
        log(f"对比日期: {self.compare_dates['previous']} vs {self.compare_dates['current']}")
        log(f"保存目录: {self.output_dir}")

        # 检查并打印缓存状态
        self._check_cache_status()

    def _check_cache_status(self):
        """检查缓存状态并打印"""
        previous_pcp_path = os.path.join("downloads", "pcp", self.compare_dates['previous'])
        previous_tmp_path = os.path.join("downloads", "tmp", self.compare_dates['previous'])
        current_pcp_path = os.path.join("downloads", "pcp", self.compare_dates['current'])
        current_tmp_path = os.path.join("downloads", "tmp", self.compare_dates['current'])

        # 检查前一天数据
        pcp_prev_exists = os.path.exists(previous_pcp_path)
        tmp_prev_exists = os.path.exists(previous_tmp_path)

        if pcp_prev_exists and tmp_prev_exists:
            pcp_count = len(os.listdir(previous_pcp_path)) if pcp_prev_exists else 0
            tmp_count = len(os.listdir(previous_tmp_path)) if tmp_prev_exists else 0
            log(f"缓存状态: 前一天数据存在 (pcp:{pcp_count}张, tmp:{tmp_count}张)", "SUCCESS")
        else:
            log(f"缓存状态: 前一天数据不存在 (首次运行)", "WARN")

        # 检查当天数据
        pcp_curr_exists = os.path.exists(current_pcp_path)
        tmp_curr_exists = os.path.exists(current_tmp_path)

        if pcp_curr_exists or tmp_curr_exists:
            pcp_count = len(os.listdir(current_pcp_path)) if pcp_curr_exists else 0
            tmp_count = len(os.listdir(current_tmp_path)) if tmp_curr_exists else 0
            log(f"缓存状态: 当天数据已存在 (pcp:{pcp_count}张, tmp:{tmp_count}张)", "INFO")

    def process_weather_data(self, weather_type):
        """处理指定类型的天气数据"""
        # 查找需要对比的图片对
        image_pairs = self.find_image_pairs(weather_type)

        if not image_pairs:
            return

        # 为美国创建对比文档
        self.create_comparison_document(weather_type, image_pairs, "usa")

        # 为巴西创建对比文档
        self.create_comparison_document(weather_type, image_pairs, "brazil")

        # 为阿根廷创建对比文档
        self.create_comparison_document(weather_type, image_pairs, "argentina")

        # 为其他国家创建对比文档
        self.create_comparison_document(weather_type, image_pairs, "others")

        # 为所有国家创建对比文档
        self.create_comparison_document(weather_type, image_pairs, "all")

    def find_image_pairs(self, weather_type):
        """查找需要对比的图片对"""
        pairs = []

        # 构建两天的图片路径（使用项目相对路径）
        previous_path = os.path.join("downloads", weather_type, self.compare_dates['previous'])
        current_path = os.path.join("downloads", weather_type, self.compare_dates['current'])

        # 检查路径是否存在
        if not os.path.exists(previous_path):
            log(f"前一天路径不存在，将使用当天路径", "WARN")
            previous_path = current_path

        if not os.path.exists(current_path):
            log(f"当天路径不存在: {current_path}", "ERROR")
            return pairs

        # 获取两天的图片文件列表
        previous_files = os.listdir(previous_path) if os.path.exists(previous_path) else []
        current_files = os.listdir(current_path)

        # 查找匹配的图片对
        for prev_file in previous_files:
            if prev_file in current_files:
                pair = {
                    "previous": os.path.join(previous_path, prev_file),
                    "current": os.path.join(current_path, prev_file),
                    "filename": prev_file
                }
                pairs.append(pair)

        return pairs

    def create_comparison_document(self, vrbl, image_pairs, group_type="all"):
        """创建对比图片（左右结构）

        Args:
            vrbl: 天气变量（"pcp"表示降水，"tmp"表示温度）
            image_pairs: 图片对列表
            group_type: 分组类型（"usa"表示美国，"brazil"表示巴西，"argentina"表示阿根廷，"others"表示其他国家，"all"表示全部）

        Returns:
            str: 生成的图片路径
        """
        # 筛选图片对
        filtered_pairs = []
        for pair in image_pairs:
            today_path = pair["current"]
            yesterday_path = pair["previous"]
            filename = pair["filename"]

            # 从文件名中提取region和subregion信息
            # 格式: vrbl_soybeans_region_subregion_forecast.png
            parts = filename.split("_")
            if len(parts) >= 5:
                region = parts[2]
                subregion = parts[3]

                # 根据group_type筛选
                if group_type == "usa" and region == "usa":
                    filtered_pairs.append((today_path, yesterday_path, region, subregion))
                elif group_type == "brazil" and region == "brazil":
                    filtered_pairs.append((today_path, yesterday_path, region, subregion))
                elif group_type == "argentina" and region == "argentina":
                    filtered_pairs.append((today_path, yesterday_path, region, subregion))
                elif group_type == "others" and region not in ["usa", "brazil", "argentina"]:
                    filtered_pairs.append((today_path, yesterday_path, region, subregion))
                elif group_type == "all":
                    filtered_pairs.append((today_path, yesterday_path, region, subregion))

        if not filtered_pairs:
            return None

        # 生成图片文件路径
        if group_type == "usa":
            img_path = os.path.join(self.output_dir, f"weather_summary_{vrbl}_{group_type}_{self.save_date_str}.png")
            group_desc = "美国"
        elif group_type == "brazil":
            img_path = os.path.join(self.output_dir, f"weather_summary_{vrbl}_{group_type}_{self.save_date_str}.png")
            group_desc = "巴西"
        elif group_type == "argentina":
            img_path = os.path.join(self.output_dir, f"weather_summary_{vrbl}_{group_type}_{self.save_date_str}.png")
            group_desc = "阿根廷"
        elif group_type == "others":
            img_path = os.path.join(self.output_dir, f"weather_summary_{vrbl}_{group_type}_{self.save_date_str}.png")
            group_desc = "其他国家"
        else:
            img_path = os.path.join(self.output_dir, f"weather_summary_{vrbl}_{self.save_date_str}.png")
            group_desc = "所有国家"

        # 使用新的图片生成器直接创建对比图片
        try:
            create_image_comparison(
                image_pairs=filtered_pairs,
                output_path=img_path,
                weather_type=vrbl,
                group_desc=group_desc,
                compare_dates=self.compare_dates,
                save_date_str=self.save_date_str
            )
            # 简化日志，只显示文件名
            filename = os.path.basename(img_path)
            log(f"生成: {filename} ({len(filtered_pairs)}个地区)", "SUCCESS")
            return img_path
        except Exception as e:
            log(f"生成失败 {group_desc}: {e}", "ERROR")
            return None


    def run(self):
        """运行每日天气总结的主要流程"""
        log("开始下载天气数据...")

        # 大豆的crop_index是1
        soybean_crop_index = 1
        # 默认使用15天预报
        forecast_days = 15

        # 只下载当前需要保存日期的数据
        target_date = self.compare_dates['current']

        # 下载降水数据
        log("[1/2] 下载降水数据 (pcp)...")
        self.downloader.download_all_images_by_crop(
            crop_index=soybean_crop_index,
            vrbl="pcp",
            nday=forecast_days,
            date_str=target_date
        )

        # 下载温度数据
        log("[2/2] 下载温度数据 (tmp)...")
        self.downloader.download_all_images_by_crop(
            crop_index=soybean_crop_index,
            vrbl="tmp",
            nday=forecast_days,
            date_str=target_date
        )

        log("数据下载完成", "SUCCESS")

        # 处理降水数据
        log("生成降水对比图片...")
        self.process_weather_data("pcp")

        # 处理温度数据
        log("生成温度对比图片...")
        self.process_weather_data("tmp")

        log("=" * 50)
        log("任务完成!", "SUCCESS")


def main():
    """主函数，用于支持命令行调用"""
    summary = DailyWeatherSummary()
    summary.run()

if __name__ == "__main__":
    main()