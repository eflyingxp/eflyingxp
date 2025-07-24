@echo off
echo 视频时长统计工具打包脚本
echo ----------------------------------------

:: 检查Python是否已安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到Python，请安装Python 3.6或更高版本
    pause
    exit /b 1
)

:: 运行打包脚本
python build_app.py

pause