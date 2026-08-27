"""Ders metnini gösteren görünüm.

Sayfanın tamamı (metin, başlık listesi, alt gezinme) tek bir HTML belgesi
olarak üretilip `DocumentView` ile çiziliyor. Böylece maketteki düzen birebir
çalışıyor: metin ortada sınırlı genişlikte, başlık listesi sağda ve sayfa
kayarken yerinde kalıyor.

Ders seçili dilde yoksa Türkçesi gösterilir ve üstte bunu belirten bir şerit
çıkar. Bu bir hata değil; içerik önce Türkçe yazılıyor.
"""

from __future__ import annotations

import html
from pathlib import Path

import markdown

from PySide6.QtCore import QTimer, Signal
from PySide6.QtWidgets import QVBoxLayout, QWidget

from ..core.language import LanguageManager
from ..widgets.document_view import DocumentView

MARKDOWN_EXTENSIONS = ["fenced_code", "tables", "sane_lists", "toc"]

# Sayfa kayarken hangi başlıkta olduğumuzu işaretleyen küçük script.
SCROLL_SPY = """
<script>
(function () {
  const links = [...document.querySelectorAll('.toc-inner a[href^="#"]')];
  if (!links.length) return;
  const targets = links
      .map(a => document.getElementById(a.getAttribute('href').slice(1)))
      .filter(Boolean);
  const spy = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      links.forEach(a => a.classList.remove('on'));
      const hit = links.find(a => a.getAttribute('href') === '#' + entry.target.id);
      if (hit) hit.classList.add('on');
    });
  }, { rootMargin: '0px 0px -70% 0px', threshold: 0 });
  targets.forEach(t => spy.observe(t));
})();
</script>
"""

# Dersin sonuna gelindiğinde bir kez haber verir. Bölümü açmak okumak
# sayılmıyor; kullanıcı metnin sonuna inince "okundu" işaretleniyor.
# Sayfanın sonuna inilip inilmediğini soran ölçüm. Python tarafından
# aralıklarla çalıştırılıyor; sayfanın kendisi haber veremiyor, çünkü
# Chromium kullanıcı tıklaması olmadan `app:` adresine gitmeyi engelliyor —
# sayfa içine konan bir betiğin `location.href` ataması sessizce düşüyor.
#
# `document.scrollingElement` kaydırmayı hangi öğe yapıyorsa onu veriyor;
# `body` üzerinden hesaplamak her düzende doğru sonuç vermiyor.
# `clientHeight > 0` şartı, daha çizilmemiş sayfanın "okundu" sayılmasını
# engelliyor. Sayfa ekrana sığıyorsa (kaydırma yoksa) okunmuş sayılıyor.
READ_PROBE = """
(function () {
  var el = document.scrollingElement || document.documentElement;
  if (!el || el.clientHeight <= 0) return false;
  return (el.scrollHeight - el.scrollTop - el.clientHeight) <= 80;
})()
"""

# Ölçümün sıklığı. Okundu işareti konunca zamanlayıcı duruyor.
READ_POLL_MS = 1000


def render_markdown(text: str) -> tuple[str, list[tuple[str, str]]]:
    """Markdown'ı HTML'e çevirir ve ikinci seviye başlıkları döndürür.

    Başlıklar sağdaki listede kullanılıyor; `toc` uzantısı başlıklara
    kendiliğinden `id` verdiği için çapalar çalışıyor.
    """
    converter = markdown.Markdown(extensions=MARKDOWN_EXTENSIONS)
    body = converter.convert(text)

    headings = [
        (token["id"], token["name"])
        for token in getattr(converter, "toc_tokens", [])
        for token in [token, *token.get("children", [])]
        if token["level"] == 2
    ]
    return body, headings


class LessonView(QWidget):
    """Bir dersin metnini gösterir."""

    # Alt gezinme düğmelerine basıldığında yayılır ("next", "previous"...).
    action = Signal(str)

    def __init__(
        self,
        language: LanguageManager,
        parent: QWidget | None = None,
        compact: bool = False,
        show_toc: bool = True,
        track_reading: bool = False,
    ) -> None:
        """`compact`, dar bir panelde (alıştırma yönergesi gibi) kullanılır.

        `track_reading` açıkken, kullanıcı metnin sonuna indiğinde
        `action` sinyaliyle `lesson-read` bildirilir.
        """
        super().__init__(parent)
        self._language = language
        self._compact = compact
        self._show_toc = show_toc and not compact
        self._track_reading = track_reading

        self._source = ""
        self._meta: list[str] = []
        self._banners: list[tuple[str, str]] = []
        self._footer: list[tuple[str, str, bool]] = []
        self._extra = ""
        self._progress = (0, "")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self._document = DocumentView(self)
        self._document.action.connect(self.action)
        layout.addWidget(self._document)

        # Okuma takibi: sayfaya sorup sonuna inilmiş mi diye bakıyoruz.
        self._read_reported = False
        self._read_timer = QTimer(self)
        self._read_timer.setInterval(READ_POLL_MS)
        self._read_timer.timeout.connect(self._probe_reading)

    # --- içerik -----------------------------------------------------------

    def show_lesson(
        self,
        path: Path | None,
        is_fallback: bool = False,
        completed: bool = False,
    ) -> None:
        """Ders dosyasını yükler."""
        if path is None or not path.exists():
            self._source = f"*{self._language.t('content.not_found', path=path or '-')}*"
        else:
            self._source = path.read_text(encoding="utf-8")

        self._banners = []
        if completed:
            self._banners.append(("ok", self._language.t("section.completed_banner")))
        if is_fallback:
            self._banners.append(("warn", self._language.t("content.translation_missing")))

        # Yeni ders: okuma takibi baştan başlıyor.
        self._read_reported = False
        self._render()

    def _probe_reading(self) -> None:
        """Sayfaya "metnin sonuna inildi mi" diye sorar."""
        if self._read_reported:
            self._read_timer.stop()
            return
        # Ders sekmesi görünmüyorken ölçüm anlamsız; kullanıcı sınavdayken
        # dersi okunmuş saymak yanlış olurdu.
        if not self.isVisible():
            return
        self._document.page().runJavaScript(READ_PROBE, self._on_read_probe)

    def _on_read_probe(self, reached: object) -> None:
        if self._read_reported or not reached:
            return
        self._read_reported = True
        self._read_timer.stop()
        self.action.emit("lesson-read")

    def show_text(self, text: str) -> None:
        """Hazır markdown metnini gösterir (alıştırma yönergesi gibi)."""
        self._source = text
        self._banners = []
        self._render()

    def set_meta(self, items: list[str]) -> None:
        """Başlığın altındaki bilgi satırı: süre, alıştırma ve sınav sayısı."""
        self._meta = [item for item in items if item]
        if self._source:
            self._render()

    def set_progress(self, percent: int, caption: str) -> None:
        self._progress = (percent, caption)
        if self._source:
            self._render()

    def set_footer(self, buttons: list[tuple[str, str, bool]]) -> None:
        """Alt gezinme düğmeleri: (eylem, metin, birincil mi)."""
        self._footer = buttons
        if self._source:
            self._render()

    def set_extra(self, html_after: str) -> None:
        """Metnin altına eklenecek hazır HTML (alıştırma ipucu kutusu gibi)."""
        self._extra = html_after
        if self._source:
            self._render()

    # --- çizim ------------------------------------------------------------

    def _render(self) -> None:
        body, headings = render_markdown(self._source)

        parts = ["".join(self._banner_html(tone, text) for tone, text in self._banners)]
        parts.append(self._meta_html(body))
        parts.append(self._extra)
        parts.append(self._footer_html())
        content = f'<div class="content">{"".join(parts)}</div>'

        if self._compact:
            page_class = "page compact"
            aside = ""
        elif self._show_toc:
            page_class = "page"
            aside = self._toc_html(headings)
        else:
            page_class = "page narrow"
            aside = ""

        scripts = SCROLL_SPY if aside else ""
        self._document.set_body(
            f'<div class="{page_class}">{content}{aside}</div>{scripts}'
        )
        if self._track_reading and not self._read_reported:
            self._read_timer.start()

    def _banner_html(self, tone: str, text: str) -> str:
        icon = "✓" if tone == "ok" else "!"
        return (
            f'<div class="banner {tone}"><span>{icon}</span>'
            f"<span>{html.escape(text)}</span></div>"
        )

    def _meta_html(self, body: str) -> str:
        """Bilgi satırını ilk başlığın hemen altına yerleştirir."""
        if not self._meta:
            return body

        row = '<div class="meta">' + "".join(
            f"<span>{html.escape(item)}</span>" for item in self._meta
        ) + "</div>"

        closing = body.find("</h1>")
        if closing == -1:
            return row + body
        cut = closing + len("</h1>")
        return body[:cut] + row + body[cut:]

    def _toc_html(self, headings: list[tuple[str, str]]) -> str:
        if not headings:
            return ""

        links = "".join(
            f'<a href="#{anchor}"{" class=\'on\'" if index == 0 else ""}>'
            f"{html.escape(title)}</a>"
            for index, (anchor, title) in enumerate(headings)
        )

        percent, caption = self._progress
        progress = (
            '<div class="prog">'
            f'<div class="h2">{html.escape(self._language.t("section.section_progress"))}</div>'
            f'<div class="bar"><i style="width:{percent}%"></i></div>'
            f'<div class="h2" style="margin:9px 0 0">{html.escape(caption)}</div>'
            "</div>"
        )

        return (
            '<aside class="toc"><div class="toc-inner">'
            f'<div class="h">{html.escape(self._language.t("section.on_this_page"))}</div>'
            f"{links}{progress}</div></aside>"
        )

    def _footer_html(self) -> str:
        """Alt gezinme düğmeleri.

        Gidilecek yeri olmayan düğme hiç çizilmiyor. Soluk ama tıklanamaz bir
        düğme bırakmak kullanıcıyı boşuna uğraştırıyor; son nottayken
        "Sonraki not" görünmemeli.
        """
        available = [(a, label, primary) for a, label, primary in self._footer if a]
        if not available:
            return ""

        buttons = []
        for index, (action, label, primary) in enumerate(available):
            classes = ["pri"] if primary else []
            # Sağa yaslama: birden fazla düğme varsa sonuncusu, tek düğme
            # varsa yalnızca birincil olan sağa gider.
            if (index == len(available) - 1 and len(available) > 1) or (
                len(available) == 1 and primary
            ):
                classes.append("sp")

            attribute = f' class="{" ".join(classes)}"' if classes else ""
            buttons.append(
                f'<a href="app:{action}"{attribute}>{html.escape(label)}</a>'
            )

        return f'<div class="foot">{"".join(buttons)}</div>'

    # --- tema ve dil ------------------------------------------------------

    def set_mode(self, mode: str) -> None:
        self._document.set_mode(mode)

    def retranslate(self) -> None:
        if self._source:
            self._render()
