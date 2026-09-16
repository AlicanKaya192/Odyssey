"""Bir düğmenin üstünde açılan küçük panel (bildirimler, kısayollar).

Çerçevesi, aşağı bakan oku, gölgesi ve dışına tıklanınca kapanması burada;
içini dolduran panel kendi işine bakıyor. İki panel bunu paylaşıyor.

**Ayrı bir pencere değil, pencerenin içinde bir katman.** Önce `Qt.Popup`
idi ve açıkken fareyi de klavyeyi de kendine kilitliyordu:

- `F1` ana pencereye ulaşmadığı için ikinci kez basmak paneli kapatmıyordu;
- başlık çubuğundaki küçült/büyüt/kapat düğmelerine yapılan ilk tıklama
  paneli kapatmaya gidiyor, düğmeye ulaşmıyordu — Alican iki kez tıklamak
  zorunda kalıyordu.

Katman yalnızca pencerenin kendi alanını kaplıyor; başlık çubuğu Windows'un
elinde kalıyor ve kısayollar ana pencerede çalışmaya devam ediyor.
"""

from __future__ import annotations

from PySide6.QtCore import QPoint, QRectF, Qt
from PySide6.QtGui import QColor, QPainter, QPainterPath, QPen
from PySide6.QtWidgets import (
    QAbstractButton,
    QApplication,
    QGraphicsDropShadowEffect,
    QVBoxLayout,
    QWidget,
)

from ..resources.theme.tokens import PALETTES, RADIUS

# Okun içeriğin sağ kenarına uzaklığı ve ölçüleri.
ARROW_RIGHT = 16
ARROW_HEIGHT = 10
ARROW_WIDTH = 16

# Panelin düğmeyle arasındaki ve pencere kenarlarıyla arasındaki en az pay.
ANCHOR_GAP = 4
EDGE_GAP = 8


class PopoverBody(QWidget):
    """İçeriği taşıyan kutu: yuvarlak çerçeve, aşağı bakan ok, gölge."""

    def __init__(self, mode: str = "dark", parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._mode = mode
        # Zemini kendisi çiziyor; genel `QWidget` kuralı sayfa zeminini
        # boyamasın.
        self.setProperty("role", "bare")
        self.apply_shadow()

    def set_mode(self, mode: str) -> None:
        self._mode = mode
        self.apply_shadow()
        self.update()

    def apply_shadow(self) -> None:
        from ..resources.theme.tokens import shadow_color

        r, g, b, a = shadow_color(self._mode, strong=True)
        effect = QGraphicsDropShadowEffect(self)
        effect.setBlurRadius(24)
        effect.setOffset(0, 4)
        effect.setColor(QColor(r, g, b, a))
        self.setGraphicsEffect(effect)

    def paintEvent(self, event) -> None:  # noqa: N802
        super().paintEvent(event)

        p = PALETTES.get(self._mode, PALETTES["dark"])
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        radius = RADIUS.get("md", 8)
        rect = QRectF(self.rect())
        rect.setHeight(rect.height() - ARROW_HEIGHT)
        # Kenarlık çizilirken köşeler kesilmesin diye yarım piksel pay.
        rect.adjust(0.5, 0.5, -0.5, -0.5)

        path = QPainterPath()
        path.addRoundedRect(rect, radius, radius)

        # Okun ucu düğmenin ortasına geliyor; hizalamayı `Popover._place`
        # yapıyor, burada yeri sabit.
        merkez = rect.width() - ARROW_RIGHT
        ok = QPainterPath()
        # Üçgenin üst kenarı kutunun bir piksel içinden başlıyor: birleşince
        # aralarında çizgi kalmıyor, tek parça görünüyor.
        ok.moveTo(merkez - ARROW_WIDTH / 2, rect.bottom() - 1)
        ok.lineTo(merkez, rect.bottom() + ARROW_HEIGHT)
        ok.lineTo(merkez + ARROW_WIDTH / 2, rect.bottom() - 1)
        ok.closeSubpath()

        painter.setBrush(QColor(p["surface"]))
        painter.setPen(QPen(QColor(p["border"]), 1.0))
        painter.drawPath(path.united(ok))
        painter.end()


class Popover(QWidget):
    """Pencereyi kaplayan saydam katman; içinde panelin kutusu.

    İçerik `self.content` düzenine ekleniyor; yüksekliği panel kendisi
    biliyor ve `fit_height` ile bildiriyor.
    """

    def __init__(self, width: int, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        # Katman görünmez: yalnızca dışarı tıklamayı yakalıyor.
        self.setProperty("role", "bare")
        self._mode = "dark"
        self._width = width
        self._anchor: QWidget | None = None
        self.hide()

        self.body = PopoverBody(self._mode, self)
        self.body.setFixedWidth(width)

        self.content = QVBoxLayout(self.body)
        # Altta oka yer.
        self.content.setContentsMargins(0, 0, 0, ARROW_HEIGHT)
        self.content.setSpacing(0)

    def set_mode(self, mode: str) -> None:
        self._mode = mode
        self.body.set_mode(mode)

    def fit_height(self, content_height: int) -> None:
        """Kutuyu içeriğin boyuna kilitler (ok payı dahil).

        Esnek bırakılınca önceki açılıştan kalan yükseklik içeriği ortaya
        itiyordu.
        """
        self.body.setFixedSize(self._width, content_height + ARROW_HEIGHT)
        if self.isVisible():
            self._place()

    def show_above(self, anchor: QWidget) -> None:
        """Paneli verilen düğmenin hemen üstünde açar."""
        self._anchor = anchor
        self._place()
        self.show()
        self.raise_()

    def reposition(self) -> None:
        """Pencere boyu değişince katmanı ve kutuyu yeniden yerleştirir."""
        if self.isVisible():
            self._place()

    def _place(self) -> None:
        parent = self.parentWidget()
        if parent is None or self._anchor is None:
            return
        self.setGeometry(parent.rect())

        nokta = self.mapFromGlobal(self._anchor.mapToGlobal(QPoint(0, 0)))
        # Okun ucu düğmenin ortasına gelsin.
        x = nokta.x() + self._anchor.width() // 2 + ARROW_RIGHT - self._width
        y = nokta.y() - self.body.height() - ANCHOR_GAP
        self.body.move(
            max(EDGE_GAP, min(x, self.width() - self._width - EDGE_GAP)),
            max(EDGE_GAP, y),
        )

    def mousePressEvent(self, event) -> None:  # noqa: N802
        """Kutunun dışına tıklamak kapatıyor; tıklama altındaki düğmeye gidiyor.

        Katman pencereyi kapladığı için tıklama normalde yalnızca paneli
        kapatırdı ve kullanıcı ikinci kez tıklamak zorunda kalırdı. Kapanışta
        tıklamanın altındaki düğme çalıştırılıyor: panel açıkken şeride ya da
        zile basmak tek tıklamada iş görüyor. Paneli açan düğme dışarıda
        bırakılıyor; yoksa panel kapanıp hemen yeniden açılırdı.
        """
        if self.body.geometry().contains(event.position().toPoint()):
            super().mousePressEvent(event)
            return

        self.close()
        kure = event.globalPosition().toPoint()
        hedef = QApplication.widgetAt(kure)
        if hedef is not None and hedef is not self._anchor and isinstance(hedef, QAbstractButton):
            hedef.click()
