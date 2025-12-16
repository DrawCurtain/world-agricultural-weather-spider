import os
import datetime
from downloader import ImageDownloader
from parser import WeatherParser

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
        self.today = datetime.datetime.now()
        self.yesterday = self.today - datetime.timedelta(days=1)
        self.today_str = self.today.strftime("%Y%m%d")
        self.yesterday_str = self.yesterday.strftime("%Y%m%d")
        
        # 创建输出目录结构
        self.output_root = "output"
        self.today_output_dir = os.path.join(self.output_root, self.today_str)
        self.yesterday_output_dir = os.path.join(self.output_root, self.yesterday_str)
        
        # 创建目录
        os.makedirs(self.today_output_dir, exist_ok=True)
        print(f"创建输出目录: {self.today_output_dir}")
    
    def download_weather_data(self, date_str):
        """下载指定日期的天气数据
        
        Args:
            date_str: 日期字符串（格式：YYYYMMDD）
            
        Returns:
            tuple: (pcp_results, tmp_results)
        """
        print(f"=== 开始下载{date_str}的天气数据 ===")
        
        # 下载大豆的降水预报
        print("\n下载大豆降水预报数据...")
        pcp_results = self.downloader.download_all_images_by_crop(
            crop_index=1,  # soybeans
            vrbl="pcp",
            nday=15,
            date_str=date_str
        )
        
        # 下载大豆的温度预报
        print("\n下载大豆温度预报数据...")
        tmp_results = self.downloader.download_all_images_by_crop(
            crop_index=1,  # soybeans
            vrbl="tmp",
            nday=15,
            date_str=date_str
        )
        
        # 统计结果
        pcp_success = sum(1 for success in pcp_results.values() if success)
        tmp_success = sum(1 for success in tmp_results.values() if success)
        
        print(f"\n=== 下载完成 ===")
        print(f"降水数据: 成功 {pcp_success}/{len(pcp_results)}")
        print(f"温度数据: 成功 {tmp_success}/{len(tmp_results)}")
        
        return pcp_results, tmp_results
    
    def find_image_pairs(self, vrbl):
        """查找今天和前一天的图片对
        
        Args:
            vrbl: 天气变量（"pcp"表示降水，"tmp"表示温度）
            
        Returns:
            list: 包含今天和前一天图片路径的元组列表
        """
        image_pairs = []
        
        # 获取大豆的所有地区和子地区
        crop_index = 1  # soybeans
        regions = self.parser.get_regions_by_crop(crop_index)
        
        for region_index, region in enumerate(regions):
            subregions = self.parser.get_subregions_by_crop_and_region(crop_index, region_index)
            
            # 处理所有子地区，包括第一个地区标识
            for subregion_index, subregion in enumerate(subregions):
                # 生成今天和前一天的图片路径（使用与generate_save_path相同的格式）
                today_path = f"downloads/{vrbl}/{self.today_str}/{vrbl}_soybeans_{region}_{subregion}_forecast.png"
                yesterday_path = f"downloads/{vrbl}/{self.yesterday_str}/{vrbl}_soybeans_{region}_{subregion}_forecast.png"
                
                # 检查今天的图片是否存在
                if os.path.exists(today_path):
                    # 如果昨天的图片不存在，使用今天的图片替代
                    if not os.path.exists(yesterday_path):
                        yesterday_path = today_path
                        print(f"警告：{vrbl}_soybeans_{region}_{subregion}_forecast.png 的昨天图片不存在，使用今天图片替代")
                    
                    image_pairs.append((today_path, yesterday_path, region, subregion))
        
        print(f"找到 {len(image_pairs)} 个{vrbl}图片对")
        return image_pairs
    
    def add_image_with_caption(self, md_content, image_path, caption):
        """添加图片到Markdown内容并添加标题"""
        # 添加图片（使用相对路径，假设Markdown文件和downloads目录在同一层级）
        md_content.append(f"![{caption}]({image_path})")
        md_content.append(f"**{caption}**")
        md_content.append("")  # 空行
        
    def create_comparison_document(self, vrbl, image_pairs, group_type="all"):
        """创建对比HTML文档（左右结构）
        
        Args:
            vrbl: 天气变量（"pcp"表示降水，"tmp"表示温度）
            image_pairs: 图片对列表
            group_type: 分组类型（"usa"表示美国，"others"表示其他国家，"all"表示全部）
            
        Returns:
            str: 生成的HTML文档路径
        """
        log(f"\n=== 创建对比文档 ===")
        log(f"天气变量: {vrbl}")
        log(f"分组类型: {group_type}")
        log(f"总图片对数量: {len(image_pairs)}")
        
        # 筛选图片对
        filtered_pairs = []
        for today_path, yesterday_path, region, subregion in image_pairs:
            if group_type == "usa" and region == "usa":
                filtered_pairs.append((today_path, yesterday_path, region, subregion))
            elif group_type == "others" and region != "usa":
                filtered_pairs.append((today_path, yesterday_path, region, subregion))
            elif group_type == "all":
                filtered_pairs.append((today_path, yesterday_path, region, subregion))
        
        log(f"筛选后图片对数量: {len(filtered_pairs)}")
        
        if not filtered_pairs:
            log(f"没有找到{group_type}的图片对")
            return None
        
        # 生成HTML文件路径
        print(f"DEBUG: group_type = {group_type}")
        if group_type == "usa":
            html_path = os.path.join(self.today_output_dir, f"weather_summary_{vrbl}_{group_type}_{self.today_str}.html")
            group_desc = "美国"
        elif group_type == "others":
            html_path = os.path.join(self.today_output_dir, f"weather_summary_{vrbl}_{group_type}_{self.today_str}.html")
            group_desc = "其他国家"
        else:
            html_path = os.path.join(self.today_output_dir, f"weather_summary_{vrbl}_{self.today_str}.html")
            group_desc = "所有国家"
        print(f"DEBUG: html_path = {html_path}")
        
        # 设置文档标题（中文）
        title = "大豆作物15天天气预报对比"
        if vrbl == "pcp":
            title += " - 降水"
        else:
            title += " - 温度"
        
        title += f" ({group_desc})"
        
        # 构建完整的HTML内容字符串
        html_content = []
        html_content.append("<!DOCTYPE html>")
        html_content.append("<html>")
        html_content.append("<head>")
        html_content.append("<meta charset='utf-8'>")
        html_content.append(f"<title>{title}</title>")
        html_content.append("<style>")
        html_content.append("body { font-family: Arial, sans-serif; margin: 20px; }")
        html_content.append("h1 { text-align: center; color: #333; }")
        html_content.append("h2 { text-align: center; color: #666; }")
        html_content.append("h3 { color: #444; border-bottom: 1px solid #ddd; padding-bottom: 5px; }")
        html_content.append("table { width: 100%; border-collapse: collapse; margin-bottom: 30px; }")
        html_content.append("td { width: 50%; padding: 10px; text-align: center; vertical-align: top; }")
        html_content.append("img { max-width: 100%; height: auto; }")
        html_content.append(".divider { border-top: 1px solid #ddd; margin: 20px 0; }")
        html_content.append("</style>")
        html_content.append("</head>")
        html_content.append("<body>")
        html_content.append(f"<h1>{title}</h1>")
        html_content.append(f"<h2>{self.yesterday_str} vs {self.today_str}</h2>")
        
        # 添加每个地区的对比图（左右结构）
        for today_path, yesterday_path, region, subregion in filtered_pairs:
            # 手动处理特殊情况
            # 对于国家层面的子地区（与国家名称相同），使用"全国"作为子地区名称
            if subregion == region:
                chinese_subregion = "全国"
            else:
                chinese_subregion = self.parser.get_chinese_region_name(subregion)
            
            # 获取中文地区名称
            chinese_region = self.parser.get_chinese_region_name(region)
            
            # 添加地区标题
            html_content.append(f"<h3>{chinese_region} - {chinese_subregion}</h3>")
            
            # 添加左右对比表格
            html_content.append("<table>")
            html_content.append("<tr>")
            
            # 左侧：前一天图片
            html_content.append("<td>")
            html_content.append(f"<h4>{self.yesterday_str}</h4>")
            # 计算相对于HTML文件的正确图片路径
            rel_yesterday_path = os.path.join("..", "..", yesterday_path)
            html_content.append(f"<img src='{rel_yesterday_path}' alt='{self.yesterday_str}'>")
            html_content.append("</td>")
            
            # 右侧：今天图片
            html_content.append("<td>")
            html_content.append(f"<h4>{self.today_str}</h4>")
            # 计算相对于HTML文件的正确图片路径
            rel_today_path = os.path.join("..", "..", today_path)
            html_content.append(f"<img src='{rel_today_path}' alt='{self.today_str}'>")
            html_content.append("</td>")
            
            html_content.append("</tr>")
            html_content.append("</table>")
            html_content.append("<div class='divider'></div>")
        
        # 添加HTML尾部
        html_content.append("</body>")
        html_content.append("</html>")
        
        # 将HTML内容写入文件
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(html_content))
        
        return html_path
    

    
    def run(self):
        """运行完整的汇总流程"""
        # 下载今天和昨天的数据
        print(f"\n=== 下载今天({self.today_str})的天气数据 ===")
        pcp_results_today, tmp_results_today = self.download_weather_data(self.today_str)
        
        print(f"\n=== 下载昨天({self.yesterday_str})的天气数据 ===")
        pcp_results_yesterday, tmp_results_yesterday = self.download_weather_data(self.yesterday_str)
        
        # 处理降水数据
        print("\n=== 创建降水对比文档 ===")
        pcp_image_pairs = self.find_image_pairs("pcp")
        print(f"降水图片对数量: {len(pcp_image_pairs)}")
        if pcp_image_pairs:
            # 打印一些图片对的信息
            print(f"图片对示例: {pcp_image_pairs[:3]}")
            
            # 创建美国降水文档
            pcp_usa_doc_path = self.create_comparison_document("pcp", pcp_image_pairs, group_type="usa")
            print(f"美国降水文档路径: {pcp_usa_doc_path}")
            if pcp_usa_doc_path:
                print(f"✅ 美国降水对比文档已生成: {pcp_usa_doc_path}")
                # 检查文件是否存在
                if os.path.exists(pcp_usa_doc_path):
                    print(f"文件大小: {os.path.getsize(pcp_usa_doc_path)} 字节")
                else:
                    print(f"❌ 文件不存在: {pcp_usa_doc_path}")
                
            # 创建其他国家降水文档
            pcp_others_doc_path = self.create_comparison_document("pcp", pcp_image_pairs, group_type="others")
            print(f"其他国家降水文档路径: {pcp_others_doc_path}")
            if pcp_others_doc_path:
                print(f"✅ 其他国家降水对比文档已生成: {pcp_others_doc_path}")
                # 检查文件是否存在
                if os.path.exists(pcp_others_doc_path):
                    print(f"文件大小: {os.path.getsize(pcp_others_doc_path)} 字节")
                else:
                    print(f"❌ 文件不存在: {pcp_others_doc_path}")
        else:
            print("没有找到降水图片对，无法生成对比文档")
        
        # 处理温度数据
        print("\n=== 创建温度对比文档 ===")
        tmp_image_pairs = self.find_image_pairs("tmp")
        print(f"温度图片对数量: {len(tmp_image_pairs)}")
        if tmp_image_pairs:
            # 创建美国温度文档
            tmp_usa_doc_path = self.create_comparison_document("tmp", tmp_image_pairs, group_type="usa")
            print(f"美国温度文档路径: {tmp_usa_doc_path}")
            if tmp_usa_doc_path:
                print(f"✅ 美国温度对比文档已生成: {tmp_usa_doc_path}")
                # 检查文件是否存在
                if os.path.exists(tmp_usa_doc_path):
                    print(f"文件大小: {os.path.getsize(tmp_usa_doc_path)} 字节")
                else:
                    print(f"❌ 文件不存在: {tmp_usa_doc_path}")
                
            # 创建其他国家温度文档
            tmp_others_doc_path = self.create_comparison_document("tmp", tmp_image_pairs, group_type="others")
            print(f"其他国家温度文档路径: {tmp_others_doc_path}")
            if tmp_others_doc_path:
                print(f"✅ 其他国家温度对比文档已生成: {tmp_others_doc_path}")
                # 检查文件是否存在
                if os.path.exists(tmp_others_doc_path):
                    print(f"文件大小: {os.path.getsize(tmp_others_doc_path)} 字节")
                else:
                    print(f"❌ 文件不存在: {tmp_others_doc_path}")
        else:
            print("没有找到温度图片对，无法生成对比文档")
        
        print("\n=== 开始转换HTML文档为图片 ===")
        
        # 转换所有生成的HTML文档为图片
        html_files = [
            os.path.join(self.today_output_dir, f"weather_summary_pcp_usa_{self.today_str}.html"),
            os.path.join(self.today_output_dir, f"weather_summary_pcp_others_{self.today_str}.html"),
            os.path.join(self.today_output_dir, f"weather_summary_tmp_usa_{self.today_str}.html"),
            os.path.join(self.today_output_dir, f"weather_summary_tmp_others_{self.today_str}.html")
        ]
        
        # 使用html_to_image.py脚本转换图片
        import subprocess
        wkhtmltoimage_path = "D:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltoimage.exe"
        
        for html_file in html_files:
            if os.path.exists(html_file):
                print(f"\n转换 {html_file} 为图片...")
                try:
                    # 调用html_to_image.py脚本转换图片
                    cmd = ["python", "html_to_image.py", "-e", wkhtmltoimage_path, html_file]
                    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                    print(result.stdout.strip())
                    print(f"✅ 成功将 {html_file} 转换为图片")
                except subprocess.CalledProcessError as e:
                    print(f"❌ 转换 {html_file} 失败")
                    print(f"错误信息: {e.stderr.strip()}")
                except Exception as e:
                    print(f"❌ 转换 {html_file} 失败: {e}")
            else:
                print(f"⚠️  HTML文件不存在: {html_file}")
        
        print(f"\n=== 汇总完成 ===")

if __name__ == "__main__":
    summary = DailyWeatherSummary()
    summary.run()
