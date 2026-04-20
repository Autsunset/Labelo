#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查标签数量工具
"""

import os


def check_label_counts(label_dir, threshold=1):
    """
    检查标签文件中的标签数量
    
    Args:
        label_dir: 标签文件所在目录
        threshold: 阈值，列出标签数量大于此值的文件，默认值为1
    
    Returns:
        dict: 统计信息
    """
    stats = {
        'total_files': 0,
        'files_with_no_labels': 0,
        'files_with_one_label': 0,
        'files_with_multiple_labels': [],
        'max_labels': 0,
        'avg_labels': 0,
        'threshold': threshold
    }
    
    total_labels = 0
    
    for filename in os.listdir(label_dir):
        if filename.endswith('.txt'):
            stats['total_files'] += 1
            filepath = os.path.join(label_dir, filename)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = [line.strip() for line in f if line.strip()]
                label_count = len(lines)
            
            total_labels += label_count
            
            if label_count == 0:
                stats['files_with_no_labels'] += 1
            elif label_count <= threshold:
                stats['files_with_one_label'] += 1
            else:
                stats['files_with_multiple_labels'].append(filename)
            
            if label_count > stats['max_labels']:
                stats['max_labels'] = label_count
    
    if stats['total_files'] > 0:
        stats['avg_labels'] = total_labels / stats['total_files']
    
    print(f"标签数量统计 (阈值: {threshold}):")
    print(f"总文件数: {stats['total_files']}")
    print(f"无标签文件数: {stats['files_with_no_labels']}")
    print(f"标签数<=阈值文件数: {stats['files_with_one_label']}")
    print(f"标签数>阈值文件数: {len(stats['files_with_multiple_labels'])}")
    print(f"最大标签数: {stats['max_labels']}")
    print(f"平均标签数: {stats['avg_labels']:.2f}")
    
    return stats


def analyze_label_content(label_dir, threshold=1):
    """
    分析多标签文件内容
    
    Args:
        label_dir: 标签文件所在目录
        threshold: 阈值，列出标签数量大于此值的文件，默认值为1
    """
    print(f"\n标签数>{threshold}的文件详情:")
    for filename in os.listdir(label_dir):
        if filename.endswith('.txt'):
            filepath = os.path.join(label_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = [line.strip() for line in f if line.strip()]
                if len(lines) > threshold:
                    print(f"{filename}: {len(lines)} 个标签")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='检查标签数量')
    parser.add_argument('--label_dir', type=str, required=True, help='标签文件目录')
    parser.add_argument('--threshold', type=int, default=1, help='阈值，列出标签数量大于此值的文件，默认值为1')
    
    args = parser.parse_args()
    stats = check_label_counts(args.label_dir, args.threshold)
    if stats['files_with_multiple_labels']:
        analyze_label_content(args.label_dir, args.threshold)