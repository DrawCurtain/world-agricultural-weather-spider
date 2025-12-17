import sys
import os
import datetime
import tempfile

# 将weather_spider目录的父目录添加到Python路径
sys.path.append(os.path.dirname(__file__))

from weather_spider.daily_summary import DailyWeatherSummary

def test_html_to_image_layout():
    print("=== 测试HTML到图片的布局转换 ===")
    
    # 创建DailyWeatherSummary实例
    summary = DailyWeatherSummary()
    
    # 创建测试用的图片对
    # 由于没有实际下载的图片，我们创建一个模拟的HTML文件来测试布局
    test_html_path = os.path.join(summary.output_dir, "test_layout.html")
    
    # 创建一个简单的测试HTML，包含左右布局的图片容器
    test_html_content = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test Layout</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f0f0f0;
            width: 2000px; /* 固定宽度以确保左右布局有足够空间 */
        }
        .container {
            width: 1960px; /* 容器宽度略小于body，提供内边距空间 */
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        h1 {
            text-align: center;
            color: #333;
        }
        .image-container {
            margin-bottom: 40px;
            border: 1px solid #eee;
            padding: 15px;
            border-radius: 8px;
        }
        .image-pair {
            display: flex;
            justify-content: space-around;
            flex-wrap: nowrap;
            white-space: nowrap;
            overflow: hidden;
            width: 100%;
            height: auto;
        }
        .image-column {
            text-align: center;
            width: 48%;
            min-width: 0;
            box-sizing: border-box;
            padding: 0 5px;
            float: left;
        }
        img {
            max-width: 100%;
            height: auto;
            border: 1px solid #ddd;
            box-sizing: border-box;
            width: 900px; /* 固定图片宽度 */
            height: 600px; /* 固定图片高度 */
            background-color: #f5f5f5;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>测试左右布局</h1>
        
        <div class="image-container">
            <h3>测试图片对 - 左右布局</h3>
            <div class="image-pair">
                <div class="image-column">
                    <h4>左图片</h4>
                    <img src="data:image/svg+xml;charset=utf-8,%3Csvg%20xmlns%3D'http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg'%20width%3D'900'%20height%3D'600'%3E%3Crect%20width%3D'900'%20height%3D'600'%20fill%3D'%23f5f5f5'/%3E%3Ctext%20x%3D'450'%20y%3D'300'%20font-family%3D'Arial'%20font-size%3D'48'%20fill%3D'%23333'%20text-anchor%3D'middle'%20dominant-baseline%3D'middle'%3E左图片%3C/text%3E%3C/svg%3E" alt="Left Image">
                </div>
                <div class="image-column">
                    <h4>右图片</h4>
                    <img src="data:image/svg+xml;charset=utf-8,%3Csvg%20xmlns%3D'http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg'%20width%3D'900'%20height%3D'600'%3E%3Crect%20width%3D'900'%20height%3D'600'%20fill%3D'%23f5f5f5'/%3E%3Ctext%20x%3D'450'%20y%3D'300'%20font-family%3D'Arial'%20font-size%3D'48'%20fill%3D'%23333'%20text-anchor%3D'middle'%20dominant-baseline%3D'middle'%3E右图片%3C/text%3E%3C/svg%3E" alt="Right Image">
                </div>
            </div>
        </div>
    </div>
</body>
</html>'''
    
    # 确保输出目录存在
    if not os.path.exists(summary.output_dir):
        os.makedirs(summary.output_dir)
    
    # 写入测试HTML文件
    with open(test_html_path, "w", encoding="utf-8") as f:
        f.write(test_html_content)
    
    print(f"创建了测试HTML文件: {test_html_path}")
    
    # 使用summary对象的convert_html_to_image方法转换为图片
    print("开始将HTML转换为图片...")
    img_path = summary.convert_html_to_image(test_html_path)
    
    if img_path and os.path.exists(img_path):
        print(f"图片转换成功: {img_path}")
        print("请检查生成的图片，确认布局是否为左右并排")
    else:
        print("图片转换失败")

if __name__ == "__main__":
    test_html_to_image_layout()