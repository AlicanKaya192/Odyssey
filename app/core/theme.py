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
from PySide6.QtGui import QColor, QFont, QGuiApplication, QPalette
from PySide6.QtWidgets import QApplication

from ..resources.theme.tokens import (
    FONT_SIZES,
    FONTS,
    PALETTES,
    build_variables,
)

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


def build_palette(mode: str) -> QPalette:
    """Qt'nin kendi renk paletini temaya göre kurar.

    Stil dosyası tek başına yetmiyor: Windows yeni bir pencereyi (ayarlar
    kutusu gibi) işletim sisteminin varsayılan fırçasıyla oluşturuyor ve
    Qt daha ilk boyamasını yapmadan bir kare beyaz görünüyor. Aynısı,
    Chromium'un ilk karesi gelene kadar belge alanlarında da oluyordu.
    Paleti de temaya çekince pencere daha doğduğu anda koyu oluyor.
    """
    p = PALETTES.get(mode, PALETTES["light"])
    palette = QPalette()

    zemin = QColor(p["bg"])
    yuzey = QColor(p["surface"])
    metin = QColor(p["text"])

    for grup in (QPalette.ColorGroup.Active, QPalette.ColorGroup.Inactive,
                 QPalette.ColorGroup.Disabled):
        palette.setColor(grup, QPalette.ColorRole.Window, zemin)
        palette.setColor(grup, QPalette.ColorRole.Base, yuzey)
        palette.setColor(grup, QPalette.ColorRole.AlternateBase, QColor(p["surface_alt"]))
        palette.setColor(grup, QPalette.ColorRole.Button, yuzey)
        palette.setColor(grup, QPalette.ColorRole.WindowText, metin)
        palette.setColor(grup, QPalette.ColorRole.Text, metin)
        palette.setColor(grup, QPalette.ColorRole.ButtonText, metin)
        palette.setColor(grup, QPalette.ColorRole.ToolTipBase, yuzey)
        palette.setColor(grup, QPalette.ColorRole.ToolTipText, metin)
        palette.setColor(grup, QPalette.ColorRole.Highlight, QColor(p["accent"]))
        palette.setColor(grup, QPalette.ColorRole.HighlightedText, QColor("#FFFFFF"))

    soluk = QColor(p["text_muted"])
    palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, soluk)
    palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, soluk)
    palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, soluk)

    return palette


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

        app.setPalette(build_palette(self.effective_mode))

        # Stil dosyası **önce boşaltılıyor, sonra veriliyor.**
        #
        # Görünüşte gereksiz bir adım ama ölçüm başka söylüyor: dolu bir stil
        # dosyasının üstüne yenisini yazmak 298 widget'lık ağaçta ~160 ms
        # sürüyor, çünkü Qt önce eskisini her widget'tan söküyor. Önce boşaltıp
        # sonra vermek aynı işi ~36 ms'de bitiriyor (boşaltma 11 ms + verme
        # 22 ms). Tema değişiminde gözle görülen gecikme buradan geliyordu.
        #
        # İki çağrı arasında olay döngüsü çalışmadığı için ekranda stilsiz bir
        # kare görünmüyor; ölçüldü.
        app.setStyleSheet("")
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
