"""Pencerenin altındaki telif şeridi.

Her ekranda görünüyor. Önceden yalnızca "Bağlantılarım / Ekstra İçerikler /
Lisans" sayfalarının en altında duruyordu; oysa sürüm numarasını görmek
isteyen biri en çok ders okurken ya da alıştırma çözerken merak ediyor.

Yıl elle yazılmıyor: `date.today().year` her açılışta güncel yılı veriyor,
böylece yılbaşında dosyaya dokunmak gerekmiyor.

Yeni bir sürüm yayınlandığında şeride tıklanabilir bir satır ekleniyor.
Yeri burası çünkü şerit her ekranda duruyor; kullanıcı sürümü nerede
görüyorsa yenisini de orada görüyor.
"""

from __future__ import annotations

import json
from datetime import date
from html import escape

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QWidget

from ..core.language import LanguageManager
from ..paths import content_dir
from ..version import APP_VERSION
from ..resources.theme.tokens import PALETTES, SPACING


def _author_name() -> str:
    """Telif satırındaki ad `content/about.json` dosyasından geliyor."""
    path = content_dir() / "about.json"
    if not path.exists():
        return ""
    with path.open(encoding="utf-8") as handle:
        return json.load(handle).get("author", {}).get("name", "")


class Footer(QFrame):
    """Telif, sürüm ve lisans bilgisini taşıyan ince şerit."""

    # Yeni sürüm duyurusuna tıklandı. Şerit bağlantıyı kendisi açmıyor:
    # tarayıcıya atmak kullanıcıyı sürüm sayfasında bırakıyordu, oysa
    # uygulama güncellemeyi kendisi kurabiliyor. Karar pencerede veriliyor.
    update_clicked = Signal()

    def __init__(self, language: LanguageManager, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._language = language
        self._author = _author_name()
        self._update_version = ""
        self._update_url = ""
        # Bağlantının rengi QSS'ten gelmiyor: `QLabel` içindeki `<a>`
        # etiketine QSS ulaşmıyor, renk HTML'in içine yazılıyor.
        self._link_color = PALETTES["dark"]["accent"]

        self.setProperty("role", "footer")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(SPACING["lg"], SPACING["xs"], SPACING["lg"], SPACING["xs"])
        layout.setSpacing(0)

        self._label = QLabel()
        self._label.setProperty("role", "footnote")
        self._label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._label.setOpenExternalLinks(False)
        self._label.setTextInteractionFlags(
            Qt.TextInteractionFlag.LinksAccessibleByMouse
        )
        self._label.linkActivated.connect(lambda _: self.update_clicked.emit())
        layout.addWidget(self._label, 1)

        self.retranslate()

    def set_update(self, version: str, url: str) -> None:
        """Yeni sürüm duyurusunu şeride koyar; boş sürüm kaldırıyor."""
        if (version, url) == (self._update_version, self._update_url):
            return
        self._update_version = version
        self._update_url = url
        self.retranslate()

    def set_mode(self, mode: str) -> None:
        self._link_color = PALETTES.get(mode, PALETTES["dark"])["accent"]
        self.retranslate()

    def retranslate(self) -> None:
        # Yıl ile ad aynı öbek: "© 2026 Alican Kaya".
        owner = f"© {date.today().year}"
        if self._author:
            owner = f"{owner} {self._author}"

        parts = [escape(owner)]
        parts.append(escape(f"{self._language.t('app.title')} {APP_VERSION}"))
        parts.append(escape(self._language.t("about.mit")))

        if self._update_version:
            metin = self._language.t(
                "update.available", version=self._update_version
            )
            parts.append(
                f'<a href="{escape(self._update_url, quote=True)}" '
                f'style="color:{self._link_color}; text-decoration:none;">'
                f"{escape(metin)}</a>"
            )

        self._label.setText(" · ".join(parts))
