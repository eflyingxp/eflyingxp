; 视频时长统计工具 - Inno Setup 脚本
; 用于创建Windows安装程序

#define MyAppName "视频时长统计工具"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "eflyingxp"
#define MyAppURL ""
#define MyAppExeName "视频时长统计工具.exe"

[Setup]
; 注意: AppId的值为唯一标识此应用程序。
; 不要在其他安装程序中使用相同的AppId值。
AppId={{E8F5A3B7-F2D4-4E8C-9F3D-A5C6E4F7B8D9}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DisableProgramGroupPage=yes
LicenseFile=LICENSE.txt
; 如果您希望允许用户自定义安装目录，请删除以下行
; DisableDirPage=yes
; 如果您希望在开始菜单中创建一个文件夹，请取消注释以下行
DefaultGroupName={#MyAppName}
; 取消注释以下行以在"添加/删除程序"中运行安装程序
UninstallDisplayIcon={app}\{#MyAppExeName}
; 设置安装程序图标
SetupIconFile=app_icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "chinesesimplified"; MessagesFile: "compiler:Languages\ChineseSimplified.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
; 添加其他文件或目录
Source: "USER_GUIDE.md"; DestDir: "{app}"; Flags: ignoreversion
; 如果有LICENSE文件，请取消注释以下行
; Source: "LICENSE.txt"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Code]
function InitializeSetup(): Boolean;
begin
  // 在这里添加安装前的检查代码
  Result := True;
end;