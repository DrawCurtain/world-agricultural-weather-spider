# World Agricultural Weather Spider

全球农业天气数据爬虫，自动采集主要农业产区的降水和温度预报数据，并生成可视化对比图片。

## 功能特性

- 支持 5 种主要农作物：玉米、大豆、小麦、油菜籽、大麦
- 覆盖全球 9 个主要农业产区：美国、巴西、阿根廷、中国、加拿大、欧洲、乌克兰、澳大利亚、印度
- 自动下载降水（pcp）和温度（tmp）预报图片
- 生成左右对比的可视化图片（前一天 vs 当天）
- 支持按国家分组查看：美国、巴西、阿根廷、其他国家、全部

## 数据来源

- 数据源：全球农业天气预报系统
- 图片类型：15天降水预报、15天温度预报

## 本地运行

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行爬虫

```bash
# 方式1：使用模块方式
python -m weather_spider

# 方式2：安装后使用命令
pip install -e .
weather-spider
```

### 环境变量配置

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `WEATHER_SPIDER_TIMEZONE` | `Asia/Shanghai` | 时区设置 |
| `WEATHER_SPIDER_MODE` | `local` | 运行模式（local/github_actions） |
| `REQUEST_TIMEOUT` | `30` | 请求超时时间（秒） |
| `MAX_RETRIES` | `3` | 最大重试次数 |
| `RETRY_DELAY` | `5` | 重试延迟（秒） |

## 项目结构

```
world-agricultural-weather-spider/
├── run_weather_spider.py          # 主程序入口（用于打包exe）
├── weather_spider/                 # 核心爬虫模块
│   ├── __main__.py                # 包的主入口点
│   ├── config.py                  # 配置管理
│   ├── daily_summary.py           # 主要业务逻辑
│   ├── downloader.py              # 图片下载器
│   ├── parser.py                  # 数据解析器和URL构建
│   ├── network.py                 # 网络请求模块
│   └── image_generator.py         # 图片对比生成器
├── downloads/                      # 下载的原始图片数据
│   ├── pcp/                       # 降水数据
│   └── tmp/                       # 温度数据
├── output/                        # 生成的对比图片输出
├── requirements.txt               # 依赖包列表
└── setup.py                       # 项目安装配置
```

## 数据说明

### 时间逻辑

- **19:30 前**：下载前一天的数据
- **19:30 后**：下载当天的数据

### 对比图片生成

每次运行会生成以下对比图片：
- `weather_summary_pcp_usa_YYYYMMDD.png` - 美国降水对比
- `weather_summary_pcp_brazil_YYYYMMDD.png` - 巴西降水对比
- `weather_summary_pcp_argentina_YYYYMMDD.png` - 阿根廷降水对比
- `weather_summary_pcp_others_YYYYMMDD.png` - 其他国家降水对比
- `weather_summary_pcp_YYYYMMDD.png` - 所有国家降水对比
- `weather_summary_tmp_*.png` - 温度对比（同上结构）

## GitHub Actions

项目配置了 GitHub Actions 自动运行：

### 自动运行

- **触发时间**：每天 UTC 11:30（北京时间 19:30）
- **数据缓存**：使用 GitHub Actions Cache 缓存下载的图片数据
- **输出保留**：30 天
- **日志保留**：7 天

### 手动触发

在 GitHub 仓库的 Actions 页面，选择 "Daily Weather Spider" workflow，点击 "Run workflow" 按钮即可手动触发。

### 自动清理

每周日自动清理 30 天前的 artifacts，避免存储成本过高。

## 依赖项

```
requests          # HTTP请求库
Pillow>=9.0.0     # 图像处理库
retrying          # 重试机制
pytz              # 时区处理
```

## 许可证

MIT License
