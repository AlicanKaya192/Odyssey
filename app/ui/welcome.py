"""İlk kurulumda çıkan hoş geldiniz penceresi.

1.0'a kadar burada açık beta uyarısı vardı ("kararsız çalışabilir").
1.0'da uyarı kalktı; yeni kuran kişiye programın ne olduğu, verisinin
yalnızca kendi bilgisayarında durduğu ve sorunu nasıl bildireceği
anlatılıyor.

Sürüm başına bir kez sayılıyor: ayar boşsa (ilk kurulum) bu pencere,
doluysa ve sürüm değiştiyse (güncelleme) "Neler yeni?" çıkıyor
(`main.py`). Görülen sürüm `beta_notice_seen` ayarında; ad eski ama
değiştirilmiyor, yoksa güncelleyen herkes ilk kurulum sayılıp bu pencereyi
görürdü.
"""

from __future__ import annotations

import webbrowser

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ..core.language import LanguageManager
from ..core.progress import ProgressStore
from ..resources.theme.tokens import SPACING
from ..version import APP_VERSION

SETTING_KEY = "beta_notice_seen"
ISSUES_URL = "https://github.com/AlicanKaya192/Odyssey/issues"


def should_show(store: ProgressStore) -> bool:
    """Bu sürüm için açılış penceresi (hoş geldiniz ya da "Neler yeni?") gösterildi mi?"""
    return store.setting(SETTING_KEY, "") != APP_VERSION


def mark_seen(store: ProgressStore) -> None:
    store.set_setting(SETTING_KEY, APP_VERSION)


class WelcomeDialog(QDialog):
    """İlk kurulumdaki hoş geldiniz penceresi."""

    def __init__(
        self,
        language: LanguageManager,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._language = language

        self.setModal(True)
        self.setMinimumWidth(460)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            SPACING["lg"], SPACING["lg"], SPACING["lg"], SPACING["lg"]
        )
        layout.setSpacing(SPACING["md"])

        self._heading = QLabel()
        self._heading.setProperty("role", "title")
        self._heading.setWordWrap(True)
        layout.addWidget(self._heading)

        # Üç ayrı paragraf: program ne, verisine ne oluyor, nasıl bildirir.
        self._body = QLabel()
        self._data = QLabel()
        self._feedback = QLabel()
        for label in (self._body, self._data, self._feedback):
            label.setWordWrap(True)
            label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            layout.addWidget(label)

        layout.addSpacing(SPACING["xs"])

        buttons = QHBoxLayout()
        self._report_button = QPushButton()
        self._report_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._report_button.clicked.connect(self._open_issues)
        buttons.addWidget(self._report_button)
        buttons.addStretch(1)

        self._close_button = QPushButton()
        self._close_button.setProperty("variant", "primary")
        self._close_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._close_button.clicked.connect(self.accept)
        buttons.addWidget(self._close_button)
        layout.addLayout(buttons)

        self._close_button.setDefault(True)
        self.retranslate()

    def _open_issues(self) -> None:
        """Adresi sistemin tarayıcısına veriyor; uygulama ağa çıkmıyor."""
        webbrowser.open(ISSUES_URL)

    def retranslate(self) -> None:
        self.setWindowTitle(self._language.t("welcome.title"))
        self._heading.setText(self._language.t("welcome.heading"))
        self._body.setText(self._language.t("welcome.body"))
        self._data.setText(self._language.t("welcome.data"))
        self._feedback.setText(self._language.t("welcome.feedback"))
        self._report_button.setText(self._language.t("welcome.report"))
        self._close_button.setText(self._language.t("welcome.close"))
