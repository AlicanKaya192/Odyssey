"""Yol düğmesi (ui-taslak.md C3).

Önce QSS'le boyanan düz bir düğmeydi; durum değişince renk anında atlıyor,
yol açılırken bir şey olmuyordu. Şimdi kendisi çiziyor:

- **tamamlandı**: patikanın renginde degrade daire, beyaz onay;
- **şu an**: vurgu renginde, daha büyük, oynat işareti ve çevresinden
  yavaşça açılıp sönen bir halka (döngü; pencere etkin değilken ya da
  Animasyonlar kapalıyken durur, ui-taslak §1.6);
- **devam ediyor**: uyarı renginde, sıra numarası;
- **başlanmadı**: nötr daire, sıra numarası;
- **kilitli**: nötr daire, kilit; **yakında**: kesik çerçeve.

Hareketler: yol ilk açıldığında düğme esneyerek belirir (`appear`), üzerine
gelince yayla büyür, tamamlanınca rengi değişip onay zıplar (`set_state`).
"""

from __future__ import annotations

from PySide6.QtCore import Property, QPointF, QRectF, QSize, Qt, QTimer
from PySide6.QtGui import QColor, QFont, QIcon, QLinearGradient, QPainter, QPen
from PySide6.QtWidgets import QApplication, QPushButton, QWidget

from ..resources.theme.motion import DURATION, bounce, out_cubic
from ..resources.theme.tokens import mix
from . import motion
from .effects import theme_palette

# Düğmenin görünen dairesi 82 px'lik alana sığıyor; çevresinde her yönde
# `PAD` kadar çizim payı var. Üzerine gelince büyüme, gölge ve "şu an"
# halkası bu paya taşıyor; pay yokken köşelerden kırpılıyordu (Alican:
# "köşelerden sıkıştırıyor"). Yol satırları bu pay kadar üst üste biniyor
# (`PathView`), yerleşim değişmiyor.
PAD = 14
SIZE = 82 + 2 * PAD
RADIUS = 37
RADIUS_CURRENT = 40
RING_PERIOD = 2400


class NodeButton(QPushButton):
    def __init__(self, state: str, order: int, color: str, lock_color: str = "",
                 parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._state = state
        self._order = order
        self._color = QColor(color)
        self._lock_color = lock_color or "#FBBF24"
        self._appear = 1.0
        self._hover = 0.0
        self._pop = 1.0      # onayın esnemesi (tamamlanınca)
        self._blend = 1.0    # eski durumdan yenisine renk geçişi
        self._from_state = state
        self._ring = 0.0
        self.setProperty("variant", "node-painted")
        self.setFixedSize(SIZE, SIZE)
        self.setFocusPolicy(Qt.FocusPolicy.TabFocus)
        self._ring_timer = QTimer(self)
        self._ring_timer.setInterval(16)
        self._ring_timer.timeout.connect(self._tick_ring)
        self._ring_clock = 0
        motion.on_enabled_changed(lambda _on: self._sync_ring(), owner=self)

    # --- canlandırılan özellikler
    def _prop(name):  # noqa: N805 — sınıf gövdesinde yardımcı
        def get(self):
            return getattr(self, "_" + name)

        def set_(self, v):
            setattr(self, "_" + name, v)
            self.update()
        return Property(float, get, set_)

    appear = _prop("appear")
    hover = _prop("hover")
    pop = _prop("pop")
    blend = _prop("blend")
    del _prop

    @property
    def state(self) -> str:
        return self._state

    def sizeHint(self) -> QSize:  # noqa: N802
        return QSize(SIZE, SIZE)

    def hitButton(self, pos) -> bool:  # noqa: N802
        dx = pos.x() - self.width() / 2
        dy = pos.y() - self.height() / 2
        return dx * dx + dy * dy <= (RADIUS_CURRENT + 2) ** 2

    # --- hareketler
    def start_appear(self, delay: int) -> None:
        """Yol ilk açılınca: küçükten esneyerek belirir."""
        self._appear = 0.0
        motion.animate_property(self, "appear", 1.0, "bounce", "linear", start=0.0, delay=delay)

    def set_state(self, state: str, animate: bool = True) -> None:
        if state == self._state:
            return
        self._from_state = self._state
        self._state = state
        if animate:
            motion.animate_property(self, "blend", 1.0, "short", "out", start=0.0)
            if state == "completed":
                motion.animate_property(self, "pop", 1.0, "bounce", "linear", start=0.0)
        else:
            self._blend = 1.0
            self._pop = 1.0
        self._sync_ring()
        self.update()

    def enterEvent(self, event) -> None:  # noqa: N802
        super().enterEvent(event)
        if self.isEnabled():
            motion.animate_property(self, "hover", 1.0, "spring", "spring")

    def leaveEvent(self, event) -> None:  # noqa: N802
        super().leaveEvent(event)
        motion.animate_property(self, "hover", 0.0, "base", "out")

    # --- "şu an buradasın" halkası
    def _sync_ring(self) -> None:
        calissin = (self._state == "current" and motion.enabled() and self.isVisible())
        if calissin and not self._ring_timer.isActive():
            self._ring_timer.start()
        elif not calissin and self._ring_timer.isActive():
            self._ring_timer.stop()
            self._ring = 0.0
            self.update()

    def _tick_ring(self) -> None:
        pencere = self.window()
        if pencere is not None and not pencere.isActiveWindow():
            return
        self._ring_clock = (self._ring_clock + 16) % RING_PERIOD
        self._ring = self._ring_clock / RING_PERIOD
        self.update()

    def showEvent(self, event) -> None:  # noqa: N802
        super().showEvent(event)
        self._sync_ring()

    def hideEvent(self, event) -> None:  # noqa: N802
        super().hideEvent(event)
        self._ring_timer.stop()

    # --- çizim
    def _fill_for(self, state: str, p: dict) -> tuple[QColor, QColor, QColor]:
        """(üst, alt, çerçeve) renkleri."""
        if state == "completed":
            return QColor(mix(self._color.name(), "#FFFFFF", 0.3)), self._color, QColor(mix(self._color.name(), "#FFFFFF", 0.35))
        if state == "current":
            return QColor(p["accent_hover"]), QColor(p["accent_second"]), QColor(p["accent"])
        if state == "in_progress":
            return QColor(mix(p["warning"], "#FFFFFF", 0.2)), QColor(p["warning"]), QColor(p["warning"])
        if state == "planned":
            return QColor(0, 0, 0, 0), QColor(0, 0, 0, 0), QColor(p["border"])
        return QColor(p["field"]), QColor(p["surface_alt"]), QColor(p["border_strong"])

    def paintEvent(self, event) -> None:  # noqa: N802
        p = theme_palette()
        g = QPainter(self)
        g.setRenderHint(QPainter.RenderHint.Antialiasing)
        merkez = QPointF(self.width() / 2, self.height() / 2)
        olcek = bounce(self._appear) * (1 + 0.08 * self._hover)
        if olcek <= 0.01:
            return
        g.translate(merkez)
        g.scale(olcek, olcek)

        r = RADIUS_CURRENT if self._state == "current" else RADIUS
        # Kilitli bölüm prototipte `.pnode.locked { opacity: .55 }`.
        if self._state == "locked":
            g.setOpacity(0.55)
        k = out_cubic(max(0.0, min(1.0, self._blend)))
        ust, alt, cerceve = self._fill_for(self._state, p)
        if k < 1.0:
            u0, a0, c0 = self._fill_for(self._from_state, p)
            ust = QColor(mix(u0.name(), ust.name(), k)) if u0.alpha() and ust.alpha() else ust
            alt = QColor(mix(a0.name(), alt.name(), k)) if a0.alpha() and alt.alpha() else alt
            r = r if self._from_state != "current" else RADIUS_CURRENT + (r - RADIUS_CURRENT) * k

        # "Şu an" halkası: dışa açılıp söner.
        if self._state == "current" and self._ring > 0:
            halka = QColor(p["accent"])
            halka.setAlphaF(0.4 * (1 - self._ring))
            g.setPen(QPen(halka, 2))
            g.setBrush(Qt.BrushStyle.NoBrush)
            rr = r + 2 + (PAD - 3) * out_cubic(self._ring)
            g.drawEllipse(QPointF(0, 0), rr, rr)

        # Yumuşak gölge.
        if self._state not in ("planned",):
            golge = QColor(0, 0, 0, 60 if QApplication.instance().property("theme_mode") == "dark" else 26)
            if self._state in ("completed", "current"):
                golge = QColor(alt)
                golge.setAlpha(90)
            g.setPen(Qt.PenStyle.NoPen)
            g.setBrush(golge)
            g.drawEllipse(QPointF(0, 4), r * 0.92, r * 0.92)

        degrade = QLinearGradient(QPointF(-r, -r), QPointF(r, r))
        degrade.setColorAt(0.0, ust)
        degrade.setColorAt(1.0, alt)
        if self._state == "planned":
            kalem = QPen(cerceve, 2, Qt.PenStyle.DashLine)
            g.setPen(kalem)
            g.setBrush(Qt.BrushStyle.NoBrush)
        else:
            g.setPen(QPen(cerceve, 2))
            g.setBrush(degrade)
        g.drawEllipse(QPointF(0, 0), r - 1, r - 1)

        # İçerik.
        beyaz = QColor("#FFFFFF")
        if self._state == "completed":
            s = bounce(self._pop)
            g.save()
            g.scale(s, s)
            g.setPen(QPen(beyaz, 3.4, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
            g.drawPolyline([QPointF(-9, 0.5), QPointF(-2.5, 7), QPointF(10, -6.5)])
            g.restore()
        elif self._state == "current":
            g.setPen(Qt.PenStyle.NoPen)
            g.setBrush(beyaz)
            from PySide6.QtGui import QPolygonF
            g.drawPolygon(QPolygonF([QPointF(-6, -10), QPointF(11, 0), QPointF(-6, 10)]))
        else:
            f = QFont(self.font())
            f.setPixelSize(20)
            f.setWeight(QFont.Weight.Bold)
            g.setFont(f)
            if self._state == "in_progress":
                g.setPen(beyaz)
            else:
                # Girilmemiş bölümün numarası saydam (Alican; prototipte soluk).
                sayi = QColor(p["text_muted"])
                sayi.setAlphaF(0.45)
                g.setPen(sayi)
            g.drawText(QRectF(-r, -r, 2 * r, 2 * r), Qt.AlignmentFlag.AlignCenter, str(self._order))
