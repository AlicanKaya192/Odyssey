"""Bildirim paneli ve butonu.

Footer'ın sağ tarafında zil simgeli bir buton duruyor; butonun üzerinde
okunmamış bildirim sayısı gösteriliyor. Tıklandığında yukarı doğru açılan
bir panel beliriyor ve son bildirimleri listeliyor.

Her bildirimde okundu işareti (✓) var: tıklandığında bildirim soluklaşıyor.
Panelin sağ üstünde "Temizle" düğmesi tüm bildirimleri siliyor.

Panel dışına tıklanınca kendiliğinden kapanıyor.
"""

from __future__ import annotations

from PySide6.QtCore import QPoint, QRect, QRectF, QSize, Qt, Signal
from PySide6.QtGui import QPainter, QColor, QPainterPath, QPen
from PySide6.QtWidgets import (
    QFrame,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from ..resources.icons import icon, pixmap
from ..resources.theme.tokens import PALETTES, RADIUS, SPACING


# Panel ölçüleri.
PANEL_WIDTH = 340
PANEL_MAX_HEIGHT = 400

# Zil düğmesi alt şeritte duruyor; şeridin yazı satırı kadar ince kalması
# için yazıdan biraz yüksek. Sayı rozeti zilin sağ üst köşesinde.
BELL_SIZE = 18
BELL_ICON = 14
BADGE_SIZE = 11

# Pencerenin gölge için bıraktığı saydam pay ve okun içeriğin sağ
# kenarından uzaklığı. `show_above` ikisini kullanarak okun ucunu zilin
# tam ortasına getiriyor.
SHADOW_MARGIN = 24
ARROW_RIGHT = 16
ARROW_HEIGHT = 10

# Başlık çubuğu ve ayırıcı: listeye kalan en fazla yükseklik bundan.
HEADER_ALLOWANCE = 56


class NotificationButton(QPushButton):
    """Footer'ın sağ tarafındaki zil butonu.

    Okunmamış bildirim varsa butonun üzerinde küçük bir sayı rozeti
    çiziliyor.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._count = 0
        self._mode = "dark"
        self.setProperty("variant", "notification-bell")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedSize(BELL_SIZE, BELL_SIZE)
        self.setToolTip("")
        self._refresh_icon()

    def set_count(self, count: int) -> None:
        if self._count == count:
            return
        self._count = count
        self.update()

    def set_mode(self, mode: str) -> None:
        self._mode = mode
        self._refresh_icon()
        self.update()

    def _refresh_icon(self) -> None:
        p = PALETTES.get(self._mode, PALETTES["dark"])
        self.setIcon(icon("bell", p["text_muted"], size=BELL_ICON))
        self.setIconSize(QSize(BELL_ICON, BELL_ICON))

    def paintEvent(self, event) -> None:  # noqa: N802
        super().paintEvent(event)
        if self._count <= 0:
            return

        p = PALETTES.get(self._mode, PALETTES["dark"])
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Sayı rozeti: sağ üst köşede kırmızı daire.
        metin = str(self._count) if self._count <= 9 else "9+"
        boyut = BADGE_SIZE
        x = self.width() - boyut
        y = 0

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(p["danger"]))
        painter.drawEllipse(x, y, boyut, boyut)

        painter.setPen(QColor("#FFFFFF"))
        font = painter.font()
        font.setPixelSize(7)
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(QRect(x, y, boyut, boyut), Qt.AlignmentFlag.AlignCenter, metin)
        painter.end()


class _NotificationItem(QFrame):
    """Tek bir bildirim satırı."""

    mark_read = Signal(int)  # notification id

    def __init__(
        self,
        notification: dict,
        mode: str,
        mark_read_text: str = "",
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._id = notification["id"]
        self._is_read = bool(notification["is_read"])
        self._mode = mode

        self.setProperty("role", "notification-item")
        self.setProperty("read", str(self._is_read).lower())

        layout = QHBoxLayout(self)
        layout.setContentsMargins(SPACING["sm"], SPACING["sm"], SPACING["sm"], SPACING["sm"])
        layout.setSpacing(SPACING["sm"])

        # İkon
        p = PALETTES.get(mode, PALETTES["dark"])
        icon_name = notification.get("icon", "bell")
        if not icon_name:
            icon_name = "trophy" if notification["kind"] == "badge" else "check-circle"
        icon_label = QLabel()
        icon_color = p["accent"] if notification["kind"] == "badge" else p["success"]
        icon_label.setPixmap(pixmap(icon_name, icon_color, size=20))
        icon_label.setFixedSize(24, 24)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon_label)

        # Metin
        # Metin gösterilirken seçili dilde üretiliyor (`text`); yoksa kayıt.
        text_label = QLabel(notification.get("text") or notification["title_key"])
        text_label.setWordWrap(True)
        text_label.setProperty("role", "notification-text")
        if self._is_read:
            text_label.setProperty("read", "true")
        layout.addWidget(text_label, 1)

        # Okundu butonu (tik)
        if not self._is_read:
            check_btn = QPushButton()
            check_btn.setProperty("variant", "notification-check")
            check_btn.setIcon(icon("check-circle", p["success"], size=16))
            check_btn.setIconSize(QSize(16, 16))
            check_btn.setFixedSize(28, 28)
            check_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            check_btn.setToolTip(mark_read_text)
            check_btn.clicked.connect(lambda: self.mark_read.emit(self._id))
            layout.addWidget(check_btn)


class _NotificationContainer(QWidget):
    """Bildirim içeriğini çizen ve gölgeyi barındıran alt katman."""

    def __init__(self, mode: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._mode = mode
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def set_mode(self, mode: str) -> None:
        self._mode = mode
        self._apply_shadow()
        self.update()

    def _apply_shadow(self) -> None:
        from ..resources.theme.tokens import shadow_color
        r, g, b, a = shadow_color(self._mode, strong=True)
        effect = QGraphicsDropShadowEffect(self)
        effect.setBlurRadius(24)
        effect.setOffset(0, 4)
        effect.setColor(QColor(r, g, b, a))
        self.setGraphicsEffect(effect)

    def paintEvent(self, event) -> None:  # noqa: N802
        super().paintEvent(event)

        p = PALETTES.get(self._mode, PALETTES["dark"])
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        arrow_w = 16
        arrow_h = ARROW_HEIGHT
        radius = RADIUS.get("md", 8)

        # Arka plan alanının ana dikdörtgeni (ok hariç)
        rect = QRectF(self.rect())
        rect.setHeight(rect.height() - arrow_h)
        # Sınır çizgisi çizilirken köşeler kesilmesin diye 0.5 pay bırakılıyor
        rect.adjust(0.5, 0.5, -0.5, -0.5)

        path = QPainterPath()
        path.addRoundedRect(rect, radius, radius)

        # Aşağıya doğru üçgen (ok). Ucunun zilin ortasına gelmesini
        # `NotificationPanel.show_above` sağlıyor; burada yalnızca yeri sabit.
        center_x = rect.width() - ARROW_RIGHT
        arrow_path = QPainterPath()
        # Üçgenin üst kenarını dikdörtgenin içine 1px sokuyoruz ki
        # birleştirildiğinde arada çizgi (border) kalmasın, tek parça olsun.
        arrow_path.moveTo(center_x - arrow_w / 2, rect.bottom() - 1)
        arrow_path.lineTo(center_x, rect.bottom() + arrow_h)
        arrow_path.lineTo(center_x + arrow_w / 2, rect.bottom() - 1)
        arrow_path.closeSubpath()

        # Yolları birleştir
        path = path.united(arrow_path)

        painter.setBrush(QColor(p["surface"]))
        painter.setPen(QPen(QColor(p["border"]), 1.0))
        painter.drawPath(path)
        painter.end()


class NotificationPanel(QFrame):
    """Yukarı doğru açılan bildirim paneli."""

    cleared = Signal()
    notification_read = Signal(int)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(
            parent,
            Qt.WindowType.Popup
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.NoDropShadowWindowHint,
        )
        self._mode = "dark"
        self.setProperty("role", "notification-panel")
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFrameShape(QFrame.Shape.NoFrame)

        # Pencere boyutları: İçerik boyutu + Gölge payları (24 sağ/sol/üst)
        self.setFixedWidth(PANEL_WIDTH + 2 * SHADOW_MARGIN)

        main_layout = QVBoxLayout(self)
        # Gölge için ana pencere kenarlarına pay bırakıyoruz
        main_layout.setContentsMargins(
            SHADOW_MARGIN, SHADOW_MARGIN, SHADOW_MARGIN, SHADOW_MARGIN
        )
        main_layout.setSpacing(0)

        self._container = _NotificationContainer(self._mode)
        main_layout.addWidget(self._container)

        root = QVBoxLayout(self._container)
        # İçeriğin alt kısmına üçgen (ok) kadar boşluk
        root.setContentsMargins(0, 0, 0, 10)
        root.setSpacing(0)

        # --- başlık çubuğu ------------------------------------------------
        header = QFrame()
        header.setProperty("role", "notification-header")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(
            SPACING["md"], SPACING["sm"], SPACING["sm"], SPACING["sm"]
        )

        self._title = QLabel()
        self._title.setProperty("role", "notification-title")
        header_layout.addWidget(self._title, 1)

        self._clear_btn = QPushButton()
        self._clear_btn.setProperty("variant", "notification-clear")
        self._clear_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._clear_btn.clicked.connect(self._on_clear)
        # Bildirim yokken düğme gizleniyor ama yeri korunuyor: yoksa başlık
        # çubuğu kısalıyor ve boş durumda panel sıkışık görünüyordu.
        politika = self._clear_btn.sizePolicy()
        politika.setRetainSizeWhenHidden(True)
        self._clear_btn.setSizePolicy(politika)
        header_layout.addWidget(self._clear_btn)

        root.addWidget(header)
        self._header = header

        # --- ayırıcı çizgi ------------------------------------------------
        divider = QFrame()
        divider.setProperty("role", "divider")
        divider.setFixedHeight(1)
        root.addWidget(divider)

        # --- kaydırılabilir liste -----------------------------------------
        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)
        self._scroll.setFrameShape(QFrame.Shape.NoFrame)
        self._scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        self._list = QWidget()
        self._list.setProperty("role", "bare")
        self._list_layout = QVBoxLayout(self._list)
        self._list_layout.setContentsMargins(SPACING["xs"], SPACING["xs"], SPACING["xs"], SPACING["xs"])
        self._list_layout.setSpacing(2)
        self._list_layout.addStretch()

        self._scroll.setWidget(self._list)
        root.addWidget(self._scroll, 1)

        # --- boş durum etiketi -------------------------------------------
        self._empty = QLabel()
        self._empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._empty.setProperty("role", "notification-empty")
        root.addWidget(self._empty)

        self._container._apply_shadow()

    def set_mode(self, mode: str) -> None:
        self._mode = mode
        self._container.set_mode(mode)

    def populate(
        self,
        notifications: list[dict],
        title_text: str,
        clear_text: str,
        empty_text: str,
        mark_read_text: str = "",
    ) -> None:
        """Listeyi verilen bildirimlerle doldurur."""
        self._title.setText(title_text)
        self._clear_btn.setText(clear_text)
        self._empty.setText(empty_text)

        # Eski öğeleri temizle
        while self._list_layout.count() > 1:
            item = self._list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not notifications:
            self._empty.show()
            self._scroll.hide()
            self._clear_btn.hide()
        else:
            self._empty.hide()
            self._scroll.show()
            self._clear_btn.show()
            for notif in notifications:
                item = _NotificationItem(notif, self._mode, mark_read_text)
                item.mark_read.connect(self._on_mark_read)
                self._list_layout.insertWidget(
                    self._list_layout.count() - 1, item
                )
            self._scroll.setFixedHeight(
                min(self._list_height(), PANEL_MAX_HEIGHT - HEADER_ALLOWANCE)
            )

        self._fit_height()

    def _list_height(self) -> int:
        """Satırların toplam yüksekliği, görünürlüğe bakmadan.

        Panel açıkken yeniden dolduruluyor (okundu işareti). Görünür bir
        widget'a eklenen satırları Qt bir sonraki turda gösteriyor; o ana
        kadar gizli sayıldıkları için yerleşimin ölçtüğü boy neredeyse
        sıfırdı. Liste birkaç piksele iniyor, başlık da boş kalan pencerenin
        ortasına kayıyordu. Boy burada satırların kendisinden hesaplanıyor.
        """
        kenar = self._list_layout.contentsMargins()
        genislik = PANEL_WIDTH - kenar.left() - kenar.right()
        satirlar = [
            self._list_layout.itemAt(i).widget()
            for i in range(self._list_layout.count())
        ]
        satirlar = [s for s in satirlar if s is not None]
        toplam = sum(
            s.heightForWidth(genislik) if s.hasHeightForWidth()
            else s.sizeHint().height()
            for s in satirlar
        )
        toplam += self._list_layout.spacing() * max(0, len(satirlar) - 1)
        return toplam + kenar.top() + kenar.bottom()

    def _fit_height(self) -> None:
        """Pencerenin boyu içeriğin toplamı: başlık, çizgi, liste ya da boş
        durum, ok ve gölge payları. Sabitleniyor, çünkü esnek bırakılınca
        önceki açılıştan kalan yükseklik başlığı ortaya itiyordu."""
        if not self._scroll.isHidden():
            govde = self._scroll.height()
        else:
            govde = self._empty.sizeHint().height()
        icerik = self._header.sizeHint().height() + 1 + govde + ARROW_HEIGHT
        self.setFixedHeight(icerik + 2 * SHADOW_MARGIN)

    def _on_mark_read(self, notification_id: int) -> None:
        self.notification_read.emit(notification_id)

    def _on_clear(self) -> None:
        self.cleared.emit()
        self.close()

    def show_above(self, anchor: QWidget) -> None:
        """Paneli verilen widget'ın hemen üstünde gösterir."""
        # Boy `populate` içinde sabitlendi (`_fit_height`).
        global_pos = anchor.mapToGlobal(QPoint(0, 0))
        # Okun ucu zilin ortasına gelsin: ok içeriğin sağ kenarından
        # ARROW_RIGHT içeride, içerik de pencerenin kenarından SHADOW_MARGIN
        # içeride. Ok ucu zilin üst kenarının biraz üstünde duruyor.
        x = (global_pos.x() + anchor.width() // 2
             + SHADOW_MARGIN + ARROW_RIGHT - self.width())
        y = global_pos.y() - self.height() + SHADOW_MARGIN - 4
        self.move(x, y)
        self.show()

    def mousePressEvent(self, event) -> None:  # noqa: N802
        """Pencere içindeki saydam gölge paylarına tıklanırsa paneli kapatır."""
        # Tıklama, asıl içeriği taşıyan _container'ın dışında mı?
        if not self._container.geometry().contains(event.pos()):
            self.close()
        else:
            super().mousePressEvent(event)
