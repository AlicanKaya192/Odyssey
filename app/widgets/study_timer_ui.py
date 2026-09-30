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
    QButtonGroup,
    QFrame,
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
from ..resources.theme.tokens import PALETTES, SPACING
from . import motion
from .common import DropdownBox
from .popover import Popover
from .progress_bar import ProgressBar

PANEL_WIDTH = 360
CHIP_HEIGHT = 20
ICON = 14
RING = 11
FONT_PX = 11.5
# Son saniyelerde en fazla bu kadar büyüyor.
GROW = 0.16


def _phase_color(timer: core.StudyTimer, p: dict) -> str:
    return p["success"] if timer.phase == "break" else p["accent"]


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
        duzen.setSpacing(6)

        self._hint = QLabel()
        self._hint.setProperty("role", "popover-text")
        self._hint.setWordWrap(True)
        duzen.addWidget(self._hint)
        duzen.addSpacing(4)

        self._group = QButtonGroup(self)
        self._group.setExclusive(True)
        self._preset_buttons: dict[str, QPushButton] = {}
        for kimlik in [p.id for p in core.PRESETS] + ["custom"]:
            dugme = QPushButton()
            dugme.setProperty("variant", "timer-preset")
            dugme.setCheckable(True)
            dugme.setCursor(Qt.CursorShape.PointingHandCursor)
            dugme.clicked.connect(lambda _=False, k=kimlik: self._choose(k))
            self._group.addButton(dugme)
            self._preset_buttons[kimlik] = dugme
            duzen.addWidget(dugme)

        self._custom = QWidget()
        self._custom.setProperty("role", "bare")
        ozel = QHBoxLayout(self._custom)
        ozel.setContentsMargins(0, 2, 0, 0)
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
            kutu.setFixedWidth(92)
            kutu.currentIndexChanged.connect(self._custom_changed)
        ozel.addWidget(self._work_label)
        ozel.addWidget(self._work_box)
        ozel.addSpacing(SPACING["xs"])
        ozel.addWidget(self._break_label)
        ozel.addWidget(self._break_box)
        ozel.addStretch(1)
        duzen.addWidget(self._custom)

        self._about = QLabel()
        self._about.setProperty("role", "timer-about")
        self._about.setWordWrap(True)
        duzen.addWidget(self._about)

        duzen.addSpacing(4)
        self._start = QPushButton()
        self._start.setProperty("variant", "primary")
        self._start.setCursor(Qt.CursorShape.PointingHandCursor)
        self._start.clicked.connect(self._on_start)
        duzen.addWidget(self._start)

        self._today_setup = QLabel()
        self._today_setup.setProperty("role", "timer-today")
        self._today_setup.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        duzen.addWidget(self._today_setup)
        return sayfa

    # --- çalışan sayfa --------------------------------------------------------

    def _build_active(self) -> QWidget:
        sayfa = QWidget()
        sayfa.setProperty("role", "bare")
        duzen = QVBoxLayout(sayfa)
        duzen.setContentsMargins(SPACING["md"], SPACING["sm"], SPACING["md"], SPACING["md"])
        duzen.setSpacing(6)

        self._phase = QLabel()
        self._phase.setProperty("role", "timer-phase")
        self._phase.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        duzen.addWidget(self._phase)
        self._clock = QLabel()
        self._clock.setProperty("role", "timer-clock")
        self._clock.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        duzen.addWidget(self._clock)
        self._bar = ProgressBar()
        duzen.addWidget(self._bar)
        self._plan = QLabel()
        self._plan.setProperty("role", "timer-today")
        self._plan.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        duzen.addWidget(self._plan)

        duzen.addSpacing(4)
        satir = QHBoxLayout()
        satir.setSpacing(SPACING["xs"])
        self._main = QPushButton()
        self._main.setProperty("variant", "primary")
        self._main.setCursor(Qt.CursorShape.PointingHandCursor)
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

        self._today_active = QLabel()
        self._today_active.setProperty("role", "timer-today")
        self._today_active.setAlignment(Qt.AlignmentFlag.AlignHCenter)
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

    def _render_setup(self) -> None:
        t = self._language.t
        secili = self._store.setting(core.PRESET_KEY, core.DEFAULT_PRESET)
        for kimlik, dugme in self._preset_buttons.items():
            p = core.preset(self._store, kimlik)
            dugme.setText(f"{t(f'timer.preset.{kimlik}')}   ·   {self._preset_line(p)}")
            dugme.setChecked(kimlik == secili)
        self._custom.setVisible(secili == "custom")
        ozel = core.preset(self._store, "custom")
        self._custom_loading = True
        self._work_box.setCurrentIndex(max(0, self._work_box.findData(ozel.work)))
        self._break_box.setCurrentIndex(max(0, self._break_box.findData(ozel.rest)))
        self._custom_loading = False
        self._about.setText(t(f"timer.about.{secili}"))
        self._today_setup.setText(self._today_text())

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
        self._phase.setText(self._language.t_upper("timer.phase_wrap", text=etiket))
        self._clock.setText(core.format_clock(tm.remaining) if tm.running else "00:00")
        self._bar.set_color(_phase_color(tm, p))
        self._bar.set_percent(100 * tm.ratio if tm.running else 100, animate=False)
        self._plan.setText(f"{t(f'timer.preset.{tm.preset.id}')} · {self._preset_line(tm.preset)}")
        if tm.phase == "ready":
            self._main.setText(t("timer.next"))
        else:
            self._main.setText(t("timer.resume") if tm.paused else t("timer.pause"))
        self._skip.setVisible(tm.phase == "break")
        self._skip.setText(t("timer.skip"))
        self._stop.setText(t("timer.stop"))
        self._today_active.setText(self._today_text())

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
        muted = PALETTES.get(mode, PALETTES["dark"])["text_muted"]
        for kutu in (self._work_box, self._break_box):
            kutu.set_arrow_color(muted)
        self._bar.set_mode(mode)
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
