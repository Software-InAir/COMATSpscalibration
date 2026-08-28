#ifndef AppVersion
  #define AppVersion "0.0.0-dev"
#endif

#define RootDir ExtractFileDir(SourcePath)

[Setup]
AppId={{9A6C4B5D-4B49-4F0F-9A89-1C7E6B2F7E31}
AppName=PowerSupplyCalibrator
AppVersion={#AppVersion}
AppVerName=PowerSupplyCalibrator {#AppVersion}

DefaultDirName={autopf}\PowerSupplyCalibrator
DefaultGroupName=PowerSupplyCalibrator

OutputDir={#RootDir}\installer-output
OutputBaseFilename=PowerSupplyCalibrator-{#AppVersion}-Setup

Compression=lzma2
SolidCompression=yes
DisableProgramGroupPage=yes

ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
PrivilegesRequired=admin

UninstallDisplayIcon={app}\main.exe

CloseApplications=yes
RestartApplications=no

[Tasks]
Name: "desktopicon"; \
    Description: "Create a &desktop icon"; \
    GroupDescription: "Additional icons:"; \
    Flags: unchecked

[Files]
; Complete PyInstaller one-directory build
Source: "{#RootDir}\dist\main\*"; \
    DestDir: "{app}"; \
    Flags: recursesubdirs createallsubdirs ignoreversion


[Icons]
Name: "{group}\PowerSupplyCalibrator"; \
    Filename: "{app}\main.exe"; \
    WorkingDir: "{app}"

Name: "{commondesktop}\PowerSupplyCalibrator"; \
    Filename: "{app}\main.exe"; \
    WorkingDir: "{app}"; \
    Tasks: desktopicon

[Registry]
Root: HKLM; \
    Subkey: "Software\PowerSupplyCalibrator"; \
    ValueType: string; \
    ValueName: "Version"; \
    ValueData: "{#AppVersion}"; \
    Flags: uninsdeletekey

[Run]


Filename: "{app}\main.exe"; \
    WorkingDir: "{app}"; \
    Flags: nowait postinstall skipifsilent



