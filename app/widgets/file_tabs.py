"""Çok dosyalı alıştırmada editörün üstündeki dosya sekmeleri.

Her sekme: dilin simgesi, dosyanın adı; salt okunur dosyada kilit, son
çalıştırmada hata veren dosyada kırmızı nokta. Seçili sekmenin altında vurgu
çizgisi. Kendisi çiziyor (QSS değil): sekmeler editör kartının içinde, kodun
zemininde duruyor ve kartın köşeleriyle uyumlu kalmalı.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from PySide6.QtCore import QRectF, QSize, Qt, Signal
from PySide6.QtGui import QColor, QFont, QFontMetrics, QPainter, QPen
from PySide6.QtWidgets import QWidget

from ..resources.icons import pixmap
from ..resources.theme.tokens import FONTS, PALETTES, mix

# Dilin simgesi.
LANGUAGE_ICONS = {
    "python": "python",
    "tsql": "database",
    "dockerfile": "box",
    "shell": "terminal",
}
DEFAULT_ICON = "file-text"

HEIGHT = 38
PAD_X = 12
ICON = 14
GAP = 6
LOCK = 12
DOT = 6


@dataclass
class _Tab:
    name: str
    language: str
    readonly: bool
    rect: QRectF = field(default_factory=QRectF)


class FileTabs(QWidget):
    """Dosya sekmeleri; seçim değişince `current_changed(ad)`."""

    current_changed = Signal(str)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._tabs: list[_Tab] = []
        self._current = ""
        self._error = ""
        self._hover = -1
        self._mode = "light"
        self._readonly_tip = ""
        self._error_tip = ""
        self.setMouseTracking(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedHeight(HEIGHT)
        font = QFont()
        font.setFamily(FONTS["mono"].split(",")[0].strip().strip('"'))
        font.setPointSizeF(9.5)
        self.setFont(font)

    # --- veri -------------------------------------------------------------

    def set_files(self, files: list[tuple[str, str, bool]]) -> None:
        """Sekmeler: (ad, dil, salt okunur). İlk dosya seçili gelir."""
        self._tabs = [_Tab(name, language, readonly) for name, language, readonly in files]
        self._current = self._tabs[0].name if self._tabs else ""
        self._error = ""
        self._hover = -1
        self._layout()
        self.update()

    @property
    def current(self) -> str:
        return self._current

    @property
    def names(self) -> list[str]:
        return [tab.name for tab in self._tabs]

    def set_current(self, name: str) -> None:
        """Sekmeyi seçer (sinyal yayar; aynıysa bir şey yapmaz)."""
        if name == self._current or name not in self.names:
            return
        self._current = name
        self.update()
        self.current_changed.emit(name)

    def step(self, delta: int) -> None:
        """Sonraki / önceki dosya (uçlarda başa sarıyor)."""
        names = self.names
        if len(names) < 2:
            return
        index = names.index(self._current) if self._current in names else 0
        self.set_current(names[(index + delta) % len(names)])

    def set_error(self, name: str) -> None:
        """Son çalıştırmada hatanın olduğu dosya ("" kaldırır)."""
        if name != self._error:
            self._error = name
            self.update()

    def set_mode(self, mode: str) -> None:
        self._mode = mode
        self.update()

    def set_texts(self, readonly_tip: str, error_tip: str) -> None:
        self._readonly_tip = readonly_tip
        self._error_tip = error_tip

    # --- ölçü ---------------------------------------------------------------

    def _tab_width(self, tab: _Tab) -> float:
        width = PAD_X + ICON + GAP + QFontMetrics(self.font()).horizontalAdvance(tab.name) + PAD_X
        if tab.readonly:
            width += GAP + LOCK
        return width + GAP + DOT

    def _layout(self) -> None:
        x = 6.0
        for tab in self._tabs:
            width = self._tab_width(tab)
            tab.rect = QRectF(x, 4, width, HEIGHT - 4)
            x += width + 2

    def sizeHint(self) -> QSize:  # noqa: N802
        width = sum(self._tab_width(tab) + 2 for tab in self._tabs) + 12
        return QSize(int(width), HEIGHT)

    def _index_at(self, pos) -> int:
        for index, tab in enumerate(self._tabs):
            if tab.rect.contains(pos):
                return index
        return -1

    # --- olaylar ------------------------------------------------------------

    def mouseMoveEvent(self, event) -> None:  # noqa: N802
        index = self._index_at(event.position())
        if index != self._hover:
            self._hover = index
            tip = ""
            if index >= 0:
                tab = self._tabs[index]
                if tab.name == self._error:
                    tip = self._error_tip
                elif tab.readonly:
                    tip = self._readonly_tip
            self.setToolTip(tip)
            self.update()

    def leaveEvent(self, event) -> None:  # noqa: N802
        self._hover = -1
        self.update()
        super().leaveEvent(event)

    def mousePressEvent(self, event) -> None:  # noqa: N802
        if event.button() == Qt.MouseButton.LeftButton:
            index = self._index_at(event.position())
            if index >= 0:
                self.set_current(self._tabs[index].name)

    # --- çizim --------------------------------------------------------------

    def paintEvent(self, event) -> None:  # noqa: N802
        p = PALETTES.get(self._mode, PALETTES["light"])
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        metrics = QFontMetrics(self.font())

        # Alttaki ince çizgi: sekmeler ile kod arasında.
        pen = QPen(QColor(mix(p["border"], p["code_bg"], 0.35)))
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.drawLine(0, self.height() - 1, self.width(), self.height() - 1)

        for index, tab in enumerate(self._tabs):
            rect = tab.rect
            current = tab.name == self._current
            if current or index == self._hover:
                zemin = QColor(p["accent_soft"] if current else p["surface_hover"])
                if not current:
                    zemin.setAlphaF(0.6)
                painter.setPen(Qt.PenStyle.NoPen)
                painter.setBrush(zemin)
                painter.drawRoundedRect(rect.adjusted(0, 0, 0, 6), 8, 8)
            renk = p["text"] if current else p["text_muted"]
            x = rect.left() + PAD_X
            orta = rect.center().y() - 1
            simge = pixmap(LANGUAGE_ICONS.get(tab.language, DEFAULT_ICON),
                           p["accent"] if current else p["text_muted"], ICON)
            painter.drawPixmap(int(x), int(orta - ICON / 2), simge)
            x += ICON + GAP
            painter.setPen(QColor(renk))
            ad_genislik = metrics.horizontalAdvance(tab.name)
            painter.drawText(QRectF(x, rect.top(), ad_genislik + 2, rect.height() - 2),
                             Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, tab.name)
            x += ad_genislik
            if tab.readonly:
                x += GAP
                kilit = pixmap("lock", p["text_muted"], LOCK)
                painter.drawPixmap(int(x), int(orta - LOCK / 2), kilit)
                x += LOCK
            if tab.name == self._error:
                painter.setPen(Qt.PenStyle.NoPen)
                painter.setBrush(QColor(p["danger"]))
                painter.drawEllipse(QRectF(x + GAP, orta - DOT / 2, DOT, DOT))
            if current:
                painter.setPen(Qt.PenStyle.NoPen)
                painter.setBrush(QColor(p["accent"]))
                painter.drawRoundedRect(QRectF(rect.left() + 8, self.height() - 3,
                                               rect.width() - 16, 2.5), 1.25, 1.25)
        painter.end()
