"""Tek bir ad soran küçük pencere (Notlarım'da klasör açma, yeniden adlandırma).

Görünüşü ve davranışı yeni not penceresiyle ortak (`modal.py`). Ad boşken
onay düğmesi basılmıyor.
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget

from ..resources.theme.tokens import SPACING
from . import modal

DIALOG_WIDTH = 440


class NameDialog(QDialog):
    """Başlık, etiket, tek bir metin kutusu ve iki düğme."""

    def __init__(
        self,
        title: str,
        label: str,
        placeholder: str,
        initial: str,
        confirm_text: str,
        cancel_text: str,
        max_length: int,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        modal.prepare(self)
        self.setFixedWidth(DIALOG_WIDTH)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(SPACING["xl"], SPACING["xl"], SPACING["xl"], SPACING["xl"])
        layout.setSpacing(SPACING["sm"])

        heading = QLabel(title)
        heading.setProperty("role", "subtitle")
        layout.addWidget(heading)
        layout.addSpacing(SPACING["sm"])

        caption = QLabel(label)
        caption.setProperty("role", "muted")
        layout.addWidget(caption)

        self._field = QLineEdit(initial)
        self._field.setMaxLength(max_length)
        self._field.setPlaceholderText(placeholder)
        self._field.textChanged.connect(self._validate)
        self._field.returnPressed.connect(self._accept_if_valid)
        layout.addWidget(self._field)

        layout.addSpacing(SPACING["md"])
        buttons = QHBoxLayout()
        buttons.setSpacing(SPACING["sm"])
        buttons.addStretch(1)
        cancel = QPushButton(cancel_text)
        cancel.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel.clicked.connect(self.reject)
        buttons.addWidget(cancel)
        self._confirm = QPushButton(confirm_text)
        self._confirm.setProperty("variant", "primary")
        self._confirm.setCursor(Qt.CursorShape.PointingHandCursor)
        self._confirm.clicked.connect(self._accept_if_valid)
        buttons.addWidget(self._confirm)
        layout.addLayout(buttons)

        self._validate()
        self._field.setFocus()
        self._field.selectAll()
        modal.freeze(self)

    def _validate(self) -> None:
        self._confirm.setEnabled(bool(self._field.text().strip()))

    def _accept_if_valid(self) -> None:
        if self._field.text().strip():
            self.accept()

    def value(self) -> str:
        return self._field.text().strip()
