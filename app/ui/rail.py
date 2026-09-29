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

from PySide6.QtCore import QPointF, QRectF, QSize, Qt, QTimer, Signal
from PySide6.QtGui import (
    QColor,
    QIcon,
    QPainter,
    QPainterPath,
    QPen,
    QPixmap,
)
from PySide6.QtWidgets import QFrame, QPushButton, QVBoxLayout, QWidget

from ..core.avatar import load_avatar
from ..core.language import LanguageManager
from ..resources.icons import MODERN_FILL_ACTIVE, MODERN_FILL_HOVER, icon
from ..resources.theme.tokens import mix
from ..widgets import motion
from ..resources.theme.tokens import PALETTES, RAIL_COLORS, RAIL_WIDTH, SPACING
from ..widgets.effects import repolish

# (ekran anahtarı, ikon adı, çeviri anahtarı)
# Şerit iki öbeğe ayrılıyor.
#
# Üstte her gün girilen ekranlar duruyor: en tepede profil (kişinin kendi
# fotoğrafı, şeridin en görünür yeri), altında öğrenme yolu ve hangi
# sırayla çalışılacağını anlatan rotalar. Altta, ayar
# simgesinin hemen üstünde, ara sıra açılan ekranlar var: sürüm notları ve
# Hakkında. Arama düğmesi ikisinin arasında, şeridin ortasında.
#
# Ortada önce genel ilerleme halkası duruyordu. Aynı yüzde öğrenme yolu
# ekranında zaten yazıyor; Alican 16 Eylül'de halkayı kaldırıp yerine
# aramayı koymak istedi.
#
# Bağlantılarım, Ekstra İçerikler ve Lisans bir zamanlar burada ayrı
# simgelerdi; Bilgi ve SSS de eklenince şerit dokuz simgeye çıkacaktı.
# Beşi Hakkında ekranının sekmelerine taşındı.
TOP_DESTINATIONS = [
    ("profile", "user", "nav.profile"),
    ("journey", "compass", "nav.path"),
    ("roadmap", "signpost", "nav.roadmap"),
    ("notes", "notebook", "nav.notes"),
]

# Şeridin ortasındaki düğme. Ekran değil, üstte açılan arama kutusu (`Ctrl+K`).
MIDDLE_DESTINATIONS = [
    ("search", "search", "nav.search"),
]

BOTTOM_DESTINATIONS = [
    ("releases", "megaphone", "nav.releases"),
    ("about", "info", "nav.about"),
]

# Çevirilerin ve renklerin dolaştığı tam liste.
DESTINATIONS = TOP_DESTINATIONS + MIDDLE_DESTINATIONS + BOTTOM_DESTINATIONS

ICON_SIZE = 24

# Simge çizgi kalınlıkları.
STROKE_ACTIVE = 2.1
STROKE_IDLE = 1.8

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


class RailIndicator(QWidget):
    """Seçili düğmenin arkasındaki zemin ve solundaki renkli çizgi (B3).

    Önce zemin her düğmenin kendi QSS'indeydi ve seçim değişince bir
    düğmeden sönüp ötekinde anında beliriyordu. Şimdi tek bir katman var:
    yeni düğmeye yayla kayıyor, rengi o bölümün rengine geçiyor.
    """

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self._y = 0.0
        self._color = QColor("#8B84FF")
        self._bg = QColor("#0A0C11")
        self._button = QRectF(0, 0, 52, 50)
        self._placed = False

    def set_background(self, color: str) -> None:
        self._bg = QColor(color)
        self.update()

    def move_to(self, button: QWidget, color: str) -> None:
        hedef_y = float(button.y())
        self._button = QRectF(button.x(), 0, button.width(), button.height())
        self.setGeometry(0, 0, self.parentWidget().width(), self.parentWidget().height())
        renk = QColor(color)
        if not self._placed:
            self._placed = True
            self._y, self._color = hedef_y, renk
            self.update()
            return
        motion.animate(self, "y", self._y, hedef_y, self._set_y, "spring", "spring")
        motion.animate(self, "c", QColor(self._color), renk, self._set_color, "base", "out")

    def _set_y(self, v: float) -> None:
        self._y = v
        self.update()

    def _set_color(self, c: QColor) -> None:
        self._color = c
        self.update()

    def paintEvent(self, event) -> None:  # noqa: N802
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        r = QRectF(self._button.x(), self._y, self._button.width(), self._button.height())
        zemin = QColor(mix(self._bg.name(), self._color.name(), 0.16))
        cerceve = QColor(self._color)
        cerceve.setAlphaF(0.28)
        p.setBrush(zemin)
        p.setPen(QPen(cerceve, 1))
        p.drawRoundedRect(r.adjusted(0.5, 0.5, -0.5, -0.5), 16, 16)
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(self._color)
        p.drawRoundedRect(QRectF(-2, r.center().y() - 10, 6, 20), 3, 3)


class RailButton(QPushButton):
    """Şerit düğmesi. Gerekirse üstünde bildirim noktası taşır."""

    hover_changed = Signal(bool)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._dot = False

    def enterEvent(self, event) -> None:  # noqa: N802
        super().enterEvent(event)
        self.hover_changed.emit(True)

    def leaveEvent(self, event) -> None:  # noqa: N802
        super().leaveEvent(event)
        self.hover_changed.emit(False)

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


class RailToggle(QPushButton):
    """Şeridi açıp kapatan küçük tutamak.

    Şeridin sağ kenarına, çizginin üstüne oturan dar bir hap: yarısı
    şeritte, yarısı içerikte. Fark edilecek kadar belirgin (kenarlık ve ok)
    ama bir düğme sırası kadar yer kaplamıyor. Şerit kapalıyken pencerenin
    sol kenarında duruyor; ok yönü ne olacağını gösteriyor.
    """

    # Arama simgesiyle aynı hizada duruyor; boyu simgeyle orantılı. 38
    # piksellikken simgenin yanında iri ve kaymış duruyordu (Alican).
    WIDTH = 14
    HEIGHT = 28

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setFixedSize(self.WIDTH, self.HEIGHT)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self._collapsed = False
        self._hover = False
        self._colors = PALETTES["light"]

    def set_collapsed(self, value: bool) -> None:
        self._collapsed = value
        self.update()

    def set_mode(self, mode: str) -> None:
        self._colors = PALETTES.get(mode, PALETTES["light"])
        self.update()

    def enterEvent(self, event) -> None:  # noqa: N802
        self._hover = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event) -> None:  # noqa: N802
        self._hover = False
        self.update()
        super().leaveEvent(event)

    def paintEvent(self, event) -> None:  # noqa: N802
        p = self._colors
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = QRectF(self.rect()).adjusted(0.5, 0.5, -0.5, -0.5)
        path = QPainterPath()
        path.addRoundedRect(rect, self.WIDTH / 2, self.WIDTH / 2)
        painter.fillPath(path, QColor(p["accent_soft"] if self._hover else p["surface"]))
        pen = QPen(QColor(p["accent"] if self._hover else p["border_strong"]))
        pen.setWidthF(1.0)
        painter.setPen(pen)
        painter.drawPath(path)

        ok = QPen(QColor(p["accent"] if self._hover else p["text_muted"]))
        ok.setWidthF(1.7)
        ok.setCapStyle(Qt.PenCapStyle.RoundCap)
        ok.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        painter.setPen(ok)
        cx, cy = self.width() / 2, self.height() / 2
        # Kapalıyken sağa (aç), açıkken sola (kapat) bakan ok.
        yon = 1 if self._collapsed else -1
        painter.drawPolyline([
            QPointF(cx - 1.6 * yon, cy - 4),
            QPointF(cx + 1.6 * yon, cy),
            QPointF(cx - 1.6 * yon, cy + 4),
        ])
        painter.end()


class Rail(QFrame):
    """Ana bölümler arasında geçiş şeridi."""

    navigate = Signal(str)

    def __init__(self, language: LanguageManager, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._language = language
        self._mode = "light"
        self._current = "journey"
        self._hovered = ""
        self._buttons: dict[str, RailButton] = {}
        # Seçili düğmenin kayan zemini; düğmelerin arkasında.
        self._indicator = RailIndicator(self)
        self._indicator.lower()

        self.setProperty("role", "rail")
        self.setFixedWidth(RAIL_WIDTH)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, SPACING["lg"], 0, SPACING["lg"])
        layout.setSpacing(SPACING["xs"])
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        for key, icon_name, _ in TOP_DESTINATIONS:
            layout.addWidget(
                self._make_button(key, icon_name), 0, Qt.AlignmentFlag.AlignHCenter
            )

        # Arama iki öbeğin arasında, şeridin ortasında. İki eşit esneme payı
        # onu boşluğun ortasına koyuyor, alt öbek ayar simgesine yapışık
        # kalıyor.
        layout.addStretch(1)
        for key, icon_name, _ in MIDDLE_DESTINATIONS:
            layout.addWidget(
                self._make_button(key, icon_name), 0, Qt.AlignmentFlag.AlignHCenter
            )
        layout.addStretch(1)

        for key, icon_name, _ in BOTTOM_DESTINATIONS:
            layout.addWidget(
                self._make_button(key, icon_name), 0, Qt.AlignmentFlag.AlignHCenter
            )

        layout.addSpacing(SPACING["sm"])
        layout.addWidget(
            self._make_button("settings", "sliders"), 0, Qt.AlignmentFlag.AlignHCenter
        )

        self.set_mode(self._mode)
        self.retranslate()

    def anchor_button(self) -> QWidget:
        """Açma/kapama tutamağının hizalandığı düğme (arama)."""
        return self._buttons["search"]

    def _make_button(self, key: str, icon_name: str) -> RailButton:
        button = RailButton()
        button.setProperty("variant", "rail")
        button.setProperty("icon_name", icon_name)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.clicked.connect(lambda _=False, k=key: self.navigate.emit(k))
        button.hover_changed.connect(lambda on, k=key: self._on_hover(k, on))
        self._buttons[key] = button
        return button

    def _on_hover(self, key: str, on: bool) -> None:
        self._hovered = key if on else ("" if self._hovered == key else self._hovered)
        self._refresh_icons()

    def _place_indicator(self) -> None:
        button = self._buttons.get(self._current)
        if button is None or not self.isVisible():
            return
        renk = RAIL_COLORS.get(self._mode, RAIL_COLORS["light"]).get(self._current, "#8B84FF")
        self._indicator.move_to(button, renk)

    def showEvent(self, event) -> None:  # noqa: N802
        super().showEvent(event)
        QTimer.singleShot(0, self._place_indicator)

    def resizeEvent(self, event) -> None:  # noqa: N802
        super().resizeEvent(event)
        self._indicator._placed = False  # noqa: SLF001 — boyut değişti, animasyonsuz yerleş
        QTimer.singleShot(0, self._place_indicator)

    # --- durum ------------------------------------------------------------

    def set_current(self, key: str) -> None:
        """Hangi bölümde olduğumuzu işaretler.

        Ayarlar bir pencere, arama bir kutu olarak açıldığı için kalıcı
        olarak işaretlenmez.
        """
        if key not in ("settings", "search"):
            self._current = key
        self._refresh_icons()
        self._place_indicator()

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
        self._indicator.set_background(PALETTES.get(mode, PALETTES["light"])["rail_bg"])
        self._refresh_icons()
        self._indicator._placed = False  # noqa: SLF001 — renk yeni temada, kaymadan
        self._place_indicator()

    def _refresh_icons(self) -> None:
        """Simgeleri seçili duruma ve temaya göre yeniden çizer."""
        palette = PALETTES.get(self._mode, PALETTES["light"])
        colors = RAIL_COLORS.get(self._mode, RAIL_COLORS["light"])

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
                    fill_opacity=(MODERN_FILL_ACTIVE if active
                                  else MODERN_FILL_HOVER if key == self._hovered else None),
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
        self._buttons["search"].setToolTip(f"{self._language.t('nav.search')}  (Ctrl+K)")
