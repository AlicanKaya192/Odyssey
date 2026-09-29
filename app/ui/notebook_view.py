"""Notlarım: kullanıcının kendi notları.

Solda klasör ağacı, sağda seçili not. Klasörler önce patikalar (katalog
sırasıyla), sonra kullanıcının kendi açtığı klasörler, en sonda gerekirse
"Diğer" (patikası bu sürümde olmayan notlar). Her klasörün not sayısı
satırın sağında, soluk; boş klasörde "0" — sayı yalnızca dolu klasörde
yazılınca boş olanlar "sayı gelmedi" gibi okunuyordu.

Not önce okuma hâlinde açılıyor (dersler gibi çizilmiş); "Düzenle" ile
yazma hâline geçiliyor. "Taşı" notu başka bir klasöre koyuyor: kendi
klasörüne giden not dersine bağlı kalıyor, başka bir patikaya giden not
bağlantısını kaybediyor (`ProgressStore.move_notebook_entry`).

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

from PySide6.QtCore import QElapsedTimer, QPoint, QPointF, QRectF, QSize, QStandardPaths, Qt, QTimer, Signal
from PySide6.QtGui import QColor, QFont, QIcon, QKeySequence, QPainter, QPen, QShortcut, QTextCursor
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMenu,
    QPushButton,
    QStackedWidget,
    QStyle,
    QStyledItemDelegate,
    QStyleFactory,
    QStyleOptionViewItem,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from ..widgets import motion
from ..core.catalog import Catalog
from ..core.language import LanguageManager
from ..core.progress import ProgressStore
from ..core.user_notes import (
    FOLDER_MAX_LENGTH,
    TITLE_MAX_LENGTH,
    build_zip,
    note_to_markdown,
    read_notes_file,
    render_note,
    safe_filename,
)
from ..resources.icons import icon
from ..resources.theme.tokens import RAIL_COLORS, PALETTES, READING_WIDTH, SPACING
from ..widgets.document_view import DocumentView
from ..widgets.note_editor import NoteEditor
from ..widgets.note_toolbar import NoteToolbar
from . import titlebar
from .confirm_dialog import ConfirmDialog
from .modal import Backdrop
from .name_dialog import NameDialog
from ..widgets.empty_state import EmptyState
from ..resources.logos import logo_key, logo_pixmap
from .new_note_dialog import FOLDER_PREFIX, NewNoteDialog

SIDE_WIDTH = 300

# Yazmayı bıraktıktan kaç milisaniye sonra kaydedilsin. Her tuşta yazmak
# gereksiz; bir saniyeden uzunu da "kaydetti mi" diye düşündürüyor.
SAVE_DELAY_MS = 700

ROLE_KIND = Qt.ItemDataRole.UserRole
ROLE_ID = Qt.ItemDataRole.UserRole + 1
# Klasördeki not sayısı; satırın sağına ayrı çiziliyor.
ROLE_COUNT = Qt.ItemDataRole.UserRole + 2

# Klasör adı uzunsa sayıyla çakışmasın diye sağda bırakılan pay.
COUNT_SPACE = 56

# Katalogda karşılığı olmayan klasör (başka bir sürümden gelen not gibi).
OTHER_FOLDER = ""

PAGE_EMPTY, PAGE_READ, PAGE_EDIT = 0, 1, 2


class _TreeDelegate(QStyledItemDelegate):
    """Ağacın çizimi.

    Klasörün altındaki not içeri alınarak çiziliyor: seçim ve üzerine
    gelme zemini notun kendi kutusuyla başlıyor, girinti boşluğu boş
    kalıyor. Klasörün not sayısı satırın sağında soluk renkte; adı uzunsa
    sayının altına girmeden kısaltılıyor.
    """

    FOLDER_HEIGHT = 40
    NOTE_HEIGHT = 34
    LOGO = 24

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.count_color = QColor("#98A1AF")
        self.text_color = QColor("#E6E9EF")
        self.hover_color = QColor("#1E222B")
        self.select_color = QColor("#221F3D")
        # Sıralı giriş saati (klasör satırları 40 ms arayla 8 px aşağıdan).
        self.enter_clock = None
        # Klasör okunun açısı (0 sağa, 1 aşağı); açılıp kapanırken yayla döner.
        self.turn: dict = {}

    def sizeHint(self, option, index) -> QSize:  # noqa: N802
        boy = self.NOTE_HEIGHT if index.parent().isValid() else self.FOLDER_HEIGHT
        return QSize(option.rect.width(), boy)

    def paint(self, painter, option, index) -> None:
        if index.parent().isValid():
            option = QStyleOptionViewItem(option)
            option.rect = option.rect.adjusted(SPACING["lg"] + 8, 0, 0, 0)
            super().paint(painter, option, index)
            return

        # Klasör satırı (prototip `.ntree .fold`): 24 px logo, kalın ad,
        # sağda not sayısı ve açılınca aşağı dönen ok.
        count = index.data(ROLE_COUNT)
        opt = QStyleOptionViewItem(option)
        self.initStyleOption(opt, index)
        r = QRectF(opt.rect).adjusted(2, 2, -2, -2)
        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        if self.enter_clock is not None:
            from ..resources.theme.motion import spring
            gecen = self.enter_clock.elapsed() - min(index.row(), 7) * 40
            k = spring(max(0.0, min(1.0, gecen / 420)))
            painter.setOpacity(max(0.0, min(1.0, k)))
            painter.translate(0, 8 * (1 - k))
        if opt.state & QStyle.StateFlag.State_Selected:
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(self.select_color)
            painter.drawRoundedRect(r, 10, 10)
        elif opt.state & QStyle.StateFlag.State_MouseOver:
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(self.hover_color)
            painter.drawRoundedRect(r, 10, 10)

        x = r.left() + 8
        simge = index.data(Qt.ItemDataRole.DecorationRole)
        if isinstance(simge, QIcon):
            pix = simge.pixmap(self.LOGO, self.LOGO)
            painter.drawPixmap(QRectF(x, r.center().y() - self.LOGO / 2, self.LOGO, self.LOGO), pix, QRectF(pix.rect()))
        x += self.LOGO + 10

        sag = r.right() - 10
        # Ok: sağa bakan ince çizgi; klasör açıkken aşağı döner.
        # Boş klasörde açılacak bir şey yok; ok hep sağa bakıyor.
        acik = bool(opt.state & QStyle.StateFlag.State_Open) and index.model().rowCount(index) > 0
        aci = self.turn.get(index.data(ROLE_ID), 1.0 if acik else 0.0)
        painter.save()
        painter.translate(sag - 5, r.center().y())
        painter.rotate(90 * aci)
        kalem = QPen(self.count_color, 1.6)
        kalem.setCapStyle(Qt.PenCapStyle.RoundCap)
        kalem.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        painter.setPen(kalem)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawPolyline([QPointF(-2, -4), QPointF(2, 0), QPointF(-2, 4)])
        painter.restore()
        sag -= 20

        font = QFont(opt.font)
        if count is not None:
            font.setWeight(QFont.Weight.Normal)
            painter.setFont(font)
            painter.setPen(self.count_color)
            yazi = str(count)
            genis = painter.fontMetrics().horizontalAdvance(yazi)
            painter.drawText(QRectF(sag - genis, r.top(), genis, r.height()),
                             int(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter), yazi)
            sag -= genis + 10

        font.setWeight(QFont.Weight.DemiBold)
        font.setPixelSize(14)
        painter.setFont(font)
        painter.setPen(self.text_color)
        ad = painter.fontMetrics().elidedText(opt.text, Qt.TextElideMode.ElideRight, int(max(0, sag - x)))
        painter.drawText(QRectF(x, r.top(), max(0, sag - x), r.height()),
                         int(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter), ad)
        painter.restore()


class _Frozen:
    """Sıralı giriş başlamadan: süre hep 0 (satırlar görünmez bekler)."""

    def elapsed(self) -> int:
        return -1000


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
        # Kullanıcının kendi klasörleri.
        self._custom: list[dict] = []
        self._custom_ids: set[int] = set()
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

        # İndirme/yükleme/taşıma sonucunu söyleyen satır bir süre sonra
        # kayboluyor.
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

        top = QHBoxLayout()
        top.setSpacing(SPACING["sm"])
        self._new_button = QPushButton()
        self._new_button.setProperty("variant", "primary")
        self._new_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._new_button.clicked.connect(self.new_note)
        top.addWidget(self._new_button, 1)
        self._folder_button = QPushButton()
        self._folder_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._folder_button.setIconSize(QSize(18, 18))
        self._folder_button.setFixedWidth(46)
        self._folder_button.clicked.connect(self.new_folder)
        top.addWidget(self._folder_button)
        column.addLayout(top)

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
        # Ağacın kendi girintisi yok; notları `_TreeDelegate` içeri alıyor.
        # Girinti ağaçta olunca seçim o boşluğu da ayrı bir parça olarak
        # boyuyordu ve notun solunda kopuk bir vurgu kalıyordu.
        self._tree.setIndentation(0)
        self._delegate = _TreeDelegate(self._tree)
        self._tree.setItemDelegate(self._delegate)
        self._tree.setIconSize(QSize(18, 18))
        self._tree.setMouseTracking(True)
        self._tree.itemClicked.connect(self._on_item_clicked)
        # Klasör açılırken notlar kayarak açılıyor (prototip `.kids`), ok dönüyor.
        self._tree.setAnimated(True)
        self._tree.itemExpanded.connect(lambda item: self._turn_arrow(item, 1.0))
        self._tree.itemCollapsed.connect(lambda item: self._turn_arrow(item, 0.0))
        self._tree_entered = False
        self._enter_timer = QTimer(self)
        self._enter_timer.setInterval(16)
        self._enter_timer.timeout.connect(self._tick_tree_enter)
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
        self._move_button = self._bar_button("ghost", self._show_move_menu)
        self._delete_button = self._bar_button("ghost", self._delete)
        self._edit_button = self._bar_button("primary", self._toggle_edit)
        for button in (self._lesson_button, self._move_button, self._delete_button, self._edit_button):
            bar_row.addWidget(button)
        column.addWidget(bar)

        self._pages = QStackedWidget()

        # Boş durum kartı (ui-taslak.md B10): simge, başlık, cümle, düğme.
        self._empty = EmptyState()
        self._empty.action.connect(self.new_note)
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

    # --- klasörler --------------------------------------------------------

    def refresh(self) -> None:
        """Notları ve klasörleri veritabanından yeniden okur."""
        self._entries = self._store.notebook_entries()
        self._custom = self._store.notebook_folders()
        self._custom_ids = {folder["id"] for folder in self._custom}
        if self._current is not None and all(e["id"] != self._current for e in self._entries):
            self._current = None
            self._editing = False
        self._rebuild_tree()
        self._show_current()

    def _folders(self) -> list[tuple[str, str, str, str]]:
        """(anahtar, ad, simge, renk): patikalar, kendi klasörleri, gerekirse "Diğer"."""
        palette = PALETTES.get(self._mode, PALETTES["light"])
        folders = [
            (chapter.id, self._language.pick(chapter.title), chapter.icon, chapter.color)
            for chapter in self._catalog.chapters
            if chapter.sections
        ]
        folders += [
            (f"{FOLDER_PREFIX}{folder['id']}", folder["name"], "folder", palette["accent"])
            for folder in self._custom
        ]
        if any(self._entry_key(e) == OTHER_FOLDER for e in self._entries):
            folders.append(
                (OTHER_FOLDER, self._language.t("notebook.other"), "folder", palette["text_muted"])
            )
        return folders

    def _entry_key(self, entry: dict) -> str:
        """Notun ağaçta durduğu klasörün anahtarı."""
        folder_id = entry.get("folder_id")
        if folder_id is not None and folder_id in self._custom_ids:
            return f"{FOLDER_PREFIX}{folder_id}"
        if self._catalog.chapter(entry["chapter_id"]) is not None:
            return entry["chapter_id"]
        return OTHER_FOLDER

    @staticmethod
    def _custom_id(key: str) -> int | None:
        return int(key[len(FOLDER_PREFIX):]) if key.startswith(FOLDER_PREFIX) else None

    def _folder_title(self, key: str) -> str:
        custom_id = self._custom_id(key)
        if custom_id is not None:
            for folder in self._custom:
                if folder["id"] == custom_id:
                    return folder["name"]
        chapter = self._catalog.chapter(key) if key and custom_id is None else None
        return self._language.pick(chapter.title) if chapter else self._language.t("notebook.other")

    def _folder_entries(self, key: str) -> list[dict]:
        return [e for e in self._entries if self._entry_key(e) == key]

    def _rebuild_tree(self) -> None:
        palette = PALETTES.get(self._mode, PALETTES["light"])
        self._tree.clear()

        grouped: dict[str, list[dict]] = {}
        for entry in self._entries:
            grouped.setdefault(self._entry_key(entry), []).append(entry)

        for key, title, icon_name, color in self._folders():
            notes = grouped.get(key, [])
            folder = QTreeWidgetItem([title])
            folder.setData(0, ROLE_KIND, "folder")
            folder.setData(0, ROLE_ID, key)
            folder.setData(0, ROLE_COUNT, len(notes))
            # Patika klasörlerinde patikanın logosu (E2); kendi klasörlerinde simge.
            if self._catalog.chapter(key) is not None:
                folder.setIcon(0, QIcon(logo_pixmap(logo_key(icon_name, key), color, 24)))
            else:
                folder.setIcon(0, icon(icon_name or "folder", color or palette["text_muted"], 22))
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

    def _turn_arrow(self, item: QTreeWidgetItem, hedef: float) -> None:
        anahtar = item.data(0, ROLE_ID)
        if item.childCount() == 0:
            hedef = 0.0
        simdi = self._delegate.turn.get(anahtar, 1.0 - hedef)

        def ayarla(v: float, a=anahtar) -> None:
            self._delegate.turn[a] = v
            self._tree.viewport().update()

        motion.animate(self._tree, f"turn:{anahtar}", simdi, hedef, ayarla, "spring", "spring")

    def _tick_tree_enter(self) -> None:
        self._tree.viewport().update()
        saat = self._delegate.enter_clock
        if saat is None or saat.elapsed() > 420 + 7 * 40:
            self._delegate.enter_clock = None
            self._enter_timer.stop()
            self._tree.viewport().update()

    def showEvent(self, event) -> None:  # noqa: N802
        super().showEvent(event)
        # Oturumdaki ilk gösterimde klasörler sırayla gelir (prototip `.stg`).
        if not self._tree_entered and motion.enabled():
            self._tree_entered = True
            from ..widgets.fade_stack import after_reveal
            # Geçiş başlayana kadar satırlar görünmez bekliyor.
            self._delegate.enter_clock = _Frozen()

            def basla() -> None:
                saat = QElapsedTimer()
                saat.start()
                self._delegate.enter_clock = saat
                self._enter_timer.start()

            after_reveal(self, basla)

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
        """Sağ tık menüsü.

        Notta: Düzenle, Taşı, İndir, Sil. Patika klasöründe: klasörü indir.
        Kendi klasöründe: yeniden adlandır, indir, sil. Her klasörde ve
        boş yerde: Yeni klasör. Eylemler kendi `triggered` sinyaline bağlı;
        `exec`'in döndürdüğü eylemin kimliğine güvenilmiyor.
        """
        item = self._tree.itemAt(position)
        t = self._language.t
        menu = QMenu(self)

        if item is not None and item.data(0, ROLE_KIND) == "note":
            entry_id = int(item.data(0, ROLE_ID))
            entry = self._store.notebook_entry(entry_id)
            menu.addAction(t("notebook.edit")).triggered.connect(
                lambda: self.open_note(entry_id, edit=True)
            )
            if entry is not None:
                tasi = menu.addMenu(t("notebook.move"))
                for key, title in self._move_targets(entry):
                    tasi.addAction(title).triggered.connect(
                        lambda _=False, k=key: self.move_note(entry_id, k)
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
            if item is not None:
                key = item.data(0, ROLE_ID)
                custom_id = self._custom_id(key)
                if custom_id is not None:
                    menu.addAction(t("notebook.rename_folder")).triggered.connect(
                        lambda: self.rename_folder(custom_id)
                    )
                indir = menu.addAction(t("notebook.download_folder", folder=self._folder_title(key)))
                indir.setEnabled(bool(self._folder_entries(key)))
                indir.triggered.connect(lambda: self.download_folder(key))
                if custom_id is not None:
                    menu.addSeparator()
                    menu.addAction(t("notebook.delete_folder")).triggered.connect(
                        lambda: self.delete_folder(custom_id)
                    )
                menu.addSeparator()
            menu.addAction(t("notebook.new_folder")).triggered.connect(self.new_folder)

        menu.exec(self._tree.viewport().mapToGlobal(position))

    def _ask_name(self, title: str, initial: str, confirm: str) -> str | None:
        kok = self.window()
        perde = Backdrop(kok)
        perde.show()
        t = self._language.t
        dialog = NameDialog(
            title,
            t("notebook.folder_name"),
            t("notebook.folder_placeholder"),
            initial,
            confirm,
            t("common.cancel"),
            FOLDER_MAX_LENGTH,
            kok,
        )
        kabul = dialog.exec()
        perde.deleteLater()
        return dialog.value() if kabul else None

    def new_folder(self) -> None:
        """Kullanıcının kendi klasörünü açar."""
        self.flush()
        ad = self._ask_name(
            self._language.t("notebook.new_folder"), "", self._language.t("notebook.create")
        )
        if not ad:
            return
        folder_id = self._store.add_notebook_folder(ad)
        self._folder_hint = f"{FOLDER_PREFIX}{folder_id}"
        self.refresh()

    def rename_folder(self, folder_id: int) -> None:
        eski = self._folder_title(f"{FOLDER_PREFIX}{folder_id}")
        ad = self._ask_name(
            self._language.t("notebook.rename_folder_title"), eski, self._language.t("common.save")
        )
        if ad:
            self._store.rename_notebook_folder(folder_id, ad)
            self.refresh()

    def delete_folder(self, folder_id: int, confirm: bool = True) -> None:
        """Klasörü siler; içindeki notlar patikalarının klasörüne döner."""
        self.flush()
        key = f"{FOLDER_PREFIX}{folder_id}"
        if confirm:
            t = self._language.t
            dialog = ConfirmDialog(
                t("notebook.delete_folder_title"),
                t("notebook.delete_folder_message", name=self._folder_title(key)),
                t("notebook.delete_folder"),
                t("common.cancel"),
                self.window(),
            )
            titlebar.apply(dialog, self._mode)
            if dialog.exec() != ConfirmDialog.DialogCode.Accepted:
                return
        self._store.delete_notebook_folder(folder_id)
        if self._folder_hint == key:
            self._folder_hint = ""
        self.refresh()

    def _move_targets(self, entry: dict) -> list[tuple[str, str]]:
        """Notun taşınabileceği klasörler: bulunduğu klasör ve "Diğer" hariç."""
        current = self._entry_key(entry)
        return [
            (key, title)
            for key, title, *_ in self._folders()
            if key != OTHER_FOLDER and key != current
        ]

    def _show_move_menu(self) -> None:
        entry = self._entry()
        if entry is None:
            return
        menu = QMenu(self)
        for key, title in self._move_targets(entry):
            menu.addAction(title).triggered.connect(
                lambda _=False, k=key: self.move_note(entry["id"], k)
            )
        menu.exec(self._move_button.mapToGlobal(QPoint(0, self._move_button.height() + 4)))

    def move_note(self, entry_id: int, key: str) -> None:
        """Notu `key` klasörüne taşır."""
        self.flush()
        custom_id = self._custom_id(key)
        if custom_id is not None:
            son = self._store.move_notebook_entry(entry_id, folder_id=custom_id)
        else:
            son = self._store.move_notebook_entry(entry_id, chapter_id=key)
        if son is None:
            return
        self._collapsed.discard(key)
        self._folder_hint = key
        self._show_status(self._language.t("notebook.moved", folder=self._folder_title(key)))
        self.refresh()

    # --- indirme ve yükleme -----------------------------------------------

    def _full(self, entries: list[dict]) -> list[dict]:
        """Ağaçtaki satırlar gövdesiz; indirilecek notların tamamı.

        Kendi klasöründeki notun klasör adı da ekleniyor; bilgi bloğuna
        yazılıyor, yükleyende aynı adla klasör açılıyor.
        """
        adlar = {folder["id"]: folder["name"] for folder in self._custom}
        tam: list[dict] = []
        for e in entries:
            full = self._store.notebook_entry(e["id"])
            if full is None:
                continue
            if full.get("folder_id") in adlar:
                full["folder"] = adlar[full["folder_id"]]
            tam.append(full)
        return tam

    def _show_status(self, text: str) -> None:
        self._status.setText(text)
        self._status.show()
        self._status_timer.start()

    def _show_download_menu(self) -> None:
        self.flush()
        t = self._language.t
        entry = self._entry()
        klasor = self._entry_key(entry) if entry else self._folder_hint

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
        entries = self._full([{"id": entry_id}])
        if not entries:
            return False
        entry = entries[0]
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
        not "(2)" alıyor (`ProgressStore.add_notebook_entry`). Notun
        bilgi bloğunda bir klasör adı varsa aynı adlı klasöre giriyor, yoksa
        o klasör açılıyor.
        """
        self.flush()
        t = self._language.t
        try:
            notes, problems = read_notes_file(path, t("notebook.untitled"))
        except (OSError, zipfile.BadZipFile, ValueError):
            self._show_status(t("notebook.import_failed"))
            return 0

        ids = []
        for note in notes:
            folder_id = (
                self._store.find_or_add_notebook_folder(note["folder"]) if note.get("folder") else None
            )
            ids.append(
                self._store.add_notebook_entry(
                    note["chapter_id"], note["section_id"], note["title"], note["body"], folder_id
                )
            )
        parca = [t("notebook.imported", count=len(ids)) if ids else t("notebook.import_none")]
        if problems:
            parca.append(t("notebook.import_problems", count=problems))
        self._show_status(" ".join(parca))

        if ids:
            self._current = ids[0]
            self._editing = False
            self.refresh()
            ilk = self._store.notebook_entry(ids[0])
            if ilk is not None:
                self._collapsed.discard(self._entry_key(ilk))
                self._rebuild_tree()
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
            self._folder_hint = self._entry_key(entry)
        self._rebuild_tree()
        self._show_current()

    def new_note(self) -> None:
        """"Yeni not": en son bakılan klasör önerilir."""
        self.create_note(self._folder_hint)

    def create_note(self, folder_key: str = "", section_id: str = "", title: str = "") -> None:
        """Ad soran pencereyi açar; onaylanırsa notu yazma hâlinde açar."""
        self.flush()
        kok = self.window()
        perde = Backdrop(kok)
        perde.show()
        dialog = NewNoteDialog(
            self._catalog, self._language, self._custom, folder_key, section_id, title,
            self._mode, kok,
        )
        kabul = dialog.exec()
        perde.deleteLater()
        if not kabul:
            return

        chapter_id, section_id, title, folder_id = dialog.values()
        self._current = self._store.add_notebook_entry(
            chapter_id, section_id, title, folder_id=folder_id
        )
        self._editing = True
        key = f"{FOLDER_PREFIX}{folder_id}" if folder_id is not None else chapter_id
        self._folder_hint = key
        self._collapsed.discard(key)
        self.refresh()
        self.changed.emit()

    def _entry(self) -> dict | None:
        if self._current is None:
            return None
        return self._store.notebook_entry(self._current)

    def _show_current(self) -> None:
        entry = self._entry()
        t = self._language.t

        for button in (self._edit_button, self._move_button, self._delete_button):
            button.setVisible(entry is not None)
        self._saved.hide()

        if entry is None:
            self._crumb.setText("")
            self._lesson_button.hide()
            renk = RAIL_COLORS.get(self._mode, RAIL_COLORS["light"])["notes"]
            if self._entries:
                self._empty.set_content("file-text", renk, t("notebook.pick_title"), t("notebook.empty"))
            else:
                self._empty.set_content("notebook", renk, t("notebook.first_title"), t("notebook.first"),
                                        t("notebook.first_button"))
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
            from ..widgets.pop_effect import enter
            enter(self._pages.currentWidget(), 16, "short")
            self._editor.setFocus()
            self._editor.moveCursor(QTextCursor.MoveOperation.End)
        else:
            self._render_reader(entry)
            self._pages.setCurrentIndex(PAGE_READ)

    def _update_bar(self, entry: dict) -> None:
        """Eylem şeridinin metinleri. Editördeki metne dokunmuyor.

        Yer satırı notun ağaçta durduğu klasörü ve (varsa) bağlı olduğu
        dersi gösteriyor: kendi klasörüne taşınmış bir not "Sınav öncesi ›
        Koşul Durumları" gibi.
        """
        t = self._language.t
        section = (
            self._catalog.section(entry["chapter_id"], entry["section_id"])
            if entry["section_id"]
            else None
        )
        yer = [self._folder_title(self._entry_key(entry))]
        if section is not None:
            yer.append(self._language.pick(section.title))
        self._crumb.setText("  ›  ".join(yer))

        self._lesson_button.setVisible(section is not None)
        self._lesson_button.setText(t("notebook.go_to_lesson"))
        self._move_button.setText(f"{t('notebook.move')}  ▾")
        self._delete_button.setText(t("notebook.delete"))
        self._edit_button.setText(t("notebook.done") if self._editing else t("notebook.edit"))

    def _render_reader(self, entry: dict) -> None:
        t = self._language.t
        body = entry["body"] if entry["body"].strip() else f"*{t('notebook.empty_body')}*"
        meta = [t("notebook.updated", date=_format_time(entry["updated_at"], self._language.language))]
        content = render_note(entry["title"], body, meta)
        self._reader.set_lang(self._language.language)
        # Not açılınca 16 px aşağıdan belirir (prototip `.neditor`, `pgIn`).
        self._reader.set_body(
            f'<div class="page narrow notebook"><div class="content pgin">{content}</div></div>'
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

        # Boş not ilk kez yazıya döndü: rozet koşulu bunu bekliyor. Her
        # kayıtta değil yalnızca bu geçişte haber veriliyor; ilerleme ve
        # rozet hesabı her 700 ms'de bir koşacak iş değil.
        if not entry["body"].strip() and self._editor.toPlainText().strip():
            self.changed.emit()

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
        palette = PALETTES.get(mode, PALETTES["light"])
        self._apply_tree_style()
        self._delegate.count_color = QColor(palette["text_muted"])
        self._delegate.text_color = QColor(palette["text"])
        self._delegate.hover_color = QColor(palette["surface_hover"])
        self._delegate.select_color = QColor(palette["accent_soft"])
        self._new_button.setIcon(icon("plus", "#FFFFFF", 16))
        self._download_button.setIcon(icon("download", palette["text"], 16))
        self._upload_button.setIcon(icon("upload", palette["text"], 16))
        self._folder_button.setIcon(icon("folder-plus", palette["text"], 18))
        self._reader.set_mode(mode)
        self._editor.set_mode(mode)
        self._rebuild_tree()

    def retranslate(self) -> None:
        t = self._language.t
        self._new_button.setText(f"  {t('notebook.new')}")
        self._new_button.setToolTip("Ctrl+N")
        self._folder_button.setToolTip(t("notebook.new_folder"))
        self._download_button.setText(f"  {t('notebook.download')}  ▾")
        self._upload_button.setText(f"  {t('notebook.upload')}")
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
