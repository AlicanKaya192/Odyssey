"""Aç/kapa anahtarı.

Qt'nin `QCheckBox` ve `QRadioButton` bileşenleri işletim sisteminin kutu
ve yuvarlak çizimini kullanıyor; ayarlar ekranında bunlar hem küçük hem de
"seçildi mi seçilmedi mi" sorusunu uzaktan cevaplamıyor.

Bu anahtar durumu **konum ve renkle** birlikte gösteriyor: kapalıyken topuz
solda ve zemin nötr, açıkken sağda ve zemin vurgu renginde. İkisi arasında
kısa bir geçiş var — anahtarın hangi yöne gittiği görülüyor.

Renkler `set_colors` ile dışarıdan veriliyor, çünkü QSS bir widget'ın kendi
`paintEvent` çizimine ulaşamıyor; tema değişince çağıran taraf yeniliyor.
"""

from __future__ import annotations

from PySide6.QtCore import (
    Property,
    QEasingCurve,
    QPropertyAnimation,
    QRectF,
    QSize,
    Qt,
    Signal,
)
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import QWidget

# Geçiş süresi. Daha uzunu ayarı değiştirdikten sonra bekletiyor, daha
# kısası hareketi göstermiyor.
DURATION_MS = 140


class ToggleSwitch(QWidget):
    """İki durumlu anahtar."""

    toggled = Signal(bool)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._checked = False
        self._position = 0.0

        self._track_off = QColor("#D5D9E2")
        self._track_on = QColor("#4F46E5")
        self._knob = QColor("#FFFFFF")
        self._border = QColor("#C7CCD6")

        self._animation = QPropertyAnimation(self, b"position", self)
        self._animation.setDuration(DURATION_MS)
        self._animation.setEasingCurve(QEasingCurve.Type.OutCubic)

        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setFixedSize(46, 26)

    # --- durum ------------------------------------------------------------

    def is_checked(self) -> bool:
        return self._checked

    def set_checked(self, value: bool, animate: bool = True) -> None:
        """Durumu değiştirir. `toggled` sinyali yayılmaz.

        Sinyalsiz olması bilinçli: ayar penceresi açılırken kayıtlı değerler
        yerleştiriliyor ve bunun ayarı yeniden yazmaması gerekiyor.
        """
        value = bool(value)
        if value == self._checked:
            return
        self._checked = value
        hedef = 1.0 if value else 0.0
        if animate and self.isVisible():
            self._animation.stop()
            self._animation.setStartValue(self._position)
            self._animation.setEndValue(hedef)
            self._animation.start()
        else:
            self._position = hedef
            self.update()

    def set_colors(self, track_off: str, track_on: str, knob: str, border: str) -> None:
        self._track_off = QColor(track_off)
        self._track_on = QColor(track_on)
        self._knob = QColor(knob)
        self._border = QColor(border)
        self.update()

    # --- animasyon --------------------------------------------------------

    def _get_position(self) -> float:
        return self._position

    def _set_position(self, value: float) -> None:
        self._position = value
        self.update()

    position = Property(float, _get_position, _set_position)

    # --- etkileşim --------------------------------------------------------

    def _flip(self) -> None:
        self.set_checked(not self._checked)
        self.toggled.emit(self._checked)

    def mouseReleaseEvent(self, event) -> None:  # noqa: N802
        if event.button() == Qt.MouseButton.LeftButton and self.rect().contains(
            event.position().toPoint()
        ):
            self._flip()
        super().mouseReleaseEvent(event)

    def keyPressEvent(self, event) -> None:  # noqa: N802
        # Klavyeyle de çevrilebiliyor; ayarlar ekranı fareye bağlı kalmasın.
        if event.key() in (Qt.Key.Key_Space, Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self._flip()
            return
        super().keyPressEvent(event)

    def sizeHint(self) -> QSize:  # noqa: N802
        return QSize(46, 26)

    # --- çizim ------------------------------------------------------------

    def paintEvent(self, event) -> None:  # noqa: N802
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        yukseklik = self.height()
        yaricap = yukseklik / 2

        # Zemin rengi iki uç arasında karışıyor; anahtar hareket ederken
        # renk de birlikte geçiyor, iki ayrı adımda sıçramıyor.
        zemin = QColor(
            int(self._track_off.red() + (self._track_on.red() - self._track_off.red()) * self._position),
            int(self._track_off.green() + (self._track_on.green() - self._track_off.green()) * self._position),
            int(self._track_off.blue() + (self._track_on.blue() - self._track_off.blue()) * self._position),
        )

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(zemin)
        painter.drawRoundedRect(QRectF(0, 0, self.width(), yukseklik), yaricap, yaricap)

        # Kapalıyken ince bir çerçeve: açık temada zemin arka planla
        # karışıyor ve anahtarın nerede bittiği belli olmuyordu.
        if self._position < 0.5:
            kalem = painter.pen()
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.setPen(self._border)
            painter.drawRoundedRect(
                QRectF(0.5, 0.5, self.width() - 1, yukseklik - 1), yaricap, yaricap
            )
            painter.setPen(kalem)

        bosluk = 3.0
        topuz = yukseklik - bosluk * 2
        sol = bosluk + (self.width() - topuz - bosluk * 2) * self._position

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self._knob)
        painter.drawEllipse(QRectF(sol, bosluk, topuz, topuz))

        if self.hasFocus():
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.setPen(self._track_on)
            painter.drawRoundedRect(
                QRectF(-1.5, -1.5, self.width() + 3, yukseklik + 3),
                yaricap + 2, yaricap + 2,
            )

        painter.end()
