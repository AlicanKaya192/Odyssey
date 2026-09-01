"""Pencerenin altındaki telif şeridi.

Her ekranda görünüyor. Önceden yalnızca "Bağlantılarım / Ekstra İçerikler /
Lisans" sayfalarının en altında duruyordu; oysa sürüm numarasını görmek
isteyen biri en çok ders okurken ya da alıştırma çözerken merak ediyor.

Yıl elle yazılmıyor: `date.today().year` her açılışta güncel yılı veriyor,
böylece yılbaşında dosyaya dokunmak gerekmiyor.
"""

from __future__ import annotations

import json
from datetime import date

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QWidget

from ..core.language import LanguageManager
from ..paths import content_dir
from ..version import APP_VERSION
from ..resources.theme.tokens import SPACING


def _author_name() -> str:
    """Telif satırındaki ad `content/about.json` dosyasından geliyor."""
    path = content_dir() / "about.json"
    if not path.exists():
        return ""
    with path.open(encoding="utf-8") as handle:
        return json.load(handle).get("author", {}).get("name", "")


class Footer(QFrame):
    """Telif, sürüm ve lisans bilgisini taşıyan ince şerit."""

    def __init__(self, language: LanguageManager, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._language = language
        self._author = _author_name()

        self.setProperty("role", "footer")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(SPACING["lg"], SPACING["xs"], SPACING["lg"], SPACING["xs"])
        layout.setSpacing(0)

        self._label = QLabel()
        self._label.setProperty("role", "footnote")
        self._label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._label, 1)

        self.retranslate()

    def retranslate(self) -> None:
        # Yıl ile ad aynı öbek: "© 2026 Alican Kaya".
        owner = f"© {date.today().year}"
        if self._author:
            owner = f"{owner} {self._author}"

        parts = [owner]
        parts.append(f"{self._language.t('app.title')} {APP_VERSION}")
        parts.append(self._language.t("about.mit"))
        self._label.setText(" · ".join(parts))
