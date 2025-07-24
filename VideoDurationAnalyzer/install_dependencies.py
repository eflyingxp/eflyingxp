#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import platform

def install_dependencies():
    print("正在安装视频时长统计工具所需的依赖...\
")
    
    # 检查Python版本
    python_version = sys.version_info
    print(f"Python版本: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 6):
        print("错误: 需要Python 3.6或更高版本")
        sys.exit(1)
    
    # 安装依赖
    dependencies = [
        "pandas",
        "openpyxl",
        "moviepy==1.0.3",
        "pyinstaller"
    ]
    
    for dep in dependencies:
        print(f"\n正在安装 {dep}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            print(f"{dep} 安装成功")
        except subprocess.CalledProcessError as e:
            print(f"错误: 安装 {dep} 失败: {str(e)}")
            sys.exit(1)
    
    print("\n所有依赖安装完成!")
    
    # 检查是否有图标文件
    system = platform.system()
    if system == "Darwin":  # macOS
        if not os.path.exists("app_icon.icns"):
            print("\n警告: 未找到 app_icon.icns 文件，这是macOS打包所需的图标文件")
            print("请准备一个.icns格式的图标文件，并命名为app_icon.icns")
    elif system == "Windows":
        if not os.path.exists("app_icon.ico"):
            print("\n警告: 未找到 app_icon.ico 文件，这是Windows打包所需的图标文件")
            print("请准备一个.ico格式的图标文件，并命名为app_icon.ico")
    
    print("\n准备打包命令:")
    print("pyinstaller video_duration_analyzer.spec")

def main():
    install_dependencies()
    
    print("\n按Enter键退出...")
    input()

if __name__ == "__main__":
    main()