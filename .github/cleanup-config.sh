#!/bin/bash
# GitHub Actions 清理配置
# 可以通过修改这些变量来自定义清理行为

# 保留天数（默认7天）
RETENTION_DAYS=${RETENTION_DAYS:-7}

# 需要清理的目录
CLEANUP_DIRS=(
    "downloads"
    "output"
)

# 日志文件保留天数（如果需要的话）
LOG_RETENTION_DAYS=${LOG_RETENTION_DAYS:-3}

# 文件类型模式（可选，留空表示清理所有文件）
FILE_PATTERNS=(
    "*.png"
    "*.jpg"
    "*.jpeg"
    "*.log"
)

# 清理函数
cleanup_old_files() {
    local dir=$1
    local days=$2

    echo "清理目录: $dir (保留 $days 天)"

    if [ -d "$dir" ]; then
        # 清理旧文件
        if [ ${#FILE_PATTERNS[@]} -gt 0 ] && [ "${FILE_PATTERNS[0]}" != "" ]; then
            # 按文件类型清理
            for pattern in "${FILE_PATTERNS[@]}"; do
                find "$dir" -type f -name "$pattern" -mtime +$days -delete 2>/dev/null || true
            done
        else
            # 清理所有文件
            find "$dir" -type f -mtime +$days -delete 2>/dev/null || true
        fi

        # 清理空目录
        find "$dir" -type d -empty -delete 2>/dev/null || true
    else
        echo "目录不存在: $dir"
    fi
}

# 主清理流程
echo "开始清理旧文件..."
echo "保留天数: $RETENTION_DAYS"

for dir in "${CLEANUP_DIRS[@]}"; do
    cleanup_old_files "$dir" "$RETENTION_DAYS"
done

echo "清理完成！"