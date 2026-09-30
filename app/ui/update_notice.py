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

Görünüm ayarlar penceresiyle aynı (çerçevesiz, yuvarlak; `modal.py`);
üstünde açılış animasyonunun sahnesi, sentor nişan alıp bekliyor.
"Güncelle"ye basınca kutu kapanıyor ve indirme ayrı, sıradan bir pencerede
sürüyor (`update_window.py`).
"""

from __future__ import annotations

import webbrowser

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ..core import updater
from ..core.language import LanguageManager
from ..core.updates import UpdateInfo
from ..resources.theme.tokens import SPACING
from ..version import APP_VERSION
from . import modal
from .update_scene import UpdateScene

WIDTH = 540


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
        modal.prepare(self)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(SPACING["lg"], SPACING["lg"], SPACING["lg"], SPACING["lg"])
        layout.setSpacing(SPACING["md"])

        self._scene = UpdateScene("idle")
        self._scene.setFixedHeight(160)
        layout.addWidget(self._scene)
        layout.addSpacing(SPACING["xs"])

        self._heading = QLabel()
        self._heading.setProperty("role", "modal-page-title")
        self._heading.setWordWrap(True)
        layout.addWidget(self._heading)

        # İki paragraf: ne çıktı, ne yapman gerekiyor.
        self._body = QLabel()
        self._howto = QLabel()
        for label in (self._body, self._howto):
            label.setWordWrap(True)
            label.setProperty("role", "muted")
            label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            layout.addWidget(label)

        layout.addSpacing(SPACING["xs"])

        buttons = QHBoxLayout()
        buttons.setSpacing(SPACING["sm"])
        self._later_button = QPushButton()
        self._later_button.setProperty("variant", "ghost")
        self._later_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._later_button.clicked.connect(self.reject)
        buttons.addWidget(self._later_button)
        buttons.addStretch(1)

        self._open_button = QPushButton()
        self._open_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._open_button.clicked.connect(self._open_page)
        buttons.addWidget(self._open_button)

        # Güncelleme yalnızca paketlenmiş, yeri yeten bir kurulumda ve
        # sürümde kurulum programı varken öneriliyor. Olmuyorsa düğme hiç
        # görünmüyor ve sebebi ekranda yazıyor — basılıp hiçbir şey
        # olmayan bir düğme, olmayan düğmeden kötü.
        # Bu sürümün yaması varsa yalnızca değişen dosyalar iniyor (0.9.1+).
        self._asset = updater.pick_update(info.assets, info.version)
        self._can_update, self._blocker = updater.can_update()
        if self._asset is None and self._can_update:
            self._can_update, self._blocker = False, "asset"

        self._update_button = QPushButton()
        self._update_button.setProperty("variant", "primary")
        self._update_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._update_button.clicked.connect(self._start_update)
        self._update_button.setVisible(self._can_update)
        buttons.addWidget(self._update_button)
        layout.addLayout(buttons)

        (self._update_button if self._can_update else self._open_button).setDefault(True)
        if not self._can_update:
            self._open_button.setProperty("variant", "primary")

        self.setFixedWidth(WIDTH)
        self.retranslate()
        modal.freeze(self)

    def _start_update(self) -> None:
        """İndirme penceresini açar; kutu kapanıyor, indirme orada sürüyor."""
        from ..widgets.effects import theme_mode
        from . import titlebar
        from .update_window import UpdateWindow

        sahip = self.parent()
        pencere = UpdateWindow(self._language, self._info, self._asset)
        if sahip is not None:
            # Referans tutuluyor (yoksa pencere hemen siliniyor); ana pencere
            # kapanırken onu da kapatıyor.
            sahip._update_window = pencere
        pencere.ready.connect(lambda yol: install(yol, pencere, sahip))
        self.accept()
        pencere.start()
        titlebar.apply(pencere, theme_mode())

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
        self._howto.setText(
            t("update.notice_howto") if self._can_update
            else t(f"update.blocked_{self._blocker}")
        )
        self._later_button.setText(t("update.notice_later"))
        self._open_button.setText(t("update.notice_open"))
        self._update_button.setText(t("update.notice_update"))


def install(path, window, owner) -> None:
    """Kurulum programını başlatıp uygulamayı kapatır.

    Kurulum programı bu sürecin kapanmasını bekliyor. Ana pencere onay
    sormadan kapanıyor: çıkış onayı güncelleme penceresinin arkasında kalıp
    güncellemeyi bekletiyordu.
    """
    if not updater.start_installer(path):
        window.show_error("start")
        return
    window.release()
    if owner is not None and hasattr(owner, "close_for_update"):
        owner.close_for_update()
    else:
        QApplication.quit()
