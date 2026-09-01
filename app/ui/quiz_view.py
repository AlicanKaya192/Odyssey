"""Sınav görünümü.

İki ekran var. **Sınav sekmesine geçince sorular hemen görünmüyor**; önce
bir başlangıç ekranı çıkıyor: kaç soru olduğu, ne kadar süre tanındığı ve
varsa önceki denemenin notu. Hazır olduğunda "Sınavı Başlat" deniyor.
Sorular sekmeye dokunur dokunmaz açılsaydı süre, kişi daha ne olduğunu
anlamadan işlemeye başlardı.

Başladıktan sonra bütün sorular tek sayfada listeleniyor; kullanıcı istediği
sırayla cevaplayıp hepsini birden gönderiyor. Gönderdikten sonra her sorunun
doğru cevabı ve açıklaması görünüyor — sınavın amacı not vermek değil,
öğretmek.

Süre dolunca sınav kendiliğinden gönderiliyor; boş kalan sorular yanlış
sayılıyor. Sayaç sağ üst köşede duruyor, kaydırmayla kaymıyor ve içeriğin
üstünü örtmüyor.

Her denemede sorular ve şıklar yeniden karışıyor (`app/core/quiz_shuffle.py`).
"""

from __future__ import annotations

import json
from pathlib import Path

from PySide6.QtCore import QEvent, Qt, QTimer, Signal
from PySide6.QtWidgets import (
    QButtonGroup,
    QStackedWidget,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QRadioButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from ..core.language import LanguageManager
from ..core.quiz_shuffle import prepare
from ..resources.theme.tokens import PALETTES, READING_WIDTH, SPACING
from ..widgets import richtext
from ..widgets.common import Card
from ..widgets.timer_ring import TimerRing, format_clock


class OptionRow(QWidget):
    """Tek bir şık: yuvarlak seçim düğmesi ve yanında metni.

    `QRadioButton` zengin metin çizemiyor, bu yüzden şık metni ayrı bir
    `QLabel` olarak duruyor. Metne tıklamak da şıkkı seçiyor; kullanan kişi
    için ikisi tek bir düğme gibi davranıyor.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 2, 0, 2)
        layout.setSpacing(SPACING["sm"])

        self.button = QRadioButton()
        self.button.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(self.button, 0, Qt.AlignmentFlag.AlignTop)

        self.label = QLabel()
        self.label.setWordWrap(True)
        self.label.setCursor(Qt.CursorShape.PointingHandCursor)
        self.label.installEventFilter(self)
        layout.addWidget(self.label, 1)

    def eventFilter(self, watched, event):  # noqa: N802 (Qt adlandırması)
        if (
            watched is self.label
            and event.type() == QEvent.Type.MouseButtonRelease
            and self.button.isEnabled()
        ):
            self.button.setChecked(True)
            return True
        return super().eventFilter(watched, event)

    def set_text(self, text: str, mode: str) -> None:
        self.label.setText(richtext.render(text, mode))

    def set_enabled(self, enabled: bool) -> None:
        self.button.setEnabled(enabled)
        self.label.setCursor(
            Qt.CursorShape.PointingHandCursor
            if enabled
            else Qt.CursorShape.ArrowCursor
        )

    def set_tone(self, tone: str) -> None:
        for widget in (self.button, self.label):
            widget.setProperty("tone", tone)
            widget.style().unpolish(widget)
            widget.style().polish(widget)


class QuestionCard(QFrame):
    """Tek bir soru."""

    def __init__(
        self,
        index: int,
        question: dict,
        language: LanguageManager,
        mode: str = "light",
    ) -> None:
        super().__init__()
        self._question = question
        self._language = language
        self._answered = False
        self._mode = mode
        self._total = 0
        self.setProperty("surface", "true")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(SPACING["lg"], SPACING["lg"], SPACING["lg"], SPACING["lg"])
        layout.setSpacing(SPACING["sm"])

        self._number = QLabel()
        self._number.setProperty("role", "section")
        layout.addWidget(self._number)

        self._text = QLabel()
        self._text.setWordWrap(True)
        self._text.setTextFormat(Qt.TextFormat.RichText)
        self._text.setProperty("role", "subtitle")
        layout.addWidget(self._text)
        layout.addSpacing(SPACING["xs"])

        self._group = QButtonGroup(self)
        self._buttons: list[QRadioButton] = []

        self._rows: list[OptionRow] = []

        options = language.pick(question.get("options"), []) or []
        for position, _ in enumerate(options):
            row = OptionRow()
            row.button.setProperty("index", position)
            self._group.addButton(row.button, position)
            self._buttons.append(row.button)
            self._rows.append(row)
            layout.addWidget(row)

        # Açıklama, konu anlatımındaki ipucu kutusuyla aynı görünümde:
        # ampul simgesi, vurgu renginde sol kenar ve dolgulu zemin. Düz metin
        # olarak bırakıldığında şıkların arasında kaybolup gidiyordu.
        self._feedback = QFrame()
        self._feedback.setProperty("banner", "accent")
        self._feedback.hide()

        feedback_layout = QHBoxLayout(self._feedback)
        feedback_layout.setContentsMargins(
            SPACING["md"], SPACING["sm"], SPACING["md"], SPACING["sm"]
        )
        feedback_layout.setSpacing(SPACING["sm"])

        self._feedback_icon = QLabel("💡")
        self._feedback_icon.setFixedWidth(20)
        self._feedback_icon.setAlignment(Qt.AlignmentFlag.AlignTop)
        feedback_layout.addWidget(self._feedback_icon)

        self._feedback_text = QLabel()
        self._feedback_text.setWordWrap(True)
        self._feedback_text.setTextFormat(Qt.TextFormat.RichText)
        self._feedback_text.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        feedback_layout.addWidget(self._feedback_text, 1)

        layout.addSpacing(SPACING["xs"])
        layout.addWidget(self._feedback)

        self._index = index
        self.retranslate()

    @property
    def selected(self) -> int | None:
        checked = self._group.checkedId()
        return None if checked < 0 else checked

    @property
    def is_correct(self) -> bool:
        return self.selected == int(self._question.get("answer", -1))

    def reveal(self) -> None:
        """Doğru cevabı ve açıklamayı gösterir."""
        self._answered = True
        correct = int(self._question.get("answer", -1))

        for position, row in enumerate(self._rows):
            row.set_enabled(False)
            if position == correct:
                row.set_tone("success")
            elif position == self.selected:
                row.set_tone("danger")

        explanation = self._language.pick(self._question.get("explanation"))
        if explanation:
            self._feedback_text.setText(
                richtext.render(explanation, self._mode)
            )
            self._feedback.show()

    def reset(self) -> None:
        self._answered = False
        self._group.setExclusive(False)
        for row in self._rows:
            row.button.setChecked(False)
            row.set_enabled(True)
            row.set_tone("")
        self._group.setExclusive(True)
        self._feedback.hide()

    def retranslate(self, total: int = 0) -> None:
        self._total = total or self._total
        self._number.setText(
            self._language.t("quiz.question", current=self._index + 1, total=total)
            if total
            else f"{self._index + 1}."
        )
        self._text.setText(
            richtext.render(self._language.pick(self._question.get("text")), self._mode)
        )

        options = self._language.pick(self._question.get("options"), []) or []
        for row, option in zip(self._rows, options):
            row.set_text(option, self._mode)

        if self._answered:
            explanation = self._language.pick(self._question.get("explanation"))
            if explanation:
                self._feedback_text.setText(
                    richtext.render(explanation, self._mode)
                )

    def set_mode(self, mode: str) -> None:
        """Tema değişince kod parçalarının renkleri yeniden üretiliyor."""
        self._mode = mode
        self.retranslate(self._total)


class QuizView(QWidget):
    """Bir alt bölümün sınavı: başlangıç ekranı ve sorular."""

    completed = Signal(int, bool)  # puan, geçti mi

    def __init__(self, language: LanguageManager, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._language = language
        self._cards: list[QuestionCard] = []
        self._questions: list[dict] = []
        self._pass_score = 70
        self._mode = "light"

        self._time_limit = 0
        self._left = 0
        self._untimed = False
        self._previous_score: int | None = None
        self._previous_passed = False

        self._timer = QTimer(self)
        self._timer.setInterval(1000)
        self._timer.timeout.connect(self._tick)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self._stack = QStackedWidget()
        self._stack.addWidget(self._build_start_page())
        self._stack.addWidget(self._build_quiz_page())
        layout.addWidget(self._stack)

        # Sayaç kaydırma alanının içinde değil, görünümün kendi çocuğu:
        # sayfa kayarken yerinde kalıyor ve metnin üstünü örtmüyor.
        self._corner = TimerRing(58, 4, self)
        self._corner.hide()

    # --- başlangıç ekranı --------------------------------------------------

    def _build_start_page(self) -> QWidget:
        page = QWidget()
        outer = QVBoxLayout(page)
        outer.setContentsMargins(SPACING["xl"], SPACING["xxl"], SPACING["xl"], SPACING["xl"])
        outer.addStretch(1)

        row = QHBoxLayout()
        row.addStretch(1)

        card = Card(mode=self._mode, padding=SPACING["xl"])
        card.setMaximumWidth(460)
        self._start_card = card

        self._start_title = QLabel()
        self._start_title.setProperty("role", "subtitle")
        self._start_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card.body.addWidget(self._start_title)

        self._start_help = QLabel()
        self._start_help.setProperty("role", "muted")
        self._start_help.setWordWrap(True)
        self._start_help.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card.body.addWidget(self._start_help)
        card.body.addSpacing(SPACING["lg"])

        self._preview_ring = TimerRing(112, 6)
        card.body.addWidget(self._preview_ring, 0, Qt.AlignmentFlag.AlignHCenter)
        card.body.addSpacing(SPACING["md"])

        self._previous_label = QLabel()
        self._previous_label.setWordWrap(True)
        self._previous_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._previous_label.hide()
        card.body.addWidget(self._previous_label)
        card.body.addSpacing(SPACING["md"])

        self._start_button = QPushButton()
        self._start_button.setProperty("variant", "primary")
        self._start_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._start_button.clicked.connect(self._start)
        card.body.addWidget(self._start_button)

        row.addWidget(card)
        row.addStretch(1)
        outer.addLayout(row)
        outer.addStretch(2)
        return page

    # --- soru ekranı -------------------------------------------------------

    def _build_quiz_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        container = QWidget()
        row = QHBoxLayout(container)
        row.setContentsMargins(SPACING["xl"], SPACING["xl"], SPACING["xl"], SPACING["xxl"])
        row.addStretch(1)

        column = QWidget()
        column.setMaximumWidth(READING_WIDTH)
        column.setMinimumWidth(320)
        column.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self._column = QVBoxLayout(column)
        self._column.setContentsMargins(0, 0, 0, 0)
        self._column.setSpacing(SPACING["md"])

        self._result = QLabel()
        self._result.setWordWrap(True)
        self._result.setProperty("role", "subtitle")
        self._result.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._result.hide()
        self._column.addWidget(self._result)

        self._cards_holder = QVBoxLayout()
        self._cards_holder.setSpacing(SPACING["md"])
        self._column.addLayout(self._cards_holder)

        buttons = QHBoxLayout()
        buttons.addStretch(1)
        self._retry_button = QPushButton()
        self._retry_button.clicked.connect(self._reset)
        self._retry_button.hide()
        buttons.addWidget(self._retry_button)

        self._submit_button = QPushButton()
        self._submit_button.setProperty("variant", "primary")
        self._submit_button.clicked.connect(self._submit)
        buttons.addWidget(self._submit_button)
        self._column.addLayout(buttons)

        row.addWidget(column, 8)
        row.addStretch(1)
        scroll.setWidget(container)
        layout.addWidget(scroll)
        return page

    # --- yükleme -----------------------------------------------------------

    def show_quiz(
        self,
        path: Path,
        pass_score: int = 70,
        time_limit_sec: int = 0,
        previous_score: int | None = None,
        previous_passed: bool = False,
        untimed: bool = False,
    ) -> None:
        """Sınav dosyasını yükler ve başlangıç ekranını gösterir.

        `untimed`, ayarlardan süre kaldırıldığında geliyor. Bölümün kendi
        süresi `_time_limit` içinde duruyor ama sayaç çalıştırılmıyor;
        ayar kapatıldığında bölümün süresi olduğu gibi geri geliyor.
        """
        self._pass_score = pass_score
        self._untimed = bool(untimed)
        self._time_limit = max(0, int(time_limit_sec))
        self._previous_score = previous_score
        self._previous_passed = previous_passed

        with path.open(encoding="utf-8") as handle:
            data = json.load(handle)
        self._questions = data.get("questions", [])

        self._clear()
        self._show_start()

    def _show_start(self) -> None:
        self._timer.stop()
        self._corner.hide()
        self._stack.setCurrentIndex(0)
        self._preview_ring.set_untimed(self._untimed)
        self._preview_ring.set_total(self._time_limit)
        self.retranslate()

    def _clear(self) -> None:
        for card in self._cards:
            card.deleteLater()
        self._cards = []
        self._result.hide()
        self._retry_button.hide()
        self._submit_button.show()

    # --- akış --------------------------------------------------------------

    def _start(self) -> None:
        """Soruları karıştırıp sınavı başlatır."""
        self._clear()

        for index, question in enumerate(prepare(self._questions)):
            card = QuestionCard(index, question, self._language, self._mode)
            self._cards.append(card)
            self._cards_holder.addWidget(card)

        self._stack.setCurrentIndex(1)
        self.retranslate()

        if self._untimed:
            # Sayaç yok ama köşedeki halka duruyor: sınavın süresiz
            # olduğunu sınav sırasında da görmek gerekiyor.
            self._corner.set_untimed(True)
            self._corner.show()
            self._corner.raise_()
            self._place_corner()
        elif self._time_limit:
            self._left = self._time_limit
            self._corner.set_total(self._time_limit)
            self._corner.show()
            self._corner.raise_()
            self._place_corner()
            self._timer.start()

    def _tick(self) -> None:
        self._left -= 1
        self._corner.set_left(self._left)
        if self._left <= 0:
            self._timer.stop()
            # Süre bitti: boş kalanlar yanlış sayılıyor, sınav gönderiliyor.
            self._submit(timed_out=True)

    def _place_corner(self) -> None:
        pay = SPACING["lg"]
        self._corner.move(self.width() - self._corner.width() - pay, pay)

    def resizeEvent(self, event) -> None:  # noqa: N802
        super().resizeEvent(event)
        self._place_corner()

    def _submit(self, timed_out: bool = False) -> None:
        if not self._cards:
            return

        unanswered = sum(1 for card in self._cards if card.selected is None)
        if unanswered and not timed_out:
            self._result.setText(
                self._language.t("quiz.unanswered", count=unanswered)
            )
            self._result.setProperty("tone", "warning")
            self._result.style().unpolish(self._result)
            self._result.style().polish(self._result)
            self._result.show()
            return

        self._timer.stop()
        self._corner.hide()

        correct = sum(1 for card in self._cards if card.is_correct)
        score = round(correct * 100 / len(self._cards))
        passed = score >= self._pass_score

        for card in self._cards:
            card.reveal()

        message = self._language.t("quiz.score", score=score)
        message += "  —  " + (
            self._language.t("quiz.passed")
            if passed
            else self._language.t("quiz.failed", pass_score=self._pass_score)
        )
        if timed_out:
            message = self._language.t("quiz.timed_out") + "  —  " + message

        self._result.setText(message)
        self._result.setProperty("tone", "success" if passed else "danger")
        self._result.style().unpolish(self._result)
        self._result.style().polish(self._result)
        self._result.show()

        self._submit_button.hide()
        self._retry_button.show()

        # Bir sonraki denemede "önceki notun" olarak bu görünecek.
        self._previous_score = score
        self._previous_passed = passed
        self.completed.emit(score, passed)

    def _reset(self) -> None:
        """Baştan dene: başlangıç ekranına dönüyor, sorular yeniden karışıyor."""
        self._show_start()

    # --- tema ve dil -------------------------------------------------------

    def set_mode(self, mode: str) -> None:
        """Arayüz renkleri tema dosyasından geliyor, ama soru metinlerindeki
        kod parçaları HTML içine gömülü renklerle çiziliyor; onları elle
        yenilemek gerekiyor."""
        self._mode = mode
        self._start_card.set_mode(mode)

        palette = PALETTES.get(mode, PALETTES["light"])
        for ring in (self._preview_ring, self._corner):
            ring.set_colors(
                palette["border"],
                palette["accent"],
                palette["warning"],
                palette["danger"],
                palette["text"],
            )

        for card in self._cards:
            card.set_mode(mode)

    def retranslate(self) -> None:
        self._submit_button.setText(self._language.t("quiz.submit"))
        self._retry_button.setText(self._language.t("quiz.retry"))
        self._start_button.setText(self._language.t("quiz.start"))
        self._start_title.setText(self._language.t("quiz.ready_title"))

        sayi = len(self._questions)
        if self._untimed:
            self._start_help.setText(
                self._language.t(
                    "quiz.ready_help_untimed", count=sayi, pass_score=self._pass_score
                )
            )
        elif self._time_limit:
            self._start_help.setText(
                self._language.t(
                    "quiz.ready_help",
                    count=sayi,
                    time=format_clock(self._time_limit),
                    pass_score=self._pass_score,
                )
            )
        else:
            self._start_help.setText(
                self._language.t(
                    "quiz.ready_help_untimed", count=sayi, pass_score=self._pass_score
                )
            )

        if self._previous_score is None:
            self._previous_label.hide()
        else:
            self._previous_label.setText(
                self._language.t("quiz.previous", score=self._previous_score)
            )
            self._previous_label.setProperty(
                "tone", "success" if self._previous_passed else "danger"
            )
            self._previous_label.style().unpolish(self._previous_label)
            self._previous_label.style().polish(self._previous_label)
            self._previous_label.show()

        for card in self._cards:
            card.retranslate(len(self._cards))
