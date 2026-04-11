#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
查找无标签图像工具
"""

import os


def find_images_without_labels(image_dir, label_dir):
    """
    查找没有对应标签文件的图像
    
    Args:
        image_dir: 图像文件目录
        label_dir: 标签文件目录
    
    Returns:
        list: 无标签图像列表
    """
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp'}
    images_without_labels = []
    
    for filename in os.listdir(image_dir):
        file_ext = os.path.splitext(filename)[1].lower()
        if file_ext in image_extensions:
            base_name = os.path.splitext(filename)[0]
            label_path = os.path.join(label_dir, f"{base_name}.txt")
            
            if not os.path.exists(label_path):
                images_without_labels.append(filename)
    
    return images_without_labels


def save_results(images_without_labels, output_file=None):
    """
    保存结果
    
    Args:
        images_without_labels: 无标签图像列表
        output_file: 输出文件路径
    """
    if not output_file:
        output_file = 'images_without_labels.txt'
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for img in images_without_labels:
            f.write(f"{img}\n")
    
    print(f"找到 {len(images_without_labels)} 个无标签图像")
    print(f"结果已保存到: {output_file}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='查找无标签图像')
    parser.add_argument('--image_dir', type=str, required=True, help='图像文件目录')
    parser.add_argument('--label_dir', type=str, required=True, help='标签文件目录')
    parser.add_argument('--output_file', type=str, default=None, help='输出文件路径')
    
    args = parser.parse_args()
    images = find_images_without_labels(args.image_dir, args.label_dir)
    save_results(images, args.output_file)