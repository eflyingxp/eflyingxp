# 视频时长统计工具

这是一个简单易用的视频时长统计工具，可以帮助您分析文件夹中所有视频文件的时长，并将结果导出为Excel表格。

## 功能特点

- 支持多种视频格式（mp4, avi, mov, mkv, wmv, flv等）
- 递归扫描文件夹中的所有视频文件
- 显示每个视频的文件名、路径和时长（分钟）
- 导出结果到Excel表格
- 带有进度条的用户友好界面

## 安装依赖

在使用此工具前，您需要安装以下Python库：

### 方法一：使用虚拟环境（推荐）

在macOS和某些Linux系统上，Python环境可能是外部管理的，直接安装包会出错。推荐使用虚拟环境：

```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
# 在macOS/Linux上:
source venv/bin/activate
# 在Windows上:
# venv\Scripts\activate

# 安装依赖
pip install moviepy pandas openpyxl
```

### 方法二：直接安装

如果您的系统允许直接安装包，可以使用以下命令：

```bash
# 在macOS/Linux上
pip3 install moviepy pandas openpyxl

# 在Windows上
pip install moviepy pandas openpyxl
```

注意：
- `tkinter`通常已包含在Python标准库中，但在某些系统上需要单独安装：
  - 在macOS上：`brew install python-tk`
  - 在Ubuntu/Debian上：`sudo apt-get install python3-tk`
  - 在Fedora上：`sudo dnf install python3-tkinter`
- 如果遇到权限错误，可以尝试添加`--user`标志：`pip install --user moviepy pandas openpyxl`
- 在macOS上如果遇到"externally-managed-environment"错误，请使用上面的虚拟环境方法

## 使用方法

1. 运行程序：

```bash
python video_duration_analyzer.py
```

2. 在界面上点击"浏览..."按钮选择要分析的文件夹
3. 如有需要，可以修改视频扩展名列表（默认已包含常见格式）
4. 点击"分析视频"按钮开始分析
5. 分析完成后，点击"导出Excel"按钮将结果保存为Excel文件

## 注意事项

- 对于大量视频文件或大型视频文件，分析过程可能需要一些时间
- 分析过程中可以随时取消
- 如果某些视频文件无法正确读取，程序会跳过这些文件并继续处理其他文件

## 系统要求

- Python 3.6或更高版本
- 足够的磁盘空间用于处理视频文件