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

from PySide6.QtCore import Property, QPointF, QRectF, Qt, Signal
from PySide6.QtGui import QColor, QLinearGradient, QPainter, QPainterPath, QPen
from PySide6.QtWidgets import QFrame, QGridLayout, QLabel, QVBoxLayout, QWidget

from ..resources.medals import TIER_ACCENTS, medal_pixmap
from ..resources.theme.motion import bounce
from ..resources.theme.tokens import SPACING
from . import motion
from .fade_stack import BACK, FORWARD, grab_clear, play_swap

# Madalyanın boyu (ui-taslak.md E3: profil duvarında 72 px).
MEDAL = 72

# Bir rozetin adıyla birlikte kapladığı genişlik.
#
# Ad iki satıra sarabiliyor ama **tek kelimelik adlar saramıyor**:
# "Alışkanlık" tek satırda 120 piksel istiyor ve 96 piksellik hücrede
# kırpılıyordu. Genişlik en uzun tek kelimeye göre seçildi.
CELL_WIDTH = 124
# Çipin yüksekliği **sabit**: `QGridLayout` sıra yüksekliğini bir çipin
# `sizeHint`'inden alıyor ve içerik uzunluğuna göre değişen bir yükseklik
# duvarı zıplatıyordu.
#
# Ölçüldü: en uzun rozet adı ("Makine Öğrenmesi Ustası") iki satıra sarıp
# 32 piksel istiyor; daire 56 ve aradaki boşluk 4 ile toplam 92. 120 bunun
# üstünde, yani yeni bir rozet adı biraz daha uzun olsa da kırpılmıyor.
CELL_HEIGHT = 128
MIN_COLUMNS = 3

# Bir sayfada kaç sıra rozet duruyor.
#
# Duvar artık profil kartının yanında, onun boyunda bir kartın içinde;
# sığmayanlar aşağı taşmak yerine sonraki sayfaya geçiyor. Sıra sayısı
# sabit, sütun sayısı genişliğe göre hesaplanıyor.
ROWS = 2


class MedalMark(QWidget):
    """Madalya ve hareketleri (ui-taslak.md C9).

    - üzerine gelince yayla 3 px kalkar, −4° döner, %6 büyür;
    - kazanılmışsa yüzeyinden çapraz bir parlama geçer;
    - son ziyaretten beri kazanıldıysa esneyerek belirir, çevresinden bir
      halka dalgası açılır (kutlama kartıyla aynı dil).
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setFixedSize(MEDAL + 16, MEDAL + 12)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self._pix = None
        self._earned = False
        self._ring_color = QColor("#8B84FF")
        self._hover = 0.0
        self._sheen = 0.0
        self._pop = 1.0
        self._ring = 0.0

    def _prop(name):  # noqa: N805
        def get(self):
            return getattr(self, "_" + name)

        def set_(self, v):
            setattr(self, "_" + name, v)
            self.update()
        return Property(float, get, set_)

    hover = _prop("hover")
    sheen = _prop("sheen")
    pop = _prop("pop")
    ring = _prop("ring")
    del _prop

    def set_medal(self, badge, earned: bool) -> None:
        shape, tier = (list(badge.medal) + ["bronze"])[:2]
        self._pix = medal_pixmap(shape, tier, badge.icon, MEDAL, earned)
        self._earned = earned
        self._ring_color = QColor(TIER_ACCENTS.get(tier, ("#8B84FF",))[0])
        self.update()

    def set_hovered(self, on: bool) -> None:
        if on:
            motion.animate_property(self, "hover", 1.0, "spring", "spring")
            if self._earned:
                motion.animate_property(self, "sheen", 1.0, 700, "out", start=0.0,
                                        on_done=lambda: self._set_sheen0())
        else:
            motion.animate_property(self, "hover", 0.0, "base", "out")

    def _set_sheen0(self) -> None:
        self._sheen = 0.0
        self.update()

    def celebrate(self, delay: int = 200) -> None:
        """Yeni kazanılan rozet: esneyerek belirir, halka dalgası açılır."""
        self._pop = 0.0
        motion.animate_property(self, "pop", 1.0, "bounce", "linear", start=0.0, delay=delay)
        motion.animate_property(self, "ring", 1.0, "celebrate", "out", start=0.0, delay=delay + 50,
                                on_done=lambda: setattr(self, "_ring", 0.0))

    def paintEvent(self, event) -> None:  # noqa: N802
        if self._pix is None:
            return
        g = QPainter(self)
        g.setRenderHint(QPainter.RenderHint.Antialiasing)
        g.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        merkez = QPointF(self.width() / 2, self.height() / 2 + 2 - 3 * self._hover)
        if 0 < self._ring < 1:
            renk = QColor(self._ring_color)
            renk.setAlphaF(0.7 * (1 - self._ring))
            g.setPen(QPen(renk, 2))
            g.setBrush(Qt.BrushStyle.NoBrush)
            rr = MEDAL * 0.42 * (0.9 + 0.8 * self._ring)
            g.drawEllipse(merkez, rr, rr)
        olcek = bounce(self._pop) * (1 + 0.06 * self._hover)
        if olcek <= 0.01:
            return
        g.translate(merkez)
        g.rotate(-4 * self._hover)
        g.scale(olcek, olcek)
        g.drawPixmap(QPointF(-MEDAL / 2, -MEDAL / 2), self._pix)
        if 0 < self._sheen < 1:
            # Çapraz parlama: madalyanın üstünden soldan sağa geçen ışık bandı.
            yol = QPainterPath()
            yol.addEllipse(QPointF(0, -2), MEDAL * 0.36, MEDAL * 0.36)
            g.setClipPath(yol)
            x = -MEDAL * 0.7 + MEDAL * 1.4 * self._sheen
            isik = QLinearGradient(QPointF(x - 14, 0), QPointF(x + 14, 0))
            isik.setColorAt(0.0, QColor(255, 255, 255, 0))
            isik.setColorAt(0.5, QColor(255, 255, 255, 150))
            isik.setColorAt(1.0, QColor(255, 255, 255, 0))
            g.rotate(20)
            g.fillRect(QRectF(x - 14, -MEDAL, 28, MEDAL * 2), isik)


class BadgeChip(QWidget):
    """Madalya ve altında rozetin adı."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setFixedSize(CELL_WIDTH, CELL_HEIGHT)
        self.setAttribute(Qt.WidgetAttribute.WA_Hover, True)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)
        self.circle = MedalMark()
        layout.addWidget(self.circle, 0, Qt.AlignmentFlag.AlignHCenter)
        self.name = QLabel()
        self.name.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.name.setProperty("role", "badge-name")
        self.name.setWordWrap(True)
        self.name.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.name)
        # "YENİ" etiketi: son ziyaretten beri kazanılan rozette.
        self.new_tag = QLabel(self)
        self.new_tag.setProperty("role", "new-tag")
        self.new_tag.hide()
        self._tooltip = ""
        self._badge_id = ""

    def enterEvent(self, event) -> None:  # noqa: N802
        super().enterEvent(event)
        if self.circle.isVisible():
            self.circle.set_hovered(True)

    def leaveEvent(self, event) -> None:  # noqa: N802
        super().leaveEvent(event)
        self.circle.set_hovered(False)

    @property
    def badge_id(self) -> str:
        return self._badge_id

    def set_empty(self) -> None:
        """Çipi boşaltır ama yerinde bırakır (ızgara sütunları kaymasın)."""
        self._tooltip = ""
        self._badge_id = ""
        self.setToolTip("")
        self.circle.hide()
        self.name.hide()
        self.new_tag.hide()

    def apply(self, badge, title: str, tooltip: str, color: str) -> None:
        self._badge_id = badge.id
        self.circle.show()
        self.name.show()
        self.circle.set_medal(badge, badge.earned)
        self.name.setText(title)
        self.name.setProperty("earned", badge.earned)
        self.name.style().unpolish(self.name)
        self.name.style().polish(self.name)
        self._tooltip = tooltip
        # İpucu Qt'nin kendi yoluyla (TooltipStyle ile kısaltılmış bekleme).
        self.setToolTip(tooltip)
        self.new_tag.hide()

    def show_new(self, text: str) -> None:
        self.new_tag.setText(text)
        self.new_tag.adjustSize()
        self.new_tag.move(self.width() - self.new_tag.width() - 14, 2)
        self.new_tag.show()
        self.new_tag.raise_()
        self.circle.celebrate()


class BadgeWall(QWidget):
    """Rozetleri sayfa sayfa ızgara hâlinde gösterir."""

    # Sayfa sayısı ya da açık sayfa değişti; kart oklarını güncelliyor.
    paging_changed = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._layout = QGridLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setHorizontalSpacing(8)
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
        # Prototipte 5 sütun × 2 satır (`.bpage`), dar aralıkla.
        adim = CELL_WIDTH + 8
        return max(MIN_COLUMNS, min(5, (self.width() + 8) // adim))

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

    def set_page(self, index: int, animate: bool = False) -> None:
        index = max(0, min(self.page_count - 1, index))
        if index == self._page:
            return
        # Yarım kalan geçiş önce kapanıyor: katmanı açıkken görüntü alınınca
        # önceki sayfanın rozetleri görüntüye girip takılı kalıyordu (hızlı
        # art arda basınca).
        katman = getattr(self, "_swap_overlay", None)
        if katman is not None and katman.isVisible():
            motion.stop(katman, "t")
            katman.hide()
        eski = grab_clear(self) if animate and self.isVisible() else None
        yon = FORWARD if index > self._page else BACK
        self._page = index
        self._apply_all()
        if eski is not None:
            play_swap(self, eski, yon)
        self.paging_changed.emit()

    def celebrate(self, ids: set, text: str) -> None:
        """Bu sayfadaki yeni rozetleri kutlar (profil açılınca)."""
        for chip in self._chips:
            if chip.badge_id in ids:
                chip.show_new(text)

    def page_of(self, badge_id: str) -> int:
        for i, b in enumerate(self._badges):
            if b.id == badge_id:
                return i // self.page_size
        return 0

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
