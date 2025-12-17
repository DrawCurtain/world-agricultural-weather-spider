import os
import sys
import datetime
from .downloader import ImageDownloader
from .parser import WeatherParser

# 设置日志文件
log_file = "debug.log"

def log(message):
    """将日志信息写入文件"""
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")
    print(message)

class DailyWeatherSummary:
    """每日天气数据汇总模块，用于生成今天和前一天的天气对比Word文档"""
    
    def __init__(self):
        self.downloader = ImageDownloader()
        self.parser = WeatherParser()
        
        # 获取当前时间
        now = datetime.datetime.now()
        cutoff_time = now.replace(hour=19, minute=30, second=0, microsecond=0)
        
        if now < cutoff_time:
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
            log(f"创建输出目录: {self.output_dir}")
    
    def download_weather_data(self, date_str):
        """下载指定日期的天气数据
        
        Args:
            date_str: 日期字符串，格式为"YYYYMMDD"
        """
        log(f"=== 开始下载{date_str}的天气数据 ===")
        
        # 下载大豆降水预报数据
        log(f"\n下载大豆降水预报数据...")
        self.downloader.download_weather_images(date_str, "pcp", "soybeans")
        
        # 下载大豆温度预报数据
        log(f"\n下载大豆温度预报数据...")
        self.downloader.download_weather_images(date_str, "tmp", "soybeans")

    def process_weather_data(self, weather_type):
        """处理指定类型的天气数据"""
        # 查找需要对比的图片对
        image_pairs = self.find_image_pairs(weather_type)
        
        if not image_pairs:
            log(f"未找到{weather_type}数据的对比图片")
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
            log(f"前一天图片路径不存在: {previous_path}")
            previous_path = current_path  # 如果前一天路径不存在，使用当前日期路径
        
        if not os.path.exists(current_path):
            log(f"当前图片路径不存在: {current_path}")
            return pairs
        
        # 获取两天的图片文件列表
        previous_files = os.listdir(previous_path)
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
        """创建对比HTML文档（左右结构）
        
        Args:
            vrbl: 天气变量（"pcp"表示降水，"tmp"表示温度）
            image_pairs: 图片对列表
            group_type: 分组类型（"usa"表示美国，"brazil"表示巴西，"argentina"表示阿根廷，"others"表示其他国家，"all"表示全部）
            
        Returns:
            str: 生成的HTML文档路径
        """
        log("\n=== 创建对比文档 ===")
        log(f"天气变量: {vrbl}")
        log(f"分组类型: {group_type}")
        log(f"总图片对数量: {len(image_pairs)}")
        
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
        
        log(f"筛选后图片对数量: {len(filtered_pairs)}")
        
        if not filtered_pairs:
            log(f"没有找到{group_type}的图片对")
            return None
        
        # 生成HTML文件路径
        if group_type == "usa":
            html_path = os.path.join(self.output_dir, f"weather_summary_{vrbl}_{group_type}_{self.save_date_str}.html")
            group_desc = "美国"
        elif group_type == "brazil":
            html_path = os.path.join(self.output_dir, f"weather_summary_{vrbl}_{group_type}_{self.save_date_str}.html")
            group_desc = "巴西"
        elif group_type == "argentina":
            html_path = os.path.join(self.output_dir, f"weather_summary_{vrbl}_{group_type}_{self.save_date_str}.html")
            group_desc = "阿根廷"
        elif group_type == "others":
            html_path = os.path.join(self.output_dir, f"weather_summary_{vrbl}_{group_type}_{self.save_date_str}.html")
            group_desc = "其他国家"
        else:
            html_path = os.path.join(self.output_dir, f"weather_summary_{vrbl}_{self.save_date_str}.html")
            group_desc = "所有国家"
        
        # 设置天气变量文本描述
        if vrbl == "pcp":
            vrbl_text = "降水预报"
        else:
            vrbl_text = "温度预报"
        
        # 生成图片HTML部分
        images_html = ""
        for i, (today_path, yesterday_path, region, subregion) in enumerate(filtered_pairs):
            # 生成在HTML中使用的相对路径
            today_img_path = os.path.relpath(today_path, os.path.dirname(html_path))
            yesterday_img_path = os.path.relpath(yesterday_path, os.path.dirname(html_path))
            
            # 添加到图片列表
            if vrbl == "pcp":
                images_html += f"<div class='image-container'>\n"
                images_html += f"    <h3>{self.parser.get_chinese_region_name(region)} - {self.parser.get_chinese_region_name(subregion)} 降水预报</h3>\n"
                images_html += f"    <div class='image-pair'>\n"
                images_html += f"        <div class='image-column'>\n"
                images_html += f"            <h4>前一天</h4>\n"
                images_html += f"            <img src='{yesterday_img_path}' alt='Yesterday {region} {subregion} PCP Forecast'>\n"
                images_html += f"        </div>\n"
                images_html += f"        <div class='image-column'>\n"
                images_html += f"            <h4>今天</h4>\n"
                images_html += f"            <img src='{today_img_path}' alt='Today {region} {subregion} PCP Forecast'>\n"
                images_html += f"        </div>\n"
                images_html += f"    </div>\n"
                images_html += f"</div>\n"  
            else:  # tmp
                images_html += f"<div class='image-container'>\n"
                images_html += f"    <h3>{self.parser.get_chinese_region_name(region)} - {self.parser.get_chinese_region_name(subregion)} 温度预报</h3>\n"
                images_html += f"    <div class='image-pair'>\n"
                images_html += f"        <div class='image-column'>\n"
                images_html += f"            <h4>前一天</h4>\n"
                images_html += f"            <img src='{yesterday_img_path}' alt='Yesterday {region} {subregion} TMP Forecast'>\n"
                images_html += f"        </div>\n"
                images_html += f"        <div class='image-column'>\n"
                images_html += f"            <h4>今天</h4>\n"
                images_html += f"            <img src='{today_img_path}' alt='Today {region} {subregion} TMP Forecast'>\n"
                images_html += f"        </div>\n"
                images_html += f"    </div>\n"
                images_html += f"</div>\n"
        
        # 生成完整的HTML文档
        html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Weather Forecast Comparison</title>
    <style>
        body {{ 
            font-family: Arial, sans-serif; 
            margin: 0; 
            padding: 20px; 
            background-color: #f0f0f0; 
            width: 2000px; /* 固定宽度以确保左右布局有足够空间 */
        }}
        .container {{ 
            width: 1960px; /* 容器宽度略小于body，提供内边距空间 */
            margin: 0 auto; 
            background-color: white; 
            padding: 20px; 
            border-radius: 8px; 
            box-shadow: 0 0 10px rgba(0,0,0,0.1); 
        }}
        h1 {{ 
            text-align: center; 
            color: #333; 
        }}
        h2 {{ 
            color: #555; 
            border-bottom: 2px solid #ddd; 
            padding-bottom: 10px; 
        }}
        h3 {{ 
            color: #666; 
            margin-top: 30px; 
        }}
        h4 {{ 
            color: #777; 
            margin-bottom: 10px; 
        }}
        .image-container {{ 
            margin-bottom: 40px; 
            border: 1px solid #eee; 
            padding: 15px; 
            border-radius: 8px; 
        }}
        .image-pair {{ 
            display: flex; 
            justify-content: space-around; 
            flex-wrap: nowrap; /* 防止折行 */
            white-space: nowrap; /* 确保不换行 */
            overflow: hidden; /* 隐藏溢出内容 */
            width: 100%; /* 确保占满容器宽度 */
            height: auto; /* 自适应高度 */
        }}
        .image-column {{ 
            text-align: center; 
            width: 48%; 
            min-width: 0; /* 修复flexbox布局问题 */
            box-sizing: border-box; /* 确保宽度计算正确 */
            padding: 0 5px; /* 添加内边距 */
            float: left; /* 辅助float布局确保左右排列 */
        }}
        img {{ 
            max-width: 100%; 
            height: auto; 
            border: 1px solid #ddd; 
            box-sizing: border-box; /* 确保宽度计算正确 */
        }}
        .info {{ 
            text-align: center; 
            color: #888; 
            margin-top: 30px; 
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>天气预报对比</h1>
        <h2>{vrbl_text} - {group_desc}</h2>
        <div class="info">
            <p>生成时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>当前数据日期: {datetime.datetime.strptime(self.compare_dates['current'], '%Y%m%d').strftime('%Y-%m-%d')}</p>
            <p>前一天数据日期: {datetime.datetime.strptime(self.compare_dates['previous'], '%Y%m%d').strftime('%Y-%m-%d')}</p>
        </div>
        
        {images_html}
    </div>
</body>
</html>"""
        
        # 写入HTML文件
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        log(f"成功生成对比文档: {html_path}")
        
        # 转换为图片
        self.convert_html_to_image(html_path)
        
        return html_path

    def convert_html_to_image(self, html_path):
        """将HTML文档转换为图片
        
        Args:
            html_path: HTML文档路径
            
        Returns:
            str: 生成的图片路径
        """
        if not html_path:
            return None
            
        # 检查是否存在imgkit
        try:
            import imgkit
        except ImportError:
            log("警告: 未安装imgkit库，跳过图片转换")
            return None
        
        # 检查是否存在wkhtmltoimage
        try:
            # 尝试使用不同路径查找wkhtmltoimage
            bin_path = None
            
            # 1. 检查PyInstaller打包后的临时目录
            if hasattr(sys, '_MEIPASS'):
                # PyInstaller打包环境
                bin_path = os.path.join(sys._MEIPASS, "bin", "wkhtmltoimage.exe")
                log(f"尝试使用PyInstaller临时目录: {bin_path}")
            
            # 2. 检查当前工作目录
            if not bin_path or not os.path.exists(bin_path):
                bin_path = os.path.join(os.getcwd(), "bin", "wkhtmltoimage.exe")
                log(f"尝试使用当前工作目录: {bin_path}")
            
            # 3. 检查相对路径
            if not os.path.exists(bin_path):
                bin_path = os.path.join("bin", "wkhtmltoimage.exe")
                log(f"尝试使用相对路径: {bin_path}")
            
            if os.path.exists(bin_path):
                config = imgkit.config(wkhtmltoimage=bin_path)
                log(f"使用wkhtmltoimage: {bin_path}")
            else:
                log(f"警告: 无法找到wkhtmltoimage: {bin_path} 不存在")
                return None
        except Exception as e:
            log(f"警告: 无法找到wkhtmltoimage: {e}")
            return None
        
        log(f"将HTML转换为图片: {html_path}")
        
        # 生成图片路径
        img_path = html_path.replace(".html", ".png")
        
        try:
            # 使用imgkit转换，添加更多选项确保布局正确
            imgkit.from_file(html_path, img_path, config=config, options={
                "width": 2000,  # 大幅增加宽度确保左右布局不折叠
                "zoom": 1.0,  # 缩放比例
                "enable-local-file-access": "",  # 允许访问本地文件
                "disable-smart-width": "",  # 禁用智能宽度调整
                "no-stop-slow-scripts": "",  # 不禁用缓慢脚本
                "minimum-font-size": 12  # 确保文字清晰
            })
            
            log(f"成功生成图片: {img_path}")
            return img_path
        except Exception as e:
            log(f"图片转换失败: {e}")
            return None

    def run(self):
        """运行每日天气总结的主要流程"""
        log(f"\n=== 开始每日天气总结流程 ===")
        log(f"当前时间: {datetime.datetime.now()}")
        log(f"比较日期: {self.compare_dates['previous']} vs {self.compare_dates['current']}")
        log(f"保存目录: {self.output_dir}")
        
        # 下载当天和前一天的大豆降水预报图片
        log(f"\n开始下载大豆降水预报图片...")
        
        # 大豆的crop_index是1
        soybean_crop_index = 1
        # 默认使用15天预报
        forecast_days = 15
        
        # 只下载当前需要保存日期的数据
        target_date = self.compare_dates['current']
        
        # 下载降水数据
        self.downloader.download_all_images_by_crop(
            crop_index=soybean_crop_index,
            vrbl="pcp",
            nday=forecast_days,
            date_str=target_date
        )
        
        # 下载温度数据
        self.downloader.download_all_images_by_crop(
            crop_index=soybean_crop_index,
            vrbl="tmp",
            nday=forecast_days,
            date_str=target_date
        )
        
        log(f"\n图片下载完成")
        
        # 处理降水数据
        self.process_weather_data("pcp")
        
        # 处理温度数据
        self.process_weather_data("tmp")
        
        log(f"\n=== 每日天气总结流程完成 ===")


def main():
    """主函数，用于支持命令行调用"""
    summary = DailyWeatherSummary()
    summary.run()

if __name__ == "__main__":
    main()