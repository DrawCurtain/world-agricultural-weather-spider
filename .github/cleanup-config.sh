#!/bin/bash
# GitHub Actions 清理配置
# 按日期目录名清理，保留最近几天的数据用于对比

# 保留天数（默认90天，确保有足够的历史数据用于对比）
RETENTION_DAYS=${RETENTION_DAYS:-90}

# 需要清理的目录
CLEANUP_DIRS=(
    "downloads/pcp"
    "downloads/tmp"
)

# 日志文件保留天数（如果需要的话）
LOG_RETENTION_DAYS=${LOG_RETENTION_DAYS:-3}

# 清理函数 - 按日期目录清理
cleanup_old_date_dirs() {
    local base_dir=$1
    local days=$2

    echo "清理目录: $base_dir (保留最近 $days 天的数据)"

    if [ -d "$base_dir" ]; then
        # 获取当前日期的YYYYMMDD格式
        local current_date=$(date +%Y%m%d)

        # 计算要删除的日期阈值（RETENTION_DAYS天前的日期）
        local cutoff_date=$(date -d "$days days ago" +%Y%m%d 2>/dev/null || date -v-${days}d +%Y%m%d 2>/dev/null)

        if [ -z "$cutoff_date" ]; then
            echo "无法计算截止日期，跳过清理"
            return
        fi

        echo "当前日期: $current_date"
        echo "截止日期: $cutoff_date (此日期之前的目录将被删除)"

        # 遍历所有日期目录（格式为YYYYMMDD）
        for date_dir in "$base_dir"/*; do
            if [ -d "$date_dir" ]; then
                # 提取目录名中的日期部分
                local dirname=$(basename "$date_dir")

                # 检查是否是有效的日期格式（8位数字）
                if [[ "$dirname" =~ ^[0-9]{8}$ ]]; then
                    # 如果日期早于截止日期，则删除该目录
                    if [ "$dirname" -lt "$cutoff_date" ]; then
                        echo "删除旧目录: $date_dir"
                        rm -rf "$date_dir" 2>/dev/null || true
                    else
                        echo "保留目录: $date_dir"
                    fi
                fi
            fi
        done

        # 清理空目录
        find "$base_dir" -type d -empty -delete 2>/dev/null || true
    else
        echo "目录不存在: $base_dir"
    fi
}

# 清理函数 - 按文件修改时间清理（用于output目录）
cleanup_old_files_by_mtime() {
    local dir=$1
    local days=$2

    echo "清理目录: $dir (保留 $days 天)"

    if [ -d "$dir" ]; then
        # 清理所有旧文件
        find "$dir" -type f -mtime +$days -delete 2>/dev/null || true

        # 清理空目录
        find "$dir" -type d -empty -delete 2>/dev/null || true
    else
        echo "目录不存在: $dir"
    fi
}

# 主清理流程
echo "开始清理旧文件..."
echo "保留天数: $RETENTION_DAYS"

# 按日期目录清理downloads
for dir in "${CLEANUP_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        cleanup_old_date_dirs "$dir" "$RETENTION_DAYS"
    fi
done

# 按文件修改时间清理output目录
if [ -d "output" ]; then
    cleanup_old_files_by_mtime "output" "$RETENTION_DAYS"
fi

echo "清理完成！"