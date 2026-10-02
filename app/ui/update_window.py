"""Güncellemeyi indiren pencere.

Önceki indirme kutusu (0.8.3) masaüstünü kilitliyordu (GitHub #15): Alt+Tab
ve görev çubuğu cevap vermiyordu. Kutu başlık çubuğu olmayan, küçültülemeyen
bir kip pencereydi ve indirmenin her parçasında (256 KB; hızlı bağlantıda
saniyede onlarca kez) yazısını değiştirip kendini yeniden boyutluyordu.
Bu pencere:

- **Sıradan bir pencere:** başlık çubuğu, küçültme düğmesi, görev
  çubuğunda kendi yeri var; Alt+Tab ile başka pencereye geçiliyor. Kip
  değil: indirme sürerken Odyssey kullanılmaya devam edilebiliyor.
  "Arka planda sürsün" pencereyi küçültüyor.
- **Sabit boyutlu** ve ilerlemeyi saniyede en fazla on kez yazıyor.
- İlerleme satırı: yüzde, inen / toplam MB, hız, kalan süre. Başlıkta da
  yüzde var; pencere küçültülmüşken görev çubuğunda okunuyor.

Üstte açılış animasyonunun sahnesi: indirme sürerken sentor koşuyor;
indirme ve denetim bitince okunu atıyor, ok hedefe saplanınca kurulum
başlıyor. Kurulum programı pencere açmadan çalışıyor (`/VERYSILENT`), yeni
sürüm açılış animasyonuyla açılıyor.

İptal yarım dosyayı da siliyor. Kurulum bu pencerede yapılmıyor; uygulama
kapandıktan sonra kurulum programı yapıyor.
"""

from __future__ import annotations

import time
import webbrowser
from pathlib import Path

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QSizePolicy, QVBoxLayout, QWidget

from ..core import log, updater
from ..core.language import LanguageManager
from ..core.updater import Asset
from ..core.updates import UpdateInfo
from ..paths import updates_dir
from ..resources.theme.tokens import FONTS, SPACING
from ..widgets.progress_bar import ProgressBar
from .update_scene import UpdateScene

# Kurulum başlamadıysa sebebe göre metin; listede olmayan her hata indirme hatası.
ERROR_TEXTS = {
    "blocked": "update.blocked_by_windows",
    "start": "update.start_failed",
}

MB = 1024 * 1024
# İlerleme en fazla bu aralıkla yazılıyor (sn).
PROGRESS_INTERVAL = 0.1
WIDTH = 560


class DownloadWorker(QThread):
    """İndirme ve denetleme işini arka planda yapıyor."""

    # inen bayt, toplam bayt, bayt/sn
    progress = Signal(int, int, float)
    verifying = Signal()
    # başarılıysa indirilen kurulum dosyası, değilse None ve hata anahtarı
    finished_with = Signal(object, str)

    def __init__(self, asset: Asset, parent=None) -> None:
        super().__init__(parent)
        self._asset = asset
        self._cancelled = False

    def cancel(self) -> None:
        self._cancelled = True

    def run(self) -> None:  # noqa: D102
        hedef = updates_dir() / self._asset.name
        basla = time.monotonic()
        son = [0.0]

        def inerken(inen: int, toplam: int) -> None:
            simdi = time.monotonic()
            # Seyrek yazılıyor: her parçada yazmak arayüzü mesaja boğuyordu.
            if simdi - son[0] < PROGRESS_INTERVAL and inen < toplam:
                return
            son[0] = simdi
            gecen = max(0.001, simdi - basla)
            self.progress.emit(inen, toplam, inen / gecen)

        hata = updater.download(self._asset, hedef, inerken, lambda: self._cancelled)
        if hata:
            self.finished_with.emit(None, hata)
            return

        self.verifying.emit()
        hata = updater.verify_installer(hedef, self._asset.size)
        if hata:
            hedef.unlink(missing_ok=True)
            self.finished_with.emit(None, hata)
            return
        self.finished_with.emit(hedef, "")


def _mb(value: float, language: str) -> str:
    metin = f"{value / MB:.1f}"
    return metin.replace(".", ",") if language == "tr" else metin


def _duration(seconds: float, t) -> str:
    seconds = max(1, round(seconds))
    if seconds < 60:
        return t("update.seconds", n=seconds)
    return t("update.minutes", n=(seconds + 30) // 60)


class UpdateWindow(QWidget):
    """İndirme penceresi; iş bitince `ready(kurulum dosyası)` yayıyor."""

    ready = Signal(object)

    def __init__(self, language: LanguageManager, info: UpdateInfo, asset: Asset) -> None:
        super().__init__(None)
        self._language = language
        self._info = info
        self._asset = asset
        self._state = "download"   # download · verify · done · error
        self._staged: Path | None = None
        self._percent = 0

        # Sıradan pencere: küçültülür, görev çubuğunda durur, Alt+Tab'da
        # görünür. Büyütme yok (içerik sabit boyutlu).
        self.setWindowFlags(
            Qt.WindowType.Window
            | Qt.WindowType.WindowTitleHint
            | Qt.WindowType.WindowSystemMenuHint
            | Qt.WindowType.WindowMinimizeButtonHint
            | Qt.WindowType.WindowCloseButtonHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(SPACING["lg"], SPACING["lg"], SPACING["lg"], SPACING["lg"])
        layout.setSpacing(0)

        self._scene = UpdateScene("run")
        self._scene.setFixedHeight(190)
        self._scene.finished.connect(self._on_shot)
        layout.addWidget(self._scene)
        layout.addSpacing(SPACING["lg"])

        # Tek satır: sarma açıkken pencere ölçülürken yüksekliği şişiyordu.
        self._heading = QLabel()
        self._heading.setProperty("role", "title")
        self._heading.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        layout.addWidget(self._heading)
        layout.addSpacing(SPACING["md"])

        satir = QHBoxLayout()
        satir.setSpacing(SPACING["sm"])
        self._percent_label = QLabel("")
        self._percent_label.setStyleSheet(
            f"font-family: {FONTS['display']}; font-size: 26px; font-weight: 700;"
        )
        satir.addWidget(self._percent_label, 0, Qt.AlignmentFlag.AlignBottom)
        satir.addStretch(1)
        self._detail = QLabel("")
        self._detail.setProperty("role", "muted")
        satir.addWidget(self._detail, 0, Qt.AlignmentFlag.AlignBottom)
        layout.addLayout(satir)
        layout.addSpacing(SPACING["sm"])

        from ..widgets.effects import theme_mode

        self._bar = ProgressBar()
        self._bar.set_mode(theme_mode())
        layout.addWidget(self._bar)
        layout.addSpacing(SPACING["sm"])

        self._status = QLabel("")
        self._status.setProperty("role", "muted")
        self._status.setWordWrap(True)
        # İki satırlık sabit yer: aşamalar arasında yazının uzunluğu değişiyor,
        # pencere oynamasın.
        self._status.setFixedHeight(44)
        self._status.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self._status)
        layout.addStretch(1)
        layout.addSpacing(SPACING["sm"])

        dugmeler = QHBoxLayout()
        dugmeler.setSpacing(SPACING["sm"])
        self._page_button = QPushButton()
        self._page_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._page_button.clicked.connect(self._open_page)
        self._page_button.hide()
        dugmeler.addWidget(self._page_button)
        dugmeler.addStretch(1)
        self._background_button = QPushButton()
        self._background_button.setProperty("variant", "ghost")
        self._background_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._background_button.clicked.connect(self.showMinimized)
        dugmeler.addWidget(self._background_button)
        self._cancel_button = QPushButton()
        self._cancel_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._cancel_button.clicked.connect(self.close)
        dugmeler.addWidget(self._cancel_button)
        layout.addLayout(dugmeler)

        self._worker = DownloadWorker(asset, self)
        self._worker.progress.connect(self._on_progress)
        self._worker.verifying.connect(self._on_verifying)
        self._worker.finished_with.connect(self._on_finished)

        self.setFixedWidth(WIDTH)
        self.retranslate()
        self.adjustSize()
        self.setFixedSize(self.size())

    # --- akış --------------------------------------------------------------------------

    def start(self) -> None:
        self.show()
        if not self._worker.isRunning():
            self._worker.start()

    def _on_progress(self, inen: int, toplam: int, hiz: float) -> None:
        t, dil = self._language.t, self._language.language
        yuzde = int(inen * 100 / toplam) if toplam else 0
        self._percent = yuzde
        self._percent_label.setText(t("home.percent", value=yuzde))
        self._bar.set_percent(yuzde, animate=False)
        parca = [t("update.size", done=_mb(inen, dil), total=_mb(toplam, dil))]
        if hiz > 0:
            parca.append(t("update.speed", speed=_mb(hiz, dil)))
            if toplam > inen:
                parca.append(t("update.remaining", time=_duration((toplam - inen) / hiz, t)))
        self._detail.setText("  ·  ".join(parca))
        self._render_title()

    def _on_verifying(self) -> None:
        self._state = "verify"
        self._bar.set_percent(100, animate=False)
        self._percent_label.setText(self._language.t("home.percent", value=100))
        self._status.setText(self._language.t("update.stage_verify"))
        self._render_title()

    def _on_finished(self, staged, hata: str) -> None:
        if hata:
            if hata == "cancelled":
                return
            log.get(__name__).warning("Güncelleme tamamlanamadı: %s", hata)
            self._state = "error"
            self._scene.set_mode("idle")
            self._heading.setText(self._language.t("update.failed_heading"))
            self._status.setText(self._language.t(ERROR_TEXTS.get(hata, "update.download_failed")))
            if hata in ERROR_TEXTS:
                # İndirme bitmişti, sorun kurulumda: yüzde ve çubuk bir şey
                # söylemiyor. Yerlerini açıklama alıyor (üç satıra sığmıyordu).
                for parca in (self._percent_label, self._detail, self._bar):
                    parca.hide()
                self._status.setFixedHeight(88)
            self._detail.setText("")
            self._page_button.show()
            self._background_button.hide()
            self._cancel_button.show()
            self._cancel_button.setEnabled(True)
            self._cancel_button.setText(self._language.t("update.close"))
            self._render_title()
            return
        # Hazır: sentor okunu atıyor, ok saplanınca kurulum başlıyor.
        self._state = "done"
        self._staged = staged
        self._heading.setText(self._language.t("update.ready_heading", version=self._info.version))
        self._status.setText(self._language.t("update.installing"))
        self._background_button.hide()
        self._cancel_button.hide()
        self._render_title()
        if self.isMinimized():
            self.showNormal()
        self._scene.shoot()

    def _on_shot(self) -> None:
        if self._staged is not None:
            self.ready.emit(self._staged)

    def show_error(self, key: str) -> None:
        """Kurulum programı başlatılamadıysa (çağıran söylüyor)."""
        self._on_finished(None, key)

    def release(self) -> None:
        """Kurulum başladı, uygulama kapanıyor: pencere artık kapanmayı
        reddetmiyor. Qt 6'da `quit()` önce pencereleri kapatıyor; reddeden
        bir pencere çıkışı durdururdu."""
        self._state = "installing"

    def _open_page(self) -> None:
        webbrowser.open(self._info.url)
        self.close()

    def closeEvent(self, event) -> None:  # noqa: N802
        # Kapatmak indirmeyi iptal etmek demek; kurulum başladıktan sonra
        # kapanmıyor (uygulama zaten kendisi kapanacak).
        if self._state == "done":
            event.ignore()
            return
        if self._worker.isRunning():
            self._worker.cancel()
            self._worker.wait(3000)
        super().closeEvent(event)

    # --- metinler ----------------------------------------------------------------------

    def _render_title(self) -> None:
        t = self._language.t
        ad = t("update.window_title", version=self._info.version)
        if self._state == "download" and self._percent:
            ad = f"{t('home.percent', value=self._percent)} · {ad}"
        self.setWindowTitle(ad)

    def retranslate(self) -> None:
        t = self._language.t
        self._heading.setText(t("update.downloading_heading", version=self._info.version))
        if self._state == "download":
            self._status.setText(t("update.download_note"))
            self._percent_label.setText(t("home.percent", value=self._percent))
        self._background_button.setText(t("update.background"))
        self._cancel_button.setText(t("update.cancel"))
        self._page_button.setText(t("update.notice_open"))
        self._render_title()
