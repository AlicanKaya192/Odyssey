"""Not editörünün araç çubuğu: Başlık, Kalın, Liste, Kod ▾.

Notlarım ekranı ve bölüm ekranındaki not paneli aynı çubuğu kullanıyor.
İki yerde ayrı ayrı yazılsaydı biri çevrilip öbürü eski dilde kalırdı —
bu projede en sık tekrarlanan hata türü.

Düğmeler odak almıyor: basıldığında editördeki seçim kaybolmasın, işaret
seçimin etrafına konabilsin.
"""

from __future__ import annotations

from PySide6.QtCore import QPoint, Qt
from PySide6.QtWidgets import QHBoxLayout, QMenu, QPushButton, QWidget

from ..resources.theme.tokens import SPACING
from .note_editor import NoteEditor

TOOLS = ("heading", "bold", "list")


def make_tool_button() -> QPushButton:
    """Araç çubuğu düğmesi: küçük, metinli, odak almayan."""
    button = QPushButton()
    button.setProperty("variant", "tool")
    button.setCursor(Qt.CursorShape.PointingHandCursor)
    button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
    return button


class NoteToolbar(QWidget):
    """Bir `NoteEditor`'a bağlı araç çubuğu."""

    def __init__(self, editor: NoteEditor, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setProperty("role", "bare")

        self._row = QHBoxLayout(self)
        self._row.setContentsMargins(0, SPACING["xs"], 0, SPACING["xs"])
        self._row.setSpacing(SPACING["xs"])

        self._buttons: dict[str, QPushButton] = {}
        for key in TOOLS:
            button = make_tool_button()
            self._row.addWidget(button)
            self._buttons[key] = button
        self._buttons["heading"].clicked.connect(editor.toggle_heading)
        self._buttons["bold"].clicked.connect(editor.toggle_bold)
        self._buttons["list"].clicked.connect(editor.toggle_list)

        # Kod düğmesi dil soruyor: Python bloğu renkleniyor, SQL düz duruyor
        # (ders metinlerindeki gibi).
        self._code = make_tool_button()
        self._code_menu = QMenu(self._code)
        self._code_python = self._code_menu.addAction("")
        self._code_sql = self._code_menu.addAction("")
        self._code_python.triggered.connect(lambda: editor.insert_code("python"))
        self._code_sql.triggered.connect(lambda: editor.insert_code("sql"))
        # Menü düğmeye bağlanmıyor, basınca açılıyor: `setMenu` ile bağlı
        # düğme ilk çizildiğinde Qt "QFont::setPointSize: Point size <= 0"
        # uyarısı basıyordu (düz bir düğmede de; ölçüldü). Notlarım'daki
        # "İndir" düğmesi de böyle.
        self._code.clicked.connect(
            lambda: self._code_menu.exec(self._code.mapToGlobal(QPoint(0, self._code.height() + 4)))
        )
        self._row.addWidget(self._code)

        self._row.addStretch(1)

    def add_button(self, button: QPushButton) -> None:
        """Çubuğun sonuna (esnemenin önüne) ekranın kendi düğmesini koyar."""
        self._row.insertWidget(self._row.count() - 1, button)

    def retranslate(self, t) -> None:
        for key, button in self._buttons.items():
            button.setText(t(f"notebook.{key}"))
        self._buttons["bold"].setToolTip("Ctrl+B")
        self._code.setText(f"{t('notebook.code')}  ▾")
        self._code_python.setText(t("notebook.code_python"))
        self._code_sql.setText(t("notebook.code_sql"))
