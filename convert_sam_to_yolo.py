#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将xanylableing的sam标签转换为YOLO格式的矩形框标签
"""

import os
import json
from pathlib import Path
from PIL import Image


def convert_sam_to_yolo(input_dir, output_dir):
    """
    将xanylableing的sam标签转换为YOLO格式的矩形框标签
    
    Args:
        input_dir: 包含图像和sam标签的目录
        output_dir: 输出YOLO标签的目录
    """
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 遍历输入目录中的所有文件
    for file in os.listdir(input_dir):
        if file.endswith('.jpg') or file.endswith('.jpeg') or file.endswith('.png'):
            # 获取图像路径
            image_path = os.path.join(input_dir, file)
            
            # 获取对应的sam标签文件路径
            base_name = os.path.splitext(file)[0]
            sam_label_path = os.path.join(input_dir, f"{base_name}.json")
            
            if not os.path.exists(sam_label_path):
                print(f"警告：{file} 没有对应的sam标签文件")
                continue
            
            try:
                # 读取图像尺寸
                with Image.open(image_path) as img:
                    img_width, img_height = img.size
                
                # 读取sam标签
                with open(sam_label_path, 'r', encoding='utf-8') as f:
                    sam_data = json.load(f)
                
                # 处理标签数据
                yolo_labels = []
                
                # 检查sam标签的结构
                if 'annotations' in sam_data:
                    # 处理annotations格式
                    for annotation in sam_data['annotations']:
                        if 'segmentation' in annotation:
                            # 提取边界框
                            segmentation = annotation['segmentation']
                            if isinstance(segmentation, list):
                                # 处理多边形点
                                x_coords = []
                                y_coords = []
                                
                                # 扁平化多边形点列表
                                if isinstance(segmentation[0], list):
                                    # 处理多个多边形
                                    for poly in segmentation:
                                        for i in range(0, len(poly), 2):
                                            x_coords.append(poly[i])
                                            y_coords.append(poly[i+1])
                                else:
                                    # 处理单个多边形
                                    for i in range(0, len(segmentation), 2):
                                        x_coords.append(segmentation[i])
                                        y_coords.append(segmentation[i+1])
                                
                                # 计算边界框
                                if x_coords and y_coords:
                                    x_min = min(x_coords)
                                    y_min = min(y_coords)
                                    x_max = max(x_coords)
                                    y_max = max(y_coords)
                                    
                                    # 转换为YOLO格式
                                    x_center = (x_min + x_max) / 2 / img_width
                                    y_center = (y_min + y_max) / 2 / img_height
                                    width = (x_max - x_min) / img_width
                                    height = (y_max - y_min) / img_height
                                    
                                    # 假设类别为0（可根据实际情况调整）
                                    class_id = 0
                                    yolo_labels.append(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")
                elif 'shapes' in sam_data:
                    # 处理shapes格式（类似LabelMe）
                    for shape in sam_data['shapes']:
                        if shape['shape_type'] == 'polygon':
                            # 提取边界框
                            points = shape['points']
                            x_coords = [p[0] for p in points]
                            y_coords = [p[1] for p in points]
                            
                            # 计算边界框
                            x_min = min(x_coords)
                            y_min = min(y_coords)
                            x_max = max(x_coords)
                            y_max = max(y_coords)
                            
                            # 转换为YOLO格式
                            x_center = (x_min + x_max) / 2 / img_width
                            y_center = (y_min + y_max) / 2 / img_height
                            width = (x_max - x_min) / img_width
                            height = (y_max - y_min) / img_height
                            
                            # 假设类别为0（可根据实际情况调整）
                            class_id = 0
                            yolo_labels.append(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")
                
                # 保存YOLO标签文件
                if yolo_labels:
                    yolo_label_path = os.path.join(output_dir, f"{base_name}.txt")
                    with open(yolo_label_path, 'w', encoding='utf-8') as f:
                        f.write('\n'.join(yolo_labels))
                    print(f"已转换: {file} -> {os.path.basename(yolo_label_path)}")
                else:
                    print(f"警告：{file} 没有有效的标签数据")
                
            except Exception as e:
                print(f"错误处理 {file}: {str(e)}")


def main():
    """主函数"""
    print("=" * 60)
    print("SAM标签转YOLO格式工具")
    print("=" * 60)
    
    # 参考标签目录
    input_dir = "D:\\Pythoncode\\yolov5-7.0\\data\\xinxianghuaxian_carton\\ACT\\images"
    output_dir = "D:\\Pythoncode\\yolov5-7.0\\data\\xinxianghuaxian_carton\\ACT\\labels"
    
    print(f"输入目录: {input_dir}")
    print(f"输出目录: {output_dir}")
    
    # 验证输入目录
    if not os.path.isdir(input_dir):
        print(f"错误：输入目录不存在：{input_dir}")
        return
    
    # 执行转换
    convert_sam_to_yolo(input_dir, output_dir)
    print("\n转换完成！")


if __name__ == "__main__":
    main()
