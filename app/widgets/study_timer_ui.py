"""Çalışma zamanlayıcısının arayüzü: alt şeritteki küçük sayaç ve paneli.

Sayaç **dikkat dağıtmasın** (Alican): alt şeridin sağında, telif yazısıyla
aynı boyda küçük bir halka ve kalan süre. Evrenin son `FINAL_SECONDS`
saniyesinde hafifçe büyüyüp belirginleşiyor; başka hiçbir anda hareket
etmiyor. Boştayken yalnızca saat simgesi.

Panel kısayol paneliyle aynı katman (`popover.py`): düzen seçimi ve
başlatma, çalışırken kalan süre, duraklat / devam, molayı atla, bitir.
"""

from __future__ import annotations

import math

from PySide6.QtCore import QRectF, QSize, Qt, Signal
from PySide6.QtGui import QColor, QFont, QFontMetrics, QPainter, QPen
from PySide6.QtWidgets import (
    QAbstractButton,
    QButtonGroup,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from ..core import study_timer as core
from ..core.language import LanguageManager
from ..resources.icons import icon
from ..resources.theme.tokens import FONTS, PALETTES, SPACING
from . import motion
from .common import DropdownBox
from .popover import Popover

PANEL_WIDTH = 380
CHIP_HEIGHT = 20
ICON = 14
RING = 11
FONT_PX = 11.5
# Son saniyelerde en fazla bu kadar büyüyor.
GROW = 0.16

# Düzen kartlarının simgesi (Lucide); her düzen kendi ritmini anlatıyor.
PRESET_ICONS = {"pomodoro": "repeat", "flow": "wave", "deep": "target", "short": "zap", "custom": "sliders"}
TILE_HEIGHT = 58
PREVIEW_HEIGHT = 138
# Önizleme şeridinde gösterilen tur sayısı (Pomodoro'nun bir döngüsü).
CYCLE_ROUNDS = 4
ACTIVE_RING = 168


def _phase_color(timer: core.StudyTimer, p: dict) -> str:
    return p["success"] if timer.phase == "break" else p["accent"]


def _px_font(base: QFont, px: float, weight: QFont.Weight = QFont.Weight.Normal, family: str = "") -> QFont:
    f = QFont(base)
    if family:
        f.setFamilies([part.strip().strip('"') for part in family.split(",")])
    f.setPixelSize(round(px))
    f.setWeight(weight)
    return f


def _cycle(preset: core.Preset) -> list[tuple[str, int]]:
    """Önizleme şeridinin parçaları: [("work", 25), ("rest", 5), ...]."""
    parcalar: list[tuple[str, int]] = []
    for tur in range(1, CYCLE_ROUNDS + 1):
        parcalar.append(("work", preset.work))
        if preset.long_every and tur % preset.long_every == 0 and preset.long_rest:
            parcalar.append(("long", preset.long_rest))
        elif preset.rest:
            parcalar.append(("rest", preset.rest))
    return parcalar


class PresetTile(QAbstractButton):
    """Düzen kartı: simge dairesi, ad ve "25 / 5 dk". Seçili olan vurgu renginde."""

    def __init__(self, kimlik: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.kimlik = kimlik
        self._mode = "dark"
        self._name = ""
        self._line = ""
        self.setCheckable(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setAttribute(Qt.WidgetAttribute.WA_Hover)
        self.setFixedHeight(TILE_HEIGHT)

    def set_texts(self, name: str, line: str) -> None:
        self._name, self._line = name, line
        self.setAccessibleName(f"{name}, {line}")
        self.update()

    def set_mode(self, mode: str) -> None:
        self._mode = mode
        self.update()

    def sizeHint(self) -> QSize:  # noqa: N802
        return QSize(150, TILE_HEIGHT)

    def paintEvent(self, event) -> None:  # noqa: N802
        p = PALETTES.get(self._mode, PALETTES["dark"])
        secili = self.isChecked()
        uzerinde = self.underMouse()
        g = QPainter(self)
        g.setRenderHint(QPainter.RenderHint.Antialiasing)
        kutu = QRectF(self.rect()).adjusted(0.75, 0.75, -0.75, -0.75)
        zemin = p["accent_soft"] if secili else (p["surface_hover"] if uzerinde else p["surface_alt"])
        g.setBrush(QColor(zemin))
        cerceve = p["accent"] if secili else (p["border_strong"] if uzerinde else p["border"])
        g.setPen(QPen(QColor(cerceve), 1.5 if secili else 1))
        g.drawRoundedRect(kutu, 12, 12)

        # Simge dairesi
        cap = 32
        daire = QRectF(12, (self.height() - cap) / 2, cap, cap)
        g.setPen(Qt.PenStyle.NoPen)
        g.setBrush(QColor(p["accent"] if secili else p["surface"]))
        g.drawEllipse(daire)
        renk = p["text_inverse"] if secili else p["text_muted"]
        simge = icon(PRESET_ICONS.get(self.kimlik, "clock"), renk, 16).pixmap(QSize(16, 16), self.devicePixelRatioF())
        g.drawPixmap(QRectF(daire.center().x() - 8, daire.center().y() - 8, 16, 16), simge, QRectF(simge.rect()))

        x = daire.right() + 10
        alan = QRectF(x, 0, self.width() - x - 10, self.height())
        g.setPen(QColor(p["accent"] if secili else p["text"]))
        g.setFont(_px_font(self.font(), 13, QFont.Weight.DemiBold))
        ust = QRectF(alan.x(), self.height() / 2 - 18, alan.width(), 18)
        g.drawText(ust, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom,
                   QFontMetrics(g.font()).elidedText(self._name, Qt.TextElideMode.ElideRight, int(ust.width())))
        g.setPen(QColor(p["text_muted"]))
        g.setFont(_px_font(self.font(), 11.5))
        alt = QRectF(alan.x(), self.height() / 2 + 2, alan.width(), 16)
        g.drawText(alt, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop,
                   QFontMetrics(g.font()).elidedText(self._line, Qt.TextElideMode.ElideRight, int(alt.width())))
        g.end()


class PresetPreview(QWidget):
    """Seçili düzenin özeti: odak/mola oranı halkası, ad, açıklama ve dört
    turluk döngü şeridi (odak mor, mola yeşil, uzun mola koyu yeşil)."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._mode = "dark"
        self._preset = core.PRESETS[0]
        self._name = ""
        self._line = ""
        self._unit = ""
        self._cycle_text = ""
        self.setFixedHeight(PREVIEW_HEIGHT)

    def set_preset(self, preset: core.Preset, name: str, line: str, unit: str, cycle_text: str) -> None:
        self._preset, self._name, self._line, self._unit, self._cycle_text = preset, name, line, unit, cycle_text
        self.update()

    def set_mode(self, mode: str) -> None:
        self._mode = mode
        self.update()

    def paintEvent(self, event) -> None:  # noqa: N802
        p = PALETTES.get(self._mode, PALETTES["dark"])
        pr = self._preset
        g = QPainter(self)
        g.setRenderHint(QPainter.RenderHint.Antialiasing)
        kart = QRectF(self.rect()).adjusted(0.5, 0.5, -0.5, -0.5)
        g.setPen(QPen(QColor(p["border"]), 1))
        g.setBrush(QColor(p["surface_alt"]))
        g.drawRoundedRect(kart, 14, 14)

        # Oran halkası: odak (vurgu) + mola (yeşil), aralarında küçük boşluk.
        cap = 86
        halka = QRectF(16, 16, cap, cap)
        kalinlik = 9
        g.setBrush(Qt.BrushStyle.NoBrush)
        g.setPen(QPen(QColor(p["border"]), kalinlik))
        g.drawEllipse(halka)
        toplam = pr.work + pr.rest
        bosluk = 6 if pr.rest else 0
        odak = 360 * pr.work / toplam if toplam else 360
        for renk, bas, aci in ((p["accent"], 90, odak), (p["success"], 90 - odak, 360 - odak)):
            if aci <= bosluk:
                continue
            kalem = QPen(QColor(renk), kalinlik)
            kalem.setCapStyle(Qt.PenCapStyle.RoundCap)
            g.setPen(kalem)
            g.drawArc(halka, round((bas - bosluk / 2) * 16), -round((aci - bosluk) * 16))
        g.setPen(QColor(p["text"]))
        g.setFont(_px_font(self.font(), 26, QFont.Weight.Bold, FONTS["display"]))
        g.drawText(QRectF(halka.x(), halka.y() + 18, cap, 32), Qt.AlignmentFlag.AlignCenter, str(pr.work))
        g.setPen(QColor(p["text_muted"]))
        g.setFont(_px_font(self.font(), 10.5, QFont.Weight.DemiBold))
        g.drawText(QRectF(halka.x(), halka.y() + 48, cap, 16), Qt.AlignmentFlag.AlignCenter, self._unit)

        # Sağ: ad, satır, döngü şeridi.
        x = halka.right() + 18
        genislik = self.width() - x - 16
        g.setPen(QColor(p["text"]))
        g.setFont(_px_font(self.font(), 16, QFont.Weight.Bold, FONTS["display"]))
        g.drawText(QRectF(x, 18, genislik, 24), Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                   QFontMetrics(g.font()).elidedText(self._name, Qt.TextElideMode.ElideRight, int(genislik)))
        g.setPen(QColor(p["text_muted"]))
        g.setFont(_px_font(self.font(), 12))
        g.drawText(QRectF(x, 44, genislik, 18), Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                   QFontMetrics(g.font()).elidedText(self._line, Qt.TextElideMode.ElideRight, int(genislik)))

        parcalar = _cycle(pr)
        sure = sum(dk for _, dk in parcalar)
        aralik = 3
        serit_y = 76
        kullanilir = genislik - aralik * (len(parcalar) - 1)
        px = x
        renkler = {"work": QColor(p["accent"]), "rest": QColor(p["success"]),
                   "long": QColor(p["success"])}
        for tur, dk in parcalar:
            w = max(4.0, kullanilir * dk / sure) if sure else 0
            renk = QColor(renkler[tur])
            if tur == "rest":
                renk.setAlphaF(0.55)
            g.setPen(Qt.PenStyle.NoPen)
            g.setBrush(renk)
            g.drawRoundedRect(QRectF(px, serit_y, w, 10), 3, 3)
            px += w + aralik
        g.setPen(QColor(p["text_muted"]))
        g.setFont(_px_font(self.font(), 11.5))
        g.drawText(QRectF(x, serit_y + 16, genislik, 18), Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                   self._cycle_text)
        g.end()


class ActiveRing(QWidget):
    """Çalışan sayfanın büyük halkası: kalan süre, evre ve ilerleme."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._mode = "dark"
        self._ratio = 1.0
        self._color = "#8B84FF"
        self._clock = "00:00"
        self._phase = ""
        self._paused = False
        self.setFixedHeight(ACTIVE_RING + 8)

    def set_state(self, ratio: float, color: str, clock: str, phase: str, paused: bool) -> None:
        self._ratio, self._color, self._clock, self._phase, self._paused = ratio, color, clock, phase, paused
        self.update()

    def set_mode(self, mode: str) -> None:
        self._mode = mode
        self.update()

    def paintEvent(self, event) -> None:  # noqa: N802
        p = PALETTES.get(self._mode, PALETTES["dark"])
        g = QPainter(self)
        g.setRenderHint(QPainter.RenderHint.Antialiasing)
        cap = ACTIVE_RING
        halka = QRectF((self.width() - cap) / 2, 4, cap, cap)
        kalinlik = 10
        g.setPen(QPen(QColor(p["surface_alt"]), kalinlik))
        g.drawEllipse(halka.adjusted(kalinlik / 2, kalinlik / 2, -kalinlik / 2, -kalinlik / 2))
        renk = QColor(p["text_muted"] if self._paused else self._color)
        if self._ratio > 0:
            kalem = QPen(renk, kalinlik)
            kalem.setCapStyle(Qt.PenCapStyle.RoundCap)
            g.setPen(kalem)
            g.drawArc(halka.adjusted(kalinlik / 2, kalinlik / 2, -kalinlik / 2, -kalinlik / 2),
                      90 * 16, -round(360 * 16 * self._ratio))
        g.setPen(QColor(p["text_muted"] if self._paused else p["text"]))
        g.setFont(_px_font(self.font(), 38, QFont.Weight.Bold, FONTS["display"]))
        g.drawText(QRectF(halka.x(), halka.y() + cap / 2 - 30, cap, 46), Qt.AlignmentFlag.AlignCenter, self._clock)
        g.setPen(QColor(renk))
        g.setFont(_px_font(self.font(), 11, QFont.Weight.Bold))
        g.drawText(QRectF(halka.x(), halka.y() + cap / 2 + 18, cap, 18), Qt.AlignmentFlag.AlignCenter, self._phase)
        g.end()


class TimerChip(QPushButton):
    """Alt şeritteki sayaç düğmesi."""

    def __init__(self, timer: core.StudyTimer, language: LanguageManager,
                 parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._timer = timer
        self._language = language
        self._mode = "dark"
        self._grow = 0.0
        self._growing = False
        self.setProperty("variant", "footer-icon")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedHeight(CHIP_HEIGHT)
        timer.changed.connect(self._on_changed)
        self._on_changed()

    # --- durum -------------------------------------------------------------

    def _font(self) -> QFont:
        f = QFont(self.font())
        f.setPixelSize(round(FONT_PX))
        f.setWeight(QFont.Weight.DemiBold)
        return f

    def _text(self) -> str:
        t = self._timer
        if t.phase == "ready":
            return self._language.t("timer.chip_ready")
        return core.format_clock(t.remaining)

    def _on_changed(self) -> None:
        t = self._timer
        if t.phase == "idle":
            self.setFixedWidth(18)
            self.setIcon(icon("clock", PALETTES[self._mode]["text_muted"], ICON))
            self.setIconSize(QSize(ICON, ICON))
        else:
            self.setIcon(icon("clock", "#00000000", 1))
            genis = QFontMetrics(self._font()).horizontalAdvance("0:00:00" if t.remaining >= 3600 else "00:00")
            genis = max(genis, QFontMetrics(self._font()).horizontalAdvance(self._language.t("timer.chip_ready")))
            self.setFixedWidth(RING + 6 + genis + 12)
        son = t.running and not t.paused and t.remaining <= core.FINAL_SECONDS
        if son != self._growing:
            self._growing = son
            motion.animate(self, "grow", self._grow, 1.0 if son else 0.0, self._set_grow, 420, "out")
        self.setToolTip(self._tooltip())
        self.update()

    def _set_grow(self, value: float) -> None:
        self._grow = value
        self.update()

    def _tooltip(self) -> str:
        t = self._timer
        if t.phase == "idle":
            return self._language.t("timer.tooltip_idle")
        if t.phase == "ready":
            return self._language.t("timer.tooltip_ready")
        anahtar = "timer.tooltip_break" if t.phase == "break" else "timer.tooltip_focus"
        return self._language.t(anahtar, time=core.format_clock(t.remaining))

    def set_mode(self, mode: str) -> None:
        self._mode = mode
        self._on_changed()

    # --- çizim -----------------------------------------------------------------

    def paintEvent(self, event) -> None:  # noqa: N802
        super().paintEvent(event)
        t = self._timer
        if t.phase == "idle":
            return
        p = PALETTES.get(self._mode, PALETTES["dark"])
        renk = QColor(_phase_color(t, p))
        g = QPainter(self)
        g.setRenderHint(QPainter.RenderHint.Antialiasing)
        # Hafifçe büyüme: ortadan ölçekleniyor, yazı rengi koyulaşıyor.
        olcek = 0.9 + GROW * self._grow
        g.translate(self.width() / 2, self.height() / 2)
        g.scale(olcek, olcek)
        g.translate(-self.width() / 2, -self.height() / 2)

        x = 6.0
        y = (self.height() - RING) / 2
        halka = QRectF(x, y, RING, RING)
        g.setPen(QPen(QColor(p["border"]), 2))
        g.drawEllipse(halka)
        if t.phase != "ready":
            kalem = QPen(renk, 2)
            kalem.setCapStyle(Qt.PenCapStyle.RoundCap)
            g.setPen(kalem)
            g.drawArc(halka, 90 * 16, -round(360 * 16 * (1 - t.ratio)))
        else:
            g.setBrush(renk)
            g.setPen(Qt.PenStyle.NoPen)
            g.drawEllipse(halka.adjusted(3, 3, -3, -3))

        yazi = QColor(p["text_muted"] if t.paused else p["text"])
        if self._grow > 0:
            yazi = QColor(renk) if self._grow > 0.5 else yazi
        g.setPen(yazi)
        g.setFont(self._font())
        g.drawText(QRectF(x + RING + 6, 0, self.width() - x - RING - 6, self.height()),
                   Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, self._text())
        g.end()


class TodayLine(QWidget):
    """Panelin altındaki "bugün" satırı: alev simgesi ve özet, ortalanmış."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setProperty("role", "bare")
        self._mode = "dark"
        self._active = False
        satir = QHBoxLayout(self)
        satir.setContentsMargins(0, 0, 0, 0)
        satir.setSpacing(6)
        satir.addStretch(1)
        self._icon = QLabel()
        self._icon.setFixedSize(14, 14)
        self._text = QLabel()
        self._text.setProperty("role", "timer-today")
        satir.addWidget(self._icon)
        satir.addWidget(self._text)
        satir.addStretch(1)

    def set_text(self, text: str, active: bool) -> None:
        self._text.setText(text)
        self._active = active
        self._paint_icon()

    def set_mode(self, mode: str) -> None:
        self._mode = mode
        self._paint_icon()

    def _paint_icon(self) -> None:
        p = PALETTES.get(self._mode, PALETTES["dark"])
        renk = p["warning"] if self._active else p["text_muted"]
        self._icon.setPixmap(icon("flame", renk, 14).pixmap(QSize(14, 14), self.devicePixelRatioF()))


class TimerPanel(Popover):
    """Düzen seçimi ve çalışan sayacın denetimleri."""

    # Panelin boyu değişti (sayfa geçişi); ana pencere yeniden yerleştirir.
    resized = Signal()

    def __init__(self, timer: core.StudyTimer, store, language: LanguageManager,
                 parent: QWidget | None = None) -> None:
        super().__init__(PANEL_WIDTH, parent)
        self._timer = timer
        self._store = store
        self._language = language
        self._mode = "dark"

        self._title = QLabel()
        self._title.setProperty("role", "popover-title")
        self._title.setContentsMargins(SPACING["md"], SPACING["sm"], SPACING["md"], SPACING["sm"])
        self.content.addWidget(self._title)
        cizgi = QFrame()
        cizgi.setProperty("role", "divider")
        cizgi.setFixedHeight(1)
        self.content.addWidget(cizgi)

        self._pages = QStackedWidget()
        self._pages.setProperty("role", "bare")
        self._pages.addWidget(self._build_setup())
        self._pages.addWidget(self._build_active())
        self.content.addWidget(self._pages)

        timer.changed.connect(self._refresh)
        self.retranslate()

    # --- kurulum sayfası ------------------------------------------------------

    def _build_setup(self) -> QWidget:
        sayfa = QWidget()
        sayfa.setProperty("role", "bare")
        duzen = QVBoxLayout(sayfa)
        duzen.setContentsMargins(SPACING["md"], SPACING["sm"], SPACING["md"], SPACING["md"])
        duzen.setSpacing(SPACING["sm"])

        self._hint = QLabel()
        self._hint.setProperty("role", "popover-text")
        self._hint.setWordWrap(True)
        duzen.addWidget(self._hint)

        # Seçili düzenin önizlemesi: oran halkası + döngü şeridi.
        self._preview = PresetPreview()
        duzen.addWidget(self._preview)
        self._about = QLabel()
        self._about.setProperty("role", "timer-about")
        self._about.setWordWrap(True)
        duzen.addWidget(self._about)

        # Düzen kartları: dördü ikili ızgarada, "kendi düzenin" tam genişlik.
        izgara = QGridLayout()
        izgara.setHorizontalSpacing(SPACING["xs"])
        izgara.setVerticalSpacing(SPACING["xs"])
        self._group = QButtonGroup(self)
        self._group.setExclusive(True)
        self._preset_buttons: dict[str, PresetTile] = {}
        kimlikler = [p.id for p in core.PRESETS] + ["custom"]
        for sira, kimlik in enumerate(kimlikler):
            kart = PresetTile(kimlik)
            kart.clicked.connect(lambda _=False, k=kimlik: self._choose(k))
            self._group.addButton(kart)
            self._preset_buttons[kimlik] = kart
            if kimlik == "custom":
                izgara.addWidget(kart, sira // 2, 0, 1, 2)
            else:
                izgara.addWidget(kart, sira // 2, sira % 2)
        duzen.addLayout(izgara)

        self._custom = QWidget()
        self._custom.setProperty("role", "bare")
        ozel = QHBoxLayout(self._custom)
        ozel.setContentsMargins(4, 0, 0, 0)
        ozel.setSpacing(SPACING["xs"])
        self._work_label = QLabel()
        self._work_label.setProperty("role", "popover-text")
        self._work_box = DropdownBox()
        for dakika in core.CUSTOM_WORK_CHOICES:
            self._work_box.addItem("", dakika)
        self._break_label = QLabel()
        self._break_label.setProperty("role", "popover-text")
        self._break_box = DropdownBox()
        for dakika in core.CUSTOM_BREAK_CHOICES:
            self._break_box.addItem("", dakika)
        for kutu in (self._work_box, self._break_box):
            kutu.setFixedWidth(100)
            kutu.currentIndexChanged.connect(self._custom_changed)
        ozel.addWidget(self._work_label)
        ozel.addWidget(self._work_box)
        ozel.addSpacing(SPACING["sm"])
        ozel.addWidget(self._break_label)
        ozel.addWidget(self._break_box)
        ozel.addStretch(1)
        duzen.addWidget(self._custom)

        duzen.addSpacing(2)
        self._start = QPushButton()
        self._start.setProperty("variant", "primary")
        self._start.setCursor(Qt.CursorShape.PointingHandCursor)
        self._start.setIconSize(QSize(15, 15))
        self._start.clicked.connect(self._on_start)
        duzen.addWidget(self._start)

        self._today_setup = TodayLine()
        duzen.addWidget(self._today_setup)
        return sayfa

    # --- çalışan sayfa --------------------------------------------------------

    def _build_active(self) -> QWidget:
        sayfa = QWidget()
        sayfa.setProperty("role", "bare")
        duzen = QVBoxLayout(sayfa)
        duzen.setContentsMargins(SPACING["md"], SPACING["sm"], SPACING["md"], SPACING["md"])
        duzen.setSpacing(SPACING["sm"])

        self._ring = ActiveRing()
        duzen.addWidget(self._ring)
        self._plan = QLabel()
        self._plan.setProperty("role", "timer-about")
        self._plan.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        duzen.addWidget(self._plan)

        duzen.addSpacing(2)
        satir = QHBoxLayout()
        satir.setSpacing(SPACING["xs"])
        self._main = QPushButton()
        self._main.setProperty("variant", "primary")
        self._main.setCursor(Qt.CursorShape.PointingHandCursor)
        self._main.setIconSize(QSize(15, 15))
        self._main.clicked.connect(self._on_main)
        self._skip = QPushButton()
        self._skip.setCursor(Qt.CursorShape.PointingHandCursor)
        self._skip.clicked.connect(self._timer.skip_break)
        self._stop = QPushButton()
        self._stop.setProperty("variant", "ghost")
        self._stop.setCursor(Qt.CursorShape.PointingHandCursor)
        self._stop.clicked.connect(self._timer.stop)
        satir.addWidget(self._main, 1)
        satir.addWidget(self._skip, 1)
        satir.addWidget(self._stop)
        duzen.addLayout(satir)

        self._today_active = TodayLine()
        duzen.addWidget(self._today_active)
        return sayfa

    # --- olaylar ----------------------------------------------------------------

    def _choose(self, kimlik: str) -> None:
        self._timer.choose(kimlik)
        self._render_setup()
        self._fit()

    def _custom_changed(self) -> None:
        if self._custom_loading:
            return
        self._timer.set_custom(self._work_box.currentData(), self._break_box.currentData())
        self._render_setup()

    def _on_start(self) -> None:
        self._timer.start()

    def _on_main(self) -> None:
        t = self._timer
        if t.phase == "ready":
            t.start()
        elif t.paused:
            t.resume()
        else:
            t.pause()

    # --- görünüm -----------------------------------------------------------------

    _custom_loading = False

    def _minutes(self, minutes: int) -> str:
        return self._language.t("timer.minutes", n=minutes)

    def _preset_line(self, p: core.Preset) -> str:
        if p.rest:
            return self._language.t("timer.line", work=p.work, rest=p.rest)
        return self._language.t("timer.line_norest", work=p.work)

    def _today_text(self) -> str:
        dakika, adet = self._store.focus_today()
        if not adet:
            return self._language.t("timer.today_none")
        saat, dk = divmod(dakika, 60)
        sure = (self._language.t("timer.hours_minutes", h=saat, m=dk) if saat
                else self._minutes(dk))
        return self._language.t("timer.today", time=sure, count=adet)

    def _tile_line(self, p: core.Preset) -> str:
        if p.rest:
            return self._language.t("timer.tile_line", work=p.work, rest=p.rest)
        return self._language.t("timer.tile_line_norest", work=p.work)

    def _duration(self, minutes: int) -> str:
        saat, dk = divmod(minutes, 60)
        if saat and dk:
            return self._language.t("timer.hours_minutes", h=saat, m=dk)
        if saat:
            return self._language.t("timer.hours", h=saat)
        return self._minutes(dk)

    def _render_setup(self) -> None:
        t = self._language.t
        secili = self._store.setting(core.PRESET_KEY, core.DEFAULT_PRESET)
        for kimlik, kart in self._preset_buttons.items():
            p = core.preset(self._store, kimlik)
            kart.set_texts(t(f"timer.preset.{kimlik}"), self._tile_line(p))
            kart.setChecked(kimlik == secili)
        self._custom.setVisible(secili == "custom")
        ozel = core.preset(self._store, "custom")
        self._custom_loading = True
        self._work_box.setCurrentIndex(max(0, self._work_box.findData(ozel.work)))
        self._break_box.setCurrentIndex(max(0, self._break_box.findData(ozel.rest)))
        self._custom_loading = False
        sec = core.preset(self._store, secili)
        toplam = sum(dk for _, dk in _cycle(sec))
        self._preview.set_preset(sec, t(f"timer.preset.{secili}"), self._preset_line(sec), t("timer.focus_unit"),
                                 t("timer.cycle", rounds=CYCLE_ROUNDS, time=self._duration(toplam)))
        self._about.setText(t(f"timer.about.{secili}"))
        self._start.setText(" " + t("timer.start_with", minutes=sec.work))
        self._today_setup.set_text(self._today_text(), self._store.focus_today()[1] > 0)

    def _refresh(self) -> None:
        tm = self._timer
        aktif = tm.phase != "idle"
        sayfa = 1 if aktif else 0
        if self._pages.currentIndex() != sayfa:
            self._pages.setCurrentIndex(sayfa)
            if sayfa == 0:
                self._render_setup()
            self._fit()
        if not aktif:
            return
        t = self._language.t
        p = PALETTES.get(self._mode, PALETTES["dark"])
        if tm.phase == "ready":
            etiket = t("timer.phase_ready")
        elif tm.phase == "break":
            etiket = t("timer.phase_long_break" if tm.is_long_break else "timer.phase_break")
        else:
            etiket = t("timer.phase_focus", round=tm.round)
        if tm.paused:
            etiket = f"{etiket} · {t('timer.paused')}"
        self._ring.set_state(
            (1 - tm.ratio) if tm.running else 1.0, _phase_color(tm, p),
            core.format_clock(tm.remaining) if tm.running else "00:00",
            self._language.t_upper("timer.phase_wrap", text=etiket), tm.paused)
        self._plan.setText(f"{t(f'timer.preset.{tm.preset.id}')} · {self._preset_line(tm.preset)}")
        ters = p["text_inverse"]
        if tm.phase == "ready":
            self._main.setText(" " + t("timer.next"))
            self._main.setIcon(icon("play", ters, 15))
        elif tm.paused:
            self._main.setText(" " + t("timer.resume"))
            self._main.setIcon(icon("play", ters, 15))
        else:
            self._main.setText(" " + t("timer.pause"))
            self._main.setIcon(icon("pause", ters, 15))
        self._skip.setVisible(tm.phase == "break")
        self._skip.setText(t("timer.skip"))
        self._stop.setText(t("timer.stop"))
        self._today_active.set_text(self._today_text(), self._store.focus_today()[1] > 0)

    def _fit(self) -> None:
        sayfa = self._pages.currentWidget()
        sayfa.adjustSize()
        self._pages.setFixedHeight(sayfa.sizeHint().height())
        self.fit_height(self._title.sizeHint().height() + 1 + sayfa.sizeHint().height())

    def show_above(self, anchor: QWidget) -> None:
        self._render_setup()
        self._refresh()
        self._fit()
        super().show_above(anchor)

    def set_mode(self, mode: str) -> None:
        self._mode = mode
        super().set_mode(mode)
        p = PALETTES.get(mode, PALETTES["dark"])
        for kutu in (self._work_box, self._break_box):
            kutu.set_arrow_color(p["text_muted"])
        for kart in self._preset_buttons.values():
            kart.set_mode(mode)
        for parca in (self._preview, self._ring, self._today_setup, self._today_active):
            parca.set_mode(mode)
        self._start.setIcon(icon("play", p["text_inverse"], 15))
        self._refresh()

    def retranslate(self) -> None:
        t = self._language.t
        self._title.setText(t("timer.title"))
        self._hint.setText(t("timer.hint"))
        self._start.setText(t("timer.start"))
        self._work_label.setText(t("timer.work"))
        self._break_label.setText(t("timer.break"))
        for i, dakika in enumerate(core.CUSTOM_WORK_CHOICES):
            self._work_box.setItemText(i, self._minutes(dakika))
        for i, dakika in enumerate(core.CUSTOM_BREAK_CHOICES):
            self._break_box.setItemText(i, self._minutes(dakika) if dakika else t("timer.no_break"))
        self._render_setup()
        self._refresh()
