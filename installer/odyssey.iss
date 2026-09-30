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

; Deneme kipi (/DTestMode /DTestDir=<klasör>): yalnızca fark kurulumunu
; sınamak için. Başka bir kimlik ve ad, geçici klasör; kısayol, kurulum
; sonrası açma, hatırlatma görevi ve bildirim kayıtları yok. Böylece deneme
; bilgisayardaki gerçek Odyssey kurulumuna hiç dokunmuyor.
#ifdef TestMode
  #define AppName "OdysseyPatchTest"
  #define AppGuid "5F1C2B7A-3D4E-4F60-9A1B-7C8D9E0F1A2B"
#else
  #define AppName "Odyssey"
  #define AppGuid "960B6191-7788-4E14-B672-4B50AF6DC638"
#endif
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

; Fark kurulumu (0.9.1'den itibaren): `tools/build_installer.py` önceki bir
; sürümün dosya kaydıyla (`installer/manifests/<sürüm>.json.gz`) bugünkü
; paketi karşılaştırıp /DPatchFrom=<eski sürüm> ve /DPatchList=<dosya> ile
; bu betiği ikinci kez derliyor. Çıktı `Odyssey-<yeni>-patch-<eski>.exe`:
; yalnızca değişen ve yeni dosyalar, kaldırılanların silinmesi. Uygulama
; yamayı ancak kendi sürümü <eski>'ye eşitse seçiyor (`updater.pick_update`);
; yine de kurulu sürüm burada bir kez daha denetleniyor.

[Setup]
AppId={{{#AppGuid}}
AppName={#AppName}
AppVersion={#AppVersion}
AppVerName={#AppName} {#AppVersion}
AppPublisher=Alican Kaya
AppPublisherURL=https://github.com/AlicanKaya192/Odyssey
AppSupportURL=https://github.com/AlicanKaya192/Odyssey/issues
AppUpdatesURL=https://github.com/AlicanKaya192/Odyssey/releases
VersionInfoVersion={#AppVersion}
#ifdef TestMode
DefaultDirName={#TestDir}
#else
DefaultDirName={localappdata}\Programs\{#AppName}
#endif
DefaultGroupName={#AppName}
DisableProgramGroupPage=yes
; Klasör sayfası yalnızca ilk kurulumda; güncellemede aynı yere kuruluyor.
DisableDirPage=auto
UsePreviousAppDir=yes
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
OutputDir={#OutputDir}
#ifdef PatchFrom
OutputBaseFilename={#AppName}-{#AppVersion}-patch-{#PatchFrom}
#else
OutputBaseFilename={#AppName}-{#AppVersion}-setup
#endif
SetupIconFile=..\app\resources\icon.ico
; Kurulum bitince Windows'a "simgeleri yenile" denir (SHChangeNotify). Yoksa
; masaüstü kısayolu, .exe'nin simgesi değişse de önbellekteki eski simgeyi
; gösteriyordu (0.9.0'da sentor simgesine geçerken oldu).
ChangesAssociations=yes
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

#ifdef PatchFrom
; Fark kurulumu: dosya listesi ve silinecekler araçtan geliyor
; ([InstallDelete] ve [Files] bölümleriyle birlikte).
#include PatchList
#else
[InstallDelete]
; Önceki sürümün paketi baştan siliniyor: yeni sürümde kaldırılan bir kütüphane
; dosyası eskisinden kalıp yanlış yüklenmesin.
Type: filesandordirs; Name: "{app}\_internal"

[Files]
Source: "{#SourceDir}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
#endif

#ifndef TestMode
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
#endif

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

#ifdef PatchFrom
const
  UNINSTALL_KEY = 'Software\Microsoft\Windows\CurrentVersion\Uninstall\{{#AppGuid}}_is1';

{ Fark kurulumu yalnızca {#PatchFrom} kuruluysa çalışır: başka bir sürümün
  üstüne yazılırsa dosyalar karışır. Tutmazsa hiçbir şeye dokunmadan
  çıkılır ve (eski süreç kapanınca) program yeniden açılır; uygulama bir
  sonraki denemede tam kurulumu indirir (`updater.patch_failed_before`). }
function InitializeSetup(): Boolean;
var
  Version, Location: String;
  ResultCode: Integer;
begin
  Result := True;
  if not RegQueryStringValue(HKCU, UNINSTALL_KEY, 'DisplayVersion', Version) then
    Version := '';
  if Version = '{#PatchFrom}' then
    Exit;
  Result := False;
#ifdef TestMode
  Exit;
#endif
  if RegQueryStringValue(HKCU, UNINSTALL_KEY, 'InstallLocation', Location) and
     FileExists(AddBackslash(Location) + '{#AppExe}') then
  begin
    WaitForOldProcess();
    Exec(AddBackslash(Location) + '{#AppExe}', '', Location, SW_SHOWNORMAL, ewNoWait, ResultCode);
  end;
end;
#endif

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
