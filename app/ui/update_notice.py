"""Yeni sürüm çıktığında açılan bilgilendirme penceresi.

Şeritteki satır kalıcı ama sessiz: bakmayan görmüyor. Yeni bir sürüm ilk
kez görüldüğünde bir kez de pencere açılıyor, böylece güncelleme kaçmıyor.

**Sürüm başına bir kez.** Aynı sürüm için her açılışta çıkan bir kutu,
okunmadan kapatılan bir engele dönüşüyor — beta uyarısında da aynı kural
var. Gösterildiği sürüm `update_notified` ayarında saklanıyor.

Pencere yalnızca **açılışta** yapılan denetimden sonra çıkıyor. Uygulama
açıkken üç saatte bir yapılan denetim yalnızca şeridi güncelliyor: ders
okurken ya da sınav çözerken önüne kutu çıkması, verdiği bilgiden daha çok
rahatsız ederdi.
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
from ..core.updates import UpdateInfo
from ..resources.theme.tokens import SPACING
from ..version import APP_VERSION


class UpdateNoticeDialog(QDialog):
    """"Yeni sürüm yayınlandı" kutusu."""

    def __init__(
        self,
        language: LanguageManager,
        info: UpdateInfo,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._language = language
        self._info = info

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

        # İki paragraf: ne çıktı, ne yapman gerekiyor.
        self._body = QLabel()
        self._howto = QLabel()
        for label in (self._body, self._howto):
            label.setWordWrap(True)
            label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            layout.addWidget(label)

        layout.addSpacing(SPACING["xs"])

        buttons = QHBoxLayout()
        self._later_button = QPushButton()
        self._later_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._later_button.clicked.connect(self.reject)
        buttons.addWidget(self._later_button)
        buttons.addStretch(1)

        self._open_button = QPushButton()
        self._open_button.setProperty("variant", "primary")
        self._open_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._open_button.clicked.connect(self._open_page)
        buttons.addWidget(self._open_button)
        layout.addLayout(buttons)

        self._open_button.setDefault(True)
        self.retranslate()

    def _open_page(self) -> None:
        """Adresi sistemin tarayıcısına veriyor; uygulama sayfayı açmıyor."""
        webbrowser.open(self._info.url)
        self.accept()

    def retranslate(self) -> None:
        t = self._language.t
        self.setWindowTitle(t("update.notice_title"))
        self._heading.setText(
            t("update.notice_heading", version=self._info.version)
        )
        self._body.setText(
            t("update.notice_body", version=self._info.version, current=APP_VERSION)
        )
        self._howto.setText(t("update.notice_howto"))
        self._later_button.setText(t("update.notice_later"))
        self._open_button.setText(t("update.notice_open"))
