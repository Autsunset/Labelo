import os
import sys
import json
from flask import Flask, render_template, request, jsonify, Response
from werkzeug.utils import secure_filename
import threading
import traceback

app = Flask(__name__)
app.config['SECRET_KEY'] = 'labelo-web-secret-key'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class ToolFunctions:
    """工具函数类，调用现有的工具模块"""
    
    @staticmethod
    def crop_images_bottom_half(input_folder, output_folder):
        from image_cropper import crop_images_bottom_half
        return crop_images_bottom_half(input_folder, output_folder)
    
    @staticmethod
    def split_images(input_folder, output_folder):
        from image_splitter import main as split_main
        return split_main(input_folder, output_folder)
    
    @staticmethod
    def check_labels(label_dir):
        from check_labels import check_label_classes
        return check_label_classes(label_dir)
    
    @staticmethod
    def check_square_labels(labels_dir, aspect_ratio_threshold, image_dir):
        from check_square_labels import check_square_labels, save_results
        problematic_labels = check_square_labels(labels_dir, aspect_ratio_threshold, image_dir)
        return problematic_labels
    
    @staticmethod
    def distribute_labels(num_people, input_dir, output_dir):
        from distribute_labels import distribute_files
        return distribute_files(num_people, input_dir, output_dir)
    
    @staticmethod
    def find_images_without_labels(image_dir, label_dir):
        from find_images_without_labels import find_images_without_labels
        return find_images_without_labels(image_dir, label_dir)
    
    @staticmethod
    def check_label_counts(label_dir):
        from check_label_counts import check_label_counts
        return check_label_counts(label_dir)
    
    @staticmethod
    def check_label_count_class(label_dir, output_file):
        from check_label_count_class import check_label_counts_and_classes
        return check_label_counts_and_classes(label_dir, output_file)
    
    @staticmethod
    def data_augmentation(image_dir, label_dir):
        from data_augmentation import main as aug_main
        return aug_main(image_dir, label_dir)
    
    @staticmethod
    def find_extra_labels(image_dir, label_dir):
        from find_extra_labels import find_extra_labels
        return find_extra_labels(image_dir, label_dir)
    
    @staticmethod
    def remove_duplicate_images(image_dir):
        from remove_duplicate_images import main as dup_main
        return dup_main(image_dir)
    
    @staticmethod
    def separate_images_by_labels(image_dir, label_dir, output_dir):
        from separate_images_by_labels import separate_images_by_labels
        return separate_images_by_labels(image_dir, label_dir, output_dir, move_files=True)
    
    @staticmethod
    def voc_to_yolo(voc_dir, yolo_dir):
        from voc_to_yolo import convert_voc_to_yolo
        return convert_voc_to_yolo(voc_dir, yolo_dir)
    
    @staticmethod
    def delete_images_without_labels(image_dir, label_dir):
        from delete_images_without_labels import delete_images_without_labels
        return delete_images_without_labels(image_dir, label_dir)
    
    @staticmethod
    def sample_images_by_timestamp(image_dir, output_dir, sample_count):
        from sample_images_by_timestamp import sample_images_by_timestamp
        return sample_images_by_timestamp(image_dir, output_dir, sample_count)
    
    @staticmethod
    def extract_frames_from_videos(input_dir, output_dir, frame_interval):
        from extract_frames_from_videos import extract_frames_from_videos
        return extract_frames_from_videos(input_dir, output_dir, frame_interval)
    
    @staticmethod
    def move_images_to_folder(image_dir, target_folder):
        from move_images_to_folder import move_images_to_folder
        return move_images_to_folder(image_dir, target_folder)
    
    @staticmethod
    def huafen(input_folder, output_folder):
        from huafen import main as huafen_main
        return huafen_main(input_folder, output_folder)
    
    @staticmethod
    def fuyangbentxt(input_folder, output_folder):
        from fuyangbentxt import main as fuyangbentxt_main
        return fuyangbentxt_main(input_folder, output_folder)
    
    @staticmethod
    def video_to_images(input_folder, output_folder):
        from video_to_images import main as video_to_images_main
        return video_to_images_main(input_folder, output_folder)
    
    @staticmethod
    def convert_labelme_to_yolo(input_folder, output_folder):
        from convert_labelme_to_yolo import main as labelme_to_yolo_main
        return labelme_to_yolo_main(input_folder, output_folder)


FUNCTIONS_CONFIG = {
    "图像处理": {
        "图片裁剪": {
            "desc": "读取文件夹中的jpg文件，裁切掉下半部分，然后输出到另一个文件夹",
            "fields": [
                {"name": "input_folder", "label": "输入文件夹", "type": "folder"},
                {"name": "output_folder", "label": "输出文件夹", "type": "folder"}
            ],
            "action": "crop_images"
        },
        "图片分割": {
            "desc": "将1536x1024的图片裁剪并分割成多个1536x150的图片",
            "fields": [
                {"name": "input_folder", "label": "输入文件夹", "type": "folder"},
                {"name": "output_folder", "label": "输出文件夹", "type": "folder"}
            ],
            "action": "split_images"
        },
        "移除重复图像": {
            "desc": "移除文件夹中的重复图像",
            "fields": [
                {"name": "input_folder", "label": "图像文件夹", "type": "folder"}
            ],
            "action": "remove_duplicate"
        },
        "按时间戳采样图像": {
            "desc": "根据时间戳采样图像",
            "fields": [
                {"name": "input_folder", "label": "输入文件夹", "type": "folder"},
                {"name": "output_folder", "label": "输出文件夹", "type": "folder"},
                {"name": "sample_count", "label": "采样数量", "type": "number", "default": 100}
            ],
            "action": "sample_images"
        }
    },
    "视频处理": {
        "从视频提取帧": {
            "desc": "从视频提取图像帧（支持多种格式和调整大小）",
            "fields": [
                {"name": "input_folder", "label": "视频文件夹", "type": "folder"},
                {"name": "output_folder", "label": "输出文件夹", "type": "folder"},
                {"name": "frame_interval", "label": "帧间隔", "type": "number", "default": 10}
            ],
            "action": "extract_frames"
        },
        "视频转图像": {
            "desc": "将视频文件转换为图像序列",
            "fields": [
                {"name": "input_folder", "label": "视频文件夹", "type": "folder"},
                {"name": "output_folder", "label": "输出文件夹", "type": "folder"}
            ],
            "action": "video_to_images"
        }
    },
    "标签处理": {
        "检查标签类别": {
            "desc": "检查标签文件中的类别分布，特别查找是否存在类别1的标签",
            "fields": [
                {"name": "label_folder", "label": "标签文件夹", "type": "folder"}
            ],
            "action": "check_labels"
        },
        "检查正方形标签": {
            "desc": "检查标签文件夹中的边界框是否近似正方形，找出可能有问题的长方形标签",
            "fields": [
                {"name": "label_folder", "label": "标签文件夹", "type": "folder"},
                {"name": "image_folder", "label": "图像文件夹", "type": "folder"},
                {"name": "threshold", "label": "长宽比阈值", "type": "number", "default": 1.2}
            ],
            "action": "check_square"
        },
        "检查标签数量": {
            "desc": "检查标签文件中的标签数量",
            "fields": [
                {"name": "label_folder", "label": "标签文件夹", "type": "folder"}
            ],
            "action": "check_counts"
        },
        "检查标签和类别": {
            "desc": "检查标签和类别数量",
            "fields": [
                {"name": "label_folder", "label": "标签文件夹", "type": "folder"},
                {"name": "output_file", "label": "输出文件", "type": "text", "default": "label_count_class_report.txt"}
            ],
            "action": "check_count_class"
        },
        "查找无标签图像": {
            "desc": "查找无对应标签的图像",
            "fields": [
                {"name": "image_folder", "label": "图像文件夹", "type": "folder"},
                {"name": "label_folder", "label": "标签文件夹", "type": "folder"}
            ],
            "action": "find_no_labels"
        },
        "查找多余标签": {
            "desc": "查找无对应图像的标签",
            "fields": [
                {"name": "image_folder", "label": "图像文件夹", "type": "folder"},
                {"name": "label_folder", "label": "标签文件夹", "type": "folder"}
            ],
            "action": "find_extra"
        },
        "删除无标签图像": {
            "desc": "删除无对应标签的图像",
            "fields": [
                {"name": "image_folder", "label": "图像文件夹", "type": "folder"},
                {"name": "label_folder", "label": "标签文件夹", "type": "folder"}
            ],
            "action": "delete_no_labels"
        },
        "VOC转YOLO": {
            "desc": "VOC格式转YOLO格式",
            "fields": [
                {"name": "voc_folder", "label": "VOC文件夹", "type": "folder"},
                {"name": "yolo_folder", "label": "YOLO输出文件夹", "type": "folder"}
            ],
            "action": "voc_to_yolo"
        },
        "Labelme转YOLO": {
            "desc": "Labelme格式转YOLO格式",
            "fields": [
                {"name": "input_folder", "label": "Labelme文件夹", "type": "folder"},
                {"name": "output_folder", "label": "YOLO输出文件夹", "type": "folder"}
            ],
            "action": "labelme_to_yolo"
        }
    },
    "数据管理": {
        "分配标签": {
            "desc": "分配文件到多个文件夹",
            "fields": [
                {"name": "num_people", "label": "分配人数", "type": "number", "default": 2},
                {"name": "input_folder", "label": "输入文件夹", "type": "folder"},
                {"name": "output_folder", "label": "输出文件夹", "type": "folder"}
            ],
            "action": "distribute"
        },
        "按标签分离图像": {
            "desc": "按标签分离图像到不同文件夹",
            "fields": [
                {"name": "image_folder", "label": "图像文件夹", "type": "folder"},
                {"name": "label_folder", "label": "标签文件夹", "type": "folder"},
                {"name": "output_folder", "label": "输出文件夹", "type": "folder"}
            ],
            "action": "separate"
        },
        "移动图像到文件夹": {
            "desc": "移动图像到指定文件夹",
            "fields": [
                {"name": "image_list", "label": "图像列表文件", "type": "file"},
                {"name": "output_folder", "label": "目标文件夹", "type": "folder"}
            ],
            "action": "move_images"
        },
        "划分": {
            "desc": "划分数据集",
            "fields": [
                {"name": "input_folder", "label": "输入文件夹", "type": "folder"},
                {"name": "output_folder", "label": "输出文件夹", "type": "folder"}
            ],
            "action": "huafen"
        }
    },
    "其他功能": {
        "数据增强": {
            "desc": "图像和标签数据增强",
            "fields": [
                {"name": "image_folder", "label": "图像文件夹", "type": "folder"},
                {"name": "label_folder", "label": "标签文件夹", "type": "folder"}
            ],
            "action": "augmentation"
        },
        "负样本txt": {
            "desc": "处理负样本txt文件",
            "fields": [
                {"name": "input_folder", "label": "输入文件夹", "type": "folder"},
                {"name": "output_folder", "label": "输出文件夹", "type": "folder"}
            ],
            "action": "fuyangbentxt"
        }
    }
}


@app.route('/')
def index():
    """渲染主页面"""
    return render_template('index.html', functions=FUNCTIONS_CONFIG)


@app.route('/api/execute', methods=['POST'])
def execute_function():
    """执行工具函数"""
    data = request.json
    action = data.get('action')
    params = data.get('params', {})
    
    try:
        if action == 'crop_images':
            result = ToolFunctions.crop_images_bottom_half(
                params.get('input_folder'),
                params.get('output_folder')
            )
        elif action == 'split_images':
            result = ToolFunctions.split_images(
                params.get('input_folder'),
                params.get('output_folder')
            )
        elif action == 'remove_duplicate':
            result = ToolFunctions.remove_duplicate_images(
                params.get('input_folder')
            )
        elif action == 'sample_images':
            result = ToolFunctions.sample_images_by_timestamp(
                params.get('input_folder'),
                params.get('output_folder'),
                int(params.get('sample_count', 100))
            )
        elif action == 'extract_frames':
            result = ToolFunctions.extract_frames_from_videos(
                params.get('input_folder'),
                params.get('output_folder'),
                int(params.get('frame_interval', 10))
            )
        elif action == 'check_labels':
            result = ToolFunctions.check_labels(
                params.get('label_folder')
            )
        elif action == 'check_square':
            result = ToolFunctions.check_square_labels(
                params.get('label_folder'),
                float(params.get('threshold', 1.2)),
                params.get('image_folder')
            )
        elif action == 'check_counts':
            result = ToolFunctions.check_label_counts(
                params.get('label_folder')
            )
        elif action == 'check_count_class':
            result = ToolFunctions.check_label_count_class(
                params.get('label_folder'),
                params.get('output_file', 'label_count_class_report.txt')
            )
        elif action == 'find_no_labels':
            result = ToolFunctions.find_images_without_labels(
                params.get('image_folder'),
                params.get('label_folder')
            )
        elif action == 'find_extra':
            result = ToolFunctions.find_extra_labels(
                params.get('image_folder'),
                params.get('label_folder')
            )
        elif action == 'delete_no_labels':
            result = ToolFunctions.delete_images_without_labels(
                params.get('image_folder'),
                params.get('label_folder')
            )
        elif action == 'voc_to_yolo':
            result = ToolFunctions.voc_to_yolo(
                params.get('voc_folder'),
                params.get('yolo_folder')
            )
        elif action == 'distribute':
            result = ToolFunctions.distribute_labels(
                int(params.get('num_people', 2)),
                params.get('input_folder'),
                params.get('output_folder')
            )
        elif action == 'separate':
            result = ToolFunctions.separate_images_by_labels(
                params.get('image_folder'),
                params.get('label_folder'),
                params.get('output_folder')
            )
        elif action == 'move_images':
            result = ToolFunctions.move_images_to_folder(
                params.get('image_list'),
                params.get('output_folder')
            )
        elif action == 'augmentation':
            result = ToolFunctions.data_augmentation(
                params.get('image_folder'),
                params.get('label_folder')
            )
        elif action == 'huafen':
            result = ToolFunctions.huafen(
                params.get('input_folder'),
                params.get('output_folder')
            )
        elif action == 'fuyangbentxt':
            result = ToolFunctions.fuyangbentxt(
                params.get('input_folder'),
                params.get('output_folder')
            )
        elif action == 'video_to_images':
            result = ToolFunctions.video_to_images(
                params.get('input_folder'),
                params.get('output_folder')
            )
        elif action == 'labelme_to_yolo':
            result = ToolFunctions.convert_labelme_to_yolo(
                params.get('input_folder'),
                params.get('output_folder')
            )
        else:
            return jsonify({'success': False, 'error': f'未知操作: {action}'})
        
        return jsonify({'success': True, 'result': str(result) if result else '执行成功'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e), 'trace': traceback.format_exc()})


@app.route('/api/browse', methods=['POST'])
def browse_folder():
    """获取目录列表"""
    from pathlib import Path
    path = request.json.get('path', '')
    
    if not path or not os.path.exists(path):
        path = os.getcwd()
    
    try:
        items = []
        p = Path(path)
        
        for item in p.iterdir():
            items.append({
                'name': item.name,
                'type': 'folder' if item.is_dir() else 'file',
                'path': str(item.absolute())
            })
        
        items.sort(key=lambda x: (not x['type'], x['name'].lower()))
        
        return jsonify({'success': True, 'items': items, 'current_path': str(p.absolute())})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
