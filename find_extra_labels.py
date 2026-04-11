#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
查找多余标签工具
"""

import os


def find_extra_labels(image_dir=None, label_dir=None):
    """
    查找没有对应图像的标签文件
    
    Args:
        image_dir: 图像文件目录（可选）
        label_dir: 标签文件目录（可选）
    
    Returns:
        list: 多余标签文件列表
    """
    if image_dir is None:
        image_dir = input("请输入图像文件夹路径: ")
    
    if label_dir is None:
        label_dir = input("请输入标签文件夹路径: ")
    
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp'}
    image_basenames = set()
    
    for filename in os.listdir(image_dir):
        file_ext = os.path.splitext(filename)[1].lower()
        if file_ext in image_extensions:
            base_name = os.path.splitext(filename)[0]
            image_basenames.add(base_name)
    
    extra_labels = []
    for filename in os.listdir(label_dir):
        if filename.endswith('.txt'):
            base_name = os.path.splitext(filename)[0]
            if base_name not in image_basenames:
                extra_labels.append(filename)
    
    return extra_labels


def save_results(extra_labels, output_file=None):
    """
    保存结果
    
    Args:
        extra_labels: 多余标签文件列表
        output_file: 输出文件路径
    """
    if not output_file:
        output_file = 'extra_labels.txt'
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for label in extra_labels:
            f.write(f"{label}\n")
    
    print(f"找到 {len(extra_labels)} 个多余标签文件")
    print(f"结果已保存到: {output_file}")


def main():
    """主函数（兼容原始调用方式）"""
    extra_labels = find_extra_labels()
    save_results(extra_labels)


if __name__ == "__main__":
    main()