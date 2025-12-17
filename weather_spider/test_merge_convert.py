import os
import sys
import datetime
import shutil
import tempfile

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from weather_spider.daily_summary import DailyWeatherSummary

def test_merge_and_convert():
    """测试HTML合并和图片转换功能"""
    print("=== 测试HTML合并和图片转换功能 ===")
    
    # 创建DailyWeatherSummary实例
    summary = DailyWeatherSummary()
    
    # 创建测试图片对
    # 注意：这里我们需要使用真实存在的图片文件路径
    # 首先创建临时目录
    test_dir = tempfile.mkdtemp()
    
    try:
        # 创建模拟图片（实际项目中这些图片会被下载）
        # 我们可以使用空的PNG文件作为测试
        def create_empty_png(path):
            """创建空的PNG文件"""
            with open(path, 'wb') as f:
                # 写入最小的PNG文件头
                f.write(b'\x89PNG\r\n\x1a\n')
                f.write(b'\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x00\x00\x00\x00')
                f.write(b'\xdb\x15\x9f\x00\x00\x00\x0cIDAT\x08\xd7c\xf8\xff\xff?\x00\x05\xfe\x02')
                f.write(b'\xfe\xdc\xcc\x59\xe7\x00\x00\x00\x00IEND\xaeB`\x82')
        
        # 创建模拟图片对
        image_pairs = []
        
        # 创建昨天和今天的目录结构
        yesterday_date = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y%m%d')
        today_date = datetime.datetime.now().strftime('%Y%m%d')
        
        yesterday_pcp_dir = os.path.join(test_dir, "downloads", "pcp", yesterday_date)
        today_pcp_dir = os.path.join(test_dir, "downloads", "pcp", today_date)
        
        os.makedirs(yesterday_pcp_dir, exist_ok=True)
        os.makedirs(today_pcp_dir, exist_ok=True)
        
        # 创建模拟图片
        test_images = [
            "pcp_soybeans_usa_midwest_forecast.png",
            "pcp_soybeans_brazil_parana_forecast.png",
            "pcp_soybeans_argentina_buenosaires_forecast.png"
        ]
        
        for img_name in test_images:
            yesterday_img_path = os.path.join(yesterday_pcp_dir, img_name)
            today_img_path = os.path.join(today_pcp_dir, img_name)
            
            create_empty_png(yesterday_img_path)
            create_empty_png(today_img_path)
            
            image_pairs.append({
                "previous": yesterday_img_path,
                "current": today_img_path,
                "filename": img_name
            })
        
        # 保存原始的output_dir和compare_dates
        original_output_dir = summary.output_dir
        original_compare_dates = summary.compare_dates
        
        try:
            # 修改output_dir到临时目录
            summary.output_dir = os.path.join(test_dir, "output")
            os.makedirs(summary.output_dir, exist_ok=True)
            
            # 修改compare_dates
            summary.compare_dates = {
                'previous': yesterday_date,
                'current': today_date
            }
            
            # 调用create_comparison_document方法生成HTML
            print("\n1. 测试HTML文档生成...")
            html_path = summary.create_comparison_document("pcp", image_pairs, "all")
            
            if html_path and os.path.exists(html_path):
                print(f"   ✓ HTML文档生成成功: {html_path}")
                
                # 检查HTML内容中的图片布局
                with open(html_path, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                
                # 检查是否包含flex布局
                if 'display: flex' in html_content and 'flex-wrap: nowrap' in html_content:
                    print("   ✓ HTML中包含正确的flex布局设置")
                else:
                    print("   ✗ HTML中缺少正确的flex布局设置")
            else:
                print("   ✗ HTML文档生成失败")
                return False
            
            # 调用convert_html_to_image方法将HTML转换为图片
            print("\n2. 测试图片转换...")
            img_path = summary.convert_html_to_image(html_path)
            
            if img_path and os.path.exists(img_path):
                print(f"   ✓ 图片转换成功: {img_path}")
                return True
            else:
                print("   ✗ 图片转换失败")
                return False
                
        finally:
            # 恢复原始的output_dir和compare_dates
            summary.output_dir = original_output_dir
            summary.compare_dates = original_compare_dates
            
    finally:
        # 清理临时目录
        shutil.rmtree(test_dir)

if __name__ == "__main__":
    # 运行测试
    test_merge_and_convert()
    print("\n=== 测试完成 ===")
