"""Belge alanlarını çizen görünüm.

Qt'nin kendi metin motoru CSS'in çok küçük bir alt kümesini destekliyor:
yuvarlak köşe, gölge, yapışkan konumlandırma ve kod renklendirmesi yok. Bu
yüzden ders metinleri Chromium tabanlı `QWebEngineView` ile çiziliyor;
böylece maketteki stil dosyası birebir çalışıyor.

Sayfa içindeki bağlantılar `app:` ile başlıyor ve dışarı çıkmıyor; tıklanınca
`action` sinyali yayılıyor. Böylece "sonraki bölüm" gibi düğmeler HTML'in
içinde durabiliyor ama işi uygulama yapıyor.
"""

from __future__ import annotations

from PySide6.QtCore import QUrl, Signal
from PySide6.QtGui import QColor
from PySide6.QtWebEngineCore import QWebEnginePage, QWebEngineSettings
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QWidget

from ..core.highlight import highlight_code_blocks
from ..resources.theme.document import build_css
from ..resources.theme.tokens import PALETTES

ACTION_SCHEME = "app"


class DocumentPage(QWebEnginePage):
    """Sayfa içi bağlantıları uygulamaya yönlendirir."""

    action = Signal(str)

    def acceptNavigationRequest(  # noqa: N802 (Qt adlandırması)
        self, url: QUrl, kind: QWebEnginePage.NavigationType, is_main_frame: bool
    ) -> bool:
        if url.scheme() == ACTION_SCHEME:
            self.action.emit(url.path() or url.toString()[len(ACTION_SCHEME) + 1:])
            return False

        # Sayfa içi çapa (başlık listesi) serbest; dış bağlantılar engelli.
        if url.scheme() in ("", "data", "file", "qrc") or url.hasFragment():
            return True

        return False

    def javaScriptConsoleMessage(self, *args) -> None:  # noqa: N802
        # Sayfanın konsol çıktısı terminale karışmasın.
        pass


class DocumentView(QWebEngineView):
    """Markdown'dan üretilmiş HTML'i gösterir."""

    action = Signal(str)

    def __init__(self, parent: QWidget | None = None, mode: str = "light") -> None:
        super().__init__(parent)
        self._mode = mode
        self._body = ""

        self._page = DocumentPage(self)
        self._page.action.connect(self.action)
        self.setPage(self._page)

        settings = self.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.ShowScrollBars, True)
        # Sağ tık menüsü uygulamanın içinde yabancı duruyor.
        settings.setAttribute(QWebEngineSettings.WebAttribute.FocusOnNavigationEnabled, False)

        self._apply_background()

    def _apply_background(self) -> None:
        palette = PALETTES.get(self._mode, PALETTES["light"])
        self._page.setBackgroundColor(QColor(palette["bg"]))

    def set_body(self, body_html: str) -> None:
        """Gövde HTML'ini alır, stil ve renklendirmeyle birlikte gösterir."""
        self._body = body_html
        self._render()

    def _render(self) -> None:
        painted = highlight_code_blocks(self._body, self._mode)
        document = (
            "<!doctype html><html><head><meta charset='utf-8'>"
            f"<style>{build_css(self._mode)}</style></head>"
            f"<body>{painted}</body></html>"
        )
        # Yerel görsellerin (içerik klasöründeki png'ler) çözülebilmesi için
        # taban adres veriliyor.
        self.setHtml(document, QUrl.fromLocalFile(str(self._base_path())))

    def _base_path(self) -> str:
        from ..paths import content_dir

        return f"{content_dir()}/"

    def set_mode(self, mode: str) -> None:
        self._mode = mode
        self._apply_background()
        if self._body:
            self._render()

    def scroll_to(self, anchor: str) -> None:
        """Sayfayı belirtilen çapaya kaydırır."""
        self.page().runJavaScript(
            f"document.getElementById({anchor!r})?.scrollIntoView({{behavior:'smooth'}});"
        )
