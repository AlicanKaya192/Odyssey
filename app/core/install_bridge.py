"""Güncelleme kurulurken görünen "Odyssey güncelleniyor" penceresi.

Güncelleme penceresi kapanınca kurulum programı sessiz çalışıyor ve yeni
sürüm açılana kadar (on saniyeden bir dakikaya kadar) ekranda hiçbir şey
yoktu; kişi programın çöktüğünü ya da kendisinin açması gerektiğini
sanıyordu (Alican).

Bu pencereyi Odyssey açık tutamaz: kurulum, dosyalarını değiştirebilmek için
eski sürecin kapanmasını bekliyor. Pencere Windows'un kendi PowerShell'i ile
ayrı bir süreçte açılıyor (Windows Forms; bildirim gösterirken de PowerShell
kullanılıyor, `win_notify.py`). Programın renkleri ve güncelleme
penceresinin sentorlu görseli taşınıyor; küçültülebiliyor, görev çubuğunda
Odyssey simgesiyle duruyor.

**Ne zaman kapanıyor:** kurulum süreci bitince yeni Odyssey'in açıldığını
gösteren kilit (`win_notify.MUTEX_NAME`) beklenip pencere kapanıyor; kilit
25 sn'de gelmezse yine kapanıyor. Kurulum hata koduyla biterse pencere
kapanmıyor, ne yapılacağını yazıyor. Her ihtimale karşı 10 dakikada kapanır.

Görsel ve simge `updates/` klasörüne kopyalanıyor ve belleğe okunuyor:
kurulum programın kendi dosyalarını değiştirirken kilitli kalmasınlar.
"""

from __future__ import annotations

import base64
import shutil
import subprocess
import sys
from pathlib import Path

from . import log
from .win_notify import MUTEX_NAME

_log = log.get(__name__)


def _ps(text: str) -> str:
    """PowerShell tek tırnaklı dize."""
    return "'" + str(text).replace("'", "''") + "'"


def _rgb(hex_color: str) -> str:
    h = hex_color.lstrip("#")
    return f"[System.Drawing.Color]::FromArgb({int(h[0:2], 16)},{int(h[2:4], 16)},{int(h[4:6], 16)})"


def script(pid: int, texts: dict, colors: dict, icon: Path | None, image: Path | None) -> str:
    """Pencereyi açan PowerShell betiği (test için ayrı)."""
    ikon = _ps(icon) if icon else "''"
    gorsel = _ps(image) if image else "''"
    return f"""
$ErrorActionPreference = 'SilentlyContinue'
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
[System.Windows.Forms.Application]::EnableVisualStyles()
# Ekran ölçeğini bilen pencere: yoksa Windows %125'te bitmap'i büyütüyor ve
# yazılar bulanıklaşıyordu. Ölçüler `S` ile ölçeğe çevriliyor; yazı tipleri
# punto olduğu için kendiliğinden büyüyor.
try {{
  Add-Type -Namespace OdysseyBridge -Name Win -MemberDefinition '[DllImport("user32.dll")] public static extern bool SetProcessDPIAware(); [DllImport("dwmapi.dll")] public static extern int DwmSetWindowAttribute(System.IntPtr h, int a, ref int v, int s);'
  [OdysseyBridge.Win]::SetProcessDPIAware() | Out-Null
}} catch {{}}
$k = [System.Drawing.Graphics]::FromHwnd([System.IntPtr]::Zero).DpiX / 96.0
function script:S($v) {{ return [int][Math]::Round($v * $k) }}
$proc = Get-Process -Id {int(pid)}
# Tutamaç süreç bitmeden açılmalı; yoksa ExitCode sonradan okunamıyor.
if ($proc -ne $null) {{ $null = $proc.Handle }}
$f = New-Object System.Windows.Forms.Form
$f.Text = {_ps(texts['title'])}
$f.FormBorderStyle = 'FixedSingle'
$f.MaximizeBox = $false
$f.MinimizeBox = $true
$f.StartPosition = 'CenterScreen'
$f.ShowInTaskbar = $true
$f.BackColor = {_rgb(colors['bg'])}
$ikon = {ikon}
if ($ikon -and (Test-Path $ikon)) {{ $f.Icon = New-Object System.Drawing.Icon($ikon) }}
$y = S 20
$gorsel = {gorsel}
if ($gorsel -and (Test-Path $gorsel)) {{
  $resim = [System.Drawing.Image]::FromStream((New-Object System.IO.MemoryStream(,[System.IO.File]::ReadAllBytes($gorsel))))
  $pb = New-Object System.Windows.Forms.PictureBox
  $pb.Image = $resim
  $pb.SizeMode = 'Zoom'
  $pb.SetBounds((S 20), (S 20), (S 500), [int]((S 500) * $resim.Height / $resim.Width))
  $f.Controls.Add($pb)
  $y = $pb.Bottom + (S 18)
}}
$h = New-Object System.Windows.Forms.Label
$h.Text = {_ps(texts['heading'])}
$h.ForeColor = {_rgb(colors['text'])}
$h.Font = New-Object System.Drawing.Font('Segoe UI', 14, [System.Drawing.FontStyle]::Bold)
$h.SetBounds((S 18), $y, (S 504), (S 34))
$f.Controls.Add($h)
$t = New-Object System.Windows.Forms.Label
$t.Text = {_ps(texts['text'])}
$t.ForeColor = {_rgb(colors['muted'])}
$t.Font = New-Object System.Drawing.Font('Segoe UI', 10)
$t.SetBounds((S 20), ($y + (S 40)), (S 500), (S 44))
$f.Controls.Add($t)
function script:Yuvarlak($x, $yy, $w, $hh) {{
  $yol = New-Object System.Drawing.Drawing2D.GraphicsPath
  $yol.AddArc($x, $yy, $hh, $hh, 90, 180)
  $yol.AddArc($x + $w - $hh, $yy, $hh, $hh, 270, 180)
  $yol.CloseFigure()
  return $yol
}}
$bar = New-Object System.Windows.Forms.PictureBox
$bar.SetBounds((S 20), ($y + (S 96)), (S 500), (S 6))
$bar.BackColor = $f.BackColor
$script:poz = 0.0
$bar.Add_Paint({{
  param($s, $e)
  $g = $e.Graphics
  $g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
  $w = $s.Width - 1; $hh = $s.Height - 1
  $iz = Yuvarlak 0 0 $w $hh
  $g.FillPath((New-Object System.Drawing.SolidBrush({_rgb(colors['track'])})), $iz)
  $g.SetClip($iz)
  # Kayan parça: yavaşlayıp hızlanarak (kosinüs) soldan sağa.
  $u = (1 - [Math]::Cos([Math]::PI * $script:poz)) / 2
  $parca = [int]($w * 0.34)
  $x = [int](($w + $parca) * $u) - $parca
  $alan = New-Object System.Drawing.Rectangle($x, 0, $parca, ($hh + 1))
  $firca = New-Object System.Drawing.Drawing2D.LinearGradientBrush($alan, {_rgb(colors['accent'])}, {_rgb(colors['accent2'])}, 0.0)
  $g.FillPath($firca, (Yuvarlak $x 0 $parca $hh))
}})
$f.Controls.Add($bar)
$akis = New-Object System.Windows.Forms.Timer
$akis.Interval = 16
$akis.Add_Tick({{ $script:poz = ($script:poz + 0.008) % 1.0; $bar.Invalidate() }})
$f.ClientSize = New-Object System.Drawing.Size((S 540), ($y + (S 126)))
$script:basla = Get-Date
$script:bitti = $null
$zaman = New-Object System.Windows.Forms.Timer
$zaman.Interval = 400
$zaman.Add_Tick({{
  if ($script:bitti -eq $null) {{
    if ($proc -eq $null -or $proc.HasExited) {{
      $kod = 0
      try {{ if ($proc -ne $null) {{ $kod = $proc.ExitCode }} }} catch {{ $kod = 0 }}
      if ($kod -ne $null -and $kod -ne 0) {{
        $h.Text = {_ps(texts['error_heading'])}
        $t.Text = {_ps(texts['error_text'])}
        $bar.Visible = $false
        $akis.Stop()
        $zaman.Stop()
        return
      }}
      $script:bitti = Get-Date
    }}
  }} else {{
    $m = $null
    if ([System.Threading.Mutex]::TryOpenExisting({_ps(MUTEX_NAME)}, [ref]$m)) {{ $m.Dispose(); $f.Close() }}
    elseif (((Get-Date) - $script:bitti).TotalSeconds -gt 25) {{ $f.Close() }}
  }}
  if (((Get-Date) - $script:basla).TotalMinutes -gt 10) {{ $f.Close() }}
}})
$f.Add_Shown({{
  try {{
    $koyu = {1 if colors.get('dark') else 0}
    [OdysseyBridge.Win]::DwmSetWindowAttribute($f.Handle, 20, [ref]$koyu, 4) | Out-Null
  }} catch {{}}
  $f.Activate()
}})
$zaman.Start()
$akis.Start()
[System.Windows.Forms.Application]::Run($f)
"""


def show(pid: int, texts: dict, colors: dict, icon: Path | None = None,
         image: Path | None = None, folder: Path | None = None) -> bool:
    """Pencereyi ayrı bir süreçte açar; açılamazsa False (güncelleme yine sürer)."""
    if sys.platform != "win32":
        return False
    try:
        if folder is not None:
            folder.mkdir(parents=True, exist_ok=True)
            if icon is not None and icon.exists():
                kopya = folder / "bridge-icon.ico"
                shutil.copyfile(icon, kopya)
                icon = kopya
        kod = script(pid, texts, colors, icon, image)
        subprocess.Popen(
            ["powershell.exe", "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass",
             "-EncodedCommand", base64.b64encode(kod.encode("utf-16-le")).decode()],
            creationflags=subprocess.CREATE_NO_WINDOW | subprocess.CREATE_NEW_PROCESS_GROUP,
            stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            close_fds=True,
        )
        return True
    except Exception:  # noqa: BLE001 — pencere çıkmazsa güncelleme yine sürer
        _log.exception("Kurulum penceresi açılamadı")
        return False
