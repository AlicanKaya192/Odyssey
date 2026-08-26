"""Uygulamanın giriş noktası.

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
from app.version import APP_VERSION  # noqa: E402

MIN_PYTHON = (3, 10)


def check_python() -> None:
    if sys.version_info[:2] < MIN_PYTHON:
        raise SystemExit(
            f"Bu uygulama Python {MIN_PYTHON[0]}.{MIN_PYTHON[1]} veya üstünü "
            f"gerektiriyor. Şu an {sys.version.split()[0]} kullanılıyor."
        )


def main() -> int:
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

    from app.core.progress import ProgressStore
    from app.ui.main_window import MainWindow

    application = QApplication(sys.argv)
    application.setApplicationName("Proje A")
    application.setApplicationVersion(APP_VERSION)

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
