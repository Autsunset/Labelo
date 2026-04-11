#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
移动图像到文件夹工具
"""

import os
import shutil


def move_images_to_folder(image_dir=None, target_folder=None):
    """
    将图像移动到指定文件夹（核心函数）
    
    Args:
        image_dir: 源图像目录（可选）
        target_folder: 目标文件夹（可选）
    """
    if image_dir is None:
        image_dir = input("请输入图像文件夹路径: ")
    
    if target_folder is None:
        target_folder = input("请输入目标文件夹路径: ")
    
    os.makedirs(target_folder, exist_ok=True)
    
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif'}
    moved_count = 0
    
    for filename in os.listdir(image_dir):
        file_ext = os.path.splitext(filename)[1].lower()
        if file_ext in image_extensions:
            src_path = os.path.join(image_dir, filename)
            dst_path = os.path.join(target_folder, filename)
            
            if os.path.exists(dst_path):
                os.remove(dst_path)
            
            shutil.move(src_path, target_folder)
            moved_count += 1
    
    print(f"移动完成！共移动 {moved_count} 个图像文件")


def main():
    """主函数（兼容原始调用方式）"""
    move_images_to_folder()


if __name__ == "__main__":
    main()