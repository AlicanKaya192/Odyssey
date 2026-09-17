"""Çalışma kâğıdının solundaki matematik sembolleri.

Klavyede yazılması zor ya da kısayolu bilinmeyen işaretler. Bir sembole
basınca kâğıt onu "damga" olarak hazırlıyor; kâğıda tıklanan yere konuyor.

İki grup var:

- **Genel semboller** her problemde aynı; hepsi uygulamanın içinde tanımlı.
- **Probleme özel semboller** `exercise.json` → `symbols` listesinden geliyor
  (`log₂`, `log₃` gibi o soruda sık yazılacak ifadeler) ve genel listenin
  **önünde** duruyor: o soruda en çok gerekecek olan en kolay bulunan yerde.
"""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QGridLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from ..resources.theme.tokens import SPACING
from .effects import repolish

# Genel semboller. Sıra: işlemler, karşılaştırma, kuvvet ve kök, sabitler ve
# fonksiyonlar, mantık ve kümeler, Grek harfleri. Klavyede doğrudan yazılan
# `+ - = ( )` yok; kişi onları zaten çiziyor.
GENERAL_SYMBOLS = [
    "×", "÷", "±", "·",
    "≠", "≈", "≤", "≥",
    "²", "³", "ⁿ", "⁻¹",
    "√", "∛", "|x|", "%",
    "π", "e", "∞", "°",
    "log", "ln", "Σ", "∫",
    "⇒", "⇔", "∈", "∅",
    "α", "β", "θ", "Δ",
]

# Tek başına küçük ve düğmenin tepesine yapışık görünen işaretler düğmede
# kutuyla gösteriliyor ("□²" gibi, hesap makinesi klavyelerindeki alışkanlık);
# kâğıda yine yalnızca işaretin kendisi konuyor.
BUTTON_LABELS = {"²": "□²", "³": "□³", "ⁿ": "□ⁿ", "⁻¹": "□⁻¹"}

COLUMNS = 4
BUTTON_SIZE = 38


class SymbolPalette(QWidget):
    """Sembol düğmeleri. Seçilen sembol `picked` ile bildiriliyor."""

    picked = Signal(str)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._buttons: list[QPushButton] = []
        self._special: list[str] = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(SPACING["xs"])

        self._special_label = QLabel()
        self._special_label.setProperty("role", "muted")
        layout.addWidget(self._special_label)
        self._special_grid = QGridLayout()
        self._special_grid.setSpacing(4)
        layout.addLayout(self._special_grid)

        self._general_label = QLabel()
        self._general_label.setProperty("role", "muted")
        layout.addWidget(self._general_label)
        general = QGridLayout()
        general.setSpacing(4)
        for index, symbol in enumerate(GENERAL_SYMBOLS):
            general.addWidget(self._make_button(symbol), index // COLUMNS, index % COLUMNS)
        layout.addLayout(general)
        layout.addStretch(1)

        self._show_special([])

    def _make_button(self, symbol: str) -> QPushButton:
        button = QPushButton(BUTTON_LABELS.get(symbol, symbol))
        button.setProperty("variant", "symbol")
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        # Yazı tipi QSS'te (`variant="symbol"`): genel düğme stili `font-size`
        # verdiği için `setFont` ile verilen boyut ezilip küçük çıkıyordu.
        button.setProperty("long", "true" if len(button.text()) > 2 else "false")
        button.setMinimumWidth(BUTTON_SIZE)
        button.clicked.connect(lambda _=False, s=symbol, b=button: self._pick(s, b))
        self._buttons.append(button)
        return button

    def set_special(self, symbols: list[str]) -> None:
        """Probleme özel sembolleri kurar; yoksa o bölüm gizleniyor."""
        if symbols == self._special:
            return
        self._show_special(symbols)

    def _show_special(self, symbols: list[str]) -> None:
        while self._special_grid.count():
            item = self._special_grid.takeAt(0)
            widget = item.widget()
            if widget is not None:
                self._buttons.remove(widget)
                widget.deleteLater()
        self._special = list(symbols)
        # Özel ifadeler çoğunlukla uzun (`log₂`); iki sütun yetiyor.
        for index, symbol in enumerate(symbols):
            self._special_grid.addWidget(self._make_button(symbol), index // 2, index % 2)
        self._special_label.setVisible(bool(symbols))

    def _pick(self, symbol: str, button: QPushButton) -> None:
        self.clear_selection()
        button.setProperty("active", "true")
        repolish(button)
        self.picked.emit(symbol)

    def clear_selection(self) -> None:
        for button in self._buttons:
            if button.property("active") == "true":
                button.setProperty("active", "false")
                repolish(button)

    def set_labels(self, special: str, general: str) -> None:
        self._special_label.setText(special)
        self._general_label.setText(general)
