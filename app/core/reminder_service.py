"""Hatırlatmaları açma, kapatma ve denetleyiciyi çalıştırma.

Karar mantığı `reminders.py`, Windows'a özgü parçalar `win_notify.py` ve
`reminder_task.py` içinde; burası onları birleştiriyor. Ayarlar penceresi,
ilk açılıştaki soru ve `main.py --reminder-check` buradan geçiyor.
"""

from __future__ import annotations

import threading
from datetime import datetime
from pathlib import Path

from ..paths import install_root
from . import reminder_task, reminders, win_notify


def supported() -> bool:
    return win_notify.supported()


def icon_path() -> Path | None:
    path = install_root() / "app" / "resources" / "icon.png"
    return path if path.exists() else None


def enable(store, at: str | None = None) -> tuple[bool, str]:
    """Hatırlatmaları açar: kimlik kaydı ve zamanlanmış görev.

    Görev kurulamazsa ayar kapalı kalıyor ve hata metni dönüyor; ayar
    "açık" görünüp hiçbir şey olmaması en kötü sonuç olurdu.
    """
    if at:
        store.set_setting(reminders.TIME_KEY, at)
    saat = reminders.reminder_time(store)
    try:
        win_notify.register(icon_path(), reminder_task.launch_command())
    except OSError as exc:
        store.set_setting(reminders.ENABLED_KEY, "0")
        return False, str(exc)
    ok, error = reminder_task.install(saat)
    store.set_setting(reminders.ENABLED_KEY, "1" if ok else "0")
    return ok, error


def disable(store) -> None:
    """Hatırlatmaları kapatır; görevi ve kayıtları siler."""
    store.set_setting(reminders.ENABLED_KEY, "0")
    reminder_task.remove()
    win_notify.unregister()


def decline(store) -> None:
    """İlk açılıştaki soruya "hayır" denildi: bir daha sorulmuyor."""
    store.set_setting(reminders.ENABLED_KEY, "0")


def ensure_async(store) -> None:
    """Açılışta: hatırlatmalar açıksa görevi ve kaydı arka planda tazeler.

    Güncellemeden ya da klasör taşındıktan sonra programın yolu değişmiş
    olabilir; görev eski yolu çağırıp sessizce hiçbir şey yapmasın.
    """
    if not supported() or not reminders.enabled(store):
        return
    saat = reminders.reminder_time(store)
    komut = reminder_task.launch_command()

    def work() -> None:
        try:
            win_notify.register(icon_path(), komut)
            reminder_task.install(saat)
        except Exception:  # noqa: BLE001 - açılışı hiçbir koşulda bozmasın
            pass

    threading.Thread(target=work, name="reminder-refresh", daemon=True).start()


def send_test(store, catalog=None) -> bool:
    """Ayarlardaki "Deneme bildirimi" düğmesi: seri uyarısından bir örnek."""
    win_notify.register(icon_path(), reminder_task.launch_command())
    title, body, _ = reminders.compose(
        store,
        "streak_risk",
        datetime.now(),
        reminders.last_section_title(store, catalog) if catalog is not None else "",
    )
    return win_notify.show_toast(title, body, icon_path())


def run_check() -> str | None:
    """`--reminder-check`: Görev Zamanlayıcı'nın çağırdığı giriş noktası.

    Arayüz kurulmuyor. Program açıksa bildirim gönderilmiyor: kişi zaten
    uygulamanın başında.
    """
    from .catalog import Catalog
    from .progress import ProgressStore
    from ..paths import content_dir

    if win_notify.app_running():
        return None
    store = ProgressStore()
    try:
        catalog = Catalog.load(content_dir())
    except Exception:  # noqa: BLE001 - katalog olmadan da bildirim gidebilir
        catalog = None
    icon = icon_path()
    return reminders.run_check(
        store,
        datetime.now(),
        lambda title, body: win_notify.show_toast(title, body, icon),
        catalog,
    )
