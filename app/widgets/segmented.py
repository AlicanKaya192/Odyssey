"""Segment seçici: yan yana duran, biri seçili düğmeler.

Aç/kapa anahtarı iki durumlu bir ayar için doğru bileşen ama **iki seçenek
arasında seçim** için değil. Dil öyle bir ayar: "açık" ile "kapalı" arasında
bir ilişki yok, `TR` ile `EN` arasında var. Anahtar kullanıldığında hangi
tarafın hangi dil olduğunu ancak açıklamayı okuyunca anlaşılıyordu.

Burada iki seçenek de ekranda yazılı duruyor ve seçili olan dolu bir zeminle
işaretleniyor.

Çizim QSS'e bırakılıyor (anahtarın aksine): bunlar gerçek `QPushButton`
olduğu için stil dosyası onlara ulaşıyor ve tema değişimi kendiliğinden
çalışıyor.
"""

from __future__ import annotations

from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtWidgets import QFrame, QHBoxLayout, QPushButton, QVBoxLayout, QWidget

from ..resources.icons import icon


# Simgeli seçeneklerde simgenin boyutu.
ICON_SIZE = 17


class SegmentedControl(QFrame):
    """Verilen seçeneklerden birini seçtirir."""

    selected = Signal(str)

    def __init__(
        self,
        options: list[tuple[str, str]],
        vertical: bool = False,
        parent: QWidget | None = None,
    ) -> None:
        """`options`, `(değer, etiket)` çiftlerinden oluşur.

        Etiket yerine bir **simge** de verilebiliyor: `(değer, "", simge_adı)`
        üçlüsü yazıldığında düğmede yazı yerine o simge çiziliyor. Tema
        seçicisi böyle — "açık"/"koyu" yazmak yerine güneş ve ay.

        `vertical`, seçeneklerin alt alta dizilmesi için. Etkinlik
        ızgarasının yanındaki yıl listesi böyle: ızgara zaten yatayda
        bütün genişliği kullanıyor, yıllar ancak yanına dikey sığıyor.
        """
        super().__init__(parent)
        self.setProperty("role", "segmented")
        # Tek seçenek varken zemin ve kenarlık çizilmiyor. O zemin
        # "seçilmemiş alan" demek; seçenek tek olduğunda seçilmemiş alan
        # yok ve geriye kartın üstünde duran boş bir kutu kalıyor
        # (profildeki yıl seçicisinde görüldü: 2026 düğmesinin arkasında
        # anlamsız bir çerçeve).
        self.setProperty("single", "true" if len(options) < 2 else "false")

        layout = QVBoxLayout(self) if vertical else QHBoxLayout(self)
        layout.setContentsMargins(3, 3, 3, 3)
        layout.setSpacing(3)

        self._buttons: dict[str, QPushButton] = {}
        self._icons: dict[str, str] = {}
        self._colors = ("#666F7D", "#FFFFFF")
        self._value = options[0][0] if options else ""

        for secenek in options:
            value, label = secenek[0], secenek[1]
            simge = secenek[2] if len(secenek) > 2 else ""
            button = QPushButton(label)
            if simge:
                self._icons[value] = simge
                button.setIconSize(QSize(ICON_SIZE, ICON_SIZE))
            button.setProperty("variant", "pill")
            button.setProperty("active", "false")
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.setFlat(True)
            # `clicked` yerine lambda: hangi düğmeye basıldığını taşımak
            # gerekiyor ve Qt sinyali bunu vermiyor.
            button.clicked.connect(lambda _=False, v=value: self._choose(v))
            layout.addWidget(button)
            self._buttons[value] = button

        self._apply()

    # --- durum ------------------------------------------------------------

    def value(self) -> str:
        return self._value

    def set_value(self, value: str) -> None:
        """Seçimi değiştirir; `selected` sinyali yayılmaz.

        Sinyalsiz olması bilinçli: pencere açılırken kayıtlı değer
        yerleştiriliyor ve bunun ayarı yeniden yazmaması gerekiyor.
        """
        if value not in self._buttons or value == self._value:
            return
        self._value = value
        self._apply()

    def _choose(self, value: str) -> None:
        if value == self._value:
            return
        self._value = value
        self._apply()
        self.selected.emit(value)

    def set_tooltips(self, tooltips: dict[str, str]) -> None:
        """Seçeneklerin ipucu metinleri.

        Yalnızca simge taşıyan düğmelerde gerekiyor: güneşin açık, ayın
        koyu tema demek olduğu simgeden okunmuyor.
        """
        for value, metin in tooltips.items():
            if value in self._buttons:
                self._buttons[value].setToolTip(metin)

    def set_icon_colors(self, inactive: str, active: str) -> None:
        """Simgelerin rengini temadan alır.

        Simge bir `QIcon`; QSS ona ulaşamıyor, tema değişince çağıran
        taraf yeniliyor (anahtar ve ızgarayla aynı sebep).
        """
        self._colors = (inactive, active)
        self._apply()

    def _apply(self) -> None:
        pasif, aktif = self._colors
        for value, button in self._buttons.items():
            secili = value == self._value
            button.setProperty("active", "true" if secili else "false")
            if value in self._icons:
                button.setIcon(
                    icon(self._icons[value], aktif if secili else pasif, ICON_SIZE)
                )
            # Qt özellik değişince stili kendiliğinden yenilemiyor; seçili
            # düğme aynı görünmeye devam ediyordu.
            button.style().unpolish(button)
            button.style().polish(button)
