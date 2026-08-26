"""Odyssey — uygulamanın giriş noktası.

Çalıştırmak için:
    .venv\\Scripts\\python app\\main.py
"""

from __future__ import annotations

import sys
from pathlib import Path

# Doğrudan `python app/main.py` ile çalıştırıldığında proje kökü içe aktarma
# yolunda olmuyor; bunu elle ekliyoruz.
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.language import LanguageManager  # noqa: E402
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


def _claim_taskbar_identity() -> None:
    """Windows görev çubuğunda uygulamanın kendi simgesini göstermesini sağlar.

    Aksi hâlde Windows uygulamayı "Python" sayıyor ve simgesini pencereye
    verdiğimiz simgeyle değiştirmiyor. Kendimize ayrı bir kimlik tanıtınca
    görev çubuğu doğru simgeyi çiziyor.
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
    from app.ui.main_window import MainWindow

    application = QApplication(sys.argv)
    application.setApplicationName("Odyssey")
    application.setApplicationVersion(APP_VERSION)

    _claim_taskbar_identity()
    icon_path = Path(__file__).resolve().parent / "resources" / "icon.ico"
    if icon_path.exists():
        application.setWindowIcon(QIcon(str(icon_path)))

    # Ayarlar kullanıcının kendi bilgisayarındaki veritabanından okunuyor.
    store = ProgressStore()
    language = LanguageManager(store.setting("language", "tr"))
    theme = ThemeManager(store.setting("theme", "system"))
    theme.apply(application)

    window = MainWindow(language, theme, store)
    # Tema başlangıçta da görünümlere bildirilsin.
    window._on_theme_changed(theme.effective_mode)
    window.show()

    return application.exec()


if __name__ == "__main__":
    raise SystemExit(main())
