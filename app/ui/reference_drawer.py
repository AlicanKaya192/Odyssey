"""Hızlı başvuru çekmecesi: bölümlerin başvuru notları, her ekrandan.

Alt şeritteki düğme ya da `Ctrl+R` ile sağdan kayarak açılıyor. Bölümdeyken
o bölümün notu, dışarıdayken en son açılan bölümünkü; üstteki kutudan başka
bölümlerin notları aranıyor. İçerik `core.reference_notes`'tan.

**Kip değil, dışarı tıklayınca kapanmıyor.** Asıl kullanımı alıştırma
yazarken komut kartına bakmak: editöre tıklamak çekmeceyi kapatsaydı her
bakışta yeniden açmak gerekirdi. Kapatmak: çarpı, `Esc`, `Ctrl+R`, düğme.

**Pencerenin içinde bir katman** (kısayol paneli gibi), ayrı pencere değil.
Belge görünümü (Chromium) ilk açılışta kuruluyor: açılışta tarayıcı
bileşeni yüklenmiyor (CLAUDE.md → Açılış animasyonu, 15 Ekim).
"""

from __future__ import annotations

from PySide6.QtCore import QEvent, Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QSizePolicy,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from ..core import reference_notes
from ..core.catalog import Catalog
from ..core.language import LanguageManager
from ..resources.icons import icon, pixmap
from ..resources.theme.tokens import PALETTES, SPACING
from ..widgets import motion
from ..widgets.common import DropdownBox
from .note_panel import ROLE_ID, ROLE_WHERE, NoteRow

# Genişlik: pencerenin en fazla bu oranı, en az / en çok bu kadar piksel.
WIDTH_SHARE = 0.42
MIN_WIDTH = 380
MAX_WIDTH = 520
# Pencere kenarlarıyla arası (bölümdeki not paneli gibi yüzen kart).
MARGIN = 12

PAGE_READ = 0
PAGE_RESULTS = 1


class ReferenceDrawer(QFrame):
    """Sağda yüzen başvuru paneli."""

    closed = Signal()

    def __init__(self, catalog: Catalog, language: LanguageManager, parent: QWidget) -> None:
        super().__init__(parent)
        self._language = language
        self._mode = "dark"
        self._entries = reference_notes.build_entries(catalog)
        self._by_key = {kayit.key: kayit for kayit in self._entries}
        self._entry: reference_notes.ReferenceEntry | None = None
        self._note = 0
        self._missing_key: tuple[str, str] | None = None
        self._bottom = 0
        self._slide = 1.0  # 0 = yerinde, 1 = pencerenin dışında
        self._closing = False
        self._reader = None  # LessonView, ilk açılışta

        self.setProperty("role", "note-panel")
        self.hide()

        dis = QVBoxLayout(self)
        dis.setContentsMargins(0, 0, 0, 0)
        dis.setSpacing(0)

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
        self._where = QLabel()
        self._where.setProperty("role", "drawer-sub")
        self._where.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred)
        top.addWidget(self._where, 1)
        self._close_button = QPushButton()
        self._close_button.setProperty("variant", "round")
        self._close_button.setFixedSize(28, 28)
        self._close_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._close_button.clicked.connect(self.close_drawer)
        top.addWidget(self._close_button)
        dis.addWidget(ust)

        govde = QWidget()
        govde.setProperty("role", "bare")
        icerik = QVBoxLayout(govde)
        icerik.setContentsMargins(14, 12, 14, 10)
        icerik.setSpacing(SPACING["sm"])
        self._search = QLineEdit()
        self._search.setClearButtonEnabled(True)
        self._search.textChanged.connect(self._on_search)
        self._search.returnPressed.connect(self._open_first)
        self._search.installEventFilter(self)
        icerik.addWidget(self._search)

        self._pages = QStackedWidget()
        self._pages.setProperty("role", "bare")
        self._pages.addWidget(self._build_read_page())
        self._pages.addWidget(self._build_results_page())
        icerik.addWidget(self._pages, 1)
        dis.addWidget(govde, 1)

        self.set_mode(self._mode)
        self.retranslate()

    def _build_read_page(self) -> QWidget:
        sayfa = QWidget()
        sayfa.setProperty("role", "bare")
        self._read_layout = QVBoxLayout(sayfa)
        self._read_layout.setContentsMargins(0, 0, 0, 0)
        self._read_layout.setSpacing(SPACING["sm"])
        # Bölümde birden çok not varsa seçim; başvuru notu ilk sırada.
        self._picker = DropdownBox()
        self._picker.currentIndexChanged.connect(self._on_pick)
        self._picker.hide()
        self._read_layout.addWidget(self._picker)
        self._empty = QLabel()
        self._empty.setProperty("role", "drawer-sub")
        self._empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._empty.setWordWrap(True)
        self._empty.hide()
        self._read_layout.addWidget(self._empty, 1)
        return sayfa

    def _build_results_page(self) -> QWidget:
        sayfa = QWidget()
        sayfa.setProperty("role", "bare")
        duzen = QVBoxLayout(sayfa)
        duzen.setContentsMargins(0, 0, 0, 0)
        self._list = QListWidget()
        self._list.setProperty("role", "search-results")
        self._row = NoteRow(self._list)
        self._list.setItemDelegate(self._row)
        self._list.setUniformItemSizes(True)
        self._list.setMouseTracking(True)
        self._list.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._list.itemClicked.connect(self._open_item)
        self._list.itemActivated.connect(self._open_item)
        duzen.addWidget(self._list, 1)
        self._no_match = QLabel()
        self._no_match.setProperty("role", "drawer-sub")
        self._no_match.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._no_match.setWordWrap(True)
        self._no_match.hide()
        duzen.addWidget(self._no_match)
        duzen.addStretch(0)
        return sayfa

    def _ensure_reader(self):
        if self._reader is None:
            from .lesson_view import LessonView

            self._reader = LessonView(self._language, compact=True, glossary=True)
            self._reader.set_mode(self._mode)
            self._read_layout.addWidget(self._reader, 1)
        return self._reader

    # --- açma / kapama -------------------------------------------------------

    @property
    def is_open(self) -> bool:
        """Açık ya da açılıyor (kapanırken değil)."""
        return self.isVisible() and not self._closing

    def open_for(self, key: tuple[str, str] | None) -> None:
        """Çekmeceyi açar; `key` (modül, bölüm) varsa o bölümün notuyla."""
        self._search.blockSignals(True)
        self._search.clear()
        self._search.blockSignals(False)
        if key is not None and key in self._by_key:
            self._show_entry(self._by_key[key], 0)
        else:
            self._missing_key = key
            self._show_missing()
        self._closing = False
        if not self.isVisible():
            self._slide = 1.0
            self._place()
            self.show()
        self.raise_()
        if self._slide > 0:
            motion.animate(self, "slide", self._slide, 0.0, self._set_slide, "base", "out")
        if self._entry is None:
            self._search.setFocus()

    def close_drawer(self) -> None:
        if not self.is_open:
            return
        self._closing = True
        # Animasyonlar kapalıysa `on_done` hemen çağrılıyor.
        motion.animate(self, "slide", self._slide, 1.0, self._set_slide, "short", "out",
                       on_done=self._finish_close)

    def _finish_close(self) -> None:
        self.hide()
        self.closed.emit()

    def _set_slide(self, value: float) -> None:
        self._slide = value
        self._place()

    def reposition(self, bottom: int | None = None) -> None:
        """Pencere boyu değişince yer; `bottom` alttaki şeridin yüksekliği."""
        if bottom is not None:
            self._bottom = bottom
        if self.isVisible():
            self._place()

    def _place(self) -> None:
        parent = self.parentWidget()
        if parent is None:
            return
        genislik = max(MIN_WIDTH, min(MAX_WIDTH, round(parent.width() * WIDTH_SHARE)))
        boy = parent.height() - self._bottom - 2 * MARGIN
        x = parent.width() - genislik - MARGIN + round(self._slide * (genislik + 2 * MARGIN))
        self.setGeometry(x, MARGIN, genislik, max(200, boy))

    # --- içerik --------------------------------------------------------------

    def _show_entry(self, kayit: reference_notes.ReferenceEntry, note: int) -> None:
        self._entry = kayit
        self._missing_key = None
        self._note = max(0, min(note, len(kayit.documents) - 1))
        self._pages.setCurrentIndex(PAGE_READ)
        self._empty.hide()
        self._fill_picker()
        self._render_note()
        self._update_where()

    def _show_missing(self) -> None:
        """Bölümün notu yok ya da hiç bölüm açılmamış: aramaya yönlendir."""
        self._entry = None
        self._pages.setCurrentIndex(PAGE_READ)
        self._picker.hide()
        if self._reader is not None:
            self._reader.hide()
        t = self._language.t
        self._empty.setText(t("reference.no_notes" if self._missing_key else "reference.start"))
        self._empty.show()
        self._update_where()

    def _fill_picker(self) -> None:
        kayit = self._entry
        self._picker.blockSignals(True)
        self._picker.clear()
        if kayit is not None:
            for not_kaydi in kayit.documents:
                self._picker.addItem(self._language.pick(not_kaydi.get("title")))
            self._picker.setCurrentIndex(self._note)
        self._picker.blockSignals(False)
        self._picker.setVisible(kayit is not None and len(kayit.documents) > 1)

    def _on_pick(self, index: int) -> None:
        if self._entry is not None and index >= 0:
            self._note = index
            self._render_note()

    def _render_note(self) -> None:
        kayit = self._entry
        if kayit is None:
            return
        okuyucu = self._ensure_reader()
        okuyucu.show()
        dil = self._language.language
        yol = kayit.path_for(self._note, dil)
        baslik = self._language.pick(kayit.documents[self._note].get("title"))
        if yol is None or not yol.exists():
            govde = f"*{self._language.t('content.not_found', path=kayit.documents[self._note].get('file', '-'))}*"
        else:
            govde = yol.read_text(encoding="utf-8")
        # Notun görselleri ve sözlük kapsamı notun klasöründen.
        okuyucu.set_base_dir(yol.parent if yol is not None else kayit.directory)
        okuyucu.show_text(f"# {baslik}\n\n{govde}")

    def _update_where(self) -> None:
        kayit = self._entry
        if kayit is None:
            self._where.setText("")
            return
        self._where.setText(f"{self._language.pick(kayit.chapter_title)} · "
                            f"{self._language.pick(kayit.section_title)}")

    # --- arama ---------------------------------------------------------------

    def _on_search(self, text: str) -> None:
        if not text.strip():
            if self._entry is not None:
                self._pages.setCurrentIndex(PAGE_READ)
            else:
                self._show_missing()
            return
        dil = self._language.language
        sonuclar = reference_notes.search(self._entries, text, dil)
        self._list.clear()
        for kayit in sonuclar:
            notlar = ", ".join(self._language.pick(n.get("title")) for n in kayit.documents)
            item = QListWidgetItem(self._language.pick(kayit.section_title))
            item.setData(ROLE_ID, kayit.key)
            item.setData(ROLE_WHERE, f"{self._language.pick(kayit.chapter_title)} · {notlar}")
            self._list.addItem(item)
        self._no_match.setText(self._language.t("reference.no_match"))
        self._no_match.setVisible(not sonuclar)
        self._list.setVisible(bool(sonuclar))
        self._pages.setCurrentIndex(PAGE_RESULTS)

    def _open_first(self) -> None:
        if self._pages.currentIndex() == PAGE_RESULTS and self._list.count():
            self._open_item(self._list.item(0))

    def _open_item(self, item: QListWidgetItem) -> None:
        kayit = self._by_key.get(tuple(item.data(ROLE_ID)))
        if kayit is None:
            return
        self._search.blockSignals(True)
        self._search.clear()
        self._search.blockSignals(False)
        self._show_entry(kayit, 0)

    def eventFilter(self, watched, event) -> bool:  # noqa: N802
        """Arama kutusunda ↓ sonuç listesine iner (Enter ile açılır)."""
        if (watched is self._search and event.type() == QEvent.Type.KeyPress
                and event.key() == Qt.Key.Key_Down and self._pages.currentIndex() == PAGE_RESULTS
                and self._list.count()):
            self._list.setFocus()
            self._list.setCurrentRow(0)
            return True
        return super().eventFilter(watched, event)

    # --- tema ve dil -----------------------------------------------------------

    def set_mode(self, mode: str) -> None:
        self._mode = mode
        p = PALETTES.get(mode, PALETTES["dark"])
        self._head_icon.setPixmap(pixmap("file-text", p["accent"], 18))
        self._close_button.setIcon(icon("x", p["text_muted"], 15))
        self._picker.set_arrow_color(p["text_muted"])
        self._row.palette = p
        self._list.viewport().update()
        if self._reader is not None:
            self._reader.set_mode(mode)

    def retranslate(self) -> None:
        t = self._language.t
        self._heading.setText(t("reference.title"))
        self._close_button.setToolTip(t("common.close") + "  (Esc)")
        self._search.setPlaceholderText(t("reference.search"))
        if self._entry is not None:
            self._fill_picker()
            self._render_note()
            self._update_where()
            if self._search.text().strip():
                self._on_search(self._search.text())
        elif self.isVisible():
            self._show_missing()
        if self._reader is not None:
            self._reader.retranslate()
