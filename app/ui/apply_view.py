"""Yardımcı kip: dosyaları değiştiren küçük pencere.

Uygulama `--apply-update` ile açıldığında buraya geliyor. Bu süreç
**yeni sürümün** kopyası; eski sürüm kapanmayı bekliyor, sonra kurulum
klasörü yenileniyor ve uygulama tekrar açılıyor.

Pencere küçük ve tek işi var: ne olduğunu söylemek. Kullanıcı bu sırada
uygulamanın kapanmış olduğunu görüyor; ekranda hiçbir şey olmasaydı
güncellemenin çöktüğünü sanardı.
"""

from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QLabel,
    QProgressBar,
    QVBoxLayout,
)

from ..core import updater
from ..core.language import AVAILABLE_LANGUAGES, LanguageManager, system_language
from ..core.progress import ProgressStore
from ..core.theme import ThemeManager
from ..paths import database_path
from ..resources.theme.tokens import SPACING


class ApplyWorker(QThread):
    """Kopyalamayı arka planda yapıyor; pencere donmuyor."""

    progress = Signal(int)
    finished_with = Signal(str)

    def __init__(self, target: Path, pid: int, parent=None) -> None:
        super().__init__(parent)
        self._target = target
        self._pid = pid

    def run(self) -> None:  # noqa: D102
        def ilerleme(sira: int, toplam: int) -> None:
            self.progress.emit(int(sira * 100 / toplam) if toplam else 0)

        try:
            hata = updater.apply_update(self._target, self._pid, ilerleme)
        except Exception as beklenmeyen:  # noqa: BLE001
            hata = f"unexpected: {beklenmeyen!r}"
        self.finished_with.emit(hata)


class ApplyWindow(QDialog):
    """"Güncelleniyor…" penceresi."""

    def __init__(self, language: LanguageManager, target: Path, pid: int) -> None:
        super().__init__()
        self._language = language
        self._target = target
        self.error = ""

        self.setWindowTitle(language.t("update.notice_title"))
        self.setWindowFlags(
            Qt.WindowType.Dialog | Qt.WindowType.CustomizeWindowHint
        )
        self.setFixedWidth(420)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            SPACING["lg"], SPACING["lg"], SPACING["lg"], SPACING["lg"]
        )
        layout.setSpacing(SPACING["md"])

        heading = QLabel(language.t("update.applying_heading"))
        heading.setProperty("role", "title")
        heading.setWordWrap(True)
        layout.addWidget(heading)

        self._bar = QProgressBar()
        self._bar.setRange(0, 100)
        self._bar.setTextVisible(False)
        layout.addWidget(self._bar)

        self._status = QLabel()
        self._status.setProperty("role", "muted")
        self._status.setWordWrap(True)
        layout.addWidget(self._status)
        self._set_status(language.t("update.applying_wait"))

        self._worker = ApplyWorker(target, pid, self)
        self._worker.progress.connect(self._on_progress)
        self._worker.finished_with.connect(self._on_finished)
        self._worker.start()

    def _set_status(self, text: str) -> None:
        """Durum satırını yazar ve pencereyi metne göre yeniden ölçer.

        Pencere kurulurken kısa bir cümle yazıyor, kopyalama başlayınca
        uzun olanı geliyor. Yükseklik kurulumda sabitlenirse uzun cümlenin
        son satırı kırpılıyor (ekran görüntüsüyle görüldü).
        """
        self._status.setText(text)
        # Sarmalı etiketin yüksekliği genişliğe bağlı; layout tek başına
        # bunu hesaplamıyor.
        genislik = self.width() - 2 * SPACING["lg"]
        if genislik > 0:
            self._status.setMinimumHeight(self._status.heightForWidth(genislik))
        self.adjustSize()

    def _on_progress(self, yuzde: int) -> None:
        self._bar.setValue(yuzde)
        self._set_status(self._language.t("update.applying_copy"))

    def _on_finished(self, hata: str) -> None:
        self.error = hata
        if not hata:
            updater.relaunch(self._target)
        self.accept()


def run_apply(target: Path, pid: int) -> int:
    """Yardımcı kipin giriş noktası. Süreç çıkış kodunu döndürüyor."""
    application = QApplication(sys.argv[:1])

    store = ProgressStore(database_path())

    # Dil, uygulamanın kendisiyle aynı kuralla seçiliyor: kullanıcının
    # seçimi varsa o, yoksa bilgisayarın dili (Türkçe değilse İngilizce).
    # Burada `LanguageManager(store)` yazılmıştı ve o **bir dil kodu**
    # bekliyor; store geçersiz sayılıp pencere herkese Türkçe açılıyordu.
    kayitli = store.setting("language", "")
    if kayitli not in AVAILABLE_LANGUAGES:
        kayitli = system_language()
    language = LanguageManager(kayitli)

    theme = ThemeManager(store)
    theme.apply(application)

    pencere = ApplyWindow(language, target, pid)
    pencere.exec()

    hata = pencere.error
    store.close()

    if hata:
        # Sorun çıktıysa eski sürüm yerinde duruyor; kullanıcı onu açmaya
        # devam edebilsin diye eski kurulum yeniden başlatılıyor.
        updater.relaunch(target)
        return 1
    return 0
