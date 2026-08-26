"""Sürüm notları ekranı.

Kök dizindeki `CHANGELOG.md` dosyasını okuyup kart hâlinde gösterir. Böylece
sürüm notları tek yerde yazılıyor: GitHub'da yayınlanan sürüm açıklamasıyla
uygulamanın içinde görünen metin aynı kaynaktan geliyor.

Dosya biçimi:

    ## [0.3] — 26 Ağustos 2026
    ### Eklendi
    - ...
    ### Düzeltildi
    - ...
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from ..core.language import LanguageManager
from ..paths import install_root
from ..resources.theme.tokens import READING_WIDTH, SPACING
from ..widgets.common import Card
from ..widgets.effects import repolish

VERSION_PATTERN = re.compile(r"^##\s*\[?([^\]\n—-]+)\]?\s*(?:[—-]\s*(.+))?$")
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
    group: str = ""

    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()

        version_match = VERSION_PATTERN.match(stripped)
        if version_match:
            current = Release(
                version=version_match.group(1).strip(),
                date=(version_match.group(2) or "").strip(),
            )
            releases.append(current)
            group = ""
            continue

        if current is None:
            continue

        group_match = GROUP_PATTERN.match(stripped)
        if group_match:
            group = group_match.group(1).strip()
            current.groups.append((group, []))
            continue

        item_match = ITEM_PATTERN.match(stripped)
        if item_match:
            if not current.groups:
                current.groups.append(("", []))
            current.groups[-1][1].append(item_match.group(1).strip())

    return releases


class ReleaseCard(Card):
    """Bir sürümün kartı."""

    def __init__(
        self,
        release: Release,
        language: LanguageManager,
        newest: bool,
        mode: str,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent, mode, padding=SPACING["lg"])
        self.body.setSpacing(SPACING["sm"])

        header = QHBoxLayout()
        header.setSpacing(SPACING["sm"])

        version = QLabel(release.version)
        version.setProperty("role", "subtitle")
        header.addWidget(version)

        if newest:
            badge = QLabel(language.t("release.new"))
            badge.setProperty("role", "chip")
            badge.setProperty("tone", "accent")
            header.addWidget(badge)

        header.addStretch(1)

        if release.date:
            date = QLabel(release.date)
            date.setProperty("role", "muted")
            header.addWidget(date)

        self.body.addLayout(header)

        for title, items in release.groups:
            if title:
                group_label = QLabel(title.upper())
                group_label.setProperty("role", "section")
                self.body.addSpacing(SPACING["sm"])
                self.body.addWidget(group_label)

            for item in items:
                bullet = QLabel(f"•  {item}")
                bullet.setWordWrap(True)
                bullet.setContentsMargins(SPACING["sm"], 0, 0, 0)
                self.body.addWidget(bullet)


class ReleaseView(QWidget):
    """Sürüm notlarının listelendiği ekran."""

    def __init__(self, language: LanguageManager, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._language = language
        self._mode = "light"

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        container = QWidget()
        row = QHBoxLayout(container)
        row.setContentsMargins(
            SPACING["xl"], SPACING["xl"], SPACING["xl"], SPACING["xxl"]
        )
        row.addStretch(1)

        column = QWidget()
        column.setMaximumWidth(READING_WIDTH + 80)
        column.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self._column = QVBoxLayout(column)
        self._column.setContentsMargins(0, 0, 0, 0)
        self._column.setSpacing(SPACING["md"])

        row.addWidget(column, 8)
        row.addStretch(1)

        scroll.setWidget(container)
        layout.addWidget(scroll)

        self.refresh()

    def refresh(self) -> None:
        """`CHANGELOG.md`'yi yeniden okur."""
        while self._column.count():
            item = self._column.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        releases = parse_changelog(install_root() / "CHANGELOG.md")

        if not releases:
            empty = QLabel(self._language.t("release.empty"))
            empty.setProperty("role", "muted")
            empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self._column.addWidget(empty)
            self._column.addStretch(1)
            return

        for index, release in enumerate(releases):
            self._column.addWidget(
                ReleaseCard(release, self._language, index == 0, self._mode)
            )
        self._column.addStretch(1)

    def set_mode(self, mode: str) -> None:
        self._mode = mode
        self.refresh()

    def retranslate(self) -> None:
        self.refresh()
