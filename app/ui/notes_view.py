"""Ders notları görünümü.

Notlar PDF olarak gömülmüyor, metin olarak gösteriliyor. Sebepleri:
uygulama içinde aranabiliyor, kopyalanabiliyor, yazı boyutu kullanıcının
ayarına uyuyor ve açık/koyu temayla uyumlu duruyor. Gömülü bir PDF bunların
hiçbirini yapamıyor.

Bir bölümde birden fazla not olabilir; solda liste, sağda seçili notun metni
duruyor. İlerleyen modüllerde not sayısı arttığında bu yapı bozulmuyor.
"""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from ..core.catalog import Block
from ..core.language import LanguageManager
from ..resources.theme.tokens import SPACING
from ..widgets.common import section_label
from ..widgets.effects import repolish
from .lesson_view import LessonView

LIST_WIDTH = 270


class NotesView(QWidget):
    """Bir bölümün ders notları."""

    def __init__(self, language: LanguageManager, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._language = language
        self._documents: list[dict] = []
        self._directory: Path | None = None
        self._current = 0
        self._buttons: list[QPushButton] = []

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addWidget(self._build_list())
        layout.addWidget(self._build_document(), 1)

    def _build_list(self) -> QWidget:
        panel = QFrame()
        panel.setProperty("surface", "alt")
        panel.setFixedWidth(LIST_WIDTH)

        outer = QVBoxLayout(panel)
        outer.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        holder = QWidget()
        self._list_layout = QVBoxLayout(holder)
        self._list_layout.setContentsMargins(
            SPACING["md"], SPACING["lg"], SPACING["md"], SPACING["lg"]
        )
        self._list_layout.setSpacing(2)

        self._list_title = section_label("")
        self._list_layout.addWidget(self._list_title)
        self._list_layout.addSpacing(SPACING["xs"])
        self._list_layout.addStretch(1)

        scroll.setWidget(holder)
        outer.addWidget(scroll)
        return panel

    def _build_document(self) -> QWidget:
        holder = QWidget()
        layout = QVBoxLayout(holder)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self._reader = LessonView(self._language, show_toc=False)
        layout.addWidget(self._reader, 1)

        footer = self._reader.footer_layout()
        self._previous_button = QPushButton()
        self._previous_button.clicked.connect(lambda: self._step(-1))
        footer.addWidget(self._previous_button)
        footer.addStretch(1)

        self._next_button = QPushButton()
        self._next_button.setProperty("variant", "primary")
        self._next_button.clicked.connect(lambda: self._step(1))
        footer.addWidget(self._next_button)

        self._empty = QLabel()
        self._empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._empty.setProperty("role", "muted")
        layout.addWidget(self._empty)
        self._empty.hide()

        return holder

    # --- içerik -----------------------------------------------------------

    def show_notes(self, block: Block) -> None:
        """Blok içindeki not listesini kurar."""
        self._documents = block.documents
        self._directory = block.directory
        self._current = 0
        self._rebuild_list()
        self._show_current()

    def _rebuild_list(self) -> None:
        while self._list_layout.count() > 2:
            item = self._list_layout.takeAt(1)
            if item.widget():
                item.widget().deleteLater()
        self._buttons = []

        for index, document in enumerate(self._documents):
            title = self._language.pick(document.get("title"))
            button = QPushButton(f"{index + 1:02d}    {title}")
            button.setProperty("variant", "listitem")
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(lambda _=False, i=index: self._select(i))
            self._list_layout.insertWidget(self._list_layout.count() - 1, button)
            self._buttons.append(button)

    def _select(self, index: int) -> None:
        self._current = max(0, min(index, len(self._documents) - 1))
        self._show_current()

    def _step(self, delta: int) -> None:
        self._select(self._current + delta)

    def _show_current(self) -> None:
        has_notes = bool(self._documents)
        self._reader.setVisible(has_notes)
        self._empty.setVisible(not has_notes)

        if not has_notes:
            self._empty.setText(self._language.t("notes.empty"))
            self.retranslate()
            return

        document = self._documents[self._current]
        resolved = self._resolve(document)

        # Not metninin başına başlığı ve sıra bilgisini ekliyoruz; kaynak
        # dosyalar yalnızca gövdeyi içeriyor.
        title = self._language.pick(document.get("title"))
        counter = self._language.t(
            "notes.counter", current=self._current + 1, total=len(self._documents)
        )

        if resolved is None or not resolved.exists():
            body = f"*{self._language.t('content.not_found', path=document.get('file', '-'))}*"
            fallback = False
        else:
            body = resolved.read_text(encoding="utf-8")
            fallback = document.get("_fallback", False)

        self._reader.show_text(f"# {title}\n\n*{counter}*\n\n{body}")
        if fallback:
            pass  # dil geri düşüşü şeridi ders sayfasında gösteriliyor

        for index, button in enumerate(self._buttons):
            button.setProperty("active", "true" if index == self._current else "false")
            repolish(button)

        self.retranslate()

    def _resolve(self, document: dict) -> Path | None:
        """Not dosyasının yolunu seçili dile göre çözer."""
        if self._directory is None:
            return None

        template = document.get("file", "")
        if not template:
            return None

        if "{lang}" in template:
            wanted = self._directory / template.replace("{lang}", self._language.language)
            if wanted.exists():
                document["_fallback"] = False
                return wanted
            document["_fallback"] = True
            return self._directory / template.replace("{lang}", "tr")

        return self._directory / template

    # --- tema ve dil ------------------------------------------------------

    def set_mode(self, mode: str) -> None:
        self._reader.set_mode(mode)

    def retranslate(self) -> None:
        self._list_title.setText(self._language.t("notes.list_title").upper())
        self._previous_button.setText(self._language.t("notes.previous"))
        self._next_button.setText(self._language.t("notes.next"))
        self._previous_button.setEnabled(self._current > 0)
        self._next_button.setEnabled(self._current < len(self._documents) - 1)
        self._reader.retranslate()
