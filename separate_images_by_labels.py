#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
按标签分离图像工具
将有标签和无标签的图像分离到不同文件夹
"""

import os
import shutil


def separate_images_by_labels(image_dir, label_dir, output_dir=None, move_files=True):
    """
    将图像按是否有标签分离
    
    Args:
        image_dir: 图像文件所在目录
        label_dir: 标签文件所在目录
        output_dir: 输出目录（默认与image_dir相同）
        move_files: 是否实际移动文件
    
    Returns:
        tuple: (有标签的图像数量, 无标签的图像数量)
    """
    if not os.path.exists(image_dir):
        raise FileNotFoundError(f"图像目录不存在: {image_dir}")
    
    if not os.path.exists(label_dir):
        raise FileNotFoundError(f"标签目录不存在: {label_dir}")
    
    # 创建目标子文件夹
    if output_dir:
        labeled_dir = os.path.join(output_dir, 'labeled')
        unlabeled_dir = os.path.join(output_dir, 'unlabeled')
    else:
        labeled_dir = os.path.join(image_dir, 'labeled')
        unlabeled_dir = os.path.join(image_dir, 'unlabeled')
    
    os.makedirs(labeled_dir, exist_ok=True)
    os.makedirs(unlabeled_dir, exist_ok=True)
    
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff'}
    
    image_files = []
    for filename in os.listdir(image_dir):
        file_ext = os.path.splitext(filename)[1].lower()
        if file_ext in image_extensions:
            image_path = os.path.join(image_dir, filename)
            if not (image_path.startswith(labeled_dir) or image_path.startswith(unlabeled_dir)):
                image_files.append(filename)
    
    total_files = len(image_files)
    print(f"总共找到 {total_files} 个图像文件")
    
    labeled_count = 0
    unlabeled_count = 0
    processed_count = 0
    
    print("开始分离图像文件...")
    for filename in image_files:
        base_name = os.path.splitext(filename)[0]
        label_filename = f"{base_name}.txt"
        label_path = os.path.join(label_dir, label_filename)
        image_path = os.path.join(image_dir, filename)
        
        if os.path.exists(label_path):
            labeled_count += 1
            target_dir = labeled_dir
        else:
            unlabeled_count += 1
            target_dir = unlabeled_dir
        
        if move_files:
            target_path = os.path.join(target_dir, filename)
            try:
                if os.path.exists(target_path):
                    os.remove(target_path)
                shutil.move(image_path, target_dir)
            except Exception as e:
                print(f"移动文件 {filename} 时出错: {e}")
        
        processed_count += 1
        
        if processed_count % 10 == 0 or processed_count == total_files:
            print(f"已处理 {processed_count} 个文件，进度: {int(processed_count/total_files*100)}%")
    
    print("图像分离已完成！")
    return labeled_count, unlabeled_count


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='将有标签和无标签的图像分离')
    parser.add_argument('--image_dir', type=str, required=True, help='图像文件所在目录')
    parser.add_argument('--label_dir', type=str, required=True, help='标签文件所在目录')
    parser.add_argument('--output_dir', type=str, default=None, help='输出目录')
    parser.add_argument('--dry_run', action='store_true', help='只显示操作但不实际移动文件')
    
    args = parser.parse_args()
    
    try:
        labeled_count, unlabeled_count = separate_images_by_labels(
            args.image_dir, 
            args.label_dir, 
            args.output_dir,
            move_files=not args.dry_run
        )
        
        action = "将执行" if args.dry_run else "已完成"
        print(f"\n{action}图像分离操作:")
        print(f"- 总图像数量: {labeled_count + unlabeled_count}")
        print(f"- 有标签的图像数量: {labeled_count}")
        print(f"- 无标签的图像数量: {unlabeled_count}")
        
    except Exception as e:
        print(f"执行过程中出错: {e}")