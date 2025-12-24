# GitHub Actions 天气数据获取时区问题修复总结

## 问题描述

项目在 GitHub Actions 上运行，无法获取前一天的天气数据，导致每天生成的合并文件都不对。

### 根本原因

**时区处理错误**：

1. **GitHub Actions 设置了时区环境变量**：
   ```yaml
   env:
     TZ: 'Asia/Shanghai'  # 设置时区为北京时间
   ```

2. **但代码中的时间获取逻辑有问题**：
   ```python
   # 修复前（weather_spider/config.py:26-30）
   def get_current_time(self) -> datetime.datetime:
       """获取当前时间（考虑时区）"""
       # 在GitHub Actions中，时区已经在workflow中设置
       # 在本地，使用系统时间
       return datetime.datetime.now()  # ❌ 没有使用时区！
   ```

3. **时间判断逻辑错误**：
   - 在容器中，`datetime.datetime.now()` 可能返回 UTC 时间
   - 当 GitHub Actions 设置为北京时间 19:30 时，实际的 `now` 可能是 UTC 时间
   - 这导致日期判断错误，下载了错误的日期数据

## 修复方案

### 1. 修改 config.py - 正确处理时区

#### 添加时区库支持

```python
try:
    # Python 3.9+ 有内置的 zoneinfo
    from zoneinfo import ZoneInfo
    HAS_ZONEINFO = True
except (ImportError, Exception):
    # 对于旧版本，使用 pytz
    try:
        import pytz
        HAS_ZONEINFO = False
    except ImportError:
        # 如果都没有，使用系统时间（备选）
        HAS_ZONEINFO = None
```

#### 初始化时区对象

```python
def __init__(self):
    # 从环境变量获取时区设置
    self.timezone_str = os.getenv('WEATHER_SPIDER_TIMEZONE', 'Asia/Shanghai')

    # 初始化时区
    self.timezone = None
    if HAS_ZONEINFO is True:
        try:
            self.timezone = ZoneInfo(self.timezone_str)
        except Exception as e:
            print(f"警告：无法初始化ZoneInfo '{self.timezone_str}': {e}")
    elif HAS_ZONEINFO is False:
        try:
            self.timezone = pytz.timezone(self.timezone_str)
        except Exception as e:
            print(f"警告：无法初始化pytz时区 '{self.timezone_str}': {e}")
```

#### 修复 get_current_time 方法

```python
def get_current_time(self) -> datetime.datetime:
    """获取当前时间（考虑时区）"""
    if self.timezone:
        # 如果有时区信息，返回带时区的时间
        if HAS_ZONEINFO is True:
            return datetime.datetime.now(self.timezone)
        elif HAS_ZONEINFO is False:
            return datetime.datetime.now(self.timezone)
    else:
        # 如果没有时区库，返回系统本地时间
        return datetime.datetime.now()
```

#### 修复时间比较逻辑

```python
def get_cutoff_time(self, current_time: datetime.datetime) -> datetime.datetime:
    """获取截止时间（北京时间19:30）"""
    # 确保 current_time 是带时区的 datetime
    if current_time.tzinfo is None and self.timezone:
        if HAS_ZONEINFO is True:
            current_time = current_time.replace(tzinfo=self.timezone)
        elif HAS_ZONEINFO is False:
            current_time = self.timezone.localize(current_time)

    # 创建截止时间（保留时区信息）
    if current_time.tzinfo:
        cutoff_naive = current_time.replace(hour=19, minute=30, second=0, microsecond=0)
        if cutoff_naive.tzinfo != current_time.tzinfo:
            cutoff_naive = cutoff_naive.replace(tzinfo=current_time.tzinfo)
        return cutoff_naive
    else:
        return current_time.replace(hour=19, minute=30, second=0, microsecond=0)

def should_download_previous_day(self, current_time: datetime.datetime) -> bool:
    """判断是否应该下载前一天的数据（19:30前）"""
    # 确保 current_time 包含时区信息
    if current_time.tzinfo is None and self.timezone:
        if HAS_ZONEINFO is True:
            current_time = current_time.replace(tzinfo=self.timezone)
        elif HAS_ZONEINFO is False:
            current_time = self.timezone.localize(current_time)

    cutoff_time = self.get_cutoff_time(current_time)
    return current_time < cutoff_time
```

### 2. 更新 requirements.txt

添加 `pytz` 依赖，确保在所有 Python 版本中都能正确处理时区：

```
requests
pyinstaller
Pillow>=9.0.0
retrying
pytz
```

### 3. GitHub Actions 工作流验证

确认 `.github/workflows/daily-weather-spider.yml` 中的时区设置正确：

```yaml
env:
  PYTHONUNBUFFERED: '1'
  TZ: 'Asia/Shanghai'  # 设置时区为北京时间
```

## 修复效果

### 修复前

- ❌ `datetime.datetime.now()` 返回系统本地时间（可能是 UTC）
- ❌ 时间比较在错误时区中进行
- ❌ 导致下载错误日期的数据
- ❌ 合并文件使用错误的对比日期

### 修复后

- ✅ `get_current_time()` 正确返回北京时间
- ✅ 时间比较在正确的时区中进行
- ✅ 确保在 19:30 前下载前一天数据，19:30 后下载当天数据
- ✅ 合并文件使用正确的对比日期

## 测试验证

创建了 `test_timezone_fix.py` 测试脚本，验证：

1. 配置正确加载
2. 当前时间获取正确
3. 截止时间计算正确
4. 判断逻辑正确
5. 日期逻辑正确

### 测试结果示例

```
时区修复测试
============================================================

1. 检查配置:
   时区字符串: Asia/Shanghai
   时区对象: pytz timezone 'Asia/Shanghai'
   运行模式: github_actions

2. 获取当前时间:
   当前时间: 2025-12-24 14:46:07.762721+08:00
   时区信息: CST+08:00

3. 测试截止时间:
   截止时间 (19:30): 2025-12-24 19:30:00+08:00

4. 测试判断逻辑:
   是否应该下载前一天数据: True

5. 模拟测试:
   北京时间 10:00 - 是否下载前一天: True (应该是 True)
   北京时间 20:00 - 是否下载前一天: False (应该是 False)

6. 检查日期逻辑:
   当前判断：下载昨天数据
   保存日期: 20251223
   对比日期: 20251222 vs 20251223

7. 验证结果:
   当前时间 14:46 < 19:30，预期下载前一天: True
   ✅ 时区逻辑正确！
```

## 兼容性说明

1. **Python 3.9+**: 使用内置的 `zoneinfo` 模块
2. **Python 3.8 及以下**: 使用 `pytz` 库（已在 requirements.txt 中添加）
3. **无时区库**: 回退到系统本地时间（不推荐，但确保程序不崩溃）

## 部署建议

1. 提交修复后的代码到仓库
2. 等待下次 GitHub Actions 定时运行或手动触发
3. 查看运行日志，确认时区设置正确
4. 检查下载的数据日期是否正确
5. 验证生成的合并文件是否使用正确的对比日期

## 监控要点

在 GitHub Actions 日志中关注：

```
时区设置: Asia/Shanghai
运行模式: github_actions
当前时间: 2025-12-24 19:30:00  # 应该显示北京时间
```

确保时间显示为北京时间且时区信息正确。

## 总结

此次修复解决了 GitHub Actions 中天气数据获取的时区问题，确保：

1. 正确识别当前北京时间
2. 正确判断是否应该下载前一天数据
3. 正确生成对比文件

修复后的代码具有更好的兼容性，能在不同 Python 版本和环境中稳定运行。
