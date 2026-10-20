"""Bölüm ekranının sağındaki not paneli.

Not almanın asıl anı dersi okurken; Notlarım ekranına gidip gelmek o anı
kaçırıyordu. Panel ders ekranda dururken yanında açılıyor. Notlar
Notlarım'dakilerle aynı yerde (`notebook_entries`) ve o patikanın
klasöründe duruyor, bu derse bağlı olarak.

**Boş not yazılmıyor.** Paneli açmak not oluşturmuyor: bu derse bağlı
notun yoksa panel bölümün adıyla boş bir sayfa gösteriyor, kayıt ancak
ilk harf yazılınca açılıyor. Yoksa merakla açılan her panel Notlarım'da
boş bir not bırakırdı.

Bu derse birden fazla not varsa üstteki kutudan aralarında geçiliyor;
"+" bu derse yeni bir not açıyor. Kaydetme Notlarım'daki gibi
kendiliğinden (`flush`).

**Bütün notlar da buradan açılıyor** (Alican 13 Ekim: alıştırmada takılan
kişi bölümü kapatmadan başka bir notuna bakıp karşılaştırabilsin).
Başlıktaki kitaplık düğmesi aramalı bir liste açıyor: önce bu dersin
notları, sonra en son değişenler. Seçilen not panelde açılıyor ve
düzenlenebiliyor; "Bu dersin notu" bölümün notuna geri götürüyor.
"""

from __future__ import annotations

from typing import Callable

from PySide6.QtCore import QRect, QSize, Qt, QTimer, Signal
from PySide6.QtGui import QColor, QFont, QPainter, QTextCursor
from PySide6.QtWidgets import (
    QFrame, QHBoxLayout, QLabel, QLineEdit, QListWidget, QListWidgetItem, QPushButton,
    QSizePolicy, QStackedWidget, QStyle, QStyledItemDelegate, QVBoxLayout, QWidget,
)

from ..core.catalog import Catalog
from ..core.language import LanguageManager
from ..core.progress import ProgressStore
from ..core.search import fold
from ..core.user_notes import TITLE_MAX_LENGTH
from ..resources.icons import icon, pixmap
from ..resources.theme.tokens import PALETTES, RAIL_COLORS, SPACING
from ..widgets.common import DropdownBox
from ..widgets.note_editor import NoteEditor
from ..widgets.note_toolbar import NoteToolbar, make_tool_button

PANEL_WIDTH = 360
SAVE_DELAY_MS = 700

# Kutudaki "henüz kaydedilmemiş yeni not" satırının verisi.
UNSAVED = -1

# Panelin iki sayfası.
PAGE_EDIT = 0
PAGE_BROWSE = 1

# Tüm notlar listesi: satırın verisi notun id'si, ikinci satırı nereye ait olduğu.
ROLE_ID = Qt.ItemDataRole.UserRole
ROLE_WHERE = Qt.ItemDataRole.UserRole + 1
ROW_HEIGHT = 50


class NoteRow(QStyledItemDelegate):
    """Tüm notlar listesinin satırı: notun adı, altında klasörü ya da dersi.

    Hızlı başvuru çekmecesi de kullanıyor (bölümün adı, altında modülü).
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.palette = PALETTES["light"]

    def sizeHint(self, option, index) -> QSize:  # noqa: N802
        return QSize(option.rect.width(), ROW_HEIGHT)

    def paint(self, painter: QPainter, option, index) -> None:
        p = self.palette
        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        if option.state & (QStyle.StateFlag.State_MouseOver | QStyle.StateFlag.State_Selected):
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QColor(p["surface_hover"]))
            painter.drawRoundedRect(option.rect.adjusted(0, 2, 0, -2), 9, 9)

        alan = option.rect.adjusted(12, 7, -12, -7)
        satir = alan.height() // 2
        for metin, boyut, kalin, renk, ust in (
            (index.data(Qt.ItemDataRole.DisplayRole), 13, True, p["text"], alan.top()),
            (index.data(ROLE_WHERE), 12, False, p["text_muted"], alan.top() + satir),
        ):
            font = QFont(option.font)
            font.setPixelSize(boyut)
            if kalin:
                font.setWeight(QFont.Weight.DemiBold)
            painter.setFont(font)
            painter.setPen(QColor(renk))
            kisa = painter.fontMetrics().elidedText(metin or "", Qt.TextElideMode.ElideRight, alan.width())
            painter.drawText(QRect(alan.left(), ust, alan.width(), satir),
                             Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, kisa)
        painter.restore()


class NotePanel(QFrame):
    """Açık bölüme bağlı notlar; istenirse bütün notlar."""

    # "Notlarım'da aç": notun id'si.
    open_in_notebook = Signal(int)
    close_requested = Signal()
    # Yeni bir not kaydedildi.
    changed = Signal()

    def __init__(
        self,
        language: LanguageManager,
        store: ProgressStore,
        catalog: Catalog,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._language = language
        self._store = store
        self._catalog = catalog
        self._mode = "light"

        self._chapter_id = ""
        self._section_id = ""
        self._section_title = ""
        self._entries: list[dict] = []
        # Açık notun id'si; `None` henüz kaydedilmemiş yeni not.
        self._current: int | None = None
        # Açık not bu derse değil başka bir yere ait (listeden açıldı).
        self._foreign = False
        self._dirty = False
        self._loading = False
        # Tüm notlar listesi açılırken okunuyor: (not, aranacak metin).
        self._browse: list[tuple[dict, str]] = []
        # Açık alıştırmanın kodunu veren fonksiyon; alıştırmada değilken yok.
        self._code_source: Callable[[], tuple[str, str] | None] | None = None

        self.setProperty("role", "note-panel")
        self.setFixedWidth(PANEL_WIDTH)

        self._save_timer = QTimer(self)
        self._save_timer.setSingleShot(True)
        self._save_timer.setInterval(SAVE_DELAY_MS)
        self._save_timer.timeout.connect(self.flush)

        dis = QVBoxLayout(self)
        dis.setContentsMargins(0, 0, 0, 0)
        dis.setSpacing(0)

        # Başlık (prototip `.drawer header`): not simgesi, "Not al", bölümün
        # adı, tüm notlar, yeni not ve kapat; altında ince çizgi.
        ust = QFrame()
        ust.setProperty("role", "drawer-head")
        top = QHBoxLayout(ust)
        top.setContentsMargins(16, 12, 10, 12)
        top.setSpacing(8)
        self._head_icon = QLabel()
        self._head_icon.setFixedSize(18, 18)
        top.addWidget(self._head_icon)
        self._heading = QLabel()
        self._heading.setProperty("role", "drawer-title")
        top.addWidget(self._heading)
        self._section_label = QLabel()
        self._section_label.setProperty("role", "drawer-sub")
        self._section_label.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred)
        top.addWidget(self._section_label, 1)
        self._browse_button = self._small_button("", self._toggle_browse)
        self._new_button = self._small_button("", self._new_note)
        self._close_button = self._small_button("", self.close_requested.emit)
        top.addWidget(self._browse_button)
        top.addWidget(self._new_button)
        top.addWidget(self._close_button)
        dis.addWidget(ust)

        self._pages = QStackedWidget()
        self._pages.setProperty("role", "bare")
        self._pages.addWidget(self._build_edit_page())
        self._pages.addWidget(self._build_browse_page())
        dis.addWidget(self._pages, 1)

        # Alt şerit (prototip `.drawer footer`): "Kaydedildi" ve Notlarım düğmesi.
        alt = QFrame()
        alt.setProperty("role", "drawer-foot")
        bottom = QHBoxLayout(alt)
        bottom.setContentsMargins(14, 10, 12, 10)
        bottom.setSpacing(6)
        self._saved_icon = QLabel()
        self._saved_icon.setFixedSize(14, 14)
        self._saved_icon.hide()
        bottom.addWidget(self._saved_icon)
        self._saved = QLabel()
        self._saved.setProperty("role", "drawer-saved")
        self._saved.hide()
        bottom.addWidget(self._saved)
        bottom.addStretch(1)
        self._open_button = QPushButton()
        self._open_button.setProperty("variant", "primary")
        self._open_button.setProperty("size", "sm")
        self._open_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._open_button.clicked.connect(self._open_in_notebook)
        bottom.addWidget(self._open_button)
        dis.addWidget(alt)

        self.retranslate()

    def _build_edit_page(self) -> QWidget:
        govde = QWidget()
        govde.setProperty("role", "bare")
        layout = QVBoxLayout(govde)
        layout.setContentsMargins(14, 12, 14, 8)
        layout.setSpacing(SPACING["sm"])

        # Listeden başka bir not açıldıysa bölümün notuna dönüş.
        self._back_button = QPushButton()
        self._back_button.setProperty("variant", "ghost")
        self._back_button.setProperty("size", "sm")
        self._back_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._back_button.clicked.connect(self._back_to_lesson)
        self._back_button.hide()
        layout.addWidget(self._back_button, 0, Qt.AlignmentFlag.AlignLeft)

        self._picker = DropdownBox()
        self._picker.currentIndexChanged.connect(self._on_pick)
        self._picker.hide()
        layout.addWidget(self._picker)

        self._title_edit = QLineEdit()
        self._title_edit.setProperty("role", "note-title")
        self._title_edit.setProperty("compact", "true")
        self._title_edit.setMaxLength(TITLE_MAX_LENGTH)
        self._title_edit.textEdited.connect(self._on_edited)
        self._title_edit.editingFinished.connect(self.flush)
        layout.addWidget(self._title_edit)

        self._editor = NoteEditor(mode=self._mode)
        self._editor.setProperty("drawer", "true")
        self._editor.textChanged.connect(self._on_edited)

        self._toolbar = NoteToolbar(self._editor)
        self._code_button = make_tool_button()
        self._code_button.clicked.connect(self._add_own_code)
        self._code_button.hide()
        self._toolbar.add_button(self._code_button)
        layout.addWidget(self._toolbar)
        layout.addWidget(self._editor, 1)
        return govde

    def _build_browse_page(self) -> QWidget:
        govde = QWidget()
        govde.setProperty("role", "bare")
        layout = QVBoxLayout(govde)
        layout.setContentsMargins(14, 12, 14, 8)
        layout.setSpacing(SPACING["sm"])

        self._search = QLineEdit()
        self._search.setClearButtonEnabled(True)
        self._search.textChanged.connect(self._fill_list)
        self._search.returnPressed.connect(self._open_first)
        layout.addWidget(self._search)

        self._list = QListWidget()
        self._list.setProperty("role", "search-results")
        self._row = NoteRow(self._list)
        self._list.setItemDelegate(self._row)
        self._list.setUniformItemSizes(True)
        self._list.setMouseTracking(True)
        self._list.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._list.itemClicked.connect(lambda item: self._open_entry(item.data(ROLE_ID)))
        layout.addWidget(self._list, 1)

        self._list_empty = QLabel()
        self._list_empty.setProperty("role", "drawer-sub")
        self._list_empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._list_empty.setWordWrap(True)
        self._list_empty.hide()
        layout.addWidget(self._list_empty)
        return govde

    def _small_button(self, text: str, handler) -> QPushButton:
        button = QPushButton(text)
        button.setProperty("variant", "round")
        button.setFixedSize(28, 28)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.clicked.connect(handler)
        return button

    # --- bölüm ------------------------------------------------------------

    def set_section(self, chapter_id: str, section_id: str, section_title: str) -> None:
        """Açık bölüm değişti: önceki notun son harfleri kaydedilip yenisi yükleniyor."""
        self.flush()
        self._chapter_id = chapter_id
        self._section_id = section_id
        self._section_title = section_title
        self._load()

    def set_section_title(self, section_title: str) -> None:
        """Dil değişince bölümün adı değişiyor; kaydedilmemiş boş notun adı da."""
        eski = self._section_title
        self._section_title = section_title
        self._update_label()
        if self._current is None and self._title_edit.text() in ("", eski):
            self._loading = True
            self._title_edit.setText(section_title)
            self._loading = False

    def reload(self) -> None:
        """Notlar başka yerde değişmiş olabilir (Notlarım); yeniden okur."""
        self.flush()
        self._load(keep=self._current)

    def _section_entries(self) -> list[dict]:
        return [
            entry
            for entry in self._store.notebook_entries()
            if entry["chapter_id"] == self._chapter_id and entry["section_id"] == self._section_id
        ]

    def _load(self, keep: int | None = None) -> None:
        self._entries = self._section_entries()
        ids = [entry["id"] for entry in self._entries]
        if keep in ids:
            secilen = keep
        elif self._entries:
            # Birden fazla not varsa en son üzerinde çalışılan açılıyor.
            secilen = max(self._entries, key=lambda e: e["updated_at"])["id"]
        else:
            secilen = None
        self._show(secilen)

    def _show(self, entry_id: int | None) -> None:
        self._current = entry_id
        entry = self._store.notebook_entry(entry_id) if entry_id is not None else None
        if entry is None:
            self._current = None
        self._foreign = self._current is not None and all(
            e["id"] != self._current for e in self._entries
        )

        self._loading = True
        self._title_edit.setText(entry["title"] if entry else self._section_title)
        self._editor.setPlainText(entry["body"] if entry else "")
        self._loading = False
        self._dirty = False
        self._saved.hide()
        self._saved_icon.hide()
        self._open_button.setEnabled(self._current is not None)
        self._back_button.setVisible(self._foreign)
        self._update_label()
        self._rebuild_picker()
        self._pages.setCurrentIndex(PAGE_EDIT)

    def _update_label(self) -> None:
        """Başlıktaki ikinci yazı: bölümün adı, başka bir not açıksa onun yeri."""
        entry = self._store.notebook_entry(self._current) if self._foreign else None
        self._section_label.setText(self._where(entry, self._folder_names()) if entry else self._section_title)

    def _rebuild_picker(self) -> None:
        """Bu dersin notları arasında geçiş kutusu; tek not varsa ya da başka
        bir not açıksa gizli."""
        self._picker.blockSignals(True)
        self._picker.clear()
        for entry in self._entries:
            self._picker.addItem(entry["title"], entry["id"])
        if self._current is None and self._entries:
            self._picker.addItem(self._language.t("notebook.new"), UNSAVED)
        index = self._picker.findData(UNSAVED if self._current is None else self._current)
        self._picker.setCurrentIndex(max(index, 0))
        self._picker.blockSignals(False)
        self._picker.setVisible(not self._foreign and self._picker.count() > 1)

    def _on_pick(self, index: int) -> None:
        data = self._picker.itemData(index)
        hedef = None if data == UNSAVED else data
        if hedef == self._current:
            return
        self.flush()
        self._show(hedef)

    def _new_note(self) -> None:
        """Bu derse yeni not. Kayıt yine ilk harfte açılıyor."""
        self.flush()
        self._show(None)
        self._editor.setFocus()

    def _back_to_lesson(self) -> None:
        self.flush()
        self._load()
        self._editor.setFocus()

    # --- tüm notlar -------------------------------------------------------

    def _toggle_browse(self) -> None:
        if self._pages.currentIndex() == PAGE_BROWSE:
            self._pages.setCurrentIndex(PAGE_EDIT)
            return
        self.flush()
        self._read_all()
        self._search.blockSignals(True)
        self._search.clear()
        self._search.blockSignals(False)
        self._fill_list()
        self._pages.setCurrentIndex(PAGE_BROWSE)
        self._search.setFocus()

    def _read_all(self) -> None:
        """Bütün notlar: önce bu dersinkiler, sonra en son değişen üstte."""
        notlar = sorted(self._store.notebook_entries_with_body(),
                        key=lambda e: (e["updated_at"], e["id"]), reverse=True)
        notlar.sort(key=lambda e: (e["chapter_id"], e["section_id"]) != (self._chapter_id, self._section_id))
        klasorler = self._folder_names()
        self._browse = []
        for entry in notlar:
            where = self._where(entry, klasorler)
            self._browse.append((dict(entry, where=where), fold(f"{entry['title']} {where} {entry['body']}")))

    def _folder_names(self) -> dict[int, str]:
        return {folder["id"]: folder["name"] for folder in self._store.notebook_folders()}

    def _where(self, entry: dict, folders: dict[int, str]) -> str:
        """Notun yeri: bu ders, kendi klasörü, bağlı olduğu ders ya da patika."""
        if (entry["chapter_id"], entry["section_id"]) == (self._chapter_id, self._section_id):
            return self._language.t("notebook.this_lesson")
        if entry.get("folder_id") in folders:
            return folders[entry["folder_id"]]
        section = self._catalog.section(entry["chapter_id"], entry["section_id"]) if entry["section_id"] else None
        if section is not None:
            return self._language.pick(section.title)
        chapter = self._catalog.chapter(entry["chapter_id"])
        return self._language.pick(chapter.title) if chapter else self._language.t("notebook.other")

    def _fill_list(self) -> None:
        kelimeler = fold(self._search.text()).split()
        self._list.clear()
        for entry, metin in self._browse:
            if all(kelime in metin for kelime in kelimeler):
                item = QListWidgetItem(entry["title"])
                item.setData(ROLE_ID, entry["id"])
                item.setData(ROLE_WHERE, entry["where"])
                item.setToolTip(entry["title"])
                self._list.addItem(item)
        bos = self._list.count() == 0
        self._list_empty.setText(self._language.t(
            "notebook.no_match" if self._browse else "notebook.first_title"))
        self._list_empty.setVisible(bos)
        self._list.setVisible(not bos)

    def _open_first(self) -> None:
        if self._list.count():
            self._open_entry(self._list.item(0).data(ROLE_ID))

    def _open_entry(self, entry_id: int) -> None:
        self.flush()
        self._show(entry_id)
        self._editor.setFocus()

    # --- yazma ------------------------------------------------------------

    def _on_edited(self, *_args) -> None:
        if self._loading:
            return
        self._dirty = True
        self._saved.hide()
        self._saved_icon.hide()
        self._save_timer.start()

    def flush(self) -> None:
        """Yazılmamış değişikliği kaydeder; boş yeni not kaydedilmiyor."""
        self._save_timer.stop()
        if not self._dirty or not self._chapter_id:
            return
        self._dirty = False

        body = self._editor.toPlainText()
        title = self._title_edit.text().strip() or self._section_title

        son_ad = None
        if self._current is not None:
            onceki = self._store.notebook_entry(self._current)
            son_ad = self._store.update_notebook_entry(self._current, title=title, body=body)
            # Boş not ilk kez yazıya döndü (Notlarım'da açılıp burada
            # yazılan not): rozet koşulu bunu bekliyor.
            if onceki is not None and not onceki["body"].strip() and body.strip():
                self.changed.emit()
            if son_ad is None:
                # Not bu arada Notlarım'da silinmiş: yazılan kaybolmasın,
                # yeni not olarak kaydediliyor.
                self._current = None
                self._foreign = False
                self._back_button.hide()

        if self._current is None:
            if not body.strip():
                return
            self._current = self._store.add_notebook_entry(
                self._chapter_id, self._section_id, title, body
            )
            son_ad = self._store.notebook_entry(self._current)["title"]
            self.changed.emit()

        if son_ad is not None and son_ad != self._title_edit.text():
            self._loading = True
            self._title_edit.setText(son_ad)
            self._loading = False

        self._entries = self._section_entries()
        self._update_label()
        self._rebuild_picker()
        self._open_button.setEnabled(True)
        self._saved.setText(self._language.t("notebook.saved"))
        self._saved.show()
        self._saved_icon.show()

    def _append(self, block: str) -> None:
        """Notun sonuna bir blok ekler, arasında boş satır bırakarak."""
        self._pages.setCurrentIndex(PAGE_EDIT)
        mevcut = self._editor.toPlainText()
        if not mevcut.strip():
            ayrac = ""
        elif mevcut.endswith("\n\n"):
            ayrac = ""
        elif mevcut.endswith("\n"):
            ayrac = "\n"
        else:
            ayrac = "\n\n"
        self._editor.moveCursor(QTextCursor.MoveOperation.End)
        self._editor.insertPlainText(f"{ayrac}{block}\n")
        self._editor.moveCursor(QTextCursor.MoveOperation.End)
        self._editor.ensureCursorVisible()
        self._editor.setFocus()

    def add_quote(self, text: str) -> None:
        """Dersten seçilen metni alıntı olarak ekler."""
        satirlar = [line.rstrip() for line in text.strip().splitlines()]
        if not satirlar:
            return
        self._append("\n".join(f"> {line}" if line else ">" for line in satirlar))

    def add_code(self, code: str, language: str) -> None:
        """Kodu kod bloğu olarak ekler."""
        if code.strip():
            self._append(f"```{language}\n{code.rstrip()}\n```")

    def set_code_source(self, source: Callable[[], tuple[str, str] | None] | None) -> None:
        """Alıştırma sekmesindeyken "Kodumu ekle" düğmesi görünüyor."""
        self._code_source = source
        self._code_button.setVisible(source is not None)

    def _add_own_code(self) -> None:
        if self._code_source is None:
            return
        sonuc = self._code_source()
        if sonuc:
            self.add_code(*sonuc)

    def _open_in_notebook(self) -> None:
        self.flush()
        if self._current is not None:
            self.open_in_notebook.emit(self._current)

    def focus_editor(self) -> None:
        """Panel açılınca imleç notta; liste açık kalmışsa nota dönülüyor."""
        self._pages.setCurrentIndex(PAGE_EDIT)
        self._editor.setFocus()
        self._editor.moveCursor(QTextCursor.MoveOperation.End)

    def hideEvent(self, event) -> None:  # noqa: N802
        self.flush()
        super().hideEvent(event)

    # --- tema ve dil ------------------------------------------------------

    def set_mode(self, mode: str) -> None:
        self._mode = mode
        p = PALETTES.get(mode, PALETTES["light"])
        yesil = RAIL_COLORS.get(mode, RAIL_COLORS["light"])["notes"]
        self._head_icon.setPixmap(pixmap("notebook", yesil, 18))
        self._browse_button.setIcon(icon("library", p["text_muted"], 15))
        self._new_button.setIcon(icon("plus", p["text_muted"], 15))
        self._close_button.setIcon(icon("x", p["text_muted"], 15))
        self._back_button.setIcon(icon("arrow-left", p["text_muted"], 14))
        self._saved_icon.setPixmap(pixmap("check", p["success"], 14))
        self._editor.set_mode(mode)
        self._picker.set_arrow_color(p["text_muted"])
        self._row.palette = p
        self._list.viewport().update()

    def retranslate(self) -> None:
        t = self._language.t
        self._heading.setText(t("notebook.take_note"))
        self._browse_button.setToolTip(t("notebook.all_notes"))
        self._new_button.setToolTip(t("notebook.new_for_lesson"))
        self._close_button.setToolTip(t("common.close"))
        self._back_button.setText(t("notebook.back_to_lesson_note"))
        self._title_edit.setPlaceholderText(t("notebook.title_placeholder"))
        self._editor.setPlaceholderText(t("notebook.panel_hint"))
        self._search.setPlaceholderText(t("notebook.search_notes"))
        self._toolbar.retranslate(t)
        self._code_button.setText(t("notebook.add_code"))
        self._open_button.setText(t("notebook.open_in_notebook"))
        if self._current is None and self._entries:
            self._rebuild_picker()
        if self._foreign:
            self._update_label()
        if self._pages.currentIndex() == PAGE_BROWSE:
            # Satırların ikinci yazısı (ders ve patika adları) dile bağlı.
            self._read_all()
            self._fill_list()
