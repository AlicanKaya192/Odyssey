"""Ekranların üst şeridi.

Tek bir yerleşim var: **en solda geri düğmesi, ortada ekranın adı, sağda
ekrana özel denetim.** Başlık şeridin tam ortasında duruyor.

Ortalama şöyle çalışıyor: iki yan bölge de, ikisinden geniş olanın
genişliğine ayarlanıyor. Aradaki iki esneme eşit kalıyor, başlık da tam
ortaya oturuyor. Yan bölgelerin **içeriği** sıkışmıyor — dar olan tarafa
yalnızca boşluk ekleniyor. Bir ara üç bölgeye eşit genişlik verilmişti;
o zaman denetim şeridin üçte birine sıkışıp sekmeler birbirine yapışıyordu.
Sonra da başlık iki bölgenin arasına ortalanmıştı; bu sefer sağdaki denetim
genişleyince başlık sola kaçıyordu.

Önceden ikinci bir yerleşim daha vardı: denetimi olmayan ekranlarda başlık,
sayfa gövdesiyle aynı sütuna sola hizalanıyordu. Şerit genişken başlık sol
dipte kalıyor, ekranın ortasındaki içerikle hiç konuşmuyordu. Artık her
ekranda ortada.

İki tasarım kararı:

* **Bağlam üstte, ad altta.** Önce büyük başlık, altında soluk bir açıklama
  vardı; ikisi de aynı ağırlıkta okunuyordu. Şimdi bağlam üstte küçük ve
  vurgu renginde, altında asıl ad büyük ve kalın.
* **Vurgu çizgisi başlığın altında, yatay.** Başlığın solundaki dikey çubuk,
  başlık ortalanınca ortada asılı kalıyordu. Altına çekilen kısa yatay çizgi
  başlığı sayfaya bağlıyor ve ortalamayı bozmuyor.
"""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QFontMetrics
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ..core.language import LanguageManager, upper
from ..resources.icons import icon
from ..resources.theme.tokens import PALETTES, SPACING

HEADER_HEIGHT = 108

# Başlığın altındaki kısa vurgu çizgisi. Başlık kadar uzun olursa altı çizili
# bir bağlantıya benziyor; kısa tutulunca süs olarak okunuyor.
ACCENT_LINE_WIDTH = 44
ACCENT_LINE_HEIGHT = 3

# Uzun başlıklar ("Türevin Uygulamaları: En Büyük ve En Küçük") iki yan
# bölgenin arasına sığmayınca etiket metni iki ucundan kırpıyordu. Önce yazı
# bu boyutlar sırasıyla denenerek küçülüyor; en küçüğünde de sığmazsa sonu
# "…" ile kısaltılıyor ve tam ad ipucunda duruyor. İlk değer QSS'teki boyut.
TITLE_SIZES = (26, 24, 22, 20, 18)

# Başlıkla yan bölgeler arasında bırakılan toplam pay; yoksa başlık yan
# bölgelere yapışık duruyor.
TITLE_PADDING = 16


class ScreenHeader(QFrame):
    """Başlık şeridi."""

    back_clicked = Signal()

    def __init__(self, language: LanguageManager, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._language = language
        self._mode = "light"
        self._accent = ""
        self._full_title = ""
        self._full_eyebrow = ""
        self._title_size = TITLE_SIZES[0]

        # `_balance()` en son hangi genişliği verdi. Aynı değeri tekrar
        # vermek yeni bir yerleşim turu başlatıyor; gereksiz.
        self._balanced: tuple[int, int] = (-1, -1)

        self.setProperty("role", "topbar")
        self.setFixedHeight(HEADER_HEIGHT)

        outer = QHBoxLayout(self)
        outer.setContentsMargins(SPACING["lg"], 0, SPACING["lg"], 0)
        outer.setSpacing(SPACING["md"])

        self._left = self._build_left()
        self._centre = self._build_centre()
        self._right = self._build_right()

        outer.addWidget(self._left, 0)
        outer.addStretch(1)
        outer.addWidget(self._centre, 0)
        outer.addStretch(1)
        outer.addWidget(self._right, 0)

        self.set_mode(self._mode)

    def _side_widths(self) -> tuple[int, int]:
        """Sol ve sağ bölgenin **içeriğinin** doğal genişliği.

        Ölçü, bölgelerin kendi `sizeHint`'inden değil içeriğinden alınıyor.
        Bölgeye en küçük genişlik verdiğimiz an `sizeHint` de büyüyor; ondan
        ölçseydik her çağrıda bir öncekinin üstüne biner, şerit şişerdi.
        """
        # `isVisible()` değil `isHidden()`: gösterilmemiş bir pencerenin
        # içindeki her widget `isVisible() == False` döndürüyor. Ölçüm
        # pencere açılmadan yapıldığı için geri düğmesi hep sıfır
        # sayılıyordu ve bölgeler hiç dengelenmiyordu.
        sol = 0 if self._back.isHidden() else self._back.sizeHint().width()

        sag = 0
        görünen = 0
        for index in range(self._slot.count()):
            widget = self._slot.itemAt(index).widget()
            if widget is not None and not widget.isHidden():
                sag += widget.sizeHint().width()
                görünen += 1
        if görünen > 1:
            sag += self._slot.spacing() * (görünen - 1)
        return sol, sag

    def _balance(self) -> None:
        """Yan bölgeleri ayarlar ve başlığı ortaya sığdırır (bkz. `_fit_title`)."""
        self._fit_title()

    def _set_sides(self, left: int, right: int) -> None:
        # Aynı değeri tekrar vermek yeni bir yerleşim turu başlatıyor; gereksiz.
        if (left, right) == self._balanced:
            return
        self._balanced = (left, right)
        self._left.setMinimumWidth(left)
        self._right.setMinimumWidth(right)

    def resizeEvent(self, event) -> None:  # noqa: N802
        super().resizeEvent(event)
        self._fit_title()

    def _two_lines(self, metrics: QFontMetrics, room: int) -> str | None:
        """Başlığı kelime sınırından iki dengeli satıra böler.

        Uzun satırı en kısa yapan bölme noktası seçiliyor; iki satır da
        sığmıyorsa `None`.
        """
        kelimeler = self._full_title.split()
        en_iyi = None
        for i in range(1, len(kelimeler)):
            ust, alt = " ".join(kelimeler[:i]), " ".join(kelimeler[i:])
            genis = max(metrics.horizontalAdvance(ust), metrics.horizontalAdvance(alt))
            if genis <= room and (en_iyi is None or genis < en_iyi[0]):
                en_iyi = (genis, f"{ust}\n{alt}")
        return en_iyi[1] if en_iyi else None

    def _choose(self, font: QFont, room: int) -> tuple[int, str, bool]:
        """`room` genişliğine göre (boyut, metin, tam mı) seçer.

        Sıra: tek satır ve yazı küçülerek; sonra iki satır (şerit iki satırı
        alacak kadar yüksek); en son sonu "…" ile kısaltılmış tek satır.
        """
        for aday in TITLE_SIZES:
            font.setPixelSize(aday)
            if QFontMetrics(font).horizontalAdvance(self._full_title) + TITLE_PADDING <= room:
                return aday, self._full_title, True
        for aday in TITLE_SIZES[-2:]:
            font.setPixelSize(aday)
            iki = self._two_lines(QFontMetrics(font), room - TITLE_PADDING)
            if iki is not None:
                return aday, iki, True
        boyut = TITLE_SIZES[-1]
        font.setPixelSize(boyut)
        kisa = QFontMetrics(font).elidedText(
            self._full_title, Qt.TextElideMode.ElideRight, max(room - TITLE_PADDING, 0)
        )
        return boyut, kisa, False

    def _fit_title(self) -> None:
        """Yan bölgeleri dengeler, başlığı ve bağlam satırını ortaya sığdırır.

        Normalde iki yan bölge, ikisinden geniş olanın genişliğine getiriliyor;
        aradaki iki esneme eşit kalıyor ve başlık şeridin tam ortasına düşüyor.
        Dar olan tarafa yalnızca boşluk ekleniyor.

        Uzun ders adları ("Türevin Uygulamaları: En Büyük ve En Küçük") bu
        ortada sığmayınca etiket metni iki ucundan kırpıyordu. Şimdi başlık
        önce küçülüyor, sonra iki satıra bölünüyor. Dar bir pencerede o da
        yetmezse ortalamadan vazgeçiliyor: yan bölgeler doğal genişliğine
        dönüyor ve başlık aradaki bütün boşluğu kullanıyor. En son çare sonu
        "…" ile kısaltmak; tam ad ipucunda duruyor.
        """
        sol, sag = self._side_widths()
        if self.width() <= 0:
            # Pencere henüz açılmadı; ilk `resizeEvent` sığdırmayı yapacak.
            genis = max(sol, sag)
            self._set_sides(genis, genis)
            self._title.setText(self._full_title)
            self._eyebrow.setText(self._full_eyebrow)
            return

        margins = self.layout().contentsMargins()
        toplam = self.width() - margins.left() - margins.right() - 4 * SPACING["md"]

        font = QFont(self._title.font())
        font.setWeight(QFont.Weight.Bold)
        font.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, -0.3)

        ortali = True
        oda = toplam - 2 * max(sol, sag)
        boyut, metin, tam = self._choose(font, oda)
        if not tam:
            ortali = False
            oda = toplam - sol - sag
            boyut, metin, tam = self._choose(font, oda)

        if ortali:
            self._set_sides(max(sol, sag), max(sol, sag))
        else:
            self._set_sides(sol, sag)

        if boyut != self._title_size:
            self._title_size = boyut
            # QSS'teki boyutu yalnızca küçülttüğümüzde eziyoruz; ağırlık ve
            # renk ortak kuraldan gelmeye devam ediyor.
            self._title.setStyleSheet(
                "" if boyut == TITLE_SIZES[0] else f"font-size: {boyut}px;"
            )
        self._title.setText(metin)
        self._title.setToolTip("" if tam else self._full_title)

        kas = QFontMetrics(self._eyebrow.font())
        ust = kas.elidedText(
            self._full_eyebrow, Qt.TextElideMode.ElideRight, max(oda - TITLE_PADDING, 0)
        )
        self._eyebrow.setText(ust)
        self._eyebrow.setToolTip("" if ust == self._full_eyebrow else self._full_eyebrow)

    # --- parçalar ---------------------------------------------------------

    def _build_left(self) -> QWidget:
        """Geri düğmesi şeridin en solunda; içeri girilen yön orası."""
        holder = QWidget()
        row = QHBoxLayout(holder)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(0)

        self._back = QPushButton()
        self._back.setProperty("variant", "ghost")
        self._back.setCursor(Qt.CursorShape.PointingHandCursor)
        self._back.clicked.connect(self.back_clicked)
        self._back.hide()
        row.addWidget(self._back, 0, Qt.AlignmentFlag.AlignVCenter)
        # Bölge dengelenirken genişleyebiliyor; düğme sola yapışık kalsın.
        row.addStretch(1)
        return holder

    def _build_centre(self) -> QWidget:
        holder = QWidget()
        column = QVBoxLayout(holder)
        column.setContentsMargins(0, 0, 0, 0)
        column.setSpacing(3)
        column.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._eyebrow = QLabel()
        self._eyebrow.setProperty("role", "eyebrow")
        self._eyebrow.setAlignment(Qt.AlignmentFlag.AlignCenter)
        column.addWidget(self._eyebrow, 0, Qt.AlignmentFlag.AlignHCenter)

        # Boyut ve ağırlık QSS'te: uygulama stil şablonu piksel cinsinden
        # yazı boyutu veriyor, buradan setPointSize ile verilen değer piksele
        # çevrilip başlığı büyütmek yerine küçültüyordu.
        self._title = QLabel()
        self._title.setProperty("role", "screen")
        self._title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        column.addWidget(self._title, 0, Qt.AlignmentFlag.AlignHCenter)

        self._line = QFrame()
        self._line.setFixedSize(ACCENT_LINE_WIDTH, ACCENT_LINE_HEIGHT)
        column.addSpacing(SPACING["xs"])
        column.addWidget(self._line, 0, Qt.AlignmentFlag.AlignHCenter)

        return holder

    def _build_right(self) -> QWidget:
        holder = QWidget()
        row = QHBoxLayout(holder)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(SPACING["sm"])
        row.addStretch(1)

        self._slot = QHBoxLayout()
        self._slot.setSpacing(SPACING["sm"])
        row.addLayout(self._slot)
        return holder

    # --- içerik -----------------------------------------------------------

    def set_titles(self, title: str, eyebrow: str = "") -> None:
        """Büyük başlık ve üstündeki küçük bağlam satırı.

        Bağlam satırı büyük harfe çevrilirken dilin kuralı kullanılıyor:
        Python'un upper() metodu Türkçede i harfini I yapıyor ve
        "PYTHON TEMELLERI" gibi yanlış sonuç çıkıyor.
        """
        self._full_title = title
        self._full_eyebrow = upper(eyebrow, self._language.language) if eyebrow else ""
        self._eyebrow.setVisible(bool(eyebrow))
        self._fit_title()

        # Yerleşimi elle tazeliyoruz. `set_back()` bu metottan önce çağrılıyor
        # ve `_balance()` orada yan bölgelere en küçük genişlik veriyor; bu
        # da bir yerleşim turu başlatıyor. Tur, başlık **eski** metniyken
        # koşuyor ve orta bölgeyi o genişlikte sabitliyordu. Sonuç:
        # "Öğrenme Yolu" için hesaplanan 171 pikselde kalan kutu, "Python
        # Temelleri" yazınca metni iki ucundan kırpıyordu ("ython Temelle").
        self._centre.updateGeometry()
        self._centre.adjustSize()
        layout = self.layout()
        if layout is not None:
            layout.invalidate()
            layout.activate()

    def set_accent(self, color: str) -> None:
        """Vurgu çizgisinin ve bağlam satırının rengi.

        Şeritteki simgeyle aynı renk veriliyor; ekranlar arasında geçerken
        aynı rengin devam etmesi, nerede olunduğunu renkten de okutuyor.
        """
        self._accent = color
        self._apply_accent()

    def _apply_accent(self) -> None:
        palette = PALETTES.get(self._mode, PALETTES["light"])
        renk = self._accent or palette["accent"]
        self._line.setStyleSheet(
            f"background-color: {renk}; border-radius: {ACCENT_LINE_HEIGHT // 2}px;"
        )
        self._eyebrow.setStyleSheet(f"color: {renk};")

    def set_back(self, visible: bool, text: str = "") -> None:
        """Geri düğmesini gösterir ya da gizler."""
        self._back.setVisible(visible)
        if text:
            self._back.setText(f"  {text}")
        self._balance()

    def add_widget(self, widget: QWidget) -> None:
        """Başlığın sağına ekrana özel bir denetim yerleştirir."""
        self._slot.addWidget(widget)
        self._balance()

    def set_mode(self, mode: str) -> None:
        self._mode = mode
        palette = PALETTES.get(mode, PALETTES["light"])
        self._back.setIcon(icon("arrow-left", palette["text"], 18))
        self._apply_accent()
