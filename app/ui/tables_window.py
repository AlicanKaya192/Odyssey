"""SQL alıştırmalarında veritabanının o anki hâlini gösteren pencere.

Sorgu yazarken en çok sorulan şey "elimde ne var": hangi tablolar duruyor,
sütunları ne, içinde ne yazıyor. Yönergeye bakmak yetmiyor, çünkü kişi
kendi tablosunu da yaratıyor.

**Gösterilen şey son çalıştırmanın sonundaki hâl.** Anlık görüntü
öğrencinin SQL'i çalıştıktan sonra, geri almadan önce alınıyor; yani
`CREATE TABLE` yazdıysa kendi tablosu da burada görünüyor. Geri almadan
sonra bakmak yalnızca hazır veriyi gösterirdi ve "benim tablom nerede"
sorusunu doğururdu.

Tablolar **alt alta değil, sekmeli** duruyor. İleri bölümlerde bir
alıştırmanın sekiz ya da daha fazla tablosu olacak; hepsini tek sayfaya
dizmek, üçüncü tabloyu görmek için sayfayı metrelerce kaydırmak demek.

Bir tablo **ayrı pencereye taşınabiliyor**: iki tabloyu yan yana koymadan
`JOIN` yazmak zor. Taşınan pencereler her çalıştırmada kendiliğinden
tazeleniyor.

Pencereler **kip değil**: açıkken editörde yazmaya devam edilebiliyor.
Ayarlar penceresinin aksine başlık çubuğu duruyor, çünkü bunlar bir işi
bitirmek için değil, yanında açık kalması için var — taşınması ve
boyutlandırılması gerekiyor.
"""

from __future__ import annotations

import html

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QFrame,
    QHBoxLayout,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from ..core.language import LanguageManager
from ..resources.theme.tokens import SPACING
from ..widgets.document_view import DocumentView
from ..widgets.segmented import SegmentedControl

# Ana pencerenin açılış boyutu. Editörün yanında durabilecek kadar dar,
# dört sütunlu bir tabloyu kaydırmadan gösterecek kadar geniş.
BASLANGIC_GENISLIK = 620
BASLANGIC_YUKSEKLIK = 700

# Ayrılan pencereler daha küçük açılıyor: birden fazlası aynı anda
# ekranda duracak.
AYRIK_GENISLIK = 520
AYRIK_YUKSEKLIK = 460

# Her yeni pencere bir öncekinden bu kadar kaydırılıyor, yoksa üst üste
# açılıp tek pencere gibi görünüyorlar.
BASAMAK = 28


def _hucre(value: object) -> str:
    """Bir hücreyi tabloya yazılacak metne çevirir."""
    if value is None:
        # Boş dizeyle karıştırılmasın: SQL'de ikisi ayrı şey ve bu ayrım
        # ilerideki bölümlerin (NULL kontrolü) konusu.
        return "<i>NULL</i>"
    return html.escape(str(value))


def table_html(table: dict, language: LanguageManager) -> str:
    """Tek bir tabloyu HTML'e çevirir.

    Belge alanı (`DocumentView`) kullanılıyor, `QTableWidget` değil: tablo
    stili zaten ders sayfalarında tanımlı ve temayla birlikte değişiyor.
    Qt'nin tablo widget'ı için ayrıca stil yazmak gerekirdi.
    """
    toplam = int(table.get("total", 0))
    satirlar = table.get("rows", [])
    parcalar = [
        f"<p class='meta'>{html.escape(language.t('tables.row_count', count=toplam))}</p>"
    ]

    hata = table.get("error")
    if hata:
        return f"<p>{html.escape(str(hata))}</p>"

    sutunlar = table.get("columns", [])
    if not sutunlar:
        return "".join(parcalar)

    basliklar = "".join(f"<th>{html.escape(str(c))}</th>" for c in sutunlar)
    govde = "".join(
        "<tr>" + "".join(f"<td>{_hucre(h)}</td>" for h in satir) + "</tr>"
        for satir in satirlar
    )
    parcalar.append(
        f"<table><thead><tr>{basliklar}</tr></thead><tbody>{govde}</tbody></table>"
    )

    if toplam > len(satirlar):
        parcalar.append(
            "<p class='meta'>"
            + html.escape(
                language.t("tables.truncated", shown=len(satirlar), total=toplam)
            )
            + "</p>"
        )
    return "".join(parcalar)


def _wrap(body: str) -> str:
    """Gövdeyi diğer belge ekranlarıyla aynı düzene sarar."""
    return f"<div class='page compact'><div class='content'>{body}</div></div>"


class _DocumentWindow(QDialog):
    """Belge alanı taşıyan, kip olmayan pencerelerin ortak yanı."""

    def __init__(
        self,
        language: LanguageManager,
        parent: QWidget | None = None,
        mode: str = "dark",
    ) -> None:
        super().__init__(parent)
        self._language = language
        self.setModal(False)
        self.setWindowFlag(Qt.WindowType.Window, True)

        self._outer = QVBoxLayout(self)
        self._outer.setContentsMargins(0, 0, 0, 0)
        self._outer.setSpacing(0)

        self._document = DocumentView(self, mode)

    def set_mode(self, mode: str) -> None:
        self._document.set_mode(mode)

    def _show(self, body: str) -> None:
        self._document.set_lang(self._language.language)
        self._document.set_body(_wrap(body))


class TableWindow(_DocumentWindow):
    """Tek bir tabloyu gösteren, ayrılmış pencere."""

    def __init__(
        self,
        name: str,
        language: LanguageManager,
        parent: QWidget | None = None,
        mode: str = "dark",
    ) -> None:
        super().__init__(language, parent, mode)
        self._name = name
        self._table: dict | None = None
        self.resize(AYRIK_GENISLIK, AYRIK_YUKSEKLIK)
        self._outer.addWidget(self._document, 1)
        self.retranslate()

    @property
    def table_name(self) -> str:
        return self._name

    def set_table(self, table: dict | None) -> None:
        """Tabloyu tazeler. `None` verilirse tablo artık yok demektir."""
        self._table = table
        self._render()

    def _render(self) -> None:
        if self._table is None:
            # Öğrenci `DROP TABLE` yazdıysa ya da başka bir alıştırmaya
            # geçtiyse bu pencerenin tablosu ortadan kalkıyor. Pencereyi
            # kendiliğinden kapatmak yerine sebebini yazıyoruz.
            self._show(f"<p>{html.escape(self._language.t('tables.gone'))}</p>")
            return
        self._show(table_html(self._table, self._language))

    def retranslate(self) -> None:
        self.setWindowTitle(
            f"{self._name} — {self._language.t('tables.title')}"
        )
        self._render()


class TablesWindow(_DocumentWindow):
    """Veritabanındaki tabloları sekmeli gösteren pencere."""

    def __init__(
        self,
        language: LanguageManager,
        parent: QWidget | None = None,
        mode: str = "dark",
    ) -> None:
        super().__init__(language, parent, mode)
        self._mode = mode
        self._tables: list[dict] = []
        self._note = ""
        self._current = ""
        self._detached: dict[str, TableWindow] = {}

        self.resize(BASLANGIC_GENISLIK, BASLANGIC_YUKSEKLIK)

        self._bar = QFrame()
        self._bar.setProperty("role", "topbar")
        bar_layout = QHBoxLayout(self._bar)
        bar_layout.setContentsMargins(
            SPACING["md"], SPACING["sm"], SPACING["md"], SPACING["sm"]
        )
        bar_layout.setSpacing(SPACING["sm"])

        # Sekmeler kaydırılabilir bir şeritte: sekiz tablolu bir
        # alıştırmada adlar pencereye sığmıyor ve son sekmeler
        # erişilemez oluyordu.
        self._strip = QScrollArea()
        self._strip.setWidgetResizable(True)
        self._strip.setFrameShape(QFrame.Shape.NoFrame)
        self._strip.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self._strip.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        # Genel kaydırma çubuğu 12 piksel; sekmelerin hemen altında bu
        # kadar kalın bir şerit ikinci bir sıra gibi duruyor. Yalnızca
        # burada inceltiliyor — şerit zaten dar bir bant.
        self._strip.horizontalScrollBar().setStyleSheet(
            "QScrollBar:horizontal { height: 6px; }"
            "QScrollBar::handle:horizontal { min-width: 24px; margin: 1px; }"
        )
        bar_layout.addWidget(self._strip, 1)

        self._detach_button = QPushButton()
        self._detach_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._detach_button.clicked.connect(self._detach_current)
        bar_layout.addWidget(self._detach_button)

        self._outer.addWidget(self._bar)
        self._outer.addWidget(self._document, 1)

        self._segments: SegmentedControl | None = None
        self.retranslate()

    # --- veri -------------------------------------------------------------

    def set_tables(self, tables: list[dict], note: str = "") -> None:
        """Gösterilecek anlık görüntüyü değiştirir."""
        self._tables = tables or []
        self._note = note

        adlar = [str(t.get("name", "")) for t in self._tables]
        # Bakılan sekme korunuyor: çalıştırma sonrası hep ilk tabloya
        # dönmek, aynı tabloyu izleyen birini her seferinde geri
        # tıklamaya zorluyordu.
        if self._current not in adlar:
            self._current = adlar[0] if adlar else ""

        self._build_strip(adlar)
        self._render()
        self._refresh_detached()

    def _build_strip(self, adlar: list[str]) -> None:
        """Sekme şeridini yeniden kurar.

        `SegmentedControl` seçenekleri kurulurken alıyor; alıştırma
        değişince tablo adları da değiştiği için baştan kuruluyor.
        """
        eski = self._strip.takeWidget()
        if eski is not None:
            eski.deleteLater()
        self._segments = None
        if not adlar:
            return

        self._segments = SegmentedControl([(ad, ad) for ad in adlar])
        self._segments.set_value(self._current)
        self._segments.selected.connect(self._choose)

        # Şerit sola yaslanıyor; kalan boşluğu esneme dolduruyor, yoksa
        # tek tablolu bir alıştırmada sekme pencere boyunca uzuyordu.
        holder = QWidget()
        row = QHBoxLayout(holder)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(0)
        row.addWidget(self._segments)
        row.addStretch(1)
        self._strip.setWidget(holder)
        # Bant içeriği kadar yüksek olsun: kaydırma alanı kendi başına
        # yüksek bir kutu istiyor ve sekmelerin altında boşluk kalıyordu.
        gerekli = holder.sizeHint().height()
        cubuk = self._strip.horizontalScrollBar().sizeHint().height()
        self._strip.setFixedHeight(gerekli + cubuk)

    def _choose(self, name: str) -> None:
        self._current = name
        self._render()

    def _table(self, name: str) -> dict | None:
        for tablo in self._tables:
            if str(tablo.get("name", "")) == name:
                return tablo
        return None

    def _render(self) -> None:
        if self._note:
            self._show(f"<p class='meta'>{html.escape(self._note)}</p>")
            return

        tablo = self._table(self._current)
        if tablo is None:
            self._show(f"<p>{html.escape(self._language.t('tables.empty'))}</p>")
            return

        self._detach_button.setEnabled(self._current not in self._detached)
        govde = table_html(tablo, self._language)
        govde += (
            "<p class='meta'>"
            + html.escape(self._language.t("tables.footnote"))
            + "</p>"
        )
        self._show(govde)

    # --- ayrı pencereler --------------------------------------------------

    def _detach_current(self) -> None:
        """Bakılan tabloyu kendi penceresine taşır."""
        if not self._current or self._current in self._detached:
            return

        pencere = TableWindow(self._current, self._language, self, self._mode)
        pencere.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, False)
        pencere.finished.connect(
            lambda _=0, ad=self._current: self._detached.pop(ad, None)
        )
        # Üst üste açılmasınlar: her yeni pencere bir basamak kayıyor.
        kayma = BASAMAK * (len(self._detached) + 1)
        pencere.move(self.x() + kayma, self.y() + kayma)
        pencere.set_table(self._table(self._current))
        self._detached[self._current] = pencere
        pencere.show()
        self._detach_button.setEnabled(False)

    def _refresh_detached(self) -> None:
        for ad, pencere in self._detached.items():
            pencere.set_table(self._table(ad))

    def closeEvent(self, event) -> None:  # noqa: N802
        # Ana pencere kapanınca ayrılanlar da kapanıyor: arkada sahipsiz
        # pencereler bırakmak, kullanıcının onları tek tek toplamasını
        # gerektiriyordu.
        for pencere in list(self._detached.values()):
            pencere.close()
        self._detached.clear()
        super().closeEvent(event)

    # --- tema ve dil ------------------------------------------------------

    def set_mode(self, mode: str) -> None:
        self._mode = mode
        super().set_mode(mode)
        for pencere in self._detached.values():
            pencere.set_mode(mode)

    def retranslate(self) -> None:
        self.setWindowTitle(self._language.t("tables.title"))
        self._detach_button.setText(self._language.t("tables.detach"))
        self._render()
        for pencere in self._detached.values():
            pencere.retranslate()
