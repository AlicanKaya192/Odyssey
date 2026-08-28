"""Ekranların üst şeridi.

İki yerleşimi var.

**Dar yerleşim** (varsayılan): geri düğmesi ve başlık, sayfa gövdesiyle aynı
sütuna hizalanıyor. Şerit pencerenin en solundan başlarken içerik ortada
duruyordu; ikisi hizalanmıyor, başlık köşede öksüz kalıyordu.

**Geniş yerleşim** (`add_widget` çağrılınca): solda geri düğmesi, ortada
ekranın adı, sağda ekrana özel denetim. Konu ekranındaki segmented control
dar sütuna sıkıştığında ortada asılı bir kutu gibi duruyordu.

Başlık, geri düğmesiyle denetimin **arasına** ortalanıyor — şeridin mutlak
ortasına değil. Bir ara üç bölgeye eşit genişlik verilmişti; başlık gerçekten
tam ortaya oturuyordu ama denetim şeridin üçte birine sıkışıp sekmeler
birbirine yapışıyordu. Denetim artık doğal genişliğini alıyor.

Bir tasarım kararı daha: **bağlam üstte, ad altta.** Önce büyük başlık,
altında soluk bir açıklama vardı; ikisi de aynı ağırlıkta okunuyordu. Şimdi
bağlam üstte küçük ve vurgu renginde, altında asıl ad büyük ve kalın.
"""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from ..core.language import LanguageManager, upper
from ..resources.icons import icon
from ..resources.theme.tokens import CONTENT_WIDTH, PALETTES, SPACING

HEADER_HEIGHT = 108

# Başlığın solundaki ince renkli çubuğun ölçüleri. Şeridi sayfaya bağlayan
# tek görsel öge; kaldırıldığında başlık yine havada duruyor.
ACCENT_BAR_WIDTH = 3
ACCENT_BAR_HEIGHT = 50


class ScreenHeader(QFrame):
    """Başlık şeridi."""

    back_clicked = Signal()

    def __init__(self, language: LanguageManager, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._language = language
        self._mode = "light"
        self._accent = ""
        self._wide = False

        self.setProperty("role", "topbar")
        self.setFixedHeight(HEADER_HEIGHT)

        self._left = self._build_left()
        self._centre = self._build_centre()
        self._right = self._build_right()

        self._outer = QHBoxLayout(self)
        self._outer.setContentsMargins(SPACING["lg"], 0, SPACING["lg"], 0)
        self._outer.setSpacing(SPACING["md"])
        self._apply_narrow()

        self.set_mode(self._mode)

    # --- parçalar ---------------------------------------------------------

    def _build_left(self) -> QWidget:
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
        row.addStretch(1)
        return holder

    def _build_centre(self) -> QWidget:
        holder = QWidget()
        row = QHBoxLayout(holder)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(SPACING["md"])

        self._bar = QFrame()
        self._bar.setFixedSize(ACCENT_BAR_WIDTH, ACCENT_BAR_HEIGHT)
        row.addWidget(self._bar, 0, Qt.AlignmentFlag.AlignVCenter)

        titles = QVBoxLayout()
        titles.setSpacing(3)
        titles.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        titles.addStretch(1)

        self._eyebrow = QLabel()
        self._eyebrow.setProperty("role", "eyebrow")
        titles.addWidget(self._eyebrow)

        # Boyut ve ağırlık QSS'te: uygulama stil şablonu piksel cinsinden
        # yazı boyutu veriyor, buradan `setPointSize` ile verilen değer
        # piksele çevrilip başlığı büyütmek yerine küçültüyordu.
        self._title = QLabel()
        self._title.setProperty("role", "screen")
        titles.addWidget(self._title)

        titles.addStretch(1)
        row.addLayout(titles)
        self._centre_row = row
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

    # --- yerleşim ---------------------------------------------------------

    def _clear_outer(self) -> None:
        while self._outer.count():
            item = self._outer.takeAt(0)
            if item.widget() is not None:
                item.widget().setParent(None)

    def _apply_narrow(self) -> None:
        """Geri düğmesi ve başlık, sayfa gövdesiyle aynı sütunda."""
        self._clear_outer()

        column = QWidget()
        column.setMaximumWidth(CONTENT_WIDTH)
        column.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        row = QHBoxLayout(column)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(SPACING["md"])
        row.addWidget(self._left, 0)
        row.addWidget(self._centre, 0)
        row.addStretch(1)
        row.addWidget(self._right, 0)

        self._outer.addStretch(1)
        self._outer.addWidget(column, 10)
        self._outer.addStretch(1)
        self._column = column

    def _apply_wide(self) -> None:
        """Solda geri düğmesi, ortada ekranın adı, sağda denetim.

        Üç bölgeye eşit genişlik verilmiyor: denetim (segmented control)
        kendi doğal genişliğini alıyor, yoksa şeridin üçte birine sıkışıp
        sekmeler birbirine yapışıyordu. Başlık, geri düğmesiyle denetimin
        **arasına** ortalanıyor.
        """
        self._clear_outer()

        self._centre_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._outer.addWidget(self._left, 0)
        self._outer.addStretch(1)
        self._outer.addWidget(self._centre, 0)
        self._outer.addStretch(1)
        self._outer.addWidget(self._right, 0)
        self._wide = True

    # --- içerik -----------------------------------------------------------

    def set_titles(self, title: str, eyebrow: str = "") -> None:
        """Büyük başlık ve üstündeki küçük bağlam satırı.

        Bağlam satırı büyük harfe çevrilirken dilin kuralı kullanılıyor:
        Python'un `upper()` metodu Türkçede `i` harfini `I` yapıyor ve
        "PYTHON TEMELLERI" gibi yanlış sonuç çıkıyor.
        """
        self._title.setText(title)
        self._eyebrow.setText(
            upper(eyebrow, self._language.language) if eyebrow else ""
        )
        self._eyebrow.setVisible(bool(eyebrow))

    def set_accent(self, color: str) -> None:
        """Sol çubuğun ve bağlam satırının rengi.

        Şeritteki simgeyle aynı renk veriliyor; ekranlar arasında geçerken
        aynı rengin devam etmesi, nerede olunduğunu renkten de okutuyor.
        """
        self._accent = color
        self._apply_accent()

    def _apply_accent(self) -> None:
        palette = PALETTES.get(self._mode, PALETTES["light"])
        renk = self._accent or palette["accent"]
        self._bar.setStyleSheet(
            f"background-color: {renk}; border-radius: {ACCENT_BAR_WIDTH // 2}px;"
        )
        self._eyebrow.setStyleSheet(f"color: {renk};")

    def set_back(self, visible: bool, text: str = "") -> None:
        """Geri düğmesini gösterir ya da gizler."""
        self._back.setVisible(visible)
        if text:
            self._back.setText(f"  {text}")

    def add_widget(self, widget: QWidget) -> None:
        """Başlığın sağına ekrana özel bir denetim yerleştirir.

        Denetim eklenince şerit dar sütundan çıkıp tüm genişliğe açılıyor.
        """
        self._slot.addWidget(widget)
        if not self._wide:
            self._apply_wide()

    def set_mode(self, mode: str) -> None:
        self._mode = mode
        palette = PALETTES.get(mode, PALETTES["light"])
        self._back.setIcon(icon("arrow-left", palette["text"], 18))
        self._apply_accent()
