"""Açılan kutuların giriş/çıkış efekti (prototip `.palette`, `.modal`).

Kutu saydamlıktan belirir, %96'dan büyür ve 10 px aşağıdan yerine oturur.
`QGraphicsEffect` kutuyu ekran dışında bir görüntüye çizip onu dönüştürüyor;
böylece içerideki satırların kendi animasyonları da görüntüye giriyor.

Efekt **yalnızca animasyon süresince** takılı: kalıcı bir grafik efekti
her çizimi ekran dışından geçirdiği için pahalı (gölge efektinde ölçüldü).
"""

from __future__ import annotations

from PySide6.QtCore import QPoint, QPointF, Qt
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QGraphicsEffect, QWidget

from ..resources.theme.motion import out_cubic
from . import motion


class PopEffect(QGraphicsEffect):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.opacity = 1.0
        self.scale = 1.0
        self.dy = 0.0
        # Ölçeğin merkezi (widget koordinatında); yoksa kendi ortası.
        self.origin: QPointF | None = None

    def set_state(self, opacity: float, scale: float, dy: float) -> None:
        self.opacity, self.scale, self.dy = opacity, scale, dy
        self.update()

    def draw(self, painter: QPainter) -> None:  # noqa: D102
        # PySide konumu döndürmüyor; dolgusuz kipte görüntü kaynağın sınır
        # dikdörtgeninin köşesinde duruyor.
        pix = self.sourcePixmap(Qt.CoordinateSystem.LogicalCoordinates, QPoint(),
                                QGraphicsEffect.PixmapPadMode.NoPad)
        if pix.isNull():
            return
        ofs = self.sourceBoundingRect(Qt.CoordinateSystem.LogicalCoordinates).topLeft()
        painter.save()
        painter.setOpacity(max(0.0, min(1.0, self.opacity)))
        if abs(self.scale - 1.0) < 0.003:
            # Ölçek yok: görüntü doğrudan, tam piksele çiziliyor. Yumuşatarak
            # ölçekleme her karede pahalıydı (arama açılırken kare 19–25 ms).
            painter.drawPixmap(QPointF(ofs.x(), ofs.y() + round(self.dy)), pix)
            painter.restore()
            return
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        w = pix.width() / pix.devicePixelRatio()
        h = pix.height() / pix.devicePixelRatio()
        merkez = self.origin if self.origin is not None else QPointF(ofs.x() + w / 2, ofs.y() + h / 2)
        painter.translate(merkez.x(), merkez.y() + self.dy)
        painter.scale(self.scale, self.scale)
        painter.translate(-merkez.x(), -merkez.y())
        painter.drawPixmap(ofs, pix)
        painter.restore()


def pop_in(widget: QWidget, on_done=None) -> None:
    """Saydamlık 180 ms, ölçek ve kayma 420 ms yayla (prototip `.on`)."""
    _run(widget, True, on_done)


def pop_out(widget: QWidget, on_done=None) -> None:
    """Kısa ve hızlanarak kaybolur (180 ms)."""
    _run(widget, False, on_done)


def _run(widget: QWidget, opening: bool, on_done) -> None:
    from .effects import shadow_of

    if not motion.enabled():
        if on_done:
            on_done()
        return
    etki = PopEffect(widget)
    widget.setGraphicsEffect(etki)
    golge = shadow_of(widget)

    def adim(t: float) -> None:
        if opening:
            from ..resources.theme.motion import spring
            o = out_cubic(min(1.0, t * 420 / 180))
            k = spring(t)
            etki.set_state(o, 0.96 + 0.04 * k, 10 * (1 - k))
        else:
            from ..resources.theme.motion import in_cubic
            k = in_cubic(t)
            o = 1 - k
            etki.set_state(o, 1 - 0.04 * k, 10 * k)
        if golge is not None:
            golge.set_fade(o)

    def bitti() -> None:
        widget.setGraphicsEffect(None)
        if golge is not None:
            golge.set_fade(1.0 if opening else 0.0)
        if on_done:
            on_done()

    adim(0.0)
    motion.animate(widget, "pop", 0.0, 1.0, adim, "spring" if opening else "short", "linear", on_done=bitti)


def enter(widget: QWidget, dy: float, duration_name="spring", delay: int = 0,
          shadow_of_widget: QWidget | None = None, hold: bool = False):
    """Prototipin giriş kareleri: saydamdan, `dy` piksel aşağıdan yerine.

    - ekran `pgIn`: 16 px, 420 ms yay
    - kart `sIn`: 8 px, 420 ms yay, sırayla
    - başlık `hIn`: 4 px, 180 ms

    Efekt ilk karede hemen takılıyor (gecikme süresince görünmez kalsın) ve
    bitince kaldırılıyor. Efekt parçanın görüntüsünü bir kez alıyor; yalnızca
    saydamlık ve konum değiştiği için her karede yeniden çizim yok.

    `hold`: parça hemen gizlenir ama animasyon başlamaz; dönen işlev
    çağrılınca başlar. Pencerenin ilk çizimi olay döngüsünü ~250 ms
    tutuyor; animasyon ondan önce başlarsa o süre "yenip" iş bitmiş
    görünüyordu. Çağıran ilk çizimden sonra başlatıyor.
    """
    from ..resources.theme.motion import spring
    from .effects import shadow_of

    if not motion.enabled() or widget is None:
        return
    etki = PopEffect(widget)
    widget.setGraphicsEffect(etki)
    golge = shadow_of(shadow_of_widget or widget)
    yay = duration_name == "spring"

    def adim(t: float) -> None:
        k = spring(t) if yay else out_cubic(t)
        o = max(0.0, min(1.0, k))
        try:
            etki.set_state(o, 1.0, dy * (1 - k))
        except RuntimeError:
            return  # yerine yeni bir giriş efekti takıldı
        if golge is not None:
            golge.set_fade(o, dy * (1 - k))

    def bitti() -> None:
        try:
            if widget.graphicsEffect() is etki:
                widget.setGraphicsEffect(None)
        except RuntimeError:
            return
        # Efekt kalkınca parça yeniden çizilsin; yoksa efektin son (saydam)
        # görüntüsü ekranda kalabiliyordu (Notlarım başlığı geç belirdi).
        widget.update()
        ust = widget.parentWidget()
        if ust is not None:
            ust.update(widget.geometry())
        if golge is not None:
            golge.set_fade(1.0)

    def basla() -> None:
        try:
            if widget.graphicsEffect() is not etki:
                return  # bu arada başka bir giriş efekti takıldı
        except RuntimeError:
            return
        motion.animate(widget, "enter", 0.0, 1.0, adim, duration_name, "linear", delay=delay, on_done=bitti)

    adim(0.0)
    if hold:
        return basla
    basla()
    return None
