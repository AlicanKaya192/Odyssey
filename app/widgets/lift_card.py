"""Üzerine gelince kalkan kart (ui-taslak.md B2).

İki parça:

- `GlowCard`: kartın kendisi (QFrame, zemini QSS'ten). Üzerine gelince
  `hover` 0 → 1 canlanıyor; kart bununla sol üst köşesinde vurgu renginde
  bir ışıma, üst kenarında ince renkli bir çizgi ve vurgu rengine dönen bir
  çerçeve çiziyor, gölgesi derinleşiyor. Hepsi `paintEvent`'te: QSS'te geçiş
  yok, `:hover` anında atlıyordu.
- `LiftSlot`: kartı taşıyan yuva. Kart yerleşimdeki yerinden oynatılamıyor
  (yerleşim konumu geri yazar), bu yüzden yuva kartı kendisi
  konumluyor ve yukarı kaldırıyor. Yuva kartın boyundan `LIFT` kadar uzun.

Kalkma yayla (`spring`), inme düz (`out`); ikisi de `motion` üzerinden, yani
Animasyonlar kapalıysa kart kalkmıyor, yalnızca rengi değişiyor.
"""

from __future__ import annotations

from PySide6.QtCore import Property, QEvent, QPointF, QRectF, QSize, Qt, Signal
from PySide6.QtGui import QColor, QLinearGradient, QPainter, QPainterPath, QPen, QRadialGradient
from PySide6.QtWidgets import QFrame, QSizePolicy, QWidget

from .effects import shadow_of

from ..resources.theme.tokens import PALETTES, RADIUS, mix
from . import motion

LIFT = 4
# Sıralı girişte kart 8 px aşağıdan geliyor (B8); yuvanın altında o kadar pay.
ENTER = 8
SHADOW_BLUR = (24, 38)
SHADOW_Y = (6, 12)


class GlowCard(QFrame):
    """Vurgu rengiyle ışıyan, üzerine gelince canlanan kart zemini."""

    hovered = Signal(bool)

    def __init__(self, parent: QWidget | None = None, interactive: bool = True) -> None:
        super().__init__(parent)
        self._hover = 0.0
        self._interactive = interactive
        self._accent = QColor("#8B84FF")
        self._mode = "dark"
        self._radius = RADIUS["lg"]

    def _get_hover(self) -> float:
        return self._hover

    def _set_hover(self, v: float) -> None:
        self._hover = v
        # Gölge ayrı katmanda (effects.ShadowLayer): yalnızca derinliği değişiyor.
        golge = shadow_of(self)
        if golge is not None:
            golge.set_strength(max(0.0, min(1.0, v)))
        self.update()

    hover = Property(float, _get_hover, _set_hover)

    def set_accent(self, color: str) -> None:
        self._accent = QColor(color)
        self.update()

    def set_card_mode(self, mode: str) -> None:
        self._mode = mode
        self.update()

    def set_interactive(self, value: bool) -> None:
        self._interactive = value

    def enterEvent(self, event) -> None:  # noqa: N802
        super().enterEvent(event)
        if self._interactive:
            motion.animate_property(self, "hover", 1.0, "micro", "out")
            self.hovered.emit(True)

    def leaveEvent(self, event) -> None:  # noqa: N802
        super().leaveEvent(event)
        if self._interactive:
            motion.animate_property(self, "hover", 0.0, "base", "out")
            self.hovered.emit(False)

    def paintEvent(self, event) -> None:  # noqa: N802
        super().paintEvent(event)
        k = max(0.0, min(1.0, self._hover))
        if k <= 0.001:
            return
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        r = QRectF(self.rect()).adjusted(0.5, 0.5, -0.5, -0.5)
        yol = QPainterPath()
        yol.addRoundedRect(r, self._radius, self._radius)
        p.setClipPath(yol)
        koyu = self._mode == "dark"
        # Sol üstte vurgu renginde ışıma.
        isik = QRadialGradient(QPointF(r.left(), r.top()), max(160.0, r.width() * 0.8))
        renk = QColor(self._accent)
        renk.setAlpha(int((46 if koyu else 30) * k))
        isik.setColorAt(0.0, renk)
        renk.setAlpha(0)
        isik.setColorAt(1.0, renk)
        p.fillRect(r, isik)
        # Üst kenarda ince renkli çizgi (vurgudan saydama).
        cizgi = QLinearGradient(r.left(), 0, r.right(), 0)
        c1 = QColor(self._accent)
        c1.setAlphaF(k)
        c2 = QColor(self._accent)
        c2.setAlphaF(0.25 * k)
        cizgi.setColorAt(0.0, c1)
        cizgi.setColorAt(1.0, c2)
        p.fillRect(QRectF(r.left(), r.top(), r.width(), 3), cizgi)
        p.setClipping(False)
        # Çerçeve vurgu rengine döner.
        kenar = QColor(mix(PALETTES[self._mode]["border"], self._accent.name(), 0.6))
        kenar.setAlphaF(k)
        p.setPen(QPen(kenar, 1))
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawPath(yol)


class LiftSlot(QWidget):
    """Kartı taşıyan yuva: kart üzerine gelince `LIFT` piksel yukarı kalkar."""

    def __init__(self, card: GlowCard, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._card = card
        self._offset = 0.0
        card.setParent(self)
        card.installEventFilter(self)
        card.hovered.connect(self._on_hover)
        # Kartın gölgesi yuvanın bir üstünde çizilsin (yuva kartın boyunda).
        self.setProperty("shadow_passthrough", True)
        pol = card.sizePolicy()
        self.setSizePolicy(pol.horizontalPolicy(), QSizePolicy.Policy.Fixed)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self._sync_height()

    @property
    def card(self) -> GlowCard:
        return self._card

    def _get_offset(self) -> float:
        return self._offset

    def _set_offset(self, v: float) -> None:
        self._offset = v
        self._place()

    lift = Property(float, _get_offset, _set_offset)

    def _on_hover(self, on: bool) -> None:
        if on:
            motion.animate_property(self, "lift", float(LIFT), "spring", "spring")
        else:
            motion.animate_property(self, "lift", 0.0, "base", "out")

    def _sync_height(self) -> None:
        self.setFixedHeight(self._card.height() + LIFT + ENTER)
        self._place()

    def _place(self) -> None:
        self._card.setGeometry(0, round(LIFT - self._offset), self.width(), self._card.height())

    def sizeHint(self) -> QSize:  # noqa: N802
        s = self._card.sizeHint()
        return QSize(s.width(), self._card.height() + LIFT + ENTER)

    def minimumSizeHint(self) -> QSize:  # noqa: N802
        s = self._card.minimumSizeHint()
        return QSize(s.width(), self._card.height() + LIFT + ENTER)

    def resizeEvent(self, event) -> None:  # noqa: N802
        super().resizeEvent(event)
        self._place()

    def eventFilter(self, obj, event) -> bool:  # noqa: N802
        if obj is self._card and event.type() == QEvent.Type.Resize:
            if self.height() != self._card.height() + LIFT + ENTER:
                self.setFixedHeight(self._card.height() + LIFT + ENTER)
        return False
