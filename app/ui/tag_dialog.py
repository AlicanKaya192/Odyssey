"""Unvan penceresi: kazanılan unvanlardan birini seçmek.

Profilde adın altındaki unvana tıklanınca açılıyor. Bütün unvanlar
listeleniyor: kazanılmış olan açık ve tıklanınca hemen kullanılmaya
başlıyor; kazanılmamış olan kilitli ve üzerine gelince nasıl kazanılacağı
yazıyor. Seçili unvana yeniden tıklamak onu kaldırıyor.

Görünümü ve davranışı öbür kip pencerelerle ortak (`modal.py`).
"""

from __future__ import annotations

from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (
    QDialog,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ..core.language import LanguageManager
from ..resources.icons import icon
from ..resources.theme.tokens import PALETTES, SPACING
from ..widgets import tips
from . import modal

DIALOG_WIDTH = 600
COLUMNS = 3
ICON = 14
# Gruplar bu sırayla; `tags.json` → `kind`.
KINDS = ("level", "track", "feat")


class TagDialog(QDialog):
    """Unvanları gösterir; seçilen `selected` içinde döner."""

    def __init__(
        self,
        language: LanguageManager,
        tags: list[dict],
        earned,
        current: str = "",
        mode: str = "light",
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        t = language.t
        p = PALETTES.get(mode, PALETTES["light"])
        # Seçilen unvanın kimliği; kaldırıldıysa boş. Pencere kapatılırsa
        # (`reject`) açılıştaki değer geçerli.
        self.selected = current

        modal.prepare(self)
        self.setFixedWidth(DIALOG_WIDTH)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(SPACING["xl"], SPACING["xl"], SPACING["xl"], SPACING["xl"])
        layout.setSpacing(SPACING["sm"])

        heading = QLabel(t("tags.title"))
        heading.setProperty("role", "modal-title")
        layout.addWidget(heading)

        kazanilan = sum(1 for tag in tags if tag.get("id") in earned)
        alt = QLabel(t("tags.subtitle", earned=kazanilan, total=len(tags)))
        alt.setProperty("role", "muted")
        alt.setWordWrap(True)
        layout.addWidget(alt)

        self._buttons: dict[str, QPushButton] = {}
        for kind in KINDS:
            grup = [tag for tag in tags if tag.get("kind", "feat") == kind]
            if not grup:
                continue
            layout.addSpacing(SPACING["sm"])
            baslik = QLabel(language.t_upper(f"tags.group_{kind}"))
            baslik.setProperty("role", "tag-group")
            layout.addWidget(baslik)

            izgara = QGridLayout()
            izgara.setHorizontalSpacing(8)
            izgara.setVerticalSpacing(8)
            for sutun in range(COLUMNS):
                izgara.setColumnStretch(sutun, 1)
            for sira, tag in enumerate(grup):
                kimlik = tag.get("id", "")
                acik = kimlik in earned
                secili = acik and kimlik == current
                dugme = QPushButton(language.pick(tag.get("title"), kimlik))
                dugme.setProperty("variant", "tag-item")
                dugme.setProperty("state", "selected" if secili else "earned" if acik else "locked")
                dugme.setIconSize(QSize(ICON, ICON))
                nasil = language.pick(tag.get("how"), "")
                ad = language.pick(tag.get("title"), kimlik)
                if secili:
                    dugme.setIcon(icon("check", "#FFFFFF", ICON, stroke=2.6))
                    dugme.setToolTip(tips.rich(ad, nasil + "\n\n" + t("tags.tip_selected"),
                                               "✓  " + t("tags.state_selected"), "accent"))
                elif acik:
                    dugme.setToolTip(tips.rich(ad, nasil + "\n\n" + t("tags.tip_earned"),
                                               "✓  " + t("tags.state_earned"), "success"))
                else:
                    dugme.setIcon(icon("lock", p["text_muted"], ICON))
                    dugme.setToolTip(tips.rich(ad, nasil, "○  " + t("tags.state_locked"), "muted"))
                if acik:
                    dugme.setCursor(Qt.CursorShape.PointingHandCursor)
                    dugme.clicked.connect(lambda _=False, k=kimlik: self._pick(k))
                # Kilitli düğme devre dışı bırakılmıyor: ipucu görünsün ve
                # yazı stil dosyasındaki soluk renkte kalsın. Tıklama boşa gidiyor.
                dugme.setFocusPolicy(Qt.FocusPolicy.TabFocus if acik else Qt.FocusPolicy.NoFocus)
                izgara.addWidget(dugme, sira // COLUMNS, sira % COLUMNS)
                self._buttons[kimlik] = dugme
            layout.addLayout(izgara)

        layout.addSpacing(SPACING["md"])
        buttons = QHBoxLayout()
        buttons.setSpacing(SPACING["sm"])
        ipucu = QLabel(t("tags.hint"))
        ipucu.setProperty("role", "muted")
        ipucu.setWordWrap(True)
        buttons.addWidget(ipucu, 1)
        kapat = QPushButton(t("common.close"))
        kapat.setCursor(Qt.CursorShape.PointingHandCursor)
        kapat.clicked.connect(self.reject)
        kapat.setDefault(True)
        buttons.addWidget(kapat, 0, Qt.AlignmentFlag.AlignBottom)
        layout.addLayout(buttons)

        modal.freeze(self)
        modal.center(self)
        kapat.setFocus()

    def _pick(self, tag_id: str) -> None:
        """Unvanı seçer; zaten seçiliyse kaldırır. Pencere kapanıyor."""
        self.selected = "" if tag_id == self.selected else tag_id
        self.accept()
