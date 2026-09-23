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

# Silgi yarıçapı (piksel). Silgi dokunduğu çizginin **yalnızca bu dairenin
# içindeki kısmını** siliyor; çizgi oradan ikiye bölünüyor. Önce dokunduğu
# çizginin tamamını siliyordu — tek harfi düzeltmek isteyen bütün kelimeyi
# kaybediyordu (Alican: "çok op").
ERASER_RADIUS = 11

# Çizgi noktaları en fazla bu kadar aralıklı tutuluyor (piksel). Fare olayları
# seyrek gelebiliyor; iki uzak nokta arasındaki kısım silgiye hiç "nokta"
# vermezse silinemezdi. Araya nokta eklemek silginin çizginin her yerini
# yakalamasını sağlıyor.
POINT_SPACING = 3.0

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


def _densify(stroke: list, width: float) -> list:
    """Noktaları en fazla `POINT_SPACING` piksel aralıklı yapar (eski kayıtlar için)."""
    if len(stroke) < 2:
        return [tuple(p) for p in stroke]
    result = [tuple(stroke[0])]
    for (x0, y0), (x1, y1) in zip(stroke, stroke[1:]):
        distance = math.hypot((x1 - x0) * width, (y1 - y0) * width)
        steps = max(1, math.ceil(distance / POINT_SPACING))
        for step in range(1, steps + 1):
            result.append((
                round(x0 + (x1 - x0) * step / steps, POINT_DIGITS),
                round(y0 + (y1 - y0) * step / steps, POINT_DIGITS),
            ))
    return result


def _is_dot(piece: list, original: list) -> bool:
    """Tek noktalık parça kişinin kendi koyduğu nokta mı (ondalık virgülü gibi)?"""
    return any(len(stroke) == 1 and tuple(stroke[0]) == tuple(piece[0]) for stroke in original)


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
        self._future: list[dict] = []
        self._current: list[tuple[float, float]] | None = None
        self._tool = PEN
        self._stamp = ""
        self._hover: QPointF | None = None
        self._erased = False
        self._last_erase: QPointF | None = None
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
        self._future = []
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

    @property
    def tool(self) -> str:
        return self._tool

    def set_tool(self, tool: str) -> None:
        self._tool = tool
        self._stamp = ""
        # Silgide sistem imleci gizleniyor; imlecin yerine silginin kendisi
        # (dolu daire) çiziliyor. Ok ya da el imleci silginin nereyi sileceğini
        # göstermiyordu ve silginin açık olduğu fark edilmiyordu.
        self.setCursor(
            Qt.CursorShape.BlankCursor if tool == ERASER else Qt.CursorShape.CrossCursor
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

    def can_undo(self) -> bool:
        return bool(self._history)

    def can_redo(self) -> bool:
        return bool(self._future)

    def undo(self) -> None:
        if not self._history:
            return
        self._future.append(self.drawing())
        self._drawing = self._history.pop()
        self.update()
        self.changed.emit()

    def redo(self) -> None:
        if not self._future:
            return
        self._history.append(self.drawing())
        self._drawing = self._future.pop()
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
        """Değişiklikten önceki hâli geçmişe atar; yeni bir değişiklik ileri almayı siler."""
        self._history.append(self.drawing())
        self._future = []
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
            self._last_erase = point
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
                self._erase_along(point)
            elif self._current is not None:
                self._extend_current(point)
        self.update()

    def _erase_along(self, point: QPointF) -> None:
        """Silgiyi son konumdan bu konuma kadar aralıksız sürükler.

        Hızlı bir sürüklemede fare olayları birbirinden uzak geliyor; yalnızca
        o noktalarda silmek arada silinmemiş çizgi adacıkları bırakıyordu.
        """
        start = self._last_erase or point
        distance = math.hypot(point.x() - start.x(), point.y() - start.y())
        steps = max(1, math.ceil(distance / (ERASER_RADIUS / 2)))
        for step in range(1, steps + 1):
            self._erase_at(start + (point - start) * (step / steps))
        self._last_erase = point

    def _extend_current(self, point: QPointF) -> None:
        """Çizgiye nokta ekler; uzak kalan aralığı ara noktalarla doldurur."""
        width = max(1, self.width())
        last_x, last_y = self._current[-1]
        dx, dy = point.x() - last_x * width, point.y() - last_y * width
        steps = max(1, math.ceil(math.hypot(dx, dy) / POINT_SPACING))
        for step in range(1, steps + 1):
            self._current.append(
                self._normal(QPointF(last_x * width + dx * step / steps, last_y * width + dy * step / steps))
            )

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
        if event.matches(QKeySequence.StandardKey.Redo):
            self.redo()
            return
        super().keyPressEvent(event)

    def _erase_at(self, point: QPointF) -> None:
        """Silgi dairesinin içindeki çizgi parçalarını siler, çizgiyi böler.

        Damga (sembol) bölünemez: silgi değerse tamamı siliniyor.
        """
        width = max(1, self.width())
        radius = ERASER_RADIUS / width
        px, py = point.x() / width, point.y() / width

        def near(x: float, y: float) -> bool:
            return (x - px) ** 2 + (y - py) ** 2 <= radius ** 2

        strokes = []
        for stroke in self._drawing["strokes"]:
            dense = _densify(stroke, width)
            if not any(near(x, y) for x, y in dense):
                strokes.append(stroke)
                continue
            piece: list = []
            for x, y in dense:
                if near(x, y):
                    if piece:
                        strokes.append(piece)
                    piece = []
                else:
                    piece.append((x, y))
            if piece:
                strokes.append(piece)
        # Silginin kenarında kalan tek noktalar kâğıtta toz gibi duruyor.
        strokes = [s for s in strokes if len(s) > 1 or len(s) == 1 and _is_dot(s, self._drawing["strokes"])]

        metrics = QFontMetricsF(math_font(width * STAMP_RATIO))
        stamps = []
        for stamp in self._drawing["stamps"]:
            box = metrics.boundingRect(stamp["t"]).translated(stamp["x"] * width, stamp["y"] * width)
            if not box.adjusted(-ERASER_RADIUS, -ERASER_RADIUS, ERASER_RADIUS, ERASER_RADIUS).contains(point):
                stamps.append(stamp)

        if strokes != self._drawing["strokes"] or len(stamps) != len(self._drawing["stamps"]):
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
            # Silginin kendisi: vurgu renginde kenarlı, yarı saydam dolu daire.
            fill = QColor(self._accent)
            fill.setAlpha(55)
            painter.setBrush(fill)
            painter.setPen(QPen(self._accent, 2))
            painter.drawEllipse(self._hover, ERASER_RADIUS, ERASER_RADIUS)
            painter.setBrush(Qt.BrushStyle.NoBrush)

        painter.setClipping(False)
        if self._tool == ERASER:
            # Silgi açıkken kâğıdın çerçevesi vurgu renginde: fare kâğıdın
            # üstünde olmasa da hangi aracın seçili olduğu görünüyor.
            painter.setPen(QPen(self._accent, 2))
            painter.drawRoundedRect(rect.adjusted(0.5, 0.5, -0.5, -0.5), 12, 12)
        else:
            painter.setPen(QPen(self._grid, 1))
            painter.drawRoundedRect(rect, 12, 12)
        painter.end()
