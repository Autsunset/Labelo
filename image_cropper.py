#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片裁剪工具 - 裁剪图片下半部分
"""

import os
import cv2


def crop_images_bottom_half(input_folder, output_folder):
    """
    裁剪图片的下半部分
    
    Args:
        input_folder: 输入文件夹
        output_folder: 输出文件夹
    """
    os.makedirs(output_folder, exist_ok=True)
    
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp'}
    count = 0
    
    for filename in os.listdir(input_folder):
        file_ext = os.path.splitext(filename)[1].lower()
        if file_ext in image_extensions:
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            
            img = cv2.imread(input_path)
            if img is None:
                print(f"无法读取图像: {filename}")
                continue
            
            height, width = img.shape[:2]
            cropped_img = img[:height//2, :]
            
            cv2.imwrite(output_path, cropped_img)
            count += 1
    
    print(f"裁剪完成！共处理 {count} 张图片")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='裁剪图片下半部分')
    parser.add_argument('--input_folder', type=str, required=True, help='输入文件夹')
    parser.add_argument('--output_folder', type=str, required=True, help='输出文件夹')
    
    args = parser.parse_args()
    crop_images_bottom_half(args.input_folder, args.output_folder)