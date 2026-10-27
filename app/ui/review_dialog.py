"""Tekrar kutusu penceresi (`core/review_box.py`).

İki sayfa: sorular, sonuç. Sınav ekranının soru kartı (`QuestionCard`)
kullanılıyor; seviye tespitinden farklı olarak bu bir ders: cevaptan sonra
doğrusu ve açıklaması gösteriliyor. Her cevap o an kaydediliyor, yani
pencere yarıda kapatılırsa (Esc) cevaplananlar işlenmiş, kalanlar kutuda.

Klavye: 1–4 / A–D şık, Enter cevapla / sonraki (sınav ekranıyla aynı).
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

from datetime import date, timedelta

from ..core import practice_exam, review_box
from ..core.language import LanguageManager
from ..core.quiz_shuffle import prepare
from ..resources.theme.tokens import SPACING
from . import modal
from .quiz_view import QuestionCard

DIALOG_WIDTH = 700
DIALOG_HEIGHT = 640


class ReviewDialog(QDialog):
    """Bugünün tekrar soruları; cevaplar o an işleniyor.

    `source` soruların kaynağı: burada katalog, tekrar sınavında modül
    (`PracticeDialog`). Alt sınıf `_load_items`, `_record` ve
    `_result_texts`'i değiştiriyor; akış ve klavye ortak.
    """

    TITLE_KEY = "review.title"

    def __init__(self, language: LanguageManager, store, source, mode: str = "light",
                 parent: QWidget | None = None, today=None, rng=None) -> None:
        super().__init__(parent)
        self._language = language
        self._store = store
        self._mode = mode
        self._today = today
        self._rng = rng
        self._items = self._load_items(source)
        self._index = 0
        self._correct = 0
        self._answered = 0
        self._card: QuestionCard | None = None
        t = language.t

        modal.prepare(self)
        self.setFixedSize(DIALOG_WIDTH, DIALOG_HEIGHT)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        kok = QVBoxLayout(self)
        kok.setContentsMargins(SPACING["xl"], SPACING["xl"], SPACING["xl"], SPACING["xl"])
        self._stack = QStackedWidget()
        self._stack.setProperty("role", "bare")
        kok.addWidget(self._stack)

        # --- sorular -------------------------------------------------------
        sorular = QWidget()
        sorular.setProperty("role", "bare")
        self._question_page = sorular
        s = QVBoxLayout(sorular)
        s.setContentsMargins(0, 0, 0, 0)
        s.setSpacing(SPACING["sm"])
        baslik = QLabel(t(self.TITLE_KEY))
        baslik.setProperty("role", "modal-title")
        s.addWidget(baslik)
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
        bitir = QPushButton(t("review.finish"))
        bitir.setProperty("variant", "ghost")
        bitir.setCursor(Qt.CursorShape.PointingHandCursor)
        bitir.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        bitir.clicked.connect(self._finish)
        alt.addWidget(bitir)
        alt.addStretch(1)
        self._next_button = QPushButton()
        self._next_button.setProperty("variant", "primary")
        self._next_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._next_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self._next_button.clicked.connect(self._advance)
        alt.addWidget(self._next_button)
        s.addLayout(alt)
        self._stack.addWidget(sorular)

        # --- sonuç ---------------------------------------------------------
        sonuc = QWidget()
        sonuc.setProperty("role", "bare")
        self._result_page = sonuc
        r = QVBoxLayout(sonuc)
        r.setContentsMargins(0, 0, 0, 0)
        r.setSpacing(SPACING["sm"])
        self._result_title = QLabel()
        self._result_title.setProperty("role", "modal-title")
        self._result_title.setWordWrap(True)
        r.addWidget(self._result_title)
        self._result_text = QLabel()
        self._result_text.setTextFormat(Qt.TextFormat.RichText)
        self._result_text.setProperty("role", "muted")
        self._result_text.setWordWrap(True)
        r.addWidget(self._result_text)
        r.addSpacing(SPACING["md"])
        alt = QHBoxLayout()
        alt.addStretch(1)
        tamam = QPushButton(t("review.done"))
        self._done_button = tamam
        tamam.setProperty("variant", "primary")
        tamam.setCursor(Qt.CursorShape.PointingHandCursor)
        tamam.clicked.connect(self.accept)
        alt.addWidget(tamam)
        r.addLayout(alt)
        self._stack.addWidget(sonuc)

        if self._items:
            self._show_question()
        else:
            self._finish()

    def _load_items(self, catalog) -> list[tuple[dict, object, dict]]:
        """Bugünün kayıtları → (kayıt, bölüm, soru). Sorusu artık dosyada
        olmayan (bölüm kalkmış ya da soru değişmiş) kayıt kutudan çıkıyor."""
        sonuc = []
        dosyalar: dict[tuple[str, str], list[dict]] = {}
        for item in review_box.today_items(self._store, self._today):
            anahtar = (item["chapter_id"], item["section_id"])
            section = catalog.section(*anahtar)
            if anahtar not in dosyalar:
                dosyalar[anahtar] = review_box.load_questions(section, self._language.language)
            soru = review_box.find_question(dosyalar[anahtar], item)
            if section is None or soru is None:
                self._store.set_review(item["chapter_id"], item["section_id"],
                                       item["question_key"], None)
                continue
            sonuc.append((item, section, prepare([soru], self._rng)[0]))
        return sonuc

    @property
    def answered(self) -> int:
        return self._answered

    def showEvent(self, event) -> None:  # noqa: N802
        super().showEvent(event)
        modal.center(self)

    # --- akış --------------------------------------------------------------

    def _show_question(self) -> None:
        t = self._language.t
        item, section, soru = self._items[self._index]
        self._progress.setText(t("review.progress", n=self._index + 1, total=len(self._items)))
        self._section_label.setText(self._language.pick(section.title))
        kart = QuestionCard(self._index, soru, self._language, self._mode)
        kart.picked.connect(self._sync_button)
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
        self._revealed = False
        self._sync_button()
        self.setFocus()

    def _sync_button(self) -> None:
        t = self._language.t
        if self._revealed:
            son = self._index + 1 >= len(self._items)
            self._next_button.setText(t("review.finish") if son else t("review.next"))
            self._next_button.setEnabled(True)
        else:
            self._next_button.setText(t("review.answer"))
            self._next_button.setEnabled(self._card is not None and self._card.selected is not None)

    def _advance(self) -> None:
        if self._card is None:
            return
        if not self._revealed:
            if self._card.selected is None:
                return
            self._record(self._card.is_correct)
            self._card.reveal()
            self._revealed = True
            self._sync_button()
            return
        self._index += 1
        if self._index >= len(self._items):
            self._finish()
        else:
            self._show_question()

    def _record(self, correct: bool) -> None:
        item, section, _soru = self._items[self._index]
        review_box.answer(self._store, item, correct, self._today)
        self._answered += 1
        self._correct += int(correct)
        # Tekrar da çalışmadır: seri ve etkinlik takvimi (XP yok).
        self._store.mark_study_day()
        self._store.record_activity("review", item["chapter_id"], item["section_id"])

    def _result_texts(self) -> tuple[str, str]:
        t = self._language.t
        if self._answered:
            return t("review.result_title"), html.escape(
                t("review.result_text", correct=self._correct, total=self._answered))
        return t("review.title"), html.escape(t("review.result_none"))

    def _finish(self) -> None:
        baslik, metin = self._result_texts()
        self._result_title.setText(baslik)
        self._result_text.setText(metin)
        # Soru sayfası yığından çıkıyor: yığın en büyük sayfanın en küçük
        # boyunu koruyor, sonuç sayfası küçülemiyordu.
        self._stack.setCurrentWidget(self._result_page)
        if self._stack.indexOf(self._question_page) >= 0:
            self._stack.removeWidget(self._question_page)
            self._question_page.hide()
        # Sonuç iki satır: pencere yazısı kadar (soru sayfasının boyunda boş
        # duruyordu). Boy parçalardan toplanıyor; `totalHeightForWidth` bu
        # sayfada fazlasını veriyordu (ölçüldü).
        kenar = SPACING["xl"]
        ic = DIALOG_WIDTH - 2 * kenar
        boy = (self._result_title.heightForWidth(ic) + self._result_text.heightForWidth(ic)
               + self._done_button.sizeHint().height() + SPACING["sm"] * 2 + SPACING["md"])
        self.setFixedHeight(boy + 2 * kenar)
        modal.center(self)
        self.setFocus()

    # --- klavye ------------------------------------------------------------

    def keyPressEvent(self, event: QKeyEvent) -> None:  # noqa: N802
        tus = event.key()
        sonuc = self._stack.currentWidget() is self._result_page
        if not sonuc and self._card is not None:
            harf = event.text().upper()
            secenek = None
            if Qt.Key.Key_1 <= tus <= Qt.Key.Key_9:
                secenek = tus - Qt.Key.Key_1
            elif harf and "A" <= harf <= "H" and len(harf) == 1:
                secenek = ord(harf) - ord("A")
            if secenek is not None and not self._revealed and secenek < len(self._card._tiles):  # noqa: SLF001
                self._card._pick(secenek)  # noqa: SLF001
                return
            if tus in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
                self._advance()
                return
        if sonuc and tus in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self.accept()
            return
        super().keyPressEvent(event)


class PracticeDialog(ReviewDialog):
    """Tekrar sınavı (`core/practice_exam.py`): modülde bitirilen
    bölümlerden karışık sorular. Yanlışlar tekrar kutusuna giriyor; kilit,
    XP ve rozet değişmiyor."""

    TITLE_KEY = "practice.title"

    def __init__(self, language: LanguageManager, store, chapter, mode: str = "light",
                 parent: QWidget | None = None, today=None, rng=None) -> None:
        self._chapter = chapter
        self._per_section: dict[str, list[int]] = {}
        super().__init__(language, store, chapter, mode, parent, today, rng)

    def _load_items(self, chapter) -> list[tuple[dict, object, dict]]:
        bolumler = practice_exam.done_sections(chapter, self._store, self._language.language)
        sonuc = []
        for soru in practice_exam.build(bolumler, self._language.language, self._rng):
            bolum = soru["section"]
            kayit = {"chapter_id": bolum.chapter_id, "section_id": bolum.id,
                     "question_index": soru["index"],
                     "question_key": review_box.question_key(soru["question"])}
            sonuc.append((kayit, bolum, prepare([soru["question"]], self._rng)[0]))
        return sonuc

    def _record(self, correct: bool) -> None:
        item, section, _soru = self._items[self._index]
        self._answered += 1
        self._correct += int(correct)
        sayac = self._per_section.setdefault(section.id, [0, 0])
        sayac[0] += int(correct)
        sayac[1] += 1
        if not correct:
            yarin = (self._today or date.today()) + timedelta(days=1)
            self._store.add_review_items(item["chapter_id"], item["section_id"],
                                         [(item["question_index"], item["question_key"])], yarin)
        self._store.mark_study_day()
        self._store.record_activity("practice", item["chapter_id"], item["section_id"])

    def _result_texts(self) -> tuple[str, str]:
        t = self._language.t
        if not self._answered:
            return t(self.TITLE_KEY), html.escape(t("practice.result_none"))
        practice_exam.save(self._store, self._chapter.id, self._correct, self._answered, self._today)
        yanlis = self._answered - self._correct
        metin = (t("practice.result_wrong", correct=self._correct, total=self._answered, wrong=yanlis)
                 if yanlis else t("practice.result_all", total=self._answered))
        # Bölüm bölüm: hangi konuya dönmeli. Sorulma sırasıyla değil modüldeki sırayla.
        adlar = {bolum.id: self._language.pick(bolum.title) for _k, bolum, _s in self._items}
        sira = [b.id for b in self._chapter.sections if b.id in self._per_section]
        satirlar = [f"{html.escape(adlar[i])}: {self._per_section[i][0]}/{self._per_section[i][1]}"
                    for i in sira]
        return t("practice.result_title"), html.escape(metin) + "<br><br>" + "<br>".join(satirlar)
