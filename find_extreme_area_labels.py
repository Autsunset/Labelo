#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
找出标签面积中位数，并找出大于面积中位数或小于中位数XX%的标签
"""

import os
import statistics
import time


def calculate_label_area(width, height, x_center, y_center, bbox_width, bbox_height):
    """
    计算标签的面积（像素数）
    
    Args:
        width: 图像宽度
        height: 图像高度
        x_center: 归一化的x中心坐标
        y_center: 归一化的y中心坐标
        bbox_width: 归一化的边界框宽度
        bbox_height: 归一化的边界框高度
    
    Returns:
        float: 标签面积（像素数）
    """
    bbox_width_pixel = bbox_width * width
    bbox_height_pixel = bbox_height * height
    
    return bbox_width_pixel * bbox_height_pixel


def find_extreme_area_labels(label_dir, image_dir, above_percent=150, below_percent=50):
    """
    找出标签面积中位数，并找出大于面积中位数或小于中位数XX%的标签
    
    Args:
        label_dir: 标签文件所在目录
        image_dir: 图像文件所在目录
        above_percent: 大于中位数的百分比阈值，默认150%（即大于中位数1.5倍）
        below_percent: 小于中位数的百分比阈值，默认50%（即小于中位数的一半）
    
    Returns:
        dict: 统计信息和极端面积标签
    """
    from PIL import Image
    
    stats = {
        'total_files': 0,
        'total_labels': 0,
        'median_area': 0,
        'above_threshold': above_percent,
        'below_threshold': below_percent,
        'large_labels': [],
        'small_labels': []
    }
    
    areas_only = []
    large_labels_data = []
    small_labels_data = []
    
    start_time = time.time()
    
    # 获取所有标签文件
    label_files = [f for f in os.listdir(label_dir) if f.endswith('.txt')]
    total_files = len(label_files)
    
    print(f"开始分析标签面积，共 {total_files} 个标签文件...")
    
    # 遍历标签文件
    for idx, filename in enumerate(label_files, 1):
        label_path = os.path.join(label_dir, filename)
        
        # 获取对应的图像文件
        image_name = os.path.splitext(filename)[0]
        image_path = None
        for ext in ['.jpg', '.jpeg', '.png', '.bmp']:
            temp_path = os.path.join(image_dir, image_name + ext)
            if os.path.exists(temp_path):
                image_path = temp_path
                break
        
        if not image_path:
            print(f"警告：找不到 {filename} 对应的图像文件")
            continue
        
        # 读取图像尺寸（使用PIL，比OpenCV更快）
        try:
            with Image.open(image_path) as img:
                width, height = img.size
        except Exception as e:
            print(f"警告：处理图像 {image_path} 时出错: {e}")
            continue
        
        # 读取标签文件
        with open(label_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
        
        for line in lines:
            parts = line.split()
            if len(parts) >= 5:
                try:
                    class_id = int(parts[0])
                    x_center = float(parts[1])
                    y_center = float(parts[2])
                    bbox_width = float(parts[3])
                    bbox_height = float(parts[4])
                    
                    area = calculate_label_area(width, height, x_center, y_center, bbox_width, bbox_height)
                    bbox_w_pixel = bbox_width * width
                    bbox_h_pixel = bbox_height * height
                    
                    areas_only.append(area)
                    
                    # 临时保存数据用于后续分析
                    large_labels_data.append({
                        'filename': filename,
                        'class_id': class_id,
                        'area': area,
                        'width': bbox_w_pixel,
                        'height': bbox_h_pixel
                    })
                    
                    stats['total_labels'] += 1
                
                except ValueError as e:
                    print(f"警告：解析标签 {filename} 时出错: {e}")
        
        stats['total_files'] += 1
        
        # 打印进度（每处理100个文件或最后一个文件时显示）
        if idx % 100 == 0 or idx == total_files:
            elapsed = time.time() - start_time
            print(f"进度: {idx}/{total_files} ({(idx/total_files*100):.1f}%) - 已处理 {stats['total_labels']} 个标签 - 耗时 {elapsed:.2f} 秒")
    
    # 计算中位数和极端标签
    if areas_only:
        stats['median_area'] = statistics.median(areas_only)
        
        above_threshold_area = stats['median_area'] * above_percent / 100
        below_threshold_area = stats['median_area'] * below_percent / 100
        
        for item in large_labels_data:
            if item['area'] > above_threshold_area:
                stats['large_labels'].append(item)
            elif item['area'] < below_threshold_area:
                stats['small_labels'].append(item)
    
    total_time = time.time() - start_time
    
    # 打印统计信息
    print("\n" + "=" * 60)
    print("标签面积分析结果")
    print("=" * 60)
    print(f"分析的标签文件数: {stats['total_files']}")
    print(f"总标签数: {stats['total_labels']}")
    print(f"标签面积中位数: {stats['median_area']:.2f} 像素")
    print(f"大于中位数 {above_percent}% 的阈值: {above_threshold_area:.2f} 像素")
    print(f"小于中位数 {below_percent}% 的阈值: {below_threshold_area:.2f} 像素")
    print(f"\n大于阈值的标签数: {len(stats['large_labels'])}")
    print(f"小于阈值的标签数: {len(stats['small_labels'])}")
    print(f"\n总处理时间: {total_time:.2f} 秒")
    
    if stats['large_labels']:
        print("\n" + "=" * 60)
        print(f"大于中位数 {above_percent}% 的标签:")
        print("-" * 60)
        for item in stats['large_labels']:
            print(f"{item['filename']} (类别{item['class_id']}): {item['area']:.2f} 像素 "
                  f"({item['width']:.1f}x{item['height']:.1f})")
    
    if stats['small_labels']:
        print("\n" + "=" * 60)
        print(f"小于中位数 {below_percent}% 的标签:")
        print("-" * 60)
        for item in stats['small_labels']:
            print(f"{item['filename']} (类别{item['class_id']}): {item['area']:.2f} 像素 "
                  f"({item['width']:.1f}x{item['height']:.1f})")
    
    return stats


def main():
    """主函数"""
    print("=" * 60)
    print("标签面积极端值分析工具")
    print("=" * 60)
    
    label_dir = input("请输入标签文件夹路径：").strip()
    image_dir = input("请输入图像文件夹路径：").strip()
    
    while True:
        try:
            above_percent = int(input("请输入大于中位数的百分比阈值（默认150）：").strip() or "150")
            break
        except ValueError:
            print("请输入有效数字")
    
    while True:
        try:
            below_percent = int(input("请输入小于中位数的百分比阈值（默认50）：").strip() or "50")
            break
        except ValueError:
            print("请输入有效数字")
    
    if not os.path.isdir(label_dir):
        print(f"错误：标签文件夹不存在：{label_dir}")
        return
    
    if not os.path.isdir(image_dir):
        print(f"错误：图像文件夹不存在：{image_dir}")
        return
    
    find_extreme_area_labels(label_dir, image_dir, above_percent, below_percent)


if __name__ == "__main__":
    main()