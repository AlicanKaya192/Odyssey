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
from math import ceil
from pathlib import Path

from PySide6.QtWidgets import QVBoxLayout, QWidget

from ..core.language import LanguageManager
from ..paths import install_root
from ..widgets.document_view import DocumentView

# Sürüm başlığı iki şart taşıyor:
#   `(?!#)`  — `### Eklendi` gibi alt başlıklar sürüm sanılmasın.
#   `(\d...)` — numara rakamla başlar. Bu olmadan dosyadaki açıklama
#              başlıkları ("## Sürüm numaraları nasıl ilerliyor?") da sürüm
#              olarak listeleniyordu.
VERSION_PATTERN = re.compile(r"^##(?!#)\s*\[?(\d[^\]\n—-]*)\]?\s*(?:[—-]\s*(.+))?$")
GROUP_PATTERN = re.compile(r"^###\s+(.+)$")
ITEM_PATTERN = re.compile(r"^[-*]\s+(.+)$")

# Bir sayfada gösterilecek sürüm sayısı. Hepsi alt alta dizilince ekran
# gereğinden uzun oluyordu.
PAGE_SIZE = 3

# Madde metinlerinde satır içi markdown kullanılıyor. Metin ham basılırsa
# yıldızlar ve ters tırnaklar ekranda göründüğü için burada HTML'e çevriliyor.
INLINE_CODE_PATTERN = re.compile(r"`([^`]+)`")
INLINE_BOLD_PATTERN = re.compile(r"\*\*(.+?)\*\*")


def _is_alpha(version: str) -> bool:
    """1.0'dan önceki her sürüm alpha sayılıyor.

    Ana numara sıfırken uygulama hâlâ yapım aşamasında; sürüm notunun yanında
    bunu yazmak, o sürümü indiren birine ne beklemesi gerektiğini söylüyor.
    1.0 çıktığında rozet kendiliğinden kayboluyor, ayrıca bir şey silmek
    gerekmiyor.
    """
    head = version.strip().lstrip("vV").split(".")[0]
    return head.isdigit() and int(head) == 0


def _inline(text: str) -> str:
    """`**kalın**` ve `` `kod` `` işaretlerini HTML'e çevirir.

    Önce kaçış uygulanıyor; böylece metindeki `<` işareti etiket sanılmıyor.
    Kod ile kalın sırası önemli: kod bloğunun içindeki yıldızlar kalın
    yazıya dönüşmesin diye kod önce işleniyor.
    """
    escaped = html.escape(text)
    escaped = INLINE_CODE_PATTERN.sub(r"<code>\1</code>", escaped)
    return INLINE_BOLD_PATTERN.sub(r"<strong>\1</strong>", escaped)


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
            continue

        # Devam satırı: dosyada maddeler seksen sütuna sığsın diye alt
        # satıra taşırılıyor ve devamı boşlukla girintileniyor. Bu satırlar
        # önce hiç okunmuyordu; uzun maddeler ekranda yarıda kesiliyordu
        # ("...ekranın adı bir kez de sayfanın" diye bitiyordu).
        if stripped and line[:1].isspace() and current.groups and current.groups[-1][1]:
            current.groups[-1][1][-1] += " " + stripped

    return releases


class ReleaseView(QWidget):
    """Sürüm notlarının listelendiği ekran."""

    def __init__(self, language: LanguageManager, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._language = language

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self._page = 0

        self._document = DocumentView(self)
        self._document.action.connect(self._on_action)
        layout.addWidget(self._document)

        self.refresh()

    def _changelog_path(self) -> Path:
        """Seçili dilin sürüm notu dosyası.

        İngilizcesi yoksa Türkçesine düşer; sürüm notu boş kalmasın.
        """
        if self._language.language != "tr":
            wanted = install_root() / f"CHANGELOG.{self._language.language}.md"
            if wanted.exists():
                return wanted
        return install_root() / "CHANGELOG.md"

    def latest_version(self) -> str:
        """En yeni sürüm numarası; bildirim noktası buna bakıyor."""
        releases = parse_changelog(self._changelog_path())
        return releases[0].version if releases else ""

    def _on_action(self, action: str) -> None:
        """Sayfa değiştirme bağlantıları."""
        if action.startswith("page:"):
            try:
                self._page = int(action[len("page:"):])
            except ValueError:
                return
            self.refresh()

    def refresh(self) -> None:
        """Sürüm notlarını seçili dilde okur.

        Bütün sürümler tek sayfada listelenince ekran uzayıp gidiyordu; bu
        yüzden sayfa başına `PAGE_SIZE` sürüm gösteriliyor, altta sayfa
        düğmeleri duruyor.
        """
        self._document.set_lang(self._language.language)
        releases = parse_changelog(self._changelog_path())

        if not releases:
            self._page = 0
            body = (
                f'<p class="meta">{html.escape(self._language.t("release.empty"))}</p>'
            )
        else:
            total_pages = max(1, ceil(len(releases) / PAGE_SIZE))
            # Dil değişince ya da sürüm silinince sayfa numarası taşabilir.
            self._page = max(0, min(self._page, total_pages - 1))

            start = self._page * PAGE_SIZE
            shown = releases[start:start + PAGE_SIZE]

            body = "".join(
                self._card(release, newest=(start + offset) == 0)
                for offset, release in enumerate(shown)
            )
            body += self._pager_html(total_pages)

        self._document.set_body(
            f'<div class="page narrow"><div class="content">{body}</div></div>'
        )

    def _pager_html(self, total_pages: int) -> str:
        """Alttaki sayfa düğmeleri. Tek sayfa varsa hiç çizilmiyor."""
        if total_pages < 2:
            return ""

        parts = []

        if self._page > 0:
            parts.append(f'<a class="pg" href="app:page:{self._page - 1}">&#8592;</a>')
        else:
            parts.append('<span class="pg off">&#8592;</span>')

        for index in range(total_pages):
            if index == self._page:
                parts.append(f'<span class="pg on">{index + 1}</span>')
            else:
                parts.append(f'<a class="pg" href="app:page:{index}">{index + 1}</a>')

        if self._page < total_pages - 1:
            parts.append(f'<a class="pg" href="app:page:{self._page + 1}">&#8594;</a>')
        else:
            parts.append('<span class="pg off">&#8594;</span>')

        # Sayfa numaraları zaten kaçıncı sayfada olduğunu gösteriyor;
        # ayrıca "Sayfa 1 / 2" yazmak aynı bilgiyi ikinci kez söylüyordu.
        return f'<div class="pager">{"".join(parts)}</div>'

    def _card(self, release: Release, newest: bool) -> str:
        badge = (
            f'<span class="new">{html.escape(self._language.t("release.new"))}</span>'
            if newest
            else ""
        )
        stage = (
            f'<span class="stage">{html.escape(self._language.t("release.alpha"))}</span>'
            if _is_alpha(release.version)
            else ""
        )
        date = f'<span class="dt">{html.escape(release.date)}</span>' if release.date else ""

        parts = [
            f'<div class="v"><b>{html.escape(release.version)}</b>'
            f"{stage}{badge}{date}</div>"
        ]

        for title, items in release.groups:
            if title:
                parts.append(f"<h4>{html.escape(title)}</h4>")
            if items:
                bullets = "".join(f"<li>{_inline(item)}</li>" for item in items)
                parts.append(f"<ul>{bullets}</ul>")

        return f'<div class="relcard">{"".join(parts)}</div>'

    def set_mode(self, mode: str) -> None:
        self._document.set_mode(mode)

    def retranslate(self) -> None:
        self.refresh()
