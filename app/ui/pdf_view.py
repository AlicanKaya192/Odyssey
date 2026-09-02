"""PDF ders notlarını gösteren görünüm.

PySide6 kendi PDF görüntüleyicisiyle geliyor (`QtPdf` / `QtPdfWidgets`), o
yüzden ek bir bağımlılığa gerek yok. PDF uygulamanın içinde açılıyor,
kullanıcı dışarıda bir program açmak zorunda kalmıyor.
"""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtPdf import QPdfDocument
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ..core.language import LanguageManager
from ..resources.theme.tokens import SPACING

ZOOM_STEP = 0.15
ZOOM_MIN = 0.4
ZOOM_MAX = 3.0


class PdfView(QWidget):
    """Gömülü PDF görüntüleyici."""

    def __init__(self, language: LanguageManager, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._language = language
        self._document = QPdfDocument(self)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(SPACING["lg"], SPACING["md"], SPACING["lg"], SPACING["lg"])
        layout.setSpacing(SPACING["sm"])

        # Üst şerit: dosya adı ve yakınlaştırma
        toolbar = QHBoxLayout()
        toolbar.setSpacing(SPACING["sm"])

        self._title = QLabel()
        self._title.setProperty("role", "muted")
        toolbar.addWidget(self._title)
        toolbar.addStretch(1)

        self._zoom_out = QPushButton("−")
        self._zoom_out.setCursor(Qt.CursorShape.PointingHandCursor)
        self._zoom_out.setProperty("variant", "ghost")
        self._zoom_out.setFixedWidth(40)
        self._zoom_out.clicked.connect(lambda: self._zoom(-ZOOM_STEP))

        self._zoom_label = QLabel("100%")
        self._zoom_label.setProperty("role", "muted")
        self._zoom_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._zoom_label.setFixedWidth(56)

        self._zoom_in = QPushButton("+")
        self._zoom_in.setCursor(Qt.CursorShape.PointingHandCursor)
        self._zoom_in.setProperty("variant", "ghost")
        self._zoom_in.setFixedWidth(40)
        self._zoom_in.clicked.connect(lambda: self._zoom(ZOOM_STEP))

        toolbar.addWidget(self._zoom_out)
        toolbar.addWidget(self._zoom_label)
        toolbar.addWidget(self._zoom_in)
        layout.addLayout(toolbar)

        self._viewer = QPdfView()
        self._viewer.setDocument(self._document)
        self._viewer.setPageMode(QPdfView.PageMode.MultiPage)
        self._viewer.setZoomMode(QPdfView.ZoomMode.FitToWidth)
        self._viewer.setFrameShape(QFrame.Shape.NoFrame)
        layout.addWidget(self._viewer, 1)

        self._empty = QLabel()
        self._empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._empty.setProperty("role", "muted")
        layout.addWidget(self._empty)
        self._empty.hide()

    def _zoom(self, delta: float) -> None:
        """Yakınlaştırma. İlk elle ayarda sayfaya-sığdır kipinden çıkılır."""
        if self._viewer.zoomMode() != QPdfView.ZoomMode.Custom:
            self._viewer.setZoomMode(QPdfView.ZoomMode.Custom)

        factor = min(ZOOM_MAX, max(ZOOM_MIN, self._viewer.zoomFactor() + delta))
        self._viewer.setZoomFactor(factor)
        self._zoom_label.setText(f"{int(factor * 100)}%")

    def show_pdf(self, path: Path | None, title: str = "") -> None:
        """PDF dosyasını yükler."""
        if path is None or not path.exists():
            self._viewer.hide()
            self._empty.setText(self._language.t("content.not_found", path=path or "-"))
            self._empty.show()
            return

        self._document.load(str(path))
        self._title.setText(title or path.name)
        self._viewer.setZoomMode(QPdfView.ZoomMode.FitToWidth)
        self._zoom_label.setText("100%")
        self._empty.hide()
        self._viewer.show()

    def retranslate(self) -> None:
        # Başlık içerikten geliyor, çeviri gerektiren sabit metin yok.
        pass
