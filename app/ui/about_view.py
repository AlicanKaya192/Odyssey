"""Hakkında ekranı: bağlantılar, projeler ve lisans.

Üç bölüm segmented control ile ayrılıyor:

- **Bağlantılar** — proje sahibinin GitHub, LinkedIn, portfolyo ve Medium
  adresleri.
- **Ekstra İçerikler** — buradaki müfredatın ötesine geçmek isteyenler için
  açık kaynak projeler.
- **Lisans** — uygulamanın ve içeriğin lisansı, telif satırı.

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

SECTIONS = ("links", "projects", "license")


def load_about() -> dict:
    """`content/about.json` dosyasını okur."""
    path = content_dir() / "about.json"
    if not path.exists():
        return {}
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


class AboutView(QWidget):
    """Bağlantılar, projeler ve lisans."""

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

    def show_section(self, name: str) -> None:
        if name in SECTIONS:
            self._section = name
            self.refresh()

    def _on_action(self, action: str) -> None:
        """Sayfa içindeki bağlantılar.

        `open:<adres>` sistem tarayıcısında açar; başka bir şey uygulama
        içinde gezinme demektir.
        """
        if action.startswith("open:"):
            QDesktopServices.openUrl(QUrl(action[len("open:"):]))
            return
        self.show_section(action)

    # --- çizim ------------------------------------------------------------

    def refresh(self) -> None:
        builders = {
            "links": self._links_html,
            "projects": self._projects_html,
            "license": self._license_html,
        }
        body = builders[self._section]()

        self._document.set_body(
            '<div class="page narrow"><div class="content">'
            f"{self._segments_html()}{body}{self._footnote_html()}"
            "</div></div>"
        )

    def _segments_html(self) -> str:
        labels = {
            "links": self._language.t("about.links"),
            "projects": self._language.t("about.projects"),
            "license": self._language.t("about.license"),
        }
        buttons = "".join(
            f'<a href="app:{name}" class="{"pri" if name == self._section else ""}">'
            f"{html.escape(labels[name])}</a>"
            for name in SECTIONS
        )
        return f'<div class="foot" style="margin:0 0 28px;padding:0;border:none">{buttons}</div>'

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

    def _card(self, title: str, url: str, description: str, go_label: str) -> str:
        return (
            f'<a class="linkcard" href="app:open:{html.escape(url)}">'
            f'<div class="row"><b>{html.escape(title)}</b>'
            f'<span class="go">{html.escape(go_label)} →</span></div>'
            f"<p>{html.escape(description)}</p>"
            f'<div class="url">{html.escape(url)}</div></a>'
        )

    def _links_html(self) -> str:
        cards = "".join(
            self._card(
                item.get("label", ""),
                item.get("url", ""),
                self._language.pick(item.get("description")),
                self._language.t("about.open"),
            )
            for item in self._data.get("links", [])
        )
        return f"{self._author_html()}{cards}"

    def _projects_html(self) -> str:
        intro = f'<p class="meta">{html.escape(self._language.t("about.projects_intro"))}</p>'
        cards = "".join(
            self._card(
                self._language.pick(item.get("title")),
                item.get("url", ""),
                self._language.pick(item.get("description")),
                self._language.t("about.open"),
            )
            for item in self._data.get("projects", [])
        )
        return f"<h1>{html.escape(self._language.t('about.projects'))}</h1>{intro}{cards}"

    def _license_html(self) -> str:
        path = install_root() / "LICENSE"
        text = path.read_text(encoding="utf-8") if path.exists() else ""

        return (
            f"<h1>{html.escape(self._language.t('about.license'))}</h1>"
            f"<p>{html.escape(self._language.t('about.license_summary'))}</p>"
            f'<div class="licensebox">{html.escape(text)}</div>'
            f"<h2>{html.escape(self._language.t('about.content_license'))}</h2>"
            f"<p>{html.escape(self._language.t('about.content_license_text'))}</p>"
        )

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
