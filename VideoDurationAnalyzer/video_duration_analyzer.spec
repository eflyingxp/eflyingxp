# -*- mode: python ; coding: utf-8 -*-
import sys

block_cipher = None

a = Analysis(
    ['video_duration_analyzer.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['pandas', 'openpyxl', 'moviepy', 'moviepy.editor', 'moviepy.video.io.VideoFileClip'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# macOS应用程序配置
if sys.platform == 'darwin':
    exe = EXE(
        pyz,
        a.scripts,
        [],
        exclude_binaries=True,
        name='视频时长统计工具',
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        console=False,
        disable_windowed_traceback=False,
        argv_emulation=True,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
        icon='app_icon.icns',  # macOS图标文件
    )
    
    coll = COLLECT(
        exe,
        a.binaries,
        a.zipfiles,
        a.datas,
        strip=False,
        upx=True,
        upx_exclude=[],
        name='视频时长统计工具',
    )
    
    app = BUNDLE(
        coll,
        name='视频时长统计工具.app',
        icon='app_icon.icns',  # macOS图标文件
        bundle_identifier='com.eflyingxp.videodurationanalyzer',
        info_plist={
            'NSHighResolutionCapable': 'True',  # 支持Retina显示
            'CFBundleShortVersionString': '1.0.0',
            'CFBundleVersion': '1.0.0',
            'NSHumanReadableCopyright': '© 2023 eflyingxp',
            'CFBundleName': '视频时长统计工具',
            'CFBundleDisplayName': '视频时长统计工具',
            'CFBundleGetInfoString': '视频时长统计工具',
            'CFBundleIdentifier': 'com.eflyingxp.videodurationanalyzer',
        }
    )

# Windows应用程序配置
else:
    exe = EXE(
        pyz,
        a.scripts,
        a.binaries,
        a.zipfiles,
        a.datas,
        [],
        name='视频时长统计工具',
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        upx_exclude=[],
        runtime_tmpdir=None,
        console=False,
        disable_windowed_traceback=False,
        argv_emulation=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
        icon='app_icon.ico',  # Windows图标文件
        version='file_version_info.txt',
    )