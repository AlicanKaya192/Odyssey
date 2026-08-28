"""Açılış ekranı.

Uygulama açılırken bir süre hiçbir şey görünmüyordu: Chromium (QtWebEngine)
ve içerik kataloğu yüklenene kadar ekranda hiçbir belirti olmuyor, kullanıcı
çift tıkladığından emin olamıyordu. Bu pencere o boşluğu dolduruyor.

Süre uydurma değil: pencere, ana pencere kurulurken açık duruyor ve kurulum
bitince kapanıyor. Kurulum çok hızlı biterse en az `MINIMUM_MS` kadar
görünüyor — yoksa ekranda tek karelik bir parlama olarak beliriyor ve daha
kötü duruyor.

Kendi çizimini kendisi yapıyor: köşeleri yuvarlatmak için pencere saydam
olmak zorunda, saydam pencerede QSS zemini güvenilir çalışmıyor.
"""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import (
    QEasingCurve,
    QParallelAnimationGroup,
    QPoint,
    QPropertyAnimation,
    QRectF,
    Qt,
    QTimer,
)
from PySide6.QtGui import QColor, QFont, QIcon, QPainter, QPainterPath, QPen
from PySide6.QtWidgets import QGraphicsOpacityEffect, QLabel, QVBoxLayout, QWidget

from ..resources.theme.tokens import FONTS, PALETTES, RADIUS

# Gölgenin sığması için pencere karttan biraz büyük; kart bu payın
# içinde çiziliyor.
SHADOW_MARGIN = 18
SHADOW_STEPS = 7

WIDTH = 380 + 2 * SHADOW_MARGIN
HEIGHT = 300 + 2 * SHADOW_MARGIN
LOGO_SIZE = 104

# Simge belirir, hemen ardından ad. Toplam yaklaşık bir saniye; daha uzunu
# açılışı yavaşlatıyormuş hissi veriyor.
LOGO_FADE_MS = 420
NAME_DELAY_MS = 220
NAME_FADE_MS = 340
FADE_OUT_MS = 260

# Pencerenin ekranda kalacağı en kısa süre.
MINIMUM_MS = 1700


class SplashScreen(QWidget):
    """Uygulama adı ve simgesiyle açılış penceresi."""

    def __init__(self, icon_path: Path | None, mode: str = "dark") -> None:
        super().__init__(None)
        self._palette = PALETTES.get(mode, PALETTES["dark"])
        self._closing = False

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.SplashScreen
            | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(WIDTH, HEIGHT)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            SHADOW_MARGIN, SHADOW_MARGIN, SHADOW_MARGIN, SHADOW_MARGIN
        )
        layout.setSpacing(0)
        layout.addStretch(1)

        self._logo = QLabel()
        self._logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if icon_path is not None and icon_path.exists():
            # `QPixmap` çok boyutlu bir `.ico` dosyasından küçük bir kareyi
            # alıp büyütüyor ve logo bulanık çıkıyordu. `QIcon` istenen
            # boyuta en yakın kareyi seçiyor. Ekran ölçeği ile çarpmak da
            # yüksek DPI'da netliği koruyor.
            oran = self.devicePixelRatioF() or 1.0
            kenar = int(LOGO_SIZE * oran)
            pixmap = QIcon(str(icon_path)).pixmap(kenar, kenar)
            pixmap.setDevicePixelRatio(oran)
            self._logo.setPixmap(pixmap)
        layout.addWidget(self._logo)

        layout.addSpacing(22)

        self._name = QLabel("Odyssey")
        self._name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setFamily(FONTS["ui"].split(",")[0].strip('"'))
        font.setPointSize(19)
        font.setWeight(QFont.Weight.DemiBold)
        self._name.setFont(font)
        self._name.setStyleSheet(f"color: {self._palette['text']};")
        layout.addWidget(self._name)

        layout.addStretch(1)

        self._logo_fade = QGraphicsOpacityEffect(self._logo)
        self._logo_fade.setOpacity(0.0)
        self._logo.setGraphicsEffect(self._logo_fade)

        self._name_fade = QGraphicsOpacityEffect(self._name)
        self._name_fade.setOpacity(0.0)
        self._name.setGraphicsEffect(self._name_fade)

        self._animations = QParallelAnimationGroup(self)
        self._build_entrance()

    # --- çizim -----------------------------------------------------------

    def paintEvent(self, event) -> None:  # noqa: N802 (Qt adlandırması)
        """Kartı, gölgesini ve kenarlığını çizer.

        Ölçüldü: gölge ve belirgin kenarlık olmadan kart, arkasındaki koyu
        pencereden yalnızca 1-6 RGB birimi farklı çıkıyor ve görünmüyordu —
        ekranda havada duran bir logo ve yazı kalıyordu.
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Gölge: iç içe, gitgide saydamlaşan yuvarlak dikdörtgenler. Qt'nin
        # gölge efekti saydam pencerede güvenilir çalışmıyor.
        for adim in range(SHADOW_STEPS, 0, -1):
            pay = adim * 2
            alpha = int(26 * (1 - adim / (SHADOW_STEPS + 1)))
            golge = QPainterPath()
            golge.addRoundedRect(
                QRectF(
                    SHADOW_MARGIN - pay,
                    SHADOW_MARGIN - pay + 3,
                    self.width() - 2 * (SHADOW_MARGIN - pay),
                    self.height() - 2 * (SHADOW_MARGIN - pay),
                ),
                RADIUS["xl"] + pay,
                RADIUS["xl"] + pay,
            )
            painter.fillPath(golge, QColor(0, 0, 0, alpha))

        card = QRectF(
            SHADOW_MARGIN,
            SHADOW_MARGIN,
            self.width() - 2 * SHADOW_MARGIN,
            self.height() - 2 * SHADOW_MARGIN,
        )
        path = QPainterPath()
        path.addRoundedRect(card, RADIUS["xl"], RADIUS["xl"])
        painter.fillPath(path, QColor(self._palette["surface"]))

        pen = QPen(QColor(self._palette["border_strong"]))
        pen.setWidthF(1.4)
        painter.setPen(pen)
        painter.drawPath(path)

    # --- animasyon -------------------------------------------------------

    def _build_entrance(self) -> None:
        logo = QPropertyAnimation(self._logo_fade, b"opacity", self)
        logo.setDuration(LOGO_FADE_MS)
        logo.setStartValue(0.0)
        logo.setEndValue(1.0)
        logo.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._animations.addAnimation(logo)

        # Ad, simgeden biraz sonra ve hafifçe yukarı kayarak geliyor.
        name = QPropertyAnimation(self._name_fade, b"opacity", self)
        name.setDuration(NAME_FADE_MS + NAME_DELAY_MS)
        name.setStartValue(0.0)
        name.setKeyValueAt(NAME_DELAY_MS / (NAME_FADE_MS + NAME_DELAY_MS), 0.0)
        name.setEndValue(1.0)
        name.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._animations.addAnimation(name)

    def start(self) -> None:
        """Pencereyi ekranın ortasında açar ve animasyonu başlatır."""
        screen = self.screen() or self.parentWidget()
        if screen is not None and hasattr(screen, "availableGeometry"):
            alan = screen.availableGeometry()
            self.move(
                alan.center() - QPoint(self.width() // 2, self.height() // 2)
            )
        self.show()
        self._animations.start()

    def finish(self, target: QWidget | None = None) -> None:
        """Kapanış animasyonunu başlatır; bitince pencere yok ediliyor.

        `target` verilirse kapanış bitince öne alınıyor. Ana pencere açılış
        ekranının arkasında kaldığında görev çubuğunda yanıp sönüyordu.
        """
        if self._closing:
            return
        self._closing = True

        fade = QPropertyAnimation(self, b"windowOpacity", self)
        fade.setDuration(FADE_OUT_MS)
        fade.setStartValue(1.0)
        fade.setEndValue(0.0)
        fade.setEasingCurve(QEasingCurve.Type.InCubic)

        def bitti() -> None:
            self.close()
            self.deleteLater()
            if target is not None:
                target.raise_()
                target.activateWindow()

        fade.finished.connect(bitti)
        fade.start()
        self._fade_out = fade  # animasyon nesnesi yaşasın diye tutuluyor


def show_splash(icon_path: Path | None, mode: str) -> SplashScreen:
    """Açılış ekranını açar."""
    splash = SplashScreen(icon_path, mode)
    splash.start()
    return splash


def close_splash(splash: SplashScreen | None, target: QWidget, started_at: float) -> None:
    """Açılış ekranını kapatır; en az `MINIMUM_MS` görünmesini garantiler."""
    if splash is None:
        return

    import time

    gecen = (time.monotonic() - started_at) * 1000
    kalan = max(0, int(MINIMUM_MS - gecen))
    QTimer.singleShot(kalan, lambda: splash.finish(target))
