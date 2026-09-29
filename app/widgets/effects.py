"""Qt stil dosyalarının veremediği görsel etkiler.

**Gölge ayrı bir katmanda çiziliyor, `QGraphicsDropShadowEffect` ile değil.**

QSS `box-shadow` desteklemiyor; önce `QGraphicsDropShadowEffect`
kullanılıyordu. O efekt, widget'ın içinde **herhangi bir şey** değiştiğinde
(alev titremesi, kart kalkması, sınav şıkkının dolması) bütün widget'ı
yeniden çizip bulanıklaştırıyor. 0.9.0'ın hareketleriyle Öğrenme Yolu
sayfasının bir çizimi 11 ms'den 24 ms'ye çıktı ve program takılmaya başladı
(ölçüldü, `Plan/araclar/akicilik_olc.py`); sınav kartında da siyah
bozulmalar görüldü.

Şimdi gölge, kartın **arkasında** duran ayrı bir widget (`ShadowLayer`):
bir kez hazırlanan yumuşak gölge resmini çiziyor ve kart kıpırdadıkça yalnızca
yerini değiştiriyor. Kartın içindeki animasyonlar gölgeyi hiç etkilemiyor.
Renkler yine `tokens.py`'den geliyor.
"""

from __future__ import annotations

from functools import lru_cache

from PySide6.QtCore import QEvent, QPoint, QRect, QRectF, Qt
from PySide6.QtGui import QColor, QPainter, QPainterPath, QPixmap
from PySide6.QtWidgets import QWidget

from ..resources.theme.tokens import PALETTES, shadow_color

# Katman sayısı: gölge bu kadar ince halkayla yumuşatılıyor.
LAYERS = 14


@lru_cache(maxsize=128)
def _shadow_pixmap(w: int, h: int, radius: float, blur: int, rgba: tuple, ratio: float) -> QPixmap:
    """`w×h` kartın `blur` kadar yayılan yumuşak gölgesi (kenarlarda pay)."""
    kenar = blur
    pix = QPixmap(round((w + 2 * kenar) * ratio), round((h + 2 * kenar) * ratio))
    pix.setDevicePixelRatio(ratio)
    pix.fill(Qt.GlobalColor.transparent)
    g = QPainter(pix)
    g.setRenderHint(QPainter.RenderHint.Antialiasing)
    g.setPen(Qt.PenStyle.NoPen)
    r, gr, b, a = rgba
    # İçten dışa, gittikçe genişleyen ve silikleşen halkalar: Gauss'a yakın.
    for i in range(LAYERS, 0, -1):
        oran = i / LAYERS
        genis = blur * oran
        alfa = a * (1 - oran) ** 1.6 * 2.2 / LAYERS
        g.setBrush(QColor(r, gr, b, max(0, min(255, round(alfa)))))
        g.drawRoundedRect(QRectF(kenar - genis, kenar - genis, w + 2 * genis, h + 2 * genis),
                          radius + genis, radius + genis)
    g.end()
    return pix


def _host_for(target: QWidget) -> QWidget | None:
    """Gölgenin durduğu widget: hedefin üstü; kart kaldırılan bir yuvadaysa
    (LiftSlot, kartın boyunda) gölge taşabilsin diye bir üstü."""
    host = target.parentWidget()
    while host is not None and host.property("shadow_passthrough"):
        host = host.parentWidget()
    return host


class ShadowLayer(QWidget):
    """Hedef widget'ın arkasında onun gölgesini çizen katman."""

    def __init__(self, target: QWidget, host: QWidget, mode: str, strong: bool, blur: int | None,
                 offset_y: int | None, radius: float, color: tuple | None = None) -> None:
        super().__init__(host)
        self._color = color
        self._target = target
        self._mode = mode
        self._strong = strong
        self._blur = blur if blur is not None else (40 if strong else 24)
        self._offset = offset_y if offset_y is not None else (12 if strong else 6)
        self._radius = radius
        self._strength = 0.0  # 0 normal gölge, 1 "kalkmış" (daha derin) gölge
        # Giriş animasyonu: gölge kartla birlikte belirir ve kayar.
        self._fade = 1.0
        self._shift = 0.0
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        target.installEventFilter(self)
        # Hedef bir ara widget'ın içindeyse o ara widget kıpırdayınca da izle.
        ara = target.parentWidget()
        while ara is not None and ara is not host:
            ara.installEventFilter(self)
            ara = ara.parentWidget()
        self._follow()

    def set_mode(self, mode: str) -> None:
        self._mode = mode
        self.update()

    def set_strength(self, k: float) -> None:
        """Kart üzerine gelince kalkarken gölge derinleşiyor (0 → 1)."""
        self._strength = max(0.0, min(1.0, k))
        self.update()

    def set_fade(self, opacity: float, shift: float = 0.0) -> None:
        """Giriş animasyonunda gölgenin saydamlığı ve dikey kayması."""
        self._fade = max(0.0, min(1.0, opacity))
        self._shift = shift
        self.update()

    def eventFilter(self, obj, event) -> bool:  # noqa: N802
        if event.type() in (QEvent.Type.Move, QEvent.Type.Resize, QEvent.Type.Show,
                            QEvent.Type.Hide, QEvent.Type.ZOrderChange):
            self._follow()
        return False

    def detach(self) -> None:
        self._target.removeEventFilter(self)
        ara = self._target.parentWidget()
        while ara is not None and ara is not self.parentWidget():
            ara.removeEventFilter(self)
            ara = ara.parentWidget()
        self.hide()
        self.deleteLater()

    def _follow(self) -> None:
        host = self.parentWidget()
        if host is None:
            return
        gorunur = self._target.isVisibleTo(host) if self._target is not host else False
        if not gorunur:
            self.hide()
            return
        yer = self._target.mapTo(host, QPoint(0, 0))
        pay = max(self._blur, 40) + 14
        self.setGeometry(QRect(yer.x() - pay, yer.y() - pay,
                               self._target.width() + 2 * pay, self._target.height() + 2 * pay))
        self._pay = pay
        self.show()
        if self._target.parentWidget() is host:
            self.stackUnder(self._target)
        else:
            self.lower()

    def paintEvent(self, event) -> None:  # noqa: N802
        w, h = self._target.width(), self._target.height()
        if w <= 0 or h <= 0:
            return
        g = QPainter(self)
        ratio = self.devicePixelRatioF() or 1.0
        pay = getattr(self, "_pay", 0)

        if self._fade <= 0.0:
            return

        def ciz(blur: int, ofs: float, strong: bool, opacity: float) -> None:
            rgba = tuple(self._color or shadow_color(self._mode, strong))
            pix = _shadow_pixmap(w, h, float(self._radius), blur, rgba, ratio)
            g.setOpacity(opacity * self._fade)
            g.drawPixmap(QPoint(pay - blur, round(pay - blur + ofs + self._shift)), pix)

        if self._strength < 1.0:
            ciz(self._blur, self._offset, self._strong, 1.0 - self._strength if self._strength else 1.0)
        if self._strength > 0.0:
            ciz(self._blur + 14, self._offset + 6, True, self._strength)


def apply_shadow(
    widget: QWidget,
    mode: str = "light",
    strong: bool = False,
    blur: int | None = None,
    offset_y: int | None = None,
    radius: float = 18.0,
    color: tuple | None = None,
) -> "_ShadowBinder":
    """Bir widget'a yumuşak gölge verir (arkasında ayrı katman).

    `strong=True` öne çıkan kartlar için (karşılama kartı, açılır pencere),
    varsayılan ise sıradan kartlar için.
    """
    baglayici = getattr(widget, "_shadow_binder", None)
    if baglayici is None:
        baglayici = _ShadowBinder(widget)
        widget._shadow_binder = baglayici  # noqa: SLF001 — PySide nesnesine Python özniteliği
    baglayici.params = (mode, strong, blur, offset_y, radius, color)
    baglayici.rebuild()
    return baglayici


class _ShadowBinder(QWidget):
    """Gölge katmanını hedef bir yere yerleşince (ve yeri değişince) kurar.

    Kartların çoğu gölgesini kurucusunda istiyor; o anda henüz bir üst
    widget'ları yok. Katman ilk görünüşte (ya da üst widget değişince) doğru
    yere kuruluyor.
    """

    def __init__(self, target: QWidget) -> None:
        super().__init__(target)
        self.hide()
        self._target = target
        self.params = ("light", False, None, None, 18.0, None)
        self.layer: ShadowLayer | None = None
        self._fade = (1.0, 0.0)
        target.installEventFilter(self)

    def rebuild(self) -> None:
        host = _host_for(self._target)
        if self.layer is not None:
            if self.layer.parentWidget() is host:
                self.layer.set_mode(self.params[0])
                return
            self.layer.detach()
            self.layer = None
        if host is None:
            return
        mode, strong, blur, offset_y, radius, color = self.params
        self.layer = ShadowLayer(self._target, host, mode, strong, blur, offset_y, radius, color)
        self.layer.set_fade(*self._fade)

    def eventFilter(self, obj, event) -> bool:  # noqa: N802
        if obj is self._target and event.type() in (QEvent.Type.ParentChange, QEvent.Type.Show):
            if self.layer is None or self.layer.parentWidget() is not _host_for(self._target):
                self.rebuild()
        return False

    # ShadowLayer'ın dışarıya açık işleri buradan da çağrılabilsin.
    def set_mode(self, mode: str) -> None:
        self.params = (mode,) + tuple(self.params[1:])
        if self.layer is not None:
            self.layer.set_mode(mode)

    def set_strength(self, k: float) -> None:
        if self.layer is not None:
            self.layer.set_strength(k)

    def set_fade(self, opacity: float, shift: float = 0.0) -> None:
        self._fade = (opacity, shift)
        if self.layer is not None:
            self.layer.set_fade(opacity, shift)


def shadow_of(widget: QWidget):
    return getattr(widget, "_shadow_binder", None)


def refresh_shadow(widget: QWidget, mode: str, strong: bool = False) -> None:
    """Tema değiştiğinde gölge rengini günceller."""
    baglayici = shadow_of(widget)
    if baglayici is not None:
        baglayici.set_mode(mode)


def repolish(widget: QWidget) -> None:
    """Qt özelliği (property) değişince stilin yeniden uygulanmasını sağlar.

    `setProperty` tek başına görünümü değiştirmiyor; stil motorunun widget'ı
    yeniden değerlendirmesi gerekiyor.
    """
    style = widget.style()
    style.unpolish(widget)
    style.polish(widget)
    widget.update()


def theme_mode() -> str:
    """Uygulanan tema ("light" / "dark"); ThemeManager.apply yazıyor."""
    from PySide6.QtWidgets import QApplication

    app = QApplication.instance()
    mode = app.property("theme_mode") if app is not None else None
    return mode if mode in PALETTES else "dark"


def theme_palette() -> dict:
    """Uygulanan temanın renkleri (tokens.PALETTES)."""
    return PALETTES[theme_mode()]
