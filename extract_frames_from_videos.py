#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从视频提取帧工具
"""

import os
import cv2


def extract_frames_from_videos(input_dir=None, output_dir=None, frame_interval=None):
    """
    从视频文件中提取帧（核心函数）
    
    Args:
        input_dir: 视频文件目录（可选）
        output_dir: 输出目录（可选）
        frame_interval: 帧间隔（秒）（可选）
    """
    if input_dir is None:
        input_dir = input("请输入视频文件夹路径: ")
    
    if output_dir is None:
        output_dir = input("请输入输出文件夹路径: ")
    
    if frame_interval is None:
        try:
            frame_interval = int(input("请输入帧间隔（秒）: "))
        except:
            frame_interval = 1
    
    os.makedirs(output_dir, exist_ok=True)
    
    video_extensions = {'.mp4', '.avi', '.mov', '.mkv'}
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
            interval_frames = int(fps * frame_interval)
            frame_count = 0
            saved_count = 0
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                if frame_count % interval_frames == 0:
                    frame_path = os.path.join(output_dir, f"{video_name}_{saved_count:06d}.jpg")
                    cv2.imwrite(frame_path, frame)
                    saved_count += 1
                
                frame_count += 1
            
            cap.release()
            total_frames += saved_count
            print(f"处理完成: {filename}, 提取 {saved_count} 帧")
    
    print(f"\n提取完成！共提取 {total_frames} 帧")


def main():
    """主函数（兼容原始调用方式）"""
    extract_frames_from_videos()


if __name__ == "__main__":
    main()