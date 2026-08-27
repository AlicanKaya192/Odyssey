"""Açılışta çıkan beta uyarısı.

Uygulama henüz kapalı beta sürümünde. Kullanan kişi karşılaşacağı şeyi
baştan bilsin diye ilk açılışta kısa bir bilgilendirme çıkıyor: kararsız
çalışabilir, hata verebilir, eksik bölümler olabilir.

Uyarı sürüm başına bir kez gösteriliyor. Her açılışta çıkarsa kısa sürede
okunmadan kapatılan bir engel hâline gelir; hiç tekrarlanmazsa da yeni bir
beta sürümüne geçen kişi neyin değiştiğini bilmez. Görüldüğü sürüm
`beta_notice_seen` ayarında saklanıyor.
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
    """Bu sürümün uyarısı daha önce gösterildi mi?"""
    return store.setting(SETTING_KEY, "") != APP_VERSION


def mark_seen(store: ProgressStore) -> None:
    store.set_setting(SETTING_KEY, APP_VERSION)


class BetaNoticeDialog(QDialog):
    """Kapalı beta bilgilendirmesi."""

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

        # Üç ayrı paragraf: ne beklemeli, verisine ne oluyor, nasıl bildirir.
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
        self.setWindowTitle(self._language.t("beta.title"))
        self._heading.setText(self._language.t("beta.heading"))
        self._body.setText(self._language.t("beta.body"))
        self._data.setText(self._language.t("beta.data"))
        self._feedback.setText(self._language.t("beta.feedback"))
        self._report_button.setText(self._language.t("beta.report"))
        self._close_button.setText(self._language.t("beta.close"))
