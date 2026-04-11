#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视频转图像工具
"""

import os
import cv2


def batch_process(input_dir=None, output_base=None, interval=None):
    """
    批量处理视频文件，提取帧
    
    Args:
        input_dir: 视频文件所在目录（可选）
        output_base: 输出基础目录（可选）
        interval: 帧间隔（秒）（可选）
    """
    if input_dir is None:
        input_dir = input("请输入视频文件夹路径: ")
    
    if output_base is None:
        output_base = input("请输入输出基础目录: ")
    
    if interval is None:
        try:
            interval = float(input("请输入帧间隔（秒）: "))
        except:
            interval = 1.0
    
    os.makedirs(output_base, exist_ok=True)
    
    video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.flv'}
    total_frames = 0
    
    for filename in os.listdir(input_dir):
        file_ext = os.path.splitext(filename)[1].lower()
        if file_ext in video_extensions:
            video_path = os.path.join(input_dir, filename)
            video_name = os.path.splitext(filename)[0]
            
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                print(f"无法打开视频: {filename}")
                continue
            
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_interval = int(fps * interval)
            frame_count = 0
            saved_count = 0
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                if frame_count % frame_interval == 0:
                    output_folder = os.path.join(output_base, video_name)
                    os.makedirs(output_folder, exist_ok=True)
                    output_path = os.path.join(output_folder, f"{video_name}_{saved_count:06d}.jpg")
                    cv2.imwrite(output_path, frame)
                    saved_count += 1
                
                frame_count += 1
            
            cap.release()
            total_frames += saved_count
            print(f"处理完成: {filename}, 提取 {saved_count} 帧")
    
    print(f"批量处理完成！共提取 {total_frames} 帧")


def main():
    """主函数（兼容原始调用方式）"""
    batch_process()


if __name__ == "__main__":
    main()