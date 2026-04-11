#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LabelMe JSON 转 YOLO TXT 格式转换工具
"""

import json
import os
import glob
from pathlib import Path


def load_classes(classes_file):
    """加载类别映射文件"""
    if not os.path.exists(classes_file):
        print(f"警告：类别文件 {classes_file} 不存在，将自动生成类别映射")
        return {}
    
    class_map = {}
    with open(classes_file, 'r', encoding='utf-8') as f:
        for idx, line in enumerate(f):
            class_name = line.strip()
            if class_name:
                class_map[class_name] = idx
    return class_map


def create_class_map_from_json(json_files):
    """从JSON文件中自动提取所有类别并创建映射"""
    classes = set()
    
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for shape in data.get('shapes', []):
                    classes.add(shape.get('label', ''))
        except Exception as e:
            print(f"读取文件 {json_file} 时出错：{e}")
            continue
    
    sorted_classes = sorted(list(classes))
    class_map = {cls: idx for idx, cls in enumerate(sorted_classes)}
    
    return class_map


def convert_rectangle_to_yolo(points, img_width, img_height):
    """将LabelMe矩形坐标转换为YOLO格式"""
    x1, y1 = points[0]
    x2, y2 = points[1]
    
    box_width = abs(x2 - x1)
    box_height = abs(y2 - y1)
    
    center_x = (x1 + x2) / 2.0
    center_y = (y1 + y2) / 2.0
    
    center_x_rel = center_x / img_width
    center_y_rel = center_y / img_height
    width_rel = box_width / img_width
    height_rel = box_height / img_height
    
    return center_x_rel, center_y_rel, width_rel, height_rel


def convert_json_to_txt(json_file, output_dir, class_map):
    """将单个JSON文件转换为TXT文件"""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        img_width = data.get('imageWidth', 0)
        img_height = data.get('imageHeight', 0)
        
        if img_width == 0 or img_height == 0:
            print(f"警告：文件 {json_file} 缺少图像尺寸信息")
            return False
        
        json_name = Path(json_file).stem
        txt_file = os.path.join(output_dir, f"{json_name}.txt")
        
        yolo_lines = []
        for shape in data.get('shapes', []):
            label = shape.get('label', '')
            shape_type = shape.get('shape_type', '')
            points = shape.get('points', [])
            
            if not label or shape_type != 'rectangle' or len(points) != 2:
                print(f"跳过无效标注：{label}, {shape_type}")
                continue
            
            if label not in class_map:
                print(f"警告：类别 '{label}' 不在类别映射中，跳过")
                continue
            
            class_id = class_map[label]
            center_x, center_y, width, height = convert_rectangle_to_yolo(points, img_width, img_height)
            
            yolo_line = f"{class_id} {center_x:.6f} {center_y:.6f} {width:.6f} {height:.6f}"
            yolo_lines.append(yolo_line)
        
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(yolo_lines))
        
        print(f"转换完成：{json_file} -> {txt_file}")
        return True
        
    except Exception as e:
        print(f"转换文件 {json_file} 时出错：{e}")
        return False


def batch_convert(json_dir, output_dir):
    """批量转换LabelMe JSON文件为YOLO TXT格式"""
    os.makedirs(output_dir, exist_ok=True)
    
    json_pattern = os.path.join(json_dir, "*.json")
    json_files = glob.glob(json_pattern)
    
    if not json_files:
        print(f"在目录 {json_dir} 中未找到JSON文件")
        return
    
    print(f"找到 {len(json_files)} 个JSON文件")
    
    classes_file = os.path.join(output_dir, "classes.txt")
    class_map = load_classes(classes_file)
    
    if not class_map:
        print("从JSON文件中自动提取类别...")
        class_map = create_class_map_from_json(json_files)
        
        with open(classes_file, 'w', encoding='utf-8') as f:
            for class_name in sorted(class_map.keys()):
                f.write(f"{class_name}\n")
        print(f"已生成类别文件：{classes_file}")
    
    print(f"类别映射：{class_map}")
    
    success_count = 0
    for json_file in json_files:
        if convert_json_to_txt(json_file, output_dir, class_map):
            success_count += 1
    
    print(f"\n转换完成！成功：{success_count}/{len(json_files)}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='LabelMe JSON转YOLO TXT')
    parser.add_argument('--input_dir', type=str, required=True, help='JSON文件所在目录')
    parser.add_argument('--output_dir', type=str, required=True, help='输出目录')
    
    args = parser.parse_args()
    batch_convert(args.input_dir, args.output_dir)