"""Güncellemeyi indiren ve kuran pencere.

Üç aşama tek pencerede: **indiriliyor**, **denetleniyor**, **hazırlanıyor**.
Her aşamada çubuk ve altındaki satır ne olduğunu söylüyor; 280 MB'lık bir
indirmede "lütfen bekleyin" yazan bir pencere, donmuş bir pencereden ayırt
edilemiyor.

İndirme iptal edilebiliyor. İptal, yarım dosyayı da siliyor: bir sonraki
denemede yarım kalmış bir arşivin üstüne yazılmıyor.

Kurulum bu pencerede **yapılmıyor**. Pencere yalnızca indirip açıyor;
dosyaların değişmesi uygulama kapandıktan sonra, `updater.apply_update`
tarafından yapılıyor.
"""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ..core import updater
from ..core.language import LanguageManager
from ..core.updater import Asset
from ..core.updates import UpdateInfo
from ..paths import updates_dir
from ..resources.theme.tokens import SPACING

MB = 1024 * 1024


class DownloadWorker(QThread):
    """İndirme ve açma işini arka planda yapıyor."""

    # aşama anahtarı, ilerleme (0-100), ek bilgi
    progress = Signal(str, int, str)
    # başarılıysa açılan klasör, değilse boş metin ve hata anahtarı
    finished_with = Signal(object, str)

    def __init__(self, asset: Asset, parent=None) -> None:
        super().__init__(parent)
        self._asset = asset
        self._cancelled = False

    def cancel(self) -> None:
        self._cancelled = True

    def _iptal(self) -> bool:
        return self._cancelled

    def run(self) -> None:  # noqa: D102
        hedef = updates_dir() / self._asset.name

        def inerken(inen: int, toplam: int) -> None:
            yuzde = int(inen * 100 / toplam) if toplam else 0
            self.progress.emit(
                "download", yuzde, f"{inen / MB:.0f} / {toplam / MB:.0f} MB"
            )

        hata = updater.download(self._asset, hedef, inerken, self._iptal)
        if hata:
            self.finished_with.emit(None, hata)
            return

        self.progress.emit("verify", 0, "")
        hata = updater.verify(hedef, self._asset.size)
        if hata:
            hedef.unlink(missing_ok=True)
            self.finished_with.emit(None, hata)
            return

        def acilirken(sira: int, toplam: int) -> None:
            self.progress.emit("extract", int(sira * 100 / toplam) if toplam else 0, "")

        acilan = updater.extract(
            hedef, updates_dir() / "staged", acilirken, self._iptal
        )
        # Arşiv açıldıktan sonra gereksiz: 280 MB yer kaplıyor.
        hedef.unlink(missing_ok=True)

        if acilan is None:
            self.finished_with.emit(None, "cancelled" if self._cancelled else "extract")
            return

        self.finished_with.emit(acilan, "")


class UpdateProgressDialog(QDialog):
    """İndirme penceresi. Kapanırken sonucu `staged` alanında bırakıyor."""

    def __init__(
        self,
        language: LanguageManager,
        info: UpdateInfo,
        asset: Asset,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._language = language
        self._info = info
        self.staged: Path | None = None
        self.error = ""

        self.setModal(True)
        self.setMinimumWidth(460)
        # Kapatma düğmesi yok: iş yarıdayken pencerenin kaybolması,
        # arkada ne olduğu belirsiz bir indirme bırakırdı. İptal düğmesi
        # var ve o, indirmeyi gerçekten durduruyor.
        self.setWindowFlags(
            Qt.WindowType.Dialog | Qt.WindowType.CustomizeWindowHint
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            SPACING["lg"], SPACING["lg"], SPACING["lg"], SPACING["lg"]
        )
        layout.setSpacing(SPACING["md"])

        self._heading = QLabel()
        self._heading.setProperty("role", "title")
        self._heading.setWordWrap(True)
        layout.addWidget(self._heading)

        self._bar = QProgressBar()
        self._bar.setRange(0, 100)
        self._bar.setTextVisible(False)
        layout.addWidget(self._bar)

        self._status = QLabel()
        self._status.setProperty("role", "muted")
        self._status.setWordWrap(True)
        layout.addWidget(self._status)

        buttons = QHBoxLayout()
        buttons.addStretch(1)
        self._cancel_button = QPushButton()
        self._cancel_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._cancel_button.clicked.connect(self._cancel)
        buttons.addWidget(self._cancel_button)
        layout.addLayout(buttons)

        self._worker = DownloadWorker(asset, self)
        self._worker.progress.connect(self._on_progress)
        self._worker.finished_with.connect(self._on_finished)

        self.retranslate()
        self._on_progress("download", 0, "")

    def showEvent(self, event) -> None:  # noqa: N802
        super().showEvent(event)
        if not self._worker.isRunning():
            self._worker.start()

    def _cancel(self) -> None:
        self._worker.cancel()
        self._cancel_button.setEnabled(False)
        self._set_status(self._language.t("update.cancelling"))

    def _on_progress(self, asama: str, yuzde: int, ek: str) -> None:
        self._bar.setValue(yuzde)
        metin = self._language.t(f"update.stage_{asama}")
        self._set_status(f"{metin}  {ek}".strip())

    def _set_status(self, text: str) -> None:
        """Durum satırını yazar ve pencereyi yeniden ölçer.

        Aşamalar arasında metnin uzunluğu değişiyor; sabit yükseklikte
        uzun olanın son satırı kırpılıyor.
        """
        self._status.setText(text)
        genislik = self.width() - 2 * SPACING["lg"]
        if genislik > 0:
            self._status.setMinimumHeight(self._status.heightForWidth(genislik))
        self.adjustSize()

    def _on_finished(self, staged, hata: str) -> None:
        self.staged = staged
        self.error = hata
        if hata:
            self.reject()
        else:
            self.accept()

    def retranslate(self) -> None:
        t = self._language.t
        self.setWindowTitle(t("update.notice_title"))
        self._heading.setText(
            t("update.downloading_heading", version=self._info.version)
        )
        self._cancel_button.setText(t("update.cancel"))
