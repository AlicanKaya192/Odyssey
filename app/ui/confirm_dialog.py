"""Onay kutusu.

Şu an tek yerde kullanılıyor: pencereyi kapatmadan önce soran kutu. Qt'nin
`QMessageBox`'ı yerine kendi kutumuz var, çünkü `QMessageBox` düğmelerini
işletim sisteminin sırasına göre diziyor ve stil dosyasındaki düğme
görünümünü tam almıyordu.

Onay düğmesi kırmızı: basılınca geri dönüşü olmayan bir şey oluyor. Sola
"vazgeç", sağa "çık" konuyor — sağdaki, kutuyu kapatan asıl eylem.
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ..resources.theme.tokens import SPACING


class ConfirmDialog(QDialog):
    """Başlık, açıklama ve iki düğmeden oluşan onay kutusu."""

    def __init__(
        self,
        title: str,
        message: str,
        confirm_text: str,
        cancel_text: str,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self.setModal(True)
        self.setWindowTitle(title)
        self.setMinimumWidth(420)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            SPACING["lg"], SPACING["lg"], SPACING["lg"], SPACING["lg"]
        )
        layout.setSpacing(SPACING["md"])

        heading = QLabel(title)
        heading.setProperty("role", "dialog-title")
        layout.addWidget(heading)

        body = QLabel(message)
        body.setProperty("role", "muted")
        body.setWordWrap(True)
        layout.addWidget(body)

        layout.addSpacing(SPACING["xs"])

        buttons = QHBoxLayout()
        buttons.setSpacing(SPACING["sm"])
        buttons.addStretch(1)

        cancel = QPushButton(cancel_text)
        cancel.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel.clicked.connect(self.reject)
        buttons.addWidget(cancel)

        confirm = QPushButton(confirm_text)
        confirm.setProperty("variant", "danger")
        confirm.setCursor(Qt.CursorShape.PointingHandCursor)
        confirm.clicked.connect(self.accept)
        buttons.addWidget(confirm)

        layout.addLayout(buttons)

        # Enter tuşu yanlışlıkla çıkışa basmasın; odak "vazgeç"te başlıyor.
        cancel.setDefault(True)
        cancel.setFocus()
