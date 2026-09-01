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

import json

from PySide6.QtCore import QTimer, QUrl, Signal
from PySide6.QtGui import QColor
from PySide6.QtWebEngineCore import QWebEnginePage, QWebEngineSettings
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QWidget

from ..core.highlight import highlight_code_blocks
from ..resources.theme.document import build_css
from ..resources.theme.tokens import PALETTES

ACTION_SCHEME = "app"


# Kaydırma konumunun ne sıklıkla sorulacağı. Yeniden çizim anında en fazla
# bu kadarlık bir kayma olabiliyor; gözle fark edilmiyor.
SCROLL_POLL_MS = 250


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

        # Belgenin dili. Tarayıcı `text-transform: uppercase` uygularken
        # dilin kuralını kullanıyor: `lang` verilmezse Türkçe `i` harfi `I`
        # oluyor ve sürüm notlarında "EKLENDI" yazıyordu.
        self._lang = "tr"

        # Kaydırma konumu: yeniden çizimde okuyanın yerini korumak için.
        self._scroll = 0.0
        self._restore_to = 0.0
        self.loadFinished.connect(self._on_load_finished)

        self._scroll_timer = QTimer(self)
        self._scroll_timer.setInterval(SCROLL_POLL_MS)
        self._scroll_timer.timeout.connect(self._remember_scroll)
        self._scroll_timer.start()

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

    def set_body(self, body_html: str, keep_scroll: bool = False) -> None:
        """Gövde HTML'ini alır, stil ve renklendirmeyle birlikte gösterir.

        `keep_scroll` **aynı belgenin** yeniden çizildiği durumlar için:
        ilerleme kutusu güncellendiğinde ya da bir ipucu açıldığında sayfa
        baştan yükleniyor ve okuyan kişi en başa fırlıyordu. Yeni bir belge
        gösterilirken bayrak verilmiyor, sayfa doğal olarak başa dönüyor.
        """
        self._body = body_html
        self._render(keep_scroll=keep_scroll)

    def _render(self, keep_scroll: bool = False) -> None:
        painted = highlight_code_blocks(self._body, self._mode)
        document = (
            f"<!doctype html><html lang='{self._lang}'>"
            "<head><meta charset='utf-8'>"
            f"<style id='tema'>{build_css(self._mode)}</style></head>"
            f"<body>{painted}</body></html>"
        )
        if keep_scroll:
            self._restore_to = self._scroll
        else:
            # Yeni bir belge: saklanan konum da sıfırlanıyor. Yalnızca
            # `_restore_to` sıfırlanırsa, hemen arkasından gelen bir
            # `keep_scroll=True` çizimi (ilerleme kutusu, alt düğmeler,
            # bilgi satırı) eski belgenin konumunu geri yüklüyor ve yeni
            # ders, bir öncekinin kaldığı yerden açılıyordu.
            self._restore_to = 0
            self._scroll = 0.0

        # Yerel görsellerin (içerik klasöründeki png'ler) çözülebilmesi için
        # taban adres veriliyor.
        self.setHtml(document, QUrl.fromLocalFile(str(self._base_path())))

    # --- kaydırma konumu --------------------------------------------------

    def _remember_scroll(self) -> None:
        """Sayfanın kaydırma konumunu Python tarafında saklar.

        Sayfa kendiliğinden uygulamaya haber veremediği için (Chromium
        kullanıcı tıklaması olmadan `app:` adresine gitmiyor) konum
        aralıklarla sorulup saklanıyor.
        """
        self.page().runJavaScript(
            "(document.scrollingElement||document.documentElement).scrollTop",
            self._store_scroll,
        )

    def _store_scroll(self, value) -> None:
        try:
            self._scroll = float(value or 0)
        except (TypeError, ValueError):
            pass

    def _on_load_finished(self, ok: bool) -> None:
        if ok and self._restore_to:
            self.page().runJavaScript(
                "(document.scrollingElement||document.documentElement)"
                f".scrollTop = {self._restore_to};"
            )
        self._restore_to = 0

    def _base_path(self) -> str:
        from ..paths import content_dir

        return f"{content_dir()}/"

    def set_lang(self, code: str) -> None:
        """Belgenin dilini bildirir; büyük harf dönüşümü buna bakıyor."""
        if code != self._lang:
            self._lang = code
            if self._body:
                self._render(keep_scroll=True)

    def set_mode(self, mode: str) -> None:
        """Temayı değiştirir.

        Belge **yeniden yüklenmiyor**: yalnızca stil bloğunun içeriği
        değiştiriliyor. Kod renkleri de sınıfla verildiği için tek bir stil
        değişimi her şeyi kapsıyor.

        Önceden belge baştan yükleniyordu ve renk gecikmeli değişiyordu —
        ölçüldü: tema anahtarına basıldıktan ~190 ms sonra içerik alanı
        rengini alıyordu. Şimdi aynı karede değişiyor.
        """
        if mode == self._mode:
            return

        self._mode = mode
        self._apply_background()
        if not self._body:
            return

        self.page().runJavaScript(
            "(function () {"
            "  var s = document.getElementById('tema');"
            "  if (!s) return false;"
            f"  s.textContent = {json.dumps(build_css(mode))};"
            "  return true;"
            "})()"
        )

    def scroll_to(self, anchor: str) -> None:
        """Sayfayı belirtilen çapaya kaydırır."""
        self.page().runJavaScript(
            f"document.getElementById({anchor!r})?.scrollIntoView({{behavior:'smooth'}});"
        )
