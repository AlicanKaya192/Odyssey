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

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QFrame, QHBoxLayout, QPushButton, QWidget


class SegmentedControl(QFrame):
    """Verilen seçeneklerden birini seçtirir."""

    selected = Signal(str)

    def __init__(
        self,
        options: list[tuple[str, str]],
        parent: QWidget | None = None,
    ) -> None:
        """`options`, `(değer, etiket)` çiftlerinden oluşur."""
        super().__init__(parent)
        self.setProperty("role", "segmented")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(3, 3, 3, 3)
        layout.setSpacing(3)

        self._buttons: dict[str, QPushButton] = {}
        self._value = options[0][0] if options else ""

        for value, label in options:
            button = QPushButton(label)
            button.setProperty("variant", "pill")
            button.setProperty("active", False)
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

    def _apply(self) -> None:
        for value, button in self._buttons.items():
            button.setProperty("active", value == self._value)
            # Qt özellik değişince stili kendiliğinden yenilemiyor; seçili
            # düğme aynı görünmeye devam ediyordu.
            button.style().unpolish(button)
            button.style().polish(button)
