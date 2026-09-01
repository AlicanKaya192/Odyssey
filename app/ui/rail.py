"""Sol taraftaki dar ikon şeridi.

Uygulamanın ana bölümleri arasında geçiş sağlar. Dar tutulması bilinçli —
asıl yer içeriğe kalsın.

Simgeler emoji değil, gömülü SVG. Emoji her Windows sürümünde farklı
çiziliyor ve boyutu kontrol edilemiyor. Buna karşılık maketteki renkli
görünümü korumak için her bölüm kendi renginde çiziliyor; seçili olan tam
doygunlukta, diğerleri hafif soluk.

Simgeler **iki tonlu**: gövde kendi renginde düşük saydamlıkta doldurulup
üstüne çizgi çiziliyor. Yalnız çizgiden oluşan hâlleri şeritte cansız
duruyordu; dolgu ikonu zeminden ayırıyor ama renk tek kaldığı için tema
bozulmuyor.
"""

from __future__ import annotations

from PySide6.QtCore import QRectF, QSize, Qt, Signal
from PySide6.QtGui import (
    QColor,
    QFont,
    QIcon,
    QPainter,
    QPainterPath,
    QPen,
    QPixmap,
)
from PySide6.QtWidgets import QFrame, QPushButton, QVBoxLayout, QWidget

from ..core.avatar import load_avatar
from ..core.language import LanguageManager
from ..resources.icons import icon
from ..resources.theme.tokens import PALETTES, RAIL_COLORS, RAIL_WIDTH, SPACING
from ..widgets.effects import repolish

# (ekran anahtarı, ikon adı, çeviri anahtarı)
# Şerit iki öbeğe ayrılıyor.
#
# Üstte, logonun altında, her gün girilen ekranlar duruyor: öğrenme yolu ve
# profil. Altta, ayar simgesinin hemen üstünde, ara sıra açılan ekranlar var:
# sürüm notları ve Hakkında. İkisinin arasındaki boşluk, "burası günlük
# kullanım, şurası referans" ayrımını gözle görünür hâle getiriyor.
#
# Bağlantılarım, Ekstra İçerikler ve Lisans bir zamanlar burada ayrı
# simgelerdi; Bilgi ve SSS de eklenince şerit dokuz simgeye çıkacaktı.
# Beşi Hakkında ekranının sekmelerine taşındı.
TOP_DESTINATIONS = [
    ("journey", "home", "nav.path"),
    ("profile", "user", "nav.profile"),
]

BOTTOM_DESTINATIONS = [
    ("releases", "megaphone", "nav.releases"),
    ("about", "info", "nav.about"),
]

# Çevirilerin ve renklerin dolaştığı tam liste.
DESTINATIONS = TOP_DESTINATIONS + BOTTOM_DESTINATIONS

ICON_SIZE = 24

# İlerleme halkasının ölçüleri.
RING_SIZE = 40
RING_THICKNESS = 3
STROKE_ACTIVE = 2.4
STROKE_IDLE = 2.1

# Seçili olmayan simge biraz soluk; ama okunamayacak kadar değil.
IDLE_OPACITY = 0.72


def circular_icon(pixmap: QPixmap, size: int) -> QIcon:
    """Kare bir görselden yuvarlak simge üretir.

    Şeritteki profil düğmesi, kullanıcı fotoğraf koyduğunda onu gösteriyor.
    Kırpma burada elle yapılıyor: stil dosyasındaki `border-radius` görsele
    değil yalnızca widget'ın zeminine uygulanıyor.
    """
    kenar = size * 2  # yüksek yoğunluklu ekranlar için iki katı
    hedef = QPixmap(kenar, kenar)
    hedef.fill(Qt.GlobalColor.transparent)

    painter = QPainter(hedef)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

    daire = QPainterPath()
    daire.addEllipse(QRectF(0, 0, kenar, kenar))
    painter.setClipPath(daire)
    painter.drawPixmap(
        0,
        0,
        pixmap.scaled(
            kenar,
            kenar,
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation,
        ),
    )
    painter.end()

    hedef.setDevicePixelRatio(2.0)
    return QIcon(hedef)


class ProgressRing(QPushButton):
    """Genel ilerlemeyi gösteren küçük halka.

    Ortasında yüzde yazıyor. Sayı zaten karşılama kartında da var ama orası
    yalnızca ana ekranda görünüyor; ders okurken ya da alıştırma çözerken
    "ne kadarını bitirdim" sorusunun cevabı ekranda kalmıyordu.

    Halka saat on ikiden başlayıp saat yönünde ilerliyor — dolan bir çubuğun
    dairesel hâli. Qt açıları on altıda bir derece cinsinden istiyor.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._percent = 0
        self._track = QColor("#E3E6EC")
        self._fill = QColor("#4F46E5")
        self._text = QColor("#12151A")
        self.setFixedSize(RING_SIZE, RING_SIZE)
        self.setFlat(True)

    def set_percent(self, percent: int) -> None:
        percent = max(0, min(100, int(percent)))
        if percent != self._percent:
            self._percent = percent
            self.update()

    def set_colors(self, track: str, fill: str, text: str) -> None:
        self._track = QColor(track)
        self._fill = QColor(fill)
        self._text = QColor(text)
        self.update()

    def paintEvent(self, event) -> None:  # noqa: N802
        # Düğmenin kendi çizimi çağrılmıyor: stil dosyasındaki genel
        # QPushButton kuralı halkanın arkasına kutu koyuyordu.
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        yari = RING_THICKNESS / 2
        kutu = QRectF(
            yari, yari,
            self.width() - RING_THICKNESS,
            self.height() - RING_THICKNESS,
        )

        kalem = QPen(self._track, RING_THICKNESS)
        kalem.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(kalem)
        painter.drawEllipse(kutu)

        if self._percent:
            kalem.setColor(self._fill)
            painter.setPen(kalem)
            # 90 * 16 = saat on iki. Eksi işareti saat yönünü veriyor.
            painter.drawArc(kutu, 90 * 16, -int(360 * 16 * self._percent / 100))

        font = QFont(self.font())
        font.setPixelSize(12)
        font.setWeight(QFont.Weight.DemiBold)
        painter.setFont(font)
        painter.setPen(self._text)
        painter.drawText(
            self.rect(), Qt.AlignmentFlag.AlignCenter, f"%{self._percent}"
        )
        painter.end()


class RailButton(QPushButton):
    """Şerit düğmesi. Gerekirse üstünde bildirim noktası taşır."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._dot = False

    def set_dot(self, visible: bool) -> None:
        if self._dot != visible:
            self._dot = visible
            self.update()

    def paintEvent(self, event) -> None:  # noqa: N802
        super().paintEvent(event)
        if not self._dot:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(self.property("dot_color") or "#EF4444"))
        painter.drawEllipse(self.width() - 20, 10, 9, 9)
        painter.end()


class Rail(QFrame):
    """Ana bölümler arasında geçiş şeridi."""

    navigate = Signal(str)

    def __init__(self, language: LanguageManager, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._language = language
        self._mode = "light"
        self._current = "journey"
        self._buttons: dict[str, RailButton] = {}

        self.setProperty("role", "rail")
        self.setFixedWidth(RAIL_WIDTH)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, SPACING["lg"], 0, SPACING["lg"])
        layout.setSpacing(SPACING["xs"])
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # Şeridin tepesinde önce "A" harfi, sonra uygulamanın simgesi
        # duruyordu. İkisi de yer kaplayıp bir şey söylemiyordu: harf ne
        # olduğu belirsizdi, simge ise görev çubuğunda ve pencere başlığında
        # zaten var. Şimdi orada genel ilerleme halkası duruyor — şeritte
        # başka hiçbir yerde olmayan tek bilgi, her ekrandan görünüyor.
        self._progress = ProgressRing()
        self._progress.setCursor(Qt.CursorShape.PointingHandCursor)
        self._progress.clicked.connect(lambda: self.navigate.emit("journey"))
        layout.addWidget(self._progress, 0, Qt.AlignmentFlag.AlignHCenter)
        layout.addSpacing(SPACING["md"])

        for key, icon_name, _ in TOP_DESTINATIONS:
            layout.addWidget(
                self._make_button(key, icon_name), 0, Qt.AlignmentFlag.AlignHCenter
            )

        # Boşluk iki öbeğin arasında: alt öbek ayar simgesine yapışık kalıyor.
        layout.addStretch(1)

        for key, icon_name, _ in BOTTOM_DESTINATIONS:
            layout.addWidget(
                self._make_button(key, icon_name), 0, Qt.AlignmentFlag.AlignHCenter
            )

        layout.addSpacing(SPACING["sm"])
        layout.addWidget(
            self._make_button("settings", "settings"), 0, Qt.AlignmentFlag.AlignHCenter
        )

        self.set_mode(self._mode)
        self.retranslate()

    def _make_button(self, key: str, icon_name: str) -> RailButton:
        button = RailButton()
        button.setProperty("variant", "rail")
        button.setProperty("icon_name", icon_name)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.clicked.connect(lambda _=False, k=key: self.navigate.emit(k))
        self._buttons[key] = button
        return button

    # --- durum ------------------------------------------------------------

    def set_current(self, key: str) -> None:
        """Hangi bölümde olduğumuzu işaretler.

        Ayarlar bir pencere olarak açıldığı için kalıcı olarak işaretlenmez.
        """
        if key != "settings":
            self._current = key
        self._refresh_icons()

    def set_progress(self, percent: int) -> None:
        """Tepedeki halkanın gösterdiği genel ilerleme."""
        self._progress.set_percent(percent)
        self._progress.setToolTip(
            self._language.t("rail.progress", percent=percent)
        )

    def set_notification(self, key: str, visible: bool) -> None:
        """Bir bölümün üstündeki bildirim noktasını açar veya kapatır."""
        button = self._buttons.get(key)
        if button is not None:
            button.set_dot(visible)

    def refresh_avatar(self) -> None:
        """Profil fotoğrafı değişince çağrılıyor."""
        self._refresh_icons()

    def set_mode(self, mode: str) -> None:
        self._mode = mode
        self._refresh_icons()

    def _refresh_icons(self) -> None:
        """Simgeleri seçili duruma ve temaya göre yeniden çizer."""
        palette = PALETTES.get(self._mode, PALETTES["light"])
        colors = RAIL_COLORS.get(self._mode, RAIL_COLORS["light"])

        self._progress.set_colors(
            palette["border"], colors["journey"], palette["text"]
        )

        # Kullanıcı profil fotoğrafı koyduysa profil düğmesi onu gösteriyor.
        foto = load_avatar()

        for key, button in self._buttons.items():
            active = key == self._current

            if key == "profile" and foto is not None:
                button.setIcon(circular_icon(foto, ICON_SIZE))
                button.setIconSize(QSize(ICON_SIZE, ICON_SIZE))
                button.setProperty("active", "true" if active else "false")
                button.setProperty("dot_color", palette["danger"])
                repolish(button)
                continue

            color = QColor(colors.get(key, palette["text_muted"]))
            if not active:
                # Seçili olmayanı zeminle karıştırarak soluklaştırıyoruz.
                # setWindowOpacity gibi bir yol yok; renk seviyesinde yapılıyor.
                zemin = QColor(palette["surface_alt"])
                color = QColor(
                    round(color.red() * IDLE_OPACITY + zemin.red() * (1 - IDLE_OPACITY)),
                    round(color.green() * IDLE_OPACITY + zemin.green() * (1 - IDLE_OPACITY)),
                    round(color.blue() * IDLE_OPACITY + zemin.blue() * (1 - IDLE_OPACITY)),
                )

            button.setIcon(
                icon(
                    button.property("icon_name"),
                    color.name(),
                    ICON_SIZE,
                    stroke=STROKE_ACTIVE if active else STROKE_IDLE,
                    duotone=True,
                )
            )
            button.setIconSize(QSize(ICON_SIZE, ICON_SIZE))
            button.setProperty("active", "true" if active else "false")
            button.setProperty("dot_color", palette["danger"])
            repolish(button)

    def retranslate(self) -> None:
        for key, _, translation_key in DESTINATIONS:
            self._buttons[key].setToolTip(self._language.t(translation_key))
        self._buttons["settings"].setToolTip(self._language.t("settings.title"))
