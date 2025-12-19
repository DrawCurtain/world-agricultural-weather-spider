#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
直接生成图片对比工具
使用PIL库直接将图片拼接成对比图片，绕过HTML步骤
"""

import os
from PIL import Image, ImageDraw, ImageFont




def create_image_comparison(image_pairs, output_path, weather_type, group_desc, compare_dates, save_date_str):
    """直接创建图片对比

    Args:
        image_pairs: 图片对列表，格式为[(today_path, yesterday_path, region, subregion), ...]
        output_path: 输出图片路径
        weather_type: 天气类型（'pcp'或'tmp'）
        group_desc: 组描述（如'美国'、'巴西'等）
        compare_dates: 对比日期字典，包含'previous'和'current'
        save_date_str: 保存日期字符串
    """
    from datetime import datetime
    from .parser import WeatherParser

    # 初始化parser以使用get_chinese_region_name方法
    parser = WeatherParser()

    # 设置天气变量文本描述
    if weather_type == "pcp":
        weather_text = "降水预报"
    else:
        weather_text = "温度预报"

    # 配置参数：可以调整这些值来改变图片大小
    IMAGE_SCALE_FACTOR = 2.5  # 图片放大倍数
    CANVAS_WIDTH = 3200  # 画布宽度
    GAP_BETWEEN_IMAGES = 20  # 图片之间的间距

    # 计算画布大小
    # 首先计算每行的实际高度
    # 需要加载第一张图片来获取大致尺寸
    sample_row_height = 400  # 默认高度
    if image_pairs:
        try:
            sample_img = Image.open(image_pairs[0][0])
            sample_width, sample_height = sample_img.size
            # 使用配置的放大倍数计算样本高度
            sample_row_height = int(sample_height * IMAGE_SCALE_FACTOR)
        except:
            pass

    # 减小间距，让布局更紧凑
    # 每行高度：标题(40) + 图片(sample_row_height) + 间距(20) + 标签(25)
    row_height = 40 + sample_row_height + 20 + 25
    top_title_height = 100  # 减小顶部标题高度
    bottom_info_height = 60  # 减小底部信息高度
    margin = 30  # 减小边距

    # 使用配置的画布宽度
    canvas_width = CANVAS_WIDTH
    canvas_height = top_title_height + bottom_info_height + len(image_pairs) * row_height + margin * 2

    # 创建白色背景画布
    canvas = Image.new('RGB', (canvas_width, canvas_height), 'white')
    draw = ImageDraw.Draw(canvas)

    # 尝试加载字体，支持中文
    try:
        # Windows系统 - 增大字体大小并加粗
        title_font = ImageFont.truetype("simhei.ttf", 60)  # 进一步增大主标题
        # 尝试加载粗体版本
        try:
            title_font_bold = ImageFont.truetype("simhei.ttf", 60, weight="bold")
        except:
            title_font_bold = title_font

        header_font = ImageFont.truetype("simhei.ttf", 48)  # 增大地区标题
        try:
            header_font_bold = ImageFont.truetype("simhei.ttf", 48, weight="bold")
        except:
            header_font_bold = header_font

    except:
        try:
            # macOS/Linux系统 - 增大字体大小并加粗
            title_font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 60)
            try:
                title_font_bold = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 60)
            except:
                title_font_bold = title_font

            header_font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 48)
            try:
                header_font_bold = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 48)
            except:
                header_font_bold = header_font
        except:
            # 使用默认字体
            title_font = ImageFont.load_default()
            title_font_bold = title_font
            header_font = ImageFont.load_default()
            header_font_bold = header_font

    # 获取当前时间
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 绘制顶部标题 - 简化标题，更加醒目
    title_text = f"{group_desc}{weather_text}对比"
    title_bbox = draw.textbbox((0, 0), title_text, font=title_font_bold)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (canvas_width - title_width) // 2
    draw.text((title_x, 40), title_text, fill='black', font=title_font_bold)  # 使用加粗字体

    # 绘制生成时间
    time_text = f"生成时间: {current_time}"
    time_bbox = draw.textbbox((0, 0), time_text, font=header_font)
    time_width = time_bbox[2] - time_bbox[0]
    time_x = canvas_width - time_width - 50  # 右对齐，留50px边距
    draw.text((time_x, 110), time_text, fill='black', font=header_font)

    # 绘制日期信息
    date_text = f"当前数据日期: {compare_dates.get('current', save_date_str)}  前一期数据日期: {compare_dates.get('previous', '')}"
    date_bbox = draw.textbbox((0, 0), date_text, font=header_font)
    date_width = date_bbox[2] - date_bbox[0]
    date_x = (canvas_width - date_width) // 2  # 居中对齐
    draw.text((date_x, 110), date_text, fill='black', font=header_font)

    y_offset = 160  # 跳过日期信息，直接开始地区标题

    for today_path, yesterday_path, region, subregion in image_pairs:
        # 检查图片是否存在
        if not os.path.exists(today_path) or not os.path.exists(yesterday_path):
            print(f"警告: 图片不存在 - {today_path} 或 {yesterday_path}")
            continue

        # 绘制地区标题 - 使用加粗字体
        region_name = f"{parser.get_chinese_region_name(region)} - {parser.get_chinese_region_name(subregion)}"
        title = f"{region_name} {weather_text}"
        title_bbox = draw.textbbox((0, 0), title, font=header_font_bold)
        title_width = title_bbox[2] - title_bbox[0]
        title_x = (canvas_width - title_width) // 2
        draw.text((title_x, y_offset), title, fill='black', font=header_font_bold)
        y_offset += 50  # 减少间距，因为没有标签了

        # 加载并调整图片大小
        try:
            # 加载图片
            img_yesterday = Image.open(yesterday_path)
            img_today = Image.open(today_path)

            # 获取原始图片尺寸
            yest_width, yest_height = img_yesterday.size
            today_width, today_height = img_today.size

            # 使用昨天图片的尺寸作为基准（假设两张图尺寸相同）
            original_width = yest_width
            original_height = yest_height

            # 使用配置的放大倍数，让图片更大更清晰
            img_display_width = int(original_width * IMAGE_SCALE_FACTOR)
            img_display_height = int(original_height * IMAGE_SCALE_FACTOR)

            # 确保不会超出画布宽度
            max_possible_width = (canvas_width - GAP_BETWEEN_IMAGES) // 2
            if img_display_width > max_possible_width:
                img_display_width = max_possible_width
                img_display_height = int(original_height * (img_display_width / original_width))

            # 调整图片大小，保持宽高比
            img_yesterday = img_yesterday.resize((img_display_width, img_display_height), Image.Resampling.LANCZOS)
            img_today = img_today.resize((img_display_width, img_display_height), Image.Resampling.LANCZOS)

            # 计算图片位置（左右布局），居中分布
            gap_between = GAP_BETWEEN_IMAGES  # 使用配置的间距

            # 计算总宽度：两张图片 + 间距
            total_width = img_display_width * 2 + gap_between

            # 计算起始位置，让整个组合居中
            start_x = (canvas_width - total_width) // 2

            # 左边图片位置
            left_x = start_x

            # 右边图片位置：左边图片宽度 + 间距
            right_x = start_x + img_display_width + gap_between

            # 粘贴图片
            canvas.paste(img_yesterday, (left_x, y_offset))
            canvas.paste(img_today, (right_x, y_offset))

            # 不再绘制"前一天"和"今天"标签，让图片更大更清晰

            y_offset += img_display_height + 20  # 减小图片下方的间距

        except Exception as e:
            print(f"错误: 处理图片失败 - {e}")
            # 绘制错误信息
            error_text = f"图片加载失败: {region} - {subregion}"
            draw.text((100, y_offset), error_text, fill='red', font=text_font)
            y_offset += 100

    # 保存图片
    canvas.save(output_path, 'PNG', quality=95)
    print(f"成功生成对比图片: {output_path}")

    return output_path