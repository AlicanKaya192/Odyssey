"""Tanıtım turu: ilk açılışta (ve bu güncellemeden sonra herkese bir kez)
soruluyor; "evet" denirse programın her parçası tek tek gösteriliyor.

Alican istedi (30 Eylül): tur isteğe bağlı, başladıktan sonra da her an
geçilebiliyor; maskot (sentor) turda rehber.

- **Soru** `TourPromptDialog` (`modal.py`, çıkış penceresiyle aynı dil): üstte
  el sallayan sentor sahnesi, "Hayır, teşekkürler" / "Turu başlat". Yeni
  kullanıcıya "hoş geldiniz", çalışmış olana "yenilendi" diye soruyor.
- **Tur** `TourOverlay`: ana pencerenin içinde bir katman (ayrı pencere değil,
  kısayol paneli gibi). Her şeyi karartıyor, gösterilen parçanın çevresinde
  yuvarlak bir delik açıyor ve yanına bir kart koyuyor: küçük madalyonda
  sentor, adım sayısı, başlık, açıklama, Geri / İleri, "Turu geç". Delik bir
  adımdan ötekine kayarak geçiyor. Oklar ve Enter ileri-geri, Esc turu
  bitiriyor. Arkadaki ekrana tıklanmıyor.
- **Adımlar** `steps_for(window)`: her adım gerekirse ekranı değiştiriyor
  (profil, rotalar, bir bölüm…) ve hedef parçaları veriyor. Hedefler ana
  pencerenin iç parçaları; biri adını değiştirirse tur o adımda hedefsiz
  (ortada kart) kalıyor, çökmüyor.
- Ayar `tour_seen`: boşsa soruluyor; "done" / "skipped" / "declined".
  Ayarlar › Öğrenme'den tur yeniden başlatılabiliyor.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Callable

from PySide6.QtCore import QPoint, QPointF, QRect, QRectF, Qt, QTimer, Signal
from PySide6.QtGui import QColor, QLinearGradient, QPainter, QPainterPath, QPen
from PySide6.QtWidgets import (
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ..core.language import LanguageManager
from ..resources.theme.tokens import PALETTES, SPACING
from ..widgets import centaur as C
from ..widgets import motion
from . import modal
from .farewell_scene import FarewellScene
from .intro import STYLE

SEEN_KEY = "tour_seen"
CARD_WIDTH = 380
HOLE_PAD = 8
HOLE_RADIUS = 14
DIM_ALPHA = 165
MASCOT = 64


def should_ask(store) -> bool:
    return store.setting(SEEN_KEY, "") == ""


def mark(store, value: str) -> None:
    store.set_setting(SEEN_KEY, value)


def is_new_user(store) -> bool:
    """Hiç çalışmamış kişi mi (soru metni buna göre seçiliyor)."""
    try:
        return store.last_study_day() is None
    except Exception:  # noqa: BLE001
        return True


# --- soru penceresi -------------------------------------------------------------


class TourPromptDialog(QDialog):
    """"Programı tanıtan kısa bir tur ister misiniz?" kutusu."""

    def __init__(self, language: LanguageManager, new_user: bool, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        modal.prepare(self)
        t = language.t
        layout = QVBoxLayout(self)
        layout.setContentsMargins(SPACING["lg"], SPACING["lg"], SPACING["lg"], SPACING["lg"])
        layout.setSpacing(SPACING["sm"])

        self.scene = FarewellScene()
        self.scene.setFixedHeight(170)
        layout.addWidget(self.scene)
        layout.addSpacing(SPACING["sm"])

        anahtar = "tour.prompt_new" if new_user else "tour.prompt_back"
        baslik = QLabel(t(f"{anahtar}_title"))
        baslik.setProperty("role", "modal-page-title")
        baslik.setWordWrap(True)
        layout.addWidget(baslik)
        metin = QLabel(t(f"{anahtar}_text"))
        metin.setProperty("role", "muted")
        metin.setWordWrap(True)
        layout.addWidget(metin)

        layout.addSpacing(SPACING["sm"])
        dugmeler = QHBoxLayout()
        dugmeler.setSpacing(SPACING["sm"])
        dugmeler.addStretch(1)
        hayir = QPushButton(t("tour.prompt_no"))
        hayir.setCursor(Qt.CursorShape.PointingHandCursor)
        hayir.clicked.connect(self.reject)
        dugmeler.addWidget(hayir)
        evet = QPushButton(t("tour.prompt_yes"))
        evet.setProperty("variant", "primary")
        evet.setCursor(Qt.CursorShape.PointingHandCursor)
        evet.clicked.connect(self.accept)
        dugmeler.addWidget(evet)
        layout.addLayout(dugmeler)

        evet.setDefault(True)
        evet.setFocus()
        self.setWindowTitle(t("tour.prompt_new_title"))
        self.setFixedWidth(500)
        modal.freeze(self)


# --- maskot madalyonu ------------------------------------------------------------


class MascotBadge(QWidget):
    """Kartın köşesindeki yuvarlak madalyon: morda el sallayan sentor."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setFixedSize(MASCOT, MASCOT)
        self._mode = "dark"
        # Çıkış sahnesinin duruş hesabı (el sallama, eşeleme) yeniden
        # kullanılıyor; sahnenin kendisi gösterilmiyor.
        self._poser = FarewellScene()
        self._t0 = time.monotonic()
        self._timer = QTimer(self)
        self._timer.setInterval(40)
        self._timer.timeout.connect(self.update)

    def showEvent(self, event) -> None:  # noqa: N802
        super().showEvent(event)
        if motion.enabled():
            self._timer.start()

    def hideEvent(self, event) -> None:  # noqa: N802
        super().hideEvent(event)
        self._timer.stop()

    def set_mode(self, mode: str) -> None:
        self._mode = mode
        self.update()

    def paintEvent(self, event) -> None:  # noqa: N802
        p = PALETTES.get(self._mode, PALETTES["dark"])
        g = QPainter(self)
        g.setRenderHint(QPainter.RenderHint.Antialiasing)
        r = QRectF(1, 1, MASCOT - 2, MASCOT - 2)
        degrade = QLinearGradient(r.topLeft(), r.bottomRight())
        degrade.setColorAt(0, QColor("#B9B3FF"))
        degrade.setColorAt(1, QColor(p["accent"]))
        yol = QPainterPath()
        yol.addEllipse(r)
        g.fillPath(yol, degrade)
        g.setClipPath(yol)
        # Zemin çizgisi
        zemin = MASCOT * 0.86
        g.fillRect(QRectF(0, zemin, MASCOT, MASCOT - zemin), QColor(0, 0, 0, 40))
        t = time.monotonic() - self._t0 if motion.enabled() else 0.6
        poz = self._poser.pose(t)
        s = (zemin - 4) / (C.GROUND - 118.0)
        g.translate(MASCOT / 2 - 318 * s, zemin - C.GROUND * s)
        g.scale(s, s)
        C.draw_centaur(g, poz, STYLE, line=1.6)
        g.end()


# --- tur kartı ve katman ----------------------------------------------------------


@dataclass
class Step:
    title: str                                  # çeviri anahtarı
    text: str                                   # çeviri anahtarı
    targets: Callable[[], list] = field(default=lambda: [])
    prepare: Callable[[], None] | None = None   # ekranı değiştir
    wait: int = 0                               # hazırlıktan sonra bekleme (ms)


class TourCard(QFrame):
    """Açıklama kartı."""

    next_clicked = Signal()
    back_clicked = Signal()
    skip_clicked = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setProperty("role", "tour-card")
        self.setFixedWidth(CARD_WIDTH)
        duzen = QVBoxLayout(self)
        duzen.setContentsMargins(20, 18, 20, 16)
        duzen.setSpacing(8)

        ust = QHBoxLayout()
        ust.setSpacing(12)
        self.mascot = MascotBadge()
        ust.addWidget(self.mascot, 0, Qt.AlignmentFlag.AlignVCenter)
        metinler = QVBoxLayout()
        metinler.setSpacing(2)
        self.counter = QLabel()
        self.counter.setProperty("role", "tour-step")
        metinler.addWidget(self.counter)
        self.title = QLabel()
        self.title.setProperty("role", "tour-title")
        self.title.setWordWrap(True)
        metinler.addWidget(self.title)
        ust.addLayout(metinler, 1)
        duzen.addLayout(ust)

        self.text = QLabel()
        self.text.setProperty("role", "tour-text")
        self.text.setWordWrap(True)
        self.text.setTextFormat(Qt.TextFormat.RichText)
        duzen.addWidget(self.text)

        duzen.addSpacing(4)
        alt = QHBoxLayout()
        alt.setSpacing(8)
        self.skip = QPushButton()
        self.skip.setProperty("variant", "ghost")
        self.skip.setCursor(Qt.CursorShape.PointingHandCursor)
        self.skip.clicked.connect(self.skip_clicked)
        alt.addWidget(self.skip)
        alt.addStretch(1)
        self.back = QPushButton()
        self.back.setCursor(Qt.CursorShape.PointingHandCursor)
        self.back.clicked.connect(self.back_clicked)
        alt.addWidget(self.back)
        self.next = QPushButton()
        self.next.setProperty("variant", "primary")
        self.next.setCursor(Qt.CursorShape.PointingHandCursor)
        self.next.clicked.connect(self.next_clicked)
        alt.addWidget(self.next)
        duzen.addLayout(alt)
        for dugme in (self.skip, self.back, self.next):
            dugme.setFocusPolicy(Qt.FocusPolicy.NoFocus)


class TourOverlay(QWidget):
    """Karartma, delik ve kart. `finished(tamamlandı_mı)` tur bitince."""

    finished = Signal(bool)

    def __init__(self, language: LanguageManager, steps: list[Step], mode: str,
                 parent: QWidget) -> None:
        super().__init__(parent)
        self._language = language
        self._steps = steps
        self._mode = mode
        self._index = -1
        self._hole = QRectF()           # şu an çizilen delik (canlandırılıyor)
        self._fade = 0.0
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, True)
        self.card = TourCard(self)
        self.card.mascot.set_mode(mode)
        self.card.next_clicked.connect(self.next)
        self.card.back_clicked.connect(self.back)
        self.card.skip_clicked.connect(lambda: self.finish(False))
        self.card.hide()
        self.hide()

    # --- akış ----------------------------------------------------------------------

    def start(self) -> None:
        self.setGeometry(self.parentWidget().rect())
        self.show()
        self.raise_()
        self.setFocus()
        motion.animate(self, "fade", 0.0, 1.0, self._set_fade, "base", "out")
        self._go(0)

    def next(self) -> None:
        if self._index + 1 >= len(self._steps):
            self.finish(True)
        else:
            self._go(self._index + 1)

    def back(self) -> None:
        if self._index > 0:
            self._go(self._index - 1)

    def finish(self, completed: bool) -> None:
        if not self.isVisible():
            return
        self.card.hide()
        self.hide()
        self.finished.emit(completed)
        self.deleteLater()

    def _go(self, index: int) -> None:
        self._index = index
        adim = self._steps[index]
        self.card.hide()
        if adim.prepare is not None:
            try:
                adim.prepare()
            except Exception:  # noqa: BLE001 — tur bir ekranı açamazsa kart yine çıksın
                pass
        QTimer.singleShot(max(0, adim.wait), lambda i=index: self._arrive(i))

    def _arrive(self, index: int) -> None:
        if index != self._index or not self.isVisible():
            return
        self.setGeometry(self.parentWidget().rect())
        self.raise_()
        hedef = self._target_rect(self._steps[index])
        eski = QRectF(self._hole)
        if eski.isNull():
            eski = QRectF(hedef.center(), hedef.center()) if not hedef.isNull() else QRectF()
        motion.animate(self, "hole", 0.0, 1.0,
                       lambda k, a=eski, b=hedef: self._set_hole(a, b, k), "base", "out")
        self._render_card(index, hedef)

    # --- hedef ve kart ----------------------------------------------------------------

    def _target_rect(self, step: Step) -> QRectF:
        try:
            parcalar = [w for w in step.targets() if w is not None and w.isVisible()]
        except Exception:  # noqa: BLE001
            parcalar = []
        birlesik = QRect()
        for w in parcalar:
            sol_ust = w.mapTo(self.parentWidget(), QPoint(0, 0))
            birlesik = birlesik.united(QRect(sol_ust, w.size()))
        if birlesik.isNull():
            return QRectF()
        return QRectF(birlesik).adjusted(-HOLE_PAD, -HOLE_PAD, HOLE_PAD, HOLE_PAD).intersected(
            QRectF(self.rect()).adjusted(4, 4, -4, -4))

    def _render_card(self, index: int, hole: QRectF) -> None:
        t = self._language.t
        adim = self._steps[index]
        kart = self.card
        kart.counter.setText(t("tour.step", n=index + 1, total=len(self._steps)))
        kart.title.setText(t(adim.title))
        kart.text.setText(t(adim.text))
        kart.skip.setText(t("tour.skip"))
        kart.back.setText(t("tour.back"))
        kart.back.setVisible(index > 0)
        son = index == len(self._steps) - 1
        kart.next.setText(t("tour.finish") if son else t("tour.next") + "  →")
        # Sarılan etiketlerde `adjustSize` eski genişliğe göre ölçüp kartta
        # boşluk bırakıyordu; boy kartın sabit genişliğinden hesaplanıyor.
        kart.layout().invalidate()
        boy = kart.layout().heightForWidth(CARD_WIDTH)
        # +8: son satırın alt çıkıntıları (g, y, ş) kesiliyordu.
        kart.setFixedHeight((boy if boy > 0 else kart.sizeHint().height()) + 8)
        kart.move(self._card_position(hole, CARD_WIDTH, kart.height()))
        kart.show()
        kart.raise_()

    def _card_position(self, hole: QRectF, w: int, h: int) -> QPoint:
        W, H = self.width(), self.height()
        gap, kenar = 18, 16
        if hole.isNull():
            return QPoint(int((W - w) / 2), int((H - h) / 2))
        orta_y = int(min(max(hole.center().y() - h / 2, kenar), H - h - kenar))
        orta_x = int(min(max(hole.center().x() - w / 2, kenar), W - w - kenar))
        if hole.right() + gap + w <= W - kenar:
            return QPoint(int(hole.right() + gap), orta_y)
        if hole.left() - gap - w >= kenar:
            return QPoint(int(hole.left() - gap - w), orta_y)
        if hole.bottom() + gap + h <= H - kenar:
            return QPoint(orta_x, int(hole.bottom() + gap))
        if hole.top() - gap - h >= kenar:
            return QPoint(orta_x, int(hole.top() - gap - h))
        return QPoint(W - w - kenar, H - h - kenar)

    # --- çizim ------------------------------------------------------------------------

    def _set_fade(self, v: float) -> None:
        self._fade = v
        self.update()

    def _set_hole(self, a: QRectF, b: QRectF, k: float) -> None:
        if b.isNull():
            merkez = QPointF(self.width() / 2, self.height() / 2)
            b = QRectF(merkez, merkez)
        if a.isNull():
            a = QRectF(b.center(), b.center())
        self._hole = QRectF(
            a.left() + (b.left() - a.left()) * k,
            a.top() + (b.top() - a.top()) * k,
            a.width() + (b.width() - a.width()) * k,
            a.height() + (b.height() - a.height()) * k,
        )
        self.update()

    def paintEvent(self, event) -> None:  # noqa: N802
        p = PALETTES.get(self._mode, PALETTES["dark"])
        g = QPainter(self)
        g.setRenderHint(QPainter.RenderHint.Antialiasing)
        tum = QPainterPath()
        tum.addRect(QRectF(self.rect()))
        if self._hole.width() > 2 and self._hole.height() > 2:
            delik = QPainterPath()
            delik.addRoundedRect(self._hole, HOLE_RADIUS, HOLE_RADIUS)
            tum = tum.subtracted(delik)
        g.fillPath(tum, QColor(0, 0, 0, int(DIM_ALPHA * self._fade)))
        if self._hole.width() > 2 and self._hole.height() > 2:
            halka = QColor(p["accent"])
            for genis, alfa in ((8, 40), (4, 90), (2, 255)):
                halka.setAlpha(int(alfa * self._fade))
                g.setPen(QPen(halka, genis))
                g.setBrush(Qt.BrushStyle.NoBrush)
                g.drawRoundedRect(self._hole, HOLE_RADIUS, HOLE_RADIUS)
        g.end()

    # --- olaylar -----------------------------------------------------------------------

    def mousePressEvent(self, event) -> None:  # noqa: N802
        # Arkadaki ekrana tıklanmıyor; tur kartın düğmeleriyle ilerliyor.
        event.accept()

    def keyPressEvent(self, event) -> None:  # noqa: N802
        tus = event.key()
        if tus in (Qt.Key.Key_Right, Qt.Key.Key_Return, Qt.Key.Key_Enter, Qt.Key.Key_Space):
            self.next()
        elif tus == Qt.Key.Key_Left:
            self.back()
        elif tus == Qt.Key.Key_Escape:
            self.finish(False)
        else:
            super().keyPressEvent(event)

    def reposition(self) -> None:
        if not self.isVisible() or self._index < 0:
            return
        self.setGeometry(self.parentWidget().rect())
        hedef = self._target_rect(self._steps[self._index])
        self._hole = hedef
        self.card.move(self._card_position(hedef, self.card.width(), self.card.height()))
        self.update()


# --- adımlar ---------------------------------------------------------------------------

PY_CHAPTER = "00-python-temelleri"
# Alıştırma ekranını göstermek için alıştırması olan ilk bölüm. Kilitliyse de
# tur onu yalnızca gösteriyor, hiçbir şey kaydetmiyor.
EXERCISE_SECTION = "00-baslangic"


def steps_for(win) -> list[Step]:  # noqa: C901 — adım listesi uzun ama düz
    """Ana pencere için tur adımları. `win` bir `MainWindow`."""
    # Ana pencerenin iç parçalarına bilerek erişiliyor: tur onları gösteriyor.
    # ruff: noqa: SLF001

    def nav(key: str):
        return lambda: win._tour_navigate(key)

    def section(section_id: str, pane: str):
        return lambda: win._tour_open_section(PY_CHAPTER, section_id, pane)

    rail = win._rail
    journey = win._journey
    profile = win._profile
    footer = win._footer
    topic = win._topic

    def ilk_bolum() -> str:
        bolumler = win._catalog.chapter(PY_CHAPTER).sections
        return bolumler[0].id if bolumler else ""

    def hero():
        return [journey.tracks._hero] if hasattr(journey, "tracks") else []

    def kartlar():
        return list(getattr(getattr(journey, "tracks", None), "_cards", []))[:8]

    return [
        Step("tour.s_welcome_title", "tour.s_welcome_text", prepare=nav("journey"), wait=350),
        Step("tour.s_rail_title", "tour.s_rail_text", targets=lambda: [rail]),
        Step("tour.s_hero_title", "tour.s_hero_text", targets=hero),
        Step("tour.s_tracks_title", "tour.s_tracks_text", targets=kartlar),
        Step("tour.s_section_title", "tour.s_section_text",
             prepare=section(ilk_bolum(), "lesson"), wait=900,
             targets=lambda: [topic._segments]),
        Step("tour.s_lesson_title", "tour.s_lesson_text", targets=lambda: [topic._stack]),
        Step("tour.s_note_title", "tour.s_note_text", targets=lambda: [topic._note_button]),
        Step("tour.s_quiz_title", "tour.s_quiz_text", prepare=section(ilk_bolum(), "quiz"), wait=500,
             targets=lambda: [topic._stack]),
        Step("tour.s_editor_title", "tour.s_editor_text",
             prepare=section(EXERCISE_SECTION, "exercise"), wait=1000,
             targets=lambda: [topic._exercise._editor_card, topic._exercise._run_button]),
        Step("tour.s_terminal_title", "tour.s_terminal_text", targets=lambda: [topic._exercise._terminal]),
        Step("tour.s_brief_title", "tour.s_brief_text",
             targets=lambda: [topic._exercise._splitter.widget(0)]),
        Step("tour.s_profile_title", "tour.s_profile_text", prepare=nav("profile"), wait=600,
             targets=lambda: [profile._identity_card]),
        Step("tour.s_badges_title", "tour.s_badges_text", targets=lambda: [profile._badges_card]),
        Step("tour.s_activity_title", "tour.s_activity_text", targets=lambda: [profile._activity_card]),
        Step("tour.s_roadmap_title", "tour.s_roadmap_text", prepare=nav("roadmap"), wait=700,
             targets=lambda: [win._roadmap]),
        Step("tour.s_notes_title", "tour.s_notes_text", prepare=nav("notes"), wait=700,
             targets=lambda: [win._notebook]),
        Step("tour.s_search_title", "tour.s_search_text", prepare=nav("journey"), wait=450,
             targets=lambda: [rail._buttons.get("search")]),
        Step("tour.s_timer_title", "tour.s_timer_text", targets=lambda: [footer.timer_chip]),
        Step("tour.s_shortcuts_title", "tour.s_shortcuts_text", targets=lambda: [footer.shortcut_button]),
        Step("tour.s_settings_title", "tour.s_settings_text", targets=lambda: [rail._buttons.get("settings")]),
        Step("tour.s_about_title", "tour.s_about_text",
             targets=lambda: [rail._buttons.get("releases"), rail._buttons.get("about")]),
        Step("tour.s_end_title", "tour.s_end_text", targets=hero),
    ]
