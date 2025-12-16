#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML转图片工具
将HTML文件转换为PNG图片，支持中文显示
"""

import argparse
import os
import sys


def html_to_image(html_path, output_path=None, width=1200, height=None, executable=None):
    """将HTML文件转换为图片
    
    Args:
        html_path (str): HTML文件路径
        output_path (str): 输出图片路径，默认与HTML文件同名
        width (int): 图片宽度
        height (int): 图片高度，默认None（自动计算）
        
    Returns:
        bool: 是否转换成功
    """
    try:
        # 动态导入依赖，方便用户根据需要安装
        import imgkit
        
        # 设置默认输出路径
        if output_path is None:
            base_name = os.path.splitext(html_path)[0]
            output_path = f"{base_name}.png"
        
        # 检查HTML文件是否存在
        if not os.path.exists(html_path):
            print(f"错误: HTML文件 '{html_path}' 不存在")
            return False
        
        # 设置转换选项
        options = {
            'width': str(width),
            'disable-smart-width': '',
            'encoding': 'UTF-8',
            'quiet': '',  # 减少输出
            'enable-local-file-access': ''
        }
        
        # 只有当用户指定了高度时才设置
        if height is not None:
            options['height'] = str(height)
        
        # 配置imgkit
        if executable and os.path.exists(executable):
            imgkit_config = imgkit.config(wkhtmltoimage=executable)
        else:
            imgkit_config = None
        
        # 执行转换 - 使用from_file方法，保持相对路径有效性
        imgkit.from_file(html_path, output_path, options=options, config=imgkit_config)
        
        print(f"[SUCCESS] 成功将HTML转换为图片: {output_path}")
        print(f"[INFO] 图片宽度: {width}px，高度: {'自动计算' if height is None else height}px")
        return True
        
    except ImportError as e:
        print(f"[ERROR] 缺少依赖: {e}")
        print("请安装必要的依赖:")
        print("  pip install imgkit")
        print("  ")
        print("注意: 还需要安装 wkhtmltoimage，下载地址:")
        print("  Windows: https://wkhtmltopdf.org/downloads.html")
        print("  Linux: sudo apt-get install wkhtmltopdf")
        print("  MacOS: brew install wkhtmltopdf")
        return False
    except Exception as e:
        print(f"[ERROR] 转换失败: {e}")
        return False


def batch_convert(folder_path, width=1200, height=800, executable=None):
    """批量转换文件夹中的所有HTML文件
    
    Args:
        folder_path (str): 包含HTML文件的文件夹路径
        width (int): 图片宽度
        height (int): 图片高度
        
    Returns:
        int: 成功转换的文件数量
    """
    success_count = 0
    
    # 检查文件夹是否存在
    if not os.path.exists(folder_path):
        print(f"错误: 文件夹 '{folder_path}' 不存在")
        return 0
    
    # 遍历文件夹中的所有HTML文件
    for filename in os.listdir(folder_path):
        if filename.endswith('.html'):
            html_path = os.path.join(folder_path, filename)
            if html_to_image(html_path, width=width, height=height, executable=executable):
                success_count += 1
    
    print(f"\n[SUMMARY] 批量转换完成: 成功 {success_count} 个文件")
    return success_count


if __name__ == "__main__":
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description='HTML转图片工具')
    parser.add_argument('input', help='HTML文件路径或包含HTML文件的文件夹路径')
    parser.add_argument('-o', '--output', help='输出图片路径（仅用于单个文件转换）')
    parser.add_argument('-w', '--width', type=int, default=1200, help='图片宽度，默认1200px')
    parser.add_argument('-H', '--height', type=int, default=None, help='图片高度，默认自动计算')
    parser.add_argument('-b', '--batch', action='store_true', help='批量转换文件夹中的所有HTML文件')
    parser.add_argument('-e', '--executable', help='wkhtmltoimage可执行文件路径（可选）')
    
    # 解析命令行参数
    args = parser.parse_args()
    
    # 处理输入路径
    input_path = args.input
    
    # 批量转换模式
    if args.batch or os.path.isdir(input_path):
        batch_convert(input_path, width=args.width, height=args.height, executable=args.executable)
    
    # 单个文件转换模式
    else:
        html_to_image(
            input_path, 
            output_path=args.output, 
            width=args.width, 
            height=args.height,
            executable=args.executable
        )