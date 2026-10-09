"""Hakkında ekranı.

Beş bölüm tek bir ekranda toplandı: Bilgi, SSS, Bağlantılarım, Ekstra
İçerikler ve Lisans. Bölümler arasında başlıktaki sekmelerle geçiliyor —
konu ekranındaki seçicinin aynısı.

Önce her biri şeritte ayrı bir simgeydi. Bilgi ve SSS eklenince şeritte
dokuz simge olacaktı; hangisinin ne olduğunu öğrenmek için hepsinin üstüne
gelmek gerekiyordu. Beşi bir araya alınca şerit yediden beşe indi ve
bölümlerin adı simge yerine yazıyla görünür oldu.

Bağlantılar uygulamanın içinde açılmıyor; tıklanınca sistemin tarayıcısına
gidiyor. Uygulama kendi başına ağa çıkmıyor, yalnızca kullanıcının açık
isteğiyle bir adres açılıyor.

Telif satırı burada değil: pencerenin altındaki şeritte (`app/ui/footer.py`)
ve her ekranda görünüyor.
"""

from __future__ import annotations

import html
import json

import markdown

from PySide6.QtCore import QUrl, Signal
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QVBoxLayout, QWidget

from ..core.language import LanguageManager
from ..paths import content_dir, install_root
from ..widgets.document_view import DocumentView

# Sekmelerin sırası. Önce uygulamanın kendisi — ne olduğu, sık sorulanlar,
# hangi lisansla dağıtıldığı — sonra benimle ilgili olanlar: bağlantılarım
# ve diğer projelerim.
# Sözlük (0.9.2) SSS'nin yanında: ikisi de "takıldım, bakayım" sayfası.
SECTIONS = ("info", "faq", "glossary", "license", "links", "extras")

# Lisansın özgün dili. Bu dilde ayrıca çeviri gösterilmiyor.
FALLBACK_LICENSE_LANGUAGE = "en"

MARKDOWN_EXTENSIONS = ["fenced_code", "tables", "sane_lists"]


def load_about() -> dict:
    """`content/about.json` dosyasını okur."""
    return _load_json("about.json")


def load_faq() -> dict:
    """`content/faq.json` dosyasını okur."""
    return _load_json("faq.json")


def _load_json(name: str) -> dict:
    path = content_dir() / name
    if not path.exists():
        return {}
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


class AboutView(QWidget):
    """Bilgi, SSS, bağlantılar, projeler ve lisans — seçili olan gösterilir."""

    # Sekme değişince yayılıyor; başlığın rengi ve alt yazısı buna bakıyor.
    section_changed = Signal(str)

    def __init__(self, language: LanguageManager, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._language = language
        self._data = load_about()
        self._faq = load_faq()
        self._section = SECTIONS[0]

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self._document = DocumentView(self)
        self._document.action.connect(self._on_action)
        layout.addWidget(self._document)

        self.refresh()

    # --- gezinme ----------------------------------------------------------

    @property
    def section(self) -> str:
        """Hangi bölüm gösteriliyor."""
        return self._section

    @property
    def section_index(self) -> int:
        return SECTIONS.index(self._section)

    def show_section(self, name: str) -> None:
        if name not in SECTIONS:
            return
        değişti = name != self._section
        self._section = name
        if değişti:
            # Sayfa yeniden yüklenmiyor: bütün bölümler sayfada, yalnızca
            # görünen değişiyor ve yeni bölüm 16 px aşağıdan beliriyor
            # (prototip `pgIn`). Önce her sekmede sayfa baştan yükleniyor,
            # bir an boşalıyordu.
            if self._document._loaded:  # noqa: SLF001
                self._document.page().runJavaScript(
                    "document.querySelectorAll('.absec').forEach(function(e){"
                    f"var on=e.dataset.s=={name!r};e.classList.toggle('on',on);"
                    "e.classList.remove('anim');if(on){void e.offsetWidth;e.classList.add('anim');}});"
                    "(document.scrollingElement||document.documentElement).scrollTop=0;"
                )
            else:
                self.refresh(force=True)
            self.section_changed.emit(name)

    def show_index(self, index: int) -> None:
        """Sekme seçicisinden gelen sıra numarası."""
        if 0 <= index < len(SECTIONS):
            self.show_section(SECTIONS[index])

    def _on_action(self, action: str) -> None:
        """Sayfa içindeki bağlantılar sistem tarayıcısında açılır."""
        if action.startswith("open:"):
            QDesktopServices.openUrl(QUrl(action[len("open:"):]))

    # --- çizim ------------------------------------------------------------

    def refresh(self, force: bool = False) -> None:
        # Dil değişmediyse yeniden yüklenmiyor (her girişte boşalıp doluyordu).
        if not force and getattr(self, "_rendered_lang", None) == self._language.language:
            return
        self._rendered_lang = self._language.language
        self._document.set_lang(self._language.language)
        builders = {
            "info": self._info_html,
            "faq": self._faq_html,
            "glossary": self._glossary_html,
            "links": self._links_html,
            "extras": self._extras_html,
            "license": self._license_html,
        }
        body = "".join(
            f'<section class="absec{" on" if ad == self._section else ""}" data-s="{ad}">{builders[ad]()}</section>'
            for ad in SECTIONS
        )

        giris = " pre-enter" if not getattr(self, "_entered", False) and self.window().isVisible() else ""
        if giris:
            self._entered = True
        self._document.set_body(
            f'<div class="page narrow about{giris}"><div class="content">{body}</div></div>'
        )

    def _author_html(self) -> str:
        author = self._data.get("author", {})
        name = author.get("name", "")
        if not name:
            return ""

        initials = "".join(part[0] for part in name.split()[:2]).upper()
        tagline = self._language.pick(author.get("tagline"))
        return (
            f'<div class="who"><div class="av">{html.escape(initials)}</div>'
            f"<div><b>{html.escape(name)}</b>"
            f"<span>{html.escape(tagline)}</span></div></div>"
        )

    def _card(self, title: str, url: str, description: str,
              display: str = "") -> str:
        go = self._language.t("about.open")
        shown = display or url
        return (
            f'<a class="linkcard" href="app:open:{html.escape(url)}">'
            f'<div class="row"><b>{html.escape(title)}</b>'
            f'<span class="go">{html.escape(go)} →</span></div>'
            f"<p>{html.escape(description)}</p>"
            f'<div class="url">{html.escape(shown)}</div></a>'
        )

    def _grid(self, cards: list[str]) -> str:
        return f'<div class="cardgrid">{"".join(cards)}</div>'

    # --- bölümler ---------------------------------------------------------

    def _info_html(self) -> str:
        """Uygulamanın ne olduğunu anlatan metin.

        Markdown olarak `content/` altında duruyor; ders metinleriyle aynı
        yerde yazılıp aynı biçimde çiziliyor. İngilizcesi yoksa Türkçesine
        düşüyor.
        """
        for code in (self._language.language, "tr"):
            path = content_dir() / f"info.{code}.md"
            if path.exists():
                return markdown.markdown(
                    path.read_text(encoding="utf-8"),
                    extensions=MARKDOWN_EXTENSIONS,
                )
        return ""

    def _faq_html(self) -> str:
        """Sık sorulanlar, açılıp kapanan başlıklar hâlinde.

        Başlığa basınca cevap yayla açılıyor (sayfa içi, uygulamaya haber yok).
        """
        intro = f'<p class="meta">{html.escape(self._language.t("about.faq_intro"))}</p>'

        parts = []
        for item in self._faq.get("questions", []):
            soru = self._language.pick(item.get("question"))
            cevap = markdown.markdown(
                self._language.pick(item.get("answer")),
                extensions=MARKDOWN_EXTENSIONS,
            )
            # Prototip `.faq`: cevap yüksekliği yayla açılıp kapanıyor
            # (yerleşik `<details>` anında açılıyordu).
            parts.append(
                "<div class='faq'>"
                "<div class='q' onclick='this.parentElement.classList.toggle(&quot;open&quot;)'>"
                f"{html.escape(soru)}<span class='mark'></span></div>"
                f"<div class='kids'><div><div class='answer'>{cevap}</div></div></div>"
                "</div>"
            )

        return f"{intro}<div class='faqlist'>{''.join(parts)}</div>"

    def _glossary_html(self) -> str:
        """Terimler sözlüğü: patikalara göre gruplu, gruplar içinde abece sırası."""
        from ..core import glossary

        dil = self._language.language
        t = self._language.t
        parts = [f'<p class="meta">{html.escape(t("about.glossary_intro"))}</p>']
        terimler = glossary.load()
        for grup in glossary.GROUPS:
            grubun = sorted(
                (term for term in terimler if term.get("group") == grup),
                key=lambda term: glossary.sort_key(term["title"].get(dil, "")),
            )
            if not grubun:
                continue
            parts.append(f"<h2>{html.escape(t(f'glossary.group_{grup}'))}</h2><div class='gl-list'>")
            for term in grubun:
                parts.append(
                    f"<div class='gl' id='{glossary.anchor(term['id'])}'>"
                    f"<b>{html.escape(term['title'].get(dil, ''))}</b>"
                    f"<p>{glossary.text_html(term['text'].get(dil, ''))}</p></div>"
                )
            parts.append("</div>")
        return "".join(parts)

    def show_term(self, term_id: str) -> None:
        """Sözlük sekmesini açıp terime kaydırır ve kısa süre vurgular (arama)."""
        from ..core import glossary

        self.show_section("glossary")
        kimlik = json.dumps(glossary.anchor(term_id))
        betik = (
            f"(function(){{var e=document.getElementById({kimlik});if(!e)return;"
            "e.scrollIntoView({block:'center'});e.classList.remove('hit');void e.offsetWidth;"
            "e.classList.add('hit');})();"
        )
        from PySide6.QtCore import QTimer

        view = self._document
        if view._loaded:  # noqa: SLF001
            # Sekme değişiminin kaydırmayı başa alması bitsin diye bir tur sonra.
            QTimer.singleShot(60, lambda: view.page().runJavaScript(betik))
            return

        # Sayfa daha yükleniyor: yükleme bitince aynı betik (kaydır + vurgula).
        # Önce yalnızca bekleyen çapa veriliyordu; terim kaydırılıyor ama
        # vurgulanmıyordu, sözlük büyüdükçe arama çoğu zaman bu yola düşüyordu.
        def _once(ok: bool) -> None:
            view.loadFinished.disconnect(_once)
            if ok:
                QTimer.singleShot(60, lambda: view.page().runJavaScript(betik))

        view.loadFinished.connect(_once)

    def _links_html(self) -> str:
        cards = [
            self._card(
                item.get("label", ""),
                item.get("url", ""),
                self._language.pick(item.get("description")),
                display=item.get("display", ""),
            )
            for item in self._data.get("links", [])
        ]
        return f"{self._author_html()}{self._grid(cards)}"

    def _extras_html(self) -> str:
        intro = f'<p class="meta">{html.escape(self._language.t("about.extras_intro"))}</p>'
        cards = [
            self._card(
                self._language.pick(item.get("title")),
                item.get("url", ""),
                self._language.pick(item.get("description")),
            )
            for item in self._data.get("projects", [])
        ]
        return f"{intro}{self._grid(cards)}"

    def _license_html(self) -> str:
        """Lisans ekranı.

        Lisans metni seçili dilde gösteriliyor — ekranın geri kalanı gibi.
        Türkçede çeviri, İngilizcede özgün metin. İki dilde de ekranın yapısı
        aynı: tek bir lisans kutusu, altında ders içeriğinin lisansı.

        Çevirinin yanına özgün İngilizce metni de koymayı denedik; ekranı
        gereksiz yere ikiye bölüyordu. Bağlayıcı metin uygulamayla birlikte
        gelen `LICENSE` dosyasında ve depoda zaten duruyor.
        """
        translation = self._license_translation()
        if not translation:
            original = install_root() / "LICENSE"
            translation = original.read_text(encoding="utf-8") if original.exists() else ""

        return (
            f"<p>{html.escape(self._language.t('about.license_summary'))}</p>"
            f'<div class="licensebox">{html.escape(translation)}</div>'
            f"<h2>{html.escape(self._language.t('about.content_license'))}</h2>"
            f"<p>{html.escape(self._language.t('about.content_license_text'))}</p>"
        )

    def _license_translation(self) -> str:
        """Seçili dil için lisans çevirisi; İngilizcede çeviri yok."""
        if self._language.language == FALLBACK_LICENSE_LANGUAGE:
            return ""
        path = install_root() / "app" / "resources" / f"LICENSE.{self._language.language}.txt"
        return path.read_text(encoding="utf-8") if path.exists() else ""

    # --- tema ve dil ------------------------------------------------------

    def set_mode(self, mode: str) -> None:
        self._document.set_mode(mode)

    def retranslate(self) -> None:
        self.refresh()
