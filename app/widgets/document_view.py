"""Belge alanlarını çizen görünüm.

Qt'nin kendi metin motoru CSS'in çok küçük bir alt kümesini destekliyor:
yuvarlak köşe, gölge, yapışkan konumlandırma ve kod renklendirmesi yok. Bu
yüzden ders metinleri Chromium tabanlı `QWebEngineView` ile çiziliyor;
böylece maketteki stil dosyası birebir çalışıyor.

Sayfa içindeki bağlantılar `app:` ile başlıyor ve dışarı çıkmıyor; tıklanınca
`action` sinyali yayılıyor. Böylece "sonraki bölüm" gibi düğmeler HTML'in
içinde durabiliyor ama işi uygulama yapıyor.

`http`/`https` bağlantıları uygulamanın içinde açılmıyor; sistem
tarayıcısına devrediliyor. Ders metinlerinde indirme ve belge adresleri
geçiyor, bunların çalışması gerekiyor.
"""

from __future__ import annotations

from pathlib import Path

import json

from PySide6.QtCore import QTimer, QUrl, Signal
from PySide6.QtGui import QColor, QDesktopServices
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

        # Dış bağlantı: uygulamanın içinde açılmıyor, **sistem tarayıcısına**
        # veriliyor. Eskiden sessizce yok sayılıyordu; kurulum dersindeki
        # indirme bağlantılarına tıklayan kişi hiçbir şey olmadığını
        # görüyordu. Uygulama isteği kendisi yapmıyor, yalnızca adresi
        # tarayıcıya devrediyor.
        if url.scheme() in ("http", "https"):
            QDesktopServices.openUrl(url)
            return False

        # Sayfa içi çapa (başlık listesi) ve yerel kaynaklar serbest.
        # Şema kontrolü önce geliyor: `hasFragment()` başa konduğunda
        # `https://.../a#b` gibi bir adres uygulamanın içinde açılıyordu.
        return url.scheme() in ("", "data", "file", "qrc")

    def javaScriptConsoleMessage(self, *args) -> None:  # noqa: N802
        # Sayfanın konsol çıktısı terminale karışmasın.
        pass


class DocumentView(QWebEngineView):
    """Markdown'dan üretilmiş HTML'i gösterir."""

    action = Signal(str)
    # Sağ tıkta "Nota ekle": seçili metin.
    quote_requested = Signal(str)

    def __init__(self, parent: QWidget | None = None, mode: str = "light") -> None:
        super().__init__(parent)
        self._mode = mode
        self._rendered_mode = mode
        self._body = ""
        # Sayfa yüklendi mi; yüklenirken istenen kaydırma burada bekliyor.
        self._loaded = False
        self._pending_anchor = ""
        # (Nota ekle, Kopyala) etiketleri. Verilmemişse Chromium'un kendi
        # sağ tık menüsü çıkıyor.
        self._quote_labels: tuple[str, str] | None = None

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
        # Sayfanın hangi temanın stiliyle çizildiği; yükleme bitince
        # bakılıyor (`_on_load_finished`).
        self._rendered_mode = self._mode
        self._loaded = False
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
        # Tema, sayfa yüklenirken değiştiyse stil değişimi yüklenmekte olan
        # sayfaya değil eskisine uygulanmış oluyor; yeni sayfa çizildiği
        # anın temasıyla açılıp orada kalıyordu (Notlarım'da, not yüklenir
        # yüklenmez tema bildirildiğinde görüldü). Yükleme bitince fark
        # varsa stil yeniden veriliyor.
        if ok and self._rendered_mode != self._mode:
            self._rendered_mode = self._mode
            self._swap_css()
        if ok and self._restore_to:
            self.page().runJavaScript(
                "(document.scrollingElement||document.documentElement)"
                f".scrollTop = {self._restore_to};"
            )
        self._restore_to = 0
        # Yarıda kesilen yükleme (hemen arkasından yeni bir çizim) de bu
        # sinyali `ok=False` ile veriyor; bekleyen kaydırma son yüklemeye.
        if ok:
            self._loaded = True
            if self._pending_anchor:
                anchor, self._pending_anchor = self._pending_anchor, ""
                self._scroll_now(anchor)

    # Sayfadaki göreli adreslerin (resim, dosya) çözüleceği klasör.
    # Varsayılan içerik kökü; bir bölüm kendi klasörünü verdiğinde
    # `assets/adim-1.png` gibi kısa yollar yazılabiliyor.
    _base_override: Path | None = None

    def set_base_dir(self, directory: "Path | None") -> None:
        """Göreli adreslerin çözüleceği klasörü değiştirir.

        Ders metni bir bölümün klasöründen geliyor; resimleri de orada
        duruyor. Taban içerik kökünde kalırsa yazarın her resmi
        `03-sql/00-kurulum/assets/...` diye yazması gerekiyordu.
        """
        self._base_override = directory

    def _base_path(self) -> str:
        from ..paths import content_dir

        taban = self._base_override or content_dir()
        return f"{taban}/"

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
        self._swap_css()

    def _swap_css(self) -> None:
        """Sayfanın stil bloğunu seçili temanınkiyle değiştirir."""
        self.page().runJavaScript(
            "(function () {"
            "  var s = document.getElementById('tema');"
            "  if (!s) return false;"
            f"  s.textContent = {json.dumps(build_css(self._mode))};"
            "  return true;"
            "})()"
        )

    def enable_quote(self, add_label: str, copy_label: str) -> None:
        """Sağ tıkta seçimi nota ekleyen menüyü açar; etiketler dilde.

        Chromium'un kendi menüsü (Geri, Yeniden yükle, Kaynağı gör...) bu
        belgelerde bir işe yaramıyor. Menü yalnızca bir şey seçiliyken
        çıkıyor: seçimsiz sağ tıkta sunulacak bir iş yok.
        """
        self._quote_labels = (add_label, copy_label)

    def contextMenuEvent(self, event) -> None:  # noqa: N802
        if self._quote_labels is None:
            super().contextMenuEvent(event)
            return

        event.accept()
        secim = self.selectedText().strip()
        if not secim:
            return

        from PySide6.QtWidgets import QMenu

        # Eylemler kendi sinyalleriyle bağlanıyor; `exec`'in döndürdüğü
        # eylemi kimliğiyle karşılaştırmaya güvenilmiyor.
        add_label, copy_label = self._quote_labels
        menu = QMenu(self)
        menu.addAction(copy_label).triggered.connect(
            lambda: self.page().triggerAction(QWebEnginePage.WebAction.Copy)
        )
        menu.addAction(add_label).triggered.connect(lambda: self.quote_requested.emit(secim))
        menu.exec(event.globalPos())

    def scroll_to(self, anchor: str) -> None:
        """Sayfayı belirtilen çapaya kaydırır.

        Sayfa henüz yükleniyorsa (arama sonucundan bölüm yeni açıldıysa)
        kaydırma yükleme bitince yapılıyor; hemen çalıştırılan betik
        yüklenmekte olan sayfaya değil eskisine gidiyordu.
        """
        if not self._loaded:
            self._pending_anchor = anchor
            return
        self._scroll_now(anchor)

    def _scroll_now(self, anchor: str) -> None:
        self.page().runJavaScript(
            f"document.getElementById({json.dumps(anchor)})?.scrollIntoView({{block:'start'}});"
        )
