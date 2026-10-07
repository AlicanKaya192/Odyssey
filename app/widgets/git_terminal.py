"""Git patikasının etkileşimli terminali.

Kişi komut satırına yazıyor, Enter'a basıyor; komut benzeticide
(`core/git_sim.World`) çalışıyor ve çıktı Git Bash'teki renklerle aşağı
ekleniyor. Üstte alıştırmanın hedefleri (✓ tutanlar, ○ kalanlar); her
komuttan sonra güncelleniyor. Yukarı / aşağı ok önceki komutlar, Ctrl+L
ekranı temizler (`clear` da).

Terminalin renkleri iki temada da aynı koyu (alıştırma terminaliyle aynı,
`terminal_view.COLORS`).
"""

from __future__ import annotations

import html

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QKeyEvent, QTextCursor
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from .terminal_view import COLORS

# Benzeticinin renk adları → terminal renkleri (Git Bash'e yakın).
LINE_COLORS = {
    "green": COLORS["ok"],
    "red": COLORS["fail"],
    "yellow": COLORS["warn"],
    "cyan": "#67E8F9",
    "bold": "#E6EDF3",
    "": COLORS["text"],
}
MONO = "Cascadia Mono, Consolas, monospace"
# Ekranda en fazla bu kadar satır tutuluyor (eskiler düşüyor).
MAX_LINES = 1500


class _Input(QLineEdit):
    """Komut satırı: Enter çalıştırır, yukarı/aşağı geçmiş, Ctrl+L temizler."""

    submitted = Signal(str)
    clear_requested = Signal()

    def __init__(self) -> None:
        super().__init__()
        self._history: list[str] = []
        self._pos = 0

    def set_history(self, items: list[str]) -> None:
        self._history = list(items)
        self._pos = len(self._history)

    def keyPressEvent(self, event: QKeyEvent) -> None:  # noqa: N802
        key = event.key()
        if key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            text = self.text()
            if text.strip():
                self._history.append(text)
            self._pos = len(self._history)
            self.clear()
            self.submitted.emit(text)
            return
        if key == Qt.Key.Key_Up and self._history:
            self._pos = max(0, self._pos - 1)
            self.setText(self._history[self._pos])
            return
        if key == Qt.Key.Key_Down and self._history:
            self._pos = min(len(self._history), self._pos + 1)
            self.setText(self._history[self._pos] if self._pos < len(self._history) else "")
            return
        if key == Qt.Key.Key_L and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            self.clear_requested.emit()
            return
        super().keyPressEvent(event)


class GitTerminal(QFrame):
    """Hedefler + terminal ekranı + komut satırı."""

    command_entered = Signal(str)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("gitTerminal")
        self.setStyleSheet(
            f"QFrame#gitTerminal {{ background: {COLORS['bg']}; border: 1px solid {COLORS['border']};"
            " border-radius: 14px; }"
        )
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        bar = QHBoxLayout()
        bar.setContentsMargins(16, 10, 12, 10)
        bar.setSpacing(8)
        for renk in ("#F87171", "#FBBF24", "#4ADE80"):
            nokta = QLabel("●")
            nokta.setStyleSheet(f"color: {renk}; font-size: 11px; background: transparent;")
            bar.addWidget(nokta)
        self._title = QLabel("Terminal")
        self._title.setStyleSheet(f"color: {COLORS['title']}; font-weight: 700; background: transparent;")
        bar.addWidget(self._title)
        bar.addStretch(1)
        self.reset_button = QPushButton()
        self.reset_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.reset_button.setStyleSheet(self._button_qss())
        bar.addWidget(self.reset_button)
        self.clear_button = QPushButton()
        self.clear_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clear_button.setStyleSheet(self._button_qss())
        self.clear_button.clicked.connect(self.clear_screen)
        bar.addWidget(self.clear_button)
        layout.addLayout(bar)

        self._goals = QLabel()
        self._goals.setWordWrap(True)
        self._goals.setTextFormat(Qt.TextFormat.RichText)
        self._goals.setStyleSheet(
            f"color: {COLORS['text']}; background: #11141B; border-top: 1px solid {COLORS['border']};"
            f" border-bottom: 1px solid {COLORS['border']}; padding: 10px 16px; font-size: 13px;"
        )
        layout.addWidget(self._goals)

        self._screen = QTextEdit()
        self._screen.setReadOnly(True)
        self._screen.setFrameShape(QFrame.Shape.NoFrame)
        self._screen.setStyleSheet(
            f"QTextEdit {{ background: {COLORS['bg']}; color: {COLORS['text']}; border: none;"
            f" padding: 8px 14px; font-family: {MONO}; font-size: 13px; }}"
        )
        self._screen.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        self._screen.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        layout.addWidget(self._screen, 1)

        satir = QHBoxLayout()
        satir.setContentsMargins(14, 8, 14, 12)
        satir.setSpacing(8)
        self._prompt = QLabel()
        self._prompt.setStyleSheet(f"color: {COLORS['prompt']}; font-family: {MONO}; font-size: 13px;"
                                   " font-weight: 700; background: transparent;")
        satir.addWidget(self._prompt)
        self._input = _Input()
        self._input.setStyleSheet(
            f"QLineEdit {{ background: transparent; color: {COLORS['text']}; border: none;"
            f" font-family: {MONO}; font-size: 13px; selection-background-color: #2A2F3A; }}"
        )
        self._input.submitted.connect(self.command_entered)
        self._input.clear_requested.connect(self.clear_screen)
        satir.addWidget(self._input, 1)
        layout.addLayout(satir)
        self._lines = 0

    @staticmethod
    def _button_qss() -> str:
        return (f"QPushButton {{ background: transparent; color: {COLORS['title']}; border: 1px solid"
                f" {COLORS['button_border']}; border-radius: 8px; padding: 4px 10px; font-size: 12px; }}"
                f" QPushButton:hover {{ background: {COLORS['button_hover']}; }}")

    # --- dış ----------------------------------------------------------------

    def set_texts(self, title: str, reset: str, clear: str, placeholder: str) -> None:
        self._title.setText(title)
        self.reset_button.setText(reset)
        self.clear_button.setText(clear)
        self._input.setPlaceholderText(placeholder)

    def set_prompt(self, text: str) -> None:
        self._prompt.setText(html.escape(text))

    def set_history(self, commands: list[str]) -> None:
        self._input.set_history(commands)

    def focus_input(self) -> None:
        self._input.setFocus()

    def set_goals(self, title: str, goals: list[tuple[str, bool]]) -> None:
        if not goals:
            self._goals.hide()
            return
        satirlar = [f"<span style='color:{COLORS['dim']}; font-weight:700;'>{html.escape(title)}</span>"]
        for text, ok in goals:
            isaret = (f"<span style='color:{COLORS['ok']};'>✓</span>" if ok
                      else f"<span style='color:{COLORS['dim']};'>○</span>")
            renk = COLORS["dim"] if ok else COLORS["text"]
            satirlar.append(f"{isaret}&nbsp; <span style='color:{renk};'>{html.escape(text)}</span>")
        self._goals.setText("<br>".join(satirlar))
        self._goals.show()

    def clear_screen(self) -> None:
        self._screen.clear()
        self._lines = 0

    def write_command(self, prompt: str, command: str) -> None:
        self._append_html(
            f"<span style='color:{COLORS['prompt']}; font-weight:700;'>{html.escape(prompt)}</span> "
            f"<span style='color:#E6EDF3; white-space:pre-wrap;'>{html.escape(command)}</span>"
        )

    def write_lines(self, lines: list[tuple[str, str]]) -> None:
        for text, color in lines:
            renk = LINE_COLORS.get(color, COLORS["text"])
            agir = " font-weight:700;" if color == "bold" else ""
            # Boşluklar korunuyor (git status hizası), uzun satır yine sarılıyor.
            metin = html.escape(text.expandtabs(8)) or "&nbsp;"
            self._append_html(f"<span style='color:{renk};{agir} white-space:pre-wrap;'>{metin}</span>")

    def write_note(self, text: str, color: str = "ok", bold: bool = True) -> None:
        """Odyssey'nin kendi satırı (hedef tamam, baştan başlandı)."""
        agir = " font-weight:700;" if bold else ""
        self._append_html(f"<span style='color:{COLORS.get(color, COLORS['ok'])};{agir}'>"
                          f"{html.escape(text)}</span>")

    def _append_html(self, fragment: str) -> None:
        cursor = self._screen.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        if self._lines:
            cursor.insertBlock()
        cursor.insertHtml(fragment)
        self._lines += 1
        if self._lines > MAX_LINES:
            doc = self._screen.document()
            first = doc.firstBlock()
            trim = QTextCursor(first)
            trim.select(QTextCursor.SelectionType.BlockUnderCursor)
            trim.removeSelectedText()
            trim.deleteChar()
            self._lines -= 1
        self._screen.setTextCursor(cursor)
        self._screen.ensureCursorVisible()

    def plain_text(self) -> str:
        return self._screen.toPlainText()
