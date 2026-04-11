#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查标签类别工具
"""

import os


def check_label_classes(label_dir):
    """
    检查标签文件中的类别分布
    
    Args:
        label_dir: 标签文件所在目录
    """
    classes = {}
    
    for filename in os.listdir(label_dir):
        if filename.endswith('.txt'):
            filepath = os.path.join(label_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        class_id = int(line.split()[0])
                        if class_id not in classes:
                            classes[class_id] = 0
                        classes[class_id] += 1
    
    print("标签类别分布:")
    for class_id in sorted(classes.keys()):
        print(f"类别 {class_id}: {classes[class_id]} 个标签")
    
    print(f"\n总类别数: {len(classes)}")
    print(f"总标签数: {sum(classes.values())}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='检查标签类别分布')
    parser.add_argument('--label_dir', type=str, required=True, help='标签文件目录')
    
    args = parser.parse_args()
    check_label_classes(args.label_dir)