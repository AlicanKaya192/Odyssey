"""Sınav görünümü.

Bütün sorular tek sayfada listelenir; kullanıcı istediği sırayla cevaplayıp
hepsini birden gönderir. Gönderdikten sonra her sorunun doğru cevabı ve
açıklaması görünür — sınavın amacı not vermek değil, öğretmek.
"""

from __future__ import annotations

import json
from pathlib import Path

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QButtonGroup,
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
from ..resources.theme.tokens import READING_WIDTH, SPACING


class QuestionCard(QFrame):
    """Tek bir soru."""

    def __init__(self, index: int, question: dict, language: LanguageManager) -> None:
        super().__init__()
        self._question = question
        self._language = language
        self._answered = False
        self.setProperty("surface", "true")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(SPACING["lg"], SPACING["lg"], SPACING["lg"], SPACING["lg"])
        layout.setSpacing(SPACING["sm"])

        self._number = QLabel()
        self._number.setProperty("role", "section")
        layout.addWidget(self._number)

        self._text = QLabel(language.pick(question.get("text")))
        self._text.setWordWrap(True)
        self._text.setProperty("role", "subtitle")
        layout.addWidget(self._text)
        layout.addSpacing(SPACING["xs"])

        self._group = QButtonGroup(self)
        self._buttons: list[QRadioButton] = []

        options = language.pick(question.get("options"), []) or []
        for position, option in enumerate(options):
            button = QRadioButton(option)
            button.setProperty("index", position)
            self._group.addButton(button, position)
            self._buttons.append(button)
            layout.addWidget(button)

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

        for position, button in enumerate(self._buttons):
            button.setEnabled(False)
            if position == correct:
                button.setProperty("tone", "success")
            elif position == self.selected:
                button.setProperty("tone", "danger")
            button.style().unpolish(button)
            button.style().polish(button)

        explanation = self._language.pick(self._question.get("explanation"))
        if explanation:
            self._feedback_text.setText(explanation)
            self._feedback.show()

    def reset(self) -> None:
        self._answered = False
        self._group.setExclusive(False)
        for button in self._buttons:
            button.setChecked(False)
            button.setEnabled(True)
            button.setProperty("tone", "")
            button.style().unpolish(button)
            button.style().polish(button)
        self._group.setExclusive(True)
        self._feedback.hide()

    def retranslate(self, total: int = 0) -> None:
        self._number.setText(
            self._language.t("quiz.question", current=self._index + 1, total=total)
            if total
            else f"{self._index + 1}."
        )
        self._text.setText(self._language.pick(self._question.get("text")))

        options = self._language.pick(self._question.get("options"), []) or []
        for button, option in zip(self._buttons, options):
            button.setText(option)

        if self._answered:
            explanation = self._language.pick(self._question.get("explanation"))
            if explanation:
                self._feedback_text.setText(explanation)


class QuizView(QWidget):
    """Bir alt bölümün sınavı."""

    completed = Signal(int, bool)  # puan, geçti mi

    def __init__(self, language: LanguageManager, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._language = language
        self._cards: list[QuestionCard] = []
        self._pass_score = 70

        layout = QVBoxLayout(self)
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

    def show_quiz(self, path: Path, pass_score: int = 70) -> None:
        """Sınav dosyasını yükler."""
        self._pass_score = pass_score
        self._clear()

        with path.open(encoding="utf-8") as handle:
            data = json.load(handle)

        for index, question in enumerate(data.get("questions", [])):
            card = QuestionCard(index, question, self._language)
            self._cards.append(card)
            self._cards_holder.addWidget(card)

        self.retranslate()

    def _clear(self) -> None:
        for card in self._cards:
            card.deleteLater()
        self._cards = []
        self._result.hide()
        self._retry_button.hide()
        self._submit_button.show()

    def _submit(self) -> None:
        if not self._cards:
            return

        unanswered = sum(1 for card in self._cards if card.selected is None)
        if unanswered:
            self._result.setText(
                self._language.t("quiz.unanswered", count=unanswered)
            )
            self._result.setProperty("tone", "warning")
            self._result.style().unpolish(self._result)
            self._result.style().polish(self._result)
            self._result.show()
            return

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
        self._result.setText(message)
        self._result.setProperty("tone", "success" if passed else "danger")
        self._result.style().unpolish(self._result)
        self._result.style().polish(self._result)
        self._result.show()

        self._submit_button.hide()
        self._retry_button.show()
        self.completed.emit(score, passed)

    def _reset(self) -> None:
        for card in self._cards:
            card.reset()
        self._result.hide()
        self._retry_button.hide()
        self._submit_button.show()

    def set_mode(self, mode: str) -> None:
        # Renkler tema dosyasından geliyor, ek iş gerekmiyor.
        pass

    def retranslate(self) -> None:
        self._submit_button.setText(self._language.t("quiz.submit"))
        self._retry_button.setText(self._language.t("quiz.retry"))
        for card in self._cards:
            card.retranslate(len(self._cards))
