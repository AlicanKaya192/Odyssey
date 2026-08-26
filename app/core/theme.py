"""Tema yönetimi.

`base.qss` şablonundaki `@isim@` yer tutucularını seçili temanın
belirteçleriyle doldurup uygulamaya uygular. Tema değiştiğinde
`theme_changed` sinyali yayılır; ekranlar gerekiyorsa buna bağlanır.

Kullanılabilir modlar:
    "light"  — açık tema
    "dark"   — koyu tema
    "system" — işletim sisteminin tercihini takip eder
"""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QObject, Qt, Signal
from PySide6.QtGui import QFont, QGuiApplication
from PySide6.QtWidgets import QApplication

from ..resources.theme.tokens import FONT_SIZES, FONTS, build_variables

QSS_TEMPLATE = Path(__file__).resolve().parent.parent / "resources" / "theme" / "base.qss"

MODES = ("light", "dark", "system")


def resolve_mode(mode: str) -> str:
    """"system" seçiliyse işletim sisteminin temasını bulur."""
    if mode != "system":
        return mode if mode in ("light", "dark") else "light"

    hints = QGuiApplication.styleHints()
    # Qt 6.5 ve üstünde colorScheme() var; yoksa açık temaya düşüyoruz.
    scheme = getattr(hints, "colorScheme", None)
    if scheme is not None and scheme() == Qt.ColorScheme.Dark:
        return "dark"
    return "light"


def build_stylesheet(mode: str) -> str:
    """Şablonu seçili temanın renkleriyle doldurup QSS metnini döndürür."""
    variables = build_variables(resolve_mode(mode))
    stylesheet = QSS_TEMPLATE.read_text(encoding="utf-8")

    for name, value in variables.items():
        stylesheet = stylesheet.replace(f"@{name}@", str(value))

    return stylesheet


class ThemeManager(QObject):
    """Uygulamanın temasını tutar ve değiştirir."""

    theme_changed = Signal(str)

    def __init__(self, mode: str = "system") -> None:
        super().__init__()
        self._mode = mode if mode in MODES else "system"

    @property
    def mode(self) -> str:
        """Kullanıcının seçtiği mod ("light", "dark" veya "system")."""
        return self._mode

    @property
    def effective_mode(self) -> str:
        """Ekranda gerçekten uygulanan mod ("light" veya "dark")."""
        return resolve_mode(self._mode)

    def apply(self, app: QApplication | None = None) -> None:
        """Temayı uygulamaya uygular."""
        app = app or QApplication.instance()
        if app is None:
            return

        font = QFont()
        # tokens.py'deki liste virgülle ayrılmış ve tırnaklı; ilk adı alıyoruz.
        family = FONTS["ui"].split(",")[0].strip().strip('"')
        font.setFamily(family)
        font.setPointSizeF(FONT_SIZES["md"] * 0.75)  # px -> pt
        app.setFont(font)

        app.setStyleSheet(build_stylesheet(self._mode))

    def set_mode(self, mode: str) -> None:
        """Temayı değiştirir ve anında uygular."""
        if mode not in MODES or mode == self._mode:
            return
        self._mode = mode
        self.apply()
        self.theme_changed.emit(self.effective_mode)

    def toggle(self) -> None:
        """Açık ve koyu tema arasında geçiş yapar."""
        self.set_mode("dark" if self.effective_mode == "light" else "light")
