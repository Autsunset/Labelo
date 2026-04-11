#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
按时间戳采样图像工具
"""

import os
import shutil


def sample_images_by_timestamp(image_dir=None, output_dir=None, sample_count=None):
    """
    根据时间戳采样图像
    
    Args:
        image_dir: 图像文件目录（可选）
        output_dir: 输出目录（可选）
        sample_count: 采样数量（可选）
    """
    if image_dir is None:
        image_dir = input("请输入图像文件夹路径: ")
    
    if output_dir is None:
        output_dir = input("请输入输出文件夹路径: ")
    
    if sample_count is None:
        try:
            sample_count = int(input("请输入采样数量: "))
        except:
            sample_count = 100
    
    os.makedirs(output_dir, exist_ok=True)
    
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp'}
    images = []
    
    for filename in os.listdir(image_dir):
        file_ext = os.path.splitext(filename)[1].lower()
        if file_ext in image_extensions:
            filepath = os.path.join(image_dir, filename)
            mtime = os.path.getmtime(filepath)
            images.append((mtime, filename))
    
    images.sort(key=lambda x: x[0])
    
    if len(images) <= sample_count:
        step = 1
    else:
        step = len(images) // sample_count
    
    sampled = images[::step][:sample_count]
    
    for _, filename in sampled:
        src = os.path.join(image_dir, filename)
        dst = os.path.join(output_dir, filename)
        shutil.copy(src, dst)
    
    print(f"采样完成！共采样 {len(sampled)} 个图像")


def main():
    """主函数（兼容原始调用方式）"""
    sample_images_by_timestamp()


if __name__ == "__main__":
    main()