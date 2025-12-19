# 全球农业天气数据爬虫

## 项目简介

本项目用于爬取全球主要农业地区的天气预报数据（包括降水和温度），生成对比图片供农业分析使用。

## 功能特点

- 自动下载美国、巴西、阿根廷等主要农业地区的天气预报数据
- 支持降水（pcp）和温度（tmp）两种天气类型
- 生成前一天和当天的天气对比图片
- 使用PIL库直接生成高质量图片，无需HTML转换
- 按地区分类生成对比报告（美国、巴西、阿根廷等）
- 自动根据时间判断下载当天的数据还是昨天的数据

## 项目结构

```
world-agricultural-weather-spider/
├── weather_spider/              # 核心代码目录
│   ├── __init__.py
│   ├── daily_summary.py         # 主要流程控制
│   ├── downloader.py            # 图片下载模块
│   ├── parser.py                # 数据解析模块
│   └── image_generator.py       # 图片生成模块
├── downloads/                   # 下载的原始图片存储目录
│   ├── pcp/                     # 降水数据
│   │   ├── 20251218/            # 按日期存储
│   │   └── 20251217/
│   └── tmp/                     # 温度数据
│       ├── 20251218/
│       └── 20251217/
├── output/                      # 生成的对比图片存储目录
│   └── 20251218/                # 按日期存储
├── bin/                         # 可执行文件目录
├── requirements.txt             # 项目依赖
├── setup.py                     # 安装配置
├── README.md                    # 项目说明
└── README_EXE.md                # 可执行版本说明
```

## 安装与使用

### 环境要求

- Python 3.7+
- 网络连接（用于下载数据）

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行方法

#### 方法1：使用Python模块方式运行

```bash
python -m weather_spider.daily_summary
```

#### 方法2：使用可执行文件（Windows）

1. 运行 `build_exe.bat` 生成可执行文件
2. 双击运行 `bin/天气爬虫.exe`

## 输出说明

程序运行后会生成以下对比图片：

- `weather_summary_pcp_usa_YYYYMMDD.png` - 美国降水预报对比
- `weather_summary_tmp_usa_YYYYMMDD.png` - 美国温度预报对比
- `weather_summary_pcp_brazil_YYYYMMDD.png` - 巴西降水预报对比
- `weather_summary_tmp_brazil_YYYYMMDD.png` - 巴西温度预报对比
- `weather_summary_pcp_argentina_YYYYMMDD.png` - 阿根廷降水预报对比
- `weather_summary_tmp_argentina_YYYYMMDD.png` - 阿根廷温度预报对比

### 图片布局说明

生成的对比图片包含：

1. **主标题**：地区+天气类型对比（如"美国降水预报对比"）
2. **生成时间**：图片生成的时间戳（右上角）
3. **日期信息**：当前数据和前一期数据的日期（居中）
4. **地区标题**：具体地区名称（如"美国 - 爱荷华州 降水预报"）
5. **对比图片**：前一天（左）和当天（右）的天气预报图

### 时间规则

- **19:30前**：下载昨天的数据，保存到昨天的文件夹
- **19:30后**：下载今天的数据，保存到今天的文件夹

## 技术实现

### 核心改进

1. **直接图片生成**：
   - 使用PIL库直接生成对比图片
   - 去除了HTML转图片的中间步骤
   - 提高了生成效率和图片质量

2. **优化的布局**：
   - 大标题：60px，加粗
   - 地区标题：48px，加粗
   - 图片放大2.5倍，确保清晰度
   - 自动居中布局，合理利用画布空间

3. **灵活的配置**：
   - `IMAGE_SCALE_FACTOR`：图片缩放因子（默认2.5）
   - `CANVAS_WIDTH`：画布宽度（默认3200px）
   - `GAP_BETWEEN_IMAGES`：图片间距（默认20px）

### 主要模块

- **DailyWeatherSummary**：主流程控制类
- **ImageDownloader**：负责下载天气图片
- **WeatherParser**：解析天气数据
- **ImageGenerator**：生成对比图片

## 注意事项

1. 程序需要稳定的网络连接以下载数据
2. 生成的图片较大，请确保有足够的磁盘空间
3. 如果某天的数据还未更新，程序会使用前一天的数据

## 常见问题

Q: 程序运行失败怎么办？
A: 检查网络连接和依赖是否正确安装，查看日志文件了解具体错误。

Q: 可以修改下载的地区吗？
A: 可以在 `downloader.py` 中修改地区列表和对应的URL。

Q: 如何调整图片大小？
A: 修改 `image_generator.py` 中的配置参数（IMAGE_SCALE_FACTOR、CANVAS_WIDTH等）。

## 更新日志

- 2025-12-19: 重构图片生成逻辑，使用PIL直接生成图片，提高效率和品质
- 2025-12-18: 优化图片布局，增大字体，改进显示效果
- 2025-12-17: 修复日期逻辑和路径问题
- 2025-12-16: 初始版本，支持基本的图片下载和对比功能