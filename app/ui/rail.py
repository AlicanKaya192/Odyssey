"""Sol taraftaki dar ikon şeridi.

Uygulamanın ana bölümleri arasında geçiş sağlar. Dar tutulması bilinçli —
asıl yer içeriğe kalsın.

Simgeler emoji değil, gömülü SVG. Emoji her Windows sürümünde farklı
çiziliyor ve boyutu kontrol edilemiyor. Buna karşılık maketteki renkli
görünümü korumak için her bölüm kendi renginde çiziliyor; seçili olan tam
doygunlukta, diğerleri hafif soluk.
"""

from __future__ import annotations

from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import QFrame, QLabel, QPushButton, QVBoxLayout, QWidget

from ..core.language import LanguageManager
from ..resources.icons import icon
from ..resources.theme.tokens import PALETTES, RAIL_COLORS, RAIL_WIDTH, SPACING
from ..widgets.effects import repolish

# (ekran anahtarı, ikon adı, çeviri anahtarı)
# Şerit iki öbeğe ayrılıyor.
#
# Üstte, logonun altında, her gün girilen ekranlar duruyor: öğrenme yolu,
# profil, projeler. Altta, ayar simgesinin hemen üstünde, ara sıra açılan
# ekranlar var: sürüm notları, bağlantılar, lisans. İkisinin arasındaki
# boşluk, "burası günlük kullanım, şurası referans" ayrımını gözle görünür
# hâle getiriyor.
TOP_DESTINATIONS = [
    ("journey", "home", "nav.path"),
    ("profile", "user", "nav.profile"),
    ("extras", "package", "nav.extras"),
]

BOTTOM_DESTINATIONS = [
    ("releases", "megaphone", "nav.releases"),
    ("links", "link", "nav.links"),
    ("license", "scale", "nav.license"),
]

# Çevirilerin ve renklerin dolaştığı tam liste.
DESTINATIONS = TOP_DESTINATIONS + BOTTOM_DESTINATIONS

ICON_SIZE = 24
STROKE_ACTIVE = 2.4
STROKE_IDLE = 2.1

# Seçili olmayan simge biraz soluk; ama okunamayacak kadar değil.
IDLE_OPACITY = 0.72


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

        self._logo = QLabel("A")
        self._logo.setProperty("role", "logo")
        self._logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._logo, 0, Qt.AlignmentFlag.AlignHCenter)
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

    def set_notification(self, key: str, visible: bool) -> None:
        """Bir bölümün üstündeki bildirim noktasını açar veya kapatır."""
        button = self._buttons.get(key)
        if button is not None:
            button.set_dot(visible)

    def set_mode(self, mode: str) -> None:
        self._mode = mode
        self._refresh_icons()

    def _refresh_icons(self) -> None:
        """Simgeleri seçili duruma ve temaya göre yeniden çizer."""
        palette = PALETTES.get(self._mode, PALETTES["light"])
        colors = RAIL_COLORS.get(self._mode, RAIL_COLORS["light"])

        for key, button in self._buttons.items():
            active = key == self._current
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
