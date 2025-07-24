#!/bin/bash

echo "视频时长统计工具打包脚本"
echo "----------------------------------------"

# 检查Python是否已安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python，请安装Python 3.6或更高版本"
    read -p "按Enter键退出..."
    exit 1
fi

# 添加执行权限
chmod +x build_app.py
chmod +x convert_icon.py

# 运行打包脚本
python3 build_app.py

read -p "按Enter键退出..."