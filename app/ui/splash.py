"""Açılış ekranı.

Uygulama açılırken bir süre hiçbir şey görünmüyordu: Chromium (QtWebEngine)
ve içerik kataloğu yüklenene kadar ekranda hiçbir belirti olmuyor, kullanıcı
çift tıkladığından emin olamıyordu. Bu pencere o boşluğu dolduruyor.

Kartta logo, ad, kısa bir alt yazı, yükleme çubuğu, o an yapılan iş ve
sürüm yazıyor. Sürüm `APP_VERSION`'dan okunuyor; yeni sürümde numara
yükseltilince burası da kendiliğinden değişiyor.

**Çubuk gerçek aşamalarla doluyor, sürekli kaymıyor.** Ana pencere
kurulurken olay döngüsü birkaç saniye duruyor (QtWebEngine yükleniyor);
sürekli kayan bir çubuk tam o sırada donup kalıyordu. `set_stage` her
aşamada çubuğu ileri alıp ekranı kendisi tazeliyor, kurulum bitince
çubuk kalan sürede sona doluyor ve karşılama yazısı çıkıyor.

Pencere en az `MINIMUM_MS` görünüyor: logo ve yazılar okunmadan kaybolan
bir ekran parlama gibi duruyor.

Kendi çizimini kendisi yapıyor: köşeleri yuvarlatmak için pencere saydam
olmak zorunda, saydam pencerede QSS zemini güvenilir çalışmıyor.
"""

from __future__ import annotations

import time
from pathlib import Path

from PySide6.QtCore import (
    QEasingCurve,
    QParallelAnimationGroup,
    QPoint,
    QPropertyAnimation,
    QRectF,
    Qt,
    QTimer,
    QVariantAnimation,
)
from PySide6.QtGui import (
    QColor,
    QIcon,
    QLinearGradient,
    QPainter,
    QPainterPath,
    QPen,
)
from PySide6.QtWidgets import (
    QApplication,
    QGraphicsOpacityEffect,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from ..resources.theme.tokens import FONTS, PALETTES, RADIUS, mix

# Gölgenin sığması için pencere karttan biraz büyük; kart bu payın
# içinde çiziliyor.
SHADOW_MARGIN = 18
SHADOW_STEPS = 7

CARD_WIDTH = 400
CARD_HEIGHT = 340
WIDTH = CARD_WIDTH + 2 * SHADOW_MARGIN
HEIGHT = CARD_HEIGHT + 2 * SHADOW_MARGIN
LOGO_SIZE = 96
# Simge dosyasındaki köşe yarıçapı (512'de 112) logo boyuna oranlanıyor;
# parıltı logonun kendi şeklini izlesin diye.
LOGO_RADIUS = LOGO_SIZE * 112 / 512

BAR_WIDTH = 150
BAR_HEIGHT = 5

# Öğeler yukarıdan aşağı sırayla beliriyor.
FADE_MS = 380
STAGGER_MS = 140
FADE_OUT_MS = 260

# Pencerenin ekranda kalacağı en kısa süre. Alican 3–4 saniye istedi;
# kurulum daha uzun sürerse pencere kurulum bitene kadar açık kalıyor.
MINIMUM_MS = 3000
# Kurulum bittikten sonra çubuğun sona dolması için en az bu kadar süre.
FINAL_FILL_MS = 450
# Aşama geçişinde çubuğun kayması; olay döngüsü dururken elle çiziliyor.
STAGE_STEP_MS = 140


class LoadingBar(QWidget):
    """İnce, yuvarlak uçlu yükleme çubuğu (0–1)."""

    def __init__(self, palette: dict, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._palette = palette
        self._value = 0.0
        self.setFixedSize(BAR_WIDTH, BAR_HEIGHT)

    def value(self) -> float:
        return self._value

    def set_value(self, value: float) -> None:
        self._value = max(0.0, min(1.0, value))
        self.update()

    def paintEvent(self, event) -> None:  # noqa: N802 (Qt adlandırması)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        radius = BAR_HEIGHT / 2

        track = QPainterPath()
        track.addRoundedRect(QRectF(self.rect()), radius, radius)
        painter.fillPath(track, QColor(self._palette["border"]))

        width = self.width() * self._value
        if width < 1:
            return
        # Dolgu en az çubuk yüksekliği kadar: daha kısası yuvarlak uçlarla
        # bir nokta gibi değil, bozuk bir leke gibi görünüyordu.
        width = max(width, BAR_HEIGHT)
        accent = self._palette["accent"]
        gradient = QLinearGradient(0, 0, self.width(), 0)
        gradient.setColorAt(0.0, QColor(accent))
        gradient.setColorAt(1.0, QColor(mix(accent, "#A855F7", 0.55)))
        fill = QPainterPath()
        fill.addRoundedRect(QRectF(0, 0, width, self.height()), radius, radius)
        painter.fillPath(fill, gradient)


class SplashScreen(QWidget):
    """Uygulama adı, simgesi ve yükleme durumuyla açılış penceresi."""

    def __init__(
        self,
        icon_path: Path | None,
        mode: str,
        subtitle: str,
        version_line: str,
    ) -> None:
        super().__init__(None)
        self._palette = PALETTES.get(mode, PALETTES["dark"])
        self._mode = mode
        self._closing = False

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.SplashScreen
            | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(WIDTH, HEIGHT)
        # Genel QSS her widget'a sayfa zeminini veriyor; kart ise `surface`
        # renginde. Etiketler saydam olmazsa logonun ve yazıların arkasında
        # kartla aynı renk olmayan bir kare görünüyordu (Alican bildirdi).
        self.setStyleSheet("QLabel { background: transparent; border: none; }")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            SHADOW_MARGIN, SHADOW_MARGIN + 38, SHADOW_MARGIN, SHADOW_MARGIN + 24
        )
        layout.setSpacing(0)

        self._logo = QLabel()
        self._logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._logo.setFixedHeight(LOGO_SIZE)
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

        self._name = self._label("Odyssey", 26, 700, "text")
        layout.addWidget(self._name)
        layout.addSpacing(8)

        self._subtitle = self._label(subtitle, 14, 400, "text_muted")
        layout.addWidget(self._subtitle)

        layout.addStretch(1)

        self._bar = LoadingBar(self._palette)
        layout.addWidget(self._bar, 0, Qt.AlignmentFlag.AlignHCenter)
        layout.addSpacing(12)

        self._status = self._label("", 12, 400, "text_muted")
        # Aşama yazıları farklı uzunlukta; yükseklik sabit kalmazsa yazı
        # değiştikçe altındaki sürüm satırı zıplıyor.
        self._status.setFixedHeight(18)
        layout.addWidget(self._status)
        layout.addSpacing(6)

        self._version = self._label(version_line, 12, 400, "text_muted")
        layout.addWidget(self._version)

        self._entrance = QParallelAnimationGroup(self)
        self._effects: list[QGraphicsOpacityEffect] = []
        items = [self._logo, self._name, self._subtitle, (self._bar, self._status, self._version)]
        for index, item in enumerate(items):
            widgets = item if isinstance(item, tuple) else (item,)
            for widget in widgets:
                self._fade_in(widget, index * STAGGER_MS)

        # Logonun arkasındaki parıltı, logonun kendi görünürlüğünü izliyor.
        self._logo_effect = self._effects[0]

    def _label(self, text: str, size_px: int, weight: int, color: str) -> QLabel:
        # Boyut ve kalınlık stil kuralıyla veriliyor: genel QSS'teki
        # `font-size` kuralı `setFont`'u eziyor, ad küçük kalıyordu.
        label = QLabel(text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        family = FONTS["ui"].split(",")[0].strip('"')
        label.setStyleSheet(
            f"color: {self._palette[color]}; background: transparent;"
            f" font-family: '{family}'; font-size: {size_px}px; font-weight: {weight};"
        )
        return label

    def _fade_in(self, widget: QWidget, delay_ms: int) -> None:
        effect = QGraphicsOpacityEffect(widget)
        effect.setOpacity(0.0)
        widget.setGraphicsEffect(effect)
        self._effects.append(effect)

        animation = QPropertyAnimation(effect, b"opacity", self)
        animation.setDuration(FADE_MS + delay_ms)
        animation.setStartValue(0.0)
        if delay_ms:
            animation.setKeyValueAt(delay_ms / (FADE_MS + delay_ms), 0.0)
        animation.setEndValue(1.0)
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        if widget is self._logo:
            animation.valueChanged.connect(lambda _value: self.update())
        self._entrance.addAnimation(animation)

    # --- çizim -----------------------------------------------------------

    def paintEvent(self, event) -> None:  # noqa: N802 (Qt adlandırması)
        """Kartı, gölgesini, kenarlığını ve logonun parıltısını çizer.

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

        card = QRectF(SHADOW_MARGIN, SHADOW_MARGIN, CARD_WIDTH, CARD_HEIGHT)
        path = QPainterPath()
        path.addRoundedRect(card, RADIUS["xl"], RADIUS["xl"])
        painter.fillPath(path, QColor(self._palette["surface"]))

        pen = QPen(QColor(self._palette["border_strong"]))
        pen.setWidthF(1.4)
        painter.setPen(pen)
        painter.drawPath(path)

        self._paint_glow(painter)

    def _paint_glow(self, painter: QPainter) -> None:
        """Logonun altından hafifçe taşan mor parıltı.

        Logo boyunda, biraz aşağı kaydırılmış ve gitgide büyüyüp
        saydamlaşan yuvarlak kareler: bulanıklık efekti saydam pencerede
        güvenilir çalışmadığı için gölgeyle aynı yol.
        """
        opacity = self._logo_effect.opacity() if hasattr(self, "_logo_effect") else 0.0
        if opacity <= 0:
            return
        geometry = self._logo.geometry()
        center = geometry.center()
        base = QRectF(
            center.x() - LOGO_SIZE / 2,
            center.y() - LOGO_SIZE / 2 + 10,
            LOGO_SIZE,
            LOGO_SIZE,
        )
        # Koyu temada parıltı daha az gerekli; açık zeminde daha belirgin.
        peak = 16 if self._mode == "light" else 13
        painter.setPen(Qt.PenStyle.NoPen)
        steps = 10
        for step in range(steps, 0, -1):
            grow = step * 2.2
            color = QColor(mix(self._palette["accent"], "#7C3AED", 0.4))
            color.setAlpha(int(peak * opacity * (1 - step / (steps + 1))))
            glow = QPainterPath()
            glow.addRoundedRect(
                base.adjusted(-grow, -grow, grow, grow),
                LOGO_RADIUS + grow,
                LOGO_RADIUS + grow,
            )
            painter.fillPath(glow, color)

    # --- açılış ve aşamalar ----------------------------------------------

    def start(self) -> None:
        """Pencereyi ekranın ortasında açar ve animasyonu başlatır."""
        screen = self.screen()
        if screen is not None:
            alan = screen.availableGeometry()
            self.move(alan.center() - QPoint(self.width() // 2, self.height() // 2))
        self.show()
        self._entrance.start()

    def set_stage(self, text: str, value: float) -> None:
        """O an yapılan işi yazar ve çubuğu `value`'ya kadar ilerletir.

        Bu çağrının arkasından olay döngüsünü birkaç saniye durduran bir iş
        geliyor; o yüzden çubuğun kayması burada, kısa bir döngüyle elle
        çiziliyor. Aksi hâlde yazı ve çubuk ancak iş bittikten sonra
        güncelleniyordu.
        """
        if self._closing:
            return
        self._status.setText(text)
        start = self._bar.value()
        began = time.monotonic()
        while True:
            t = min(1.0, (time.monotonic() - began) * 1000 / STAGE_STEP_MS)
            eased = 1 - (1 - t) ** 3
            self._bar.set_value(start + (value - start) * eased)
            QApplication.processEvents()
            if t >= 1.0:
                break
            time.sleep(0.012)

    def finish(self, target: QWidget | None, greeting: str, remaining_ms: int) -> None:
        """Çubuğu sona doldurur, karşılamayı yazar, sonra pencereyi kapatır.

        `target` kapanış bitince **gösterilip** öne alınıyor. Ana pencere
        daha önce gösterilirse açılış ekranı hâlâ ekrandayken arkasında
        beliriyor; ikisi bir süre aynı anda duruyordu.
        """
        if self._closing:
            return
        self._closing = True
        self._status.setText(greeting)

        fill = QVariantAnimation(self)
        fill.setDuration(max(FINAL_FILL_MS, remaining_ms))
        fill.setStartValue(self._bar.value())
        fill.setEndValue(1.0)
        fill.setEasingCurve(QEasingCurve.Type.InOutCubic)
        fill.valueChanged.connect(self._bar.set_value)
        fill.finished.connect(lambda: self._fade_out(target))
        fill.start()
        self._fill = fill  # animasyon nesnesi yaşasın diye tutuluyor

    def _fade_out(self, target: QWidget | None) -> None:
        fade = QPropertyAnimation(self, b"windowOpacity", self)
        fade.setDuration(FADE_OUT_MS)
        fade.setStartValue(1.0)
        fade.setEndValue(0.0)
        fade.setEasingCurve(QEasingCurve.Type.InCubic)

        def bitti() -> None:
            # Sıra önemli: **önce hedef gösteriliyor, sonra bu pencere
            # kapanıyor.** Tersi olursa iki iş arasında ekranda hiç pencere
            # kalmıyor, Qt "son pencere kapandı" deyip uygulamayı kapatıyor.
            # Aralıklı bir hata: bazı açılışlarda uygulama kendiliğinden
            # kapanıyordu.
            if target is not None:
                # Pencere açılışta opaklığı sıfırla gösterilmiş olabilir
                # (belge alanlarını ısıtmak için); burada görünür oluyor.
                target.setWindowOpacity(1.0)
                target.show()
                target.raise_()
                target.activateWindow()
            self.close()
            self.deleteLater()

        fade.finished.connect(bitti)
        fade.start()
        self._fade = fade


def show_splash(
    icon_path: Path | None, mode: str, subtitle: str, version_line: str
) -> SplashScreen:
    """Açılış ekranını açar."""
    splash = SplashScreen(icon_path, mode, subtitle, version_line)
    splash.start()
    return splash


def close_splash(
    splash: SplashScreen | None, target: QWidget, started_at: float, greeting: str
) -> None:
    """Açılış ekranını kapatır; en az `MINIMUM_MS` görünmesini garantiler.

    Ana pencere buradan gösteriliyor, daha önce değil. Önceden pencere
    kurulur kurulmaz gösteriliyordu ve açılış ekranı hâlâ ekrandayken
    uygulama arkasında beliriyordu — iki şey aynı anda ekranda duruyordu.
    """
    if splash is None:
        target.setWindowOpacity(1.0)
        target.show()
        return

    gecen = (time.monotonic() - started_at) * 1000
    kalan = max(0, int(MINIMUM_MS - gecen))
    splash.finish(target, greeting, kalan)
