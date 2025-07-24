# 视频时长统计工具

这是一个用于分析视频文件时长并生成统计报告的工具。该工具可以扫描指定文件夹中的视频文件，计算每个视频的时长，并支持导出Excel报表。

## 功能特点

- 扫描文件夹中的视频文件并计算时长
- 支持多种视频格式（.mp4, .avi, .mov, .mkv, .wmv, .flv等）
- 可过滤0时长视频和下划线开头的文件
- 导出Excel报表，包含详细的视频列表和统计信息
- 简洁直观的图形用户界面

## 打包说明

本项目可以使用PyInstaller打包成可执行应用程序，支持Windows和macOS平台。

### 准备工作

在打包之前，请确保已安装以下依赖：

```bash
pip install pyinstaller pandas openpyxl moviepy==1.0.3
```

### 图标文件

打包前需要准备图标文件：

- Windows平台：需要准备`app_icon.ico`文件
- macOS平台：需要准备`app_icon.icns`文件

可以使用在线工具将PNG图像转换为相应格式的图标文件。

### 在macOS上打包

在macOS上，使用以下命令打包应用程序：

```bash
# 使用spec文件打包
pyinstaller video_duration_analyzer.spec
```

打包完成后，可执行文件将位于`dist/视频时长统计工具.app`。

### 在Windows上打包

在Windows上，使用以下命令打包应用程序：

```bash
# 使用spec文件打包
pyinstaller video_duration_analyzer.spec
```

打包完成后，可执行文件将位于`dist/视频时长统计工具.exe`。

### 注意事项

- PyInstaller不支持跨平台打包，必须在目标平台上进行打包
- 在macOS上，如果需要分发应用程序，可能需要进行代码签名
- 在Windows上，可能需要安装Visual C++ Redistributable

## 在macOS上签名和公证

如果需要在macOS上分发应用程序，建议进行代码签名和公证：

```bash
# 签名应用程序
codesign --deep --force --verify --verbose --sign "Developer ID Application: Your Name (Team ID)" "dist/视频时长统计工具.app"

# 验证签名
codesign --verify --deep --strict "dist/视频时长统计工具.app"

# 公证应用程序
xcrun altool --notarize-app --primary-bundle-id "com.eflyingxp.videodurationanalyzer" --username "your.apple.id@example.com" --password "app-specific-password" --file "dist/视频时长统计工具.app.zip"
```

## 使用方法

1. 启动应用程序
2. 点击"浏览..."按钮选择包含视频文件的文件夹
3. 根据需要调整视频扩展名和过滤选项
4. 点击"分析视频"按钮开始分析
5. 分析完成后，可以点击"导出Excel"按钮导出报表

## 许可证

© 2023 eflyingxp