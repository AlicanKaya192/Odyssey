"""Seviye tespit sınavı penceresi (`core/placement.py`).

Üç sayfa: giriş (ne olacağı, kaç soru), sorular, sonuç. Sorular sınav
ekranının soru kartıyla (`QuestionCard`) gösteriliyor ama **cevap
açıklanmıyor**: bu bir ders değil ölçüm; doğruyu göstermek sonraki bölümün
sorusunu kolaylaştırırdı. Sonuç sayfasında bölüm bölüm ✓ / ✕ var; ✕ olan
bölüme sonra girip öğrenebiliyor.

Her an "Burada bitir" denebiliyor; o ana kadar cevaplanan bölümler
değerlendiriliyor. Pencere kapatılırsa (Esc, Vazgeç) hiçbir şey
kaydedilmiyor.

Klavye: 1–4 / A–D şık, Enter sonraki (sınav ekranıyla aynı).
"""

from __future__ import annotations

import html

from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from ..core import placement
from ..core.language import LanguageManager
from ..resources.theme.tokens import PALETTES, SPACING
from . import modal
from .quiz_view import QuestionCard

DIALOG_WIDTH = 700
# Soru ve sonuç sayfalarının boyu; giriş sayfası yazısı kadar (Alican: kısa
# yazı büyük pencerede boş duruyordu).
DIALOG_HEIGHT = 640


class PlacementDialog(QDialog):
    """Seviye tespit sınavı; kabul edilirse sonuç kaydedilmiş olur."""

    def __init__(self, language: LanguageManager, store, chapter, mode: str = "light",
                 parent: QWidget | None = None, rng=None) -> None:
        super().__init__(parent)
        self._language = language
        self._store = store
        self._chapter = chapter
        self._mode = mode
        self._items = placement.build(chapter, language.language, rng)
        self._done = 0          # cevaplanan bölüm sayısı
        self._question = 0      # o bölümdeki soru
        self._card: QuestionCard | None = None
        self.reach_id = ""
        t = language.t

        modal.prepare(self)
        self.setFixedWidth(DIALOG_WIDTH)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        kok = QVBoxLayout(self)
        kok.setContentsMargins(SPACING["xl"], SPACING["xl"], SPACING["xl"], SPACING["xl"])
        self._stack = QStackedWidget()
        # Yalnızca yerleşim: genel `QWidget` zemini pencerede koyu leke bırakıyordu.
        self._stack.setProperty("role", "bare")
        kok.addWidget(self._stack)

        # --- giriş ---------------------------------------------------------
        giris = QWidget()
        giris.setProperty("role", "bare")
        g = QVBoxLayout(giris)
        g.setContentsMargins(0, 0, 0, 0)
        g.setSpacing(SPACING["md"])
        baslik = QLabel(t("placement.title"))
        baslik.setProperty("role", "modal-title")
        g.addWidget(baslik)
        modul = QLabel(language.pick(chapter.title))
        modul.setProperty("role", "muted")
        g.addWidget(modul)
        g.addSpacing(SPACING["sm"])
        soru = sum(len(it.questions) for it in self._items)
        for anahtar in ("placement.intro_1", "placement.intro_2", "placement.intro_3"):
            satir = QLabel(t(anahtar, sections=len(self._items), questions=soru,
                             per=placement.QUESTIONS_PER_SECTION, need=placement.PASS_CORRECT))
            satir.setWordWrap(True)
            g.addWidget(satir)
        g.addSpacing(SPACING["md"])
        alt = QHBoxLayout()
        alt.addStretch(1)
        vazgec = QPushButton(t("common.cancel"))
        vazgec.setProperty("variant", "ghost")
        vazgec.setCursor(Qt.CursorShape.PointingHandCursor)
        vazgec.clicked.connect(self.reject)
        alt.addWidget(vazgec)
        self._start_button = QPushButton(t("placement.start"))
        self._start_button.setProperty("variant", "primary")
        self._start_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._start_button.clicked.connect(self._begin)
        alt.addWidget(self._start_button)
        g.addLayout(alt)
        self._intro = giris
        self._stack.addWidget(giris)

        # --- sorular -------------------------------------------------------
        sorular = QWidget()
        sorular.setProperty("role", "bare")
        s = QVBoxLayout(sorular)
        s.setContentsMargins(0, 0, 0, 0)
        s.setSpacing(SPACING["sm"])
        self._progress = QLabel()
        self._progress.setProperty("role", "muted")
        s.addWidget(self._progress)
        self._section_label = QLabel()
        self._section_label.setProperty("role", "subtitle")
        self._section_label.setWordWrap(True)
        s.addWidget(self._section_label)
        s.addSpacing(SPACING["sm"])
        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)
        self._scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        self._scroll.setProperty("role", "bare")
        s.addWidget(self._scroll, 1)
        alt = QHBoxLayout()
        self._stop_button = QPushButton(t("placement.stop"))
        self._stop_button.setProperty("variant", "ghost")
        self._stop_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._stop_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self._stop_button.clicked.connect(self._finish)
        alt.addWidget(self._stop_button)
        alt.addStretch(1)
        self._next_button = QPushButton(t("placement.next"))
        self._next_button.setProperty("variant", "primary")
        self._next_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._next_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self._next_button.clicked.connect(self._next)
        alt.addWidget(self._next_button)
        s.addLayout(alt)
        self._stack.addWidget(sorular)

        # --- sonuç ---------------------------------------------------------
        sonuc = QWidget()
        sonuc.setProperty("role", "bare")
        r = QVBoxLayout(sonuc)
        r.setContentsMargins(0, 0, 0, 0)
        r.setSpacing(SPACING["sm"])
        self._result_title = QLabel()
        self._result_title.setProperty("role", "modal-title")
        self._result_title.setWordWrap(True)
        r.addWidget(self._result_title)
        self._result_text = QLabel()
        self._result_text.setWordWrap(True)
        self._result_text.setProperty("role", "muted")
        r.addWidget(self._result_text)
        r.addSpacing(SPACING["sm"])
        self._result_list = QLabel()
        self._result_list.setTextFormat(Qt.TextFormat.RichText)
        self._result_list.setWordWrap(True)
        self._result_list.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        liste = QScrollArea()
        liste.setWidgetResizable(True)
        liste.setFrameShape(QScrollArea.Shape.NoFrame)
        liste.setProperty("role", "bare")
        liste.setWidget(self._result_list)
        r.addWidget(liste, 1)
        alt = QHBoxLayout()
        alt.addStretch(1)
        tamam = QPushButton(t("placement.done"))
        tamam.setProperty("variant", "primary")
        tamam.setCursor(Qt.CursorShape.PointingHandCursor)
        tamam.clicked.connect(self.accept)
        alt.addWidget(tamam)
        r.addLayout(alt)
        self._stack.addWidget(sonuc)

        self._fit_intro()

    def _fit_intro(self) -> None:
        """Giriş sayfası yazısı kadar yer kaplıyor."""
        kenar = SPACING["xl"]
        ic = DIALOG_WIDTH - 2 * kenar
        self.setFixedHeight(self._intro.layout().totalHeightForWidth(ic) + 2 * kenar)

    def _grow(self) -> None:
        """Soru ve sonuç sayfaları büyük, sabit boy; pencere yeniden ortalanıyor."""
        if self.height() != DIALOG_HEIGHT:
            self.setFixedHeight(DIALOG_HEIGHT)
            modal.center(self)

    def showEvent(self, event) -> None:  # noqa: N802
        super().showEvent(event)
        modal.center(self)

    # --- akış --------------------------------------------------------------

    @property
    def done_sections(self) -> int:
        return self._done

    def _begin(self) -> None:
        if not self._items:
            self.reject()
            return
        self._stack.setCurrentIndex(1)
        self._grow()
        self._show_question()
        self.setFocus()

    def _show_question(self) -> None:
        t = self._language.t
        item = self._items[self._done]
        soru = item.questions[self._question]
        self._progress.setText(t("placement.progress", section=self._done + 1, sections=len(self._items),
                                 question=self._question + 1, questions=len(item.questions)))
        self._section_label.setText(self._language.pick(item.section.title))
        kart = QuestionCard(self._question, soru, self._language, self._mode)
        kart.picked.connect(self._sync_next)
        self._card = kart
        tasiyici = QWidget()
        tasiyici.setProperty("role", "bare")
        yer = QVBoxLayout(tasiyici)
        yer.setContentsMargins(0, 0, 8, 0)
        yer.addWidget(kart)
        yer.addStretch(1)
        eski = self._scroll.takeWidget()
        if eski is not None:
            eski.deleteLater()
        self._scroll.setWidget(tasiyici)
        self._sync_next()

    def _sync_next(self) -> None:
        self._next_button.setEnabled(self._card is not None and self._card.selected is not None)

    def _next(self) -> None:
        if self._card is None or self._card.selected is None:
            return
        item = self._items[self._done]
        item.correct.append(self._card.is_correct)
        self._question += 1
        if self._question < len(item.questions):
            self._show_question()
            return
        self._done += 1
        self._question = 0
        if self._done >= len(self._items) or placement.should_stop(self._items, self._done):
            self._finish()
            return
        self._show_question()

    def _finish(self) -> None:
        """Cevaplanan bölümleri değerlendirir, kaydeder, sonucu gösterir."""
        t = self._language.t
        # Yarıda kalan bölüm sayılmıyor.
        if self._question:
            self._items[self._done].correct = []
        self.reach_id = placement.save(self._store, self._chapter.id, self._items, self._done)
        sira = placement.reach(self._items[: self._done])
        acilan = sira + 1
        if acilan:
            self._result_title.setText(t("placement.result_title", count=acilan))
            sonraki = self._items[sira + 1].section if sira + 1 < len(self._items) else None
            self._result_text.setText(
                t("placement.result_next", section=self._language.pick(sonraki.title)) if sonraki
                else t("placement.result_all")
            )
        else:
            self._result_title.setText(t("placement.result_none_title"))
            self._result_text.setText(t("placement.result_none"))
        p = PALETTES.get(self._mode, PALETTES["light"])
        satirlar = []
        for i, item in enumerate(self._items):
            ad = html.escape(self._language.pick(item.section.title))
            if i >= self._done:
                isaret, renk, not_ = "·", p["text_muted"], t("placement.not_asked")
            elif placement.passed(item):
                isaret, renk, not_ = "✓", p["success"], t("placement.known")
            else:
                isaret, renk, not_ = "✕", p["danger"], t("placement.review")
            satirlar.append(
                f"<tr><td style='color:{renk}; padding:3px 10px 3px 0; font-weight:700;'>{isaret}</td>"
                f"<td style='color:{p['text']}; padding:3px 14px 3px 0;'>{ad}</td>"
                f"<td style='color:{renk}; padding:3px 0;'>{html.escape(not_)}</td></tr>"
            )
        self._result_list.setText("<table cellspacing='0'>" + "".join(satirlar) + "</table>")
        self._stack.setCurrentIndex(2)
        self._grow()

    # --- klavye ------------------------------------------------------------

    def keyPressEvent(self, event: QKeyEvent) -> None:  # noqa: N802
        if self._stack.currentIndex() == 1 and self._card is not None:
            tus = event.key()
            harf = event.text().upper()
            secenek = None
            if Qt.Key.Key_1 <= tus <= Qt.Key.Key_9:
                secenek = tus - Qt.Key.Key_1
            elif harf and "A" <= harf <= "H" and len(harf) == 1:
                secenek = ord(harf) - ord("A")
            if secenek is not None and secenek < len(self._card._tiles):  # noqa: SLF001
                self._card._pick(secenek)  # noqa: SLF001
                return
            if tus in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
                self._next()
                return
        if self._stack.currentIndex() == 2 and event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self.accept()
            return
        super().keyPressEvent(event)
