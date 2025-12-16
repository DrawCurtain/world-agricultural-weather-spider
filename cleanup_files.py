import os
import shutil
import glob

# 获取当前目录下的所有文件
all_files = os.listdir(".")

# 定义代码文件列表
code_files = [
    "daily_summary.py",
    "downloader.py", 
    "parser.py",
    "network.py",
    "html_to_image.py",
    "cleanup_files.py"
]

# 删除非代码文件
def cleanup():
    """删除非代码文件"""
    print("=== 开始清理非代码文件 ===")
    
    # 删除HTML文件
    html_files = glob.glob("weather_summary_*.html")
    for file in html_files:
        if os.path.exists(file):
            os.remove(file)
            print(f"删除 {file}")
    
    # 删除日志文件
    if os.path.exists("debug.log"):
        os.remove("debug.log")
        print("删除 debug.log")
    
    # 删除check_images.py和test_with_mock_data.py
    for file in ["check_images.py", "test_with_mock_data.py"]:
        if os.path.exists(file):
            os.remove(file)
            print(f"删除 {file}")
    
    # 删除downloads目录
    if os.path.exists("downloads"):
        shutil.rmtree("downloads")
        print("删除 downloads 目录")
    
    # 删除其他非代码文件
    for file in all_files:
        if file not in code_files and not file.startswith(".") and not file.startswith("__pycache__"):
            if os.path.isfile(file):
                os.remove(file)
                print(f"删除 {file}")
    
    # 删除__pycache__目录
    if os.path.exists("__pycache__"):
        shutil.rmtree("__pycache__")
        print("删除 __pycache__ 目录")
    
    print("=== 清理完成 ===")

# 主程序
if __name__ == "__main__":
    cleanup()
