"""Odyssey — uygulamanın giriş noktası.

Çalıştırmak için:
    .venv\\Scripts\\python app\\main.py
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

# Doğrudan `python app/main.py` ile çalıştırıldığında proje kökü içe aktarma
# yolunda olmuyor; bunu elle ekliyoruz.
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.language import (  # noqa: E402
    AVAILABLE_LANGUAGES,
    LanguageManager,
    system_language,
)
from app.core.theme import ThemeManager  # noqa: E402
from app.core.runner import HARNESS_FLAG  # noqa: E402
from app.version import APP_VERSION  # noqa: E402

MIN_PYTHON = (3, 10)


def _run_harness_if_asked() -> bool:
    """Uygulama denetleyici olarak mı çağrıldı?

    Paketlenmiş `.exe` içinde ayrı bir `python.exe` yok. Alıştırma kodunu
    ayrı bir süreçte çalıştırmak için uygulama kendini `--run-harness`
    bayrağıyla çağırıyor; bu durumda arayüz hiç kurulmadan `sandbox/harness.py`
    çalıştırılıyor.

    Çalıştırıldıysa True döner ve program orada biter.
    """
    if len(sys.argv) < 3 or sys.argv[1] != HARNESS_FLAG:
        return False

    from app.paths import sandbox_dir

    harness = sandbox_dir() / "harness.py"
    source = harness.read_text(encoding="utf-8")

    # Denetleyici tek başına ayakta duran bir script; kendi `main()`'ini
    # çalıştırması için argümanları onun beklediği hâle getiriyoruz.
    sys.argv = [str(harness), sys.argv[2]]
    exec(compile(source, str(harness), "exec"), {"__name__": "__main__", "__file__": str(harness)})
    return True


def _icon_file():
    """Uygulama simgesinin yolu.

    `install_root()` üzerinden çözülüyor; paketlenmiş hâlde dosyalar
    `_internal` altına taşındığı için `__file__`'a göre hesaplamak orada
    yanlış yere bakıyordu. Bulunamazsa `.png` ile deneniyor.
    """
    from app.paths import install_root

    root = install_root() / "app" / "resources"
    for name in ("icon.ico", "icon.png"):
        candidate = root / name
        if candidate.exists():
            return candidate
    return None


def _claim_taskbar_identity() -> None:
    """Windows görev çubuğunda uygulamanın kendi simgesini göstermesini sağlar.

    Aksi hâlde Windows uygulamayı "Python" sayıyor ve simgesini pencereye
    verdiğimiz simgeyle değiştirmiyor. Kendimize ayrı bir kimlik tanıtınca
    görev çubuğu doğru simgeyi çiziyor.

    Ölçüldü: bu çağrı olmadan kaynaktan çalıştırıldığında görev çubuğunda
    Python'un simgesi çıkıyor, uygulamanınki değil.
    """
    if sys.platform != "win32":
        return

    try:
        import ctypes

        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            "AlicanKaya.Odyssey"
        )
    except Exception:
        # Simge biraz yanlış görünsün ama uygulama açılsın.
        pass


def check_python() -> None:
    if sys.version_info[:2] < MIN_PYTHON:
        raise SystemExit(
            f"Bu uygulama Python {MIN_PYTHON[0]}.{MIN_PYTHON[1]} veya üstünü "
            f"gerektiriyor. Şu an {sys.version.split()[0]} kullanılıyor."
        )


def main() -> int:
    # Denetleyici olarak çağrıldıysak arayüzü hiç kurmadan işi yapıp çıkıyoruz.
    if _run_harness_if_asked():
        return 0

    check_python()

    try:
        from PySide6.QtWidgets import QApplication
    except ImportError as exc:
        raise SystemExit(
            "PySide6 yüklenemedi. Ortamı kurmak için:\n"
            "    py -3.14 tools/setup_env.py\n\n"
            "Not: Sanal ortamı Anaconda'nın Python'u ile kurma; Anaconda'nın\n"
            "taşıdığı eski MSVC kütüphaneleri Qt'nin açılmasını engelliyor.\n\n"
            f"Ayrıntı: {exc}"
        ) from exc

    from PySide6.QtGui import QIcon

    from app.core.progress import ProgressStore
    from app.ui.splash import close_splash, show_splash

    # `main_window` burada içe aktarılmıyor: QtWebEngine'i o zincir yüklüyor
    # ve birkaç saniye sürüyor. Açılış ekranı tam o beklemeyi göstermek için
    # var, dolayısıyla ondan **sonra** aktarılıyor.

    application = QApplication(sys.argv)
    application.setApplicationName("Odyssey")
    application.setApplicationVersion(APP_VERSION)

    _claim_taskbar_identity()
    icon_path = _icon_file()
    icon = QIcon(str(icon_path)) if icon_path else QIcon()
    if not icon.isNull():
        application.setWindowIcon(icon)

    # Ayarlar kullanıcının kendi bilgisayarındaki veritabanından okunuyor.
    # Bu ucuz bir iş; açılış ekranından önce yapılıyor ki ekran doğru temada
    # açılsın. Ağır olan kısım ana pencerenin kurulması (Chromium).
    store = ProgressStore()
    theme = ThemeManager(store.setting("theme", "system"))
    theme.apply(application)

    # Açılış ekranı, ağır kurulum başlamadan önce açılıyor: o kurulum bitene
    # kadar ekranda hiçbir belirti olmuyordu ve uygulama açılmamış gibi
    # duruyordu.
    splash_started = time.monotonic()
    splash = show_splash(icon_path, theme.effective_mode)
    application.processEvents()

    # İlk açılışta dil, bilgisayarın diline göre seçiliyor ve kaydediliyor.
    # Kayıtlı bir seçim varsa ona dokunulmuyor: kullanıcı ayarlardan İngilizce
    # dediyse, Türkçe bir Windows'ta bile İngilizce açılmalı.
    saved_language = store.setting("language", "")
    if saved_language not in AVAILABLE_LANGUAGES:
        saved_language = system_language()
        store.set_setting("language", saved_language)
    language = LanguageManager(saved_language)

    # Ağır kısım burada: bu satır QtWebEngine'i yüklüyor.
    from app.ui.main_window import MainWindow

    window = MainWindow(language, theme, store)
    # Simge pencereye de ayrıca veriliyor. Windows görev çubuğu ve Alt+Tab
    # listesi uygulamanınkini değil, pencerenin kendi simgesini okuyor.
    if not icon.isNull():
        window.setWindowIcon(icon)
    # Tema başlangıçta da görünümlere bildirilsin.
    window._on_theme_changed(theme.effective_mode)
    window.show()

    close_splash(splash, window, splash_started)

    # Beta uyarısı pencere göründükten sonra çıkıyor; boş ekranın önünde
    # açılan bir kutu, uygulamanın açılmadığı izlenimi veriyor.
    from app.ui.beta_notice import BetaNoticeDialog, mark_seen, should_show

    if should_show(store):
        from app.ui import titlebar

        notice = BetaNoticeDialog(language, window)
        titlebar.apply(notice, theme.effective_mode)
        notice.exec()
        mark_seen(store)

    return application.exec()


if __name__ == "__main__":
    raise SystemExit(main())
