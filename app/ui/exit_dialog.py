"""Çıkış onayı: pencere kapatılırken açılan kutu.

Önce işletim sisteminin başlık çubuğu olan düz bir onay kutusuydu
(`ConfirmDialog`); uygulamanın geri kalanı çerçevesiz ve temalı. Şimdi
güncelleme kutusuyla aynı dilde (`modal.py`): üstte sahne, altında başlık,
açıklama ve düğmeler.

Sahnede sentor el sallıyor (`farewell_scene.py`). Açıklamanın altında
bir satır seriyi söylüyor: bugün çalışıldıysa seri güvende, çalışılmadıysa
kapatmadan önce bunu bilmek işe yarıyor.

Odak "Vazgeç"te başlıyor: Enter yanlışlıkla çıkarmasın. Esc de vazgeçiyor.
"""

from __future__ import annotations

from datetime import date

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from ..core.language import LanguageManager
from ..resources.theme.tokens import SPACING
from . import modal
from .farewell_scene import FarewellScene

WIDTH = 500


class ExitDialog(QDialog):
    """"Odyssey'den çıkılsın mı?" kutusu."""

    def __init__(self, language: LanguageManager, store=None, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        modal.prepare(self)
        t = language.t

        layout = QVBoxLayout(self)
        layout.setContentsMargins(SPACING["lg"], SPACING["lg"], SPACING["lg"], SPACING["lg"])
        layout.setSpacing(SPACING["sm"])

        self.scene = FarewellScene()
        self.scene.setFixedHeight(170)
        layout.addWidget(self.scene)
        layout.addSpacing(SPACING["sm"])

        heading = QLabel(t("quit.title"))
        heading.setProperty("role", "modal-page-title")
        heading.setWordWrap(True)
        layout.addWidget(heading)

        # Seri satırı aynı etikette: ayrı etiket olunca iki sarmalı etiketin
        # yükseklik payı araya geniş bir boşluk koyuyordu.
        seri = self._streak_line(language, store)
        body = QLabel(t("quit.message") + (f"\n\n{seri}" if seri else ""))
        body.setProperty("role", "muted")
        body.setWordWrap(True)
        layout.addWidget(body)

        layout.addSpacing(SPACING["sm"])
        buttons = QHBoxLayout()
        buttons.setSpacing(SPACING["sm"])
        buttons.addStretch(1)
        cancel = QPushButton(t("quit.cancel"))
        cancel.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel.clicked.connect(self.reject)
        buttons.addWidget(cancel)
        confirm = QPushButton(t("quit.confirm"))
        confirm.setProperty("variant", "danger")
        confirm.setCursor(Qt.CursorShape.PointingHandCursor)
        confirm.clicked.connect(self.accept)
        buttons.addWidget(confirm)
        layout.addLayout(buttons)

        cancel.setDefault(True)
        cancel.setFocus()
        self.setWindowTitle(t("quit.title"))
        self.setFixedWidth(WIDTH)
        modal.freeze(self)

    @staticmethod
    def _streak_line(language: LanguageManager, store) -> str:
        """Seri varsa bir satır: bugün güvende mi, yoksa bugün çalışmak mı gerekiyor."""
        if store is None:
            return ""
        try:
            gun = store.streak()
            son = store.last_study_day()
        except Exception:  # noqa: BLE001 — kapanışta veritabanı hatası kutuyu engellemesin
            return ""
        if gun <= 0:
            return ""
        if son == date.today():
            return language.t("quit.streak_safe", count=gun)
        return language.t("quit.streak_risk", count=gun)
