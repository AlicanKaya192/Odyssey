"""Alıştırma tekrarı sayfası (`core/exercise_practice.py`).

Ayrı bir pencere değil, ana pencerenin içerik alanını kaplayan bir katman
(tur ve kısayol paneli gibi): kipli pencere ana pencereyi kilitliyordu,
başlık çubuğundan taşınamıyordu ve kenarlarından arkadaki ekran
görünüyordu (Alican 13 Kasım). `QDialog` olarak kaldı (`done`, `finished`,
Esc), ama `Qt.Widget` bayrağıyla bir çocuk bileşen.

İki sayfa: alıştırmalar (içinde ayrı bir alıştırma ekranı) ve özet. Alıştırma
ekranına gerçek depo yerine `PracticeStore` veriliyor: kişinin kayıtlı
çözümü ve deneme geçmişi değişmiyor, editör başlangıç koduyla açılıyor.

Her çözümde çalışma günü, etkinlik ve oturum sonucu o an yazılıyor (Alican:
yarıda kapanırsa çözülenler saklansın); Esc onaysız kapatıyor. Kod çalışırken
"Atla" ve "Sonraki" kapalı.
"""

from __future__ import annotations

import html
import random
from datetime import date

from PySide6.QtCore import QEvent, Qt, Signal
from PySide6.QtWidgets import (
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from ..core import exercise_practice
from ..core.language import LanguageManager
from ..resources.icons import pixmap
from ..resources.theme.tokens import PALETTES, SPACING
from .exercise_view import ExerciseView

SUMMARY_WIDTH = 640


class ExercisePracticeDialog(QDialog):
    """Bir modülün bitmiş bölümlerinden beş alıştırma."""

    # Özetteki "Bölüme git": (modül, bölüm); pencere kapanıyor.
    section_requested = Signal(str, str)

    def __init__(self, language: LanguageManager, store, chapter, mode: str = "light",
                 parent: QWidget | None = None, today: date | None = None,
                 rng: random.Random | None = None) -> None:
        super().__init__(parent)
        self._language = language
        self._store = store
        self._chapter = chapter
        self._mode = mode
        self._today = today
        self._items = exercise_practice.build(exercise_practice.done_sections(chapter, store), rng)
        self._index = 0
        # Alıştırma sırasına göre: "solved", "helped" ya da yok (çözülmedi).
        self._results: dict[int, str] = {}
        t = language.t

        # Çocuk bileşen: sahibinin (ana pencerenin içerik alanı) tamamını kaplıyor.
        self.setWindowFlags(Qt.WindowType.Widget)
        self.setObjectName("exercisePractice")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        p = PALETTES.get(mode, PALETTES["light"])
        self.setStyleSheet(f"QDialog#exercisePractice {{ background: {p['bg']}; }}")
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        if parent is not None:
            self.setGeometry(parent.rect())
            parent.installEventFilter(self)

        kok = QVBoxLayout(self)
        kok.setContentsMargins(SPACING["lg"], SPACING["lg"], SPACING["lg"], SPACING["lg"])
        self._stack = QStackedWidget()
        self._stack.setProperty("role", "bare")
        kok.addWidget(self._stack)

        # --- alıştırmalar --------------------------------------------------
        sayfa = QWidget()
        sayfa.setProperty("role", "bare")
        self._exercise_page = sayfa
        s = QVBoxLayout(sayfa)
        s.setContentsMargins(0, 0, 0, 0)
        s.setSpacing(SPACING["sm"])
        ust = QHBoxLayout()
        ust.setSpacing(SPACING["sm"])
        basliklar = QVBoxLayout()
        basliklar.setSpacing(2)
        baslik = QLabel(t("xpractice.title"))
        baslik.setProperty("role", "modal-title")
        basliklar.addWidget(baslik)
        self._progress = QLabel()
        self._progress.setProperty("role", "muted")
        basliklar.addWidget(self._progress)
        ust.addLayout(basliklar, 1)
        self._finish_button = self._button(t("xpractice.finish"), "ghost", self._finish)
        ust.addWidget(self._finish_button, 0, Qt.AlignmentFlag.AlignVCenter)
        self._skip_button = self._button(t("xpractice.skip"), "ghost", self._next)
        ust.addWidget(self._skip_button, 0, Qt.AlignmentFlag.AlignVCenter)
        self._next_button = self._button(t("xpractice.next"), "primary", self._next)
        ust.addWidget(self._next_button, 0, Qt.AlignmentFlag.AlignVCenter)
        s.addLayout(ust)

        self._practice_store = exercise_practice.PracticeStore(store)
        self._view = ExerciseView(language, self._practice_store)
        self._view.set_practice(True)
        self._view.set_mode(mode)
        self._view.solved.connect(self._on_solved)
        self._view.running_changed.connect(self._on_running)
        s.addWidget(self._view, 1)
        self._stack.addWidget(sayfa)

        # --- özet ----------------------------------------------------------
        ozet = QWidget()
        ozet.setProperty("role", "bare")
        self._summary_page = ozet
        dis = QVBoxLayout(ozet)
        dis.setContentsMargins(0, 0, 0, 0)
        dis.addStretch(1)
        orta = QHBoxLayout()
        orta.addStretch(1)
        kart = QFrame()
        kart.setObjectName("practiceSummary")
        kart.setFixedWidth(SUMMARY_WIDTH)
        kart.setStyleSheet(
            f"QFrame#practiceSummary {{ background: {p['surface']}; border: 1px solid {p['border']};"
            " border-radius: 16px; }"
            "QFrame#practiceSummary QLabel { background: transparent; border: none; }")
        self._summary_card = kart
        orta.addWidget(kart)
        orta.addStretch(1)
        dis.addLayout(orta)
        dis.addStretch(1)
        r = QVBoxLayout(kart)
        r.setContentsMargins(SPACING["xl"], SPACING["xl"], SPACING["xl"], SPACING["xl"])
        r.setSpacing(SPACING["sm"])
        self._result_title = QLabel()
        self._result_title.setProperty("role", "modal-title")
        self._result_title.setWordWrap(True)
        r.addWidget(self._result_title)
        self._result_text = QLabel()
        self._result_text.setProperty("role", "muted")
        self._result_text.setWordWrap(True)
        r.addWidget(self._result_text)
        r.addSpacing(SPACING["sm"])
        self._rows = QVBoxLayout()
        self._rows.setSpacing(SPACING["xs"])
        r.addLayout(self._rows)
        r.addSpacing(SPACING["md"])
        alt = QHBoxLayout()
        alt.addStretch(1)
        self._done_button = self._button(t("review.done"), "primary", self.accept)
        alt.addWidget(self._done_button)
        r.addLayout(alt)
        self._stack.addWidget(ozet)

        if self._items:
            self._show_current()
        else:
            self._finish()

    # --- yardımcılar ---------------------------------------------------------

    def _button(self, text: str, variant: str, slot) -> QPushButton:
        dugme = QPushButton(text)
        dugme.setProperty("variant", variant)
        dugme.setCursor(Qt.CursorShape.PointingHandCursor)
        dugme.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        dugme.clicked.connect(slot)
        return dugme

    def eventFilter(self, obj, event) -> bool:  # noqa: N802
        # Sahibi büyüyüp küçülünce sayfa da onu kaplamaya devam ediyor.
        if obj is self.parentWidget() and event.type() == QEvent.Type.Resize:
            self.setGeometry(obj.rect())
        return False

    @property
    def solved_count(self) -> int:
        return len(self._results)

    @property
    def view(self) -> ExerciseView:
        return self._view

    # --- akış ----------------------------------------------------------------

    def _show_current(self) -> None:
        section, exercise = self._items[self._index]
        self._progress.setText(self._language.t(
            "xpractice.progress", index=self._index + 1, total=len(self._items),
            section=self._language.pick(section.title)))
        son = self._index == len(self._items) - 1
        self._next_button.setText(self._language.t("xpractice.finish" if son else "xpractice.next"))
        self._skip_button.setVisible(not son)
        self._view.set_advance_label(None)
        self._view.show_exercise(exercise, section.chapter_id, section.id)
        self._sync_buttons()

    def _sync_buttons(self) -> None:
        calisiyor = self._view.is_running
        for dugme in (self._skip_button, self._next_button, self._finish_button):
            dugme.setEnabled(not calisiyor)

    def _on_running(self, _running: bool) -> None:
        self._sync_buttons()

    def _on_solved(self, exercise_id: str) -> None:
        section, exercise = self._items[self._index]
        if exercise.id != exercise_id or self._index in self._results:
            return
        self._results[self._index] = "helped" if self._view.helped else "solved"
        # Çözülen o an işleniyor: pencere yarıda kapanırsa da sayılsın.
        self._store.mark_study_day()
        self._store.record_activity("exercise_practice", section.chapter_id, section.id)
        self._save()

    def _save(self) -> None:
        yardimli = sum(1 for durum in self._results.values() if durum == "helped")
        exercise_practice.save(self._store, self._chapter.id, len(self._results), yardimli,
                               len(self._items), self._today)

    def _next(self) -> None:
        if self._view.is_running:
            return
        if self._index >= len(self._items) - 1:
            self._finish()
            return
        self._index += 1
        self._show_current()

    def _finish(self) -> None:
        if self._view.is_running:
            return
        t = self._language.t
        self._view.release_workers(self.window())
        cozulen = len(self._results)
        yardimli = sum(1 for durum in self._results.values() if durum == "helped")
        self._result_title.setText(t("xpractice.result_title") if cozulen else t("xpractice.title"))
        metin = (t("xpractice.result_text", solved=cozulen, total=len(self._items))
                 if cozulen else t("xpractice.result_none"))
        if yardimli:
            metin += " " + t("xpractice.result_helped", helped=yardimli)
        self._result_text.setText(metin)
        self._build_rows()
        self._stack.setCurrentWidget(self._summary_page)
        self.setFocus()

    def _build_rows(self) -> None:
        t = self._language.t
        p = PALETTES.get(self._mode, PALETTES["light"])
        for sira, (section, exercise) in enumerate(self._items):
            durum = self._results.get(sira)
            satir = QHBoxLayout()
            satir.setSpacing(SPACING["sm"])
            simge = QLabel()
            renk = {"solved": p["success"], "helped": p["warning"]}.get(durum, p["text_muted"])
            simge.setPixmap(pixmap("check-circle" if durum else "x", renk, 16))
            satir.addWidget(simge, 0, Qt.AlignmentFlag.AlignTop)
            yazi = QLabel(
                f"<b>{html.escape(self._language.pick(exercise.title))}</b>"
                f" · {html.escape(self._language.pick(section.title))}<br>"
                f"<span style='color:{p['text_muted']}'>"
                f"{html.escape(t('xpractice.state_' + (durum or 'open')))}</span>")
            yazi.setTextFormat(Qt.TextFormat.RichText)
            yazi.setWordWrap(True)
            satir.addWidget(yazi, 1)
            if durum != "solved":
                git = self._button(t("xpractice.go_section"), "ghost",
                                   lambda _=False, s=section: self._go_section(s))
                satir.addWidget(git, 0, Qt.AlignmentFlag.AlignVCenter)
            self._rows.addLayout(satir)

    def _go_section(self, section) -> None:
        # Önce hedef: `accept` kapanış işini hemen çalıştırıyor.
        self.section_requested.emit(section.chapter_id, section.id)
        self.accept()

    # --- kapanış ---------------------------------------------------------------

    def done(self, result: int) -> None:  # noqa: D102
        self._view.release_workers(self.window())
        if self.parentWidget() is not None:
            self.parentWidget().removeEventFilter(self)
        super().done(result)

    def keyPressEvent(self, event) -> None:  # noqa: N802
        sonuc = self._stack.currentWidget() is self._summary_page
        if sonuc and event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self.accept()
            return
        super().keyPressEvent(event)
