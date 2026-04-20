#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
根据标签类别将图片分类到不同文件夹
"""

import os
import shutil
from pathlib import Path


def sort_images_by_labels(image_dir, label_dir, classes_file, output_dir):
    """
    根据标签类别将图片分类到不同文件夹
    
    Args:
        image_dir: 图片文件夹路径
        label_dir: 标签文件夹路径
        classes_file: 类别文件 (classes.txt) 路径
        output_dir: 输出文件夹路径
    """
    # 读取类别文件
    with open(classes_file, 'r', encoding='utf-8') as f:
        class_names = [line.strip() for line in f.readlines() if line.strip()]
    
    print(f"共读取到 {len(class_names)} 个类别：{class_names}")
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 为每个类别创建子文件夹
    for class_name in class_names:
        os.makedirs(os.path.join(output_dir, class_name), exist_ok=True)
    
    # 创建一个混合类别文件夹（用于包含多个标签的图片）
    os.makedirs(os.path.join(output_dir, 'mixed'), exist_ok=True)
    
    # 统计信息
    stats = {class_name: 0 for class_name in class_names}
    stats['mixed'] = 0
    stats['no_label'] = 0
    
    # 遍历所有图片文件
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.webp']
    image_files = [f for f in os.listdir(image_dir) 
                   if os.path.splitext(f)[1].lower() in image_extensions]
    
    print(f"找到 {len(image_files)} 张图片")
    
    for image_file in image_files:
        # 获取对应的标签文件名
        base_name = os.path.splitext(image_file)[0]
        label_file = os.path.join(label_dir, f"{base_name}.txt")
        
        if not os.path.exists(label_file):
            # 没有标签文件的图片
            print(f"警告：{image_file} 没有对应的标签文件")
            stats['no_label'] += 1
            continue
        
        # 读取标签文件
        with open(label_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 提取该图片中的所有类别
        image_classes = set()
        for line in lines:
            if line.strip():
                class_id = int(line.split()[0])
                if 0 <= class_id < len(class_names):
                    image_classes.add(class_names[class_id])
        
        # 根据类别数量决定复制到哪个文件夹
        if len(image_classes) == 0:
            stats['no_label'] += 1
        elif len(image_classes) == 1:
            # 只有一个类别
            class_name = list(image_classes)[0]
            target_dir = os.path.join(output_dir, class_name)
            shutil.copy2(
                os.path.join(image_dir, image_file),
                os.path.join(target_dir, image_file)
            )
            stats[class_name] += 1
        else:
            # 包含多个类别
            target_dir = os.path.join(output_dir, 'mixed')
            shutil.copy2(
                os.path.join(image_dir, image_file),
                os.path.join(target_dir, image_file)
            )
            stats['mixed'] += 1
    
    # 打印统计信息
    print("\n分类完成！统计信息：")
    print("-" * 40)
    for class_name in class_names:
        print(f"{class_name}: {stats[class_name]} 张")
    print(f"mixed (多类别): {stats['mixed']} 张")
    print(f"no_label (无标签): {stats['no_label']} 张")
    print("-" * 40)
    print(f"总计：{sum(stats.values())} 张")
    print(f"\n输出目录：{output_dir}")


def main():
    """主函数"""
    print("=" * 60)
    print("图片按标签分类工具")
    print("=" * 60)
    
    # 获取输入
    image_dir = input("\n请输入图片文件夹路径：").strip()
    label_dir = input("请输入标签文件夹路径：").strip()
    classes_file = input("请输入类别文件 (classes.txt) 路径：").strip()
    output_dir = input("请输入输出文件夹路径：").strip()
    
    # 验证路径
    if not os.path.isdir(image_dir):
        print(f"错误：图片文件夹不存在：{image_dir}")
        return
    
    if not os.path.isdir(label_dir):
        print(f"错误：标签文件夹不存在：{label_dir}")
        return
    
    if not os.path.isfile(classes_file):
        print(f"错误：类别文件不存在：{classes_file}")
        return
    
    # 执行分类
    sort_images_by_labels(image_dir, label_dir, classes_file, output_dir)


if __name__ == "__main__":
    main()
