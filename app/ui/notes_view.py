"""Ders notları görünümü.

Notlar PDF olarak gömülmüyor, metin olarak gösteriliyor. Sebepleri:
uygulama içinde aranabiliyor, kopyalanabiliyor, yazı boyutu kullanıcının
ayarına uyuyor ve açık/koyu temayla uyumlu duruyor. Gömülü bir PDF bunların
hiçbirini yapamıyor.

**Not seçimi metnin üstünde, kenarda değil.** Önce solda 270px'lik dolu bir
liste paneli vardı. Bir bölümde en çok üç, çoğunlukla iki not olduğu için o
panel hem gereğinden ağır duruyor hem de metni sağa itip ortalamayı
bozuyordu. Şimdi notlar üstte ince bir sekme sırası; tek not varsa sıra hiç
çizilmiyor ve ekranda yalnızca metin kalıyor.
"""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget

from ..core.catalog import Block
from ..core.language import LanguageManager
from ..resources.theme.tokens import READING_WIDTH, SPACING
from ..widgets.common import SegmentedControl
from .lesson_view import LessonView


class NotesView(QWidget):
    """Bir bölümün ders notları."""

    # Son notun sonundaki düğmeye basıldığında yayılır; bölümdeki bir sonraki
    # adıma (sınav ya da alıştırma) geçilmesi isteniyor demektir.
    advance = Signal()

    def __init__(self, language: LanguageManager, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._language = language
        self._documents: list[dict] = []
        self._directory: Path | None = None
        self._current = 0
        # Son notun altında görünecek "devam et" düğmesinin etiketi. Bölümde
        # notlardan sonra ne geliyorsa (sınav, alıştırma) onun adı yazılıyor.
        self._advance_label: str | None = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addWidget(self._build_selector())

        self._reader = LessonView(self._language, show_toc=False)
        self._reader.action.connect(self._on_action)
        layout.addWidget(self._reader, 1)

        self._empty = QLabel()
        self._empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._empty.setProperty("role", "muted")
        layout.addWidget(self._empty)
        self._empty.hide()

    def _build_selector(self) -> QWidget:
        """Notlar arasında geçiş sırası.

        Genişlik `READING_WIDTH`: belgenin kendi metin sütunu bu ölçüyü
        kullanıyor. `CONTENT_WIDTH` (820px) verilseydi sekmeler metinden
        70 piksel solda başlıyordu — ölçüldü.
        """
        holder = QWidget()
        row = QHBoxLayout(holder)
        row.setContentsMargins(
            SPACING["xl"], SPACING["md"], SPACING["xl"], 0
        )
        row.setSpacing(0)

        inner = QWidget()
        inner.setMaximumWidth(READING_WIDTH)
        column = QHBoxLayout(inner)
        column.setContentsMargins(0, 0, 0, 0)
        column.setSpacing(0)

        self._tabs = SegmentedControl()
        self._tabs.changed.connect(self._select)
        column.addWidget(self._tabs)
        column.addStretch(1)

        row.addStretch(1)
        row.addWidget(inner, 10)
        row.addStretch(1)

        self._selector = holder
        return holder

    def _on_action(self, action: str) -> None:
        if action == "next":
            self._step(1)
        elif action == "previous":
            self._step(-1)
        elif action == "advance":
            self.advance.emit()

    def set_advance_label(self, label: str | None) -> None:
        """Son notun sonunda görünecek "devam et" düğmesinin adını belirler.

        `None` verilirse düğme çizilmiyor; bölümde notlardan sonra bir adım
        yoksa kullanıcıyı boşluğa yollamanın anlamı yok.
        """
        self._advance_label = label
        if self._documents:
            self._apply_footer()

    def _apply_footer(self) -> None:
        """Not okuyucusunun altındaki gezinme düğmeleri.

        Notlar arasında ileri geri gezilir; **son notta** ileri düğmesi
        bölümün bir sonraki adımına (sınav ya da alıştırma) dönüşür. Böylece
        okuyan kişi ders notunu bitirdiğinde yukarı çıkmak zorunda kalmadan
        devam edebiliyor.
        """
        son_not = self._current >= len(self._documents) - 1

        if son_not and self._advance_label:
            ileri = ("advance", f"{self._advance_label}  →", True)
        elif son_not:
            ileri = ("", "", True)
        else:
            ileri = ("next", f"{self._language.t('notes.next')}  →", True)

        # Oklar gideceği yönü gösteriyor: geri sola, ileri sağa.
        self._reader.set_footer(
            [
                (
                    "previous" if self._current > 0 else "",
                    f"←  {self._language.t('notes.previous')}",
                    False,
                ),
                ileri,
            ]
        )

    # --- içerik -----------------------------------------------------------

    def show_notes(self, block: Block) -> None:
        """Blok içindeki not listesini kurar."""
        self._documents = block.documents
        self._directory = block.directory
        self._current = 0
        self._rebuild_tabs()
        self._show_current()

    def _rebuild_tabs(self) -> None:
        """Sekmeleri kurar. Tek not varsa sıra hiç görünmüyor."""
        basliklar = [
            self._language.pick(document.get("title")) for document in self._documents
        ]
        self._tabs.set_items(basliklar)
        self._tabs.set_current(self._current, notify=False)
        self._selector.setVisible(len(self._documents) > 1)

    def _select(self, index: int) -> None:
        self._current = max(0, min(index, len(self._documents) - 1))
        self._tabs.set_current(self._current, notify=False)
        self._show_current()

    def _step(self, delta: int) -> None:
        self._select(self._current + delta)

    def _show_current(self) -> None:
        has_notes = bool(self._documents)
        self._reader.setVisible(has_notes)
        self._selector.setVisible(has_notes and len(self._documents) > 1)
        self._empty.setVisible(not has_notes)

        if not has_notes:
            self._empty.setText(self._language.t("notes.empty"))
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
        else:
            body = resolved.read_text(encoding="utf-8")

        self._reader.show_text(f"# {title}\n\n{body}")
        self._reader.set_meta([counter])
        self._apply_footer()

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
        self._rebuild_tabs()
        if self._documents:
            self._show_current()
        self._reader.retranslate()
