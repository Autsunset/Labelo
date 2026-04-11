#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据增强工具
"""

import os
import cv2
import numpy as np


def augment_data(image_dir=None, label_dir=None):
    """
    执行数据增强（核心函数）
    
    Args:
        image_dir: 图像文件目录（可选）
        label_dir: 标签文件目录（可选）
    """
    if image_dir is None:
        image_dir = input("请输入图像文件夹路径: ")
    
    if label_dir is None:
        label_dir = input("请输入标签文件夹路径: ")
    
    image_extensions = {'.jpg', '.jpeg', '.png'}
    augmented_count = 0
    
    for filename in os.listdir(image_dir):
        file_ext = os.path.splitext(filename)[1].lower()
        if file_ext in image_extensions:
            base_name = os.path.splitext(filename)[0]
            img_path = os.path.join(image_dir, filename)
            label_path = os.path.join(label_dir, f"{base_name}.txt")
            
            if not os.path.exists(label_path):
                continue
            
            image = cv2.imread(img_path)
            with open(label_path, 'r', encoding='utf-8') as f:
                labels = [line.strip() for line in f if line.strip()]
            
            # 水平翻转
            flipped_img = cv2.flip(image, 1)
            height, width = image.shape[:2]
            flipped_labels = []
            
            for line in labels:
                parts = line.split()
                if len(parts) >= 5:
                    class_id = parts[0]
                    center_x = float(parts[1])
                    center_y = float(parts[2])
                    w = float(parts[3])
                    h = float(parts[4])
                    
                    center_x = 1 - center_x
                    flipped_labels.append(f"{class_id} {center_x:.6f} {center_y:.6f} {w:.6f} {h:.6f}")
            
            cv2.imwrite(os.path.join(image_dir, f"{base_name}_flip.jpg"), flipped_img)
            with open(os.path.join(label_dir, f"{base_name}_flip.txt"), 'w', encoding='utf-8') as f:
                f.write('\n'.join(flipped_labels))
            augmented_count += 1
    
    print(f"数据增强完成！共生成 {augmented_count} 个增强样本")


def main():
    """主函数（兼容原始调用方式）"""
    augment_data()


if __name__ == "__main__":
    main()