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

import zipfile
from datetime import datetime
from pathlib import Path

from PySide6.QtCore import QPoint, QSize, QStandardPaths, Qt, QTimer, Signal
from PySide6.QtGui import QFont, QKeySequence, QShortcut, QTextCursor
from PySide6.QtWidgets import (
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMenu,
    QPushButton,
    QStackedWidget,
    QStyledItemDelegate,
    QStyleFactory,
    QStyleOptionViewItem,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from ..core.catalog import Catalog
from ..core.language import LanguageManager
from ..core.progress import ProgressStore
from ..core.user_notes import (
    TITLE_MAX_LENGTH,
    build_zip,
    note_to_markdown,
    read_notes_file,
    render_note,
    safe_filename,
)
from ..resources.icons import icon
from ..resources.theme.tokens import PALETTES, READING_WIDTH, SPACING
from ..widgets.document_view import DocumentView
from ..widgets.note_editor import NoteEditor
from ..widgets.note_toolbar import NoteToolbar
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


class _NoteIndent(QStyledItemDelegate):
    """Klasörün altındaki notu içeri alarak çizer.

    Seçim ve üzerine gelme zemini notun kendi kutusuyla başlıyor; girinti
    boşluğu boş kalıyor.
    """

    def paint(self, painter, option, index) -> None:
        if index.parent().isValid():
            option = QStyleOptionViewItem(option)
            option.rect = option.rect.adjusted(SPACING["lg"], 0, 0, 0)
        super().paint(painter, option, index)


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

        # İndirme/yükleme sonucunu söyleyen satır bir süre sonra kayboluyor.
        self._status_timer = QTimer(self)
        self._status_timer.setSingleShot(True)
        self._status_timer.setInterval(8000)
        # Dosya penceresi en son kullanılan klasörde açılsın.
        self._last_dir = Path(
            QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DownloadLocation)
            or Path.home()
        )

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

        # İndir / Yükle. İndirmenin menüsü düğmeye bağlanmıyor, basınca
        # açılıyor: bağlanınca Qt düğmenin kenarına kendi okunu çiziyor.
        transfer = QHBoxLayout()
        transfer.setSpacing(SPACING["sm"])
        self._download_button = QPushButton()
        self._download_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._download_button.clicked.connect(self._show_download_menu)
        self._upload_button = QPushButton()
        self._upload_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._upload_button.clicked.connect(self.upload)
        transfer.addWidget(self._download_button, 1)
        transfer.addWidget(self._upload_button, 1)
        column.addLayout(transfer)

        self._tree = QTreeWidget()
        self._tree.setProperty("role", "notebook-tree")
        self._tree_style = None
        self._apply_tree_style()
        self._tree.setHeaderHidden(True)
        # Açma oku yok: klasöre tıklamak açıp kapatıyor. Qt'nin oku bizim
        # temamızda çizilmiyor, yerine bir şey koymak da kalabalık ediyordu.
        self._tree.setRootIsDecorated(False)
        # Ağacın kendi girintisi yok; notları `_NoteIndent` içeri alıyor.
        # Girinti ağaçta olunca seçim o boşluğu da ayrı bir parça olarak
        # boyuyordu ve notun solunda kopuk bir vurgu kalıyordu.
        self._tree.setIndentation(0)
        self._tree.setItemDelegate(_NoteIndent(self._tree))
        self._tree.setIconSize(QSize(18, 18))
        self._tree.itemClicked.connect(self._on_item_clicked)
        self._tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self._tree.customContextMenuRequested.connect(self._tree_menu)
        column.addWidget(self._tree, 1)

        self._status = QLabel()
        self._status.setProperty("role", "muted")
        self._status.setWordWrap(True)
        self._status.hide()
        self._status_timer.timeout.connect(self._status.hide)
        column.addWidget(self._status)

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

        self._editor = NoteEditor(mode=self._mode)
        self._editor.textChanged.connect(self._on_edited)
        self._toolbar = NoteToolbar(self._editor)
        inner.addWidget(self._toolbar)
        inner.addWidget(self._editor, 1)

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
        """Sağ tık: notta Düzenle / İndir / Sil, klasörde klasörü indir.

        Eylemler kendi `triggered` sinyaline bağlı; `exec`'in döndürdüğü
        eylemin kimliğine güvenilmiyor.
        """
        item = self._tree.itemAt(position)
        if item is None:
            return
        t = self._language.t
        menu = QMenu(self)

        if item.data(0, ROLE_KIND) == "note":
            entry_id = int(item.data(0, ROLE_ID))
            menu.addAction(t("notebook.edit")).triggered.connect(
                lambda: self.open_note(entry_id, edit=True)
            )
            menu.addAction(t("notebook.download_note")).triggered.connect(
                lambda: self.download_note(entry_id)
            )
            menu.addSeparator()

            def sil() -> None:
                self.open_note(entry_id)
                self._delete()

            menu.addAction(t("notebook.delete")).triggered.connect(sil)
        else:
            key = item.data(0, ROLE_ID)
            eylem = menu.addAction(t("notebook.download_folder", folder=self._folder_title(key)))
            eylem.setEnabled(bool(self._folder_entries(key)))
            eylem.triggered.connect(lambda: self.download_folder(key))

        menu.exec(self._tree.viewport().mapToGlobal(position))

    # --- indirme ve yükleme -----------------------------------------------

    def _folder_title(self, key: str) -> str:
        chapter = self._catalog.chapter(key) if key else None
        return self._language.pick(chapter.title) if chapter else self._language.t("notebook.other")

    def _folder_entries(self, key: str) -> list[dict]:
        return [e for e in self._entries if self._folder_key(e["chapter_id"]) == key]

    def _full(self, entries: list[dict]) -> list[dict]:
        """Ağaçtaki satırlar gövdesiz; indirilecek notların tamamı."""
        return [full for e in entries if (full := self._store.notebook_entry(e["id"]))]

    def _show_status(self, text: str) -> None:
        self._status.setText(text)
        self._status.show()
        self._status_timer.start()

    def _show_download_menu(self) -> None:
        self.flush()
        t = self._language.t
        entry = self._entry()
        klasor = self._folder_key(entry["chapter_id"]) if entry else self._folder_hint

        menu = QMenu(self)
        bu_not = menu.addAction(t("notebook.download_note"))
        bu_not.setEnabled(entry is not None)
        if entry is not None:
            bu_not.triggered.connect(lambda: self.download_note(entry["id"]))
        bu_klasor = menu.addAction(t("notebook.download_folder", folder=self._folder_title(klasor)))
        bu_klasor.setEnabled(bool(self._folder_entries(klasor)))
        bu_klasor.triggered.connect(lambda: self.download_folder(klasor))
        hepsi = menu.addAction(t("notebook.download_all"))
        hepsi.setEnabled(bool(self._entries))
        hepsi.triggered.connect(lambda: self.download_all())
        menu.exec(self._download_button.mapToGlobal(QPoint(0, self._download_button.height() + 4)))

    def _ask_save_path(self, name: str, file_filter: str) -> Path | None:
        path, _ = QFileDialog.getSaveFileName(
            self, self._language.t("notebook.download"), str(self._last_dir / name), file_filter
        )
        if not path:
            return None
        self._last_dir = Path(path).parent
        return Path(path)

    def _write(self, path: Path, data: bytes) -> bool:
        try:
            path.write_bytes(data)
        except OSError:
            self._show_status(self._language.t("notebook.export_failed"))
            return False
        self._show_status(self._language.t("notebook.exported", name=path.name))
        return True

    def download_note(self, entry_id: int, path: Path | None = None) -> bool:
        """Tek notu `.md` olarak kaydeder. `path` verilmezse sorar."""
        self.flush()
        entry = self._store.notebook_entry(entry_id)
        if entry is None:
            return False
        path = path or self._ask_save_path(
            f"{safe_filename(entry['title'])}.md", self._language.t("notebook.md_filter")
        )
        return path is not None and self._write(path, note_to_markdown(entry).encode("utf-8"))

    def download_folder(self, key: str, path: Path | None = None) -> bool:
        """Bir klasörün notlarını `.zip` olarak kaydeder."""
        self.flush()
        entries = self._full(self._folder_entries(key))
        if not entries:
            return False
        baslik = self._folder_title(key)
        path = path or self._ask_save_path(
            f"Odyssey - {safe_filename(baslik)}.zip", self._language.t("notebook.zip_filter")
        )
        return path is not None and self._write(path, build_zip([(baslik, entries)]))

    def download_all(self, path: Path | None = None) -> bool:
        """Bütün notları, klasör başına bir dizinle `.zip` olarak kaydeder."""
        self.flush()
        groups = [
            (title, self._full(self._folder_entries(key)))
            for key, title, *_ in self._folders()
            if self._folder_entries(key)
        ]
        if not groups:
            return False
        path = path or self._ask_save_path(
            f"{self._language.t('notebook.all_notes_file')}.zip",
            self._language.t("notebook.zip_filter"),
        )
        return path is not None and self._write(path, build_zip(groups))

    def upload(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, self._language.t("notebook.upload"), str(self._last_dir),
            self._language.t("notebook.file_filter"),
        )
        if path:
            self._last_dir = Path(path).parent
            self.import_file(Path(path))

    def import_file(self, path: Path) -> int:
        """`.md` ya da `.zip` dosyasındaki notları ekler; eklenen sayısını döndürür.

        Hiçbir notun üstüne yazılmıyor: aynı klasörde aynı ad varsa yeni
        not "(2)" alıyor (`ProgressStore.add_notebook_entry`).
        """
        self.flush()
        t = self._language.t
        try:
            notes, problems = read_notes_file(path, t("notebook.untitled"))
        except (OSError, zipfile.BadZipFile, ValueError):
            self._show_status(t("notebook.import_failed"))
            return 0

        ids = [
            self._store.add_notebook_entry(n["chapter_id"], n["section_id"], n["title"], n["body"])
            for n in notes
        ]
        parca = [t("notebook.imported", count=len(ids)) if ids else t("notebook.import_none")]
        if problems:
            parca.append(t("notebook.import_problems", count=problems))
        self._show_status(" ".join(parca))

        if ids:
            ilk = self._store.notebook_entry(ids[0])
            self._current = ids[0]
            self._editing = False
            self._collapsed.discard(self._folder_key(ilk["chapter_id"]))
            self.refresh()
            self.changed.emit()
        return len(ids)

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
        self._download_button.setText(f"{t('notebook.download')}  ▾")
        self._upload_button.setText(t("notebook.upload"))
        self._upload_button.setToolTip(t("notebook.upload_hint"))
        self._title_edit.setPlaceholderText(t("notebook.title_placeholder"))
        self._editor.setPlaceholderText(t("notebook.body_placeholder"))
        self._toolbar.retranslate(t)

        # Klasör adları ve "Diğer" dile bağlı. Yazma hâlinde editör yeniden
        # yüklenmiyor: yüklenseydi kaydedilmemiş son harfler giderdi.
        self._rebuild_tree()
        entry = self._entry()
        if entry is not None and self._editing:
            self._update_bar(entry)
        else:
            self._show_current()
