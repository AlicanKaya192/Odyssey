"""Pencerenin altındaki telif şeridi.

Her ekranda görünüyor. Önceden yalnızca "Bağlantılarım / Ekstra İçerikler /
Lisans" sayfalarının en altında duruyordu; oysa sürüm numarasını görmek
isteyen biri en çok ders okurken ya da alıştırma çözerken merak ediyor.

Yıl elle yazılmıyor: `date.today().year` her açılışta güncel yılı veriyor,
böylece yılbaşında dosyaya dokunmak gerekmiyor.

Yeni bir sürüm yayınlandığında şeride tıklanabilir bir satır ekleniyor.
Yeri burası çünkü şerit her ekranda duruyor; kullanıcı sürümü nerede
görüyorsa yenisini de orada görüyor.

Solda deponun GitHub yıldız sayısı (tıklayınca depo açılıyor), sağda
klavye kısayolları. Sağda eskiden bir de bildirim zili vardı; kalktı,
kutlamalar artık sağ altta beliren kartlarla (`app/widgets/toast.py`).
"""

from __future__ import annotations

import json
from datetime import date
from html import escape

from PySide6.QtCore import QSize, Qt, QUrl, Signal
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QWidget

from ..core import github_stars
from ..core.language import LanguageManager
from ..resources.icons import icon
from ..widgets.common import paint_hairline
from ..widgets.shortcut_panel import ShortcutButton
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
    # Klavye düğmesi: kısayol listesi açılsın.
    shortcuts_clicked = Signal()

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

        # Solda yıldız, sağda klavye düğmesi. İki yan bölge eşit genişlikte
        # tutuluyor (`_balance`) ki ortadaki telif yazısı kaymasın.
        self.star_button = StarButton()
        self.star_button.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl(github_stars.REPO_PAGE))
        )
        self.shortcut_button = ShortcutButton()
        self.shortcut_button.clicked.connect(self.shortcuts_clicked)

        self._left = QWidget()
        sol = QHBoxLayout(self._left)
        sol.setContentsMargins(0, 0, 0, 0)
        sol.addWidget(self.star_button)
        sol.addStretch(1)
        self._right = QWidget()
        sag = QHBoxLayout(self._right)
        sag.setContentsMargins(0, 0, 0, 0)
        sag.addStretch(1)
        sag.addWidget(self.shortcut_button)

        layout.addWidget(self._left)
        layout.addWidget(self._label, 1)
        layout.addWidget(self._right)

        self.retranslate()

    def _balance(self) -> None:
        genis = max(self.star_button.sizeHint().width(), self.shortcut_button.width())
        self._left.setFixedWidth(genis)
        self._right.setFixedWidth(genis)

    def set_stars(self, count: int | None) -> None:
        """Yıldız sayısı; bilinmiyorsa (`None`) yalnızca "GitHub" yazıyor."""
        self.star_button.set_count(count)
        self.retranslate()

    def set_update(self, version: str, url: str) -> None:
        """Yeni sürüm duyurusunu şeride koyar; boş sürüm kaldırıyor."""
        if (version, url) == (self._update_version, self._update_url):
            return
        self._update_version = version
        self._update_url = url
        self.retranslate()

    def paintEvent(self, event) -> None:  # noqa: N802
        super().paintEvent(event)
        paint_hairline(self, "top")

    def set_mode(self, mode: str) -> None:
        self._link_color = PALETTES.get(mode, PALETTES["dark"])["accent"]
        self.star_button.set_mode(mode)
        self.shortcut_button.set_mode(mode)
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
        self.shortcut_button.setToolTip(self._language.t("shortcut.tooltip"))
        sayi = self.star_button.count
        self.star_button.setToolTip(
            self._language.t("footer.star_tooltip_count", count=sayi)
            if sayi is not None
            else self._language.t("footer.star_tooltip")
        )
        self._balance()


class StarButton(QPushButton):
    """Sol alttaki yıldız: sarı yıldız ve yanında deponun yıldız sayısı."""

    ICON = 13

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.count: int | None = None
        self._mode = "dark"
        self.setProperty("variant", "footer-star")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setIconSize(QSize(self.ICON, self.ICON))
        self.set_mode(self._mode)
        self.set_count(None)

    def set_count(self, count: int | None) -> None:
        self.count = count
        # Binlerce yıldızda "1.2k" gibi kısaltma; küçük sayılar olduğu gibi.
        if count is None:
            metin = "GitHub"
        elif count >= 1000:
            metin = f"{count / 1000:.1f}k".replace(".0k", "k")
        else:
            metin = str(count)
        self.setText(f" {metin}")

    def set_mode(self, mode: str) -> None:
        self._mode = mode
        palette = PALETTES.get(mode, PALETTES["dark"])
        self.setIcon(icon("star", palette["warning"], self.ICON, filled=True))
