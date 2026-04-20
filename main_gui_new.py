import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import sys
import json

# 导入各个工具模块
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 定义工具功能类
class ToolFunctions:
    @staticmethod
    def crop_images_bottom_half(input_folder, output_folder):
        from image_cropper import crop_images_bottom_half
        crop_images_bottom_half(input_folder, output_folder)
    
    @staticmethod
    def split_images():
        from image_splitter import main
        main()
    
    @staticmethod
    def video_to_images(input_dir, output_base, interval):
        from video_to_images import batch_process
        batch_process(input_dir, output_base, interval)
    
    @staticmethod
    def check_labels(label_dir):
        from check_labels import check_label_classes
        check_label_classes(label_dir)
    
    @staticmethod
    def check_square_labels(labels_dir, aspect_ratio_threshold, image_dir):
        from check_square_labels import check_square_labels, save_results
        problematic_labels = check_square_labels(labels_dir, aspect_ratio_threshold, image_dir)
        output_file = os.path.join(os.path.dirname(labels_dir), 'problematic_square_labels.txt')
        save_results(problematic_labels, output_file)
    
    @staticmethod
    def distribute_labels(num_people, input_dir, output_dir):
        from distribute_labels import distribute_files
        distribute_files(num_people)
    
    @staticmethod
    def find_images_without_labels(image_dir, label_dir, output_file=None):
        from find_images_without_labels import find_images_without_labels, save_results
        images_without_labels = find_images_without_labels(image_dir, label_dir)
        if output_file:
            save_results(images_without_labels, output_file)
        else:
            save_results(images_without_labels)
    
    @staticmethod
    def check_label_counts(label_dir, threshold=1):
        from check_label_counts import check_label_counts, analyze_label_content
        stats = check_label_counts(label_dir, threshold)
        if stats['files_with_multiple_labels']:
            analyze_label_content(label_dir, threshold)
    
    @staticmethod
    def check_label_count_class(label_dir, output_file):
        from check_label_count_class import check_label_counts_and_classes, print_summary
        stats = check_label_counts_and_classes(label_dir, output_file)
        print_summary(stats)
    
    @staticmethod
    def data_augmentation(image_dir, label_dir):
        from data_augmentation import main
        main()
    
    @staticmethod
    def find_extra_labels(image_dir, label_dir):
        from find_extra_labels import main
        main()
    
    @staticmethod
    def remove_duplicate_images(image_dir):
        from remove_duplicate_images import main
        main()
    
    @staticmethod
    def separate_images_by_labels(image_dir, label_dir, output_dir):
        from separate_images_by_labels import separate_images_by_labels
        separate_images_by_labels(image_dir, label_dir, output_dir, move_files=True)
    
    @staticmethod
    def voc_to_yolo(voc_dir, yolo_dir):
        from voc_to_yolo import main
        main()
    
    @staticmethod
    def delete_images_without_labels(image_dir, label_dir):
        from delete_images_without_labels import main
        main()
    
    @staticmethod
    def sample_images_by_timestamp(image_dir, output_dir, sample_count):
        from sample_images_by_timestamp import main
        main()
    
    @staticmethod
    def extract_frames_from_videos(video_dir, output_dir, interval):
        from extract_frames_from_videos import main
        main()
    
    @staticmethod
    def move_images_to_folder(image_list, output_dir):
        from move_images_to_folder import main
        main()
    
    @staticmethod
    def fuyangbentxt(input_dir, output_dir):
        from fuyangbentxt import main
        main()
    
    @staticmethod
    def huafen(input_dir, output_dir):
        """调用划分数据集功能
        
        Args:
            input_dir: 输入目录路径
            output_dir: 输出目录路径
        """
        from huafen import main
        # 将输入和输出目录作为参数传递给huafen模块的main函数
        main(input_dir, output_dir)
    
    @staticmethod
    def sort_images_by_labels(image_dir, label_dir, classes_file, output_dir):
        """根据标签类别将图片分类到不同文件夹
        
        Args:
            image_dir: 图片文件夹路径
            label_dir: 标签文件夹路径
            classes_file: 类别文件 (classes.txt) 路径
            output_dir: 输出文件夹路径
        """
        from sort_images_by_labels import sort_images_by_labels
        sort_images_by_labels(image_dir, label_dir, classes_file, output_dir)
    
    @staticmethod
    def sam_to_yolo(input_dir, output_dir):
        """将xanylableing的sam标签转换为YOLO格式
        
        Args:
            input_dir: 包含图像和sam标签的目录
            output_dir: 输出YOLO标签的目录
        """
        from convert_sam_to_yolo import convert_sam_to_yolo
        convert_sam_to_yolo(input_dir, output_dir)
    
    @staticmethod
    def find_extreme_area_labels(label_dir, image_dir, above_percent=150, below_percent=50):
        """找出标签面积中位数，并找出大于面积中位数或小于中位数XX%的标签
        
        Args:
            label_dir: 标签文件所在目录
            image_dir: 图像文件所在目录
            above_percent: 大于中位数的百分比阈值，默认150%
            below_percent: 小于中位数的百分比阈值，默认50%
        """
        from find_extreme_area_labels import find_extreme_area_labels
        find_extreme_area_labels(label_dir, image_dir, above_percent, below_percent)

# 主应用类
class YoloLabelToolsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Labelo")
        
        # 获取屏幕分辨率并自适应窗口大小
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # 设置窗口大小为屏幕的90%
        window_width = int(screen_width * 0.7)
        window_height = int(screen_height * 0.7)
        
        # 确保窗口大小不小于最小尺寸
        window_width = max(window_width, 800)
        window_height = max(window_height, 600)
        
        self.root.geometry(f"{window_width}x{window_height}")
        self.root.resizable(True, True)
        
        # 窗口居中显示
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"+{x}+{y}")
        
        # 配置文件路径
        self.config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
        
        # 加载配置
        self.config = self.load_config()
        
        # 设置现代风格
        self.setup_style()
        
        # 创建主框架
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建侧边栏和主内容区域
        self.create_layout()
        
        # 创建标题
        self.create_title()
        
        # 创建输出日志区域
        self.create_output_log()
        
        # 初始化当前功能
        self.current_function = None
        
        # 创建所有功能的界面
        self.create_all_functions()
        
        # 默认显示第一个功能
        self.show_function("图片裁剪")
        
        # 重定向标准输出到日志区域
        self.redirect_stdout()
    
    def create_output_log(self):
        """创建输出日志区域"""
        # 日志标题
        log_title = ttk.Label(self.content_area, text="输出日志", style='Subtitle.TLabel')
        log_title.pack(anchor=tk.W, pady=(10, 5))
        
        # 日志框架
        log_frame = ttk.Frame(self.content_area)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # 日志文本框
        self.log_text = tk.Text(log_frame, height=10, wrap=tk.WORD)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=scrollbar.set)
        
        # 设置只读
        self.log_text.config(state=tk.DISABLED)
    
    def redirect_stdout(self):
        """重定向标准输出到日志区域"""
        import sys
        
        class StdoutRedirector:
            def __init__(self, text_widget):
                self.text_widget = text_widget
            
            def write(self, text):
                self.text_widget.config(state=tk.NORMAL)
                self.text_widget.insert(tk.END, text)
                self.text_widget.see(tk.END)
                self.text_widget.config(state=tk.DISABLED)
            
            def flush(self):
                pass
        
        # 重定向标准输出和标准错误
        sys.stdout = StdoutRedirector(self.log_text)
        sys.stderr = StdoutRedirector(self.log_text)
    
    def load_config(self):
        """加载配置文件"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                messagebox.showerror("错误", f"加载配置文件失败：{str(e)}")
        return {}
    
    def save_config(self):
        """保存配置文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("错误", f"保存配置文件失败：{str(e)}")
    
    def update_config(self, key, value):
        """更新配置并保存"""
        self.config[key] = value
        self.save_config()
        
    def setup_style(self):
        """设置现代风格"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # 自定义样式
        style.configure('TLabel', font=('微软雅黑', 10))
        style.configure('TButton', font=('微软雅黑', 10), padding=6)
        style.configure('TNotebook.Tab', font=('微软雅黑', 10), padding=[15, 5])
        style.configure('Title.TLabel', font=('微软雅黑', 16, 'bold'))
        style.configure('Subtitle.TLabel', font=('微软雅黑', 12, 'bold'))
        
    def create_layout(self):
        """创建侧边栏和主内容区域布局"""
        # 创建侧边栏
        self.sidebar = ttk.Frame(self.main_frame, width=250)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        # 创建主内容区域
        self.content_area = ttk.Frame(self.main_frame)
        self.content_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 创建功能列表，包含功能名称和描述
        self.function_list = ttk.Treeview(self.sidebar, columns=('功能名称', '描述'), show='tree headings')
        self.function_list.heading('#0', text='分类')
        self.function_list.heading('功能名称', text='功能名称')
        self.function_list.heading('描述', text='功能描述')
        self.function_list.column('#0', width=80)
        self.function_list.column('功能名称', width=100)
        self.function_list.column('描述', width=200)
        self.function_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 功能分类和描述
        self.function_categories = {
            "图像处理": {
                "图片裁剪": {
                    "func": self.create_crop_function,
                    "desc": "裁剪图片下半部分"
                },
                "图片分割": {
                    "func": self.create_split_function,
                    "desc": "分割图片为多个部分"
                },
                "移除重复图像": {
                    "func": self.create_remove_duplicate_images_function,
                    "desc": "移除文件夹中的重复图像"
                },
                "按时间戳采样图像": {
                    "func": self.create_sample_images_by_timestamp_function,
                    "desc": "根据时间戳采样图像"
                }
            },
            "视频处理": {
                "从视频提取帧": {
                    "func": self.create_extract_frames_from_videos_function,
                    "desc": "从视频提取图像帧（支持多种格式和调整大小）"
                }
            },
            "标签处理": {
                "检查标签类别": {
                    "func": self.create_check_labels_function,
                    "desc": "检查标签文件中的类别分布"
                },
                "检查正方形标签": {
                    "func": self.create_check_square_function,
                    "desc": "检查边界框是否近似正方形"
                },
                "检查标签数量": {
                    "func": self.create_check_label_counts_function,
                    "desc": "检查标签文件中的标签数量"
                },
                "检查标签和类别": {
                    "func": self.create_check_label_count_class_function,
                    "desc": "检查标签和类别数量"
                },
                "查找无标签图像": {
                    "func": self.create_find_images_without_labels_function,
                    "desc": "查找无对应标签的图像"
                },
                "查找多余标签": {
                    "func": self.create_find_extra_labels_function,
                    "desc": "查找无对应图像的标签"
                },
                "删除无标签图像": {
                    "func": self.create_delete_images_without_labels_function,
                    "desc": "删除无对应标签的图像"
                },
                "VOC转YOLO": {
                    "func": self.create_voc_to_yolo_function,
                    "desc": "VOC格式转YOLO格式"
                },
                "SAM标签转YOLO": {
                    "func": self.create_sam_to_yolo_function,
                    "desc": "将xanylableing的sam标签转换为YOLO格式"
                },
                "标签面积极端值": {
                    "func": self.create_find_extreme_area_labels_function,
                    "desc": "找出标签面积中位数及极端面积标签"
                }
            },
            "数据管理": {
                "分配标签": {
                    "func": self.create_distribute_labels_function,
                    "desc": "分配文件到多个文件夹"
                },
                "按标签分离图像": {
                    "func": self.create_separate_images_by_labels_function,
                    "desc": "按标签分离图像到不同文件夹"
                },
                "按标签分类图像": {
                    "func": self.create_sort_images_by_labels_function,
                    "desc": "根据标签类别将图片分类到不同文件夹"
                },
                "移动图像到文件夹": {
                    "func": self.create_move_images_to_folder_function,
                    "desc": "移动图像到指定文件夹"
                },
                "划分": {
                    "func": self.create_huafen_function,
                    "desc": "划分数据集"
                }
            },
            "其他功能": {
                "数据增强": {
                    "func": self.create_data_augmentation_function,
                    "desc": "图像和标签数据增强"
                },
                "负样本txt": {
                    "func": self.create_fuyangbentxt_function,
                    "desc": "处理负样本txt文件"
                }
            }
        }
        
        # 构建扁平函数映射
        self.functions = {}
        for category, funcs in self.function_categories.items():
            for func_name, func_info in funcs.items():
                self.functions[func_name] = func_info["func"]
        
        # 添加功能到列表，按分类组织
        for category, funcs in self.function_categories.items():
            # 创建分类节点
            cat_node = self.function_list.insert('', tk.END, text=category, open=True)
            # 添加该分类下的所有功能
            for func_name, func_info in funcs.items():
                self.function_list.insert(cat_node, tk.END, values=(func_name, func_info["desc"]))
        
        # 绑定选择事件
        self.function_list.bind('<<TreeviewSelect>>', self.on_function_select)
        
    def create_title(self):
        """创建标题"""
        self.title_label = ttk.Label(self.content_area, text="YOLO标签工具", style='Title.TLabel')
        self.title_label.pack(pady=20)
        
    def on_function_select(self, event):
        """处理功能选择事件"""
        selected_items = self.function_list.selection()
        if selected_items:
            item = self.function_list.item(selected_items[0])
            # 检查是否是功能节点（有values属性），而不是分类节点
            if 'values' in item and item['values']:
                func_name = item['values'][0]
                self.show_function(func_name)
        
    def show_function(self, func_name):
        """显示选中的功能"""
        # 隐藏当前显示的功能
        if self.current_function:
            self.current_function.pack_forget()
        
        # 获取并显示选中的功能框架
        self.current_function = self.function_frames[func_name]
        self.current_function.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
    def create_all_functions(self):
        """创建所有功能的界面"""
        # 初始化功能字典
        self.function_frames = {}
        
        # 初始化所有功能的变量
        self.initialize_variables()
        
        # 为每个功能创建一个框架并初始化界面
        for func_name in self.functions:
            frame = ttk.Frame(self.content_area)
            self.function_frames[func_name] = frame
            
            # 调用对应的创建函数来初始化界面
            self.functions[func_name]()
        
    def initialize_variables(self):
        """初始化所有功能的变量"""
        # 从配置中获取值，不存在则使用默认值
        config = self.config
        
        # 图片裁剪
        self.crop_input_var = tk.StringVar(value=config.get("crop_input", ""))
        self.crop_output_var = tk.StringVar(value=config.get("crop_output", ""))
        
        # 图片分割
        self.split_input_var = tk.StringVar(value=config.get("split_input", ""))
        self.split_output_var = tk.StringVar(value=config.get("split_output", ""))
        
        # 检查标签类别
        self.check_labels_var = tk.StringVar(value=config.get("check_labels", ""))
        
        # 检查正方形标签
        self.square_labels_var = tk.StringVar(value=config.get("square_labels", ""))
        self.square_images_var = tk.StringVar(value=config.get("square_images", ""))
        self.square_threshold_var = tk.DoubleVar(value=config.get("square_threshold", 1.2))
        
        # 分配标签
        self.distribute_num_var = tk.IntVar(value=config.get("distribute_num", 2))
        self.distribute_input_var = tk.StringVar(value=config.get("distribute_input", ""))
        self.distribute_output_var = tk.StringVar(value=config.get("distribute_output", ""))
        
        # 查找无标签图像
        self.find_images_var = tk.StringVar(value=config.get("find_images", ""))
        self.find_labels_var = tk.StringVar(value=config.get("find_labels", ""))
        
        # 检查标签数量
        self.check_counts_var = tk.StringVar(value=config.get("check_counts", ""))
        self.check_counts_threshold_var = tk.StringVar(value=config.get("check_counts_threshold", "1"))
        
        # 检查标签和类别
        self.check_count_class_var = tk.StringVar(value=config.get("check_count_class", ""))
        self.check_count_class_output_var = tk.StringVar(value=config.get("check_count_class_output", "label_count_class_report.txt"))
        
        # 移除重复图像
        self.remove_duplicate_var = tk.StringVar(value=config.get("remove_duplicate", ""))
        
        # 按标签分离图像
        self.separate_images_var = tk.StringVar(value=config.get("separate_images", ""))
        self.separate_labels_var = tk.StringVar(value=config.get("separate_labels", ""))
        self.separate_output_var = tk.StringVar(value=config.get("separate_output", ""))
        
        # VOC转YOLO
        self.voc_input_var = tk.StringVar(value=config.get("voc_input", ""))
        self.voc_output_var = tk.StringVar(value=config.get("voc_output", ""))
        
        # 删除无标签图像
        self.delete_images_var = tk.StringVar(value=config.get("delete_images", ""))
        self.delete_labels_var = tk.StringVar(value=config.get("delete_labels", ""))
        
        # 按时间戳采样图像
        self.sample_images_var = tk.StringVar(value=config.get("sample_images", ""))
        self.sample_output_var = tk.StringVar(value=config.get("sample_output", ""))
        self.sample_count_var = tk.IntVar(value=config.get("sample_count", 100))
        
        # 从视频提取帧
        self.extract_videos_var = tk.StringVar(value=config.get("extract_videos", ""))
        self.extract_output_var = tk.StringVar(value=config.get("extract_output", ""))
        self.extract_interval_var = tk.IntVar(value=config.get("extract_interval", 10))
        self.extract_crop_var = tk.BooleanVar(value=config.get("extract_crop", False))
        
        # 移动图像到文件夹
        self.move_images_list_var = tk.StringVar(value=config.get("move_images_list", ""))
        self.move_images_output_var = tk.StringVar(value=config.get("move_images_output", ""))
        
        # 负样本txt
        self.fuyangbentxt_input_var = tk.StringVar(value=config.get("fuyangbentxt_input", ""))
        self.fuyangbentxt_output_var = tk.StringVar(value=config.get("fuyangbentxt_output", ""))
        
        # 划分数据集
        self.huafen_input_var = tk.StringVar(value=config.get("huafen_input", ""))
        self.huafen_output_var = tk.StringVar(value=config.get("huafen_output", ""))
        
        # 按标签分类图像
        self.sort_images_var = tk.StringVar(value=config.get("sort_images", ""))
        self.sort_labels_var = tk.StringVar(value=config.get("sort_labels", ""))
        self.sort_classes_var = tk.StringVar(value=config.get("sort_classes", ""))
        self.sort_output_var = tk.StringVar(value=config.get("sort_output", ""))
        
        # SAM标签转YOLO
        self.sam_input_var = tk.StringVar(value=config.get("sam_input", ""))
        self.sam_output_var = tk.StringVar(value=config.get("sam_output", ""))
        
        # 标签面积极端值分析
        self.extreme_area_labels_var = tk.StringVar(value=config.get("extreme_area_labels", ""))
        self.extreme_area_images_var = tk.StringVar(value=config.get("extreme_area_images", ""))
        self.extreme_area_above_var = tk.StringVar(value=config.get("extreme_area_above", "150"))
        self.extreme_area_below_var = tk.StringVar(value=config.get("extreme_area_below", "50"))
        
        # 数据增强
        self.augmentation_images_var = tk.StringVar(value=config.get("augmentation_images", ""))
        self.augmentation_labels_var = tk.StringVar(value=config.get("augmentation_labels", ""))
        
        # 查找多余标签
        self.extra_images_var = tk.StringVar(value=config.get("extra_images", ""))
        self.extra_labels_var = tk.StringVar(value=config.get("extra_labels", ""))
        
    def create_crop_function(self):
        """创建图片裁剪功能界面"""
        frame = self.function_frames["图片裁剪"]
        
        # 功能备注
        note_label = ttk.Label(frame, text="备注：读取文件夹中的jpg文件，裁切掉下半部分，然后输出到另一个文件夹")
        note_label.pack(anchor=tk.W, pady=(0, 15))
        
        # 输入文件夹
        ttk.Label(frame, text="输入文件夹:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(0, 5))
        input_frame = ttk.Frame(frame)
        input_frame.pack(fill=tk.X, pady=(0, 15))
        ttk.Entry(input_frame, textvariable=self.crop_input_var, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Button(input_frame, text="浏览", command=self.browse_crop_input).pack(side=tk.RIGHT)
        
        # 输出文件夹
        ttk.Label(frame, text="输出文件夹:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(0, 5))
        output_frame = ttk.Frame(frame)
        output_frame.pack(fill=tk.X, pady=(0, 20))
        ttk.Entry(output_frame, textvariable=self.crop_output_var, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Button(output_frame, text="浏览", command=self.browse_crop_output).pack(side=tk.RIGHT)
        
        # 执行按钮
        ttk.Button(frame, text="开始裁剪", command=self.run_crop, style='TButton').pack(anchor=tk.CENTER, pady=20)
        
    def create_split_function(self):
        """创建图片分割功能界面"""
        frame = self.function_frames["图片分割"]
        
        note_label = ttk.Label(frame, text="备注：将1536x1024的图片裁剪并分割成多个1536x150的图片")
        note_label.pack(anchor=tk.W, pady=(0, 15))
        
        # 输入文件夹
        ttk.Label(frame, text="输入文件夹:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(0, 5))
        input_frame = ttk.Frame(frame)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Entry(input_frame, textvariable=self.split_input_var, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Button(input_frame, text="浏览", command=self.browse_split_input).pack(side=tk.RIGHT)
        
        # 输出文件夹
        ttk.Label(frame, text="输出文件夹:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(0, 5))
        output_frame = ttk.Frame(frame)
        output_frame.pack(fill=tk.X, pady=(0, 20))
        ttk.Entry(output_frame, textvariable=self.split_output_var, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Button(output_frame, text="浏览", command=self.browse_split_output).pack(side=tk.RIGHT)
        
        # 执行按钮
        ttk.Button(frame, text="开始分割", command=self.run_split, style='TButton').pack(anchor=tk.CENTER, pady=20)
        

        
    def create_check_labels_function(self):
        """创建检查标签类别功能界面"""
        frame = self.function_frames["检查标签类别"]
        
        note_label = ttk.Label(frame, text="备注：检查标签文件中的类别分布，特别查找是否存在类别1的标签")
        note_label.pack(anchor=tk.W, pady=(0, 15))
        
        # 标签文件夹
        ttk.Label(frame, text="标签文件夹:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(0, 5))
        input_frame = ttk.Frame(frame)
        input_frame.pack(fill=tk.X, pady=(0, 20))
        ttk.Entry(input_frame, textvariable=self.check_labels_var, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Button(input_frame, text="浏览", command=self.browse_check_labels).pack(side=tk.RIGHT)
        
        # 执行按钮
        ttk.Button(frame, text="开始检查", command=self.run_check_labels, style='TButton').pack(anchor=tk.CENTER, pady=20)
        
    def create_check_square_function(self):
        """创建检查正方形标签功能界面"""
        frame = self.function_frames["检查正方形标签"]
        
        note_label = ttk.Label(frame, text="备注：检查标签文件夹中的边界框是否近似正方形，找出可能有问题的长方形标签")
        note_label.pack(anchor=tk.W, pady=(0, 15))
        
        # 标签文件夹
        ttk.Label(frame, text="标签文件夹:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(0, 5))
        labels_frame = ttk.Frame(frame)
        labels_frame.pack(fill=tk.X, pady=(0, 15))
        ttk.Entry(labels_frame, textvariable=self.square_labels_var, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Button(labels_frame, text="浏览", command=self.browse_square_labels).pack(side=tk.RIGHT)
        
        # 图像文件夹
        ttk.Label(frame, text="图像文件夹:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(0, 5))
        images_frame = ttk.Frame(frame)
        images_frame.pack(fill=tk.X, pady=(0, 15))
        ttk.Entry(images_frame, textvariable=self.square_images_var, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Button(images_frame, text="浏览", command=self.browse_square_images).pack(side=tk.RIGHT)
        
        # 宽高比阈值
        ttk.Label(frame, text="宽高比阈值:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(0, 5))
        ttk.Entry(frame, textvariable=self.square_threshold_var, width=10).pack(anchor=tk.W, pady=(0, 20))
        
        # 执行按钮
        ttk.Button(frame, text="开始检查", command=self.run_check_square, style='TButton').pack(anchor=tk.CENTER, pady=20)
        
    def create_distribute_labels_function(self):
        """创建分配标签功能界面"""
        frame = self.function_frames["分配标签"]
        
        note_label = ttk.Label(frame, text="备注：将images和labels文件夹中的文件分配到N个文件夹中")
        note_label.pack(anchor=tk.W, pady=(0, 15))
        
        # 输入文件夹
        ttk.Label(frame, text="输入文件夹:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(0, 5))
        input_frame = ttk.Frame(frame)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Entry(input_frame, textvariable=self.distribute_input_var, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Button(input_frame, text="浏览", command=self.browse_distribute_input).pack(side=tk.RIGHT)
        
        # 输出文件夹
        ttk.Label(frame, text="输出文件夹:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(0, 5))
        output_frame = ttk.Frame(frame)
        output_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Entry(output_frame, textvariable=self.distribute_output_var, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Button(output_frame, text="浏览", command=self.browse_distribute_output).pack(side=tk.RIGHT)
        
        ttk.Label(frame, text="分配人数:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(0, 5))
        ttk.Entry(frame, textvariable=self.distribute_num_var, width=10).pack(anchor=tk.W, pady=(0, 15))
        
        ttk.Button(frame, text="开始分配", command=self.run_distribute_labels, style='TButton').pack(anchor=tk.CENTER, pady=20)
        
    def create_find_images_without_labels_function(self):
        """创建查找无标签图像功能界面"""
        frame = self.function_frames["查找无标签图像"]
        
        note_label = ttk.Label(frame, text="备注：查找没有对应标签文件的图像文件")
        note_label.pack(anchor=tk.W, pady=(0, 15))
        
        ttk.Label(frame, text="图像文件夹:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(0, 5))
        input_frame = ttk.Frame(frame)
        input_frame.pack(fill=tk.X, pady=(0, 15))
        ttk.Entry(input_frame, textvariable=self.find_images_var, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Button(input_frame, text="浏览", command=self.browse_find_images).pack(side=tk.RIGHT)
        
        ttk.Label(frame, text="标签文件夹:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(0, 5))
        labels_frame = ttk.Frame(frame)
        labels_frame.pack(fill=tk.X, pady=(0, 15))
        ttk.Entry(labels_frame, textvariable=self.find_labels_var, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Button(labels_frame, text="浏览", command=self.browse_find_labels).pack(side=tk.RIGHT)
        
        ttk.Button(frame, text="开始查找", command=self.run_find_images_without_labels, style='TButton').pack(anchor=tk.CENTER, pady=20)
        
    def create_check_label_counts_function(self):
        """创建检查标签数量功能界面"""
        frame = self.function_frames["检查标签数量"]
        
        note_label = ttk.Label(frame, text="备注：检查标签文件中的标签数量，列出标签数量大于设定阈值的文件")
        note_label.pack(anchor=tk.W, pady=(0, 15))
        
        ttk.Label(frame, text="标签文件夹:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(0, 5))
        input_frame = ttk.Frame(frame)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Entry(input_frame, textvariable=self.check_counts_var, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Button(input_frame, text="浏览", command=self.browse_check_counts).pack(side=tk.RIGHT)
        
        ttk.Label(frame, text="阈值:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(0, 5))
        ttk.Label(frame, text="列出标签数量大于此值的文件").pack(anchor=tk.W, pady=(0, 10))
        ttk.Entry(frame, textvariable=self.check_counts_threshold_var, width=10).pack(anchor=tk.W, pady=(0, 20))
        
        ttk.Button(frame, text="开始检查", command=self.run_check_label_counts, style='TButton').pack(anchor=tk.CENTER, pady=20)
        
    def create_check_label_count_class_function(self):
        """创建检查标签和类别数量功能界面"""
        frame = self.function_frames["检查标签和类别"]
        
        note_label = ttk.Label(frame, text="备注：检查标签文件中的标签数量和类别数量是否超过两个")
        note_label.pack(anchor=tk.W, pady=(0, 15))
        
        ttk.Label(frame, text="标签文件夹:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(0, 5))
        input_frame = ttk.Frame(frame)
        input_frame.pack(fill=tk.X, pady=(0, 15))
        ttk.Entry(input_frame, textvariable=self.check_count_class_var, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Button(input_frame, text="浏览", command=self.browse_check_count_class).pack(side=tk.RIGHT)
        
        ttk.Label(frame, text="输出文件名:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(0, 5))
        ttk.Entry(frame, textvariable=self.check_count_class_output_var, width=50).pack(anchor=tk.W, pady=(0, 15))
        
        ttk.Button(frame, text="开始检查", command=self.run_check_label_count_class, style='TButton').pack(anchor=tk.CENTER, pady=20)
        
    def create_data_augmentation_function(self):
        """创建数据增强功能界面"""
        frame = self.function_frames["数据增强"]
        
        note_label = ttk.Label(frame, text="备注：对图像和标签进行数据增强操作")
        note_label.pack(anchor=tk.W, pady=(0, 15))
        
        ttk.Button(frame, text="开始增强", command=self.run_data_augmentation, style='TButton').pack(anchor=tk.CENTER, pady=20)
    

        
    def create_find_extra_labels_function(self):
        """创建查找多余标签功能界面"""
        frame = self.function_frames["查找多余标签"]
        
        note_label = ttk.Label(frame, text="备注：查找没有对应图像文件的标签文件")
        note_label.pack(anchor=tk.W, pady=(0, 15))
        
        ttk.Button(frame, text="开始查找", command=self.run_find_extra_labels, style='TButton').pack(anchor=tk.CENTER, pady=20)
        
    def create_remove_duplicate_images_function(self):
        """创建移除重复图像功能界面"""
        frame = self.function_frames["移除重复图像"]
        
        note_label = ttk.Label(frame, text="备注：移除文件夹中的重复图像")
        note_label.pack(anchor=tk.W, pady=(0, 15))
        
        # 图像文件夹
        ttk.Label(frame, text="图像文件夹:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(0, 5))
        input_frame = ttk.Frame(frame)
        input_frame.pack(fill=tk.X, pady=(0, 20))
        self.remove_duplicate_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.remove_duplicate_var, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Button(input_frame, text="浏览", command=self.browse_remove_duplicate).pack(side=tk.RIGHT)
        
        ttk.Button(frame, text="开始移除", command=self.run_remove_duplicate_images, style='TButton').pack(anchor=tk.CENTER, pady=20)
        
    def create_separate_images_by_labels_function(self):
        """创建按标签分离图像功能界面"""
        frame = self.function_frames["按标签分离图像"]
        
        # 详细的功能描述
        note_label = ttk.Label(frame, text="备注：该功能将图像文件根据是否有对应的标签文件分离到不同子文件夹。")
        note_label.pack(anchor=tk.W, pady=(0, 5))
        detail_label1 = ttk.Label(frame, text="- 有标签的图像：会移动到'labeled'子文件夹")
        detail_label1.pack(anchor=tk.W, pady=(0, 5))
        detail_label2 = ttk.Label(frame, text="- 无标签的图像：会移动到'unlabeled'子文件夹")
        detail_label2.pack(anchor=tk.W, pady=(0, 5))
        detail_label3 = ttk.Label(frame, text="适用于整理数据集、查找未标记图像、验证标注完整性等场景。")
        detail_label3.pack(anchor=tk.W, pady=(0, 15))
        
        # 图像文件夹
        ttk.Label(frame, text="图像文件夹:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(0, 5))
        input_frame = ttk.Frame(frame)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        self.separate_images_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.separate_images_var, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Button(input_frame, text="浏览", command=self.browse_separate_images).pack(side=tk.RIGHT)
        
        # 标签文件夹
        ttk.Label(frame, text="标签文件夹:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(0, 5))
        labels_frame = ttk.Frame(frame)
        labels_frame.pack(fill=tk.X, pady=(0, 10))
        self.separate_labels_var = tk.StringVar()
        ttk.Entry(labels_frame, textvariable=self.separate_labels_var, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Button(labels_frame, text="浏览", command=self.browse_separate_labels).pack(side=tk.RIGHT)
        
        # 输出文件夹
        ttk.Label(frame, text="输出文件夹:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(0, 5))
        output_frame = ttk.Frame(frame)
        output_frame.pack(fill=tk.X, pady=(0, 20))
        self.separate_output_var = tk.StringVar()
        ttk.Entry(output_frame, textvariable=self.separate_output_var, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Button(output_frame, text="浏览", command=self.browse_separate_output).pack(side=tk.RIGHT)
        
        ttk.Button(frame, text="开始分离", command=self.run_separate_images_by_labels, style='TButton').pack(anchor=tk.CENTER, pady=20)
        
    def create_voc_to_yolo_function(self):
        """创建VOC转YOLO功能界面"""
        frame = self.function_frames["VOC转YOLO"]
        
        note_label = ttk.Label(frame, text="备注：将VOC格式的标签转换为YOLO格式")
        note_label.pack(anchor=tk.W, pady=(0, 15))
        
        # VOC文件夹
        ttk.Label(frame, text="VOC文件夹:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(0, 5))
        input_frame = ttk.Frame(frame)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        self.voc_input_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.voc_input_var, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Button(input_frame, text="浏览", command=self.browse_voc_input).pack(side=tk.RIGHT)
        
        # YOLO输出文件夹
        ttk.Label(frame, text="YOLO输出文件夹:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(0, 5))
        output_frame = ttk.Frame(frame)
        output_frame.pack(fill=tk.X, pady=(0, 20))
        self.voc_output_var = tk.StringVar()
        ttk.Entry(output_frame, textvariable=self.voc_output_var, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Button(output_frame, text="浏览", command=self.browse_voc_output).pack(side=tk.RIGHT)
        
        ttk.Button(frame, text="开始转换", command=self.run_voc_to_yolo, style='TButton').pack(anchor=tk.CENTER, pady=20)
        
    def create_sam_to_yolo_function(self):
        """创建SAM标签转YOLO功能界面"""
        frame = self.function_frames["SAM标签转YOLO"]
        
        note_label = ttk.Label(frame, text="备注：将xanylableing的sam标签转换为YOLO格式的矩形框标签")
        note_label.pack(anchor=tk.W, pady=(0, 15))
        
        # 输入文件夹
        ttk.Label(frame, text="输入文件夹:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(0, 5))
        input_frame = ttk.Frame(frame)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Entry(input_frame, textvariable=self.sam_input_var, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Button(input_frame, text="浏览", command=self.browse_sam_input).pack(side=tk.RIGHT)
        
        # 输出文件夹
        ttk.Label(frame, text="输出文件夹:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(0, 5))
        output_frame = ttk.Frame(frame)
        output_frame.pack(fill=tk.X, pady=(0, 20))
        ttk.Entry(output_frame, textvariable=self.sam_output_var, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Button(output_frame, text="浏览", command=self.browse_sam_output).pack(side=tk.RIGHT)
        
        # 执行按钮
        ttk.Button(frame, text="开始转换", command=self.run_sam_to_yolo, style='TButton').pack(anchor=tk.CENTER, pady=20)
        
    def create_find_extreme_area_labels_function(self):
        """创建标签面积极端值分析功能界面"""
        frame = self.function_frames["标签面积极端值"]
        
        note_label = ttk.Label(frame, text="备注：找出标签面积中位数，并找出大于面积中位数或小于中位数XX%的标签")
        note_label.pack(anchor=tk.W, pady=(0, 15))
        
        # 标签文件夹
        ttk.Label(frame, text="标签文件夹:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(0, 5))
        labels_frame = ttk.Frame(frame)
        labels_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Entry(labels_frame, textvariable=self.extreme_area_labels_var, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Button(labels_frame, text="浏览", command=self.browse_extreme_area_labels).pack(side=tk.RIGHT)
        
        # 图像文件夹
        ttk.Label(frame, text="图像文件夹:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(0, 5))
        images_frame = ttk.Frame(frame)
        images_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Entry(images_frame, textvariable=self.extreme_area_images_var, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Button(images_frame, text="浏览", command=self.browse_extreme_area_images).pack(side=tk.RIGHT)
        
        # 大于中位数百分比阈值
        ttk.Label(frame, text="大于中位数百分比(%):", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(0, 5))
        ttk.Label(frame, text="找出面积大于中位数此百分比的标签（默认150，即1.5倍）").pack(anchor=tk.W, pady=(0, 5))
        ttk.Entry(frame, textvariable=self.extreme_area_above_var, width=10).pack(anchor=tk.W, pady=(0, 10))
        
        # 小于中位数百分比阈值
        ttk.Label(frame, text="小于中位数百分比(%):", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(0, 5))
        ttk.Label(frame, text="找出面积小于中位数此百分比的标签（默认50，即一半）").pack(anchor=tk.W, pady=(0, 5))
        ttk.Entry(frame, textvariable=self.extreme_area_below_var, width=10).pack(anchor=tk.W, pady=(0, 20))
        
        # 执行按钮
        ttk.Button(frame, text="开始分析", command=self.run_find_extreme_area_labels, style='TButton').pack(anchor=tk.CENTER, pady=20)
        
    def create_delete_images_without_labels_function(self):
        """创建删除无标签图像功能界面"""
        frame = self.function_frames["删除无标签图像"]
        
        note_label = ttk.Label(frame, text="备注：删除没有对应标签文件的图像文件")
        note_label.pack(anchor=tk.W, pady=(0, 15))
        
        # 图像文件夹
        ttk.Label(frame, text="图像文件夹:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(0, 5))
        input_frame = ttk.Frame(frame)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        self.delete_images_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.delete_images_var, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Button(input_frame, text="浏览", command=self.browse_delete_images).pack(side=tk.RIGHT)
        
        # 标签文件夹
        ttk.Label(frame, text="标签文件夹:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(0, 5))
        labels_frame = ttk.Frame(frame)
        labels_frame.pack(fill=tk.X, pady=(0, 20))
        self.delete_labels_var = tk.StringVar()
        ttk.Entry(labels_frame, textvariable=self.delete_labels_var, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Button(labels_frame, text="浏览", command=self.browse_delete_labels).pack(side=tk.RIGHT)
        
        ttk.Button(frame, text="开始删除", command=self.run_delete_images_without_labels, style='TButton').pack(anchor=tk.CENTER, pady=20)
        
    def create_sample_images_by_timestamp_function(self):
        """创建按时间戳采样图像功能界面"""
        frame = self.function_frames["按时间戳采样图像"]
        
        note_label = ttk.Label(frame, text="备注：根据时间戳对图像进行采样")
        note_label.pack(anchor=tk.W, pady=(0, 15))
        
        # 图像文件夹
        ttk.Label(frame, text="图像文件夹:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(0, 5))
        input_frame = ttk.Frame(frame)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        self.sample_images_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.sample_images_var, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Button(input_frame, text="浏览", command=self.browse_sample_images).pack(side=tk.RIGHT)
        
        # 输出文件夹
        ttk.Label(frame, text="输出文件夹:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(0, 5))
        output_frame = ttk.Frame(frame)
        output_frame.pack(fill=tk.X, pady=(0, 10))
        self.sample_output_var = tk.StringVar()
        ttk.Entry(output_frame, textvariable=self.sample_output_var, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Button(output_frame, text="浏览", command=self.browse_sample_output).pack(side=tk.RIGHT)
        
        # 采样数量
        ttk.Label(frame, text="采样数量:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(0, 5))
        self.sample_count_var = tk.IntVar(value=100)
        ttk.Entry(frame, textvariable=self.sample_count_var, width=10).pack(anchor=tk.W, pady=(0, 20))
        
        ttk.Button(frame, text="开始采样", command=self.run_sample_images_by_timestamp, style='TButton').pack(anchor=tk.CENTER, pady=20)
        
    def create_extract_frames_from_videos_function(self):
        """创建从视频提取帧功能界面"""
        frame = self.function_frames["从视频提取帧"]
        
        note_label = ttk.Label(frame, text="备注：从视频文件中提取图像帧")
        note_label.pack(anchor=tk.W, pady=(0, 15))
        
        # 视频文件夹
        ttk.Label(frame, text="视频文件夹:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(0, 5))
        input_frame = ttk.Frame(frame)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Entry(input_frame, textvariable=self.extract_videos_var, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Button(input_frame, text="浏览", command=self.browse_extract_videos).pack(side=tk.RIGHT)
        
        # 输出文件夹
        ttk.Label(frame, text="输出文件夹:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(0, 5))
        output_frame = ttk.Frame(frame)
        output_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Entry(output_frame, textvariable=self.extract_output_var, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Button(output_frame, text="浏览", command=self.browse_extract_output).pack(side=tk.RIGHT)
        
        # 帧间隔
        ttk.Label(frame, text="帧间隔:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(0, 5))
        interval_frame = ttk.Frame(frame)
        interval_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Entry(interval_frame, textvariable=self.extract_interval_var, width=10).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Label(interval_frame, text="（每隔多少帧保存一次）").pack(side=tk.LEFT)
        
        # 裁剪选项
        crop_frame = ttk.Frame(frame)
        crop_frame.pack(fill=tk.X, pady=(0, 20))
        self.extract_crop_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(crop_frame, text="裁剪掉图片下半部分", variable=self.extract_crop_var).pack(anchor=tk.W)
        
        ttk.Button(frame, text="开始提取", command=self.run_extract_frames_from_videos, style='TButton').pack(anchor=tk.CENTER, pady=20)
        
    def create_move_images_to_folder_function(self):
        """创建移动图像到文件夹功能界面"""
        frame = self.function_frames["移动图像到文件夹"]
        
        note_label = ttk.Label(frame, text="备注：将图像移动到指定文件夹")
        note_label.pack(anchor=tk.W, pady=(0, 15))
        
        # 图像列表文件
        ttk.Label(frame, text="图像列表文件:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(0, 5))
        input_frame = ttk.Frame(frame)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        self.move_images_list_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.move_images_list_var, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Button(input_frame, text="浏览", command=self.browse_move_images_list).pack(side=tk.RIGHT)
        
        # 输出文件夹
        ttk.Label(frame, text="输出文件夹:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(0, 5))
        output_frame = ttk.Frame(frame)
        output_frame.pack(fill=tk.X, pady=(0, 20))
        self.move_images_output_var = tk.StringVar()
        ttk.Entry(output_frame, textvariable=self.move_images_output_var, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Button(output_frame, text="浏览", command=self.browse_move_images_output).pack(side=tk.RIGHT)
        
        ttk.Button(frame, text="开始移动", command=self.run_move_images_to_folder, style='TButton').pack(anchor=tk.CENTER, pady=20)
        
    def create_fuyangbentxt_function(self):
        """创建负样本txt处理功能界面"""
        frame = self.function_frames["负样本txt"]
        
        note_label = ttk.Label(frame, text="备注：处理负样本txt文件")
        note_label.pack(anchor=tk.W, pady=(0, 15))
        
        # 输入文件夹
        ttk.Label(frame, text="输入文件夹:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(0, 5))
        input_frame = ttk.Frame(frame)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        self.fuyangbentxt_input_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.fuyangbentxt_input_var, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Button(input_frame, text="浏览", command=self.browse_fuyangbentxt_input).pack(side=tk.RIGHT)
        
        # 输出文件夹
        ttk.Label(frame, text="输出文件夹:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(0, 5))
        output_frame = ttk.Frame(frame)
        output_frame.pack(fill=tk.X, pady=(0, 20))
        self.fuyangbentxt_output_var = tk.StringVar()
        ttk.Entry(output_frame, textvariable=self.fuyangbentxt_output_var, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Button(output_frame, text="浏览", command=self.browse_fuyangbentxt_output).pack(side=tk.RIGHT)
        
        ttk.Button(frame, text="开始处理", command=self.run_fuyangbentxt, style='TButton').pack(anchor=tk.CENTER, pady=20)
        
    def create_huafen_function(self):
        """创建数据集划分功能界面"""
        frame = self.function_frames["划分"]
        
        # 功能说明
        note_label = ttk.Label(frame, text="备注：将数据集划分为训练集、验证集和测试集")
        note_label.pack(anchor=tk.W, pady=(0, 15))
        
        # 输入文件夹选择
        ttk.Label(frame, text="输入文件夹:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(0, 5))
        input_frame = ttk.Frame(frame)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        self.huafen_input_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.huafen_input_var, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Button(input_frame, text="浏览", command=self.browse_huafen_input).pack(side=tk.RIGHT)
        
        # 输出文件夹选择
        ttk.Label(frame, text="输出文件夹:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(0, 5))
        output_frame = ttk.Frame(frame)
        output_frame.pack(fill=tk.X, pady=(0, 20))
        self.huafen_output_var = tk.StringVar()
        ttk.Entry(output_frame, textvariable=self.huafen_output_var, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Button(output_frame, text="浏览", command=self.browse_huafen_output).pack(side=tk.RIGHT)
        
        # 留出位置给进度条
        self.huafen_frame = frame
        
        # 执行按钮
        ttk.Button(frame, text="开始划分", command=self.run_huafen, style='TButton').pack(anchor=tk.CENTER, pady=20)
        
    def create_sort_images_by_labels_function(self):
        """创建按标签分类图像功能界面"""
        frame = self.function_frames["按标签分类图像"]
        
        # 功能说明
        note_label = ttk.Label(frame, text="备注：根据标签类别将图片分类到不同文件夹")
        note_label.pack(anchor=tk.W, pady=(0, 15))
        
        # 图片文件夹选择
        ttk.Label(frame, text="图片文件夹:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(0, 5))
        images_frame = ttk.Frame(frame)
        images_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Entry(images_frame, textvariable=self.sort_images_var, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Button(images_frame, text="浏览", command=self.browse_sort_images).pack(side=tk.RIGHT)
        
        # 标签文件夹选择
        ttk.Label(frame, text="标签文件夹:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(0, 5))
        labels_frame = ttk.Frame(frame)
        labels_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Entry(labels_frame, textvariable=self.sort_labels_var, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Button(labels_frame, text="浏览", command=self.browse_sort_labels).pack(side=tk.RIGHT)
        
        # 类别文件选择
        ttk.Label(frame, text="类别文件 (classes.txt):", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(0, 5))
        classes_frame = ttk.Frame(frame)
        classes_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Entry(classes_frame, textvariable=self.sort_classes_var, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Button(classes_frame, text="浏览", command=self.browse_sort_classes).pack(side=tk.RIGHT)
        
        # 输出文件夹选择
        ttk.Label(frame, text="输出文件夹:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(0, 5))
        output_frame = ttk.Frame(frame)
        output_frame.pack(fill=tk.X, pady=(0, 20))
        ttk.Entry(output_frame, textvariable=self.sort_output_var, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Button(output_frame, text="浏览", command=self.browse_sort_output).pack(side=tk.RIGHT)
        
        # 执行按钮
        ttk.Button(frame, text="开始分类", command=self.run_sort_images_by_labels, style='TButton').pack(anchor=tk.CENTER, pady=20)
        
    def create_data_augmentation_function(self):
        """创建数据增强功能界面"""
        frame = self.function_frames["数据增强"]
        
        # 功能说明
        note_label = ttk.Label(frame, text="备注：对图像和标签进行数据增强操作")
        note_label.pack(anchor=tk.W, pady=(0, 15))
        
        # 图像文件夹选择
        ttk.Label(frame, text="图像文件夹:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(0, 5))
        input_frame = ttk.Frame(frame)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        self.augmentation_images_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.augmentation_images_var, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Button(input_frame, text="浏览", command=self.browse_augmentation_images).pack(side=tk.RIGHT)
        
        # 标签文件夹选择
        ttk.Label(frame, text="标签文件夹:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(0, 5))
        labels_frame = ttk.Frame(frame)
        labels_frame.pack(fill=tk.X, pady=(0, 20))
        self.augmentation_labels_var = tk.StringVar()
        ttk.Entry(labels_frame, textvariable=self.augmentation_labels_var, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Button(labels_frame, text="浏览", command=self.browse_augmentation_labels).pack(side=tk.RIGHT)
        
        # 执行按钮
        ttk.Button(frame, text="开始增强", command=self.run_data_augmentation, style='TButton').pack(anchor=tk.CENTER, pady=20)
        
    def create_find_extra_labels_function(self):
        """创建查找多余标签功能界面"""
        frame = self.function_frames["查找多余标签"]
        
        # 功能说明
        note_label = ttk.Label(frame, text="备注：查找没有对应图像文件的标签文件")
        note_label.pack(anchor=tk.W, pady=(0, 15))
        
        # 图像文件夹选择
        ttk.Label(frame, text="图像文件夹:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(0, 5))
        input_frame = ttk.Frame(frame)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        self.extra_images_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.extra_images_var, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Button(input_frame, text="浏览", command=self.browse_extra_images).pack(side=tk.RIGHT)
        
        # 标签文件夹选择
        ttk.Label(frame, text="标签文件夹:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(0, 5))
        labels_frame = ttk.Frame(frame)
        labels_frame.pack(fill=tk.X, pady=(0, 20))
        self.extra_labels_var = tk.StringVar()
        ttk.Entry(labels_frame, textvariable=self.extra_labels_var, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Button(labels_frame, text="浏览", command=self.browse_extra_labels).pack(side=tk.RIGHT)
        
        # 执行按钮
        ttk.Button(frame, text="开始查找", command=self.run_find_extra_labels, style='TButton').pack(anchor=tk.CENTER, pady=20)
        
    # 浏览文件夹函数
    def browse_crop_input(self):
        folder = filedialog.askdirectory()
        if folder:
            self.crop_input_var.set(folder)
    
    def browse_crop_output(self):
        folder = filedialog.askdirectory()
        if folder:
            self.crop_output_var.set(folder)
    

    
    def browse_check_labels(self):
        folder = filedialog.askdirectory()
        if folder:
            self.check_labels_var.set(folder)
    
    def browse_square_labels(self):
        folder = filedialog.askdirectory()
        if folder:
            self.square_labels_var.set(folder)
    
    def browse_square_images(self):
        folder = filedialog.askdirectory()
        if folder:
            self.square_images_var.set(folder)
    
    def browse_find_images(self):
        folder = filedialog.askdirectory()
        if folder:
            self.find_images_var.set(folder)
    
    def browse_find_labels(self):
        folder = filedialog.askdirectory()
        if folder:
            self.find_labels_var.set(folder)
    
    def browse_check_counts(self):
        folder = filedialog.askdirectory()
        if folder:
            self.check_counts_var.set(folder)
    
    def browse_check_count_class(self):
        folder = filedialog.askdirectory()
        if folder:
            self.check_count_class_var.set(folder)
    
    def browse_remove_duplicate(self):
        folder = filedialog.askdirectory()
        if folder:
            self.remove_duplicate_var.set(folder)
    
    def browse_separate_images(self):
        folder = filedialog.askdirectory()
        if folder:
            self.separate_images_var.set(folder)
    
    def browse_separate_labels(self):
        folder = filedialog.askdirectory()
        if folder:
            self.separate_labels_var.set(folder)
    
    def browse_separate_output(self):
        folder = filedialog.askdirectory()
        if folder:
            self.separate_output_var.set(folder)
    
    def browse_voc_input(self):
        folder = filedialog.askdirectory()
        if folder:
            self.voc_input_var.set(folder)
    
    def browse_voc_output(self):
        folder = filedialog.askdirectory()
        if folder:
            self.voc_output_var.set(folder)
    
    def browse_delete_images(self):
        folder = filedialog.askdirectory()
        if folder:
            self.delete_images_var.set(folder)
    
    def browse_delete_labels(self):
        folder = filedialog.askdirectory()
        if folder:
            self.delete_labels_var.set(folder)
    
    def browse_sample_images(self):
        folder = filedialog.askdirectory()
        if folder:
            self.sample_images_var.set(folder)
    
    def browse_sample_output(self):
        folder = filedialog.askdirectory()
        if folder:
            self.sample_output_var.set(folder)
    
    def browse_extract_videos(self):
        folder = filedialog.askdirectory()
        if folder:
            self.extract_videos_var.set(folder)
    
    def browse_extract_output(self):
        folder = filedialog.askdirectory()
        if folder:
            self.extract_output_var.set(folder)
    
    def browse_move_images_list(self):
        file = filedialog.askopenfilename(filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")])
        if file:
            self.move_images_list_var.set(file)
    
    def browse_move_images_output(self):
        folder = filedialog.askdirectory()
        if folder:
            self.move_images_output_var.set(folder)
    
    def browse_fuyangbentxt_input(self):
        folder = filedialog.askdirectory()
        if folder:
            self.fuyangbentxt_input_var.set(folder)
    
    def browse_fuyangbentxt_output(self):
        folder = filedialog.askdirectory()
        if folder:
            self.fuyangbentxt_output_var.set(folder)
    
    def browse_huafen_input(self):
        folder = filedialog.askdirectory()
        if folder:
            self.huafen_input_var.set(folder)
    
    def browse_huafen_output(self):
        folder = filedialog.askdirectory()
        if folder:
            self.huafen_output_var.set(folder)
    
    def browse_sort_images(self):
        folder = filedialog.askdirectory()
        if folder:
            self.sort_images_var.set(folder)
    
    def browse_sort_labels(self):
        folder = filedialog.askdirectory()
        if folder:
            self.sort_labels_var.set(folder)
    
    def browse_sort_classes(self):
        file = filedialog.askopenfilename(filetypes=[("文本文件", "*.txt"), ("所有文件", "*")])
        if file:
            self.sort_classes_var.set(file)
    
    def browse_sort_output(self):
        folder = filedialog.askdirectory()
        if folder:
            self.sort_output_var.set(folder)
    
    def browse_sam_input(self):
        folder = filedialog.askdirectory()
        if folder:
            self.sam_input_var.set(folder)
    
    def browse_sam_output(self):
        folder = filedialog.askdirectory()
        if folder:
            self.sam_output_var.set(folder)
    
    def browse_extreme_area_labels(self):
        folder = filedialog.askdirectory()
        if folder:
            self.extreme_area_labels_var.set(folder)
    
    def browse_extreme_area_images(self):
        folder = filedialog.askdirectory()
        if folder:
            self.extreme_area_images_var.set(folder)
    
    def browse_augmentation_images(self):
        folder = filedialog.askdirectory()
        if folder:
            self.augmentation_images_var.set(folder)
    
    def browse_augmentation_labels(self):
        folder = filedialog.askdirectory()
        if folder:
            self.augmentation_labels_var.set(folder)
    
    def browse_extra_images(self):
        folder = filedialog.askdirectory()
        if folder:
            self.extra_images_var.set(folder)
    
    def browse_extra_labels(self):
        folder = filedialog.askdirectory()
        if folder:
            self.extra_labels_var.set(folder)
    

    
    def browse_distribute_input(self):
        folder = filedialog.askdirectory()
        if folder:
            self.distribute_input_var.set(folder)
    
    def browse_distribute_output(self):
        folder = filedialog.askdirectory()
        if folder:
            self.distribute_output_var.set(folder)
    
    def browse_split_input(self):
        folder = filedialog.askdirectory()
        if folder:
            self.split_input_var.set(folder)
    
    def browse_split_output(self):
        folder = filedialog.askdirectory()
        if folder:
            self.split_output_var.set(folder)
    
    # 执行工具函数
    def run_crop(self):
        input_folder = self.crop_input_var.get()
        output_folder = self.crop_output_var.get()
        
        if not input_folder or not output_folder:
            messagebox.showerror("错误", "请选择输入和输出文件夹")
            return
        
        try:
            # 保存配置
            self.config["crop_input"] = input_folder
            self.config["crop_output"] = output_folder
            self.save_config()
            
            ToolFunctions.crop_images_bottom_half(input_folder, output_folder)
            messagebox.showinfo("成功", "图片裁剪完成！")
        except Exception as e:
            messagebox.showerror("错误", f"裁剪失败：{str(e)}")
    
    def run_split(self):
        input_dir = self.split_input_var.get()
        output_dir = self.split_output_var.get()
        
        if not input_dir or not output_dir:
            messagebox.showerror("错误", "请选择输入和输出文件夹")
            return
        
        try:
            # 保存配置
            self.config["split_input"] = input_dir
            self.config["split_output"] = output_dir
            self.save_config()
            
            # 保存当前目录，以便调用外部脚本
            current_dir = os.getcwd()
            os.chdir(input_dir)
            
            # 调用图片分割功能
            from image_splitter import main
            main()
            
            # 恢复当前目录
            os.chdir(current_dir)
            
            messagebox.showinfo("成功", "图片分割完成！")
        except Exception as e:
            messagebox.showerror("错误", f"分割失败：{str(e)}")
    
    def run_check_labels(self):
        label_dir = self.check_labels_var.get()
        
        if not label_dir:
            messagebox.showerror("错误", "请选择标签文件夹")
            return
        
        try:
            # 保存配置
            self.config["check_labels"] = label_dir
            self.save_config()
            
            ToolFunctions.check_labels(label_dir)
            messagebox.showinfo("成功", "标签检查完成！")
        except Exception as e:
            messagebox.showerror("错误", f"检查失败：{str(e)}")
    
    def run_check_square(self):
        labels_dir = self.square_labels_var.get()
        image_dir = self.square_images_var.get()
        threshold = self.square_threshold_var.get()
        
        if not labels_dir:
            messagebox.showerror("错误", "请选择标签文件夹")
            return
        
        try:
            # 保存配置
            self.config["square_labels"] = labels_dir
            self.config["square_images"] = image_dir
            self.config["square_threshold"] = threshold
            self.save_config()
            
            ToolFunctions.check_square_labels(labels_dir, threshold, image_dir)
            messagebox.showinfo("成功", "正方形标签检查完成！")
        except Exception as e:
            messagebox.showerror("错误", f"检查失败：{str(e)}")
    
    def run_distribute_labels(self):
        num_people = self.distribute_num_var.get()
        input_dir = self.distribute_input_var.get()
        output_dir = self.distribute_output_var.get()
        
        if not input_dir or not output_dir:
            messagebox.showerror("错误", "请选择输入和输出文件夹")
            return
        
        try:
            # 保存配置
            self.config["distribute_num"] = num_people
            self.config["distribute_input"] = input_dir
            self.config["distribute_output"] = output_dir
            self.save_config()
            
            ToolFunctions.distribute_labels(num_people, input_dir, output_dir)
            messagebox.showinfo("成功", "标签分配完成！")
        except Exception as e:
            messagebox.showerror("错误", f"分配失败：{str(e)}")
    
    def run_find_images_without_labels(self):
        image_dir = self.find_images_var.get()
        label_dir = self.find_labels_var.get()
        
        if not image_dir or not label_dir:
            messagebox.showerror("错误", "请选择图像和标签文件夹")
            return
        
        try:
            # 保存配置
            self.config["find_images"] = image_dir
            self.config["find_labels"] = label_dir
            self.save_config()
            
            # 创建进度条
            progress_frame = ttk.Frame(self.function_frames["查找无标签图像"])
            progress_frame.pack(fill=tk.X, padx=20, pady=(10, 20))
            ttk.Label(progress_frame, text="进度: ").pack(side=tk.LEFT)
            progress_var = tk.DoubleVar()
            progress_bar = ttk.Progressbar(progress_frame, variable=progress_var, maximum=100)
            progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
            progress_label = ttk.Label(progress_frame, text="0%")
            progress_label.pack(side=tk.LEFT, padx=5)
            
            # 在后台线程中执行
            import threading
            thread = threading.Thread(target=self._run_find_images_thread, 
                                    args=(image_dir, label_dir, progress_var, progress_label, progress_frame))
            thread.daemon = True
            thread.start()
            
        except Exception as e:
            messagebox.showerror("错误", f"查找失败：{str(e)}")
            
    def _run_find_images_thread(self, image_dir, label_dir, progress_var, progress_label, progress_frame):
        """在后台线程中执行查找无标签图像操作"""
        try:
            # 重定向打印输出到日志文本框
            import sys
            old_stdout = sys.stdout
            
            class RedirectText:
                def __init__(self, text_widget, progress_var, progress_label):
                    self.text_widget = text_widget
                    self.progress_var = progress_var
                    self.progress_label = progress_label
                    self.total_files = 0
                    self.processed_files = 0
                
                def write(self, string):
                    # 在主线程中更新UI
                    self.text_widget.after(0, self._insert_text, string)
                    self.text_widget.after(0, self.text_widget.see, tk.END)
                    
                    # 解析进度信息
                    self._parse_progress(string)
                
                def _insert_text(self, string):
                    self.text_widget.config(state=tk.NORMAL)
                    self.text_widget.insert(tk.END, string)
                    self.text_widget.config(state=tk.DISABLED)
                
                def _parse_progress(self, string):
                    # 提取总文件数
                    if "总共找到" in string and "个图像文件" in string:
                        try:
                            self.total_files = int(string.split("总共找到")[1].split("个图像文件")[0].strip())
                            self.processed_files = 0
                            self.progress_var.set(0)
                            self.text_widget.after(0, lambda: self.progress_label.config(text="0%"))
                        except:
                            pass
                    
                    # 提取已处理文件数
                    if "已处理" in string and "个文件" in string:
                        try:
                            count = int(string.split("已处理")[1].split("个文件")[0].strip())
                            self.processed_files = count
                            if self.total_files > 0:
                                progress = (self.processed_files / self.total_files) * 100
                                if count >= self.total_files:
                                    progress = 100
                                progress_percent = f"{int(progress)}%"
                                self.text_widget.after(0, lambda: self.progress_var.set(min(progress, 100)))
                                self.text_widget.after(0, lambda: self.progress_label.config(text=progress_percent))
                        except:
                            pass
                    
                    # 检测完成状态
                    if "查找完成" in string or "无标签图像查找已完成" in string:
                        self.text_widget.after(0, lambda: self.progress_var.set(100))
                        self.text_widget.after(0, lambda: self.progress_label.config(text="100%"))
                
                def flush(self):
                    pass
            
            # 创建重定向对象
            sys.stdout = RedirectText(self.log_text, progress_var, progress_label)
            
            # 执行查找操作
            ToolFunctions.find_images_without_labels(image_dir, label_dir)
            
            # 恢复标准输出
            sys.stdout = old_stdout
            
            # 在主线程中显示完成消息
            def show_complete():
                # 不再销毁进度条，使其在完成后仍然可见
                messagebox.showinfo("成功", "查找完成！")
            
            self.root.after(0, show_complete)
            
        except Exception as e:
            # 恢复标准输出
            sys.stdout = old_stdout
            
            # 在主线程中显示错误消息
            def show_error():
                # 不再销毁进度条，使其在出错后仍然可见
                messagebox.showerror("错误", f"查找失败：{str(e)}")
            
            self.root.after(0, show_error)
    
    def run_check_label_counts(self):
        label_dir = self.check_counts_var.get()
        threshold = self.check_counts_threshold_var.get()
        
        if not label_dir:
            messagebox.showerror("错误", "请选择标签文件夹")
            return
        
        if not threshold.isdigit():
            messagebox.showerror("错误", "阈值必须是数字")
            return
        
        threshold = int(threshold)
        
        try:
            # 保存配置
            self.config["check_counts"] = label_dir
            self.config["check_counts_threshold"] = str(threshold)
            self.save_config()
            
            ToolFunctions.check_label_counts(label_dir, threshold)
            messagebox.showinfo("成功", "标签数量检查完成！")
        except Exception as e:
            messagebox.showerror("错误", f"检查失败：{str(e)}")
    
    def run_check_label_count_class(self):
        label_dir = self.check_count_class_var.get()
        output_file = self.check_count_class_output_var.get()
        
        if not label_dir:
            messagebox.showerror("错误", "请选择标签文件夹")
            return
        
        try:
            # 保存配置
            self.config["check_count_class"] = label_dir
            self.config["check_count_class_output"] = output_file
            self.save_config()
            
            ToolFunctions.check_label_count_class(label_dir, output_file)
            messagebox.showinfo("成功", "标签和类别检查完成！")
        except Exception as e:
            messagebox.showerror("错误", f"检查失败：{str(e)}")
    
    def run_data_augmentation(self):
        image_dir = self.augmentation_images_var.get()
        label_dir = self.augmentation_labels_var.get()
        
        if not image_dir or not label_dir:
            messagebox.showerror("错误", "请选择图像和标签文件夹")
            return
        
        try:
            # 保存配置
            self.config["augmentation_images"] = image_dir
            self.config["augmentation_labels"] = label_dir
            self.save_config()
            
            ToolFunctions.data_augmentation(image_dir, label_dir)
            messagebox.showinfo("成功", "数据增强完成！")
        except Exception as e:
            messagebox.showerror("错误", f"增强失败：{str(e)}")
    
    def run_find_extra_labels(self):
        image_dir = self.extra_images_var.get()
        label_dir = self.extra_labels_var.get()
        
        if not image_dir or not label_dir:
            messagebox.showerror("错误", "请选择图像和标签文件夹")
            return
        
        try:
            # 保存配置
            self.config["extra_images"] = image_dir
            self.config["extra_labels"] = label_dir
            self.save_config()
            
            # 创建进度条
            progress_frame = ttk.Frame(self.function_frames["查找多余标签"])
            progress_frame.pack(fill=tk.X, padx=20, pady=(10, 20))
            ttk.Label(progress_frame, text="进度: ").pack(side=tk.LEFT)
            progress_var = tk.DoubleVar()
            progress_bar = ttk.Progressbar(progress_frame, variable=progress_var, maximum=100)
            progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
            progress_label = ttk.Label(progress_frame, text="0%")
            progress_label.pack(side=tk.LEFT, padx=5)
            
            # 在后台线程中执行
            import threading
            thread = threading.Thread(target=self._run_find_extra_thread, 
                                    args=(image_dir, label_dir, progress_var, progress_label, progress_frame))
            thread.daemon = True
            thread.start()
            
        except Exception as e:
            messagebox.showerror("错误", f"查找失败：{str(e)}")
            
    def _run_find_extra_thread(self, image_dir, label_dir, progress_var, progress_label, progress_frame):
        """在后台线程中执行查找多余标签操作"""
        try:
            # 重定向打印输出到日志文本框
            import sys
            old_stdout = sys.stdout
            
            class RedirectText:
                def __init__(self, text_widget, progress_var, progress_label):
                    self.text_widget = text_widget
                    self.progress_var = progress_var
                    self.progress_label = progress_label
                    self.total_files = 0
                    self.processed_files = 0
                
                def write(self, string):
                    # 在主线程中更新UI
                    self.text_widget.after(0, self._insert_text, string)
                    self.text_widget.after(0, self.text_widget.see, tk.END)
                    
                    # 解析进度信息
                    self._parse_progress(string)
                
                def _insert_text(self, string):
                    self.text_widget.config(state=tk.NORMAL)
                    self.text_widget.insert(tk.END, string)
                    self.text_widget.config(state=tk.DISABLED)
                
                def _parse_progress(self, string):
                    # 提取总文件数
                    if "总共找到" in string and "个标签文件" in string:
                        try:
                            self.total_files = int(string.split("总共找到")[1].split("个标签文件")[0].strip())
                            self.processed_files = 0
                            self.progress_var.set(0)
                            self.text_widget.after(0, lambda: self.progress_label.config(text="0%"))
                        except:
                            pass
                    
                    # 提取已处理文件数
                    if "已处理" in string and "个文件" in string:
                        try:
                            count = int(string.split("已处理")[1].split("个文件")[0].strip())
                            self.processed_files = count
                            if self.total_files > 0:
                                progress = (self.processed_files / self.total_files) * 100
                                if count >= self.total_files:
                                    progress = 100
                                progress_percent = f"{int(progress)}%"
                                self.text_widget.after(0, lambda: self.progress_var.set(min(progress, 100)))
                                self.text_widget.after(0, lambda: self.progress_label.config(text=progress_percent))
                        except:
                            pass
                    
                    # 检测完成状态
                    if "查找完成" in string or "多余标签查找已完成" in string:
                        self.text_widget.after(0, lambda: self.progress_var.set(100))
                        self.text_widget.after(0, lambda: self.progress_label.config(text="100%"))
                
                def flush(self):
                    pass
            
            # 创建重定向对象
            sys.stdout = RedirectText(self.log_text, progress_var, progress_label)
            
            # 执行查找操作
            ToolFunctions.find_extra_labels(image_dir, label_dir)
            
            # 恢复标准输出
            sys.stdout = old_stdout
            
            # 在主线程中显示完成消息
            def show_complete():
                # 不再销毁进度条，使其在完成后仍然可见
                messagebox.showinfo("成功", "查找完成！")
            
            self.root.after(0, show_complete)
            
        except Exception as e:
            # 恢复标准输出
            sys.stdout = old_stdout
            
            # 在主线程中显示错误消息
            def show_error():
                # 不再销毁进度条，使其在出错后仍然可见
                messagebox.showerror("错误", f"查找失败：{str(e)}")
            
            self.root.after(0, show_error)
    
    def run_remove_duplicate_images(self):
        image_dir = self.remove_duplicate_var.get()
        
        if not image_dir:
            messagebox.showerror("错误", "请选择图像文件夹")
            return
        
        try:
            # 保存配置
            self.config["remove_duplicate"] = image_dir
            self.save_config()
            
            ToolFunctions.remove_duplicate_images(image_dir)
            messagebox.showinfo("成功", "移除完成！")
        except Exception as e:
            messagebox.showerror("错误", f"移除失败：{str(e)}")
    
    def run_separate_images_by_labels(self):
        image_dir = self.separate_images_var.get()
        label_dir = self.separate_labels_var.get()
        output_dir = self.separate_output_var.get()
        
        if not image_dir or not label_dir or not output_dir:
            messagebox.showerror("错误", "请选择图像文件夹、标签文件夹和输出文件夹")
            return
        
        try:
            # 保存配置
            self.config["separate_images"] = image_dir
            self.config["separate_labels"] = label_dir
            self.config["separate_output"] = output_dir
            self.save_config()
            
            # 创建进度条
            progress_frame = ttk.Frame(self.function_frames["按标签分离图像"])
            progress_frame.pack(fill=tk.X, padx=20, pady=(10, 20))
            ttk.Label(progress_frame, text="进度: ").pack(side=tk.LEFT)
            progress_var = tk.DoubleVar()
            progress_bar = ttk.Progressbar(progress_frame, variable=progress_var, maximum=100)
            progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
            progress_label = ttk.Label(progress_frame, text="0%")
            progress_label.pack(side=tk.LEFT, padx=5)
            
            # 在后台线程中执行
            import threading
            thread = threading.Thread(target=self._run_separate_thread, 
                                    args=(image_dir, label_dir, output_dir, progress_var, progress_label, progress_frame))
            thread.daemon = True
            thread.start()
            
        except Exception as e:
            messagebox.showerror("错误", f"分离失败：{str(e)}")
    

            
    def _run_separate_thread(self, image_dir, label_dir, output_dir, progress_var, progress_label, progress_frame):
        """在后台线程中执行按标签分离图像操作"""
        try:
            # 重定向打印输出到日志文本框
            import sys
            old_stdout = sys.stdout
            
            class RedirectText:
                def __init__(self, text_widget, progress_var, progress_label):
                    self.text_widget = text_widget
                    self.progress_var = progress_var
                    self.progress_label = progress_label
                    self.total_files = 0
                    self.processed_files = 0
                
                def write(self, string):
                    # 在主线程中更新UI
                    self.text_widget.after(0, self._insert_text, string)
                    self.text_widget.after(0, self.text_widget.see, tk.END)
                    
                    # 解析进度信息
                    self._parse_progress(string)
                
                def _insert_text(self, string):
                    self.text_widget.config(state=tk.NORMAL)
                    self.text_widget.insert(tk.END, string)
                    self.text_widget.config(state=tk.DISABLED)
                
                def _parse_progress(self, string):
                    # 提取总文件数 (例如: "总共找到 100 个图像文件")
                    if "总共找到" in string and "个图像文件" in string:
                        try:
                            self.total_files = int(string.split("总共找到")[1].split("个图像文件")[0].strip())
                            self.processed_files = 0
                            self.progress_var.set(0)
                            self.text_widget.after(0, lambda: self.progress_label.config(text="0%"))
                        except:
                            pass
                    
                    # 提取已处理文件数 (例如: "已处理 10 个文件...")
                    if "已处理" in string and "个文件" in string:
                        try:
                            count = int(string.split("已处理")[1].split("个文件")[0].strip())
                            self.processed_files = count
                            if self.total_files > 0:
                                progress = (self.processed_files / self.total_files) * 100
                                # 确保在最后一步时进度显示为100%
                                if count >= self.total_files:
                                    progress = 100
                                progress_percent = f"{int(progress)}%"
                                self.text_widget.after(0, lambda: self.progress_var.set(min(progress, 100)))
                                self.text_widget.after(0, lambda: self.progress_label.config(text=progress_percent))
                        except:
                            pass
                    
                    # 检测完成状态
                    if "分离完成" in string or "图像分离已完成" in string:
                        # 操作完成时强制设置进度为100%
                        self.text_widget.after(0, lambda: self.progress_var.set(100))
                        self.text_widget.after(0, lambda: self.progress_label.config(text="100%"))
                
                def flush(self):
                    pass
            
            # 创建重定向对象
            sys.stdout = RedirectText(self.log_text, progress_var, progress_label)
            
            # 执行分离操作
            ToolFunctions.separate_images_by_labels(image_dir, label_dir, output_dir)
            
            # 恢复标准输出
            sys.stdout = old_stdout
            
            # 在主线程中显示完成消息
            def show_complete():
                # 不再销毁进度条，使其在完成后仍然可见
                messagebox.showinfo("成功", "分离完成！")
            
            self.root.after(0, show_complete)
            
        except Exception as e:
            # 恢复标准输出
            sys.stdout = old_stdout
            
            # 在主线程中显示错误消息
            def show_error():
                # 不再销毁进度条，使其在出错后仍然可见
                messagebox.showerror("错误", f"分离失败：{str(e)}")
            
            self.root.after(0, show_error)
    
    def run_voc_to_yolo(self):
        """运行VOC转YOLO格式转换"""
        voc_dir = self.voc_input_var.get()
        yolo_dir = self.voc_output_var.get()
        
        if not voc_dir or not yolo_dir:
            messagebox.showerror("错误", "请选择VOC文件夹和YOLO输出文件夹")
            return
        
        try:
            # 保存配置
            self.config["voc_input"] = voc_dir
            self.config["voc_output"] = yolo_dir
            self.save_config()
            
            # 清空输出日志
            self.log_text.delete(1.0, tk.END)
            self.log_text.insert(tk.END, "开始VOC转YOLO格式转换...\n")
            
            # 执行转换操作
            ToolFunctions.voc_to_yolo(voc_dir, yolo_dir)
            
            # 显示完成消息
            messagebox.showinfo("成功", "VOC转YOLO格式转换完成！")
            
        except Exception as e:
            messagebox.showerror("错误", f"VOC转YOLO格式转换失败：{str(e)}")
    
    def run_delete_images_without_labels(self):
        image_dir = self.delete_images_var.get()
        label_dir = self.delete_labels_var.get()
        
        if not image_dir or not label_dir:
            messagebox.showerror("错误", "请选择图像和标签文件夹")
            return
        
        try:
            # 保存配置
            self.config["delete_images"] = image_dir
            self.config["delete_labels"] = label_dir
            self.save_config()
            
            # 创建进度条
            progress_frame = ttk.Frame(self.function_frames["删除无标签图像"])
            progress_frame.pack(fill=tk.X, padx=20, pady=(10, 20))
            ttk.Label(progress_frame, text="进度: ").pack(side=tk.LEFT)
            progress_var = tk.DoubleVar()
            progress_bar = ttk.Progressbar(progress_frame, variable=progress_var, maximum=100)
            progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
            progress_label = ttk.Label(progress_frame, text="0%")
            progress_label.pack(side=tk.LEFT, padx=5)
            
            # 在后台线程中执行
            import threading
            thread = threading.Thread(target=self._run_delete_images_thread, 
                                    args=(image_dir, label_dir, progress_var, progress_label, progress_frame))
            thread.daemon = True
            thread.start()
            
        except Exception as e:
            messagebox.showerror("错误", f"删除失败：{str(e)}")
    
    def _run_delete_images_thread(self, image_dir, label_dir, progress_var, progress_label, progress_frame):
        """在后台线程中执行删除无标签图像操作"""
        try:
            # 重定向打印输出到日志文本框
            import sys
            old_stdout = sys.stdout
            
            class RedirectText:
                def __init__(self, text_widget, progress_var, progress_label):
                    self.text_widget = text_widget
                    self.progress_var = progress_var
                    self.progress_label = progress_label
                    self.total_files = 0
                    self.processed_files = 0
                
                def write(self, string):
                    # 将输出添加到日志文本框
                    self.text_widget.configure(state="normal")
                    self.text_widget.insert(tk.END, string)
                    self.text_widget.see(tk.END)
                    self.text_widget.configure(state="disabled")
                    
                    # 解析进度信息
                    self._parse_progress(string)
                
                def flush(self):
                    pass
                
                def _parse_progress(self, string):
                    # 解析总文件数
                    if "总共找到" in string and "个图像文件" in string:
                        try:
                            # 提取数字
                            start = string.find("总共找到") + 4
                            end = string.find("个图像文件")
                            self.total_files = int(string[start:end].strip())
                        except:
                            pass
                    
                    # 解析已处理文件数
                    if "已处理" in string and "个文件" in string and "进度:" in string:
                        try:
                            # 提取已处理文件数
                            start = string.find("已处理") + 3
                            end = string.find("个文件")
                            self.processed_files = int(string[start:end].strip())
                            
                            # 提取进度百分比
                            start_p = string.find("进度:") + 3
                            end_p = string.find("%", start_p)
                            progress = float(string[start_p:end_p].strip())
                            
                            # 更新进度条
                            progress_var.set(progress)
                            progress_label.config(text=f"{int(progress)}%")
                        except:
                            # 如果无法提取百分比，尝试计算
                            if self.total_files > 0:
                                progress = (self.processed_files / self.total_files) * 100
                                progress_var.set(progress)
                                progress_label.config(text=f"{int(progress)}%")
                    
                    # 检查是否完成
                    if "删除完成！" in string or "处理完成" in string:
                        # 强制设置进度为100%
                        progress_var.set(100)
                        progress_label.config(text="100%")
            
            # 创建重定向对象
            sys.stdout = RedirectText(self.log_text, progress_var, progress_label)
            
            # 执行删除操作
            ToolFunctions.delete_images_without_labels(image_dir, label_dir)
            
            # 恢复标准输出
            sys.stdout = old_stdout
            
            # 在主线程中显示完成消息
            self.root.after(0, lambda: messagebox.showinfo("成功", "删除完成！"))
            
        except Exception as e:
            # 在主线程中显示错误消息
            self.root.after(0, lambda: messagebox.showerror("错误", f"删除失败：{str(e)}"))
        finally:
            # 恢复标准输出
            sys.stdout = old_stdout
    
    def run_sample_images_by_timestamp(self):
        """按时间戳采样图像"""
        image_dir = self.sample_images_var.get()
        output_dir = self.sample_output_var.get()
        sample_count = self.sample_count_var.get()
        
        if not image_dir or not output_dir:
            messagebox.showerror("错误", "请选择图像文件夹和输出文件夹")
            return
        
        try:
            # 保存配置
            self.config["sample_images"] = image_dir
            self.config["sample_output"] = output_dir
            self.config["sample_count"] = sample_count
            self.save_config()
            
            # 清空输出日志
            self.log_text.delete(1.0, tk.END)
            self.log_text.insert(tk.END, f"开始按时间戳采样图像，采样数量：{sample_count}...\n")
            
            # 执行采样操作
            ToolFunctions.sample_images_by_timestamp(image_dir, output_dir, sample_count)
            
            # 显示完成消息
            messagebox.showinfo("成功", f"按时间戳采样完成！采样数量：{sample_count}")
            
        except Exception as e:
            messagebox.showerror("错误", f"按时间戳采样失败：{str(e)}")
    
    def run_extract_frames_from_videos(self):
        """从视频中提取帧"""
        video_dir = self.extract_videos_var.get()
        output_dir = self.extract_output_var.get()
        interval = self.extract_interval_var.get()
        crop = self.extract_crop_var.get()
        
        if not video_dir or not output_dir:
            messagebox.showerror("错误", "请选择视频文件夹和输出文件夹")
            return
        
        try:
            # 保存配置
            self.config["extract_videos"] = video_dir
            self.config["extract_output"] = output_dir
            self.config["extract_interval"] = interval
            self.config["extract_crop"] = crop
            self.save_config()
            
            # 清空输出日志
            self.log_text.delete(1.0, tk.END)
            self.log_text.insert(tk.END, f"开始从视频中提取帧，间隔：{interval}帧，裁剪：{'是' if crop else '否'}...\n")
            
            # 调用提取帧功能，传递裁剪参数
            from extract_frames_from_videos import extract_frames_from_videos
            processed_videos, total_frames = extract_frames_from_videos(video_dir, output_dir, interval, crop=crop)
            
            # 显示完成消息
            messagebox.showinfo("成功", f"视频帧提取完成！处理了{processed_videos}个视频，提取了{total_frames}帧")
            
        except Exception as e:
            messagebox.showerror("错误", f"视频帧提取失败：{str(e)}")
    
    def run_move_images_to_folder(self):
        """根据图像列表移动图像到文件夹"""
        image_list = self.move_images_list_var.get()
        output_dir = self.move_images_output_var.get()
        
        if not image_list or not output_dir:
            messagebox.showerror("错误", "请选择图像列表文件和输出文件夹")
            return
        
        try:
            # 保存配置
            self.config["move_images_list"] = image_list
            self.config["move_images_output"] = output_dir
            self.save_config()
            
            # 清空输出日志
            self.log_text.delete(1.0, tk.END)
            self.log_text.insert(tk.END, "开始根据图像列表移动图像...\n")
            
            # 执行移动操作
            ToolFunctions.move_images_to_folder(image_list, output_dir)
            
            # 显示完成消息
            messagebox.showinfo("成功", "图像移动完成！")
            
        except Exception as e:
            messagebox.showerror("错误", f"图像移动失败：{str(e)}")
    
    def run_fuyangbentxt(self):
        """复制样本txt文件"""
        input_dir = self.fuyangbentxt_input_var.get()
        output_dir = self.fuyangbentxt_output_var.get()
        
        if not input_dir or not output_dir:
            messagebox.showerror("错误", "请选择输入和输出文件夹")
            return
        
        try:
            # 保存配置
            self.config["fuyangbentxt_input"] = input_dir
            self.config["fuyangbentxt_output"] = output_dir
            self.save_config()
            
            # 清空输出日志
            self.log_text.delete(1.0, tk.END)
            self.log_text.insert(tk.END, "开始复制样本txt文件...\n")
            
            # 执行复制操作
            ToolFunctions.fuyangbentxt(input_dir, output_dir)
            
            # 显示完成消息
            messagebox.showinfo("成功", "样本txt文件复制完成！")
            
        except Exception as e:
            messagebox.showerror("错误", f"样本txt文件复制失败：{str(e)}")
    
    def run_huafen(self):
        """划分数据集"""
        input_dir = self.huafen_input_var.get()
        output_dir = self.huafen_output_var.get()
        
        if not input_dir or not output_dir:
            messagebox.showerror("错误", "请选择输入和输出文件夹")
            return
        
        try:
            # 保存配置
            self.config["huafen_input"] = input_dir
            self.config["huafen_output"] = output_dir
            self.save_config()
            
            # 清空输出日志
            self.log_text.delete(1.0, tk.END)
            self.log_text.insert(tk.END, "开始划分数据集...\n")
            
            # 创建进度条（与其他功能保持一致）
            if hasattr(self, 'huafen_progress_frame'):
                self.huafen_progress_frame.destroy()
            
            # 创建进度条框架
            self.huafen_progress_frame = ttk.Frame(self.huafen_frame)
            self.huafen_progress_frame.pack(fill=tk.X, padx=20, pady=(10, 20))
            
            # 进度条组件
            ttk.Label(self.huafen_progress_frame, text="进度: ").pack(side=tk.LEFT)
            self.huafen_progress_var = tk.DoubleVar()
            self.huafen_progress_bar = ttk.Progressbar(self.huafen_progress_frame, variable=self.huafen_progress_var, maximum=100)
            self.huafen_progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
            self.huafen_progress_label = ttk.Label(self.huafen_progress_frame, text="0%")
            self.huafen_progress_label.pack(side=tk.LEFT, padx=5)
            
            # 使用多线程执行划分操作
            import threading
            thread = threading.Thread(target=self._run_huafen_thread, args=(input_dir, output_dir))
            thread.daemon = True  # 设置为守护线程，主线程结束时自动终止
            thread.start()
            
        except Exception as e:
            messagebox.showerror("错误", f"数据集划分启动失败：{str(e)}")
    
    def _run_huafen_thread(self, input_dir, output_dir):
        """在后台线程中执行数据集划分操作"""
        try:
            # 重定向打印输出到日志文本框
            import sys
            old_stdout = sys.stdout
            
            class RedirectText:
                def __init__(self, text_widget, progress_var, progress_label):
                    self.text_widget = text_widget
                    self.progress_var = progress_var
                    self.progress_label = progress_label
                    self.total_files = 0
                    self.processed_files = 0
                
                def write(self, string):
                    # 在主线程中更新UI
                    self.text_widget.after(0, self._insert_text, string)
                    self.text_widget.after(0, self.text_widget.see, tk.END)
                    
                    # 解析进度信息
                    self._parse_progress(string)
                
                def _insert_text(self, string):
                    self.text_widget.config(state=tk.NORMAL)
                    self.text_widget.insert(tk.END, string)
                    self.text_widget.config(state=tk.DISABLED)
                
                def _parse_progress(self, string):
                    # 提取总文件数 (例如: "总共找到 5606 个图片文件")
                    if "总共找到" in string and "个图片文件" in string:
                        try:
                            self.total_files = int(string.split("总共找到")[1].split("个图片文件")[0].strip())
                            self.processed_files = 0
                            self.progress_var.set(0)
                            self.text_widget.after(0, lambda: self.progress_label.config(text="0%"))
                        except:
                            pass
                    
                    # 提取已处理文件数 (例如: "已处理 10 个文件...")
                    if "已处理" in string and "个文件" in string:
                        try:
                            count = int(string.split("已处理")[1].split("个文件")[0].strip())
                            self.processed_files = count
                            if self.total_files > 0:
                                progress = (self.processed_files / self.total_files) * 100
                                # 确保在最后一步时进度显示为100%
                                if count >= self.total_files:
                                    progress = 100
                                progress_percent = f"{int(progress)}%"
                                self.text_widget.after(0, lambda: self.progress_var.set(min(progress, 100)))
                                self.text_widget.after(0, lambda: self.progress_label.config(text=progress_percent))
                        except:
                            pass
                    
                    # 检测完成状态
                    if "划分完成" in string or "数据集划分已完成" in string:
                        # 操作完成时强制设置进度为100%
                        self.text_widget.after(0, lambda: self.progress_var.set(100))
                        self.text_widget.after(0, lambda: self.progress_label.config(text="100%"))
                
                def flush(self):
                    pass
            
            # 创建重定向对象
            sys.stdout = RedirectText(self.log_text, self.huafen_progress_var, self.huafen_progress_label)
            
            # 执行划分操作
            ToolFunctions.huafen(input_dir, output_dir)
            
            # 恢复标准输出
            sys.stdout = old_stdout
            
            # 在主线程中显示完成消息
            def show_complete():
                messagebox.showinfo("成功", "数据集划分完成！")
            
            self.root.after(0, show_complete)
            
        except Exception as e:
            # 恢复标准输出
            sys.stdout = old_stdout
            
            # 在主线程中显示错误消息
            def show_error():
                messagebox.showerror("错误", f"数据集划分失败：{str(e)}")
            
            self.root.after(0, show_error)
    
    def run_sam_to_yolo(self):
        """将xanylableing的sam标签转换为YOLO格式"""
        input_dir = self.sam_input_var.get()
        output_dir = self.sam_output_var.get()
        
        if not input_dir or not output_dir:
            messagebox.showerror("错误", "请选择输入文件夹和输出文件夹")
            return
        
        try:
            # 保存配置
            self.config["sam_input"] = input_dir
            self.config["sam_output"] = output_dir
            self.save_config()
            
            # 清空输出日志
            self.log_text.delete(1.0, tk.END)
            self.log_text.insert(tk.END, "开始SAM标签转YOLO...\n")
            
            # 执行转换操作
            ToolFunctions.sam_to_yolo(input_dir, output_dir)
            
            # 显示完成消息
            messagebox.showinfo("成功", "SAM标签转YOLO完成！")
            
        except Exception as e:
            messagebox.showerror("错误", f"转换失败：{str(e)}")
    
    def run_find_extreme_area_labels(self):
        """找出标签面积中位数及极端面积标签"""
        label_dir = self.extreme_area_labels_var.get()
        image_dir = self.extreme_area_images_var.get()
        above_percent = self.extreme_area_above_var.get()
        below_percent = self.extreme_area_below_var.get()
        
        if not label_dir or not image_dir:
            messagebox.showerror("错误", "请选择标签文件夹和图像文件夹")
            return
        
        if not above_percent.isdigit():
            messagebox.showerror("错误", "大于中位数百分比必须是数字")
            return
        
        if not below_percent.isdigit():
            messagebox.showerror("错误", "小于中位数百分比必须是数字")
            return
        
        above_percent = int(above_percent)
        below_percent = int(below_percent)
        
        try:
            # 保存配置
            self.config["extreme_area_labels"] = label_dir
            self.config["extreme_area_images"] = image_dir
            self.config["extreme_area_above"] = str(above_percent)
            self.config["extreme_area_below"] = str(below_percent)
            self.save_config()
            
            # 清空输出日志
            self.log_text.delete(1.0, tk.END)
            self.log_text.insert(tk.END, "开始分析标签面积极端值...\n")
            
            # 执行分析操作
            ToolFunctions.find_extreme_area_labels(label_dir, image_dir, above_percent, below_percent)
            
            # 显示完成消息
            messagebox.showinfo("成功", "标签面积极端值分析完成！")
            
        except Exception as e:
            messagebox.showerror("错误", f"分析失败：{str(e)}")
    
    def run_sort_images_by_labels(self):
        """根据标签类别将图片分类到不同文件夹"""
        image_dir = self.sort_images_var.get()
        label_dir = self.sort_labels_var.get()
        classes_file = self.sort_classes_var.get()
        output_dir = self.sort_output_var.get()
        
        if not image_dir or not label_dir or not classes_file or not output_dir:
            messagebox.showerror("错误", "请选择图片文件夹、标签文件夹、类别文件和输出文件夹")
            return
        
        try:
            # 保存配置
            self.config["sort_images"] = image_dir
            self.config["sort_labels"] = label_dir
            self.config["sort_classes"] = classes_file
            self.config["sort_output"] = output_dir
            self.save_config()
            
            # 清空输出日志
            self.log_text.delete(1.0, tk.END)
            self.log_text.insert(tk.END, "开始按标签分类图像...\n")
            
            # 执行分类操作
            ToolFunctions.sort_images_by_labels(image_dir, label_dir, classes_file, output_dir)
            
            # 显示完成消息
            messagebox.showinfo("成功", "图像分类完成！")
            
        except Exception as e:
            messagebox.showerror("错误", f"分类失败：{str(e)}")

# 主函数
if __name__ == "__main__":
    root = tk.Tk()
    app = YoloLabelToolsApp(root)
    root.mainloop()