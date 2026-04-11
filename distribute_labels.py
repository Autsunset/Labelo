#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分配标签工具
"""

import os
import shutil
import random


def distribute_files(num_people, input_dir=None, output_dir=None):
    """
    将标签文件分配给多个人标注
    
    Args:
        num_people: 人数
        input_dir: 输入目录（可选，如果未提供则交互式输入）
        output_dir: 输出目录（可选，如果未提供则交互式输入）
    """
    if input_dir is None:
        input_dir = input("请输入标签文件夹路径: ")
    
    if output_dir is None:
        output_dir = input("请输入输出文件夹路径: ")
    
    os.makedirs(output_dir, exist_ok=True)
    
    files = [f for f in os.listdir(input_dir) if f.endswith('.txt')]
    random.shuffle(files)
    
    files_per_person = len(files) // num_people
    remainder = len(files) % num_people
    
    start = 0
    for i in range(num_people):
        end = start + files_per_person + (1 if i < remainder else 0)
        person_files = files[start:end]
        
        person_dir = os.path.join(output_dir, f'person_{i+1}')
        os.makedirs(person_dir, exist_ok=True)
        
        for f in person_files:
            src = os.path.join(input_dir, f)
            dst = os.path.join(person_dir, f)
            shutil.copy(src, dst)
        
        start = end
        print(f"分配给 person_{i+1}: {len(person_files)} 个文件")
    
    print(f"\n分配完成！共 {len(files)} 个文件分配给 {num_people} 人")


def main():
    """主函数（兼容原始调用方式）"""
    num_people = int(input("请输入人数: "))
    distribute_files(num_people)


if __name__ == "__main__":
    main()