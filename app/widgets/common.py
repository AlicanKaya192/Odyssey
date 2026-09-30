"""Arayüzde tekrar tekrar kullanılan küçük parçalar.

Her ekranda yeniden yazmak yerine burada bir kez tanımlanıyor; görünümleri
stil dosyasındaki özelliklerden (`variant`, `role`, `tone`) geliyor.
"""

from __future__ import annotations

from PySide6.QtCore import QPointF, QRectF, QSize, Qt, QTimer, Signal
from PySide6.QtGui import QColor, QFontMetrics, QPainter, QPen, QPixmap
from PySide6.QtWidgets import (
    QSizePolicy,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ..resources.theme.tokens import SPACING
from .effects import apply_shadow, refresh_shadow, repolish, theme_mode, theme_palette
from . import motion


class Card(QFrame):
    """Gölgeli, yuvarlak köşeli kart."""

    def __init__(
        self,
        parent: QWidget | None = None,
        mode: str = "light",
        strong: bool = False,
        padding: int = SPACING["lg"],
    ) -> None:
        super().__init__(parent)
        self._strong = strong
        self.setProperty("surface", "card")
        apply_shadow(self, mode, strong)

        self.body = QVBoxLayout(self)
        self.body.setContentsMargins(padding, padding, padding, padding)
        self.body.setSpacing(SPACING["sm"])

    def set_mode(self, mode: str) -> None:
        refresh_shadow(self, mode, self._strong)


class SegmentedControl(QFrame):
    """Sekme yerine kullanılan yatay seçici (ui-taslak.md B5).

    Sekmeler ince çerçeveli bir kutunun içinde; seçili sekmenin arkasında
    yükseltilmiş bir hap var ve seçim değişince hap **yayla kayarak** yeni
    sekmenin yerini ve boyunu alıyor. Hapın altında vurgu renginde kısa bir
    çizgi. Kutu, hap ve çizgi `paintEvent`'te; QSS'te geçiş olmadığı için
    önceki alt çizgi bir sekmeden ötekine atlıyordu.
    """

    changed = Signal(int)

    PAD = 4

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setProperty("role", "segment-group")
        # Kutu içeriğinin boyunda: başlık şeridinde dikeyde uzayıp başlığın
        # tamamını kaplıyordu.
        self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(self.PAD, self.PAD, self.PAD, self.PAD)
        self._layout.setSpacing(2)
        self._buttons: list[QPushButton] = []
        self._current = 0
        self._pill = QRectF()
        self._accent: str | None = None
        self._placed = False
        self._icons: list[str] = []
        self._done: list[bool] = []
        self._done_pop: dict[int, float] = {}

    def set_icons(self, names: list[str]) -> None:
        """Sekmelerin simgeleri (iki tonlu set; seçilide dolgu koyulaşır)."""
        self._icons = list(names)
        self._paint_icons()

    def set_done(self, done: list[bool]) -> None:
        """Tamamlanan sekmelerin yanında yeşil onay; yeni tamamlanan esneyerek belirir."""
        onceki = self._done
        self._done = list(done)
        for i, d in enumerate(self._done):
            yeni = d and (i >= len(onceki) or not onceki[i]) and bool(onceki)
            if yeni:
                self._done_pop[i] = 0.0
                motion.animate(self, f"done{i}", 0.0, 1.0,
                               lambda v, k=i: (self._done_pop.__setitem__(k, v), self.update()),
                               "bounce", "linear", on_done=lambda k=i: self._done_pop.pop(k, None))
        for i, button in enumerate(self._buttons):
            metin = button.text().rstrip()
            button.setText(metin + ("      " if i < len(self._done) and self._done[i] else ""))
        QTimer.singleShot(0, self._place_pill)
        self.update()

    def _paint_icons(self) -> None:
        from ..resources.icons import MODERN_FILL_ACTIVE, icon

        renk = theme_palette()
        for i, button in enumerate(self._buttons):
            if i < len(self._icons) and self._icons[i]:
                secili = i == self._current
                button.setIcon(icon(self._icons[i], renk["text"] if secili else renk["text_muted"], 16,
                                    fill_opacity=MODERN_FILL_ACTIVE if secili else None))
                button.setIconSize(QSize(16, 16))
                if not button.text().startswith(" "):
                    button.setText(" " + button.text())

    def set_accent(self, color: str | None) -> None:
        """Hapın altındaki çizginin rengi (boşsa temanın vurgusu)."""
        self._accent = color
        self.update()

    def set_items(self, labels: list[str]) -> None:
        """Seçenekleri yeniden kurar."""
        while self._layout.count():
            item = self._layout.takeAt(0)
            if item.widget():
                # Silinmesi olay döngüsüne kalıyor; o zamana kadar eski yerinde
                # çizilmesin (aynı turda iki kez kurulunca etiketler üst üste
                # biniyordu: alıştırmada Denemelerim ve Çözüm yolları birlikte).
                item.widget().hide()
                item.widget().deleteLater()
        self._buttons = []

        for index, label in enumerate(labels):
            button = QPushButton(label)
            button.setProperty("variant", "segment")
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(lambda _=False, i=index: self.set_current(i))
            self._layout.addWidget(button)
            self._buttons.append(button)

        self._current = min(self._current, max(0, len(labels) - 1))
        self._placed = False
        self._done = []
        self._refresh()

    def set_labels(self, labels: list[str]) -> None:
        """Metinleri değiştirir (dil değişimi), seçimi bozmadan."""
        if len(labels) != len(self._buttons):
            self.set_items(labels)
            return
        for button, label in zip(self._buttons, labels):
            button.setText(label)
        if self._done:
            self.set_done(self._done)
        self._paint_icons()
        self._placed = False
        QTimer.singleShot(0, self._place_pill)

    @property
    def current(self) -> int:
        return self._current

    def set_current(self, index: int, notify: bool = True) -> None:
        if not self._buttons:
            return
        index = max(0, min(index, len(self._buttons) - 1))
        changed = index != self._current
        self._current = index
        self._refresh()
        if notify and changed:
            self.changed.emit(index)

    def _refresh(self) -> None:
        for index, button in enumerate(self._buttons):
            button.setProperty("active", "true" if index == self._current else "false")
            repolish(button)
        self._paint_icons()
        QTimer.singleShot(0, self._place_pill)

    def _target(self) -> QRectF:
        if not self._buttons:
            return QRectF()
        b = self._buttons[self._current]
        return QRectF(b.geometry())

    def _set_pill(self, r: QRectF) -> None:
        self._pill = r
        self.update()

    def _place_pill(self) -> None:
        hedef = self._target()
        if hedef.isEmpty():
            return
        if not self._placed or self._pill.isEmpty() or not self.isVisible():
            self._placed = self.isVisible()
            motion.stop(self, "pill")
            self._set_pill(hedef)
            return
        motion.animate(self, "pill", QRectF(self._pill), hedef, self._set_pill, "spring", "spring")

    def showEvent(self, event) -> None:  # noqa: N802
        super().showEvent(event)
        self._placed = False
        QTimer.singleShot(0, self._place_pill)

    def resizeEvent(self, event) -> None:  # noqa: N802
        super().resizeEvent(event)
        self._placed = False
        QTimer.singleShot(0, self._place_pill)

    def paintEvent(self, event) -> None:  # noqa: N802
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        renk = theme_palette()
        kutu = QRectF(self.rect()).adjusted(0.5, 0.5, -0.5, -0.5)
        zemin = QColor(renk["surface"])
        zemin.setAlphaF(0.7)
        p.setBrush(zemin)
        p.setPen(QPen(QColor(renk["border"]), 1))
        p.drawRoundedRect(kutu, 12, 12)
        if self._pill.isEmpty():
            return
        hap = QRectF(self._pill)
        golge = QColor(0, 0, 0, 46 if theme_mode() == "dark" else 18)
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(golge)
        p.drawRoundedRect(hap.translated(0, 1.5), 9, 9)
        p.setBrush(QColor(renk["surface_alt"] if theme_mode() == "dark" else renk["field"]))
        p.drawRoundedRect(hap, 9, 9)
        cizgi = QColor(self._accent or renk["accent"])
        p.setBrush(cizgi)
        w = hap.width() * 0.4
        p.drawRoundedRect(QRectF(hap.center().x() - w / 2, hap.bottom() - 2.5, w, 2.5), 1.25, 1.25)
        # Tamamlanan sekmenin onayı: metnin sağında küçük yeşil daire.
        from ..resources.theme.motion import bounce

        for i, button in enumerate(self._buttons):
            if i >= len(self._done) or not self._done[i]:
                continue
            g = button.geometry()
            olcek = bounce(self._done_pop[i]) if i in self._done_pop else 1.0
            merkez = QPointF(g.right() - 17, g.center().y() + 0.5)
            p.save()
            p.translate(merkez)
            p.scale(olcek, olcek)
            p.setPen(Qt.PenStyle.NoPen)
            p.setBrush(QColor(renk["success"]))
            p.drawEllipse(QPointF(0, 0), 7.5, 7.5)
            p.setPen(QPen(QColor("#FFFFFF" if theme_mode() == "dark" else "#FFFFFF"), 2,
                          Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
            p.drawPolyline([QPointF(-3.3, 0.2), QPointF(-0.9, 2.6), QPointF(3.4, -2.2)])
            p.restore()


class DropdownBox(QComboBox):
    """Sağında ok çizilen açılır kutu.

    Stil dosyası `drop-down` alanını boş bırakıyor ve kutu oksuz kalıyordu:
    açılabildiği anlaşılmıyor, düz bir metin kutusu gibi duruyordu. QSS oku
    yalnızca diskteki bir resim dosyasından çizebiliyor, simgelerimiz ise
    gömülü SVG; ok burada, tema rengiyle elle çiziliyor.
    """

    def __init__(self, parent: QWidget | None = None, color: str = "#98A1AF") -> None:
        super().__init__(parent)
        self._arrow = QColor(color)

    def set_arrow_color(self, color: str) -> None:
        self._arrow = QColor(color)
        self.update()

    def paintEvent(self, event) -> None:  # noqa: N802
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        pen = QPen(self._arrow, 1.8)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        x = self.width() - 20
        y = self.height() / 2
        painter.drawPolyline([QPointF(x - 4.5, y - 2), QPointF(x, y + 2.5), QPointF(x + 4.5, y - 2)])
        painter.end()


class StatBlock(QWidget):
    """Karşılama kartındaki sayı + açıklama ikilisi."""

    def __init__(
        self,
        value: str = "",
        label: str = "",
        inverse: bool = False,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(SPACING["xs"])

        self._value = QLabel(value)
        self._value.setProperty("role", "title")
        self._label = QLabel(label)
        self._label.setProperty("role", "muted")

        self._label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        if inverse:
            # Renkli zemin üzerinde duruyorsa metin beyaz olmalı.
            from ..resources.theme.tokens import FONTS

            # Prototip: sayı 30 px başlık yazı tipinde, etiket 12,5 px.
            self._value.setStyleSheet(
                f"color: #FFFFFF; font-size: 30px; font-weight: 700; font-family: {FONTS['display']};")
            self._label.setStyleSheet("color: rgba(255,255,255,0.85); font-size: 12.5px;")

        layout.addWidget(self._value)

        # Etiketin yanında isteğe bağlı küçük bir simge (günlük serinin
        # alevi). Boşken gizli; yer kaplamıyor.
        label_row = QHBoxLayout()
        label_row.setContentsMargins(0, 0, 0, 0)
        label_row.setSpacing(4)
        label_row.addWidget(self._label)
        self._icon = QLabel()
        self._icon.hide()
        label_row.addWidget(self._icon, 0, Qt.AlignmentFlag.AlignVCenter)
        label_row.addStretch(1)
        layout.addLayout(label_row)

    def set_icon(self, image: QPixmap | None, tooltip: str = "") -> None:
        """Etiketin yanındaki simgeyi koyar ya da (`None`) kaldırır."""
        if image is None:
            self._icon.hide()
        else:
            self._icon.setPixmap(image)
            self._icon.show()
        # İpucu bütün bloğa veriliyor: yalnızca küçük simgenin üstünde
        # çıksaydı fark edilmiyordu.
        self.setToolTip(tooltip)

    def set_centered(self, value: bool) -> None:
        """Sayıyı altındaki etiketin ortasına hizalar.

        İkisi de sola yaslıyken sayı etiketten çok daha kısa olduğu için
        sola kaçmış duruyordu ("13" 24 piksel, "Çözülen alıştırma" 238).
        Ortalamanın doğru çalışması için widget'ın **etiketi kadar geniş**
        olması gerekiyor; çağıran taraf bloğu sola yaslıyor (ızgarada
        `AlignLeft`, yatay dizide sondaki esneme payı), yoksa sayı bütün
        sütunun ortasına kayıyor.
        """
        hiza = (
            Qt.AlignmentFlag.AlignHCenter if value else Qt.AlignmentFlag.AlignLeft
        )
        self._value.setAlignment(hiza | Qt.AlignmentFlag.AlignBottom)

    def set_value(self, value: str) -> None:
        self._value.setText(value)

    def set_label(self, label: str) -> None:
        self._label.setText(label)


class ElidedText(QLabel):
    """En fazla `lines` satırlık metin; sığmazsa son satır "…" ile bitiyor.

    Kartlarda sarma açık bir etiket, metin uzadıkça kartı büyütüyor ya da
    sabit yükseklikte satırın ortasından kırpılıyordu (patika kartlarında
    açıklamalar yarım satırla bitiyordu). Burada satırlar genişliğe göre
    elle diziliyor; yükseklik her zaman `lines` satır, kesilen metnin
    tamamı ipucunda.
    """

    def __init__(self, lines: int = 2, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._full = ""
        self._lines = max(1, lines)
        self.setWordWrap(False)
        self.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

    def set_full_text(self, text: str) -> None:
        self._full = text or ""
        self._reflow()

    def full_text(self) -> str:
        return self._full

    # Genişliği metin değil yerleşim belirliyor; tek satırlık uzun bir
    # metin kartı genişletmesin.
    def sizeHint(self):  # noqa: N802 (Qt adlandırması)
        hint = super().sizeHint()
        hint.setWidth(0)
        return hint

    def minimumSizeHint(self):  # noqa: N802
        hint = super().minimumSizeHint()
        hint.setWidth(0)
        return hint

    def resizeEvent(self, event) -> None:  # noqa: N802
        super().resizeEvent(event)
        self._reflow()

    def changeEvent(self, event) -> None:  # noqa: N802
        super().changeEvent(event)
        # QSS'ten gelen yazı tipi ancak cilalamada uygulanıyor; satır
        # yüksekliği ve dizilim ona göre yeniden hesaplanıyor.
        if event.type() in (event.Type.FontChange, event.Type.StyleChange):
            self._reflow()

    def _reflow(self) -> None:
        metrics = QFontMetrics(self.font())
        self.setFixedHeight(metrics.lineSpacing() * self._lines + 2)
        width = self.contentsRect().width()
        if width <= 0:
            super().setText(self._full)
            return

        satirlar: list[str] = []
        kalan = self._full.split()
        kesildi = False
        while kalan and len(satirlar) < self._lines:
            if len(satirlar) == self._lines - 1:
                # Son satır: geri kalan her şey, sığmazsa "…" ile.
                son = " ".join(kalan)
                elided = metrics.elidedText(son, Qt.TextElideMode.ElideRight, width)
                kesildi = elided != son
                satirlar.append(elided)
                kalan = []
                break
            satir = kalan.pop(0)
            while kalan and metrics.horizontalAdvance(f"{satir} {kalan[0]}") <= width:
                satir = f"{satir} {kalan.pop(0)}"
            if metrics.horizontalAdvance(satir) > width:
                satir = metrics.elidedText(satir, Qt.TextElideMode.ElideRight, width)
                kesildi = True
            satirlar.append(satir)

        super().setText("\n".join(satirlar))
        self.setToolTip(self._full if kesildi else "")


def paint_hairline(widget: QWidget, edge: str = "bottom") -> None:
    """Ekranı bölen uzun çizgi: tam **bir ekran pikseli** kalınlığında.

    QSS kenarlığı %125 ölçekte 1,25 piksel çiziliyor ve iki piksele yayılıp
    kalın, bulanık görünüyordu (Alican: "çizgiler gözüme batıyor"). Burada
    kozmetik kalem tek bir cihaz pikseli çiziyor; çizgi o pikselin satırına
    oturtuluyor, rengi de kenarlıktan bir ton zemine yakın.
    """
    from ..resources.theme.tokens import mix

    palette = theme_palette()
    painter = QPainter(widget)
    pen = QPen(QColor(mix(palette["border"], palette["bg"], 0.2)))
    pen.setCosmetic(True)
    pen.setWidth(1)
    painter.setPen(pen)
    dpr = widget.devicePixelRatioF() or 1.0
    y = widget.height() - 0.5 / dpr if edge == "bottom" else 0.5 / dpr
    painter.drawLine(QPointF(0, y), QPointF(widget.width(), y))
    painter.end()


class HairlineFrame(QFrame):
    """Altında tek piksellik çizgi olan şerit (bkz. `paint_hairline`)."""

    def paintEvent(self, event) -> None:  # noqa: N802
        super().paintEvent(event)
        paint_hairline(self, "bottom")


def section_label(text: str) -> QLabel:
    """Küçük, seyrek harfli bölüm başlığı."""
    label = QLabel(text.upper())
    label.setProperty("role", "section")
    return label


def horizontal_rule() -> QFrame:
    line = QFrame()
    line.setProperty("role", "separator")
    line.setFrameShape(QFrame.Shape.HLine)
    line.setFixedHeight(1)
    return line
