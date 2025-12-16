# 大豆作物天气预报对比系统

## 项目描述
该项目是一个自动化的大豆作物天气预报对比系统，用于下载、分析和对比全球主要大豆产区的15天天气预报数据，生成直观的对比文档。

## 功能特性

- **自动化数据下载**：自动从世界农业气象网站下载全球主要大豆产区的降水和温度预报图片
- **智能数据检查**：优先检查本地是否已存在前一天数据，避免重复下载，提高效率
- **日期对比分析**：支持将当天预报数据与前一天进行对比分析
- **图片对比展示**：生成左右对比的HTML文档，直观展示预报变化
- **分类组织**：按国家和地区分类展示预报数据，支持美国和其他国家单独查看
- **批量图片转换**：支持将HTML文档转换为PNG图片格式
- **日期目录结构**：按日期组织输出文件，方便查阅和管理
- **可执行文件**：提供Windows平台的可执行文件，无需安装Python环境即可运行

## 安装说明

### 方法一：使用Python源代码

1. **克隆仓库**
   ```bash
   git clone <仓库地址>
   cd spiderMan
   ```

2. **安装依赖**
   使用requirements.txt安装所有依赖：
   ```bash
   pip install -r requirements.txt
   ```

3. **关于wkhtmltoimage**
   - Windows：项目已内置`bin/wkhtmltoimage.exe`，无需额外安装
   - Linux：`sudo apt-get install wkhtmltopdf`
   - macOS：`brew install wkhtmltopdf`

### 方法二：使用可执行文件（仅Windows）

直接从项目的`dist`目录下载`weather_spider.exe`文件即可使用，无需安装Python环境。

## 使用方法

### 使用Python源代码

#### 基本使用

使用模块方式运行主程序：

```bash
python -m weather_spider.daily_summary
```

脚本将自动执行以下操作：
1. 下载当天和前一天的天气预报图片
2. 生成天气对比HTML文档
3. 将HTML文档转换为PNG图片
4. 将输出文件保存到`output/[日期]/`目录

#### 指定日期

可以使用`-d`或`--date`参数指定日期：

```bash
python -m weather_spider.daily_summary -d 20231216
```

#### 指定wkhtmltoimage路径

如果内置的wkhtmltoimage无法正常工作，可以使用`-w`或`--wkhtmltoimage`参数指定路径：

```bash
python -m weather_spider.daily_summary -w "C:\Custom\Path\to\wkhtmltoimage.exe"
```

#### 清理环境

如果需要清理下载的图片和输出文件，可以运行清理脚本：

```bash
python -m weather_spider.cleanup_files
```

### 使用可执行文件

在Windows系统中，直接运行`weather_spider.exe`文件即可：

```bash
.\weather_spider.exe
```

支持的命令行参数与Python版本相同：

```bash
.\weather_spider.exe -d 20231216 -w "C:\Custom\Path\to\wkhtmltoimage.exe"
```

## 项目结构

```
spiderMan/
├── README.md           # 项目说明文档
├── README_EXE.md       # 可执行文件使用说明
├── requirements.txt    # Python依赖列表
├── setup.py            # 项目安装配置
├── .gitignore          # Git忽略规则
├── bin/
│   └── wkhtmltoimage.exe  # Windows平台HTML转图片工具
├── dist/
│   └── weather_spider.exe  # 生成的Windows可执行文件
└── weather_spider/
    ├── __init__.py     # 包初始化文件
    ├── __main__.py     # 包入口点
    ├── daily_summary.py    # 主程序入口
    ├── downloader.py       # 图片下载模块
    ├── parser.py           # 数据解析模块
    ├── html_to_image.py    # HTML转图片模块
    ├── network.py          # 网络请求模块
    └── cleanup_files.py    # 环境清理脚本
```

## 输出文件说明

脚本执行后，输出文件将保存在以下目录：

- 下载的图片：`downloads/[类型]/[日期]/`
  - `类型`包括：`pcp`（降水）和`tmp`（温度）

- 生成的文档：`output/[日期]/`
  - `weather_summary_pcp_usa_[日期].html`：美国大豆产区降水预报对比HTML
  - `weather_summary_pcp_others_[日期].html`：其他国家大豆产区降水预报对比HTML
  - `weather_summary_tmp_usa_[日期].html`：美国大豆产区温度预报对比HTML
  - `weather_summary_tmp_others_[日期].html`：其他国家大豆产区温度预报对比HTML
  - 对应的PNG图片文件：由HTML文档转换而来

## 依赖项

- Python 3.6+（仅源代码版本需要）
- requests：用于网络请求
- BeautifulSoup4：用于HTML解析
- imgkit：用于HTML转图片
- wkhtmltoimage：用于HTML转图片（内置Windows版本）

## 注意事项

1. 首次运行时，由于没有前一天的数据，系统会使用当天的数据进行对比
2. 系统默认使用当前日期作为基准日期
3. 如果网络连接不稳定，可能会导致图片下载失败
4. Windows用户优先使用内置的wkhtmltoimage工具，无需额外安装
5. 使用可执行文件时，所有输出文件将保存在可执行文件所在目录

## 许可证

MIT License