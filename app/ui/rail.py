"""Sol taraftaki dar ikon şeridi.

Uygulamanın ana bölümleri arasında geçiş sağlar: öğrenme yolu, profil, sürüm
notları ve ayarlar. Dar tutulması bilinçli — asıl yer içeriğe kalsın.
"""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QFrame, QLabel, QPushButton, QVBoxLayout, QWidget

from ..core.language import LanguageManager
from ..resources.icons import icon
from ..resources.theme.tokens import PALETTES, RAIL_WIDTH, SPACING
from ..widgets.effects import repolish

# (ekran anahtarı, ikon adı, çeviri anahtarı)
DESTINATIONS = [
    ("journey", "home", "nav.path"),
    ("profile", "user", "nav.profile"),
    ("releases", "megaphone", "nav.releases"),
]


class Rail(QFrame):
    """Ana bölümler arasında geçiş şeridi."""

    navigate = Signal(str)

    def __init__(self, language: LanguageManager, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._language = language
        self._mode = "light"
        self._current = "journey"
        self._buttons: dict[str, QPushButton] = {}

        self.setProperty("role", "rail")
        self.setFixedWidth(RAIL_WIDTH)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, SPACING["lg"], 0, SPACING["lg"])
        layout.setSpacing(SPACING["xs"])
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self._logo = QLabel("A")
        self._logo.setProperty("role", "logo")
        self._logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._logo, 0, Qt.AlignmentFlag.AlignHCenter)
        layout.addSpacing(SPACING["md"])

        for key, icon_name, _ in DESTINATIONS:
            button = self._make_button(key, icon_name)
            layout.addWidget(button, 0, Qt.AlignmentFlag.AlignHCenter)

        layout.addStretch(1)

        settings_button = self._make_button("settings", "settings")
        layout.addWidget(settings_button, 0, Qt.AlignmentFlag.AlignHCenter)

        self.set_mode(self._mode)
        self.retranslate()

    def _make_button(self, key: str, icon_name: str) -> QPushButton:
        button = QPushButton()
        button.setProperty("variant", "rail")
        button.setProperty("icon_name", icon_name)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.clicked.connect(lambda _=False, k=key: self.navigate.emit(k))
        self._buttons[key] = button
        return button

    def set_current(self, key: str) -> None:
        """Hangi bölümde olduğumuzu işaretler.

        Ayarlar bir pencere olarak açıldığı için kalıcı olarak işaretlenmez.
        """
        if key != "settings":
            self._current = key
        self._refresh_icons()

    def set_mode(self, mode: str) -> None:
        self._mode = mode
        self._refresh_icons()

    def _refresh_icons(self) -> None:
        palette = PALETTES.get(self._mode, PALETTES["light"])

        for key, button in self._buttons.items():
            active = key == self._current
            button.setProperty("active", "true" if active else "false")
            button.setIcon(
                icon(
                    button.property("icon_name"),
                    palette["accent"] if active else palette["text_muted"],
                    22,
                )
            )
            button.setIconSize(button.iconSize().scaled(22, 22, Qt.AspectRatioMode.KeepAspectRatio))
            repolish(button)

    def retranslate(self) -> None:
        for key, _, translation_key in DESTINATIONS:
            self._buttons[key].setToolTip(self._language.t(translation_key))
        self._buttons["settings"].setToolTip(self._language.t("settings.title"))
