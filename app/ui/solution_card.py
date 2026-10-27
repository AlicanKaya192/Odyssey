"""Alıştırmanın kodunu resim olarak paylaşmak (çözüm kartı).

Alican istedi (27 Ekim): kişi yazdığı kodu Discord ya da LinkedIn gibi bir
yerde paylaşabilsin. Kartta alıştırmanın adı, modül ve bölüm, renklendirilmiş
kod (öndeki dosya) ve durum (çözüldü / denendi); üslup profil paylaşım
kartıyla aynı (`ui/profile_card.py`): açılışın morunda, temadan bağımsız.
Her şey bilgisayarda çiziliyor, hiçbir yere gönderilmiyor.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import (
    QAbstractTextDocumentLayout,
    QColor,
    QFont,
    QFontMetricsF,
    QImage,
    QLinearGradient,
    QPainter,
    QPainterPath,
    QTextDocument,
    QTextOption,
)

from ..resources.theme.tokens import FONTS
from ..widgets.code_editor import HIGHLIGHTERS, LANGUAGE_TEXT
from .profile_card import ACCENT, BG_BOTTOM, BG_TOP, MUTED, PROJECT_URL, TEXT, _font

WIDTH = 1200
MARGIN = 60
CODE_PX = 19
MAX_LINES = 40
TAB_WIDTH = 4
PANEL = QColor(8, 6, 22, 190)
PANEL_BORDER = QColor(255, 255, 255, 26)
LINE_NUMBER = QColor(185, 180, 230, 110)
SOLVED = QColor("#4ADE80")
MONO_FAMILY = FONTS["mono"].split(",")[0].strip().strip('"')


@dataclass
class CardData:
    title: str
    place: str
    file_name: str
    language: str
    code: str
    status: str = ""  # "solved", "attempted" ya da boş
    github: str = ""
    labels: dict = field(default_factory=dict)


def _code_lines(code: str) -> tuple[list[str], int]:
    """Karta sığan satırlar ve kesilen satır sayısı (sondaki boş satırlar atılır)."""
    lines = code.expandtabs(TAB_WIDTH).rstrip().split("\n") if code.strip() else [""]
    if len(lines) <= MAX_LINES:
        return lines, 0
    return lines[:MAX_LINES], len(lines) - MAX_LINES


def _code_document(lines: list[str], language: str) -> tuple[QTextDocument, object]:
    """Editörün renklendiricisiyle (koyu tema) boyanmış belge."""
    font = QFont(MONO_FAMILY)
    font.setPixelSize(CODE_PX)
    font.setFixedPitch(True)
    document = QTextDocument()
    document.setDefaultFont(font)
    document.setDocumentMargin(0)
    option = QTextOption()
    option.setWrapMode(QTextOption.WrapMode.NoWrap)
    document.setDefaultTextOption(option)
    document.setPlainText("\n".join(lines))
    highlighter = HIGHLIGHTERS.get(language, HIGHLIGHTERS[LANGUAGE_TEXT])(document, "dark")
    # Renklendirici belgeyle birlikte yaşamalı; çağıran ikisini birlikte tutuyor.
    return document, highlighter


def render(data: CardData) -> QImage:
    lines, hidden = _code_lines(data.code)
    document, _highlighter = _code_document(lines, data.language)
    line_height = QFontMetricsF(document.defaultFont()).lineSpacing()
    # Belgenin kendi yüksekliği: satır aralığı yazı tipinin `lineSpacing`'inden büyük.
    code_lines_height = document.size().height()
    gutter = QFontMetricsF(document.defaultFont()).horizontalAdvance(str(len(lines))) + 28

    code_top = 214
    code_height = 64 + code_lines_height + (line_height + 6 if hidden else 0)
    height = int(code_top + code_height + 96)

    img = QImage(WIDTH, height, QImage.Format.Format_ARGB32_Premultiplied)
    p = QPainter(img)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    p.setRenderHint(QPainter.RenderHint.TextAntialiasing)

    zemin = QLinearGradient(0, 0, WIDTH * 0.4, height)
    zemin.setColorAt(0, BG_TOP)
    zemin.setColorAt(1, BG_BOTTOM)
    p.fillRect(img.rect(), zemin)
    L = data.labels

    # Sağ üst: logo ve ad (profil kartıyla aynı yerde).
    from ..resources import appicon

    p.save()
    p.translate(WIDTH - MARGIN - 56, 44)
    appicon.paint_icon(p, 60)
    p.restore()
    p.setPen(TEXT)
    p.setFont(_font(26, True))
    sag = WIDTH - MARGIN - 56 - 16
    p.drawText(QRectF(sag - 200, 44, 200, 60),
               Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, "Odyssey")

    # Sol üst: modül · bölüm, alıştırmanın adı, durum.
    metin_genislik = sag - 220 - MARGIN
    p.setPen(ACCENT)
    p.setFont(_font(18, True))
    yer = p.fontMetrics().elidedText(data.place, Qt.TextElideMode.ElideRight, int(metin_genislik))
    p.drawText(QRectF(MARGIN, 48, metin_genislik, 28), Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, yer)
    p.setPen(TEXT)
    p.setFont(_font(36, True))
    baslik = p.fontMetrics().elidedText(data.title, Qt.TextElideMode.ElideRight, int(metin_genislik))
    p.drawText(QRectF(MARGIN, 80, metin_genislik, 50), Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, baslik)
    if data.status in ("solved", "attempted"):
        _draw_status(p, data.status, L.get(data.status, ""))

    # Kod paneli: dosya adı, satır numaraları, renkli kod.
    panel = QRectF(MARGIN, code_top, WIDTH - 2 * MARGIN, code_height)
    yol = QPainterPath()
    yol.addRoundedRect(panel, 18, 18)
    p.fillPath(yol, PANEL)
    p.setPen(PANEL_BORDER)
    p.drawPath(yol)
    p.setPen(MUTED)
    p.setFont(_font(16, True))
    p.drawText(QRectF(panel.left() + 28, panel.top() + 14, panel.width() - 56, 24),
               Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, data.file_name)

    kod_sol = panel.left() + 28
    kod_ust = panel.top() + 50
    p.setFont(document.defaultFont())
    p.setPen(LINE_NUMBER)
    yerlesim = document.documentLayout()
    block = document.begin()
    numara = 1
    while block.isValid():
        kutu = yerlesim.blockBoundingRect(block)
        p.drawText(QRectF(kod_sol, kod_ust + kutu.top(), gutter - 20, kutu.height()),
                   Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop, str(numara))
        numara += 1
        block = block.next()

    alan = QRectF(0, 0, panel.right() - 28 - (kod_sol + gutter), code_lines_height + 4)
    p.save()
    p.translate(kod_sol + gutter, kod_ust)
    p.setClipRect(alan)
    context = QAbstractTextDocumentLayout.PaintContext()
    context.clip = alan
    yerlesim.draw(p, context)
    p.restore()
    if hidden:
        p.setPen(MUTED)
        p.setFont(_font(16))
        p.drawText(QRectF(kod_sol + gutter, kod_ust + code_lines_height + 6, 600, line_height),
                   Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                   L.get("more_lines", "+{n}").format(n=hidden))

    # Alt: projenin adresi, varsa kişinin GitHub adresi.
    p.setFont(_font(16))
    p.setPen(MUTED)
    alt = QRectF(MARGIN, height - 64, WIDTH - 2 * MARGIN, 30)
    p.drawText(alt, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, PROJECT_URL)
    if data.github:
        p.drawText(alt, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, f"github.com/{data.github}")
    p.end()
    return img


def _draw_status(p: QPainter, status: str, text: str) -> None:
    """Başlığın altında hap: çözüldüyse yeşil, denendiyse soluk."""
    renk = SOLVED if status == "solved" else MUTED
    p.setFont(_font(17, True))
    genislik = p.fontMetrics().horizontalAdvance(text) + 36
    hap = QRectF(MARGIN, 144, genislik, 36)
    zemin = QColor(renk)
    zemin.setAlpha(36)
    p.setPen(Qt.PenStyle.NoPen)
    p.setBrush(zemin)
    p.drawRoundedRect(hap, 18, 18)
    p.setPen(renk)
    p.drawText(hap, Qt.AlignmentFlag.AlignCenter, text)
    p.setBrush(Qt.BrushStyle.NoBrush)
