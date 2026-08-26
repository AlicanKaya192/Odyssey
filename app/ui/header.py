"""Ekranların üst şeridi.

Solda geri düğmesi ve başlık, sağda ekrana özel bir denetim (konu ekranında
segmented control) bulunur. Kalabalık bir araç çubuğu yok: başlık, gezinme ve
o ekranın tek işi kadarı duruyor.
"""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from ..core.language import LanguageManager
from ..resources.icons import icon
from ..resources.theme.tokens import PALETTES, SPACING

HEADER_HEIGHT = 76


class ScreenHeader(QFrame):
    """Başlık şeridi."""

    back_clicked = Signal()

    def __init__(self, language: LanguageManager, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._language = language
        self._mode = "light"

        self.setProperty("role", "topbar")
        self.setFixedHeight(HEADER_HEIGHT)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(
            SPACING["lg"], SPACING["md"], SPACING["lg"], SPACING["md"]
        )
        layout.setSpacing(SPACING["md"])

        self._back = QPushButton()
        self._back.setCursor(Qt.CursorShape.PointingHandCursor)
        self._back.clicked.connect(self.back_clicked)
        self._back.hide()
        layout.addWidget(self._back)

        titles = QVBoxLayout()
        titles.setSpacing(0)

        self._title = QLabel()
        self._title.setProperty("role", "subtitle")
        titles.addWidget(self._title)

        self._subtitle = QLabel()
        self._subtitle.setProperty("role", "muted")
        titles.addWidget(self._subtitle)

        layout.addLayout(titles)

        # Esneme başlıkla denetim arasında: ekrana özel denetim (segmented
        # control) sağa yaslanıyor, ortada asılı kalmıyor.
        layout.addStretch(1)

        self._slot = QHBoxLayout()
        self._slot.setSpacing(SPACING["sm"])
        layout.addLayout(self._slot)
        self.set_mode(self._mode)

    def set_titles(self, title: str, subtitle: str = "") -> None:
        self._title.setText(title)
        self._subtitle.setText(subtitle)
        self._subtitle.setVisible(bool(subtitle))

    def set_back(self, visible: bool, text: str = "") -> None:
        """Geri düğmesini gösterir ya da gizler."""
        self._back.setVisible(visible)
        if text:
            self._back.setText(f"  {text}")

    def add_widget(self, widget: QWidget) -> None:
        """Başlığın sağına ekrana özel bir denetim yerleştirir."""
        self._slot.addWidget(widget)

    def set_mode(self, mode: str) -> None:
        self._mode = mode
        palette = PALETTES.get(mode, PALETTES["light"])
        self._back.setIcon(icon("arrow-left", palette["text"], 18))
