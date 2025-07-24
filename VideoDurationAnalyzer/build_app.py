#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import platform
import shutil
from datetime import datetime

def build_app():
    print("视频时长统计工具打包脚本")
    print("-" * 40)
    
    # 检查Python版本
    python_version = sys.version_info
    print(f"Python版本: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 6):
        print("错误: 需要Python 3.6或更高版本")
        sys.exit(1)
    
    # 检查操作系统
    system = platform.system()
    print(f"操作系统: {system}")
    
    # 检查PyInstaller是否已安装
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "show", "pyinstaller"], 
                             stdout=subprocess.DEVNULL, 
                             stderr=subprocess.DEVNULL)
        print("PyInstaller已安装")
    except subprocess.CalledProcessError:
        print("PyInstaller未安装，正在安装...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("PyInstaller安装成功")
        except subprocess.CalledProcessError as e:
            print(f"错误: 安装PyInstaller失败: {str(e)}")
            sys.exit(1)
    
    # 检查spec文件
    if not os.path.exists("video_duration_analyzer.spec"):
        print("错误: 未找到video_duration_analyzer.spec文件")
        sys.exit(1)
    
    # 检查图标文件
    if system == "Darwin":  # macOS
        if not os.path.exists("app_icon.icns"):
            print("警告: 未找到app_icon.icns文件，将使用默认图标")
    elif system == "Windows":
        if not os.path.exists("app_icon.ico"):
            print("警告: 未找到app_icon.ico文件，将使用默认图标")
    
    # 清理旧的构建文件
    if os.path.exists("build"):
        print("正在清理旧的build目录...")
        try:
            shutil.rmtree("build")
        except Exception as e:
            print(f"警告: 无法删除build目录: {str(e)}")
    
    if os.path.exists("dist"):
        print("正在清理旧的dist目录...")
        try:
            shutil.rmtree("dist")
        except Exception as e:
            print(f"警告: 无法删除dist目录: {str(e)}")
    
    # 开始打包
    print("\n开始打包应用程序...")
    start_time = datetime.now()
    
    try:
        subprocess.check_call([sys.executable, "-m", "PyInstaller", "video_duration_analyzer.spec"])
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        print(f"\n打包完成! 用时: {duration:.2f}秒")
        
        # 检查打包结果
        if system == "Darwin":  # macOS
            app_path = os.path.join("dist", "视频时长统计工具.app")
            if os.path.exists(app_path):
                print(f"应用程序已生成: {os.path.abspath(app_path)}")
                print("\n您可以将此应用程序复制到Applications文件夹中使用")
            else:
                print("错误: 未找到生成的应用程序")
        elif system == "Windows":
            exe_path = os.path.join("dist", "视频时长统计工具.exe")
            if os.path.exists(exe_path):
                print(f"应用程序已生成: {os.path.abspath(exe_path)}")
                print("\n您可以将此可执行文件复制到任意位置使用")
            else:
                print("错误: 未找到生成的可执行文件")
    except subprocess.CalledProcessError as e:
        print(f"错误: 打包失败: {str(e)}")
        sys.exit(1)

def main():
    build_app()
    
    print("\n按Enter键退出...")
    input()

if __name__ == "__main__":
    main()