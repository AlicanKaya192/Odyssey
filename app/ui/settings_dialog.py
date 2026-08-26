"""Ayarlar penceresi: dil ve tema.

Seçimler anında uygulanır — kaydet düğmesine basıp uygulamayı yeniden
başlatmak gerekmiyor. Dil değişince arayüzdeki bütün metinler, tema
değişince bütün renkler o an güncellenir.
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ..core.language import AVAILABLE_LANGUAGES, LanguageManager
from ..core.theme import ThemeManager
from ..resources.theme.tokens import SPACING


class SettingsDialog(QDialog):
    """Dil ve tema ayarları."""

    def __init__(
        self,
        language: LanguageManager,
        theme: ThemeManager,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._language = language
        self._theme = theme

        self.setModal(True)
        self.setMinimumWidth(380)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(SPACING["lg"], SPACING["lg"], SPACING["lg"], SPACING["lg"])
        layout.setSpacing(SPACING["lg"])

        form = QFormLayout()
        form.setSpacing(SPACING["md"])
        form.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)

        self._language_box = QComboBox()
        for code, name in AVAILABLE_LANGUAGES.items():
            self._language_box.addItem(name, code)
        self._language_box.setCurrentIndex(
            self._language_box.findData(language.language)
        )
        self._language_box.currentIndexChanged.connect(self._on_language)

        self._theme_box = QComboBox()
        self._theme_box.currentIndexChanged.connect(self._on_theme)

        self._language_label = form.addRow("", self._language_box)
        form.addRow("", self._theme_box)
        layout.addLayout(form)

        buttons = QHBoxLayout()
        buttons.addStretch(1)
        self._close_button = QPushButton()
        self._close_button.setProperty("variant", "primary")
        self._close_button.clicked.connect(self.accept)
        buttons.addWidget(self._close_button)
        layout.addLayout(buttons)

        self._form = form
        self.retranslate()

    def _on_language(self, index: int) -> None:
        self._language.set_language(self._language_box.itemData(index))

    def _on_theme(self, index: int) -> None:
        value = self._theme_box.itemData(index)
        if value:
            self._theme.set_mode(value)

    def retranslate(self) -> None:
        self.setWindowTitle(self._language.t("settings.title"))
        self._close_button.setText(self._language.t("common.close"))

        # Tema seçenekleri dile bağlı, yeniden dolduruluyor.
        current = self._theme.mode
        self._theme_box.blockSignals(True)
        self._theme_box.clear()
        for value, key in (
            ("system", "settings.theme_system"),
            ("light", "settings.theme_light"),
            ("dark", "settings.theme_dark"),
        ):
            self._theme_box.addItem(self._language.t(key), value)
        self._theme_box.setCurrentIndex(self._theme_box.findData(current))
        self._theme_box.blockSignals(False)

        self._form.labelForField(self._language_box).setText(
            self._language.t("settings.language")
        )
        self._form.labelForField(self._theme_box).setText(
            self._language.t("settings.theme")
        )
