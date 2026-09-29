"""Çalışma kâğıdının üstündeki matematik sembolleri.

Elle çizmesi zor ya da düzgün çizilmesi zaman alan birkaç işaret. Bir
sembole basınca kâğıt onu "damga" olarak hazırlıyor; kâğıda tıklanan yere
konuyor.

**Liste kısa tutuluyor.** Önce otuz sembol vardı; kâğıdın yanında bir
klavye gibi duruyor ve yer kaplıyordu (Alican: "bu kadar fazla sembole
gerek yok"). Kişi `+ - = ( ) x` gibi işaretleri zaten çiziyor; palet
yalnızca elle çizilince kötü görünenleri veriyor.

İki grup var:

- **Genel semboller** her problemde aynı (`GENERAL_SYMBOLS`).
- **Probleme özel semboller** `exercise.json` → `symbols` listesinden
  geliyor (`log₂`, `3⁴⁰` gibi o soruda sık yazılacak ifadeler) ve genel
  listenin **önünde** duruyor.
"""

from __future__ import annotations

from PySide6.QtCore import QRectF, Qt, QTimer, Signal
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import QFrame, QHBoxLayout, QPushButton, QWidget

from . import motion
from ..resources.theme.tokens import SPACING
from .effects import repolish

# Elle çizmesi zor olanlar: kök işareti, pi, eşitsizlikler, sonsuz.
GENERAL_SYMBOLS = ["√", "π", "≠", "≤", "≥", "∞"]

BUTTON_SIZE = 36


class _Pulse(QWidget):
    """Seçili sembolün çevresinde, kâğıda konana kadar atan nabız (C8)."""

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self._clock = 0
        self._timer = QTimer(self)
        self._timer.setInterval(33)
        self._timer.timeout.connect(self._tick)
        self.hide()

    def follow(self, button: QWidget) -> None:
        if not motion.enabled():
            return
        self.setGeometry(button.geometry().adjusted(-5, -5, 5, 5))
        self._clock = 0
        self.show()
        self.raise_()
        self._timer.start()

    def stop(self) -> None:
        self._timer.stop()
        self.hide()

    def _tick(self) -> None:
        self._clock = (self._clock + 33) % 1200
        self.update()

    def paintEvent(self, event) -> None:  # noqa: N802
        import math

        from .effects import theme_palette

        k = (1 - math.cos(self._clock / 1200 * 2 * math.pi)) / 2
        renk = QColor(theme_palette()["accent"])
        renk.setAlphaF(0.35 * k)
        g = QPainter(self)
        g.setRenderHint(QPainter.RenderHint.Antialiasing)
        g.setPen(QPen(renk, 4))
        g.setBrush(Qt.BrushStyle.NoBrush)
        g.drawRoundedRect(QRectF(self.rect()).adjusted(2, 2, -2, -2), 12, 12)


class SymbolPalette(QWidget):
    """Tek satırlık sembol şeridi. Seçilen sembol `picked` ile bildiriliyor."""

    picked = Signal(str)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._buttons: list[QPushButton] = []
        self._special: list[str] = []

        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(4)

        # Özel semboller solda; araya ince bir ayırıcı giriyor.
        self._special_slot = QHBoxLayout()
        self._special_slot.setSpacing(4)
        self._layout.addLayout(self._special_slot)

        self._divider = QFrame()
        self._divider.setFrameShape(QFrame.Shape.VLine)
        self._divider.setProperty("role", "divider")
        self._divider.setFixedWidth(1)
        self._layout.addWidget(self._divider)
        self._layout.addSpacing(SPACING["xs"])

        for symbol in GENERAL_SYMBOLS:
            self._layout.addWidget(self._make_button(symbol))
        self._layout.addStretch(1)

        self._divider.hide()
        self._pulse = _Pulse(self)

    def _make_button(self, symbol: str) -> QPushButton:
        button = QPushButton(symbol)
        button.setProperty("variant", "symbol")
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        # Yazı tipi ve yükseklik QSS'te (`variant="symbol"`): genel düğme
        # kuralı `font-size` ve `min-height` verdiği için koddan verilen
        # değerler eziliyordu.
        button.setProperty("long", "true" if len(symbol) > 2 else "false")
        button.setMinimumWidth(BUTTON_SIZE)
        button.clicked.connect(lambda _=False, s=symbol, b=button: self._pick(s, b))
        self._buttons.append(button)
        return button

    def set_special(self, symbols: list[str]) -> None:
        """Probleme özel sembolleri kurar; yoksa ayırıcı da gizleniyor."""
        if symbols == self._special:
            return
        while self._special_slot.count():
            item = self._special_slot.takeAt(0)
            widget = item.widget()
            if widget is not None:
                self._buttons.remove(widget)
                widget.deleteLater()
        self._special = list(symbols)
        for symbol in symbols:
            self._special_slot.addWidget(self._make_button(symbol))
        self._divider.setVisible(bool(symbols))

    def _pick(self, symbol: str, button: QPushButton) -> None:
        self.clear_selection()
        button.setProperty("active", "true")
        repolish(button)
        self._pulse.follow(button)
        self.picked.emit(symbol)

    def clear_selection(self) -> None:
        if hasattr(self, "_pulse"):
            self._pulse.stop()
        for button in self._buttons:
            if button.property("active") == "true":
                button.setProperty("active", "false")
                repolish(button)
