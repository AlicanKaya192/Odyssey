"""Alıştırmanın mini terminali.

Önce kod çalıştırılınca editörün altında bir sonuç paneli açılıyordu:
özet satırı, kontrol satırları, grafik ve ayrı bir çıktı kutusu. Beklenen ile
gelen çıktı `repr` ile tek satıra sıkıştırıldığı için çok satırlı tablolar
okunmuyordu (`'   a  b\\n0  1  2\\n…'`). Alican yerine her zaman duran bir
terminal istedi.

Terminal her zaman görünür: açılışta `Odyssey v… · Python` karşılaması,
her çalıştırmada `❯ python cozum.py`, programın çıktısı (hatalar kırmızı) ve
altında sonuç: geçti/geçmedi, düşen kontroller, beklenen ile gelen çıktı
alt alta, hatanın ne anlama geldiği. Yazı eş aralıklı ve satırlar
kaydırılmıyor; tablolar hizalı kalıyor, uzunsa yatay kayıyor.

Renkler iki temada da aynı koyu terminal renkleri: terminal görünümü
bunu bekliyor ve çıktı renkleri (yeşil/kırmızı/sarı) açık zeminde
okunmuyordu.
"""

from __future__ import annotations

import html

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from ..resources.theme.tokens import FONTS

COLORS = {
    "bg": "#0E1117",
    "bar": "#161A22",
    "border": "#262B36",
    "text": "#D5DBE5",
    "dim": "#7C8594",
    "prompt": "#67E8F9",
    "ok": "#4ADE80",
    "fail": "#F87171",
    "warn": "#FBBF24",
    "accent": "#A5A0FF",
}

# Bir çalıştırmanın çıktısı en fazla bu kadar satır gösteriliyor; kalanı
# "… n satır daha" diye özetleniyor. Terminal sonsuz uzamasın.
MAX_OUTPUT_LINES = 400


def _esc(text: str) -> str:
    return html.escape(text, quote=False)


def line(text: str, color: str = "text", bold: bool = False, indent: int = 0) -> str:
    """Tek bir terminal satırı (HTML)."""
    agirlik = "font-weight:700;" if bold else ""
    bosluk = "&nbsp;" * indent
    return (
        f'<div style="color:{COLORS[color]};{agirlik}white-space:pre;">'
        f"{bosluk}{_esc(text) if text else '&nbsp;'}</div>"
    )


def block(text: str, color: str = "text", indent: int = 0) -> str:
    """Çok satırlı metin; satır satır, hizası korunarak."""
    satirlar = text.splitlines() or [""]
    fazla = len(satirlar) - MAX_OUTPUT_LINES
    if fazla > 0:
        satirlar = satirlar[:MAX_OUTPUT_LINES]
    parcalar = [line(s, color, indent=indent) for s in satirlar]
    if fazla > 0:
        parcalar.append(line(f"… +{fazla}", "dim", indent=indent))
    return "".join(parcalar)


class TerminalView(QFrame):
    """Başlık şeridi ve salt okunur terminal alanı."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("terminal")
        self.setStyleSheet(
            f"QFrame#terminal {{ background:{COLORS['bg']}; border:none;"
            f" border-top:1px solid {COLORS['border']}; }}"
        )
        self._blocks: list[str] = []
        self._pending = ""

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        bar = QWidget()
        bar.setObjectName("terminalBar")
        bar.setStyleSheet(
            f"QWidget#terminalBar {{ background:{COLORS['bar']};"
            f" border-bottom:1px solid {COLORS['border']}; }}"
        )
        bar_layout = QHBoxLayout(bar)
        bar_layout.setContentsMargins(14, 6, 10, 6)
        bar_layout.setSpacing(8)
        # Üç nokta ve başlık: terminal penceresi hissi.
        noktalar = QLabel(
            f'<span style="color:#F87171">●</span> '
            f'<span style="color:#FBBF24">●</span> '
            f'<span style="color:#4ADE80">●</span>'
        )
        noktalar.setStyleSheet("background:transparent; font-size:9px;")
        bar_layout.addWidget(noktalar)
        self._title = QLabel()
        self._title.setStyleSheet(
            f"background:transparent; color:{COLORS['dim']}; font-size:12px; font-weight:600;"
        )
        bar_layout.addWidget(self._title)
        bar_layout.addStretch(1)
        self.clear_button = QPushButton()
        self.clear_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clear_button.setStyleSheet(
            f"QPushButton {{ background:transparent; color:{COLORS['dim']}; border:1px solid"
            f" {COLORS['border']}; border-radius:6px; padding:2px 10px; font-size:12px;"
            f" min-height:0px; }}"
            f"QPushButton:hover {{ color:{COLORS['text']}; border-color:{COLORS['dim']}; }}"
        )
        self.clear_button.clicked.connect(self.clear)
        bar_layout.addWidget(self.clear_button)
        layout.addWidget(bar)

        self._text = QTextEdit()
        self._text.setReadOnly(True)
        self._text.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        self._text.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
            | Qt.TextInteractionFlag.TextSelectableByKeyboard
        )
        mono = FONTS["mono"]
        self._text.setStyleSheet(
            f"QTextEdit {{ background:{COLORS['bg']}; color:{COLORS['text']}; border:none;"
            f" padding:8px 14px; font-family:{mono}; font-size:13px;"
            f" selection-background-color:#34405A; }}"
        )
        layout.addWidget(self._text, 1)

        self._welcome = ""

    # --- içerik ----------------------------------------------------------

    def set_title(self, text: str) -> None:
        self._title.setText(text)

    def set_welcome(self, html_lines: str) -> None:
        """Temizlendiğinde gösterilen karşılama (sürüm, ne yapılacağı)."""
        self._welcome = html_lines
        if not self._blocks and not self._pending:
            self._render()

    def clear(self) -> None:
        self._blocks = []
        self._pending = ""
        self._render()

    def begin(self, command_html: str, running_html: str) -> None:
        """Çalıştırma başladı: komut satırı ve geçici "çalışıyor…" satırı."""
        self._pending = command_html + running_html
        self._command = command_html
        self._render()

    def finish(self, body_html: str) -> None:
        """Çalıştırma bitti: geçici satır yerini sonuca bırakıyor."""
        self._blocks.append(getattr(self, "_command", "") + body_html)
        self._pending = ""
        self._render()

    def plain_text(self) -> str:
        return self._text.toPlainText()

    def _render(self) -> None:
        parcalar = [self._welcome] + self._blocks + ([self._pending] if self._pending else [])
        ara = line("")
        self._text.setHtml(ara.join(p for p in parcalar if p))
        bar = self._text.verticalScrollBar()
        bar.setValue(bar.maximum())
        self._text.horizontalScrollBar().setValue(0)
