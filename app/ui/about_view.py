"""Bağlantılarım, Ekstra İçerikler ve Lisans ekranları.

Üçü ayrı menü öğesi; şeritten doğrudan girilir. Aynı sınıf üçünü de
çiziyor, çünkü hepsi aynı düzeni paylaşıyor: kart ızgarası ve altta telif
satırı.

Kartlar ikişerli diziliyor — dördünü alt alta uzatmak hem yer israfı hem de
hepsini bir arada görmeyi engelliyordu.

Bağlantılar uygulamanın içinde açılmıyor; tıklanınca sistemin tarayıcısına
gidiyor. Uygulama kendi başına ağa çıkmıyor, yalnızca kullanıcının açık
isteğiyle bir adres açılıyor.
"""

from __future__ import annotations

import html
import json
from datetime import date

from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QVBoxLayout, QWidget

from ..core.language import LanguageManager
from ..paths import content_dir, install_root
from ..version import APP_VERSION
from ..widgets.document_view import DocumentView

SECTIONS = ("links", "extras", "license")

# Lisansın özgün dili. Bu dilde ayrıca çeviri gösterilmiyor.
FALLBACK_LICENSE_LANGUAGE = "en"


def load_about() -> dict:
    """`content/about.json` dosyasını okur."""
    path = content_dir() / "about.json"
    if not path.exists():
        return {}
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


class AboutView(QWidget):
    """Bağlantılar, projeler veya lisans — hangisi seçiliyse onu gösterir."""

    def __init__(self, language: LanguageManager, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._language = language
        self._data = load_about()
        self._section = "links"

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self._document = DocumentView(self)
        self._document.action.connect(self._on_action)
        layout.addWidget(self._document)

        self.refresh()

    # --- gezinme ----------------------------------------------------------

    @property
    def section(self) -> str:
        """Hangi bölüm gösteriliyor: links, extras veya license."""
        return self._section

    def show_section(self, name: str) -> None:
        if name in SECTIONS and name != self._section:
            self._section = name
            self.refresh()
        elif name in SECTIONS:
            self._section = name

    def _on_action(self, action: str) -> None:
        """Sayfa içindeki bağlantılar sistem tarayıcısında açılır."""
        if action.startswith("open:"):
            QDesktopServices.openUrl(QUrl(action[len("open:"):]))

    # --- çizim ------------------------------------------------------------

    def refresh(self) -> None:
        builders = {
            "links": self._links_html,
            "extras": self._extras_html,
            "license": self._license_html,
        }
        body = builders[self._section]()

        self._document.set_body(
            '<div class="page narrow"><div class="content">'
            f"{body}{self._footnote_html()}"
            "</div></div>"
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

    def _card(self, title: str, url: str, description: str) -> str:
        go = self._language.t("about.open")
        return (
            f'<a class="linkcard" href="app:open:{html.escape(url)}">'
            f'<div class="row"><b>{html.escape(title)}</b>'
            f'<span class="go">{html.escape(go)} →</span></div>'
            f"<p>{html.escape(description)}</p>"
            f'<div class="url">{html.escape(url)}</div></a>'
        )

    def _grid(self, cards: list[str]) -> str:
        return f'<div class="cardgrid">{"".join(cards)}</div>'

    def _links_html(self) -> str:
        cards = [
            self._card(
                item.get("label", ""),
                item.get("url", ""),
                self._language.pick(item.get("description")),
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
        return (
            f"<h1>{html.escape(self._language.t('nav.extras'))}</h1>"
            f"{intro}{self._grid(cards)}"
        )

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
            f"<h1>{html.escape(self._language.t('nav.license'))}</h1>"
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

    def _footnote_html(self) -> str:
        """En alttaki telif satırı."""
        author = self._data.get("author", {}).get("name", "")
        return (
            f'<div class="footnote">© {date.today().year} {html.escape(author)} · '
            f"{html.escape(self._language.t('app.title'))} {APP_VERSION} · "
            f"{html.escape(self._language.t('about.mit'))}</div>"
        )

    # --- tema ve dil ------------------------------------------------------

    def set_mode(self, mode: str) -> None:
        self._document.set_mode(mode)

    def retranslate(self) -> None:
        self.refresh()
