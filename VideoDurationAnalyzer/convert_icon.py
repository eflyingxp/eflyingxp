#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import platform
import subprocess
from pathlib import Path

def check_command(command):
    """检查命令是否可用"""
    try:
        subprocess.run([command, "--version"], 
                       stdout=subprocess.PIPE, 
                       stderr=subprocess.PIPE, 
                       check=False)
        return True
    except FileNotFoundError:
        return False

def convert_svg_to_png(svg_path, png_path, size):
    """使用Inkscape或cairosvg将SVG转换为PNG"""
    if check_command("inkscape"):
        try:
            subprocess.run([
                "inkscape",
                "--export-filename", png_path,
                "--export-width", str(size),
                "--export-height", str(size),
                svg_path
            ], check=True)
            return True
        except subprocess.CalledProcessError:
            print(f"使用Inkscape转换失败: {svg_path} -> {png_path}")
            return False
    else:
        try:
            # 尝试导入cairosvg库
            try:
                import cairosvg
                cairosvg.svg2png(url=svg_path, write_to=png_path, output_width=size, output_height=size)
                return True
            except ImportError:
                print("错误: 未找到Inkscape或cairosvg，无法转换SVG")
                print("请安装Inkscape或使用pip install cairosvg安装cairosvg")
                return False
            except Exception as e:
                print(f"使用cairosvg转换失败: {str(e)}")
                return False
        except Exception as e:
            print(f"转换SVG过程中发生未知错误: {str(e)}")
            return False

def convert_for_macos(svg_path):
    """为macOS创建.icns图标"""
    print("正在为macOS创建图标...")
    
    # 创建临时目录
    iconset_path = "app.iconset"
    os.makedirs(iconset_path, exist_ok=True)
    
    # 生成不同尺寸的PNG
    sizes = [16, 32, 64, 128, 256, 512, 1024]
    for size in sizes:
        png_path = os.path.join(iconset_path, f"icon_{size}x{size}.png")
        if not convert_svg_to_png(svg_path, png_path, size):
            return False
        
        # 为Retina显示创建@2x版本
        if size <= 512:
            png_path_2x = os.path.join(iconset_path, f"icon_{size}x{size}@2x.png")
            if not convert_svg_to_png(svg_path, png_path_2x, size * 2):
                return False
    
    # 使用iconutil将iconset转换为icns
    if check_command("iconutil"):
        try:
            subprocess.run(["iconutil", "-c", "icns", iconset_path], check=True)
            print("成功创建app.icns")
            
            # 重命名为app_icon.icns
            if os.path.exists("app.icns"):
                os.rename("app.icns", "app_icon.icns")
                print("已重命名为app_icon.icns")
            
            return True
        except subprocess.CalledProcessError as e:
            print(f"使用iconutil转换失败: {str(e)}")
            return False
    else:
        print("错误: 未找到iconutil命令，无法创建.icns文件")
        print("这个命令应该在macOS系统上可用")
        return False

def convert_for_windows(svg_path):
    """为Windows创建.ico图标"""
    print("正在为Windows创建图标...")
    
    # 创建临时目录
    os.makedirs("icons_temp", exist_ok=True)
    
    # 生成不同尺寸的PNG
    sizes = [16, 32, 48, 64, 128, 256]
    png_files = []
    
    for size in sizes:
        png_path = os.path.join("icons_temp", f"icon_{size}x{size}.png")
        if not convert_svg_to_png(svg_path, png_path, size):
            return False
        png_files.append(png_path)
    
    # 使用PIL将PNG转换为ICO
    try:
        # 尝试导入PIL库
        try:
            from PIL import Image
        except ImportError:
            print("错误: 未找到PIL库，无法创建.ico文件")
            print("请使用pip install pillow安装PIL")
            return False
        
        # 打开所有PNG图像
        images = []
        for png in png_files:
            try:
                img = Image.open(png)
                images.append(img)
            except Exception as e:
                print(f"打开图像文件失败: {png}, 错误: {str(e)}")
                return False
        
        # 保存为ICO文件
        try:
            if images:
                images[0].save("app_icon.ico", format="ICO", sizes=[(size, size) for size in sizes], 
                             append_images=images[1:] if len(images) > 1 else [])
                print("成功创建app_icon.ico")
                return True
            else:
                print("错误: 没有有效的图像文件可用于创建ICO")
                return False
        except Exception as e:
            print(f"创建ICO文件失败: {str(e)}")
            return False
    except Exception as e:
        print(f"创建ICO文件过程中发生未知错误: {str(e)}")
        return False

def cleanup():
    """清理临时文件"""
    print("\n清理临时文件...")
    
    # 删除临时目录
    if os.path.exists("app.iconset"):
        import shutil
        shutil.rmtree("app.iconset")
    
    if os.path.exists("icons_temp"):
        import shutil
        shutil.rmtree("icons_temp")

def main():
    print("图标转换工具")
    print("-" * 40)
    
    # 检查SVG文件
    svg_path = "app_icon.svg"
    if not os.path.exists(svg_path):
        print(f"错误: 未找到{svg_path}文件")
        sys.exit(1)
    
    # 检查系统类型
    system = platform.system()
    
    # 无论系统类型，都尝试生成两种格式的图标
    success_macos = convert_for_macos(svg_path)
    success_windows = convert_for_windows(svg_path)
    
    # 只要有一种格式成功生成，就认为是成功的
    success = success_macos or success_windows
    
    # 清理临时文件
    cleanup()
    
    if success:
        print("\n图标转换成功!")
    else:
        print("\n图标转换失败!")
        sys.exit(1)

if __name__ == "__main__":
    main()