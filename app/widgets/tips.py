"""Programın kendi ipucu kartı: temada, hızlı, okunur.

Qt'nin ipucu Windows'un ipucu penceresini kullanıyordu: geç açılıyor, her
açılışta Windows'un animasyonu oynuyor (rozetten rozete geçerken takılıyor
gibiydi), zengin metni kendiliğinden sarmıyor ve temaya ancak QSS'in izin
verdiği kadar uyuyordu. Alican 2 Ekim'de "geç geliyor, kasıyor, okunmuyor,
tematik olarak kötü" dedi.

Burada tek bir kart penceresi kurulup **yeniden kullanılıyor**:

- Uygulamaya takılan olay süzgeci (`install`) her widget'ın `ToolTip`
  olayını yakalıyor ve Qt'nin ipucu yerine bu kartı gösteriyor. Var olan
  bütün `setToolTip` çağrıları olduğu gibi çalışıyor.
- Kartlar arasında geçerken pencere kapanıp açılmıyor; yalnızca içerik ve
  konum değişiyor. İlk açılış kısa bir saydamlık geçişi.
- Metin kartın genişliğine göre kendiliğinden sarılıyor (`MAX_WIDTH`).
- Başlık + durum + açıklama düzeni için `rich(...)` kullanılır; renkler
  gösterilirken o anki temadan alınıyor, metin temaya bağlı üretilmiyor.
- Kart fareyi tutmuyor (`WindowTransparentForInput`): altındaki widget'ın
  üzerinde durmaya devam ediliyor.

Tek tek kareler için (etkinlik ızgarası gibi) `show_text` / `hide_text`.
"""

from __future__ import annotations

from PySide6.QtCore import QEvent, QObject, QPoint, QPropertyAnimation, QRectF, Qt, QTimer
from PySide6.QtGui import QColor, QCursor, QGuiApplication, QPainter, QPainterPath
from PySide6.QtWidgets import QApplication, QLabel, QLayout, QVBoxLayout, QWidget

MARKER = "\x1fodyssey-tip"
SEP = "\x1f"
MAX_WIDTH = 300
SHADOW = 10
RADIUS = 10
OFFSET = QPoint(14, 20)
FADE_MS = 90
TONES = ("muted", "success", "warning", "danger", "accent")


def rich(title: str, body: str = "", status: str = "", tone: str = "muted") -> str:
    """Başlık, renkli bir durum satırı ve açıklamadan oluşan ipucu metni."""
    return SEP.join([MARKER, title, status, tone if tone in TONES else "muted", body])


def _parse(text: str) -> tuple[str, str, str, str] | None:
    if not text.startswith(MARKER):
        return None
    parcalar = text.split(SEP)[2:]
    parcalar += [""] * (4 - len(parcalar))
    return parcalar[0], parcalar[1], parcalar[2], parcalar[3]


def _palette() -> dict:
    from ..resources.theme.tokens import PALETTES
    from .effects import theme_mode

    return PALETTES.get(theme_mode(), PALETTES["dark"])


class TipCard(QWidget):
    """Gölgeli, yuvarlak köşeli kart; başlık, durum ve açıklama etiketleri."""

    def __init__(self) -> None:
        super().__init__(
            None,
            Qt.WindowType.ToolTip
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowTransparentForInput
            | Qt.WindowType.NoDropShadowWindowHint,
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        self.setStyleSheet("background: transparent;")
        duzen = QVBoxLayout(self)
        duzen.setContentsMargins(SHADOW + 12, SHADOW + 9, SHADOW + 12, SHADOW + 10)
        duzen.setSpacing(3)
        # Kart her içerikte kendi ölçüsünde: kısa ipucundan sonra uzun, uzundan
        # sonra kısa geldiğinde eski boyutta takılı kalmasın.
        duzen.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self._title = QLabel()
        self._status = QLabel()
        self._body = QLabel()
        for etiket in (self._title, self._status, self._body):
            etiket.setWordWrap(True)
            etiket.setTextFormat(Qt.TextFormat.PlainText)
            duzen.addWidget(etiket)
        self._fade = QPropertyAnimation(self, b"windowOpacity", self)
        self._fade.setDuration(FADE_MS)

    def set_text(self, text: str) -> None:
        p = _palette()
        self._colors = (QColor(p["surface"]), QColor(p["border_strong"]))
        yapi = _parse(text)
        if yapi is None:
            # Düz metin (çoğu düğme ipucu): tek etiket, metin rengi.
            baslik, durum, ton, govde = "", "", "muted", text
            govde_stil = f"color: {p['text']}; font-size: 13px;"
        else:
            baslik, durum, ton, govde = yapi
            govde_stil = f"color: {p['text_muted']}; font-size: 13px; padding-top: 4px;"
        renk = p["text_muted"] if ton == "muted" else p.get(ton, p["text_muted"])
        self._title.setStyleSheet(f"color: {p['text']}; font-size: 15px; font-weight: 700;")
        self._status.setStyleSheet(f"color: {renk}; font-size: 12px; font-weight: 600;")
        self._body.setStyleSheet(govde_stil)
        for etiket, deger in ((self._title, baslik), (self._status, durum), (self._body, govde)):
            etiket.setText(deger)
            etiket.setVisible(bool(deger))
        self._fit()

    def _fit(self) -> None:
        """Kısa metinde dar, uzunda `MAX_WIDTH`'te sarılan kart."""
        dogal = 0
        for etiket in (self._title, self._status, self._body):
            if etiket.isVisible() or etiket.text():
                for satir in etiket.text().splitlines() or [""]:
                    dogal = max(dogal, etiket.fontMetrics().horizontalAdvance(satir) + 2)
        genislik = max(40, min(MAX_WIDTH, dogal))
        for etiket in (self._title, self._status, self._body):
            etiket.setFixedWidth(genislik)
        self.layout().activate()
        self.adjustSize()

    def paintEvent(self, event) -> None:  # noqa: N802
        zemin, cerceve = getattr(self, "_colors", (QColor("#171A21"), QColor("#39404E")))
        boya = QPainter(self)
        boya.setRenderHint(QPainter.RenderHint.Antialiasing)
        kart = QRectF(self.rect()).adjusted(SHADOW, SHADOW - 2, -SHADOW, -SHADOW - 2)
        # Yumuşak gölge: genişleyen, sönen yuvarlak dikdörtgenler.
        for i in range(SHADOW, 0, -2):
            golge = QColor(0, 0, 0, int(26 * (1 - i / SHADOW)) + 2)
            yol = QPainterPath()
            yol.addRoundedRect(kart.adjusted(-i, -i + 3, i, i + 3), RADIUS + i, RADIUS + i)
            boya.fillPath(yol, golge)
        yol = QPainterPath()
        yol.addRoundedRect(kart, RADIUS, RADIUS)
        boya.fillPath(yol, zemin)
        boya.setPen(cerceve)
        boya.drawPath(yol)

    def show_at(self, pos: QPoint) -> None:
        ekran = QGuiApplication.screenAt(pos) or QGuiApplication.primaryScreen()
        alan = ekran.availableGeometry()
        x = pos.x() + OFFSET.x() - SHADOW
        y = pos.y() + OFFSET.y() - SHADOW
        if x + self.width() > alan.right():
            x = pos.x() - self.width() - 4 + SHADOW
        if y + self.height() > alan.bottom():
            y = pos.y() - self.height() - 6 + SHADOW
        self.move(max(alan.left(), x), max(alan.top(), y))
        if not self.isVisible():
            self.setWindowOpacity(0.0)
            self.show()
            self._fade.stop()
            self._fade.setStartValue(0.0)
            self._fade.setEndValue(1.0)
            self._fade.start()
        self.raise_()


class TipManager(QObject):
    """Uygulamanın bütün `ToolTip` olaylarını karta çeviren süzgeç."""

    HIDE_EVENTS = {
        QEvent.Type.MouseButtonPress, QEvent.Type.MouseButtonDblClick, QEvent.Type.Wheel,
        QEvent.Type.KeyPress, QEvent.Type.WindowDeactivate, QEvent.Type.ApplicationDeactivate,
    }

    def __init__(self, parent: QObject) -> None:
        super().__init__(parent)
        self.card = TipCard()
        self._anchor: QWidget | None = None
        self._text = ""
        # Fare hedeften çıkınca kart kalmasın; Leave olayı her zaman gelmiyor
        # (pencere üstünde açılan katmanlar), konum da denetleniyor.
        self._watch = QTimer(self)
        self._watch.setInterval(150)
        self._watch.timeout.connect(self._check_cursor)

    def show_text(self, pos: QPoint, text: str, anchor: QWidget | None) -> None:
        if not text:
            self.hide_text()
            return
        if text != self._text or not self.card.isVisible():
            self._text = text
            self.card.set_text(text)
        self._anchor = anchor
        self.card.show_at(pos)
        self._watch.start()

    def hide_text(self) -> None:
        self._watch.stop()
        self._anchor = None
        self._text = ""
        self.card.hide()

    def _check_cursor(self) -> None:
        hedef = self._anchor
        if hedef is None:
            self.hide_text()
            return
        try:
            gorunur = hedef.isVisible()
            icinde = hedef.rect().contains(hedef.mapFromGlobal(QCursor.pos()))
        except RuntimeError:  # hedef silindi
            gorunur = icinde = False
        if not (gorunur and icinde):
            self.hide_text()

    def eventFilter(self, obj, event) -> bool:  # noqa: N802
        tur = event.type()
        if tur == QEvent.Type.ToolTip and isinstance(obj, QWidget):
            metin = obj.toolTip()
            if not metin:
                return False  # üst widget'a geçsin
            self.show_text(event.globalPos(), metin, obj)
            return True
        try:
            acik = self.card.isVisible()
        except RuntimeError:  # kapanışta kart süzgeçten önce siliniyor
            return False
        if acik:
            if tur in self.HIDE_EVENTS:
                self.hide_text()
            elif tur == QEvent.Type.Leave and obj is self._anchor:
                self.hide_text()
        return False


_manager: TipManager | None = None


def install(app: QApplication) -> TipManager:
    """Süzgeci bir kez takar; tekrar çağrılırsa var olanı döndürür."""
    global _manager
    if _manager is None:
        _manager = TipManager(app)
        app.installEventFilter(_manager)
        app.aboutToQuit.connect(lambda: app.removeEventFilter(_manager))
    return _manager


def show_text(pos: QPoint, text: str, anchor: QWidget | None = None) -> None:
    """Beklemeden göster (etkinlik ızgarasının kareleri gibi)."""
    app = QApplication.instance()
    if app is not None:
        install(app).show_text(pos, text, anchor)


def hide_text() -> None:
    if _manager is not None:
        _manager.hide_text()

