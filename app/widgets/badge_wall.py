"""Rozet duvarı.

Her rozet bir simge ve adından oluşuyor. Kazanılanlar dolu, kazanılmayanlar
soluk. **Kilitliler de gösteriliyor**: neyin kazanılabileceğini görmek,
yalnızca kazanılanları görmekten daha çok işe yarıyor — üstüne gelince nasıl
alınacağı yazıyor.

Simgeler `app/resources/icons.py` içindeki SVG setinden geliyor. Önce
unicode karakterler kullanılmıştı; o modülün kendi kuralı emoji ve özel
karakter kullanmamak, çünkü her Windows sürümünde farklı çiziliyor ve boyutu
kontrol edilemiyor.
"""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QFrame, QGridLayout, QLabel, QVBoxLayout, QWidget

from ..resources.icons import pixmap
from ..resources.theme.tokens import SPACING

# Simge dairesinin çapı ve içindeki simgenin boyutu.
CIRCLE = 56
ICON = 26

# Bir rozetin adıyla birlikte kapladığı genişlik.
#
# Ad iki satıra sarabiliyor ama **tek kelimelik adlar saramıyor**:
# "Alışkanlık" tek satırda 120 piksel istiyor ve 96 piksellik hücrede
# kırpılıyordu. Genişlik en uzun tek kelimeye göre seçildi.
CELL_WIDTH = 128
MIN_COLUMNS = 3

# Bir sayfada kaç sıra rozet duruyor.
#
# Duvar artık profil kartının yanında, onun boyunda bir kartın içinde;
# sığmayanlar aşağı taşmak yerine sonraki sayfaya geçiyor. Sıra sayısı
# sabit, sütun sayısı genişliğe göre hesaplanıyor.
ROWS = 2


class BadgeChip(QWidget):
    """Simge dairesi ve altında rozetin adı."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setFixedWidth(CELL_WIDTH)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(SPACING["xs"])

        # Fare olayları çipe gelsin: daire ve etiket ayrı ayrı yakalarsa
        # ipucu aradaki geçişlerde sönüp yeniden açılıyor.
        self.setAttribute(Qt.WidgetAttribute.WA_Hover, True)

        self.circle = QFrame()
        self.circle.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.circle.setProperty("role", "badge")
        self.circle.setFixedSize(CIRCLE, CIRCLE)
        ic_duzen = QVBoxLayout(self.circle)
        ic_duzen.setContentsMargins(0, 0, 0, 0)
        self.icon = QLabel()
        self.icon.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ic_duzen.addWidget(self.icon)
        layout.addWidget(self.circle, 0, Qt.AlignmentFlag.AlignHCenter)

        self.name = QLabel()
        self.name.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.name.setProperty("role", "badge-name")
        self.name.setWordWrap(True)
        self.name.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.name)

        self._tooltip = ""

    def set_empty(self) -> None:
        """Çipi boşaltır ama yerinde bırakır.

        Yarım kalan sayfada çipi tamamen gizlemek ızgarayı bozuyordu:
        `QGridLayout` gizli widget'ın sütununu çöktürüyor, kalan rozetler
        de yanlış sütunlara kayıyordu. Çip yerinde kalıp yalnızca içeriği
        gizlenince ızgara her sayfada aynı duruyor.
        """
        self._tooltip = ""
        self.setToolTip("")
        self.circle.hide()
        self.name.hide()

    def apply(self, badge, title: str, tooltip: str, color: str) -> None:
        self.circle.show()
        self.name.show()
        self.circle.setProperty("earned", badge.earned)
        self.icon.setPixmap(pixmap(badge.icon, color, ICON))
        self.name.setText(title)
        self.name.setProperty("earned", badge.earned)
        # Aynı çip yeniden kullanıldığında Qt stili kendiliğinden
        # yenilemiyor; kazanılan bir rozet kilitli görünmeye devam ediyordu.
        for parca in (self.circle, self.name):
            parca.style().unpolish(parca)
            parca.style().polish(parca)
        self._tooltip = tooltip
        # İpucu Qt'nin kendi yoluyla gösteriliyor. Elle `QToolTip.showText`
        # çağırmak her seferinde yeni bir ipucu penceresi kurduruyor ve
        # Windows'un açılış animasyonu baştan oynuyordu — rozetten rozete
        # geçerken takılıyor gibi görünüyordu. Bekleme süresi
        # `TooltipStyle` ile kısaltıldı.
        self.setToolTip(tooltip)


class BadgeWall(QWidget):
    """Rozetleri sayfa sayfa ızgara hâlinde gösterir."""

    # Sayfa sayısı ya da açık sayfa değişti; kart oklarını güncelliyor.
    paging_changed = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._layout = QGridLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setHorizontalSpacing(SPACING["md"])
        self._layout.setVerticalSpacing(SPACING["lg"])
        self._badges: list = []
        self._chips: list[BadgeChip] = []
        self._columns = 0
        self._page = 0
        self._title_maker = None
        self._tooltip_maker = None
        self._colors = ("#FFFFFF", "#6B7280")

    def set_badges(self, badges: list, title_maker, tooltip_maker, colors) -> None:
        """Rozetleri ve metinleri yeniler.

        `colors`, `(kazanılan simge rengi, kilitli simge rengi)`.
        """
        yeniden = len(badges) != len(self._badges)
        self._badges = badges
        self._title_maker = title_maker
        self._tooltip_maker = tooltip_maker
        self._colors = colors

        # Izgara **yalnızca rozet sayısı değişince** yeniden kuruluyor.
        #
        # Eskiden her çağrıda `_columns = 0` yazılıp bütün çipler silinip
        # yeniden üretiliyordu. Bu çağrı tema değişiminde de yapılıyor ve
        # ölçüldü: 12 çipin yıkılıp kurulması 11 ms sürüyor, tema
        # geçişindeki takılmanın büyük kısmı buradan geliyordu. Renk ve
        # metin değişimi için çipleri yeniden kurmak gerekmiyor.
        if yeniden:
            self._columns = 0
            self._page = 0
            self._relayout()
        else:
            self._apply_all()

    def _fit_columns(self) -> int:
        adim = CELL_WIDTH + SPACING["md"]
        return max(MIN_COLUMNS, (self.width() + SPACING["md"]) // adim)

    # --- sayfalar ---------------------------------------------------------

    @property
    def page_size(self) -> int:
        return max(1, self._columns * ROWS)

    @property
    def page_count(self) -> int:
        if not self._badges:
            return 1
        return max(1, -(-len(self._badges) // self.page_size))

    @property
    def page(self) -> int:
        return self._page

    def set_page(self, index: int) -> None:
        index = max(0, min(self.page_count - 1, index))
        if index == self._page:
            return
        self._page = index
        self._apply_all()
        self.paging_changed.emit()

    def _page_badges(self) -> list:
        bas = self._page * self.page_size
        return self._badges[bas:bas + self.page_size]

    def _relayout(self) -> None:
        if not self._badges:
            return
        sutun = self._fit_columns()
        if sutun == self._columns:
            self._apply_all()
            return
        self._columns = sutun

        while self._layout.count():
            item = self._layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self._chips = []

        # Sayfa dolusu kadar çip kuruluyor; sayfa değişince aynı çipler
        # yeni rozetlerle dolduruluyor. Her sayfada baştan widget üretmek
        # ipuçlarını ve stil durumunu da sıfırlıyordu.
        for index in range(sutun * ROWS):
            chip = BadgeChip()
            # Sütunlar bir kaydırılıyor: 0 ve son sütun boş kalıp esneme
            # payını paylaşıyor, aradaki rozetler ortaya oturuyor. Sola
            # yaslıyken sağda tek parça bir boşluk kalıyordu.
            self._layout.addWidget(
                chip, index // sutun, 1 + index % sutun, Qt.AlignmentFlag.AlignTop
            )
            self._chips.append(chip)

        self._layout.setColumnStretch(0, 1)
        self._layout.setColumnStretch(sutun + 1, 1)

        # Sıra yüksekliği sabitleniyor.
        #
        # Son sayfa yarım kalınca o sıradaki çipler gizleniyor ve
        # `QGridLayout` boş sırayı sıfıra çöktürüyordu: iki rozetlik bir
        # sayfada duvar kısalıyor, altındaki sayfa yazısı da yukarı
        # zıplıyordu. Sıra yüksekliği bir çipin kendi ölçüsünden alınıyor.
        sira = self._chips[0].sizeHint().height()
        for satir in range(ROWS):
            self._layout.setRowMinimumHeight(satir, sira)

        self.setFixedHeight(
            ROWS * sira + (ROWS - 1) * self._layout.verticalSpacing()
        )

        # Sütun sayısı değişince sayfa sayısı da değişiyor; açık sayfa
        # dışarıda kalabilir.
        self._page = min(self._page, self.page_count - 1)
        self._apply_all()
        self.paging_changed.emit()

    def _apply_all(self) -> None:
        kazanilan, kilitli = self._colors
        sayfa = self._page_badges()
        for index, chip in enumerate(self._chips):
            if index >= len(sayfa):
                # Son sayfa yarım kalabiliyor; artan çipler boşaltılıyor,
                # gizlenmiyor — ızgaranın sütunları yerinde kalmalı.
                chip.set_empty()
                continue
            badge = sayfa[index]
            chip.apply(
                badge,
                self._title_maker(badge),
                self._tooltip_maker(badge),
                kazanilan if badge.earned else kilitli,
            )

    def resizeEvent(self, event) -> None:  # noqa: N802
        self._relayout()
        super().resizeEvent(event)
