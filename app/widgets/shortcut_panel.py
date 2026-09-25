"""Klavye kısayolları paneli.

Alt şeritteki klavye düğmesine (ya da `F1`) basınca yukarı açılıyor. Kısayollar bir yerde yazılı olmasa kimse
bilmiyordu: `Ctrl+K` arama, `Ctrl+N` not, `Ctrl+Enter` kodu çalıştırma
hiçbir ekranda görünmüyordu.

Liste **kodun kendisinden** değil buradaki tablodan geliyor; yeni bir
kısayol eklenince (`QShortcut`) buraya da bir satır eklenir.
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtCore import QSize
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ..core.language import LanguageManager
from ..resources.icons import icon
from ..resources.theme.tokens import PALETTES, SPACING
from .popover import Popover

PANEL_WIDTH = 330

# (grup anahtarı, [(tuşlar, açıklama anahtarı)])
# Tuşlar olduğu gibi yazılıyor; çevrilmiyorlar.
SHORTCUTS = [
    ("general", [
        (["Ctrl", "K"], "shortcut.search"),
        (["Ctrl", "N"], "shortcut.note"),
        (["Ctrl", ","], "shortcut.settings"),
        (["Ctrl", "M"], "shortcut.menu"),
        (["F1"], "shortcut.list"),
        (["Esc"], "shortcut.back"),
        (["Ctrl", "Z"], "shortcut.undo"),
        (["Ctrl", "Y"], "shortcut.redo"),
    ]),
    ("exercise", [
        (["Ctrl", "Enter"], "shortcut.run"),
        (["Tab"], "shortcut.indent"),
        (["Shift", "Tab"], "shortcut.dedent"),
        (["Ctrl", "/"], "shortcut.comment"),
    ]),
    ("notes", [
        (["Ctrl", "B"], "shortcut.bold"),
        (["↑", "↓", "Enter"], "shortcut.pick"),
    ]),
]


class ShortcutPanel(Popover):
    """Kısayolların listesi."""

    def __init__(self, language: LanguageManager, parent: QWidget | None = None) -> None:
        super().__init__(PANEL_WIDTH, parent)
        self._language = language

        self._title = QLabel()
        self._title.setProperty("role", "popover-title")
        self._title.setContentsMargins(
            SPACING["md"], SPACING["sm"], SPACING["md"], SPACING["sm"]
        )
        self.content.addWidget(self._title)

        divider = QFrame()
        divider.setProperty("role", "divider")
        divider.setFixedHeight(1)
        self.content.addWidget(divider)

        self._body = QWidget()
        self._body.setProperty("role", "bare")
        self._rows = QVBoxLayout(self._body)
        self._rows.setContentsMargins(
            SPACING["md"], SPACING["sm"], SPACING["md"], SPACING["md"]
        )
        self._rows.setSpacing(SPACING["xs"])
        self.content.addWidget(self._body)

        self._labels: list[tuple[QLabel, str]] = []
        self._build()
        self.retranslate()

    def _build(self) -> None:
        for index, (grup, satirlar) in enumerate(SHORTCUTS):
            baslik = QLabel()
            baslik.setProperty("role", "shortcut-group")
            if index:
                baslik.setContentsMargins(0, SPACING["sm"], 0, 0)
            self._rows.addWidget(baslik)
            self._labels.append((baslik, f"shortcut.group.{grup}"))

            for tuslar, anahtar in satirlar:
                self._rows.addWidget(self._row(tuslar, anahtar))

    def _row(self, keys: list[str], anahtar: str) -> QWidget:
        satir = QWidget()
        satir.setProperty("role", "bare")
        duzen = QHBoxLayout(satir)
        duzen.setContentsMargins(0, 2, 0, 2)
        duzen.setSpacing(SPACING["xs"])

        aciklama = QLabel()
        aciklama.setProperty("role", "popover-text")
        aciklama.setWordWrap(True)
        duzen.addWidget(aciklama, 1)
        self._labels.append((aciklama, anahtar))

        for tus in keys:
            etiket = QLabel(tus)
            etiket.setProperty("role", "key")
            etiket.setAlignment(Qt.AlignmentFlag.AlignCenter)
            duzen.addWidget(etiket)
        return satir

    def show_above(self, anchor: QWidget) -> None:
        self.fit_height(self._title.sizeHint().height() + 1 + self._body.sizeHint().height())
        super().show_above(anchor)

    def retranslate(self) -> None:
        self._title.setText(self._language.t("shortcut.title"))
        for etiket, anahtar in self._labels:
            etiket.setText(self._language.t(anahtar))


class ShortcutButton(QPushButton):
    """Alt şeridin sağ ucundaki klavye düğmesi."""

    SIZE = 18
    ICON = 14

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._mode = "dark"
        self.setProperty("variant", "footer-icon")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedSize(self.SIZE, self.SIZE)
        self.set_mode(self._mode)

    def set_mode(self, mode: str) -> None:
        self._mode = mode
        palette = PALETTES.get(mode, PALETTES["dark"])
        self.setIcon(icon("keyboard", palette["text_muted"], self.ICON))
        self.setIconSize(QSize(self.ICON, self.ICON))
