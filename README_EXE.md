# 天气数据爬虫 - 可执行文件使用说明

## 功能介绍

`daily_summary.exe` 是一个天气数据抓取和汇总工具，用于生成每日天气对比报告。它可以：

1. 自动下载指定日期的全球主要农业产区的天气数据图片
2. 解析图片中的天气信息
3. 生成HTML格式的天气对比报告
4. 将HTML报告转换为图片格式

## 生成的文件

在 `dist` 目录下可以找到以下文件：

- `daily_summary.exe` - 主程序可执行文件
- `downloads` - 下载的原始天气图片目录
- `output` - 生成的HTML报告和图片报告目录

## 使用方法

### 基本用法

1. 打开命令提示符（CMD）或PowerShell
2. 导航到 `dist` 目录：
   ```
   cd E:\spider\spiderMan\dist
   ```
3. 运行可执行文件：
   ```
   .\daily_summary.exe
   ```

程序将自动执行以下操作：
- 下载当天的天气数据图片
- 生成HTML报告
- 将HTML报告转换为图片

### 命令行参数（可选）

程序支持以下命令行参数：

- `--date` 或 `-d`：指定日期（格式：YYYYMMDD）
  ```
  .\daily_summary.exe --date 20251216
  ```

- `--wkhtmltoimage` 或 `-w`：指定wkhtmltoimage可执行文件路径（如果自动检测失败）
  ```
  .\daily_summary.exe --wkhtmltoimage "C:\path\to\wkhtmltoimage.exe"
  ```

### 输出文件说明

程序运行完成后，将在以下位置生成文件：

1. 原始图片下载位置：
   ```
   dist\downloads\pcp\[日期]
   dist\downloads\tmp\[日期]
   ```

2. HTML报告和图片报告位置：
   ```
   dist\output\[日期]
   ```
   - `weather_summary_pcp_usa_[日期].html` - 美国地区降水对比HTML报告
   - `weather_summary_pcp_others_[日期].html` - 其他地区降水对比HTML报告
   - `weather_summary_tmp_usa_[日期].html` - 美国地区温度对比HTML报告
   - `weather_summary_tmp_others_[日期].html` - 其他地区温度对比HTML报告
   - 对应的PNG图片文件

## 注意事项

1. **网络连接**：程序需要网络连接才能下载天气数据图片

2. **文件权限**：请确保程序有足够的权限读写文件和创建目录

3. **依赖文件**：
   - 程序已包含所有必要的Python依赖
   - 程序会自动检测 `bin` 目录下的 `wkhtmltoimage.exe`，用于将HTML转换为图片

4. **运行时间**：程序首次运行可能需要较长时间（约1-2分钟），因为需要下载大量图片

## 常见问题

### Q: 程序运行时提示找不到wkhtmltoimage.exe

A: 程序会自动检测 `bin` 目录下的 `wkhtmltoimage.exe`。如果检测失败，可以通过 `--wkhtmltoimage` 参数手动指定路径：

```
.\daily_summary.exe --wkhtmltoimage "E:\spider\spiderMan\dist\bin\wkhtmltoimage.exe"
```

### Q: 程序运行完成后没有生成图片报告

A: 请检查是否有 `wkhtmltoimage.exe` 文件，以及是否有足够的权限写入图片文件。

### Q: 下载的图片不完整或无法打开

A: 可能是网络连接问题导致下载失败。请检查网络连接并重试。

## 技术支持

如果遇到其他问题，请检查程序目录下的 `debug.log` 文件，查看详细的错误信息。

---

© 2025 天气数据爬虫工具
