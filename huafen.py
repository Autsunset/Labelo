#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
划分数据集工具
"""

import os
import shutil
import random


def split_dataset(input_dir, output_dir):
    """
    划分数据集为训练集、验证集和测试集
    
    Args:
        input_dir: 输入目录
        output_dir: 输出目录
    """
    os.makedirs(output_dir, exist_ok=True)
    
    train_dir = os.path.join(output_dir, 'train')
    val_dir = os.path.join(output_dir, 'val')
    test_dir = os.path.join(output_dir, 'test')
    
    os.makedirs(os.path.join(train_dir, 'images'), exist_ok=True)
    os.makedirs(os.path.join(train_dir, 'labels'), exist_ok=True)
    os.makedirs(os.path.join(val_dir, 'images'), exist_ok=True)
    os.makedirs(os.path.join(val_dir, 'labels'), exist_ok=True)
    os.makedirs(os.path.join(test_dir, 'images'), exist_ok=True)
    os.makedirs(os.path.join(test_dir, 'labels'), exist_ok=True)
    
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp'}
    images = []
    
    for filename in os.listdir(input_dir):
        file_ext = os.path.splitext(filename)[1].lower()
        if file_ext in image_extensions:
            images.append(filename)
    
    random.shuffle(images)
    
    total = len(images)
    train_count = int(total * 0.7)
    val_count = int(total * 0.2)
    
    train_images = images[:train_count]
    val_images = images[train_count:train_count + val_count]
    test_images = images[train_count + val_count:]
    
    for img in train_images:
        base_name = os.path.splitext(img)[0]
        shutil.copy(os.path.join(input_dir, img), os.path.join(train_dir, 'images', img))
        label_file = f"{base_name}.txt"
        if os.path.exists(os.path.join(input_dir, label_file)):
            shutil.copy(os.path.join(input_dir, label_file), os.path.join(train_dir, 'labels', label_file))
    
    for img in val_images:
        base_name = os.path.splitext(img)[0]
        shutil.copy(os.path.join(input_dir, img), os.path.join(val_dir, 'images', img))
        label_file = f"{base_name}.txt"
        if os.path.exists(os.path.join(input_dir, label_file)):
            shutil.copy(os.path.join(input_dir, label_file), os.path.join(val_dir, 'labels', label_file))
    
    for img in test_images:
        base_name = os.path.splitext(img)[0]
        shutil.copy(os.path.join(input_dir, img), os.path.join(test_dir, 'images', img))
        label_file = f"{base_name}.txt"
        if os.path.exists(os.path.join(input_dir, label_file)):
            shutil.copy(os.path.join(input_dir, label_file), os.path.join(test_dir, 'labels', label_file))
    
    print(f"数据集划分完成！训练集: {len(train_images)}, 验证集: {len(val_images)}, 测试集: {len(test_images)}")


def main(input_dir=None, output_dir=None):
    """主函数"""
    if input_dir is None:
        input_dir = input("请输入输入文件夹路径: ")
    
    if output_dir is None:
        output_dir = input("请输入输出文件夹路径: ")
    
    split_dataset(input_dir, output_dir)


if __name__ == "__main__":
    main()