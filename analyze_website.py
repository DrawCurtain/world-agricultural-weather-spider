import requests
from bs4 import BeautifulSoup

# 目标URL
url = 'http://www.worldagweather.com/crops.php#map=chart&crop=soybeans&region=usa&subregion=usa&vrbl=pcp&nday=15'

# 发送请求
try:
    response = requests.get(url)
    response.raise_for_status()  # 检查请求是否成功
    
    # 保存网页内容到文件，方便分析
    with open('website_content.html', 'w', encoding='utf-8') as f:
        f.write(response.text)
    
    print("网页内容已保存到 website_content.html")
    
    # 初步分析网页结构
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 查找所有图片标签
    images = soup.find_all('img')
    print(f"找到 {len(images)} 个图片标签")
    
    # 打印前10个图片的src属性
    for i, img in enumerate(images[:10]):
        src = img.get('src')
        print(f"图片 {i+1}: {src}")
    
    # 查找所有与图表相关的元素
    charts = soup.find_all(class_=lambda x: x and 'chart' in x.lower())
    print(f"找到 {len(charts)} 个与图表相关的元素")
    
    # 查找所有与降水(precipitation/pcp)和温度(temp)相关的元素
    weather_elements = soup.find_all(text=lambda x: x and ('pcp' in x.lower() or 'temp' in x.lower() or 'precipitation' in x.lower() or 'temperature' in x.lower()))
    print(f"找到 {len(weather_elements)} 个与天气相关的文本元素")
    
    # 打印前5个相关文本
    for i, elem in enumerate(weather_elements[:5]):
        print(f"天气相关文本 {i+1}: {elem.strip()}")
        
except requests.RequestException as e:
    print(f"请求失败: {e}")