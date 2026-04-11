#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VOC格式转YOLO格式工具
"""

import os
import xml.etree.ElementTree as ET


def convert_voc_to_yolo(voc_dir=None, yolo_dir=None):
    """
    将VOC格式的XML标签转换为YOLO格式的TXT标签
    
    Args:
        voc_dir: VOC格式标签所在目录（可选）
        yolo_dir: YOLO格式标签输出目录（可选）
    """
    if voc_dir is None:
        voc_dir = input("请输入VOC标签文件夹路径: ")
    
    if yolo_dir is None:
        yolo_dir = input("请输入YOLO输出文件夹路径: ")
    
    os.makedirs(yolo_dir, exist_ok=True)
    
    class_names = []
    
    for filename in os.listdir(voc_dir):
        if filename.endswith('.xml'):
            xml_path = os.path.join(voc_dir, filename)
            txt_path = os.path.join(yolo_dir, filename.replace('.xml', '.txt'))
            
            tree = ET.parse(xml_path)
            root = tree.getroot()
            
            size = root.find('size')
            img_width = int(size.find('width').text)
            img_height = int(size.find('height').text)
            
            yolo_lines = []
            
            for obj in root.findall('object'):
                class_name = obj.find('name').text
                
                if class_name not in class_names:
                    class_names.append(class_name)
                
                class_id = class_names.index(class_name)
                
                bndbox = obj.find('bndbox')
                xmin = int(bndbox.find('xmin').text)
                ymin = int(bndbox.find('ymin').text)
                xmax = int(bndbox.find('xmax').text)
                ymax = int(bndbox.find('ymax').text)
                
                # 转换为YOLO格式
                center_x = (xmin + xmax) / 2.0 / img_width
                center_y = (ymin + ymax) / 2.0 / img_height
                width = (xmax - xmin) / img_width
                height = (ymax - ymin) / img_height
                
                yolo_lines.append(f"{class_id} {center_x:.6f} {center_y:.6f} {width:.6f} {height:.6f}")
            
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(yolo_lines))
    
    # 保存类别文件
    classes_file = os.path.join(yolo_dir, 'classes.txt')
    with open(classes_file, 'w', encoding='utf-8') as f:
        for class_name in class_names:
            f.write(f"{class_name}\n")
    
    print(f"转换完成！共处理 {len([f for f in os.listdir(voc_dir) if f.endswith('.xml')])} 个文件")
    print(f"类别列表已保存到: {classes_file}")


def main():
    """主函数（兼容原始调用方式）"""
    convert_voc_to_yolo()


if __name__ == "__main__":
    main()