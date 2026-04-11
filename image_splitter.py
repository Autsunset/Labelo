#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片分割工具
"""

import os
import cv2


def split_images(input_folder=None, output_folder=None):
    """
    分割图片为多个部分
    
    Args:
        input_folder: 输入文件夹（可选）
        output_folder: 输出文件夹（可选）
    """
    if input_folder is None:
        input_folder = input("请输入图片文件夹路径: ")
    
    if output_folder is None:
        output_folder = input("请输入输出文件夹路径: ")
    
    os.makedirs(output_folder, exist_ok=True)
    
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp'}
    count = 0
    
    for filename in os.listdir(input_folder):
        file_ext = os.path.splitext(filename)[1].lower()
        if file_ext in image_extensions:
            input_path = os.path.join(input_folder, filename)
            img = cv2.imread(input_path)
            
            if img is None:
                print(f"无法读取图像: {filename}")
                continue
            
            height, width = img.shape[:2]
            
            # 分割为4部分（2x2）
            h_mid = height // 2
            w_mid = width // 2
            
            parts = [
                img[:h_mid, :w_mid],
                img[:h_mid, w_mid:],
                img[h_mid:, :w_mid],
                img[h_mid:, w_mid:]
            ]
            
            base_name = os.path.splitext(filename)[0]
            for i, part in enumerate(parts):
                output_path = os.path.join(output_folder, f"{base_name}_{i+1}.jpg")
                cv2.imwrite(output_path, part)
            count += 1
    
    print(f"分割完成！共处理 {count} 张图片，生成 {count * 4} 张小图")


def main():
    """主函数（兼容原始调用方式）"""
    split_images()


if __name__ == "__main__":
    main()