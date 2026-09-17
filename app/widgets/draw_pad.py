"""Fareyle çizilen çalışma kâğıdı.

Matematik problemlerinde kişi adımlarını klavyeyle değil **elle yazar gibi**
çiziyor: kök, kesir, üs ve logaritma klavyede yazılamıyor ya da kısayolu
bilinmiyor. Kâğıdın solundaki sembol paleti klavyede zor yazılan işaretleri
tek tıklamayla koyuyor.

Kâğıtta iki tür öğe var:

- **Çizgi:** farenin basılı tutulduğu sürece izlediği noktalar.
- **Damga:** paletten seçilip kâğıda tıklanarak konan bir sembol.

Koordinatlar **kâğıdın genişliğine bölünerek** saklanıyor. Bölücü sürüklenip
kâğıt daraldığında ya da pencere büyüdüğünde çizim de aynı oranda
büyüyüp küçülüyor; kaydedilen çizim başka bir pencere boyutunda da aynı
görünüyor.

Kayıt biçimi (JSON'a doğrudan çevrilebilen sözlük):

```json
{"strokes": [[[x, y], [x, y], ...], ...],
 "stamps": [{"t": "√", "x": 0.2, "y": 0.1}, ...]}
```
"""

from __future__ import annotations

import math

from PySide6.QtCore import QEvent, QPointF, QRectF, Qt, Signal
from PySide6.QtGui import (
    QColor,
    QFont,
    QFontMetricsF,
    QImage,
    QKeySequence,
    QPainter,
    QPainterPath,
    QPen,
)
from PySide6.QtWidgets import QSizePolicy, QWidget

from ..resources.theme.tokens import PALETTES

# Çizgi kalınlığı ve damga yazı boyutu kâğıt genişliğine oranla; kâğıt
# büyüdükçe yazı da büyüyor, el yazısıyla damga birbirine uyumlu kalıyor.
STROKE_RATIO = 0.0034
STAMP_RATIO = 0.05
MIN_STROKE = 2.0

# Kareli kâğıt aralığı (piksel). Matematik defteri hissi veriyor ve elle
# yazılan satırların hizalanmasına yardım ediyor.
GRID_STEP = 28

# Silgi yarıçapı (piksel): imleç bir çizgiye bu kadar yaklaşınca çizgi siliniyor.
ERASER_RADIUS = 12

# Geri alma geçmişi.
HISTORY_LIMIT = 60

# Kaydedilen noktalar bu hassasiyete yuvarlanıyor; kayıt boyutunu küçültüyor.
POINT_DIGITS = 4

# Matematik işaretleri için yazı tipleri; ilk bulunan kullanılıyor.
MATH_FONTS = ["Cambria Math", "Segoe UI Symbol", "Segoe UI"]

PEN = "pen"
ERASER = "eraser"


def empty_drawing() -> dict:
    return {"strokes": [], "stamps": []}


def is_empty(drawing: dict) -> bool:
    return not drawing.get("strokes") and not drawing.get("stamps")


def clean_drawing(value) -> dict:
    """Kayıttan okunan çizimi doğrular; bozuk parçaları atar."""
    drawing = empty_drawing()
    if not isinstance(value, dict):
        return drawing
    for stroke in value.get("strokes", []):
        points = [
            (float(p[0]), float(p[1]))
            for p in stroke
            if isinstance(p, (list, tuple)) and len(p) == 2
        ]
        if points:
            drawing["strokes"].append(points)
    for stamp in value.get("stamps", []):
        if isinstance(stamp, dict) and isinstance(stamp.get("t"), str):
            drawing["stamps"].append(
                {"t": stamp["t"], "x": float(stamp.get("x", 0)), "y": float(stamp.get("y", 0))}
            )
    return drawing


def math_font(pixel_size: float) -> QFont:
    font = QFont()
    font.setFamilies(MATH_FONTS)
    font.setPixelSize(max(8, round(pixel_size)))
    return font


def paint_drawing(painter: QPainter, drawing: dict, width: float, ink: QColor) -> None:
    """Çizimi verilen genişlikte çizer. Kâğıt ve dışa aktarım aynı kodu kullanıyor."""
    pen = QPen(ink, max(MIN_STROKE, width * STROKE_RATIO))
    pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
    painter.setPen(pen)
    painter.setBrush(Qt.BrushStyle.NoBrush)

    for stroke in drawing["strokes"]:
        painter.drawPath(_smooth_path(stroke, width))

    painter.setFont(math_font(width * STAMP_RATIO))
    painter.setPen(ink)
    for stamp in drawing["stamps"]:
        painter.drawText(QPointF(stamp["x"] * width, stamp["y"] * width), stamp["t"])


def _smooth_path(stroke: list, width: float) -> QPainterPath:
    """Noktaları ara noktalardan geçen yumuşak bir eğriye çevirir.

    Fare olayları seyrek geliyor; noktaları düz çizgiyle birleştirmek köşeli
    bir el yazısı veriyor. Her iki nokta arasının ortasından geçen ikinci
    derece eğri daha doğal duruyor.
    """
    points = [QPointF(x * width, y * width) for x, y in stroke]
    path = QPainterPath(points[0])
    if len(points) == 1:
        # Tek tıklama nokta bırakıyor (ondalık virgülü, çarpma noktası).
        path.lineTo(points[0] + QPointF(0.01, 0.01))
        return path
    for index in range(1, len(points) - 1):
        middle = (points[index] + points[index + 1]) / 2
        path.quadTo(points[index], middle)
    path.lineTo(points[-1])
    return path


def drawing_bounds(drawing: dict, width: float) -> QRectF:
    """Çizimin kapladığı alan (piksel); boşsa boş dikdörtgen."""
    rect = QRectF()
    for stroke in drawing["strokes"]:
        for x, y in stroke:
            rect = rect.united(QRectF(x * width, y * width, 1, 1))
    font_metrics = QFontMetricsF(math_font(width * STAMP_RATIO))
    for stamp in drawing["stamps"]:
        box = font_metrics.boundingRect(stamp["t"])
        rect = rect.united(box.translated(stamp["x"] * width, stamp["y"] * width))
    return rect


def render_image(drawing: dict, width: int, ink: QColor) -> QImage | None:
    """Çizimi saydam zeminli bir görsele çevirir; yalnızca dolu kısmı.

    Çözüm yollarının yanında "Senin çalışman" olarak gösteriliyor.
    """
    if is_empty(drawing):
        return None
    bounds = drawing_bounds(drawing, width)
    margin = 16
    top = max(0.0, bounds.top() - margin)
    height = max(40, math.ceil(bounds.bottom() - top + margin))
    image = QImage(width, height, QImage.Format.Format_ARGB32_Premultiplied)
    image.fill(Qt.GlobalColor.transparent)
    painter = QPainter(image)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)
    painter.translate(0, -top)
    paint_drawing(painter, drawing, width, ink)
    painter.end()
    return image


class DrawPad(QWidget):
    """Kareli çalışma kâğıdı: kalem, silgi, damga, geri alma."""

    changed = Signal()
    # Damga konunca ya da iptal edilince palet seçimini bıraksın.
    stamp_finished = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setMinimumHeight(160)
        self.setCursor(Qt.CursorShape.CrossCursor)

        self._drawing = empty_drawing()
        self._history: list[dict] = []
        self._current: list[tuple[float, float]] | None = None
        self._tool = PEN
        self._stamp = ""
        self._hover: QPointF | None = None
        self._erased = False
        self._placeholder = ""
        self.set_mode("dark")

    # --- durum ------------------------------------------------------------

    def drawing(self) -> dict:
        return {
            "strokes": [[list(p) for p in stroke] for stroke in self._drawing["strokes"]],
            "stamps": [dict(s) for s in self._drawing["stamps"]],
        }

    def set_drawing(self, drawing: dict) -> None:
        """Kayıttan yükler; geçmiş sıfırlanıyor (başka problemin geri alması olmaz)."""
        self._drawing = clean_drawing(drawing)
        self._history = []
        self._current = None
        self.update()

    def set_mode(self, mode: str) -> None:
        palette = PALETTES.get(mode, PALETTES["light"])
        self._paper = QColor(palette["field"])
        self._grid = QColor(palette["border_strong"])
        self._grid.setAlpha(90)
        self._ink = QColor(palette["text"])
        self._hint = QColor(palette["text_muted"])
        self._accent = QColor(palette["accent"])
        self.update()

    def ink(self) -> QColor:
        return QColor(self._ink)

    def set_placeholder(self, text: str) -> None:
        self._placeholder = text
        self.update()

    # --- araçlar ----------------------------------------------------------

    def set_tool(self, tool: str) -> None:
        self._tool = tool
        self._stamp = ""
        self.setCursor(
            Qt.CursorShape.PointingHandCursor if tool == ERASER else Qt.CursorShape.CrossCursor
        )
        self.update()

    def arm_stamp(self, text: str) -> None:
        """Bir sonraki tıklama bu sembolü koyacak; imleçte önizlemesi görünür."""
        self._stamp = text
        self.setFocus()
        self.update()

    def cancel_stamp(self) -> None:
        if self._stamp:
            self._stamp = ""
            self.update()
            self.stamp_finished.emit()

    def undo(self) -> None:
        if not self._history:
            return
        self._drawing = self._history.pop()
        self.update()
        self.changed.emit()

    def clear(self) -> None:
        if is_empty(self._drawing):
            return
        self._remember()
        self._drawing = empty_drawing()
        self.update()
        self.changed.emit()

    def _remember(self) -> None:
        self._history.append(self.drawing())
        if len(self._history) > HISTORY_LIMIT:
            self._history.pop(0)

    # --- fare ve klavye ---------------------------------------------------

    def _normal(self, point: QPointF) -> tuple[float, float]:
        width = max(1, self.width())
        return (round(point.x() / width, POINT_DIGITS), round(point.y() / width, POINT_DIGITS))

    def mousePressEvent(self, event) -> None:  # noqa: N802
        if event.button() == Qt.MouseButton.RightButton:
            self.cancel_stamp()
            return
        if event.button() != Qt.MouseButton.LeftButton:
            return
        point = event.position()

        if self._stamp:
            self._remember()
            x, y = self._normal(point)
            self._drawing["stamps"].append({"t": self._stamp, "x": x, "y": y})
            self._stamp = ""
            self.update()
            self.changed.emit()
            self.stamp_finished.emit()
            return

        if self._tool == ERASER:
            self._remember()
            self._erased = False
            self._erase_at(point)
            return

        self._remember()
        self._current = [self._normal(point)]
        self._drawing["strokes"].append(self._current)
        self.update()

    def mouseMoveEvent(self, event) -> None:  # noqa: N802
        point = event.position()
        self._hover = point
        if event.buttons() & Qt.MouseButton.LeftButton:
            if self._tool == ERASER and not self._stamp:
                self._erase_at(point)
            elif self._current is not None:
                self._current.append(self._normal(point))
        self.update()

    def mouseReleaseEvent(self, event) -> None:  # noqa: N802
        if event.button() != Qt.MouseButton.LeftButton:
            return
        if self._current is not None:
            self._current = None
            self.changed.emit()
        elif self._tool == ERASER:
            if self._erased:
                self.changed.emit()
            elif self._history:
                # Hiçbir şey silinmediyse boş bir geri alma adımı kalmasın.
                self._history.pop()

    def leaveEvent(self, event) -> None:  # noqa: N802
        self._hover = None
        self.update()

    def event(self, event) -> bool:  # noqa: D102
        # Pencerenin Esc kısayolu (bölümden çık) tuşu kâğıttan önce yakalıyor.
        # Bekleyen bir damga varsa Esc onu iptal etmeli, bölümden çıkarmamalı.
        if (
            event.type() == QEvent.Type.ShortcutOverride
            and self._stamp
            and event.key() == Qt.Key.Key_Escape
        ):
            event.accept()
            return True
        return super().event(event)

    def keyPressEvent(self, event) -> None:  # noqa: N802
        if event.key() == Qt.Key.Key_Escape and self._stamp:
            self.cancel_stamp()
            return
        if event.matches(QKeySequence.StandardKey.Undo):
            self.undo()
            return
        super().keyPressEvent(event)

    def _erase_at(self, point: QPointF) -> None:
        width = max(1, self.width())
        radius = ERASER_RADIUS / width
        px, py = point.x() / width, point.y() / width

        def near(x: float, y: float) -> bool:
            return (x - px) ** 2 + (y - py) ** 2 <= radius ** 2

        strokes = [s for s in self._drawing["strokes"] if not any(near(x, y) for x, y in s)]

        metrics = QFontMetricsF(math_font(width * STAMP_RATIO))
        stamps = []
        for stamp in self._drawing["stamps"]:
            box = metrics.boundingRect(stamp["t"]).translated(stamp["x"] * width, stamp["y"] * width)
            if not box.adjusted(-ERASER_RADIUS, -ERASER_RADIUS, ERASER_RADIUS, ERASER_RADIUS).contains(point):
                stamps.append(stamp)

        if len(strokes) != len(self._drawing["strokes"]) or len(stamps) != len(self._drawing["stamps"]):
            self._drawing["strokes"] = strokes
            self._drawing["stamps"] = stamps
            self._erased = True
            self.update()

    # --- çizim ------------------------------------------------------------

    def paintEvent(self, event) -> None:  # noqa: N802
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)

        rect = QRectF(self.rect()).adjusted(0.5, 0.5, -0.5, -0.5)
        clip = QPainterPath()
        clip.addRoundedRect(rect, 12, 12)
        painter.fillPath(clip, self._paper)
        painter.setClipPath(clip)

        painter.setPen(QPen(self._grid, 1))
        for x in range(GRID_STEP, self.width(), GRID_STEP):
            painter.drawLine(x, 0, x, self.height())
        for y in range(GRID_STEP, self.height(), GRID_STEP):
            painter.drawLine(0, y, self.width(), y)

        if is_empty(self._drawing) and self._placeholder and not self._stamp:
            painter.setPen(self._hint)
            painter.drawText(
                self.rect().adjusted(24, 24, -24, -24),
                int(Qt.AlignmentFlag.AlignCenter | Qt.TextFlag.TextWordWrap),
                self._placeholder,
            )

        paint_drawing(painter, self._drawing, self.width(), self._ink)

        if self._stamp and self._hover is not None:
            # Konacak sembolün önizlemesi: imlecin tam konacağı yerde, soluk.
            ghost = QColor(self._accent)
            ghost.setAlpha(170)
            painter.setPen(ghost)
            painter.setFont(math_font(self.width() * STAMP_RATIO))
            painter.drawText(self._hover, self._stamp)
        elif self._tool == ERASER and self._hover is not None:
            painter.setPen(QPen(self._hint, 1, Qt.PenStyle.DashLine))
            painter.drawEllipse(self._hover, ERASER_RADIUS, ERASER_RADIUS)

        painter.setClipping(False)
        painter.setPen(QPen(self._grid, 1))
        painter.drawRoundedRect(rect, 12, 12)
        painter.end()
