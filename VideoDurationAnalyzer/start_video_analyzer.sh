#!/bin/bash

# 视频时长统计工具启动脚本

echo "正在启动视频时长统计工具..."

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3。请安装Python3后再试。"
    echo "您可以从 https://www.python.org/downloads/ 下载安装。"
    exit 1
fi

# 虚拟环境目录
VENV_DIR="venv"

# 检查是否已存在虚拟环境，如果不存在则创建
if [ ! -d "$VENV_DIR" ]; then
    echo "创建Python虚拟环境..."
    python3 -m venv "$VENV_DIR"
    if [ $? -ne 0 ]; then
        echo "错误: 无法创建虚拟环境。请确保已安装venv模块。"
        echo "您可以尝试运行: pip3 install --user virtualenv"
        exit 1
    fi
    echo "虚拟环境创建成功。"
fi

# 激活虚拟环境
echo "激活虚拟环境..."
source "$VENV_DIR/bin/activate"

# 检查并安装必要的依赖
echo "检查必要的依赖..."

# 创建临时脚本来检查和安装依赖
cat > check_deps.py << 'EOF'
import importlib.util
import subprocess
import sys
import platform

# 检查tkinter是否可用
try:
    import tkinter
    print("tkinter已安装。")
except ImportError:
    print("警告: tkinter未安装或不可用。")
    system = platform.system()
    if system == "Darwin":  # macOS
        print("在macOS上，您可以使用以下命令安装tkinter:")
        print("  brew install python-tk")
    elif system == "Linux":
        distro = platform.linux_distribution()[0].lower() if hasattr(platform, 'linux_distribution') else ""
        if "ubuntu" in distro or "debian" in distro:
            print("在Ubuntu/Debian上，您可以使用以下命令安装tkinter:")
            print("  sudo apt-get install python3-tk")
        elif "fedora" in distro:
            print("在Fedora上，您可以使用以下命令安装tkinter:")
            print("  sudo dnf install python3-tkinter")
        else:
            print("请根据您的Linux发行版安装python3-tk包。")
    print("安装完成后，请重新运行此脚本。")
    sys.exit(1)

# 检查必要的库
required_packages = ["moviepy", "pandas", "openpyxl"]
all_installed = True

for package in required_packages:
    try:
        __import__(package)
        print(f"{package}已安装。")
    except ImportError:
        print(f"{package}未安装，正在安装...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        all_installed = False

if all_installed:
    print("所有依赖已安装。")
else:
    print("依赖安装完成。")
EOF

# 运行依赖检查脚本
python3 check_deps.py
rm check_deps.py

# 设置执行权限
chmod +x video_duration_analyzer.py

# 提示用户
echo "注意: 使用虚拟环境运行，避免系统Python环境的限制。"

# 运行主程序
echo "启动应用程序..."
python3 video_duration_analyzer.py