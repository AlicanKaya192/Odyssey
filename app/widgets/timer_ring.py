"""Süreyi gösteren halka.

İki yerde kullanılıyor: sınav başlamadan önce "bu sınav ne kadar sürecek"
bilgisini veren büyük hâli ve sınav sürerken köşede duran küçük hâli.

Küçük hâli bilinçli olarak sade: sayacın dikkat dağıtmaması gerekiyor.
Süre azalırken renk değişiyor — sona yaklaşınca fark edilsin diye — ama
yanıp sönmüyor, büyümüyor.
"""

from __future__ import annotations

from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QColor, QFont, QPainter, QPen
from PySide6.QtWidgets import QWidget

# Kalan sürenin hangi oranından sonra renk değişeceği.
WARN_RATIO = 0.25
DANGER_RATIO = 0.10


def format_clock(seconds: int) -> str:
    """Saniyeyi `dd:ss` biçimine çevirir."""
    seconds = max(0, int(seconds))
    return f"{seconds // 60:02d}:{seconds % 60:02d}"


class TimerRing(QWidget):
    """Kalan süreyi halka ve rakamla gösterir."""

    def __init__(self, size: int = 96, thickness: int = 5, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._total = 0
        self._left = 0
        self._untimed = False
        self._thickness = thickness

        self._track = QColor("#E3E6EC")
        self._normal = QColor("#4F46E5")
        self._warn = QColor("#B45309")
        self._danger = QColor("#B91C1C")
        self._text = QColor("#12151A")

        self.setFixedSize(size, size)

    # --- veri -------------------------------------------------------------

    def set_total(self, seconds: int) -> None:
        """Toplam süreyi verir ve halkayı dolu gösterir."""
        self._total = max(0, int(seconds))
        self._left = self._total
        self.update()

    def set_left(self, seconds: int) -> None:
        self._left = max(0, min(self._total, int(seconds)))
        self.update()

    def set_untimed(self, value: bool) -> None:
        """Süresiz kip: halka tam dolu, ortasında sonsuz işareti.

        Ayarlardan süre kaldırıldığında sayaç hiç çalışmıyor. Halkayı boş
        ya da `00:00` göstermek "süre bitti" gibi okunuyordu; sonsuz
        işareti durumu tek bakışta anlatıyor.
        """
        value = bool(value)
        if value == self._untimed:
            return
        self._untimed = value
        self.update()

    def set_colors(self, track: str, normal: str, warn: str, danger: str, text: str) -> None:
        self._track = QColor(track)
        self._normal = QColor(normal)
        self._warn = QColor(warn)
        self._danger = QColor(danger)
        self._text = QColor(text)
        self.update()

    # --- çizim ------------------------------------------------------------

    def _ring_color(self) -> QColor:
        if not self._total:
            return self._normal
        oran = self._left / self._total
        if oran <= DANGER_RATIO:
            return self._danger
        if oran <= WARN_RATIO:
            return self._warn
        return self._normal

    def paintEvent(self, event) -> None:  # noqa: N802
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        yari = self._thickness / 2
        kutu = QRectF(
            yari, yari,
            self.width() - self._thickness,
            self.height() - self._thickness,
        )

        kalem = QPen(self._track, self._thickness)
        kalem.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(kalem)
        painter.drawEllipse(kutu)

        if self._untimed:
            kalem.setColor(self._normal)
            painter.setPen(kalem)
            painter.drawEllipse(kutu)
        elif self._total and self._left:
            kalem.setColor(self._ring_color())
            painter.setPen(kalem)
            # Saat on ikiden başlayıp saat yönünde eksiliyor; Qt açıları
            # on altıda bir derece cinsinden istiyor.
            painter.drawArc(kutu, 90 * 16, -int(360 * 16 * self._left / self._total))

        font = QFont(self.font())
        # Sonsuz işareti rakamlardan daha ince duruyor; biraz büyütülmeden
        # halkanın ortasında kayıp gibi görünüyordu.
        font.setPixelSize(max(11, int(self.height() * (0.40 if self._untimed else 0.24))))
        font.setWeight(QFont.Weight.DemiBold)
        painter.setFont(font)
        painter.setPen(self._text)
        painter.drawText(
            self.rect(),
            Qt.AlignmentFlag.AlignCenter,
            "∞" if self._untimed else format_clock(self._left),
        )
        painter.end()
