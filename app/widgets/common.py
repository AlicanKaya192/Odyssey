"""Arayüzde tekrar tekrar kullanılan küçük parçalar.

Her ekranda yeniden yazmak yerine burada bir kez tanımlanıyor; görünümleri
stil dosyasındaki özelliklerden (`variant`, `role`, `tone`) geliyor.
"""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ..resources.theme.tokens import SPACING
from .effects import apply_shadow, refresh_shadow, repolish


class Card(QFrame):
    """Gölgeli, yuvarlak köşeli kart."""

    def __init__(
        self,
        parent: QWidget | None = None,
        mode: str = "light",
        strong: bool = False,
        padding: int = SPACING["lg"],
    ) -> None:
        super().__init__(parent)
        self._strong = strong
        self.setProperty("surface", "card")
        apply_shadow(self, mode, strong)

        self.body = QVBoxLayout(self)
        self.body.setContentsMargins(padding, padding, padding, padding)
        self.body.setSpacing(SPACING["sm"])

    def set_mode(self, mode: str) -> None:
        refresh_shadow(self, mode, self._strong)


class Chip(QLabel):
    """Küçük etiket: zorluk, süre, durum."""

    def __init__(self, text: str = "", tone: str = "", parent: QWidget | None = None) -> None:
        super().__init__(text, parent)
        self.setProperty("role", "chip")
        if tone:
            self.setProperty("tone", tone)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def set_tone(self, tone: str) -> None:
        self.setProperty("tone", tone)
        repolish(self)


class SegmentedControl(QFrame):
    """Sekme yerine kullanılan yatay seçici.

    Qt'nin `QTabBar`'ı yerine bunu tercih ettim: maketteki görünüme uyuyor,
    seçili öğe yükseltilmiş bir yüzey gibi duruyor ve stil vermesi daha
    öngörülebilir.
    """

    changed = Signal(int)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setProperty("role", "segment-group")

        self._layout = QHBoxLayout(self)
        # Kutu kalktığı için iç dolguya gerek yok; aralık ise arttı, sekmeler
        # birbirine yapışık duruyordu.
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(SPACING["md"])
        self._buttons: list[QPushButton] = []
        self._current = 0

    def set_items(self, labels: list[str]) -> None:
        """Seçenekleri yeniden kurar."""
        while self._layout.count():
            item = self._layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self._buttons = []

        for index, label in enumerate(labels):
            button = QPushButton(label)
            button.setProperty("variant", "segment")
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(lambda _=False, i=index: self.set_current(i))
            self._layout.addWidget(button)
            self._buttons.append(button)

        self._current = min(self._current, max(0, len(labels) - 1))
        self._refresh()

    def set_labels(self, labels: list[str]) -> None:
        """Metinleri değiştirir (dil değişimi), seçimi bozmadan."""
        if len(labels) != len(self._buttons):
            self.set_items(labels)
            return
        for button, label in zip(self._buttons, labels):
            button.setText(label)

    @property
    def current(self) -> int:
        return self._current

    def set_current(self, index: int, notify: bool = True) -> None:
        if not self._buttons:
            return
        index = max(0, min(index, len(self._buttons) - 1))
        changed = index != self._current
        self._current = index
        self._refresh()
        if notify and changed:
            self.changed.emit(index)

    def _refresh(self) -> None:
        for index, button in enumerate(self._buttons):
            button.setProperty("active", "true" if index == self._current else "false")
            repolish(button)


class StatBlock(QWidget):
    """Karşılama kartındaki sayı + açıklama ikilisi."""

    def __init__(
        self,
        value: str = "",
        label: str = "",
        inverse: bool = False,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self._value = QLabel(value)
        self._value.setProperty("role", "title")
        self._label = QLabel(label)
        self._label.setProperty("role", "muted")

        if inverse:
            # Renkli zemin üzerinde duruyorsa metin beyaz olmalı.
            self._value.setStyleSheet("color: #FFFFFF; font-size: 26px; font-weight: 750;")
            self._label.setStyleSheet("color: rgba(255,255,255,0.85); font-size: 12px;")

        layout.addWidget(self._value)
        layout.addWidget(self._label)

    def set_value(self, value: str) -> None:
        self._value.setText(value)

    def set_label(self, label: str) -> None:
        self._label.setText(label)


class Banner(QFrame):
    """Renkli bilgi şeridi: uyarı, başarı, hata."""

    def __init__(
        self,
        text: str = "",
        tone: str = "warning",
        icon: str = "",
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setProperty("banner", tone)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(SPACING["md"], SPACING["sm"], SPACING["md"], SPACING["sm"])
        layout.setSpacing(SPACING["sm"])

        self._icon = QLabel(icon)
        self._icon.setProperty("tone", tone)
        self._icon.setFixedWidth(16)
        self._icon.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self._icon)

        self._label = QLabel(text)
        self._label.setWordWrap(True)
        self._label.setProperty("tone", tone)
        layout.addWidget(self._label, 1)

    def set_text(self, text: str) -> None:
        self._label.setText(text)

    def set_tone(self, tone: str, icon: str = "") -> None:
        self.setProperty("banner", tone)
        self._label.setProperty("tone", tone)
        self._icon.setProperty("tone", tone)
        if icon:
            self._icon.setText(icon)
        repolish(self)
        repolish(self._label)
        repolish(self._icon)


def section_label(text: str) -> QLabel:
    """Küçük, seyrek harfli bölüm başlığı."""
    label = QLabel(text.upper())
    label.setProperty("role", "section")
    return label


def horizontal_rule() -> QFrame:
    line = QFrame()
    line.setProperty("role", "separator")
    line.setFrameShape(QFrame.Shape.HLine)
    line.setFixedHeight(1)
    return line
