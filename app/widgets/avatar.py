"""Yuvarlak profil fotoğrafı düğmesi.

Fotoğraf varsa onu, yoksa adın baş harflerini gösteriyor. Ad da yoksa bir
kamera işareti çıkıyor — tıklanabilir olduğunu belli etmek için.

Kendi çizimini kendisi yapıyor: yuvarlak kırpma QSS ile yapılamıyor,
`border-radius` görsele değil yalnızca widget'ın zeminine uygulanıyor.
"""

from __future__ import annotations

from PySide6.QtCore import QRectF, Qt, Signal
from PySide6.QtGui import QBrush, QColor, QFont, QPainter, QPainterPath, QPen, QPixmap
from PySide6.QtWidgets import QWidget

# Fotoğrafın üstüne gelince beliren ince halka: tıklanabilir olduğunu
# söylüyor. Sürekli çizilirse süs gibi duruyor.
HOVER_RING = 2


class AvatarView(QWidget):
    """Yuvarlak fotoğraf alanı. Tıklanınca `clicked` yayılıyor."""

    clicked = Signal()

    def __init__(self, size: int = 96, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._pixmap: QPixmap | None = None
        self._initials = ""
        self._accent = QColor("#4F46E5")
        self._text = QColor("#FFFFFF")
        self._hover = False
        self._interactive = True

        self.setFixedSize(size, size)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    # --- içerik -----------------------------------------------------------

    def set_photo(self, pixmap: QPixmap | None) -> None:
        self._pixmap = pixmap
        self.update()

    def set_initials(self, text: str) -> None:
        self._initials = text.strip()[:2].upper()
        self.update()

    def set_colors(self, accent: str, text: str) -> None:
        self._accent = QColor(accent)
        self._text = QColor(text)
        self.update()

    def set_interactive(self, value: bool) -> None:
        """Şeritteki küçük hâli tıklanınca profile gidiyor, fotoğraf seçmiyor."""
        self._interactive = value
        self.setCursor(
            Qt.CursorShape.PointingHandCursor if value else Qt.CursorShape.ArrowCursor
        )

    # --- olaylar ----------------------------------------------------------

    def enterEvent(self, event) -> None:  # noqa: N802
        self._hover = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event) -> None:  # noqa: N802
        self._hover = False
        self.update()
        super().leaveEvent(event)

    def mouseReleaseEvent(self, event) -> None:  # noqa: N802
        if event.button() == Qt.MouseButton.LeftButton and self.rect().contains(
            event.position().toPoint()
        ):
            self.clicked.emit()
        super().mouseReleaseEvent(event)

    # --- çizim ------------------------------------------------------------

    def paintEvent(self, event) -> None:  # noqa: N802
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        alan = QRectF(self.rect()).adjusted(1, 1, -1, -1)
        daire = QPainterPath()
        daire.addEllipse(alan)

        if self._pixmap is not None and not self._pixmap.isNull():
            painter.setClipPath(daire)
            # Görsel zaten kare kaydediliyor; yine de kısa kenara göre
            # ölçekleyip ortalıyoruz, dışarıdan gelen bir görsel kare
            # olmayabilir.
            olcekli = self._pixmap.scaled(
                self.size(),
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation,
            )
            painter.drawPixmap(
                int((self.width() - olcekli.width()) / 2),
                int((self.height() - olcekli.height()) / 2),
                olcekli,
            )
            painter.setClipping(False)
        else:
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(self._accent))
            painter.drawPath(daire)

            painter.setPen(self._text)
            font = QFont(self.font())
            font.setPixelSize(max(12, int(self.height() * 0.38)))
            font.setWeight(QFont.Weight.Bold)
            painter.setFont(font)
            painter.drawText(
                self.rect(),
                Qt.AlignmentFlag.AlignCenter,
                self._initials or "+",
            )

        if self._hover and self._interactive:
            kalem = QPen(self._accent, HOVER_RING)
            painter.setPen(kalem)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawEllipse(alan.adjusted(1, 1, -1, -1))

        painter.end()
