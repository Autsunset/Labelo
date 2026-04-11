#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
删除无标签图像工具
"""

import os


def delete_images_without_labels(image_dir=None, label_dir=None):
    """
    删除没有对应标签文件的图像
    
    Args:
        image_dir: 图像文件目录（可选）
        label_dir: 标签文件目录（可选）
    
    Returns:
        int: 删除的图像数量
    """
    if image_dir is None:
        image_dir = input("请输入图像文件夹路径: ")
    
    if label_dir is None:
        label_dir = input("请输入标签文件夹路径: ")
    
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp'}
    deleted_count = 0
    
    for filename in os.listdir(image_dir):
        file_ext = os.path.splitext(filename)[1].lower()
        if file_ext in image_extensions:
            base_name = os.path.splitext(filename)[0]
            label_path = os.path.join(label_dir, f"{base_name}.txt")
            
            if not os.path.exists(label_path):
                img_path = os.path.join(image_dir, filename)
                os.remove(img_path)
                deleted_count += 1
                print(f"删除: {filename}")
    
    print(f"\n删除完成！共删除 {deleted_count} 个无标签图像")
    return deleted_count


def main():
    """主函数（兼容原始调用方式）"""
    delete_images_without_labels()


if __name__ == "__main__":
    main()