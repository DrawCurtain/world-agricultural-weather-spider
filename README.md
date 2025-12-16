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

## 安装说明

1. **克隆仓库**
   ```bash
   git clone <仓库地址>
   cd spiderMan
   ```

2. **安装依赖**
   该项目依赖于以下Python库：
   - requests：用于网络请求
   - BeautifulSoup4：用于HTML解析
   - imgkit：用于HTML转图片

   ```bash
   pip install requests beautifulsoup4 imgkit
   ```

3. **安装wkhtmltoimage**
   imgkit依赖于wkhtmltoimage工具，需要单独安装：
   - Windows：下载安装包并添加到系统环境变量
   - Linux：`sudo apt-get install wkhtmltopdf`
   - macOS：`brew install wkhtmltopdf`

4. **配置wkhtmltoimage路径**：
   代码会自动检测以下默认安装路径：
   - Windows：`C:\Program Files\wkhtmltopdf\bin\wkhtmltoimage.exe`
   - Windows：`C:\Program Files (x86)\wkhtmltopdf\bin\wkhtmltoimage.exe`
   - Linux/macOS：`/usr/bin/wkhtmltoimage`
   - macOS (Homebrew)：`/opt/homebrew/bin/wkhtmltoimage`
   
   如果你的安装路径不在上述列表中，你可以：
   - 将wkhtmltoimage添加到系统PATH环境变量中
   - 或者在运行脚本时使用 `-e` 参数手动指定路径：
     ```bash
     python html_to_image.py -e "C:\\Custom\\Path\\to\\wkhtmltoimage.exe" input.html
     ```
   - 或者修改 `daily_summary.py` 文件中的 `potential_paths` 列表，添加你的自定义路径

## 使用方法

### 基本使用

直接运行主脚本：

```bash
python daily_summary.py
```

脚本将自动执行以下操作：
1. 下载当天和前一天的天气预报图片
2. 生成天气对比HTML文档
3. 将HTML文档转换为PNG图片
4. 将输出文件保存到`output/[日期]/`目录

### 清理环境

如果需要清理下载的图片和输出文件，可以运行清理脚本：

```bash
python cleanup_files.py
```

## 项目结构

```
spiderMan/
├── daily_summary.py    # 主程序入口
├── downloader.py       # 图片下载模块
├── parser.py           # 数据解析模块
├── html_to_image.py    # HTML转图片模块
├── network.py          # 网络请求模块
├── cleanup_files.py    # 环境清理脚本
├── .gitignore          # Git忽略规则
└── README.md           # 项目说明文档
```

## 输出文件说明

脚本执行后，输出文件将保存在`output/[日期]/`目录下：

- `weather_summary_pcp_usa_[日期].html`：美国大豆产区降水预报对比HTML
- `weather_summary_pcp_others_[日期].html`：其他国家大豆产区降水预报对比HTML
- `weather_summary_tmp_usa_[日期].html`：美国大豆产区温度预报对比HTML
- `weather_summary_tmp_others_[日期].html`：其他国家大豆产区温度预报对比HTML
- 对应的PNG图片文件：由HTML文档转换而来

## 依赖项

- Python 3.6+
- requests
- BeautifulSoup4
- imgkit
- wkhtmltoimage (外部工具)

## 注意事项

1. 首次运行时，由于没有前一天的数据，系统会使用当天的数据进行对比
2. 系统默认使用当前日期作为基准日期
3. 如果网络连接不稳定，可能会导致图片下载失败
4. 确保wkhtmltoimage工具已正确安装并添加到系统环境变量

## 许可证

MIT License