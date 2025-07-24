@echo off
echo 正在启动视频时长统计工具...

:: 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到Python。请安装Python后再试。
    echo 您可以从 https://www.python.org/downloads/ 下载安装。
    pause
    exit /b 1
)

:: 虚拟环境目录
set VENV_DIR=venv

:: 检查是否已存在虚拟环境，如果不存在则创建
if not exist %VENV_DIR% (
    echo 创建Python虚拟环境...
    python -m venv %VENV_DIR%
    if %errorlevel% neq 0 (
        echo 错误: 无法创建虚拟环境。请确保已安装venv模块。
        echo 您可以尝试运行: pip install virtualenv
        pause
        exit /b 1
    )
    echo 虚拟环境创建成功。
)

:: 激活虚拟环境
echo 激活虚拟环境...
call %VENV_DIR%\Scripts\activate.bat

:: 检查并安装必要的依赖
echo 检查必要的依赖...

:: 创建临时脚本来检查和安装依赖
echo import importlib.util > check_deps.py
echo import subprocess >> check_deps.py
echo import sys >> check_deps.py
echo import platform >> check_deps.py
echo. >> check_deps.py
echo def check_install(package): >> check_deps.py
echo     spec = importlib.util.find_spec(package) >> check_deps.py
echo     if spec is None: >> check_deps.py
echo         print(f"安装 {package}...") >> check_deps.py
echo         subprocess.check_call([sys.executable, "-m", "pip", "install", package]) >> check_deps.py
echo         return False >> check_deps.py
echo     return True >> check_deps.py
echo. >> check_deps.py
echo # 检查tkinter是否可用 >> check_deps.py
echo try: >> check_deps.py
echo     import tkinter >> check_deps.py
echo     print("tkinter已安装。") >> check_deps.py
echo except ImportError: >> check_deps.py
echo     print("警告: tkinter未安装或不可用。") >> check_deps.py
echo     print("在Windows上，tkinter通常随Python一起安装，但可能需要重新安装Python并勾选'tcl/tk'选项。") >> check_deps.py
echo     print("请访问 https://www.python.org/downloads/ 重新安装Python，确保在安装选项中包含tcl/tk。") >> check_deps.py
echo     print("安装完成后，请重新运行此脚本。") >> check_deps.py
echo     sys.exit(1) >> check_deps.py
echo. >> check_deps.py
echo # 检查必要的库 >> check_deps.py
echo required_packages = ["moviepy", "pandas", "openpyxl"] >> check_deps.py
echo all_installed = True >> check_deps.py
echo. >> check_deps.py
echo for package in required_packages: >> check_deps.py
echo     try: >> check_deps.py
echo         __import__(package) >> check_deps.py
echo         print(f"{package}已安装。") >> check_deps.py
echo     except ImportError: >> check_deps.py
echo         print(f"{package}未安装，正在安装...") >> check_deps.py
echo         subprocess.check_call([sys.executable, "-m", "pip", "install", package]) >> check_deps.py
echo         all_installed = False >> check_deps.py
echo. >> check_deps.py
echo if all_installed: >> check_deps.py
echo     print("所有依赖已安装。") >> check_deps.py
echo else: >> check_deps.py
echo     print("依赖安装完成。") >> check_deps.py

:: 运行依赖检查脚本
python check_deps.py
del check_deps.py

:: 提示用户
echo 注意: 使用虚拟环境运行，避免系统Python环境的限制。

:: 运行主程序
echo 启动应用程序...
python video_duration_analyzer.py

pause