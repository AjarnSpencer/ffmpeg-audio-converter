; Inno Setup Script for ffmpeg Audio Converter

[Setup]
AppName=ffmpeg Audio Converter
AppVersion=1.0.1
DefaultDirName={autopf}\\ffmpeg Audio Converter
DefaultGroupName=ffmpeg Audio Converter
OutputBaseFilename=ffmpeg_Audio_Converter_setup
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
OutputDir=dist
SetupIconFile=app_icon.ico
UninstallDisplayIcon={app}\\main.exe

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:";

[Files]
Source: "dist\\main.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\\ffmpeg Audio Converter"; Filename: "{app}\\main.exe"
Name: "{autodesktop}\\ffmpeg Audio Converter"; Filename: "{app}\\main.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\\main.exe"; Description: "Launch ffmpeg Audio Converter"; Flags: nowait postinstall skipifsilent
