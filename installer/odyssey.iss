; Odyssey kurulum programı (Inno Setup 6).
;
; Derleme: `python tools/build_installer.py` — önce `tools/build_exe.py`
; paketi `dist/Odyssey` altına üretmiş olmalı. Araç sürüm numarasını
; `app/version.py`'den okuyup buraya /DAppVersion ile veriyor.
;
; Kurallar:
;
; - **AppId hiç değişmez.** Değişirse Windows sonraki sürümü ayrı bir program
;   sayar; güncelleme yerine ikinci bir kurulum olur.
; - **Kullanıcı başına kurulum** (`%LOCALAPPDATA%\Programs\Odyssey`), yönetici
;   izni yok. Uygulama kendini sessiz kipte güncelliyor; Program Files her
;   seferinde Windows onay kutusu çıkarırdı.
; - **Kullanıcı verisine dokunulmaz.** İlerleme, notlar ve ayarlar
;   `%APPDATA%\Odyssey` içinde; ne kurulum ne kaldırma orayı siliyor.
; - Uygulamanın gönderdiği parametreler (`app/core/updater.py`):
;     /OLDPID=<süreç>  kapanması beklenen eski uygulama
;     /OLDDIR=<klasör> yalnızca zip'ten çalışan eski uygulama gönderiyor;
;                      kurulumdan sonra oradaki Odyssey.exe ve _internal
;                      siliniyor. Kurulu uygulama göndermiyor.

#define AppName "Odyssey"
#define AppExe "Odyssey.exe"

#ifndef AppVersion
  #define AppVersion "0.0.0"
#endif
#ifndef SourceDir
  #define SourceDir "..\dist\Odyssey"
#endif
#ifndef OutputDir
  #define OutputDir "..\dist"
#endif

[Setup]
AppId={{960B6191-7788-4E14-B672-4B50AF6DC638}
AppName={#AppName}
AppVersion={#AppVersion}
AppVerName={#AppName} {#AppVersion}
AppPublisher=Alican Kaya
AppPublisherURL=https://github.com/AlicanKaya192/Odyssey
AppSupportURL=https://github.com/AlicanKaya192/Odyssey/issues
AppUpdatesURL=https://github.com/AlicanKaya192/Odyssey/releases
VersionInfoVersion={#AppVersion}
DefaultDirName={localappdata}\Programs\{#AppName}
DefaultGroupName={#AppName}
DisableProgramGroupPage=yes
; Klasör sayfası yalnızca ilk kurulumda; güncellemede aynı yere kuruluyor.
DisableDirPage=auto
UsePreviousAppDir=yes
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
OutputDir={#OutputDir}
OutputBaseFilename={#AppName}-{#AppVersion}-setup
SetupIconFile=..\app\resources\icon.ico
UninstallDisplayIcon={app}\{#AppExe}
UninstallDisplayName={#AppName}
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
LicenseFile=..\LICENSE
; Eski sürecin kapanmasını kendimiz bekliyoruz (/OLDPID); Windows'un
; "uygulamayı kapat" kutusu sessiz güncellemede araya girmesin.
CloseApplications=no
RestartApplications=no

[Languages]
Name: "turkish"; MessagesFile: "compiler:Languages\Turkish.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[InstallDelete]
; Önceki sürümün paketi baştan siliniyor: yeni sürümde kaldırılan bir kütüphane
; dosyası eskisinden kalıp yanlış yüklenmesin.
Type: filesandordirs; Name: "{app}\_internal"

[Files]
Source: "{#SourceDir}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\{#AppName}"; Filename: "{app}\{#AppExe}"
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\{#AppExe}"; Tasks: desktopicon

[Run]
; Sessiz kipte de çalışıyor (skipifsilent yok): güncellemeden sonra Odyssey
; kendiliğinden açılıyor.
Filename: "{app}\{#AppExe}"; Description: "{cm:LaunchProgram,{#AppName}}"; Flags: nowait postinstall

[UninstallRun]
; Seri hatırlatmalarının zamanlanmış görevi program kaldırılınca kalmasın;
; kalsaydı her gün olmayan bir programı çağırırdı. Görev yoksa komut sessizce
; başarısız oluyor.
Filename: "{sys}\schtasks.exe"; Parameters: "/Delete /TN ""Odyssey Reminder"" /F"; Flags: runhidden; RunOnceId: "RemoveReminderTask"

[Registry]
; Hatırlatmaların bildirim kimliği ve `odyssey://` bağlantısı (uygulama
; kendisi yazıyor); kaldırılınca siliniyor.
Root: HKCU; Subkey: "Software\Classes\AppUserModelId\AlicanKaya.Odyssey"; Flags: uninsdeletekey dontcreatekey
Root: HKCU; Subkey: "Software\Classes\odyssey"; Flags: uninsdeletekey dontcreatekey

[Code]
const
  SYNCHRONIZE = $00100000;
  WAIT_TIMEOUT = $00000102;
  OLD_EXIT_WAIT_MS = 60000;

function OpenProcess(dwDesiredAccess: Cardinal; bInheritHandle: Boolean; dwProcessId: Cardinal): THandle;
  external 'OpenProcess@kernel32.dll stdcall';
function WaitForSingleObject(hObject: THandle; dwMilliseconds: Cardinal): Cardinal;
  external 'WaitForSingleObject@kernel32.dll stdcall';
function CloseHandle(hObject: THandle): Boolean;
  external 'CloseHandle@kernel32.dll stdcall';

{ Güncellemeyi başlatan eski uygulamanın kapanmasını bekler. Dosyaları kilitli
  tutuyor; beklemeden yazmak yarım bir kurulum bırakırdı. }
procedure WaitForOldProcess();
var
  Pid: Integer;
  Handle: THandle;
begin
  Pid := StrToIntDef(ExpandConstant('{param:OLDPID|0}'), 0);
  if Pid <= 0 then
    Exit;
  Handle := OpenProcess(SYNCHRONIZE, False, Pid);
  if Handle = 0 then
    Exit;
  WaitForSingleObject(Handle, OLD_EXIT_WAIT_MS);
  CloseHandle(Handle);
  { Dosya tanıtıcılarının kapanması bir an sürebiliyor. }
  Sleep(1000);
end;

function PrepareToInstall(var NeedsRestart: Boolean): String;
begin
  WaitForOldProcess();
  Result := '';
end;

function SamePath(const A, B: String): Boolean;
begin
  Result := CompareText(AddBackslash(ExpandFileName(A)), AddBackslash(ExpandFileName(B))) = 0;
end;

{ Bir klasörü birkaç denemeyle siler; eski süreç dosyayı bir an daha
  tutuyor olabilir. }
procedure DeleteTreeWithRetry(const Path: String);
var
  Attempt: Integer;
begin
  for Attempt := 1 to 5 do
  begin
    if not DirExists(Path) then
      Exit;
    DelTree(Path, True, True, True);
    if not DirExists(Path) then
      Exit;
    Sleep(500);
  end;
end;

{ Zip'ten çalışan eski Odyssey'in program dosyalarını siler.

  Yalnızca uygulamanın gönderdiği klasörde hem Odyssey.exe hem _internal
  varsa ve klasör yeni kurulum yeri değilse. Klasörün kendisi yalnızca boş
  kaldıysa siliniyor: kullanıcı yanına başka dosya koyduysa dokunulmuyor.
  Kullanıcı verisi orada değil (%APPDATA%\Odyssey). }
procedure RemoveOldZipInstall();
var
  OldDir: String;
  Attempt: Integer;
begin
  OldDir := ExpandConstant('{param:OLDDIR|}');
  if OldDir = '' then
    Exit;
  OldDir := RemoveBackslashUnlessRoot(OldDir);
  if SamePath(OldDir, ExpandConstant('{app}')) then
    Exit;
  if not (FileExists(OldDir + '\{#AppExe}') and DirExists(OldDir + '\_internal')) then
    Exit;

  DeleteTreeWithRetry(OldDir + '\_internal');
  for Attempt := 1 to 5 do
  begin
    if DeleteFile(OldDir + '\{#AppExe}') or not FileExists(OldDir + '\{#AppExe}') then
      Break;
    Sleep(500);
  end;

  { Zip güncellemesinin bıraktığı yedek klasör. }
  if FileExists(OldDir + '.old\{#AppExe}') then
    DeleteTreeWithRetry(OldDir + '.old');

  RemoveDir(OldDir);
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
    RemoveOldZipInstall();
end;
