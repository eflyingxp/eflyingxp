#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from datetime import datetime
import threading

# 检查是否已安装必要的库，如果没有则提示安装
try:
    # 先尝试导入pandas
    import pandas as pd
except ImportError as e:
    error_message = f"错误: 缺少pandas库\n\n"
    error_message += "请安装以下依赖:\n"
    error_message += "pip install pandas openpyxl\n\n"
    error_message += "或者使用提供的启动脚本自动安装依赖。"
    print(error_message)
    sys.exit(1)

# 尝试导入tkinter
try:
    import tkinter as tk
    from tkinter import filedialog, messagebox, ttk
except ImportError as e:
    error_message = f"错误: 无法导入tkinter模块\n\n"
    error_message += "tkinter是Python的标准GUI库，但在某些系统上需要单独安装。\n"
    error_message += "在macOS上，您可能需要安装Python的Tk支持:\n"
    error_message += "  brew install python-tk\n\n"
    error_message += "在Linux上，您可以使用:\n"
    error_message += "  sudo apt-get install python3-tk (Ubuntu/Debian)\n"
    error_message += "  sudo dnf install python3-tkinter (Fedora)\n\n"
    error_message += "安装后重新运行程序。"
    print(error_message)
    sys.exit(1)

# 尝试导入moviepy
try:
    # 直接尝试导入VideoFileClip，这是我们实际需要的类
    try:
        from moviepy.editor import VideoFileClip
    except ImportError:
        # 如果从editor导入失败，尝试其他可能的导入路径
        try:
            from moviepy.video.io.VideoFileClip import VideoFileClip
        except ImportError:
            # 最后尝试直接从moviepy导入
            try:
                import moviepy
                if hasattr(moviepy, 'VideoFileClip'):
                    from moviepy import VideoFileClip
                else:
                    raise ImportError("无法在moviepy中找到VideoFileClip类")
            except ImportError as e:
                error_message = f"错误: 无法导入VideoFileClip类\n\n"
                error_message += "请安装moviepy库:\n"
                error_message += "pip install moviepy==1.0.3\n\n"  # 指定一个稳定版本
                error_message += "或者使用提供的启动脚本自动安装依赖。"
                print(error_message)
                sys.exit(1)
except Exception as e:
    error_message = f"错误: 导入moviepy时出现未知错误: {str(e)}\n\n"
    error_message += "请尝试重新安装moviepy库:\n"
    error_message += "pip uninstall -y moviepy && pip install moviepy==1.0.3\n\n"
    error_message += "或者使用提供的启动脚本自动安装依赖。"
    print(error_message)
    sys.exit(1)

class VideoDurationAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("视频时长统计工具")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # 设置样式
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 12))
        self.style.configure("TLabel", font=("Arial", 12))
        
        # 创建主框架
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 文件夹选择区域
        folder_frame = ttk.Frame(main_frame)
        folder_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(folder_frame, text="选择文件夹:").pack(side=tk.LEFT, padx=5)
        
        self.folder_path = tk.StringVar()
        folder_entry = ttk.Entry(folder_frame, textvariable=self.folder_path, width=50)
        folder_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        browse_btn = ttk.Button(folder_frame, text="浏览...", command=self.browse_folder)
        browse_btn.pack(side=tk.LEFT, padx=5)
        
        # 视频扩展名选择区域
        ext_frame = ttk.Frame(main_frame)
        ext_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(ext_frame, text="视频扩展名 (用逗号分隔):").pack(side=tk.LEFT, padx=5)
        
        self.extensions = tk.StringVar(value=".mp4,.avi,.mov,.mkv,.wmv,.flv")
        ext_entry = ttk.Entry(ext_frame, textvariable=self.extensions, width=50)
        ext_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # 过滤选项区域
        filter_frame = ttk.Frame(main_frame)
        filter_frame.pack(fill=tk.X, pady=10)
        
        # 过滤0时长视频选项
        self.filter_zero_duration = tk.BooleanVar(value=True)
        ttk.Checkbutton(filter_frame, text="过滤0时长视频", variable=self.filter_zero_duration).pack(side=tk.LEFT, padx=5)
        
        # 过滤下划线开头的文件选项
        self.filter_underscore_files = tk.BooleanVar(value=True)
        ttk.Checkbutton(filter_frame, text="过滤下划线开头的文件", variable=self.filter_underscore_files).pack(side=tk.LEFT, padx=5)
        
        # 按钮区域
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        analyze_btn = ttk.Button(btn_frame, text="分析视频", command=self.start_analysis)
        analyze_btn.pack(side=tk.LEFT, padx=5)
        
        export_btn = ttk.Button(btn_frame, text="导出Excel", command=self.export_excel)
        export_btn.pack(side=tk.LEFT, padx=5)
        
        # 进度条
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, pady=10)
        
        self.status_var = tk.StringVar(value="就绪")
        status_label = ttk.Label(main_frame, textvariable=self.status_var)
        status_label.pack(anchor=tk.W, pady=5)
        
        # 结果显示区域
        result_frame = ttk.Frame(main_frame)
        result_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # 创建表格
        columns = ("文件名", "路径", "时长(分钟)")
        self.tree = ttk.Treeview(result_frame, columns=columns, show="headings")
        
        # 设置列标题
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        # 设置列宽
        self.tree.column("文件名", width=150)
        self.tree.column("路径", width=350)
        self.tree.column("时长(分钟)", width=100)
        
        # 添加滚动条
        scrollbar_y = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_y.set)
        
        scrollbar_x = ttk.Scrollbar(result_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscrollcommand=scrollbar_x.set)
        
        # 放置表格和滚动条
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 初始化数据
        self.video_data = []
        self.is_analyzing = False
    
    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.folder_path.set(folder_path)
    
    def get_video_duration(self, video_path):
        try:
            # 检查文件是否存在且可访问
            if not os.path.exists(video_path):
                print(f"文件不存在: {video_path}")
                return 0
                
            # 检查文件大小，跳过过小的文件（可能是损坏的或空的）
            file_size = os.path.getsize(video_path)
            if file_size < 1024:  # 小于1KB的文件
                print(f"文件过小，可能已损坏: {video_path} (大小: {file_size} 字节)")
                return 0
                
            clip = VideoFileClip(video_path)
            if clip.duration <= 0:
                print(f"视频时长为0或负值: {video_path}")
                clip.close()
                return 0
                
            duration = clip.duration / 60  # 转换为分钟
            clip.close()
            return duration
        except Exception as e:
            print(f"处理文件 {video_path} 时出错: {str(e)}")
            return 0
    
    def analyze_videos(self):
        self.video_data = []
        folder_path = self.folder_path.get()
        extensions = [ext.strip() for ext in self.extensions.get().split(",")]
        filter_zero = self.filter_zero_duration.get()
        filter_underscore = self.filter_underscore_files.get()
        
        if not folder_path or not os.path.isdir(folder_path):
            messagebox.showerror("错误", "请选择有效的文件夹")
            self.status_var.set("就绪")
            self.is_analyzing = False
            return
        
        # 获取所有视频文件
        video_files = []
        for root, _, files in os.walk(folder_path):
            for file in files:
                # 过滤下划线开头的文件
                if filter_underscore and os.path.basename(file).startswith("_"):
                    continue
                    
                if any(file.lower().endswith(ext.lower()) for ext in extensions):
                    video_files.append(os.path.join(root, file))
        
        if not video_files:
            messagebox.showinfo("信息", f"在 {folder_path} 中没有找到视频文件")
            self.status_var.set("就绪")
            self.is_analyzing = False
            return
        
        # 清空表格
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # 分析每个视频文件
        total_files = len(video_files)
        for i, video_path in enumerate(video_files):
            if not self.is_analyzing:
                break
                
            # 更新进度
            progress = (i + 1) / total_files * 100
            self.progress_var.set(progress)
            self.status_var.set(f"正在分析 {i+1}/{total_files}: {os.path.basename(video_path)}")
            
            # 更新UI
            self.root.update_idletasks()
            
            # 获取视频时长
            duration = self.get_video_duration(video_path)
            
            # 如果启用了过滤0时长视频的选项，则跳过0时长的视频
            if self.filter_zero_duration.get() and duration == 0:
                continue
                
            # 保存数据
            filename = os.path.basename(video_path)
            self.video_data.append({
                "文件名": filename,
                "路径": video_path,
                "时长(分钟)": round(duration, 2)
            })
            
            # 添加到表格
            self.tree.insert("", tk.END, values=(filename, video_path, round(duration, 2)))
        
        self.status_var.set(f"分析完成，共 {len(self.video_data)} 个视频文件")
        self.is_analyzing = False
    
    def start_analysis(self):
        if self.is_analyzing:
            self.is_analyzing = False
            self.status_var.set("分析已取消")
            return
        
        self.is_analyzing = True
        self.status_var.set("开始分析...")
        self.progress_var.set(0)
        
        # 在新线程中运行分析，避免UI卡顿
        threading.Thread(target=self.analyze_videos, daemon=True).start()
    
    def export_excel(self):
        if not self.video_data:
            messagebox.showwarning("警告", "没有数据可导出，请先分析视频")
            return
        
        # 创建DataFrame
        df = pd.DataFrame(self.video_data)
        
        # 计算总时长和平均时长
        total_duration = df["时长(分钟)"].sum()
        avg_duration = df["时长(分钟)"].mean() if len(df) > 0 else 0
        
        # 获取保存路径
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"视频时长统计_{timestamp}.xlsx"
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel文件", "*.xlsx")],
            initialfile=default_filename
        )
        
        if not file_path:
            return
        
        try:
            # 创建Excel写入器
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                # 写入主数据
                df.to_excel(writer, sheet_name='视频列表', index=False)
                
                # 创建统计信息表
                stats_data = {
                    "统计项": ["视频总数", "总时长(分钟)", "平均时长(分钟)", "过滤0时长视频", "过滤下划线开头文件"],
                    "数值": [
                        len(df),
                        round(total_duration, 2),
                        round(avg_duration, 2),
                        "是" if self.filter_zero_duration.get() else "否",
                        "是" if self.filter_underscore_files.get() else "否"
                    ]
                }
                
                # 写入统计信息
                pd.DataFrame(stats_data).to_excel(writer, sheet_name='统计信息', index=False)
            
            messagebox.showinfo("成功", f"数据已成功导出到 {file_path}\n\n共 {len(df)} 个视频，总时长 {round(total_duration, 2)} 分钟")
        except Exception as e:
            messagebox.showerror("错误", f"导出失败: {str(e)}")

def main():
    root = tk.Tk()
    app = VideoDurationAnalyzer(root)
    root.mainloop()

if __name__ == "__main__":
    main()