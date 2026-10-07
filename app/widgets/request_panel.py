"""API 2: kişinin yazdığı API'ye istek gönderen küçük panel.

Alıştırmanın sol tarafında "İstek" sekmesi. Yöntem, adres ve (gerekiyorsa)
JSON gövde yazılıyor; istek kodun **şu anki** hâline gidiyor. Sunucu
açılmıyor: denetleyici uygulamayı süreç içinde çağırıyor
(`fastapi_sandbox.check_http`, `capture` adımı). Kayıt yok, deneme sayılmıyor.
"""

from __future__ import annotations

import json

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget

from ..core.language import LanguageManager
from ..resources.theme.tokens import PALETTES, SPACING
from .code_editor import CodeEditor
from .common import DropdownBox
from .effects import repolish

METHODS = ("GET", "POST", "PUT", "PATCH", "DELETE")
# Gövde yalnızca bunlarda gönderiliyor.
BODY_METHODS = {"POST", "PUT", "PATCH"}


class RequestPanel(QWidget):
    """Yöntem + adres + gövde → durum kodu ve yanıt."""

    send_requested = Signal(str, str, object)  # yöntem, adres, gövde (dict/list ya da None)

    def __init__(self, language: LanguageManager, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._language = language
        self._mode = "light"
        self.setProperty("role", "bare")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(SPACING["lg"], SPACING["md"], SPACING["lg"], SPACING["md"])
        layout.setSpacing(SPACING["sm"])

        self._intro = QLabel()
        self._intro.setProperty("role", "muted")
        self._intro.setWordWrap(True)
        layout.addWidget(self._intro)

        satir = QHBoxLayout()
        satir.setSpacing(SPACING["sm"])
        self._method = DropdownBox()
        self._method.addItems(METHODS)
        self._method.setFixedWidth(104)
        self._method.currentTextChanged.connect(self._sync_body)
        satir.addWidget(self._method)
        self._path = QLineEdit("/")
        self._path.returnPressed.connect(self._send)
        satir.addWidget(self._path, 1)
        self._send_button = QPushButton()
        self._send_button.setProperty("variant", "primary")
        self._send_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._send_button.clicked.connect(self._send)
        satir.addWidget(self._send_button)
        layout.addLayout(satir)

        self._body_title = QLabel()
        self._body_title.setProperty("role", "section")
        layout.addWidget(self._body_title)
        self._body = CodeEditor()
        self._body.set_language("json")
        self._body.setFixedHeight(120)
        layout.addWidget(self._body)

        cevap = QHBoxLayout()
        cevap.setSpacing(SPACING["sm"])
        self._response_title = QLabel()
        self._response_title.setProperty("role", "section")
        cevap.addWidget(self._response_title)
        self._status = QLabel()
        self._status.setProperty("role", "chip")
        self._status.hide()
        cevap.addWidget(self._status)
        cevap.addStretch(1)
        layout.addLayout(cevap)

        self._message = QLabel()
        self._message.setWordWrap(True)
        self._message.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self._message.hide()
        layout.addWidget(self._message)
        self._response = CodeEditor()
        self._response.set_language("json")
        self._response.setReadOnly(True)
        layout.addWidget(self._response, 1)

        self._sync_body()
        self.retranslate()

    # --- dış ----------------------------------------------------------------

    def reset(self, path: str = "/") -> None:
        """Yeni alıştırmada boş başlar."""
        self._method.setCurrentText("GET")
        self._path.setText(path or "/")
        self._body.setPlainText("")
        self._response.setPlainText("")
        self._status.hide()
        self._message.hide()
        self.set_busy(False)

    def set_busy(self, busy: bool) -> None:
        self._send_button.setEnabled(not busy)
        self._send_button.setText(self._language.t("request.sending" if busy else "request.send"))

    def show_response(self, status: int, body: str) -> None:
        self.set_busy(False)
        self._message.hide()
        ton = "success" if status < 300 else "warning" if status < 500 else "danger"
        self._status.setText(str(status))
        self._status.setProperty("tone", ton)
        repolish(self._status)
        self._status.show()
        self._response.setPlainText(body)

    def show_error(self, message: str) -> None:
        """İstek gönderilemedi ya da uygulama açılmadı: neden bu satırda."""
        self.set_busy(False)
        self._status.setText("!")
        self._status.setProperty("tone", "danger")
        repolish(self._status)
        self._status.show()
        self._message.setText(message)
        self._message.setProperty("tone", "danger")
        repolish(self._message)
        self._message.show()
        self._response.setPlainText("")

    def set_mode(self, mode: str) -> None:
        self._mode = mode
        p = PALETTES.get(mode, PALETTES["dark"])
        self._method.set_arrow_color(p["text_muted"])
        self._body.set_mode(mode)
        self._response.set_mode(mode)

    def retranslate(self) -> None:
        t = self._language.t
        self._intro.setText(t("request.intro"))
        self._path.setPlaceholderText(t("request.path_placeholder"))
        self._body_title.setText(t("request.body").upper())
        self._response_title.setText(t("request.response").upper())
        self._send_button.setText(t("request.send"))
        self._sync_body()

    # --- iç -----------------------------------------------------------------

    def _sync_body(self, *_args) -> None:
        govdeli = self._method.currentText() in BODY_METHODS
        self._body.setEnabled(govdeli)
        self._body.setPlaceholderText(
            self._language.t("request.body_placeholder" if govdeli else "request.body_none"))

    def _send(self) -> None:
        method = self._method.currentText()
        path = self._path.text().strip() or "/"
        if not path.startswith("/"):
            path = "/" + path
            self._path.setText(path)
        body = None
        if method in BODY_METHODS and self._body.toPlainText().strip():
            try:
                body = json.loads(self._body.toPlainText())
            except ValueError as exc:
                self.show_error(self._language.t("request.bad_json", error=str(exc)))
                return
        self.set_busy(True)
        self.send_requested.emit(method, path, body)
