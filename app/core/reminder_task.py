"""Hatırlatma denetleyicisinin Windows Görev Zamanlayıcı görevi.

**Neden hizmet değil:** Windows hizmetleri kullanıcı oturumundan ayrı bir
yerde (oturum 0) çalışıyor ve ekrana bildirim gösteremiyor; kurmak için
yönetici izni de gerekiyor. Zamanlanmış görev kullanıcının kendi hesabında,
izinsiz kuruluyor ve yalnızca birkaç saniye çalışıp kapanıyor.

Görev iki tetikleyiciyle kuruluyor: seçilen saat ve (saat 21:30'dan
önceyse) 21:30 "son çağrı" için. `StartWhenAvailable`: bilgisayar o saatte
kapalıysa açıldığında bir kez çalışıyor; karar mantığı (`reminders.decide`)
saatin geçip geçmediğine yine kendisi bakıyor.

Uygulama her açılışta, hatırlatmalar açıksa görevi yeniden yazıyor
(`ensure`): güncellemeden ya da taşımadan sonra programın yolu değişmiş
olabilir.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from datetime import date, time
from pathlib import Path
from xml.sax.saxutils import escape

from ..paths import install_root, is_frozen

TASK_NAME = "Odyssey Reminder"
CHECK_FLAG = "--reminder-check"
LAST_CALL = time(21, 30)


def launch_parts() -> tuple[str, list[str]]:
    """Odyssey'i penceresiz başlatan program ve argümanları.

    Paketlenmiş hâlde `Odyssey.exe`. Kaynaktan çalışırken `pythonw.exe`
    (konsol penceresi açılmasın diye) ve `app/main.py`.
    """
    if is_frozen():
        return sys.executable, []
    python = Path(sys.executable)
    pythonw = python.with_name("pythonw.exe")
    program = pythonw if pythonw.exists() else python
    return str(program), [str(install_root() / "app" / "main.py")]


def launch_command() -> str:
    """`odyssey://` bağlantısının açacağı komut satırı."""
    program, args = launch_parts()
    return " ".join(f'"{part}"' for part in [program, *args])


def task_xml(at: time) -> str:
    program, args = launch_parts()
    arguments = " ".join(f'"{a}"' for a in args + [CHECK_FLAG])
    start = date.today().isoformat()
    triggers = [at]
    if at < LAST_CALL:
        triggers.append(LAST_CALL)
    trigger_xml = "".join(
        "<CalendarTrigger>"
        f"<StartBoundary>{start}T{t.strftime('%H:%M')}:00</StartBoundary>"
        "<Enabled>true</Enabled>"
        "<ScheduleByDay><DaysInterval>1</DaysInterval></ScheduleByDay>"
        "</CalendarTrigger>"
        for t in triggers
    )
    return (
        '<?xml version="1.0" encoding="UTF-16"?>'
        '<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">'
        "<RegistrationInfo><Description>Odyssey: günlük seri hatırlatması</Description>"
        "</RegistrationInfo>"
        f"<Triggers>{trigger_xml}</Triggers>"
        "<Principals><Principal id=\"Author\"><LogonType>InteractiveToken</LogonType>"
        "<RunLevel>LeastPrivilege</RunLevel></Principal></Principals>"
        "<Settings>"
        "<MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>"
        "<DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>"
        "<StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>"
        "<StartWhenAvailable>true</StartWhenAvailable>"
        "<RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>"
        "<IdleSettings><StopOnIdleEnd>false</StopOnIdleEnd><RestartOnIdle>false</RestartOnIdle>"
        "</IdleSettings>"
        "<AllowStartOnDemand>true</AllowStartOnDemand>"
        "<Enabled>true</Enabled>"
        "<Hidden>false</Hidden>"
        "<ExecutionTimeLimit>PT2M</ExecutionTimeLimit>"
        "<Priority>7</Priority>"
        "</Settings>"
        '<Actions Context="Author"><Exec>'
        f"<Command>{escape(program)}</Command>"
        f"<Arguments>{escape(arguments)}</Arguments>"
        "</Exec></Actions>"
        "</Task>"
    )


def _schtasks(*args: str) -> subprocess.CompletedProcess:
    # Çıktı konsolun OEM kod sayfasında (Türkçe Windows'ta cp857). Varsayılan
    # kodlamayla okununca çözme hatası okuyucu iş parçacığında kalıyor ve
    # `stdout` None dönüyordu (ölçüldü).
    return subprocess.run(
        ["schtasks.exe", *args],
        capture_output=True,
        text=True,
        encoding="oem",
        errors="replace",
        creationflags=subprocess.CREATE_NO_WINDOW,
        timeout=30,
    )


def install(at: time, name: str = TASK_NAME) -> tuple[bool, str]:
    """Görevi kurar ya da üzerine yazar. (başarılı mı, hata metni)"""
    if sys.platform != "win32":
        return False, "unsupported"
    with tempfile.TemporaryDirectory() as folder:
        path = Path(folder) / "task.xml"
        # schtasks XML'i UTF-16 bekliyor.
        path.write_text(task_xml(at), encoding="utf-16")
        try:
            result = _schtasks("/Create", "/TN", name, "/XML", str(path), "/F")
        except (OSError, subprocess.SubprocessError) as exc:
            return False, str(exc)
    return result.returncode == 0, (result.stderr or result.stdout or "").strip()


def remove(name: str = TASK_NAME) -> None:
    if sys.platform != "win32":
        return
    try:
        _schtasks("/Delete", "/TN", name, "/F")
    except (OSError, subprocess.SubprocessError):
        pass


def installed(name: str = TASK_NAME) -> bool:
    if sys.platform != "win32":
        return False
    try:
        return _schtasks("/Query", "/TN", name).returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False
