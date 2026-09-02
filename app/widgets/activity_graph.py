"""Yıllık etkinlik ızgarası.

Her kare bir gün; rengin koyuluğu o gün kaç iş yapıldığını gösteriyor.
Soldan sağa haftalar, yukarıdan aşağı haftanın günleri. Bir yıl gösteriliyor
ve yıl dışarıdan seçiliyor.

Veriyi `ProgressStore.activity_for_year()` veriyor. O tablo yalnızca **olay
ekliyor**: bir ders ilk okunduğunda, bir alıştırma ilk çözüldüğünde ve her
sınav denemesinde bir satır yazılıyor. Aynı dersi beş kez açmak ızgarayı
doldurmuyor; orada "ne yaptım" duruyor, "kaç kez baktım" değil.

Renkler `set_colors` ile dışarıdan veriliyor: QSS bir widget'ın kendi
`paintEvent` çizimine ulaşamıyor, tema değişince çağıran taraf yeniliyor.
"""

from __future__ import annotations

from datetime import date, timedelta

from PySide6.QtCore import QPoint, QRectF, Qt
from PySide6.QtGui import QColor, QFont, QPainter
from PySide6.QtWidgets import QToolTip, QWidget

# Bir yıl 52 ya da 53 haftaya yayılıyor; ızgara her zaman 53 sütun ayırıyor,
# yılın dışında kalan kutular çizilmiyor.
WEEKS = 53

# Izgara ölçüleri.
#
# Hücre boyutu kartın genişliğine göre hesaplanıyor. Alt ve üst sınır var:
# çok küçülünce günler fareyle seçilemiyor, çok büyüyünce ızgara duvara
# dönüyor.
# Ölçüldü: 9-10 piksel karelerde günler hem okunmuyor hem fareyle
# seçilemiyordu.
MIN_CELL = 12
MAX_CELL = 16
GAP = 3
TOP_LABEL = 18
LEFT_LABEL = 30

# Bir günde kaç iş yapıldığına göre koyuluk basamakları.
LEVELS = (1, 2, 4)


class ActivityGraph(QWidget):
    """Bir yılın günlük etkinliği."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._counts: dict[str, int] = {}
        self._days: list[date | None] = []
        self._month_names: list[str] = []
        self._weekday_names: list[str] = []
        self._tooltip_maker = None
        self._hovered: date | None = None
        self._year = date.today().year

        self._empty = QColor("#E3E6EC")
        self._scale = [QColor("#C7D2FE"), QColor("#818CF8"), QColor("#4F46E5")]
        self._text = QColor("#6B7280")

        self._cell = MIN_CELL

        self.setMouseTracking(True)
        self._build_days()
        self._apply_cell(MIN_CELL)
        self.setMinimumWidth(LEFT_LABEL + WEEKS * (MIN_CELL + GAP))

    # --- ölçü -------------------------------------------------------------

    @property
    def _step(self) -> int:
        return self._cell + GAP

    def _apply_cell(self, cell: int) -> None:
        self._cell = max(MIN_CELL, min(MAX_CELL, cell))
        self.setFixedHeight(TOP_LABEL + 7 * self._step)

    def resizeEvent(self, event) -> None:  # noqa: N802
        self._apply_cell((self.width() - LEFT_LABEL) // WEEKS - GAP)
        super().resizeEvent(event)

    # --- veri -------------------------------------------------------------

    def _build_days(self) -> None:
        """Seçili yılın gün ızgarasını kurar.

        Sütunlar hafta. Izgara, yılın ilk gününü içeren haftanın
        pazartesisinden başlıyor; yılın dışında kalan kutular `None` ve
        çizilmiyor — böylece her yıl kendi içinde duruyor.
        """
        ocak = date(self._year, 1, 1)
        baslangic = ocak - timedelta(days=ocak.weekday())
        self._days = []
        for i in range(WEEKS * 7):
            gun = baslangic + timedelta(days=i)
            self._days.append(gun if gun.year == self._year else None)

    def set_year(self, year: int) -> None:
        if year == self._year:
            return
        self._year = year
        self._build_days()
        self.update()

    @property
    def year(self) -> int:
        return self._year

    def set_counts(self, counts: dict[str, int]) -> None:
        self._counts = counts
        self.update()

    def set_labels(self, months: list[str], weekdays: list[str]) -> None:
        """Ay ve gün adlarını dile göre alır."""
        self._month_names = months
        self._weekday_names = weekdays
        self.update()

    def set_tooltip_maker(self, maker) -> None:
        """`(gün, sayı) -> metin` üreten çağrılabilir."""
        self._tooltip_maker = maker

    def set_colors(self, empty: str, scale: list[str], text: str) -> None:
        self._empty = QColor(empty)
        self._scale = [QColor(c) for c in scale]
        self._text = QColor(text)
        self.update()

    # --- yardımcılar ------------------------------------------------------

    def _level(self, count: int) -> int:
        """Sayıyı 0-3 arası koyuluk basamağına çevirir."""
        if count <= 0:
            return 0
        for index, sinir in enumerate(LEVELS):
            if count < sinir:
                return index
        return len(LEVELS)

    def _cell_rect(self, index: int) -> QRectF:
        hafta, gun = divmod(index, 7)
        return QRectF(
            LEFT_LABEL + hafta * self._step,
            TOP_LABEL + gun * self._step,
            self._cell, self._cell,
        )

    def _day_at(self, x: float, y: float):
        hafta = int((x - LEFT_LABEL) // self._step)
        gun = int((y - TOP_LABEL) // self._step)
        if not (0 <= hafta < WEEKS and 0 <= gun < 7):
            return None
        index = hafta * 7 + gun
        if index >= len(self._days):
            return None
        return self._days[index]

    # --- etkileşim --------------------------------------------------------

    def mouseMoveEvent(self, event) -> None:  # noqa: N802
        gun = self._day_at(event.position().x(), event.position().y())
        if gun is None or gun > date.today() or self._tooltip_maker is None:
            QToolTip.hideText()
            self._hovered = None
            super().mouseMoveEvent(event)
            return

        # `setToolTip` Qt'nin bekleme süresine tabi: fare kareye geldikten
        # yaklaşık 700 ms sonra çıkıyor ve kareden kareye geçerken metin
        # geç değişiyor. Kareler küçük olduğu için bu, ızgarayı okunamaz
        # hâle getiriyordu. `showText` beklemeden gösteriyor.
        if gun != self._hovered:
            self._hovered = gun
            metin = self._tooltip_maker(gun, self._counts.get(gun.isoformat(), 0))
            QToolTip.showText(event.globalPosition().toPoint(), metin, self)
        super().mouseMoveEvent(event)

    def leaveEvent(self, event) -> None:  # noqa: N802
        QToolTip.hideText()
        self._hovered = None
        super().leaveEvent(event)

    # --- çizim ------------------------------------------------------------

    def paintEvent(self, event) -> None:  # noqa: N802
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        kucuk = QFont(self.font())
        kucuk.setPixelSize(10)
        painter.setFont(kucuk)
        painter.setPen(self._text)

        # Ay adları: her ayın **ilk tam sütununun** üstüne bir kez. Ayın
        # başladığı hafta bir öncekiyle paylaşılıyorsa etiket bir sonraki
        # sütuna kayıyor; yoksa iki ay adı üst üste biniyor.
        yazilan = set()
        for hafta in range(WEEKS):
            bas = self._days[hafta * 7]
            son = self._days[hafta * 7 + 6]
            if bas is None or son is None or bas.month != son.month:
                continue
            if bas.month in yazilan:
                continue
            yazilan.add(bas.month)
            if self._month_names:
                painter.drawText(
                    int(LEFT_LABEL + hafta * self._step),
                    TOP_LABEL - 6,
                    self._month_names[bas.month - 1],
                )

        # Gün adları: kalabalık olmasın diye bir atlayarak.
        if self._weekday_names:
            for gun_index in (0, 2, 4):
                painter.drawText(
                    0,
                    int(TOP_LABEL + gun_index * self._step + self._cell - 2),
                    self._weekday_names[gun_index],
                )

        painter.setPen(Qt.PenStyle.NoPen)
        for index, gun in enumerate(self._days):
            # Yılın dışında kalan kutular çizilmiyor — her yıl kendi içinde
            # duruyor. Yılın **gelecek** günleri ise boş kare olarak
            # çiziliyor: çizilmediklerinde ızgaranın sağı ortasından
            # kesilmiş gibi duruyordu.
            if gun is None:
                continue
            basamak = self._level(self._counts.get(gun.isoformat(), 0))
            painter.setBrush(self._empty if basamak == 0 else self._scale[basamak - 1])
            painter.drawRoundedRect(self._cell_rect(index), 3, 3)

        painter.end()
