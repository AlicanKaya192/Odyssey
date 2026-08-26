"""Sürüm notları ekranı.

Kök dizindeki `CHANGELOG.md` dosyasını okuyup kart hâlinde gösterir. Böylece
sürüm notları tek yerde yazılıyor: GitHub'da yayınlanan sürüm açıklamasıyla
uygulamanın içinde görünen metin aynı kaynaktan geliyor.

Kartlar diğer belge alanları gibi `DocumentView` ile çiziliyor; maketteki
kart tasarımı (yuvarlak köşe, gölge, "YENİ" rozeti) birebir uygulanıyor.

Dosya biçimi:

    ## [0.3] — 26 Ağustos 2026
    ### Eklendi
    - ...
"""

from __future__ import annotations

import html
import re
from dataclasses import dataclass, field
from pathlib import Path

from PySide6.QtWidgets import QVBoxLayout, QWidget

from ..core.language import LanguageManager
from ..paths import install_root
from ..widgets.document_view import DocumentView

# `(?!#)` şart: bu olmadan `### Eklendi` satırı da sürüm başlığı sanılıyor ve
# her grup ayrı bir kart olarak çiziliyordu.
VERSION_PATTERN = re.compile(r"^##(?!#)\s*\[?([^\]\n—-]+)\]?\s*(?:[—-]\s*(.+))?$")
GROUP_PATTERN = re.compile(r"^###\s+(.+)$")
ITEM_PATTERN = re.compile(r"^[-*]\s+(.+)$")


@dataclass
class Release:
    """Tek bir sürüm."""

    version: str
    date: str = ""
    groups: list[tuple[str, list[str]]] = field(default_factory=list)


def parse_changelog(path: Path) -> list[Release]:
    """`CHANGELOG.md` dosyasını sürümlere ayırır."""
    if not path.exists():
        return []

    releases: list[Release] = []
    current: Release | None = None

    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()

        version_match = VERSION_PATTERN.match(stripped)
        if version_match:
            current = Release(
                version=version_match.group(1).strip(),
                date=(version_match.group(2) or "").strip(),
            )
            releases.append(current)
            continue

        if current is None:
            continue

        group_match = GROUP_PATTERN.match(stripped)
        if group_match:
            current.groups.append((group_match.group(1).strip(), []))
            continue

        item_match = ITEM_PATTERN.match(stripped)
        if item_match:
            if not current.groups:
                current.groups.append(("", []))
            current.groups[-1][1].append(item_match.group(1).strip())

    return releases


class ReleaseView(QWidget):
    """Sürüm notlarının listelendiği ekran."""

    def __init__(self, language: LanguageManager, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._language = language

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self._document = DocumentView(self)
        layout.addWidget(self._document)

        self.refresh()

    def refresh(self) -> None:
        """`CHANGELOG.md`'yi yeniden okur."""
        releases = parse_changelog(install_root() / "CHANGELOG.md")

        if not releases:
            body = (
                f'<p class="meta">{html.escape(self._language.t("release.empty"))}</p>'
            )
        else:
            body = "".join(
                self._card(release, newest=index == 0)
                for index, release in enumerate(releases)
            )

        self._document.set_body(
            f'<div class="page narrow"><div class="content">{body}</div></div>'
        )

    def _card(self, release: Release, newest: bool) -> str:
        badge = (
            f'<span class="new">{html.escape(self._language.t("release.new"))}</span>'
            if newest
            else ""
        )
        date = f'<span class="dt">{html.escape(release.date)}</span>' if release.date else ""

        parts = [
            f'<div class="v"><b>{html.escape(release.version)}</b>{badge}{date}</div>'
        ]

        for title, items in release.groups:
            if title:
                parts.append(f"<h4>{html.escape(title)}</h4>")
            if items:
                bullets = "".join(f"<li>{html.escape(item)}</li>" for item in items)
                parts.append(f"<ul>{bullets}</ul>")

        return f'<div class="relcard">{"".join(parts)}</div>'

    def set_mode(self, mode: str) -> None:
        self._document.set_mode(mode)

    def retranslate(self) -> None:
        self.refresh()
