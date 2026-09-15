"""Notlarım: kullanıcının kendi notları.

Solda patikalara göre klasörlenmiş not ağacı, sağda seçili not. Not önce
okuma hâlinde açılıyor (dersler gibi çizilmiş); "Düzenle" ile yazma
hâline geçiliyor.

**Kaydet düğmesi yok.** Yazmayı bırakınca kısa bir süre sonra, başka bir
nota geçince, "Bitti"ye basınca, ekrandan çıkınca ve uygulama kapanırken
kaydediliyor (`flush`). Kaydetmeyi unutup yazdığını kaybetmek, not
defterinde olabilecek en kötü şey.

Okuma hâlindeki çizim ders okuyucusununkinden **daha dar**: içindeki HTML
çalışmıyor, görsel yüklenmiyor, yalnızca http/https bağlantısı kalıyor
(`app/core/user_notes.py`). Not başka birinden de gelebiliyor.
"""

from __future__ import annotations

from datetime import datetime

from PySide6.QtCore import QSize, Qt, QTimer, Signal
from PySide6.QtGui import QFont, QKeySequence, QShortcut, QTextCursor
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMenu,
    QPushButton,
    QStackedWidget,
    QStyleFactory,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from ..core.catalog import Catalog
from ..core.language import LanguageManager
from ..core.progress import ProgressStore
from ..core.user_notes import TITLE_MAX_LENGTH, render_note
from ..resources.icons import icon
from ..resources.theme.tokens import PALETTES, READING_WIDTH, SPACING
from ..widgets.document_view import DocumentView
from ..widgets.note_editor import NoteEditor
from . import titlebar
from .confirm_dialog import ConfirmDialog
from .modal import Backdrop
from .new_note_dialog import NewNoteDialog

SIDE_WIDTH = 300

# Yazmayı bıraktıktan kaç milisaniye sonra kaydedilsin. Her tuşta yazmak
# gereksiz; bir saniyeden uzunu da "kaydetti mi" diye düşündürüyor.
SAVE_DELAY_MS = 700

ROLE_KIND = Qt.ItemDataRole.UserRole
ROLE_ID = Qt.ItemDataRole.UserRole + 1

# Katalogda karşılığı olmayan klasör (başka bir sürümden gelen not gibi).
OTHER_FOLDER = ""

PAGE_EMPTY, PAGE_READ, PAGE_EDIT = 0, 1, 2

TOOLS = ("heading", "bold", "list")


def _format_time(value: str, language: str) -> str:
    try:
        moment = datetime.fromisoformat(value)
    except ValueError:
        return value
    if language == "tr":
        return moment.strftime("%d.%m.%Y %H:%M")
    return moment.strftime("%d %b %Y, %H:%M")


class NotebookView(QWidget):
    """Not ağacı ve seçili not."""

    # "Derse git": notun bağlı olduğu ders açılsın.
    open_section = Signal(str, str)
    # Not eklendi ya da silindi (rozet koşulları buna bakacak).
    changed = Signal()

    def __init__(
        self,
        catalog: Catalog,
        language: LanguageManager,
        store: ProgressStore,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._catalog = catalog
        self._language = language
        self._store = store
        self._mode = "light"

        self._entries: list[dict] = []
        self._current: int | None = None
        self._editing = False
        # Editördeki metin kaydedilenden farklı mı.
        self._dirty = False
        # Editöre program metin yüklerken değişiklik sayılmasın.
        self._loading = False
        self._collapsed: set[str] = set()
        # "Yeni not" hangi klasörü önersin: en son tıklanan klasör ya da not.
        self._folder_hint = ""

        self._save_timer = QTimer(self)
        self._save_timer.setSingleShot(True)
        self._save_timer.setInterval(SAVE_DELAY_MS)
        self._save_timer.timeout.connect(self.flush)

        row = QHBoxLayout(self)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(0)
        row.addWidget(self._build_side())
        row.addWidget(self._build_main(), 1)

        kisayol = QShortcut(QKeySequence("Ctrl+N"), self, self.new_note)
        kisayol.setContext(Qt.ShortcutContext.WidgetWithChildrenShortcut)

        self.retranslate()

    # --- kurulum ----------------------------------------------------------

    def _build_side(self) -> QWidget:
        side = QFrame()
        side.setProperty("role", "notebook-side")
        side.setFixedWidth(SIDE_WIDTH)

        column = QVBoxLayout(side)
        column.setContentsMargins(SPACING["md"], SPACING["md"], SPACING["md"], SPACING["md"])
        column.setSpacing(SPACING["md"])

        self._new_button = QPushButton()
        self._new_button.setProperty("variant", "primary")
        self._new_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._new_button.clicked.connect(self.new_note)
        column.addWidget(self._new_button)

        self._tree = QTreeWidget()
        self._tree.setProperty("role", "notebook-tree")
        self._tree_style = None
        self._apply_tree_style()
        self._tree.setHeaderHidden(True)
        # Açma oku yok: klasöre tıklamak açıp kapatıyor. Qt'nin oku bizim
        # temamızda çizilmiyor, yerine bir şey koymak da kalabalık ediyordu.
        self._tree.setRootIsDecorated(False)
        self._tree.setIndentation(SPACING["lg"])
        self._tree.setIconSize(QSize(18, 18))
        self._tree.itemClicked.connect(self._on_item_clicked)
        self._tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self._tree.customContextMenuRequested.connect(self._tree_menu)
        column.addWidget(self._tree, 1)

        return side

    def _build_main(self) -> QWidget:
        main = QWidget()
        column = QVBoxLayout(main)
        column.setContentsMargins(0, 0, 0, 0)
        column.setSpacing(0)

        # Eylem şeridi: solda notun yeri, sağda düğmeler.
        bar = QWidget()
        bar_row = QHBoxLayout(bar)
        bar_row.setContentsMargins(SPACING["xl"], SPACING["md"], SPACING["xl"], SPACING["sm"])
        bar_row.setSpacing(SPACING["sm"])

        self._crumb = QLabel()
        self._crumb.setProperty("role", "muted")
        bar_row.addWidget(self._crumb)
        bar_row.addStretch(1)

        self._saved = QLabel()
        self._saved.setProperty("role", "muted")
        self._saved.hide()
        bar_row.addWidget(self._saved)

        self._lesson_button = self._bar_button("ghost", self._go_to_lesson)
        self._delete_button = self._bar_button("ghost", self._delete)
        self._edit_button = self._bar_button("primary", self._toggle_edit)
        for button in (self._lesson_button, self._delete_button, self._edit_button):
            bar_row.addWidget(button)
        column.addWidget(bar)

        self._pages = QStackedWidget()

        self._empty = QLabel()
        self._empty.setProperty("role", "muted")
        self._empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._empty.setWordWrap(True)
        self._pages.addWidget(self._empty)

        self._reader = DocumentView()
        self._pages.addWidget(self._reader)

        self._pages.addWidget(self._build_editor())
        column.addWidget(self._pages, 1)
        return main

    def _bar_button(self, variant: str, handler) -> QPushButton:
        button = QPushButton()
        button.setProperty("variant", variant)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.clicked.connect(handler)
        return button

    def _build_editor(self) -> QWidget:
        """Yazma hâli: ad, araç çubuğu, editör — ortada, okuma genişliğinde."""
        page = QWidget()
        outer = QHBoxLayout(page)
        outer.setContentsMargins(SPACING["xl"], SPACING["sm"], SPACING["xl"], SPACING["xl"])
        outer.setSpacing(0)

        column = QWidget()
        column.setMaximumWidth(READING_WIDTH + SPACING["xxl"] * 2)
        inner = QVBoxLayout(column)
        inner.setContentsMargins(0, 0, 0, 0)
        inner.setSpacing(SPACING["sm"])

        self._title_edit = QLineEdit()
        self._title_edit.setProperty("role", "note-title")
        self._title_edit.setMaxLength(TITLE_MAX_LENGTH)
        self._title_edit.textEdited.connect(self._on_edited)
        self._title_edit.editingFinished.connect(self.flush)
        inner.addWidget(self._title_edit)

        tools = QWidget()
        tools.setProperty("role", "bare")
        tools_row = QHBoxLayout(tools)
        tools_row.setContentsMargins(0, SPACING["xs"], 0, SPACING["xs"])
        tools_row.setSpacing(SPACING["xs"])

        self._tool_buttons: dict[str, QPushButton] = {}
        for key in TOOLS:
            button = QPushButton()
            button.setProperty("variant", "tool")
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            tools_row.addWidget(button)
            self._tool_buttons[key] = button

        # Kod düğmesi dil soruyor: Python bloğu renkleniyor, SQL düz duruyor
        # (ders metinlerindeki gibi).
        self._code_button = QPushButton()
        self._code_button.setProperty("variant", "tool")
        self._code_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._code_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self._code_menu = QMenu(self._code_button)
        self._code_python = self._code_menu.addAction("")
        self._code_sql = self._code_menu.addAction("")
        self._code_button.setMenu(self._code_menu)
        tools_row.addWidget(self._code_button)
        tools_row.addStretch(1)
        inner.addWidget(tools)

        self._editor = NoteEditor(mode=self._mode)
        self._editor.textChanged.connect(self._on_edited)
        inner.addWidget(self._editor, 1)

        self._tool_buttons["heading"].clicked.connect(self._editor.toggle_heading)
        self._tool_buttons["bold"].clicked.connect(self._editor.toggle_bold)
        self._tool_buttons["list"].clicked.connect(self._editor.toggle_list)
        self._code_python.triggered.connect(lambda: self._editor.insert_code("python"))
        self._code_sql.triggered.connect(lambda: self._editor.insert_code("sql"))

        outer.addStretch(1)
        outer.addWidget(column, 10)
        outer.addStretch(1)
        return page

    # --- ağaç -------------------------------------------------------------

    def refresh(self) -> None:
        """Notları veritabanından yeniden okur."""
        self._entries = self._store.notebook_entries()
        if self._current is not None and all(e["id"] != self._current for e in self._entries):
            self._current = None
            self._editing = False
        self._rebuild_tree()
        self._show_current()

    def _folders(self) -> list[tuple[str, str, str, str]]:
        """(anahtar, ad, simge, renk) — katalog sırasıyla, sonda "Diğer"."""
        palette = PALETTES.get(self._mode, PALETTES["light"])
        folders = [
            (chapter.id, self._language.pick(chapter.title), chapter.icon, chapter.color)
            for chapter in self._catalog.chapters
            if chapter.sections
        ]
        known = {key for key, *_ in folders}
        if any(e["chapter_id"] not in known for e in self._entries):
            folders.append(
                (OTHER_FOLDER, self._language.t("notebook.other"), "folder", palette["text_muted"])
            )
        return folders

    def _folder_key(self, chapter_id: str) -> str:
        return chapter_id if self._catalog.chapter(chapter_id) is not None else OTHER_FOLDER

    def _rebuild_tree(self) -> None:
        palette = PALETTES.get(self._mode, PALETTES["light"])
        self._tree.clear()

        grouped: dict[str, list[dict]] = {}
        for entry in self._entries:
            grouped.setdefault(self._folder_key(entry["chapter_id"]), []).append(entry)

        for key, title, icon_name, color in self._folders():
            notes = grouped.get(key, [])
            folder = QTreeWidgetItem([f"{title}   {len(notes)}" if notes else title])
            folder.setData(0, ROLE_KIND, "folder")
            folder.setData(0, ROLE_ID, key)
            folder.setIcon(0, icon(icon_name or "folder", color or palette["text_muted"], 18))
            font = folder.font(0)
            font.setWeight(QFont.Weight.DemiBold)
            folder.setFont(0, font)
            self._tree.addTopLevelItem(folder)

            for entry in notes:
                child = QTreeWidgetItem([entry["title"]])
                child.setData(0, ROLE_KIND, "note")
                child.setData(0, ROLE_ID, entry["id"])
                child.setIcon(0, icon("file-text", palette["text_muted"], 16))
                folder.addChild(child)
                if entry["id"] == self._current:
                    self._tree.setCurrentItem(child)

            folder.setExpanded(key not in self._collapsed)

    def _on_item_clicked(self, item: QTreeWidgetItem, _column: int) -> None:
        if item.data(0, ROLE_KIND) == "folder":
            key = item.data(0, ROLE_ID)
            self._folder_hint = key
            item.setExpanded(not item.isExpanded())
            if item.isExpanded():
                self._collapsed.discard(key)
            else:
                self._collapsed.add(key)
            return
        self.open_note(int(item.data(0, ROLE_ID)))

    def _tree_menu(self, position) -> None:
        item = self._tree.itemAt(position)
        if item is None or item.data(0, ROLE_KIND) != "note":
            return
        entry_id = int(item.data(0, ROLE_ID))
        menu = QMenu(self)
        edit = menu.addAction(self._language.t("notebook.edit"))
        delete = menu.addAction(self._language.t("notebook.delete"))
        chosen = menu.exec(self._tree.viewport().mapToGlobal(position))
        if chosen is edit:
            self.open_note(entry_id, edit=True)
        elif chosen is delete:
            self.open_note(entry_id)
            self._delete()

    # --- not --------------------------------------------------------------

    def open_note(self, entry_id: int, edit: bool = False) -> None:
        """Notu açar; önce açık olanın yazılmamış kısmı kaydediliyor."""
        if entry_id == self._current and edit == self._editing:
            return
        self.flush()
        self._current = entry_id
        self._editing = edit
        entry = self._store.notebook_entry(entry_id)
        if entry is not None:
            self._folder_hint = self._folder_key(entry["chapter_id"])
        self._rebuild_tree()
        self._show_current()

    def new_note(self) -> None:
        """"Yeni not": en son bakılan klasör önerilir."""
        self.create_note(self._folder_hint)

    def create_note(self, chapter_id: str = "", section_id: str = "", title: str = "") -> None:
        """Ad soran pencereyi açar; onaylanırsa notu yazma hâlinde açar."""
        self.flush()
        kok = self.window()
        perde = Backdrop(kok)
        perde.show()
        dialog = NewNoteDialog(
            self._catalog, self._language, chapter_id, section_id, title, self._mode, kok
        )
        kabul = dialog.exec()
        perde.deleteLater()
        if not kabul:
            return

        chapter_id, section_id, title = dialog.values()
        self._current = self._store.add_notebook_entry(chapter_id, section_id, title)
        self._editing = True
        self._folder_hint = chapter_id
        self._collapsed.discard(chapter_id)
        self.refresh()
        self.changed.emit()

    def _entry(self) -> dict | None:
        if self._current is None:
            return None
        return self._store.notebook_entry(self._current)

    def _show_current(self) -> None:
        entry = self._entry()
        t = self._language.t

        for button in (self._edit_button, self._delete_button):
            button.setVisible(entry is not None)
        self._saved.hide()

        if entry is None:
            self._crumb.setText("")
            self._lesson_button.hide()
            self._empty.setText(t("notebook.empty") if self._entries else t("notebook.first"))
            self._pages.setCurrentIndex(PAGE_EMPTY)
            return

        self._update_bar(entry)
        if self._editing:
            self._loading = True
            self._title_edit.setText(entry["title"])
            self._editor.setPlainText(entry["body"])
            self._loading = False
            self._dirty = False
            self._pages.setCurrentIndex(PAGE_EDIT)
            self._editor.setFocus()
            self._editor.moveCursor(QTextCursor.MoveOperation.End)
        else:
            self._render_reader(entry)
            self._pages.setCurrentIndex(PAGE_READ)

    def _update_bar(self, entry: dict) -> None:
        """Eylem şeridinin metinleri. Editördeki metne dokunmuyor."""
        t = self._language.t
        chapter = self._catalog.chapter(entry["chapter_id"])
        section = (
            self._catalog.section(entry["chapter_id"], entry["section_id"])
            if entry["section_id"]
            else None
        )
        yer = [self._language.pick(chapter.title) if chapter else t("notebook.other")]
        if section is not None:
            yer.append(self._language.pick(section.title))
        self._crumb.setText("  ›  ".join(yer))

        self._lesson_button.setVisible(section is not None)
        self._lesson_button.setText(t("notebook.go_to_lesson"))
        self._delete_button.setText(t("notebook.delete"))
        self._edit_button.setText(t("notebook.done") if self._editing else t("notebook.edit"))

    def _render_reader(self, entry: dict) -> None:
        t = self._language.t
        body = entry["body"] if entry["body"].strip() else f"*{t('notebook.empty_body')}*"
        meta = [t("notebook.updated", date=_format_time(entry["updated_at"], self._language.language))]
        content = render_note(entry["title"], body, meta)
        self._reader.set_lang(self._language.language)
        self._reader.set_body(
            f'<div class="page narrow notebook"><div class="content">{content}</div></div>'
        )

    # --- yazma ------------------------------------------------------------

    def _toggle_edit(self) -> None:
        if self._editing:
            self.flush()
            self._editing = False
        else:
            self._editing = True
        self._show_current()

    def _on_edited(self, *_args) -> None:
        if self._loading or not self._editing:
            return
        self._dirty = True
        self._saved.hide()
        self._save_timer.start()

    def flush(self) -> None:
        """Yazılmamış değişikliği kaydeder. Değişiklik yoksa bir şey yapmıyor."""
        self._save_timer.stop()
        if not self._dirty or not self._editing or self._current is None:
            return
        self._dirty = False

        entry = self._entry()
        if entry is None:
            return
        istenen = self._title_edit.text().strip()
        son_ad = self._store.update_notebook_entry(
            self._current, title=istenen or None, body=self._editor.toPlainText()
        )
        if son_ad is None:
            return

        # Ad boş bırakıldıysa eski ad, çakıştıysa sayılı hâli geri yazılıyor.
        if son_ad != self._title_edit.text():
            self._title_edit.setText(son_ad)
        if son_ad != entry["title"]:
            self._entries = self._store.notebook_entries()
            self._rebuild_tree()

        self._saved.setText(self._language.t("notebook.saved"))
        self._saved.show()

    def _go_to_lesson(self) -> None:
        entry = self._entry()
        if entry is None or not entry["section_id"]:
            return
        self.flush()
        self.open_section.emit(entry["chapter_id"], entry["section_id"])

    def _delete(self) -> None:
        entry = self._entry()
        if entry is None:
            return
        t = self._language.t
        dialog = ConfirmDialog(
            t("notebook.delete_title"),
            t("notebook.delete_message", title=entry["title"]),
            t("notebook.delete"),
            t("common.cancel"),
            self.window(),
        )
        titlebar.apply(dialog, self._mode)
        if dialog.exec() != ConfirmDialog.DialogCode.Accepted:
            return

        self._save_timer.stop()
        self._dirty = False
        self._store.delete_notebook_entry(entry["id"])
        self._current = None
        self._editing = False
        self.refresh()
        self.changed.emit()

    def hideEvent(self, event) -> None:  # noqa: N802
        # Ekrandan çıkılıyor: yazılan son harfler de kaydedilsin.
        self.flush()
        super().hideEvent(event)

    def warm_up(self) -> None:
        """Belge alanını bir kez çizdirir (bkz. `MainWindow.warm_up`)."""
        from PySide6.QtWidgets import QApplication

        onceki = self._pages.currentIndex()
        self._reader.set_body('<div class="page narrow notebook"></div>')
        self._pages.setCurrentIndex(PAGE_READ)
        QApplication.processEvents()
        self._pages.setCurrentIndex(onceki)

    # --- tema ve dil ------------------------------------------------------

    def _apply_tree_style(self) -> None:
        """Ağacı Fusion ile çizdirir.

        Windows 11 stili seçili satırın soluna kendi vurgu işaretini
        çiziyor; QSS onu kapatamıyor ve işaret girinti boşluğunda, notun
        yanında öksüz bir çizgi gibi kalıyordu. Görünümün geri kalanı zaten
        QSS'ten geliyor.

        **Her tema değişiminde yeniden veriliyor.** Tema, uygulamanın stil
        dosyasını boşaltıp yeniden veriyor; kendi stili olan widget'a yeni
        stil dosyası sarılmıyor ve ağaç açık temaya geçince çıplak Fusion
        görünümünde kalıyordu (kenarlık, mavi seçim — ekran görüntüsünde
        görüldü). Stil ağaca bağlanıyor, yoksa Python onu silip ağacı ölü
        bir stile bakar hâlde bırakır.
        """
        eski = self._tree_style
        self._tree_style = QStyleFactory.create("Fusion")
        self._tree_style.setParent(self._tree)
        self._tree.setStyle(self._tree_style)
        if eski is not None:
            eski.deleteLater()

    def set_mode(self, mode: str) -> None:
        self._mode = mode
        self._apply_tree_style()
        self._reader.set_mode(mode)
        self._editor.set_mode(mode)
        self._rebuild_tree()

    def retranslate(self) -> None:
        t = self._language.t
        self._new_button.setText(f"+  {t('notebook.new')}")
        self._new_button.setToolTip("Ctrl+N")
        self._title_edit.setPlaceholderText(t("notebook.title_placeholder"))
        self._editor.setPlaceholderText(t("notebook.body_placeholder"))
        for key, button in self._tool_buttons.items():
            button.setText(t(f"notebook.{key}"))
        self._tool_buttons["bold"].setToolTip("Ctrl+B")
        self._code_button.setText(f"{t('notebook.code')}  ▾")
        self._code_python.setText(t("notebook.code_python"))
        self._code_sql.setText(t("notebook.code_sql"))

        # Klasör adları ve "Diğer" dile bağlı. Yazma hâlinde editör yeniden
        # yüklenmiyor: yüklenseydi kaydedilmemiş son harfler giderdi.
        self._rebuild_tree()
        entry = self._entry()
        if entry is not None and self._editing:
            self._update_bar(entry)
        else:
            self._show_current()
