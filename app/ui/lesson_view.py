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
import json
from pathlib import Path

import markdown

from PySide6.QtCore import QTimer, Signal
from PySide6.QtWidgets import QVBoxLayout, QWidget

from ..core import math_text
from ..core.language import LanguageManager
from ..widgets.document_view import DocumentView

MARKDOWN_EXTENSIONS = ["fenced_code", "tables", "sane_lists", "toc"]

# Metnin altındaki hazır HTML'in (ipucu kutusu) kapsayıcısı; yerinde
# değiştirilirken bu kimlikle bulunuyor.
EXTRA_ID = "extra"

# Sayfa kayarken hangi başlıkta olduğumuzu işaretleyen küçük script.
#
# Önce `IntersectionObserver` kullanılıyordu ve iki hatası vardı:
#
# 1. `rootMargin` ekranın alt %70'ini kesiyordu, yani yalnızca üst şeritteki
#    başlıklar sayılıyordu. Sayfanın sonuna inildiğinde son başlık (genelde
#    "Özet") o şeride hiç çıkamıyor — sayfa daha fazla kaymıyor — ve işaret
#    ona hiç gelmiyordu.
# 2. Tek bir çağrıda birden fazla başlık bildirilebiliyor ve döngüde **en
#    son işlenen** kazanıyordu; sırası önemsendiği için işaret yukarı
#    fırlıyordu.
#
# Yerine doğrudan konum hesabı kondu: **çizginin üstünde kalan son başlık**
# hangisiyse o işaretleniyor. Sayfanın en dibindeyken son başlık seçiliyor,
# çünkü orada "aşağıda daha fazlası var" diye bir şey yok.
SCROLL_SPY = """
<script>
(function () {
  const links = [...document.querySelectorAll('.toc-inner a[href^="#"]')];
  if (!links.length) return;

  const targets = links.map(
      a => document.getElementById(a.getAttribute('href').slice(1)));

  // Başlığın "geçildi" sayılması için ekranın üstünden kaç piksel yukarıda
  // olması gerektiği. Sıfır olsaydı, başlık ekranın tam tepesindeyken
  // işaret bir önceki başlıkta kalıyordu.
  const LINE = 120;

  function update() {
    const el = document.scrollingElement || document.documentElement;
    const atBottom = el.scrollHeight - el.scrollTop - el.clientHeight <= 4;

    let current = 0;
    if (atBottom) {
      current = links.length - 1;
    } else {
      for (let i = 0; i < targets.length; i++) {
        const node = targets[i];
        if (node && node.getBoundingClientRect().top <= LINE) current = i;
      }
    }

    links.forEach((a, i) => a.classList.toggle('on', i === current));
    // Kenardaki işaret seçili başlığa yayla kayıyor (ui-taslak C5).
    const mark = document.querySelector('.toc-mark');
    const on = links[current];
    if (mark && on) {
      mark.style.transform = 'translateY(' + on.offsetTop + 'px)';
      mark.style.height = on.offsetHeight + 'px';
    }
  }

  document.addEventListener('scroll', update, { passive: true });
  window.addEventListener('resize', update);
  update();
})();
</script>
"""

# Kod bloklarına "kopyala" düğmesi (ui-taslak C5). Pano erişimi için izin
# istemeyen yol: bloğun metni seçilip `execCommand('copy')`; düğme bir an
# onaya dönüyor. Betik belge içinde çalışıyor, köprüye dokunmuyor.
COPY_BUTTONS = """
<script>
(function () {
  const COPY = '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="8" y="8" width="12" height="12" rx="2.5"/><path d="M16 8V5.5A1.5 1.5 0 0 0 14.5 4h-9A1.5 1.5 0 0 0 4 5.5v9A1.5 1.5 0 0 0 5.5 16H8"/></svg>';
  const OK = '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="m5 12.5 4.5 4.5L19 7.5"/></svg>';
  document.querySelectorAll('.content pre').forEach(function (pre) {
    const b = document.createElement('button');
    b.className = 'cp';
    b.innerHTML = COPY;
    b.addEventListener('click', function (e) {
      e.preventDefault();
      const code = pre.querySelector('code') || pre;
      const r = document.createRange();
      r.selectNodeContents(code);
      const sel = window.getSelection();
      sel.removeAllRanges();
      sel.addRange(r);
      try { document.execCommand('copy'); } catch (err) {}
      sel.removeAllRanges();
      b.innerHTML = OK;
      b.classList.add('done');
      setTimeout(function () { b.innerHTML = COPY; b.classList.remove('done'); }, 1400);
    });
    pre.appendChild(b);
  });
})();
</script>
"""

# İlerleme kutusunu **belgeyi yeniden yüklemeden** güncelleyen betik.
#
# Önce kutu değiştiğinde sayfanın tamamı baştan çiziliyordu. Uzun bir dersi
# okurken kişi metnin sonuna indiği an "okundu" işareti konuyor, o da kutuyu
# güncelliyor ve belge yeniden yükleniyordu. Kaydırma konumu geri
# yükleniyordu ama o konum en fazla dörtte bir saniye eskiydi (Python
# tarafında aralıklarla ölçülüyordu); kullanıcı hâlâ kaydırıyorsa sayfa geri
# sıçrayıp tuhaf bir yerde duruyordu.
#
# Kutunun içindeki iki şeyi doğrudan değiştirmek yeterli: çubuğun genişliği
# ve altındaki yazı. Belge yerinde kalıyor, kaydırmaya hiç dokunulmuyor.
PROGRESS_PATCH = """
(function () {
  var rows = document.querySelectorAll('.prog .step3');
  var steps = %STEPS%;
  if (rows.length !== steps.length) return false;
  steps.forEach(function (s, i) {
    rows[i].classList.toggle('done', s[1]);
    rows[i].querySelector('small').textContent = s[2];
  });
  return true;
})()
"""

# Adımın dairesindeki onay işareti (Lucide `check`).
STEP_CHECK = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"'
    ' stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>'
)


def render_markdown(text: str) -> tuple[str, list[tuple[str, str]]]:
    """Markdown'ı HTML'e çevirir ve ikinci seviye başlıkları döndürür.

    Başlıklar sağdaki listede kullanılıyor; `toc` uzantısı başlıklara
    kendiliğinden `id` verdiği için çapalar çalışıyor.
    """
    # Formüller markdown'dan önce ayrılıyor, yoksa içleri bozuluyor
    # (`app/core/math_text.py`).
    text, formulas = math_text.protect(text)
    converter = markdown.Markdown(extensions=MARKDOWN_EXTENSIONS)
    body = math_text.restore(converter.convert(text), formulas)

    headings = [
        (token["id"], math_text.plain(token["name"], formulas))
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
        self._progress: list[tuple[str, bool, str]] = []

        # İlerleme kutusu şu an çizili mi? Çiziliyse güncelleme belgeyi
        # yeniden yüklemeden yapılıyor.
        self._has_progress_box = False

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self._document = DocumentView(self)
        self._document.action.connect(self.action)
        layout.addWidget(self._document)

        # Okuma takibi: dersin sonuna inilince bir kez `lesson-read`
        # bildiriliyor. Bölümü açmak okumak sayılmıyor.
        self._read_reported = False
        if track_reading:
            self._document.at_end_changed.connect(self._check_read)

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

        # Göreli adresler dersin kendi klasörüne göre çözülüyor: yazar
        # `assets/kurulum-1.png` yazabiliyor, içerik kökünden başlayan uzun
        # yolu tekrarlamıyor.
        self.set_base_dir(path.parent if path is not None else None)

        self._banners = []
        if completed:
            self._banners.append(("ok", self._language.t("section.completed_banner")))
        if is_fallback:
            self._banners.append(("warn", self._language.t("content.translation_missing")))

        # Yeni ders: okuma takibi baştan başlıyor.
        self._read_reported = False
        self._render()

    def reset_reading(self) -> None:
        """`show_text` ile yeni bir belge verilecekse okuma takibi baştan (ders notları)."""
        self._read_reported = False

    def _check_read(self, *_: object) -> None:
        """Metnin sonundaysa ve ders görünüyorsa bir kez "okundu" bildirir.

        Ders sekmesi görünmüyorken bildirim yapılmıyor; kullanıcı
        sınavdayken dersi okunmuş saymak yanlış olurdu. Sekmeye dönüldüğünde
        `showEvent` son durumu yeniden değerlendiriyor.
        """
        if not self._track_reading or self._read_reported:
            return
        if not self.isVisible() or not self._document.at_end:
            return
        self._read_reported = True
        self.action.emit("lesson-read")

    def showEvent(self, event) -> None:  # noqa: N802
        super().showEvent(event)
        self._check_read()

    def set_base_dir(self, directory: "Path | None") -> None:
        """Sayfadaki göreli adreslerin çözüleceği klasörü bildirir.

        `show_lesson` bunu kendisi yapıyor; `show_text` ile hazır metin
        verenlerin (not, alıştırma yönergesi) klasörü ayrıca söylemesi
        gerekiyor.
        """
        self._document.set_base_dir(directory)

    def show_text(self, text: str, extra: str | None = None) -> None:
        """Hazır markdown metnini gösterir (alıştırma yönergesi gibi).

        `extra` metnin altındaki hazır HTML (ipucu kutusu); metinle birlikte
        verilince sayfa **bir kez** çiziliyor. Önce ikisi ayrı çağrılarla
        veriliyordu ve her alıştırma açılışında belge iki kez yükleniyordu.

        Metin öncekiyle aynıysa kaydırma korunuyor.
        """
        ayni = text == self._source
        self._source = text
        if extra is not None:
            self._extra = extra
        self._banners = []
        self._render(keep_scroll=ayni)

    def scroll_to(self, anchor: str) -> None:
        """Başlığın çapasına kaydırır (arama sonucundan gelince)."""
        self._document.scroll_to(anchor)

    def set_meta(self, items: list[str]) -> None:
        """Başlığın altındaki bilgi satırı: süre, alıştırma ve sınav sayısı."""
        yeni = [item for item in items if item]
        if yeni == self._meta:
            return
        self._meta = yeni
        if self._source:
            self._render(keep_scroll=True)

    def set_progress(self, steps: list[tuple[str, bool, str]]) -> None:
        """İlerleme kutusunu günceller: (adım adı, bitti mi, sağdaki sayı).

        Kutu ekrandaysa belge yeniden yüklenmiyor, kutunun içi yerinde
        değiştiriliyor — okurken sayfanın sıçramaması için.
        """
        steps = list(steps)
        if steps == self._progress:
            return

        eski = [ad for ad, _, _ in self._progress]
        self._progress = steps
        if not self._source:
            return

        if self._has_progress_box and eski == [ad for ad, _, _ in steps]:
            self._document.page().runJavaScript(
                PROGRESS_PATCH.replace("%STEPS%", json.dumps(steps))
            )
            return

        self._render(keep_scroll=True)

    def set_footer(self, buttons: list[tuple[str, str, bool]]) -> None:
        """Alt gezinme düğmeleri: (eylem, metin, birincil mi)."""
        if buttons == self._footer:
            return
        self._footer = buttons
        if self._source:
            self._render(keep_scroll=True)

    def update_extra(self, html_after: str) -> None:
        """Metnin altındaki hazır HTML'i **sayfayı yeniden yüklemeden** değiştirir.

        İpucu açılınca önce belgenin tamamı baştan yükleniyordu (üstelik iki
        kez): sayfa bir an en tepede çiziliyor, yükleme bitince eski yerine
        kaydırılıyordu — ekran yukarı gidip geri geliyordu (Alican gördü,
        dört ipuçlu bir alıştırmada). Artık yalnızca kutunun içi değişiyor,
        kaydırmaya dokunulmuyor. Sayfa henüz yüklenmemişse ya da kutu
        bulunamazsa normal çizime düşülüyor.
        """
        if html_after == self._extra:
            return
        self._extra = html_after
        if not self._source:
            return
        self._document.replace_inner(
            EXTRA_ID,
            html_after,
            body=self._compose(),
            fallback=lambda: self._render(keep_scroll=True),
        )

    # --- çizim ------------------------------------------------------------

    def _render(self, keep_scroll: bool = False) -> None:
        """Sayfayı çizer.

        `keep_scroll`, **aynı** belgenin yeniden çizildiği çağrılar için:
        ilerleme kutusu, alt düğmeler ve ipucu kutusu değişince sayfa baştan
        yükleniyor ve okuyan kişi en başa fırlıyordu. Yeni ders yüklenirken
        bayrak verilmiyor, sayfa başa dönüyor.
        """
        # Aynı olay turundaki çizim istekleri tek çizimde birleşiyor. Bir bölüm
        # açılırken içerik, bilgi satırı, alt düğmeler ve dil ayrı ayrı çizim
        # istiyordu: 14 kez markdown çevirisi ve sayfa yüklemesi, 224 ms
        # (ölçüldü, bölüme girerken takılma buydu). Yeni içerik isteyen biri
        # varsa sayfa başa dönüyor.
        bekleyen = getattr(self, "_pending_render", None)
        if bekleyen is not None:
            self._pending_render = bekleyen and keep_scroll
            return
        self._pending_render = keep_scroll
        # Görünen sayfa önce: bölüm açılınca ders notu ve alıştırma
        # sayfaları da çiziliyor ve görünen dersin yüklenmesini
        # geciktiriyordu (ölçüldü: 150–270 ms yerine ~50 ms).
        QTimer.singleShot(0 if self.isVisible() else 250, self, self._flush_render)

    def _flush_render(self) -> None:
        # Elle önceden çizildiyse zamanlayıcı boşa düşer (ikinci yükleme olmasın).
        if getattr(self, "_pending_render", None) is None:
            return
        keep_scroll = bool(self._pending_render)
        self._pending_render = None
        self._document.set_lang(self._language.language)
        self._document.set_body(self._compose(), keep_scroll=keep_scroll)

    def _compose(self) -> str:
        """Belgenin gövde HTML'i; çizim ve yerinde değişiklik aynı kaynağı kullanır."""
        # Kaynak değişmediyse çeviri yeniden yapılmıyor.
        onbellek = getattr(self, "_md_cache", None)
        if onbellek is not None and onbellek[0] == self._source:
            body, headings = onbellek[1]
        else:
            body, headings = render_markdown(self._source)
            self._md_cache = (self._source, (body, headings))

        parts = ["".join(self._banner_html(tone, text) for tone, text in self._banners)]
        parts.append(self._meta_html(body))
        parts.append(f'<div id="{EXTRA_ID}">{self._extra}</div>')
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

        self._has_progress_box = bool(aside)
        scripts = (SCROLL_SPY if aside else "") + COPY_BUTTONS
        return f'<div class="{page_class}">{content}{aside}</div>{scripts}'

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

        adimlar = "".join(
            f'<div class="step3{" done" if bitti else ""}"><span class="o">{STEP_CHECK}</span>'
            f"{html.escape(ad)}<small>{html.escape(ek)}</small></div>"
            for ad, bitti, ek in self._progress
        )
        progress = (
            '<div class="prog">'
            f'<div class="h2">{html.escape(self._language.t("section.section_progress"))}</div>'
            f'<div class="steps3">{adimlar}</div></div>'
        ) if self._progress else ""

        return (
            '<aside class="toc"><div class="toc-inner">'
            f'<div class="h">{html.escape(self._language.t("section.on_this_page"))}</div>'
            f'<div class="toc-links"><span class="toc-mark"></span>{links}</div>{progress}</div></aside>'
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
