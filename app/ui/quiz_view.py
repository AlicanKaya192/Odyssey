"""Sınav görünümü (ui-taslak.md C7, F5).

Üç ekran var:

1. **Başlangıç kartı.** Kaç soru, ne kadar süre, geçme puanı üç küçük
   çipte; süre halkası kart açılınca boştan dolarak geliyor; varsa önceki
   denemenin notu. Sorular sekmeye dokunur dokunmaz açılsaydı süre, kişi daha
   ne olduğunu anlamadan işlemeye başlardı.
2. **Sorular, teker teker.** Üstte her soru için bir nokta (sıradaki vurgulu,
   cevaplananlar yeşil ya da kırmızı), sağ üstte süre. Şık seçilince harf
   rozeti esneyerek dolar; "Cevapla" denince doğru şık soldan sağa yeşille
   dolar, yanlış seçilen şık sallanır, açıklama belirir. Sonraki soru sağdan
   kayarak gelir. (0.8.3'e kadar bütün sorular tek sayfada listeleniyor ve
   en sonda toplu gönderiliyordu; prototipte bu akış seçildi.)
3. **Sonuç.** Puan halkası dolar, puan sayar; geçtiyse halka yeşil.

Süre dolunca sınav kendiliğinden bitiyor; cevaplanmamış sorular yanlış
sayılıyor. Her denemede sorular ve şıklar yeniden karışıyor
(`app/core/quiz_shuffle.py`).
"""

from __future__ import annotations

import json
import math
from pathlib import Path

from PySide6.QtCore import Property, QEvent, QPointF, QRectF, Qt, QTimer, Signal
from PySide6.QtGui import QColor, QFont, QPainter, QPainterPath, QPen
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from ..core.language import LanguageManager
from ..core.quiz_shuffle import prepare
from ..resources.icons import icon, pixmap
from ..resources.theme.motion import DISTANCE, bounce, out_cubic
from ..resources.theme.tokens import PALETTES, SPACING, mix
from ..widgets import motion, richtext
from ..widgets.common import Card
from ..widgets.effects import theme_mode, theme_palette
from ..widgets.fade_stack import FORWARD, FadeStack
from ..widgets.timer_ring import TimerRing, format_clock

LETTERS = "ABCDEFGH"


class OptionTile(QFrame):
    """Tek bir şık: harf rozeti ve (zengin) metin; durumu kendisi çiziyor."""

    picked = Signal(int)

    def __init__(self, index: int, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._index = index
        self._selected = False
        self._result = ""        # "", "right", "wrong"
        self._pop = 1.0          # harf rozetinin esnemesi
        self._sweep = 0.0        # doğru şıkta soldan sağa dolan yeşil
        self._shake = 0.0        # yanlış şıkta sallanma
        self._home_x = 0
        self._hover = False
        self._enabled = True
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setAttribute(Qt.WidgetAttribute.WA_Hover, True)
        # Zemini `paintEvent` yuvarlak çiziyor; QSS'in dikdörtgen zemini köşelerde
        # koyu parçalar bırakıyordu.
        self.setProperty("role", "bare")

        row = QHBoxLayout(self)
        row.setContentsMargins(52, 12, 16, 12)
        row.setSpacing(0)
        self.label = QLabel()
        self.label.setWordWrap(True)
        self.label.setTextFormat(Qt.TextFormat.RichText)
        self.label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.label.setStyleSheet("background: transparent;")
        row.addWidget(self.label, 1)
        self.setMinimumHeight(50)

    def _prop(name):  # noqa: N805
        def get(self):
            return getattr(self, "_" + name)

        def set_(self, v):
            setattr(self, "_" + name, v)
            if name == "shake":
                x = round(DISTANCE["shake"] * math.sin(v * math.pi * 6) * (1 - v))
                self.move(self._home_x + x, self.y())
            self.update()
        return Property(float, get, set_)

    pop = _prop("pop")
    sweep = _prop("sweep")
    shake = _prop("shake")
    del _prop

    def set_selected(self, value: bool) -> None:
        if value and not self._selected:
            motion.animate_property(self, "pop", 1.0, "bounce", "linear", start=0.0)
        self._selected = value
        self.update()

    def set_result(self, result: str) -> None:
        self._result = result
        self._enabled = False
        self.setCursor(Qt.CursorShape.ArrowCursor)
        if result == "right":
            motion.animate_property(self, "sweep", 1.0, "long", "out", start=0.0)
        elif result == "wrong":
            self._home_x = self.x()
            motion.animate_property(self, "shake", 1.0, 300, "linear", start=0.0,
                                    on_done=lambda: self.move(self._home_x, self.y()))
        self.update()

    def event(self, e) -> bool:  # noqa: N802
        if e.type() in (QEvent.Type.HoverEnter, QEvent.Type.HoverLeave):
            self._hover = e.type() == QEvent.Type.HoverEnter
            self.update()
        return super().event(e)

    def mouseReleaseEvent(self, event) -> None:  # noqa: N802
        if self._enabled and event.button() == Qt.MouseButton.LeftButton:
            self.picked.emit(self._index)

    def paintEvent(self, event) -> None:  # noqa: N802
        p = theme_palette()
        g = QPainter(self)
        g.setRenderHint(QPainter.RenderHint.Antialiasing)
        r = QRectF(self.rect()).adjusted(1, 1, -1, -1)
        yol = QPainterPath()
        yol.addRoundedRect(r, 14, 14)
        zemin = QColor(p["surface_alt"])
        cerceve = QColor(p["border_strong"] if self._hover and self._enabled else p["border"])
        if self._selected and not self._result:
            zemin = QColor(mix(p["surface_alt"], p["accent"], 0.10))
            cerceve = QColor(p["accent"])
        if self._result == "wrong":
            zemin = QColor(p["danger_soft"])
            cerceve = QColor(p["danger"])
        if self._result == "right":
            cerceve = QColor(p["success"])
        g.fillPath(yol, zemin)
        if self._sweep > 0:
            yesil = QColor(p["success"])
            yesil.setAlphaF(0.16)
            g.save()
            g.setClipPath(yol)
            g.fillRect(QRectF(r.left(), r.top(), r.width() * out_cubic(min(1.0, self._sweep)), r.height()), yesil)
            g.restore()
        g.setPen(QPen(cerceve, 1.5))
        g.drawPath(yol)

        # Harf rozeti.
        kutu = QRectF(14, self.height() / 2 - 13, 26, 26)
        rozet = QColor(p["field"])
        yazi = QColor(p["text_muted"])
        olcek = 1.0
        if self._result == "right":
            rozet, yazi = QColor(p["success"]), QColor("#FFFFFF")
        elif self._result == "wrong":
            rozet, yazi = QColor(p["danger"]), QColor("#FFFFFF")
        elif self._selected:
            rozet, yazi = QColor(p["accent"]), QColor("#FFFFFF")
            olcek = bounce(self._pop)
        g.save()
        g.translate(kutu.center())
        g.scale(olcek, olcek)
        g.setPen(Qt.PenStyle.NoPen)
        g.setBrush(rozet)
        g.drawRoundedRect(QRectF(-13, -13, 26, 26), 8, 8)
        f = QFont(self.font())
        f.setPixelSize(12)
        f.setWeight(QFont.Weight.Bold)
        g.setFont(f)
        g.setPen(yazi)
        g.drawText(QRectF(-13, -13, 26, 26), Qt.AlignmentFlag.AlignCenter, LETTERS[self._index])
        g.restore()


class QuestionCard(QFrame):
    """Tek bir soru: metin, şıklar, cevaplayınca açıklama."""

    answered = Signal(bool)  # doğru mu
    picked = Signal()        # şık seçildi ("Cevapla" etkinleşsin)

    def __init__(self, index: int, question: dict, language: LanguageManager, mode: str = "light") -> None:
        super().__init__()
        self._question = question
        self._language = language
        self._mode = mode
        self._index = index
        self._total = 0
        self._selected: int | None = None
        self._answered = False
        self.setProperty("role", "bare")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(SPACING["sm"] + 1)

        self._text = QLabel()
        self._text.setWordWrap(True)
        self._text.setTextFormat(Qt.TextFormat.RichText)
        self._text.setProperty("role", "question")
        layout.addWidget(self._text)
        layout.addSpacing(SPACING["sm"])

        self._tiles: list[OptionTile] = []
        options = language.pick(question.get("options"), []) or []
        for position, _ in enumerate(options):
            tile = OptionTile(position)
            tile.picked.connect(self._pick)
            self._tiles.append(tile)
            layout.addWidget(tile)

        # Açıklama ampullü, dolgulu bir kutuda; cevaplanınca belirir.
        self._feedback = QFrame()
        self._feedback.setProperty("role", "qwhy")
        self._feedback.hide()
        fb = QHBoxLayout(self._feedback)
        fb.setContentsMargins(SPACING["md"], 12, SPACING["md"], 12)
        fb.setSpacing(SPACING["sm"])
        ampul = QLabel("💡")
        ampul.setFixedWidth(20)
        ampul.setAlignment(Qt.AlignmentFlag.AlignTop)
        fb.addWidget(ampul)
        self._feedback_text = QLabel()
        self._feedback_text.setWordWrap(True)
        self._feedback_text.setTextFormat(Qt.TextFormat.RichText)
        self._feedback_text.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self._feedback_text.setProperty("role", "qwhy-text")
        fb.addWidget(self._feedback_text, 1)
        layout.addSpacing(SPACING["xs"])
        layout.addWidget(self._feedback)
        self.retranslate()

    @property
    def selected(self) -> int | None:
        return self._selected

    @property
    def is_correct(self) -> bool:
        return self._selected == int(self._question.get("answer", -1))

    @property
    def is_answered(self) -> bool:
        return self._answered

    def _pick(self, index: int) -> None:
        if self._answered:
            return
        self._selected = index
        for tile in self._tiles:
            tile.set_selected(tile._index == index)  # noqa: SLF001
        self.picked.emit()

    def reveal(self) -> None:
        """Doğru cevabı ve açıklamayı gösterir."""
        if self._answered:
            return
        self._answered = True
        dogru = int(self._question.get("answer", -1))
        for tile in self._tiles:
            if tile._index == dogru:  # noqa: SLF001
                tile.set_result("right")
            elif tile._index == self._selected:  # noqa: SLF001
                tile.set_result("wrong")
            else:
                tile.set_result("")
        self._render_feedback()
        self._feedback.show()
        self.answered.emit(self.is_correct)

    def _render_feedback(self) -> None:
        dogru = int(self._question.get("answer", -1))
        bas = (self._language.t("quiz.correct") if self.is_correct
               else self._language.t("quiz.correct_is", letter=LETTERS[dogru] if 0 <= dogru < len(LETTERS) else "?"))
        aciklama = self._language.pick(self._question.get("explanation")) or ""
        renk = PALETTES.get(self._mode, PALETTES["light"])["text"]
        self._feedback_text.setText(
            f"<b style='color:{renk}'>{bas}</b> " + richtext.render(aciklama, self._mode))

    def retranslate(self, total: int = 0) -> None:
        self._total = total or self._total
        metin = richtext.render(self._language.pick(self._question.get("text")), self._mode)
        self._text.setText(f"{self._index + 1}. {metin}")
        options = self._language.pick(self._question.get("options"), []) or []
        for tile, option in zip(self._tiles, options):
            tile.label.setText(richtext.render(option, self._mode))
        if self._answered:
            self._render_feedback()

    def set_mode(self, mode: str) -> None:
        self._mode = mode
        self.retranslate(self._total)


class ProgressDots(QWidget):
    """Soru noktaları: sıradaki vurgulu, cevaplananlar yeşil/kırmızı."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._marks: list[str] = []
        self._current = 0
        self.setFixedHeight(6)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

    def set_state(self, marks: list[str], current: int) -> None:
        self._marks, self._current = list(marks), current
        self.update()

    def paintEvent(self, event) -> None:  # noqa: N802
        n = len(self._marks)
        if not n:
            return
        p = theme_palette()
        g = QPainter(self)
        g.setRenderHint(QPainter.RenderHint.Antialiasing)
        bosluk = 6
        w = (self.width() - bosluk * (n - 1)) / n
        for i, mark in enumerate(self._marks):
            renk = {"ok": p["success"], "bad": p["danger"]}.get(mark) or (p["accent"] if i == self._current else p["surface_alt"])
            g.setPen(Qt.PenStyle.NoPen)
            g.setBrush(QColor(renk))
            g.drawRoundedRect(QRectF(i * (w + bosluk), 0, w, 5), 2.5, 2.5)


class ScoreRing(QWidget):
    """Sonuç halkası: dolar, ortadaki puan sayar."""

    def __init__(self, size: int = 150, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._value = 0.0
        self._passed = True
        self._caption = ""
        self.setFixedSize(size, size)

    def _get(self) -> float:
        return self._value

    def _set(self, v: float) -> None:
        self._value = v
        self.update()

    value = Property(float, _get, _set)

    def show_score(self, score: int, passed: bool, caption: str) -> None:
        self._passed, self._caption = passed, caption
        motion.animate_property(self, "value", float(score), 1100, "out", start=0.0)

    def paintEvent(self, event) -> None:  # noqa: N802
        p = theme_palette()
        g = QPainter(self)
        g.setRenderHint(QPainter.RenderHint.Antialiasing)
        k = 9
        r = QRectF(k / 2 + 1, k / 2 + 1, self.width() - k - 2, self.height() - k - 2)
        g.setPen(QPen(QColor(p["surface_alt"]), k))
        g.drawEllipse(r)
        g.setPen(QPen(QColor(p["success"] if self._passed else p["danger"]), k,
                      Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        if self._value > 0:
            g.drawArc(r, 90 * 16, -int(360 * 16 * self._value / 100))
        f = QFont(self.font())
        f.setPixelSize(34)
        f.setWeight(QFont.Weight.Bold)
        g.setFont(f)
        g.setPen(QColor(p["text"]))
        g.drawText(QRectF(0, self.height() / 2 - 30, self.width(), 42), Qt.AlignmentFlag.AlignCenter, str(round(self._value)))
        f.setPixelSize(12)
        f.setWeight(QFont.Weight.DemiBold)
        g.setFont(f)
        g.setPen(QColor(p["text_muted"]))
        g.drawText(QRectF(0, self.height() / 2 + 12, self.width(), 18), Qt.AlignmentFlag.AlignCenter, self._caption)


class QuizView(QWidget):
    """Bir alt bölümün sınavı: başlangıç kartı, sorular, sonuç."""

    completed = Signal(int, bool)  # puan, geçti mi
    # Sonuç ekranındaki "devam" düğmesi: bölümün bir sonraki adımına geç.
    advance = Signal()

    def __init__(self, language: LanguageManager, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._language = language
        self._cards: list[QuestionCard] = []
        self._questions: list[dict] = []
        self._advance_label: str | None = None
        self._pass_score = 70
        self._mode = "light"
        self._current = 0
        self._marks: list[str] = []

        self._time_limit = 0
        self._left = 0
        self._untimed = False
        self._finished = False
        self._previous_score: int | None = None
        self._previous_passed = False
        self._last_score = 0
        self._last_correct = 0

        self._timer = QTimer(self)
        self._timer.setInterval(1000)
        self._timer.timeout.connect(self._tick)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self._stack = QStackedWidget()
        self._stack.addWidget(self._build_start_page())
        self._stack.addWidget(self._build_quiz_page())
        self._stack.addWidget(self._build_result_page())
        layout.addWidget(self._stack)

    # --- sayfalar -------------------------------------------------------------

    def _centered(self, card: QWidget, width: int) -> QWidget:
        page = QWidget()
        outer = QVBoxLayout(page)
        outer.setContentsMargins(SPACING["xl"], SPACING["xl"], SPACING["xl"], SPACING["xl"])
        outer.addStretch(1)
        row = QHBoxLayout()
        row.addStretch(1)
        card.setMaximumWidth(width)
        card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        row.addWidget(card, 10)
        row.addStretch(1)
        outer.addLayout(row)
        outer.addStretch(2)
        return page

    def _build_start_page(self) -> QWidget:
        card = Card(mode=self._mode, padding=30)
        card.setProperty("variant", "qcard")
        self._start_card = card
        self._start_title = QLabel()
        self._start_title.setProperty("role", "qcard-title")
        self._start_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card.body.addWidget(self._start_title)
        card.body.addSpacing(SPACING["sm"])

        # Soru sayısı, süre ve geçme puanı üç çipte (önce tek cümleydi).
        cips = QHBoxLayout()
        cips.setSpacing(SPACING["sm"])
        cips.addStretch(1)
        self._chip_count = QPushButton()
        self._chip_time = QPushButton()
        self._chip_pass = QPushButton()
        for c, v in ((self._chip_count, "chip"), (self._chip_time, "chip"), (self._chip_pass, "chip-accent")):
            c.setProperty("variant", v)
            c.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            c.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
            cips.addWidget(c)
        cips.addStretch(1)
        card.body.addLayout(cips)
        card.body.addSpacing(SPACING["lg"])

        self._preview_ring = TimerRing(150, 9)
        card.body.addWidget(self._preview_ring, 0, Qt.AlignmentFlag.AlignHCenter)
        card.body.addSpacing(22)

        self._previous_label = QLabel()
        self._previous_label.setWordWrap(True)
        self._previous_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._previous_label.hide()
        card.body.addWidget(self._previous_label)
        card.body.addSpacing(SPACING["sm"])

        self._start_button = QPushButton()
        self._start_button.setProperty("variant", "primary")
        self._start_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._start_button.clicked.connect(self._start)
        card.body.addWidget(self._start_button)
        return self._centered(card, 420)

    def _build_quiz_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        self._scroll = scroll

        card = Card(mode=self._mode, padding=30)
        card.setProperty("variant", "qcard")
        self._question_card = card
        ust = QHBoxLayout()
        ust.setSpacing(12)
        self._dots = ProgressDots()
        ust.addWidget(self._dots, 1)
        # Kalan süre kartın içinde, saat simgesiyle (önce sağ üstte ayrı bir
        # halkaydı; prototipte sayaç sorunun başında duruyor).
        self._clock_icon = QLabel()
        self._clock_icon.setFixedSize(15, 15)
        ust.addWidget(self._clock_icon)
        self._counter = QLabel()
        self._counter.setProperty("role", "qtime")
        ust.addWidget(self._counter)
        card.body.addLayout(ust)
        card.body.addSpacing(18 - SPACING["sm"])

        # Sorular yığında; sonraki soru sağdan kayarak geliyor. Yığın kartın
        # zeminini göstermeli: genel `QWidget` kuralı onu sayfa zemininde
        # boyuyor ve kartın ortasında koyu bir dikdörtgen kalıyordu.
        self._questions_stack = FadeStack(drop_old=True)
        self._questions_stack.setProperty("role", "bare")
        card.body.addWidget(self._questions_stack)

        alt = QHBoxLayout()
        alt.addStretch(1)
        self._answer_button = QPushButton()
        self._answer_button.setProperty("variant", "primary")
        self._answer_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._answer_button.clicked.connect(self._on_answer)
        alt.addWidget(self._answer_button)
        card.body.addSpacing(SPACING["md"])
        card.body.addLayout(alt)

        holder = self._centered(card, 640)
        scroll.setWidget(holder)
        layout.addWidget(scroll)
        return page

    def _build_result_page(self) -> QWidget:
        card = Card(mode=self._mode, padding=30)
        card.setProperty("variant", "qcard")
        self._result_card = card
        self._score_ring = ScoreRing(150)
        card.body.addWidget(self._score_ring, 0, Qt.AlignmentFlag.AlignHCenter)
        card.body.addSpacing(22 - SPACING["sm"])
        self._result_title = QLabel()
        self._result_title.setProperty("role", "qcard-title")
        self._result_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card.body.addWidget(self._result_title)
        self._result_detail = QLabel()
        self._result_detail.setProperty("role", "muted")
        self._result_detail.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._result_detail.setWordWrap(True)
        card.body.addWidget(self._result_detail)
        card.body.addSpacing(18 - SPACING["sm"])
        dugmeler = QHBoxLayout()
        dugmeler.addStretch(1)
        self._retry_button = QPushButton()
        self._retry_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._retry_button.clicked.connect(self._reset)
        dugmeler.addWidget(self._retry_button)
        self._advance_button = QPushButton()
        self._advance_button.setProperty("variant", "primary")
        self._advance_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._advance_button.clicked.connect(lambda: self.advance.emit())
        self._advance_button.hide()
        dugmeler.addWidget(self._advance_button)
        dugmeler.addStretch(1)
        card.body.addLayout(dugmeler)
        return self._centered(card, 420)

    # --- yükleme --------------------------------------------------------------

    def show_quiz(self, path: Path, pass_score: int = 70, time_limit_sec: int = 0,
                  previous_score: int | None = None, previous_passed: bool = False,
                  untimed: bool = False) -> None:
        """Sınav dosyasını yükler ve başlangıç kartını gösterir."""
        self._pass_score = pass_score
        self._untimed = bool(untimed)
        self._time_limit = max(0, int(time_limit_sec))
        self._previous_score = previous_score
        self._previous_passed = previous_passed
        with path.open(encoding="utf-8") as handle:
            data = json.load(handle)
        self._questions = data.get("questions", [])
        self._clear()
        self._show_start()

    def set_untimed(self, value: bool) -> None:
        """Süre ayarını o an uygular; sınav açıkken de (sayaç baştan başlar)."""
        value = bool(value)
        if value == self._untimed:
            return
        self._untimed = value
        if self._stack.currentIndex() == 0:
            self._show_start()
            return
        if self._finished:
            return
        if value:
            self._timer.stop()
        elif self._time_limit:
            self._left = self._time_limit
            self._timer.start()
        self._render_clock()

    def _show_start(self) -> None:
        self._timer.stop()
        self._stack.setCurrentIndex(0)
        self._preview_ring.set_untimed(self._untimed)
        self._preview_ring.set_total(self._time_limit)
        self.retranslate()
        if self.isVisible():
            self._preview_ring.play_fill()

    def showEvent(self, event) -> None:  # noqa: N802
        super().showEvent(event)
        if self._stack.currentIndex() == 0:
            self._preview_ring.play_fill()

    def _clear(self) -> None:
        self._finished = False
        for card in self._cards:
            if self._questions_stack.indexOf(card) >= 0:
                self._questions_stack.removeWidget(card)
            card.deleteLater()
        self._cards = []
        self._marks = []
        self._current = 0

    # --- akış -----------------------------------------------------------------

    def _start(self) -> None:
        self._clear()
        for index, question in enumerate(prepare(self._questions)):
            card = QuestionCard(index, question, self._language, self._mode)
            card.answered.connect(self._on_answered)
            card.picked.connect(self._sync_question_ui)
            self._cards.append(card)
        if not self._cards:
            return
        self._marks = [""] * len(self._cards)
        # Yığında yalnızca o anki soru duruyor. Hepsi dururken yığındaki her
        # değişiklikte Qt on kartın zengin metin yüksekliğini baştan
        # hesaplıyordu; sonraki soruya geçiş 60 ms takılıyordu (ölçüldü).
        self._questions_stack.addWidget(self._cards[0])
        self._questions_stack.setCurrentWidget(self._cards[0])
        self._stack.setCurrentIndex(1)
        self._scroll.verticalScrollBar().setValue(0)
        self._sync_question_ui()
        if not self._untimed and self._time_limit:
            self._left = self._time_limit
            self._timer.start()
        self._render_clock()

    def _render_clock(self) -> None:
        """Karttaki saat: kalan süre, azalınca uyarı ve tehlike renginde."""
        p = PALETTES.get(self._mode, PALETTES["light"])
        if self._untimed or not self._time_limit:
            self._counter.setText(self._language.t("quiz.chip_untimed"))
            renk = p["text_muted"]
        else:
            self._counter.setText(format_clock(self._left))
            oran = self._left / self._time_limit
            renk = p["danger"] if oran <= 0.1 else p["warning"] if oran <= 0.25 else p["text_muted"]
        self._counter.setStyleSheet(f"color: {renk};")
        self._clock_icon.setPixmap(pixmap("clock", renk, 15))

    def _sync_question_ui(self) -> None:
        self._dots.set_state(self._marks, self._current)
        self._render_clock()
        card = self._cards[self._current]
        if card.is_answered:
            son = self._current == len(self._cards) - 1
            self._answer_button.setText(self._language.t("quiz.see_result" if son else "quiz.next") + ("" if son else "  →"))
        else:
            self._answer_button.setText(self._language.t("quiz.answer"))
        self._answer_button.setEnabled(card.is_answered or card.selected is not None)

    def _on_answer(self) -> None:
        card = self._cards[self._current]
        if not card.is_answered:
            if card.selected is None:
                return
            card.reveal()
            return
        if self._current + 1 < len(self._cards):
            self._current += 1
            eski = self._questions_stack.currentWidget()
            yeni = self._cards[self._current]
            if self._questions_stack.indexOf(yeni) < 0:
                self._questions_stack.addWidget(yeni)
            self._questions_stack.slide_to(yeni, FORWARD)
            if eski is not None and eski is not yeni:
                self._questions_stack.removeWidget(eski)
            self._sync_question_ui()
        else:
            self._finish()

    def _on_answered(self, correct: bool) -> None:
        self._marks[self._current] = "ok" if correct else "bad"
        self._sync_question_ui()
        # Sıradaki kart kişi açıklamayı okurken yığına girip hazırlanıyor:
        # ilk gösterimdeki stil eşleştirmesi geçişi takılttırıyordu.
        QTimer.singleShot(80, self, self._prepare_next)

    def _prepare_next(self) -> None:
        sira = self._current + 1
        if sira >= len(self._cards):
            return
        kart = self._cards[sira]
        if self._questions_stack.indexOf(kart) < 0:
            self._questions_stack.addWidget(kart)
        kart.ensurePolished()
        for cocuk in kart.findChildren(QWidget):
            cocuk.ensurePolished()
        if kart.layout() is not None:
            kart.layout().activate()


    def _tick(self) -> None:
        self._left -= 1
        self._render_clock()
        if self._left <= 0:
            self._timer.stop()
            self._finish(timed_out=True)

    def _finish(self, timed_out: bool = False) -> None:
        if not self._cards or self._finished:
            return
        self._timer.stop()
        self._finished = True
        correct = sum(1 for c in self._cards if c.is_answered and c.is_correct)
        score = round(correct * 100 / len(self._cards))
        passed = score >= self._pass_score
        self._last_score, self._last_correct = score, correct
        self._stack.setCurrentIndex(2)
        self._render_result(timed_out)
        self._score_ring.show_score(score, passed, self._language.t("quiz.points"))
        self._advance_button.setVisible(bool(self._advance_label))
        self._previous_score = score
        self._previous_passed = passed
        self.completed.emit(score, passed)

    def _render_result(self, timed_out: bool = False) -> None:
        passed = self._last_score >= self._pass_score
        baslik = self._language.t("quiz.result_pass" if passed else "quiz.result_fail")
        if timed_out:
            baslik = self._language.t("quiz.timed_out") + " · " + baslik
        self._result_title.setText(baslik)
        self._result_detail.setText(self._language.t(
            "quiz.result_detail", correct=self._last_correct, total=len(self._cards), pass_score=self._pass_score))

    def _reset(self) -> None:
        """Baştan dene: başlangıç kartına dönüyor, sorular yeniden karışıyor."""
        self._clear()
        self._show_start()

    # --- tema ve dil ----------------------------------------------------------

    def set_mode(self, mode: str) -> None:
        self._mode = mode
        for card in (self._start_card, self._question_card, self._result_card):
            card.set_mode(mode)
        palette = PALETTES.get(mode, PALETTES["light"])
        self._preview_ring.set_colors(palette["surface_alt"], palette["accent"], palette["warning"],
                                      palette["danger"], palette["text"], palette["accent_second"])
        self._preview_ring.set_caption_color(palette["text_muted"])
        for card in self._cards:
            card.set_mode(mode)
        self._paint_chips()

    def _paint_chips(self) -> None:
        p = PALETTES.get(self._mode, PALETTES["light"])
        for chip, name, renk in ((self._chip_count, "clipboard", p["text_muted"]),
                                 (self._chip_time, "clock", p["text_muted"]),
                                 (self._chip_pass, "target", p["accent"])):
            chip.setIcon(icon(name, renk, 14))
        beyaz = "#FFFFFF"
        self._start_button.setIcon(icon("play", beyaz, 16))
        self._retry_button.setIcon(icon("refresh", p["text"], 16))
        if self._cards and self._stack.currentIndex() == 1:
            self._render_clock()

    def set_advance_label(self, label: str | None) -> None:
        """Sonuç ekranındaki "devam" düğmesinin adı; `None` ise düğme yok."""
        self._advance_label = label
        if label:
            self._advance_button.setText(f"{label}  →")
        self._advance_button.setVisible(bool(label) and self._finished)

    def retranslate(self) -> None:
        t = self._language.t
        self._retry_button.setText("  " + t("quiz.retry"))
        self._start_button.setText("  " + t("quiz.start"))
        self._start_title.setText(t("quiz.ready_title"))
        self._preview_ring.set_caption(t("quiz.ring_time"))
        self._chip_count.setText(" " + t("quiz.chip_questions", count=len(self._questions)))
        zamanli = self._time_limit and not self._untimed
        self._chip_time.setText(" " + (format_clock(self._time_limit) if zamanli else t("quiz.chip_untimed")))
        self._chip_pass.setText(" " + t("quiz.chip_pass", pass_score=self._pass_score))
        self._paint_chips()
        if self._previous_score is None:
            self._previous_label.hide()
        else:
            self._previous_label.setText(t("quiz.previous", score=self._previous_score))
            self._previous_label.setProperty("tone", "success" if self._previous_passed else "danger")
            self._previous_label.style().unpolish(self._previous_label)
            self._previous_label.style().polish(self._previous_label)
            self._previous_label.show()
        for card in self._cards:
            card.retranslate(len(self._cards))
        if self._cards and self._stack.currentIndex() == 1:
            self._sync_question_ui()
        if self._finished:
            self._render_result()
            self._score_ring._caption = t("quiz.points")  # noqa: SLF001
            self._score_ring.update()
