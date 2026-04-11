#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查标签和类别数量工具
"""

import os


def check_label_counts_and_classes(label_dir, output_file=None):
    """
    检查标签和类别数量
    
    Args:
        label_dir: 标签文件所在目录
        output_file: 输出文件路径
    
    Returns:
        dict: 统计信息
    """
    stats = {
        'total_files': 0,
        'total_labels': 0,
        'classes': {}
    }
    
    for filename in os.listdir(label_dir):
        if filename.endswith('.txt'):
            stats['total_files'] += 1
            filepath = os.path.join(label_dir, filename)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        stats['total_labels'] += 1
                        class_id = int(line.split()[0])
                        if class_id not in stats['classes']:
                            stats['classes'][class_id] = 0
                        stats['classes'][class_id] += 1
    
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("标签统计报告\n")
            f.write("=" * 30 + "\n")
            f.write(f"标签文件总数: {stats['total_files']}\n")
            f.write(f"标签总数: {stats['total_labels']}\n")
            f.write(f"类别总数: {len(stats['classes'])}\n")
            f.write("\n类别分布:\n")
            for class_id in sorted(stats['classes'].keys()):
                f.write(f"  类别 {class_id}: {stats['classes'][class_id]} 个标签\n")
    
    return stats


def print_summary(stats):
    """
    打印统计摘要
    """
    print("标签和类别统计:")
    print(f"标签文件总数: {stats['total_files']}")
    print(f"标签总数: {stats['total_labels']}")
    print(f"类别总数: {len(stats['classes'])}")
    print("\n类别分布:")
    for class_id in sorted(stats['classes'].keys()):
        print(f"  类别 {class_id}: {stats['classes'][class_id]} 个标签")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='检查标签和类别数量')
    parser.add_argument('--label_dir', type=str, required=True, help='标签文件目录')
    parser.add_argument('--output_file', type=str, default=None, help='输出文件路径')
    
    args = parser.parse_args()
    stats = check_label_counts_and_classes(args.label_dir, args.output_file)
    print_summary(stats)