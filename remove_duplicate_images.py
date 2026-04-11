#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
移除重复图像工具
"""

import os
import hashlib


def get_image_hash(filepath):
    """计算图像文件的哈希值"""
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def remove_duplicates(image_dir):
    """
    移除重复图像（核心函数）
    
    Args:
        image_dir: 图像文件目录
    
    Returns:
        int: 删除的重复图像数量
    """
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp'}
    hashes = {}
    duplicate_count = 0
    
    for filename in os.listdir(image_dir):
        file_ext = os.path.splitext(filename)[1].lower()
        if file_ext in image_extensions:
            filepath = os.path.join(image_dir, filename)
            file_hash = get_image_hash(filepath)
            
            if file_hash in hashes:
                os.remove(filepath)
                duplicate_count += 1
                print(f"删除重复: {filename}")
            else:
                hashes[file_hash] = filename
    
    print(f"\n去重完成！共删除 {duplicate_count} 个重复图像")
    return duplicate_count


def main(image_dir=None):
    """
    主函数：移除重复图像
    
    Args:
        image_dir: 图像文件目录（可选，如果未提供则交互式输入）
    """
    if image_dir is None:
        image_dir = input("请输入图像文件夹路径: ")
    
    if not os.path.exists(image_dir):
        print(f"错误：目录不存在: {image_dir}")
        return
    
    remove_duplicates(image_dir)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='移除重复图像')
    parser.add_argument('--image_dir', type=str, default=None, help='图像文件目录')
    
    args = parser.parse_args()
    main(args.image_dir)