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

from PySide6.QtCore import Property, QElapsedTimer, QEvent, QRect, QRectF, QSize, Qt, QTimer, Signal
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
from ..resources.theme.tokens import PALETTES, SPACING, RAIL_COLORS
from ..widgets.effects import apply_shadow, refresh_shadow
from ..widgets import motion
from ..widgets.empty_state import EmptyState
from ..widgets.pop_effect import pop_in, pop_out
from ..resources.logos import logo_key, logo_pixmap
from ..resources.theme.motion import out_cubic, spring

# Sonuçların sırayla gelişi: iki satır arası (ms) ve bir satırın süresi.
ROW_STAGGER = 20
ROW_ENTER = 420

CARD_WIDTH = 620
ROW_HEIGHT = 48
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
        self.catalog = None
        # Sıralı giriş saati (ms); `None` ise satırlar yerinde.
        self.enter_clock: QElapsedTimer | None = None

    def sizeHint(self, option, index) -> QSize:  # noqa: N802
        return QSize(option.rect.width(), ROW_HEIGHT)

    def paint(self, painter: QPainter, option, index) -> None:
        sonuc, kilitli = index.data(ROLE_RESULT)
        p = self.palette
        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = option.rect.adjusted(8, 0, -8, 0)
        secili = bool(option.state & QStyle.StateFlag.State_Selected)
        # Sıralı giriş: satır 8 px aşağıdan ve saydamdan gelir (ui-taslak C13).
        if self.enter_clock is not None:
            gecen = self.enter_clock.elapsed() - min(index.row(), 7) * ROW_STAGGER
            k = max(0.0, min(1.0, gecen / ROW_ENTER))
            painter.setOpacity(out_cubic(k))
            painter.translate(0, 8 * (1 - spring(k)))
        # Seçili satırın zemini listede kayan katmanda çiziliyor (_ResultList).

        item: SearchItem = sonuc.item
        chapter = self.catalog.chapter(item.target.get("chapter", "")) if self.catalog and "chapter" in item.target else None
        if "logo" in item.target:
            painter.drawPixmap(rect.left() + 12, rect.center().y() - 15,
                               logo_pixmap(item.target["logo"], item.target["color"], 30))
        elif chapter is not None and not kilitli:
            # Bölüm sonucunda patikanın logosu (E2).
            painter.drawPixmap(rect.left() + 12, rect.center().y() - 15,
                               logo_pixmap(logo_key(chapter.icon, chapter.id), chapter.color, 30))
        else:
            simge = "lock" if kilitli else item.target.get("icon") or KIND_ICONS.get(item.kind, "search")
            renk = p["accent"] if secili and not kilitli else p["text_muted"]
            painter.drawPixmap(
                rect.left() + 17, rect.center().y() - 10, icon(simge, renk, 20).pixmap(20, 20)
            )

        tur = self.kind_labels.get(item.kind, "")
        kucuk = QFont(option.font)
        kucuk.setPixelSize(12)
        hap_font = QFont(option.font)
        hap_font.setPixelSize(11)
        hap_font.setWeight(QFont.Weight.Bold)
        painter.setFont(hap_font)
        hap_genislik = painter.fontMetrics().horizontalAdvance(tur) + 20 if tur else 0
        tur_genislik = hap_genislik + 12 if tur else 0

        x = rect.left() + 54
        genislik = rect.right() - x - tur_genislik - SPACING["sm"]

        baslik_font = QFont(option.font)
        baslik_font.setPixelSize(14)
        baslik_font.setWeight(QFont.Weight.DemiBold)
        painter.setFont(baslik_font)
        painter.setPen(QColor(p["text_muted"] if kilitli else p["text"]))
        ust = QRect(x, rect.center().y() - 18, genislik, 19)
        painter.drawText(
            ust,
            int(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter),
            painter.fontMetrics().elidedText(item.title, Qt.TextElideMode.ElideRight, genislik),
        )

        ikinci = self.locked_text if kilitli else (sonuc.snippet or item.subtitle)
        painter.setFont(kucuk)
        painter.setPen(QColor(p["text_muted"]))
        alt = QRect(x, rect.center().y() + 1, genislik, 17)
        painter.drawText(
            alt,
            int(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter),
            painter.fontMetrics().elidedText(ikinci, Qt.TextElideMode.ElideRight, genislik),
        )

        if tur:
            # Tür hapı (prototip `.chip`): ikincil zemin, soluk kalın yazı.
            hap = QRectF(rect.right() - 12 - hap_genislik, rect.center().y() - 11, hap_genislik, 22)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QColor(p["surface_alt"]))
            painter.drawRoundedRect(hap, 11, 11)
            painter.setFont(hap_font)
            painter.setPen(QColor(p["text_muted"]))
            painter.drawText(hap, int(Qt.AlignmentFlag.AlignCenter), tur)
        painter.restore()


class _ResultList(QListWidget):
    """Sonuç listesi: seçili satırın zemini satırlar arasında yayla kayar."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._sel = QRectF()
        self.palette_colors = PALETTES["light"]
        self.currentRowChanged.connect(self._follow)

    def _set_sel(self, r: QRectF) -> None:
        self._sel = r
        self.viewport().update()

    def _follow(self, row: int) -> None:
        item = self.item(row)
        if item is None:
            return
        hedef = QRectF(self.visualItemRect(item)).adjusted(8, 0, -8, 0)
        if self._sel.isEmpty():
            self._set_sel(hedef)
            return
        motion.animate(self, "sel", QRectF(self._sel), hedef, self._set_sel, "spring", "spring")

    def resizeEvent(self, event) -> None:  # noqa: N802
        super().resizeEvent(event)
        # Vurgu liste son genişliğine gelmeden hesaplanınca satırın yarısında
        # kalıyordu; boyut değişince yerine oturuyor (kaymadan).
        item = self.currentItem()
        if item is not None:
            motion.stop(self, "sel")
            self._set_sel(QRectF(self.visualItemRect(item)).adjusted(8, 0, -8, 0))

    def reset_selection(self) -> None:
        motion.stop(self, "sel")
        self._sel = QRectF()

    def paintEvent(self, event) -> None:  # noqa: N802
        if not self._sel.isEmpty():
            g = QPainter(self.viewport())
            g.setRenderHint(QPainter.RenderHint.Antialiasing)
            p = self.palette_colors
            g.setPen(QColor(p["accent"]).lighter(100))
            renk = QColor(p["accent"])
            renk.setAlphaF(0.30)
            g.setPen(renk)
            g.setBrush(QColor(p["accent_soft"]))
            g.drawRoundedRect(self._sel, 12, 12)
            g.end()
        super().paintEvent(event)


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
        row.setContentsMargins(18, 12, 16, 12)
        row.setSpacing(12)
        self._glass = QLabel()
        row.addWidget(self._glass)
        self._field = QLineEdit()
        self._field.setProperty("role", "search-field")
        self._field.textChanged.connect(self._update)
        self._field.installEventFilter(self)
        row.addWidget(self._field, 1)
        esc = QLabel("Esc")
        esc.setProperty("role", "kbd")
        row.addWidget(esc, 0, Qt.AlignmentFlag.AlignVCenter)
        column.addWidget(top)

        self._rule = QFrame()
        self._rule.setProperty("role", "divider")
        self._rule.setFixedHeight(1)
        column.addWidget(self._rule)

        self._list = _ResultList()
        self._list.setProperty("role", "search-results")
        self._delegate = _ResultDelegate(self._list)
        self._list.setItemDelegate(self._delegate)
        self._list.setUniformItemSizes(True)
        self._list.setMouseTracking(True)
        self._list.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self._list.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._list.itemClicked.connect(self._activate_item)
        # Fare hangi satırdaysa seçim oraya kayar (prototip `onmouseenter`).
        self._list.entered.connect(lambda index: self._list.setCurrentRow(index.row()))
        column.addWidget(self._list)

        # Sonuç yoksa boş durum kartı (B10).
        self._empty = EmptyState()
        self._empty.setContentsMargins(SPACING["lg"], SPACING["md"], SPACING["lg"], SPACING["md"])
        column.addWidget(self._empty)
        self._dim = 0.0
        self._rise = 0.0
        self._closing = False
        self._enter_timer = QTimer(self)
        self._enter_timer.setInterval(16)
        self._enter_timer.timeout.connect(self._tick_enter)

        # Alt şerit (prototip `.foot`): tuş kutucukları ve ne yaptıkları.
        self._hint = QFrame()
        self._hint.setProperty("role", "search-hint")
        alt = QHBoxLayout(self._hint)
        alt.setContentsMargins(16, 9, 16, 9)
        alt.setSpacing(4)
        self._hint_labels: list[QLabel] = []
        for tuslar in (("↑", "↓"), ("Enter",), ("Esc",)):
            for tus in tuslar:
                k = QLabel(tus)
                k.setProperty("role", "kbd")
                alt.addWidget(k)
            yazi = QLabel()
            yazi.setProperty("role", "search-hint-text")
            alt.addWidget(yazi)
            alt.addSpacing(12)
            self._hint_labels.append(yazi)
        alt.addStretch(1)
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
        self._closing = False
        self._update()
        self.show()
        self.raise_()
        self._field.setFocus()
        # Arka plan kararır; kutu saydamlıktan belirir, %96'dan büyür ve
        # 10 px aşağıdan yayla yerine oturur (prototip `.palette.on`).
        self._rise = 0.0
        self._place()
        motion.animate_property(self, "dim", 1.0, "short", "out", start=0.0)
        pop_in(self._card)

    def close_palette(self) -> None:
        if not self.isVisible() or self._closing:
            return
        self._closing = True
        pop_out(self._card)
        motion.animate_property(self, "dim", 0.0, "short", "in", on_done=self._finish_close)

    def _finish_close(self) -> None:
        self._closing = False
        self._enter_timer.stop()
        self.hide()

    def _get_dim(self) -> float:
        return self._dim

    def _set_dim(self, v: float) -> None:
        self._dim = v
        self.update()

    dim = Property(float, _get_dim, _set_dim)

    def _get_rise(self) -> float:
        return self._rise

    def _set_rise(self, v: float) -> None:
        self._rise = v
        self._place()

    rise = Property(float, _get_rise, _set_rise)

    def _tick_enter(self) -> None:
        self._list.viewport().update()
        clock = self._delegate.enter_clock
        if clock is None or clock.elapsed() > ROW_ENTER + 8 * ROW_STAGGER:
            self._delegate.enter_clock = None
            self._enter_timer.stop()
            self._list.viewport().update()

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
            # Boşken prototipteki gibi: patikalar, ekranlar, en fazla 8 satır.
            sonuclar = [SearchResult(item, 0) for item in self._items
                        if item.kind in ("track", "screen")][:8]

        self._list.clear()
        self._list.reset_selection()
        if motion.enabled():
            saat = QElapsedTimer()
            saat.start()
            self._delegate.enter_clock = saat
            self._enter_timer.start()
        for sonuc in sonuclar:
            satir = QListWidgetItem()
            satir.setData(ROLE_RESULT, (sonuc, self._is_locked(sonuc.item.target)))
            self._list.addItem(satir)

        bos = not sonuclar
        self._list.setVisible(not bos)
        self._rule.setVisible(True)
        self._empty.setVisible(bos)
        if bos:
            renk = PALETTES.get(self._mode, PALETTES["light"])["accent"]
            self._empty.set_content("search", renk, self._language.t("search.empty_title"),
                                    self._language.t("search.empty", query=sorgu.strip()))
        else:
            self._list.setCurrentRow(0)
            self._list.setFixedHeight(min(len(sonuclar), MAX_ROWS) * ROW_HEIGHT + SPACING["sm"])
        self._place()

    def _place(self) -> None:
        genislik = min(CARD_WIDTH, self.width() - SPACING["xxl"] * 2)
        self._card.setFixedWidth(max(genislik, 320))
        self._card.adjustSize()
        x = (self.width() - self._card.width()) // 2
        y = int(self.height() * TOP_RATIO + getattr(self, "_rise", 0.0))
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
        painter.fillRect(self.rect(), QColor(0, 0, 0, int(DIM_ALPHA * self._dim)))
        painter.end()

    def resizeEvent(self, event) -> None:  # noqa: N802
        super().resizeEvent(event)
        self._place()

    # --- tema ve dil ------------------------------------------------------

    def set_mode(self, mode: str) -> None:
        self._mode = mode
        palette = PALETTES.get(mode, PALETTES["light"])
        self._delegate.palette = palette
        self._list.palette_colors = palette
        renk = RAIL_COLORS.get(mode, RAIL_COLORS["light"]).get("search", palette["accent"])
        self._glass.setPixmap(icon("search", renk, 22).pixmap(22, 22))
        refresh_shadow(self._card, mode, strong=True)
        self._list.viewport().update()

    def retranslate(self) -> None:
        t = self._language.t
        self._field.setPlaceholderText(t("search.placeholder"))
        for yazi, anahtar in zip(self._hint_labels, ("search.hint_select", "search.hint_open", "search.hint_close")):
            yazi.setText(t(anahtar))
        self._delegate.kind_labels = {
            kind: t(f"search.kind.{kind}")
            for kind in ("section", "lesson", "course_note", "exercise", "note", "screen", "track")
        }
        self._delegate.locked_text = t("search.locked")
