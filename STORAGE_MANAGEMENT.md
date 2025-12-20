# 存储管理策略

## 问题说明

随着时间推移，天气爬虫会不断生成以下文件：

1. **downloads目录**：每天下载的原始天气图片
2. **output目录**：每天生成的对比图片
3. **debug.log**：运行日志文件

如果不进行清理，这些文件会持续累积，可能导致：
- GitHub仓库存储空间不足
- GitHub Actions执行时间变长
- 文件检索和管理困难

## 自动清理机制

### 默认策略
- **保留天数**：7天（可通过环境变量自定义）
- **清理时机**：每次运行前自动清理
- **清理范围**：
  - `downloads/` 目录下超过保留天数的文件
  - `output/` 目录下超过保留天数的文件
  - 空目录自动删除

### 配置方法

#### 1. 通过环境变量修改保留天数
在GitHub Actions中添加环境变量：
```yaml
env:
  RETENTION_DAYS: 14  # 保留14天而不是默认的7天
```

#### 2. 修改清理配置
编辑 `.github/cleanup-config.sh` 文件：
```bash
RETENTION_DAYS=14  # 修改默认保留天数
CLEANUP_DIRS=(
    "downloads"
    "output"
)
FILE_PATTERNS=(
    "*.png"      # 只清理图片文件
    "*.jpg"
    "*.jpeg"
)
```

## Artifacts管理

GitHub Actions还会将生成的文件上传为Artifacts：

- **保留策略**：30天自动过期
- **命名格式**：`weather-outputs-<run-number>`
- **包含内容**：
  - `output/` 目录（生成的对比图片）
  - `debug.log`（运行日志）

## 手动清理

如果需要手动清理历史数据：

### 1. 通过GitHub网页界面
1. 进入仓库的Actions页面
2. 点击相应的workflow
3. 在Artifacts部分可以下载或删除历史Artifacts

### 2. 使用Git命令（本地）
```bash
# 查看大文件
git rev-list --objects --all | git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' | sed -n 's/^blob //p' | sort --numeric-sort --key=2 | tail -20

# 如果意外提交了大文件，使用BFG或git-filter-repo清理
```

## 存储优化建议

### 1. 调整图片质量
在代码中可以调整生成的图片质量以减少文件大小：
```python
# 在image_generator.py中
image.save(output_path, 'PNG', optimize=True, quality=85)
```

### 2. 定期检查存储使用情况
可以在workflow中添加存储检查：
```yaml
- name: Check storage usage
  run: |
    echo "Disk usage:"
    df -h
    echo "Directory sizes:"
    du -sh downloads output 2>/dev/null || true
```

### 3. 使用外部存储
对于长期存储需求，可以考虑：
- 将文件上传到CDN（如AWS S3、阿里云OSS）
- 使用GitHub Release存储重要数据
- 集成到云存储服务

## 监控和告警

可以在workflow中添加存储使用监控：
```yaml
- name: Storage monitoring
  run: |
    # 设置阈值（例如1GB）
    THRESHOLD_GB=1
    USAGE=$(du -s downloads output 2>/dev/null | awk '{sum+=$1} END {print int(sum/1024/1024)}')

    if [ "$USAGE" -gt "$THRESHOLD_GB" ]; then
      echo "⚠️ Storage usage is high: ${USAGE}GB (threshold: ${THRESHOLD_GB}GB)"
      # 可以发送通知或采取其他行动
    fi
```

## 常见问题

### Q: 清理会影响工作吗？
A: 不会。清理只删除超过保留天数的文件，当天和前几天需要的文件都会保留。

### Q: 如何保留特定文件？
A: 可以在清理配置中排除特定文件或目录：
```bash
# 在cleanup-config.sh中添加
find "$dir" -type f -mtime +$days -not -name "important_*" -delete
```

### Q: GitHub Actions有存储限制吗？
A: 是的：
- 仓库存储：10GB
- Artifacts存储：免费版500MB/月，Pro版2GB/月
- 单个Artifact：最大2GB

## 最佳实践

1. **定期检查**：每月检查一次存储使用情况
2. **合理设置**：根据实际需求调整保留天数
3. **及时清理**：不要等到存储满了才清理
4. **监控告警**：设置存储使用阈值告警
5. **备份重要**：重要数据及时备份到其他位置