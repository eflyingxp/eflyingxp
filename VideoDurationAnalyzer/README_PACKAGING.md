# 视频时长统计工具打包指南

本文档提供了将视频时长统计工具打包为可执行应用程序的详细说明，适用于macOS和Windows平台。

## 目录

- [前提条件](#前提条件)
- [文件说明](#文件说明)
- [打包步骤](#打包步骤)
  - [步骤1：准备图标](#步骤1准备图标)
  - [步骤2：运行打包脚本](#步骤2运行打包脚本)
- [平台特定说明](#平台特定说明)
  - [macOS特定说明](#macos特定说明)
  - [Windows特定说明](#windows特定说明)
- [常见问题](#常见问题)
- [故障排除](#故障排除)

## 前提条件

- Python 3.6或更高版本
- 以下Python库：
  - pandas
  - openpyxl
  - moviepy (推荐版本：1.0.3)
  - PyInstaller

可以使用以下命令安装所需的库：

```bash
pip install pandas openpyxl moviepy==1.0.3 pyinstaller
```

## 文件说明

本打包工具包含以下文件：

- `build_app.py` - 主打包脚本
- `build_app.sh` - macOS平台的启动脚本
- `build_app.bat` - Windows平台的启动脚本
- `convert_icon.py` - 图标转换工具
- `app_icon.svg` - 应用程序图标的SVG源文件
- `video_duration_analyzer.spec` - PyInstaller配置文件
- `file_version_info.txt` - Windows版本信息文件

## 打包步骤

### 步骤1：准备图标

应用程序需要特定格式的图标文件：

- macOS: `app_icon.icns`
- Windows: `app_icon.ico`

您可以使用提供的`convert_icon.py`脚本从SVG文件生成这些图标：

```bash
# macOS
python3 convert_icon.py

# Windows
python convert_icon.py
```

#### 图标转换依赖项

- macOS: 需要安装Inkscape或cairosvg，以及系统自带的iconutil
- Windows: 需要安装Inkscape或cairosvg，以及Pillow库

```bash
pip install cairosvg pillow
```

### 步骤2：运行打包脚本

#### macOS

```bash
# 添加执行权限
chmod +x build_app.sh

# 运行脚本
./build_app.sh
```

#### Windows

```bash
# 运行批处理文件
build_app.bat
```

或者直接运行Python脚本：

```bash
python build_app.py
```

## 平台特定说明

### macOS特定说明

#### 应用程序签名和公证

为了在macOS上分发应用程序，您需要对应用程序进行签名和公证。这需要一个有效的Apple开发者账号。

1. 使用以下命令对应用程序进行签名：

```bash
codesign --force --deep --sign "Developer ID Application: 您的开发者名称" "dist/视频时长统计工具.app"
```

2. 创建一个ZIP归档：

```bash
ditto -c -k --keepParent "dist/视频时长统计工具.app" "视频时长统计工具.zip"
```

3. 提交公证：

```bash
xcrun altool --notarize-app --primary-bundle-id "com.eflyingxp.videodurationanalyzer" --username "您的Apple ID" --password "您的应用专用密码" --file "视频时长统计工具.zip"
```

4. 检查公证状态：

```bash
xcrun altool --notarization-info "提交ID" --username "您的Apple ID" --password "您的应用专用密码"
```

5. 将公证信息附加到应用程序：

```bash
xcrun stapler staple "dist/视频时长统计工具.app"
```

### Windows特定说明

#### 创建安装程序

您可以使用Inno Setup等工具为Windows应用程序创建安装程序。

1. 下载并安装[Inno Setup](https://jrsoftware.org/isinfo.php)
2. 创建一个新的脚本文件，配置应用程序信息和文件
3. 编译脚本生成安装程序

## 常见问题

### Q: 打包后的应用程序无法启动

**A:** 这可能是由于缺少依赖项或权限问题。检查以下几点：

1. 确保所有必需的Python库都已安装
2. 检查应用程序日志（如果有）
3. 尝试从命令行启动应用程序以查看错误消息

### Q: 应用程序图标不显示

**A:** 确保图标文件格式正确，并且在打包前已经放置在正确的位置。

## 故障排除

### PyInstaller错误

如果PyInstaller报告错误，可以尝试以下方法：

1. 使用`--debug=all`选项运行PyInstaller以获取更详细的日志
2. 检查是否有隐藏的导入未被包含
3. 尝试使用`--clean`选项清理PyInstaller缓存

### 依赖项问题

如果应用程序启动时报告缺少依赖项，可以尝试：

1. 在spec文件中添加缺少的依赖项
2. 使用`--add-data`选项包含额外的数据文件
3. 检查是否有动态加载的模块未被包含

---

如有任何问题或建议，请联系开发者。