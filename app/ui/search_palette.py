"""Genel arama kutusu (`Ctrl+K`): ekranın üst ortasında yüzen kutu.

macOS'teki Spotlight gibi: arka plan kararıyor, kutu ortada; yazdıkça
altında öneriler çıkıyor. Ok tuşlarıyla seçilip Enter'la ya da tıklanarak
gidiliyor; Esc ya da kutunun dışına tıklamak kapatıyor. Boşken ekranlar ve
"Kaldığın yerden devam et" öneriliyor.

Arama bu kutunun işi değil (`app/core/search.py`); kutu dizini ana
pencereden alıyor (`set_provider`) ve yalnızca gösteriyor. Kilitli bir
bölüme götüren sonuç soluk ve "Kilitli" diye çiziliyor, basılınca bir
şey olmuyor: açılmayan bir yere göndermek kafa karıştırıyordu.

Satırlar bir çizim yardımcısıyla (`_ResultDelegate`) çiziliyor: simge, ad,
altında yer ya da metnin eşleşen parçası, sağda türü.
"""

from __future__ import annotations

from typing import Callable

from PySide6.QtCore import QEvent, QRect, QSize, Qt, Signal
from PySide6.QtGui import QColor, QFont, QPainter
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QStyle,
    QStyledItemDelegate,
    QVBoxLayout,
    QWidget,
)

from ..core.language import LanguageManager
from ..core.search import SearchItem, SearchResult, search
from ..resources.icons import icon
from ..resources.theme.tokens import PALETTES, SPACING
from ..widgets.effects import apply_shadow, refresh_shadow

CARD_WIDTH = 680
ROW_HEIGHT = 58
MAX_ROWS = 8
# Kutunun tepesi pencere yüksekliğinin bu oranında.
TOP_RATIO = 0.14
DIM_ALPHA = 110

KIND_ICONS = {
    "section": "book",
    "lesson": "file-text",
    "course_note": "clipboard",
    "exercise": "code",
    "note": "notebook",
    "screen": "chevron-right",
}

ROLE_RESULT = Qt.ItemDataRole.UserRole


class _ResultDelegate(QStyledItemDelegate):
    """Bir sonuç satırı: simge, ad, ikinci satır, sağda tür."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.palette = PALETTES["light"]
        self.kind_labels: dict[str, str] = {}
        self.locked_text = ""

    def sizeHint(self, option, index) -> QSize:  # noqa: N802
        return QSize(option.rect.width(), ROW_HEIGHT)

    def paint(self, painter: QPainter, option, index) -> None:
        sonuc, kilitli = index.data(ROLE_RESULT)
        p = self.palette
        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = option.rect.adjusted(SPACING["sm"], 2, -SPACING["sm"], -2)
        secili = bool(option.state & QStyle.StateFlag.State_Selected)
        ustunde = bool(option.state & QStyle.StateFlag.State_MouseOver)
        if secili or ustunde:
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QColor(p["accent_soft"] if secili else p["surface_hover"]))
            painter.drawRoundedRect(rect, 10, 10)

        item: SearchItem = sonuc.item
        simge = "lock" if kilitli else item.target.get("icon") or KIND_ICONS.get(item.kind, "search")
        renk = p["accent"] if secili and not kilitli else p["text_muted"]
        painter.drawPixmap(
            rect.left() + 14, rect.center().y() - 10, icon(simge, renk, 20).pixmap(20, 20)
        )

        tur = self.kind_labels.get(item.kind, "")
        kucuk = QFont(option.font)
        kucuk.setPixelSize(12)
        painter.setFont(kucuk)
        tur_genislik = painter.fontMetrics().horizontalAdvance(tur) + SPACING["md"] if tur else 0

        x = rect.left() + 48
        genislik = rect.right() - x - tur_genislik - SPACING["sm"]

        baslik_font = QFont(option.font)
        baslik_font.setPixelSize(14)
        baslik_font.setWeight(QFont.Weight.DemiBold)
        painter.setFont(baslik_font)
        painter.setPen(QColor(p["text_muted"] if kilitli else p["text"]))
        ust = QRect(x, rect.top() + 8, genislik, 20)
        painter.drawText(
            ust,
            int(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter),
            painter.fontMetrics().elidedText(item.title, Qt.TextElideMode.ElideRight, genislik),
        )

        ikinci = self.locked_text if kilitli else (sonuc.snippet or item.subtitle)
        painter.setFont(kucuk)
        painter.setPen(QColor(p["text_muted"]))
        alt = QRect(x, rect.top() + 29, genislik, 18)
        painter.drawText(
            alt,
            int(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter),
            painter.fontMetrics().elidedText(ikinci, Qt.TextElideMode.ElideRight, genislik),
        )

        if tur:
            painter.drawText(
                rect.adjusted(0, 0, -SPACING["md"], 0),
                int(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter),
                tur,
            )
        painter.restore()


class SearchPalette(QWidget):
    """Pencerenin üstüne açılan arama katmanı."""

    # Seçilen sonucun `target` sözlüğü.
    activated = Signal(dict)

    def __init__(self, language: LanguageManager, parent: QWidget) -> None:
        super().__init__(parent)
        self._language = language
        self._mode = "light"
        self._provider: Callable[[], list[SearchItem]] | None = None
        self._is_locked: Callable[[dict], bool] = lambda _target: False
        self._items: list[SearchItem] = []
        self.hide()

        self._card = QFrame(self)
        self._card.setProperty("role", "search-card")
        apply_shadow(self._card, self._mode, strong=True)

        column = QVBoxLayout(self._card)
        column.setContentsMargins(0, 0, 0, 0)
        column.setSpacing(0)

        top = QWidget()
        top.setProperty("role", "bare")
        row = QHBoxLayout(top)
        row.setContentsMargins(SPACING["lg"], SPACING["md"], SPACING["lg"], SPACING["md"])
        row.setSpacing(SPACING["md"])
        self._glass = QLabel()
        row.addWidget(self._glass)
        self._field = QLineEdit()
        self._field.setProperty("role", "search-field")
        self._field.textChanged.connect(self._update)
        self._field.installEventFilter(self)
        row.addWidget(self._field, 1)
        column.addWidget(top)

        self._rule = QFrame()
        self._rule.setProperty("role", "divider")
        self._rule.setFixedHeight(1)
        column.addWidget(self._rule)

        self._list = QListWidget()
        self._list.setProperty("role", "search-results")
        self._delegate = _ResultDelegate(self._list)
        self._list.setItemDelegate(self._delegate)
        self._list.setUniformItemSizes(True)
        self._list.setMouseTracking(True)
        self._list.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self._list.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._list.itemClicked.connect(self._activate_item)
        column.addWidget(self._list)

        self._empty = QLabel()
        self._empty.setProperty("role", "muted")
        self._empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._empty.setWordWrap(True)
        self._empty.setContentsMargins(SPACING["lg"], SPACING["lg"], SPACING["lg"], SPACING["lg"])
        column.addWidget(self._empty)

        self._hint = QLabel()
        self._hint.setProperty("role", "search-hint")
        self._hint.setContentsMargins(SPACING["lg"], SPACING["sm"], SPACING["lg"], SPACING["sm"])
        column.addWidget(self._hint)

        self.retranslate()
        self.set_mode(self._mode)

    # --- dışarıdan --------------------------------------------------------

    def set_provider(
        self, provider: Callable[[], list[SearchItem]], is_locked: Callable[[dict], bool]
    ) -> None:
        """Dizini veren fonksiyon ve bir sonucun kilitli olup olmadığını söyleyen."""
        self._provider = provider
        self._is_locked = is_locked

    def open(self) -> None:
        """Kutuyu açar; dizin her açılışta tazeleniyor (notlar değişmiş olabilir)."""
        self._items = self._provider() if self._provider else []
        parent = self.parentWidget()
        if parent is not None:
            self.setGeometry(parent.rect())
        self._field.blockSignals(True)
        self._field.clear()
        self._field.blockSignals(False)
        self._update()
        self.show()
        self.raise_()
        self._field.setFocus()

    def close_palette(self) -> None:
        self.hide()

    def toggle(self) -> None:
        if self.isVisible():
            self.close_palette()
        else:
            self.open()

    # --- iç işler ---------------------------------------------------------

    def _update(self) -> None:
        sorgu = self._field.text()
        if sorgu.strip():
            sonuclar = search(sorgu, self._items)
        else:
            sonuclar = [SearchResult(item, 0) for item in self._items if item.kind == "screen"]

        self._list.clear()
        for sonuc in sonuclar:
            satir = QListWidgetItem()
            satir.setData(ROLE_RESULT, (sonuc, self._is_locked(sonuc.item.target)))
            self._list.addItem(satir)

        bos = not sonuclar
        self._list.setVisible(not bos)
        self._rule.setVisible(True)
        self._empty.setVisible(bos)
        if bos:
            self._empty.setText(self._language.t("search.empty", query=sorgu.strip()))
        else:
            self._list.setCurrentRow(0)
            self._list.setFixedHeight(min(len(sonuclar), MAX_ROWS) * ROW_HEIGHT + SPACING["sm"])
        self._place()

    def _place(self) -> None:
        genislik = min(CARD_WIDTH, self.width() - SPACING["xxl"] * 2)
        self._card.setFixedWidth(max(genislik, 320))
        self._card.adjustSize()
        x = (self.width() - self._card.width()) // 2
        y = int(self.height() * TOP_RATIO)
        self._card.move(x, y)

    def _move(self, delta: int) -> None:
        if not self._list.isVisible() or self._list.count() == 0:
            return
        row = (self._list.currentRow() + delta) % self._list.count()
        self._list.setCurrentRow(row)

    def _activate_item(self, item: QListWidgetItem | None) -> None:
        if item is None:
            return
        sonuc, kilitli = item.data(ROLE_RESULT)
        if kilitli:
            return
        self.close_palette()
        self.activated.emit(sonuc.item.target)

    def eventFilter(self, obj, event) -> bool:  # noqa: N802
        if obj is self._field and event.type() == QEvent.Type.KeyPress:
            key = event.key()
            if key == Qt.Key.Key_Down:
                self._move(1)
                return True
            if key == Qt.Key.Key_Up:
                self._move(-1)
                return True
            if key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
                self._activate_item(self._list.currentItem())
                return True
            if key == Qt.Key.Key_Escape:
                self.close_palette()
                return True
        return super().eventFilter(obj, event)

    def mousePressEvent(self, event) -> None:  # noqa: N802
        # Kutunun dışına tıklamak kapatıyor.
        if not self._card.geometry().contains(event.position().toPoint()):
            self.close_palette()
            return
        super().mousePressEvent(event)

    def paintEvent(self, event) -> None:  # noqa: N802
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(0, 0, 0, DIM_ALPHA))
        painter.end()

    def resizeEvent(self, event) -> None:  # noqa: N802
        super().resizeEvent(event)
        self._place()

    # --- tema ve dil ------------------------------------------------------

    def set_mode(self, mode: str) -> None:
        self._mode = mode
        palette = PALETTES.get(mode, PALETTES["light"])
        self._delegate.palette = palette
        self._glass.setPixmap(icon("search", palette["text_muted"], 22).pixmap(22, 22))
        refresh_shadow(self._card, mode, strong=True)
        self._list.viewport().update()

    def retranslate(self) -> None:
        t = self._language.t
        self._field.setPlaceholderText(t("search.placeholder"))
        self._hint.setText(t("search.hint"))
        self._delegate.kind_labels = {
            kind: t(f"search.kind.{kind}")
            for kind in ("section", "lesson", "course_note", "exercise", "note", "screen")
        }
        self._delegate.locked_text = t("search.locked")
