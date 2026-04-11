#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查正方形标签工具
"""

import os


def check_square_labels(labels_dir, aspect_ratio_threshold=1.5, image_dir=None):
    """
    检查边界框是否近似正方形
    
    Args:
        labels_dir: 标签文件所在目录
        aspect_ratio_threshold: 宽高比阈值
        image_dir: 图像文件所在目录（可选）
    
    Returns:
        list: 问题标签文件列表
    """
    problematic_labels = []
    
    for filename in os.listdir(labels_dir):
        if filename.endswith('.txt'):
            filepath = os.path.join(labels_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        parts = line.split()
                        if len(parts) >= 5:
                            width = float(parts[3])
                            height = float(parts[4])
                            
                            if width > 0 and height > 0:
                                aspect_ratio = max(width, height) / min(width, height)
                                if aspect_ratio > aspect_ratio_threshold:
                                    problematic_labels.append(filename)
                                    break
    
    return problematic_labels


def save_results(problematic_labels, output_file):
    """
    保存检查结果
    
    Args:
        problematic_labels: 问题标签列表
        output_file: 输出文件路径
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        for label in problematic_labels:
            f.write(f"{label}\n")
    
    print(f"检查完成！发现 {len(problematic_labels)} 个非正方形标签")
    print(f"结果已保存到: {output_file}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='检查非正方形标签')
    parser.add_argument('--labels_dir', type=str, required=True, help='标签文件目录')
    parser.add_argument('--threshold', type=float, default=1.5, help='宽高比阈值')
    parser.add_argument('--image_dir', type=str, default=None, help='图像文件目录')
    
    args = parser.parse_args()
    problematic = check_square_labels(args.labels_dir, args.threshold, args.image_dir)
    output_file = os.path.join(os.path.dirname(args.labels_dir), 'problematic_square_labels.txt')
    save_results(problematic, output_file)