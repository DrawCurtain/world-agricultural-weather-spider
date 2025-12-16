import os
import shutil
import glob

# 获取项目根目录（cleanup_files.py所在目录的父目录）
project_root = os.path.dirname(os.path.abspath(__file__))

# 定义根目录中需要保留的文件列表
root_files_to_keep = [
    ".gitignore",
    "README.md",
    "requirements.txt",
    "setup.py"  # 如果存在的话
]

# 定义weather_spider目录中需要保留的文件列表
spider_files_to_keep = [
    "daily_summary.py",
    "downloader.py", 
    "parser.py",
    "network.py",
    "html_to_image.py",
    "cleanup_files.py",
    "__init__.py"
]

# 删除非代码文件
def cleanup():
    """删除非代码文件"""
    print("=== 开始清理非代码文件 ===")
    
    # 删除根目录下的HTML文件
    html_files = glob.glob(os.path.join(project_root, "weather_summary_*.html"))
    for file in html_files:
        if os.path.exists(file):
            os.remove(file)
            print(f"删除 {file}")
    
    # 删除根目录下的日志文件
    log_file = os.path.join(project_root, "debug.log")
    if os.path.exists(log_file):
        os.remove(log_file)
        print("删除 debug.log")
    
    # 删除根目录下的测试文件
    for file in ["check_images.py", "test_with_mock_data.py"]:
        file_path = os.path.join(project_root, file)
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"删除 {file}")
    
    # 删除根目录下的downloads目录
    downloads_dir = os.path.join(project_root, "downloads")
    if os.path.exists(downloads_dir):
        shutil.rmtree(downloads_dir)
        print("删除 downloads 目录")
    
    # 删除根目录下的其他非代码文件
    root_files = os.listdir(project_root)
    for file in root_files:
        file_path = os.path.join(project_root, file)
        if (file not in root_files_to_keep and 
            not file.startswith(".") and 
            not file == "bin" and
            not file == "weather_spider" and
            not file.startswith("__pycache__")):
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"删除 {file}")
    
    # 删除weather_spider目录下的__pycache__目录
    pycache_dir = os.path.join(project_root, "weather_spider", "__pycache__")
    if os.path.exists(pycache_dir):
        shutil.rmtree(pycache_dir)
        print("删除 weather_spider/__pycache__ 目录")
    
    print("=== 清理完成 ===")

# 主程序
if __name__ == "__main__":
    cleanup()
