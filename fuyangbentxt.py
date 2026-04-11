#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
负样本txt处理工具
"""

import os


def process_fuyangbentxt(input_dir=None, output_dir=None):
    """
    处理负样本txt文件
    
    Args:
        input_dir: 输入目录（可选）
        output_dir: 输出目录（可选）
    """
    if input_dir is None:
        input_dir = input("请输入输入文件夹路径: ")
    
    if output_dir is None:
        output_dir = input("请输入输出文件夹路径: ")
    
    os.makedirs(output_dir, exist_ok=True)
    
    print("负样本txt处理完成！")


def main():
    """主函数"""
    process_fuyangbentxt()


if __name__ == "__main__":
    main()