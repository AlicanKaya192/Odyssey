"""Hızlı başvuru çekmecesi: kişinin kendi başvuru kartı, her ekrandan.

Alt şeritteki düğme ya da `Ctrl+R` ile sağdan kayarak açılıyor. Kartta kişinin
dersten, ders notundan ya da alıştırma yönergesinden seçip sağ tıkla eklediği
parçalar duruyor (`DocumentView.card_requested`, kayıt `reference_cards`).
Açık bölümünkiler (bölüm dışındayken en son açılanınkiler) üstte; arama
bütün kartta. Her parçada kopyala ve kaldır.

27 Ekim'e kadar çekmece bölümün ders notlarını ikinci kez gösteriyordu; kişi
onları kendi notu sanıp silmeye çalıştı (Alican). Şimdi kart boşken yalnızca
nasıl ekleneceği ve bölümün başvuru notuna bir bağlantı var; not, bölümün
Ders Notu sekmesinde açılıyor.

**Kip değil, dışarı tıklayınca kapanmıyor.** Asıl kullanımı alıştırma
yazarken karta bakmak: editöre tıklamak çekmeceyi kapatsaydı her bakışta
yeniden açmak gerekirdi. Kapatmak: çarpı, `Esc`, `Ctrl+R`, düğme.

**Pencerenin içinde bir katman** (kısayol paneli gibi), ayrı pencere değil.
"""

from __future__ import annotations

from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from ..core.catalog import Catalog
from ..core.language import LanguageManager
from ..core.progress import ProgressStore
from ..core.reference_notes import reference_note
from ..core.search import fold
from ..resources.icons import icon, pixmap
from ..resources.theme.tokens import PALETTES, SPACING
from ..widgets import motion

# Genişlik: pencerenin en fazla bu oranı, en az / en çok bu kadar piksel.
WIDTH_SHARE = 0.42
MIN_WIDTH = 380
MAX_WIDTH = 520
# Pencere kenarlarıyla arası (bölümdeki not paneli gibi yüzen kart).
MARGIN = 12
# "Kopyalandı" işaretinin süresi (ms).
COPIED_MS = 1200

PAGE_LIST = 0
PAGE_EMPTY = 1


class CardPiece(QFrame):
    """Karttaki tek parça: bölümün adı, metin ya da kod, kopyala ve kaldır."""

    removed = Signal(int)

    def __init__(self, card: dict, where: str, language: LanguageManager, palette: dict) -> None:
        super().__init__()
        self.card = card
        self._language = language
        self._palette = palette
        self.setProperty("role", "ref-card")

        duzen = QVBoxLayout(self)
        duzen.setContentsMargins(12, 8, 8, 12)
        duzen.setSpacing(6)

        ust = QHBoxLayout()
        ust.setSpacing(2)
        self.where = QLabel(where)
        self.where.setProperty("role", "drawer-sub")
        self.where.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred)
        ust.addWidget(self.where, 1)
        self.copy_button = self._small_button(self._copy)
        self.remove_button = self._small_button(lambda: self.removed.emit(self.card["id"]))
        ust.addWidget(self.copy_button)
        ust.addWidget(self.remove_button)
        duzen.addLayout(ust)

        self.body = QLabel(card["body"])
        self.body.setProperty("role", "ref-code" if card["is_code"] else "ref-body")
        self.body.setTextFormat(Qt.TextFormat.PlainText)
        self.body.setWordWrap(True)
        self.body.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        # Uzun kod satırı kartı genişletmesin; sığmayan kısım kırpılıyor.
        self.body.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred)
        duzen.addWidget(self.body)

        self._copied = QTimer(self)
        self._copied.setSingleShot(True)
        self._copied.timeout.connect(self._paint_buttons)
        self._paint_buttons()

    def set_palette(self, palette: dict) -> None:
        self._palette = palette
        self._paint_buttons()

    def _small_button(self, slot) -> QPushButton:
        dugme = QPushButton()
        dugme.setProperty("variant", "round")
        dugme.setFixedSize(26, 26)
        dugme.setCursor(Qt.CursorShape.PointingHandCursor)
        dugme.clicked.connect(slot)
        return dugme

    def _copy(self) -> None:
        QApplication.clipboard().setText(self.card["body"])
        self._copied.start(COPIED_MS)
        self._paint_buttons()

    def _paint_buttons(self) -> None:
        p, t = self._palette, self._language.t
        kopyalandi = self._copied.isActive()
        self.copy_button.setIcon(icon("check" if kopyalandi else "clipboard",
                                      p["success"] if kopyalandi else p["text_muted"], 14))
        self.copy_button.setToolTip(t("reference.copied" if kopyalandi else "reference.copy"))
        self.remove_button.setIcon(icon("trash", p["text_muted"], 14))
        self.remove_button.setToolTip(t("reference.remove"))


class ReferenceDrawer(QFrame):
    """Sağda yüzen başvuru kartı."""

    closed = Signal()
    # Boş karttaki bağlantı: (modül, bölüm, Ders Notu sekmesindeki sırası).
    note_requested = Signal(str, str, int)

    def __init__(self, catalog: Catalog, store: ProgressStore, language: LanguageManager,
                 parent: QWidget) -> None:
        super().__init__(parent)
        self._catalog = catalog
        self._store = store
        self._language = language
        self._mode = "dark"
        self._key: tuple[str, str] | None = None
        self._cards: list[dict] = []
        self._pieces: list[CardPiece] = []
        self._bottom = 0
        self._slide = 1.0  # 0 = yerinde, 1 = pencerenin dışında
        self._closing = False

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
        self._search.textChanged.connect(lambda _metin: self._fill_list())
        icerik.addWidget(self._search)

        self._pages = QStackedWidget()
        self._pages.setProperty("role", "bare")
        self._pages.addWidget(self._build_list_page())
        self._pages.addWidget(self._build_empty_page())
        icerik.addWidget(self._pages, 1)
        dis.addWidget(govde, 1)

        self.set_mode(self._mode)
        self.retranslate()

    def _build_list_page(self) -> QWidget:
        self._list_body = QWidget()
        self._list_body.setProperty("role", "bare")
        self._list_layout = QVBoxLayout(self._list_body)
        self._list_layout.setContentsMargins(0, 0, 4, 0)
        self._list_layout.setSpacing(SPACING["sm"])
        self._list_layout.addStretch(1)
        alan = QScrollArea()
        alan.setProperty("role", "bare")
        alan.setWidgetResizable(True)
        alan.setFrameShape(QFrame.Shape.NoFrame)
        alan.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        alan.setWidget(self._list_body)
        alan.viewport().setProperty("role", "bare")
        self._scroll = alan
        return alan

    def _build_empty_page(self) -> QWidget:
        sayfa = QWidget()
        sayfa.setProperty("role", "bare")
        duzen = QVBoxLayout(sayfa)
        duzen.setContentsMargins(8, 0, 8, 0)
        duzen.setSpacing(SPACING["md"])
        duzen.addStretch(1)
        self._empty = QLabel()
        self._empty.setProperty("role", "drawer-sub")
        self._empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._empty.setWordWrap(True)
        duzen.addWidget(self._empty)
        self._note_link = QPushButton()
        self._note_link.setProperty("variant", "small")
        self._note_link.setCursor(Qt.CursorShape.PointingHandCursor)
        self._note_link.clicked.connect(self._open_note)
        duzen.addWidget(self._note_link, 0, Qt.AlignmentFlag.AlignHCenter)
        duzen.addStretch(2)
        return sayfa

    # --- açma / kapama -------------------------------------------------------

    @property
    def is_open(self) -> bool:
        """Açık ya da açılıyor (kapanırken değil)."""
        return self.isVisible() and not self._closing

    def open_for(self, key: tuple[str, str] | None) -> None:
        """Çekmeceyi açar; `key` (modül, bölüm) parçaları üste alınan bölüm."""
        self._key = key
        self._search.blockSignals(True)
        self._search.clear()
        self._search.blockSignals(False)
        self.refresh()
        self._closing = False
        if not self.isVisible():
            self._slide = 1.0
            self._place()
            self.show()
        self.raise_()
        if self._slide > 0:
            motion.animate(self, "slide", self._slide, 0.0, self._set_slide, "base", "out")

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

    def refresh(self) -> None:
        """Parçaları veritabanından yeniden okur (eklenince, kaldırılınca)."""
        self._cards = self._store.cards()
        self._update_where()
        self._search.setVisible(bool(self._cards))
        if not self._cards:
            self._show_empty()
            return
        self._pages.setCurrentIndex(PAGE_LIST)
        self._fill_list()

    def _section_name(self, chapter_id: str, section_id: str) -> str:
        bolum = self._catalog.section(chapter_id, section_id)
        return self._language.pick(bolum.title) if bolum is not None else section_id

    def _update_where(self) -> None:
        if self._key is None or self._catalog.section(*self._key) is None:
            self._where.setText("")
            return
        modul = self._catalog.chapter(self._key[0])
        self._where.setText(f"{self._language.pick(modul.title) if modul else ''} · "
                            f"{self._section_name(*self._key)}")

    def _show_empty(self) -> None:
        t = self._language.t
        self._empty.setText(t("reference.empty"))
        bolum = self._catalog.section(*self._key) if self._key is not None else None
        not_ = reference_note(bolum) if bolum is not None else None
        if not_ is not None:
            self._note_link.setText(t("reference.open_note", title=self._language.pick(not_[1].get("title"))))
        self._note_link.setVisible(not_ is not None)
        self._pages.setCurrentIndex(PAGE_EMPTY)

    def _open_note(self) -> None:
        bolum = self._catalog.section(*self._key) if self._key is not None else None
        not_ = reference_note(bolum) if bolum is not None else None
        if not_ is not None:
            self.note_requested.emit(self._key[0], self._key[1], not_[0])

    def _matches(self, card: dict, words: list[str]) -> bool:
        modul = self._catalog.chapter(card["chapter_id"])
        metin = fold(" ".join((card["body"], self._section_name(card["chapter_id"], card["section_id"]),
                               self._language.pick(modul.title) if modul else "")))
        return all(kelime in metin for kelime in words)

    def _fill_list(self) -> None:
        if not self._cards:
            return
        kelimeler = fold(self._search.text()).split()
        secilen = [kart for kart in self._cards if not kelimeler or self._matches(kart, kelimeler)]
        burada = [k for k in secilen if self._key and (k["chapter_id"], k["section_id"]) == self._key]
        oteki = [k for k in secilen if k not in burada]

        while self._list_layout.count() > 1:  # sondaki esneme kalıyor
            oge = self._list_layout.takeAt(0)
            if oge.widget() is not None:
                oge.widget().deleteLater()
        self._pieces = []

        t = self._language.t
        p = PALETTES.get(self._mode, PALETTES["dark"])
        ikisi = bool(burada) and bool(oteki)
        for baslik, grup in (("reference.group_here", burada), ("reference.group_other", oteki)):
            if not grup:
                continue
            if ikisi:
                self._add_row(self._group_label(t(baslik)))
            for kart in grup:
                parca = CardPiece(kart, self._section_name(kart["chapter_id"], kart["section_id"]),
                                  self._language, p)
                parca.removed.connect(self._remove)
                self._pieces.append(parca)
                self._add_row(parca)
        if not secilen:
            bos = QLabel(t("reference.no_match"))
            bos.setProperty("role", "drawer-sub")
            bos.setAlignment(Qt.AlignmentFlag.AlignCenter)
            bos.setWordWrap(True)
            self._add_row(bos)

    def _group_label(self, text: str) -> QLabel:
        etiket = QLabel(text)
        etiket.setProperty("role", "ref-group")
        return etiket

    def _add_row(self, widget: QWidget) -> None:
        self._list_layout.insertWidget(self._list_layout.count() - 1, widget)

    def _remove(self, card_id: int) -> None:
        self._store.remove_card(card_id)
        kaydirma = self._scroll.verticalScrollBar().value()
        self._cards = [kart for kart in self._cards if kart["id"] != card_id]
        self._search.setVisible(bool(self._cards))
        if not self._cards:
            self._search.clear()
            self._show_empty()
            return
        self._fill_list()
        QTimer.singleShot(0, lambda: self._scroll.verticalScrollBar().setValue(kaydirma))

    # --- tema ve dil -----------------------------------------------------------

    def set_mode(self, mode: str) -> None:
        self._mode = mode
        p = PALETTES.get(mode, PALETTES["dark"])
        self._head_icon.setPixmap(pixmap("file-text", p["accent"], 18))
        self._close_button.setIcon(icon("x", p["text_muted"], 15))
        for parca in self._pieces:
            parca.set_palette(p)

    def retranslate(self) -> None:
        t = self._language.t
        self._heading.setText(t("reference.title"))
        self._close_button.setToolTip(t("common.close") + "  (Esc)")
        self._search.setPlaceholderText(t("reference.search"))
        # Parçaların metni kişinin seçtiği dilde kalıyor; bölüm adları ve
        # öteki yazılar yeni dilde yeniden kuruluyor.
        if self.isVisible():
            self.refresh()
