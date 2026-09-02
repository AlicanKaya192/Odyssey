"""Ayarlar penceresi.

Seçimler anında uygulanır — kaydet düğmesine basıp uygulamayı yeniden
başlatmak gerekmiyor.

**Neden açılır kutu değil de anahtar?** Önce dil ve tema birer `QComboBox`
idi. Ayar sayısı ikiden fazlaya çıkınca bu düzen dağıldı: her satırda
kapalı bir kutu duruyor, kutunun içindeki değeri görmek için tıklamak
gerekiyor ve iki seçenekli bir ayar için bu fazladan bir adım. Şimdi her
ayar tek bakışta okunuyor: solda adı ve ne işe yaradığı, sağda açık mı
kapalı mı olduğunu konumuyla gösteren bir anahtar.

Ayarlar gruplara ayrıldı; hepsi tek listede olunca hangisinin görünümle
hangisinin öğrenmeyle ilgili olduğu ayırt edilmiyordu.
"""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ..core.language import LanguageManager
from ..core.quiz_timing import UNTIMED_QUIZ_KEY, untimed_quiz
from ..core.unlock import UNLOCK_ALL_KEY, unlock_all
from ..core.theme import ThemeManager
from ..core import updates
from .update_check import UpdateWorker
from ..resources.theme.tokens import PALETTES, SPACING
from ..widgets.segmented import SegmentedControl
from ..widgets.toggle_switch import ToggleSwitch
from . import modal

# Kilit ve süre ayarlarının veritabanındaki anahtarları.

# Dil bir aç/kapa ayarı değil, iki seçenek arasında seçim. Anahtar
# kullanıldığında hangi tarafın hangi dil olduğu ancak açıklamayı okuyunca
# anlaşılıyordu; artık iki seçenek de ekranda yazılı.
LANGUAGE_OPTIONS = [("tr", "TR"), ("en", "EN")]

# Tema seçicisi: yazı yerine simge. Ay koyu, güneş açık tema.
#
# Önce aç/kapa anahtarıydı ama anahtar iki durumlu bir **ayar** için doğru
# bileşen, iki seçenek arasında **seçim** için değil: "kapalı"nın koyu tema
# demek olduğu ancak açıklamayı okuyunca anlaşılıyordu. Dil seçicisiyle
# aynı bileşen kullanılıyor.
THEME_OPTIONS = [("dark", "", "moon"), ("light", "", "sun")]


class SettingRow(QWidget):
    """Bir ayar satırı: solda ad ve açıklama, sağda denetim.

    Denetim varsayılan olarak bir anahtar; `control` verilirse onun yerine
    o yerleştiriliyor (dil satırındaki segment seçici gibi).
    """

    def __init__(
        self, control: QWidget | None = None, parent: QWidget | None = None
    ) -> None:
        super().__init__(parent)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, SPACING["sm"], 0, SPACING["sm"])
        layout.setSpacing(SPACING["md"])

        metinler = QVBoxLayout()
        metinler.setSpacing(2)
        self.title = QLabel()
        self.title.setProperty("role", "heading")
        self.description = QLabel()
        self.description.setProperty("role", "muted")
        self.description.setWordWrap(True)
        metinler.addWidget(self.title)
        metinler.addWidget(self.description)

        layout.addLayout(metinler, 1)

        self.switch = control if control is not None else ToggleSwitch()
        # Denetim metnin ilk satırıyla hizalanıyor; açıklama uzayınca
        # ortalanmış bir denetim aşağı kayıp başlıktan kopuyordu.
        layout.addWidget(self.switch, 0, Qt.AlignmentFlag.AlignTop)


class SettingsDialog(QDialog):
    """Görünüm ve öğrenme ayarları."""

    # Kilit ayarı değişince ekranların o an yenilenmesi gerekiyor; yoksa
    # açık olan bölüm ekranı eski kilit durumunu göstermeye devam ediyor
    # ve kullanıcı çıkıp girmeden fark görmüyordu.
    lock_changed = Signal()
    # Sınav süresi ayarı: açık bir sınav varken de o an uygulanıyor.
    timing_changed = Signal()
    # Elle yapılan denetimin sonucu: şeritteki duyuruyu da güncelliyor.
    update_found = Signal(object)

    def __init__(
        self,
        language: LanguageManager,
        theme: ThemeManager,
        store,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._language = language
        self._theme = theme
        self._store = store
        self._worker: UpdateWorker | None = None

        modal.prepare(self)
        self.setMinimumWidth(460)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            SPACING["lg"], SPACING["lg"], SPACING["lg"], SPACING["lg"]
        )
        layout.setSpacing(SPACING["md"])

        # --- görünüm ------------------------------------------------------
        self._appearance_title = QLabel()
        self._appearance_title.setProperty("role", "section")
        layout.addWidget(self._appearance_title)

        self._theme_picker = SegmentedControl(THEME_OPTIONS)
        self._theme_picker.selected.connect(self._on_theme)
        self._theme_row = SettingRow(self._theme_picker)
        layout.addWidget(self._theme_row)

        self._language_picker = SegmentedControl(LANGUAGE_OPTIONS)
        self._language_picker.selected.connect(self._on_language)
        self._language_row = SettingRow(self._language_picker)
        layout.addWidget(self._language_row)

        layout.addWidget(self._separator())

        # --- öğrenme ------------------------------------------------------
        self._learning_title = QLabel()
        self._learning_title.setProperty("role", "section")
        layout.addWidget(self._learning_title)

        self._unlock_row = SettingRow()
        self._unlock_row.switch.toggled.connect(self._on_unlock)
        layout.addWidget(self._unlock_row)

        self._untimed_row = SettingRow()
        self._untimed_row.switch.toggled.connect(self._on_untimed)
        layout.addWidget(self._untimed_row)

        layout.addWidget(self._separator())

        # --- güncelleme ---------------------------------------------------
        self._update_title = QLabel()
        self._update_title.setProperty("role", "section")
        layout.addWidget(self._update_title)

        self._update_row = SettingRow()
        self._update_row.switch.toggled.connect(self._on_update_check)
        layout.addWidget(self._update_row)

        update_bar = QHBoxLayout()
        update_bar.setSpacing(SPACING["sm"])
        self._check_button = QPushButton()
        self._check_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._check_button.clicked.connect(self._check_now)
        update_bar.addWidget(self._check_button)
        self._update_status = QLabel()
        self._update_status.setProperty("role", "muted")
        self._update_status.setWordWrap(True)
        update_bar.addWidget(self._update_status, 1)
        layout.addLayout(update_bar)

        layout.addSpacing(SPACING["sm"])

        buttons = QHBoxLayout()
        buttons.addStretch(1)
        self._close_button = QPushButton()
        self._close_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._close_button.setProperty("variant", "primary")
        self._close_button.clicked.connect(self.accept)
        buttons.addWidget(self._close_button)
        layout.addLayout(buttons)

        self._load_state()
        self._paint_switches(self._theme.effective_mode)
        self.retranslate()

        # Odak kapatma düğmesinde başlıyor. Varsayılan haliyle ilk anahtara
        # gidiyor ve etrafındaki odak halkası, o ayar seçiliymiş gibi
        # duruyordu.
        self._close_button.setFocus()

        # Tema bu pencereden değiştiriliyor; anahtarların ve simgelerin
        # renkleri elle veriliyor, değişimi dinleyip yeniliyoruz.
        theme.theme_changed.connect(self._on_theme_changed)

        modal.freeze(self)

    def showEvent(self, event) -> None:  # noqa: N802
        super().showEvent(event)
        modal.center(self)

    def _separator(self) -> QFrame:
        line = QFrame()
        # Şekil **verilmiyor**: `HLine` seçilince Qt çerçeveyi kendi
        # çiziyor ve QSS'teki arka plan rengi ekrana hiç çıkmıyordu.
        line.setFrameShape(QFrame.Shape.NoFrame)
        line.setFixedHeight(1)
        line.setProperty("role", "divider")
        return line

    # --- durum ------------------------------------------------------------

    def _load_state(self) -> None:
        """Kayıtlı değerleri anahtarlara yerleştirir.

        `set_checked` sinyal yaymadığı için bu, ayarları yeniden yazmıyor.
        """
        self._theme_picker.set_value(self._theme.effective_mode)
        self._language_picker.set_value(self._language.language)
        self._unlock_row.switch.set_checked(
            unlock_all(self._store), animate=False
        )
        self._untimed_row.switch.set_checked(
            untimed_quiz(self._store), animate=False
        )
        self._update_row.switch.set_checked(
            updates.enabled(self._store), animate=False
        )

    def _paint_switches(self, mode: str) -> None:
        p = PALETTES.get(mode, PALETTES["light"])
        # Segment düğmelerinin **zeminini** QSS veriyor ama içlerindeki
        # güneş/ay birer `QIcon`; onlara QSS ulaşmıyor.
        self._theme_picker.set_icon_colors(p["text_muted"], p["text_inverse"])
        for row in (self._unlock_row, self._untimed_row, self._update_row):
            row.switch.set_colors(
                track_off=p["surface_alt"],
                track_on=p["accent"],
                knob=p["surface"] if mode == "dark" else "#FFFFFF",
                border=p["border_strong"],
            )

    # --- olaylar ----------------------------------------------------------

    def _on_theme_changed(self, mode: str) -> None:
        # Pencerenin çerçevesi yok; boyanacak başlık çubuğu da yok.
        self._paint_switches(self._theme.effective_mode)

    def _on_theme(self, mode: str) -> None:
        self._theme.set_mode(mode)

    def _on_language(self, code: str) -> None:
        self._language.set_language(code)

    def _on_unlock(self, checked: bool) -> None:
        self._store.set_setting(UNLOCK_ALL_KEY, "1" if checked else "")
        self.lock_changed.emit()

    def _on_untimed(self, checked: bool) -> None:
        self._store.set_setting(UNTIMED_QUIZ_KEY, "1" if checked else "")
        self.timing_changed.emit()

    def _on_update_check(self, checked: bool) -> None:
        updates.set_enabled(self._store, checked)
        self._check_button.setEnabled(checked)
        if not checked:
            self._set_status("")

    # --- güncelleme -------------------------------------------------------

    def _check_now(self) -> None:
        """Elle denetim: "bugün zaten baktım" kuralını atlıyor."""
        if self._worker is not None and self._worker.isRunning():
            return
        if not updates.should_check(self._store, ignore_interval=True):
            return
        self._check_button.setEnabled(False)
        self._set_status(self._language.t("update.checking"))

        self._worker = UpdateWorker(parent=self)
        self._worker.finished_with.connect(self._on_checked)
        self._worker.start()

    def _on_checked(self, info) -> None:
        updates.record(self._store, info)
        self._check_button.setEnabled(updates.enabled(self._store))
        t = self._language.t
        if info.status == "newer":
            self._set_status(t("update.available", version=info.version))
        elif info.status == "current":
            self._set_status(t("update.current"))
        elif info.status == "offline":
            self._set_status(t("update.offline"))
        else:
            self._set_status(t("update.failed"))
        self.update_found.emit(info)

    def _set_status(self, text: str) -> None:
        """Durum satırını yazar ve pencereyi yeniden ölçer.

        Pencere sabit boyutlu; satır uzayınca yazı kırpılıyordu.
        """
        self._update_status.setText(text)
        modal.refit(self)

    # --- metinler ---------------------------------------------------------

    def retranslate(self) -> None:
        t = self._language.t
        self.setWindowTitle(t("settings.title"))
        self._close_button.setText(t("common.close"))

        self._appearance_title.setText(t("settings.group_appearance"))
        self._learning_title.setText(t("settings.group_learning"))

        self._theme_row.title.setText(t("settings.theme"))
        self._theme_row.description.setText(t("settings.theme_help"))
        self._theme_picker.set_tooltips({
            "dark": t("settings.theme_dark"),
            "light": t("settings.theme_light"),
        })

        self._language_row.title.setText(t("settings.language"))
        self._language_row.description.setText(t("settings.language_help"))

        self._unlock_row.title.setText(t("settings.unlock_all"))
        self._unlock_row.description.setText(t("settings.unlock_all_help"))

        self._untimed_row.title.setText(t("settings.untimed_quiz"))
        self._untimed_row.description.setText(t("settings.untimed_quiz_help"))

        self._update_title.setText(t("settings.group_updates"))
        self._update_row.title.setText(t("settings.update_check"))
        self._update_row.description.setText(t("settings.update_check_help"))
        self._check_button.setText(t("update.check_now"))
        self._check_button.setEnabled(updates.enabled(self._store))
