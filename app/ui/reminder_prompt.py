"""İlk açılışta çıkan soru: seri hatırlatmaları açılsın mı?

Bildirimler kendiliğinden açılmıyor; Alican kullanıcıya bir kez sorulmasını
ve sistemin nasıl çalıştığının kısaca anlatılmasını istedi. Program
kapalıyken de bildirim gelmesi için Windows Görev Zamanlayıcı'ya görev
ekleniyor; bunu söylemeden yapmak kullanıcının bilgisayarında habersiz bir
değişiklik olurdu.

Cevap ("evet" ya da "hayır") `reminders` ayarına yazılıyor ve soru bir daha
çıkmıyor. Ayarlar › Öğrenme'den her zaman değiştirilebiliyor.
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ..core import reminder_service, reminders
from ..core.language import LanguageManager
from ..resources.theme.tokens import PALETTES, SPACING
from ..widgets.common import DropdownBox

# Seçilebilen saatler: 07:00–23:00, yarım saatte bir.
TIMES = [f"{h:02d}:{m:02d}" for h in range(7, 24) for m in (0, 30) if (h, m) != (23, 30)]


def should_ask(store) -> bool:
    return reminder_service.supported() and not reminders.asked(store)


class ReminderPromptDialog(QDialog):
    """Hatırlatmaları açmayı öneren kutu."""

    def __init__(
        self,
        language: LanguageManager,
        store,
        mode: str = "dark",
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._language = language
        self._store = store
        self.error = ""

        self.setModal(True)
        self.setMinimumWidth(500)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(SPACING["lg"], SPACING["lg"], SPACING["lg"], SPACING["lg"])
        layout.setSpacing(SPACING["md"])

        self._heading = QLabel()
        self._heading.setProperty("role", "title")
        self._heading.setWordWrap(True)
        layout.addWidget(self._heading)

        # Ne olacak, nasıl çalışıyor, nereden değiştirilir: üç kısa paragraf.
        self._body = QLabel()
        self._how = QLabel()
        self._how.setProperty("role", "muted")
        self._settings = QLabel()
        self._settings.setProperty("role", "muted")
        for label in (self._body, self._how, self._settings):
            label.setWordWrap(True)
            layout.addWidget(label)

        time_row = QHBoxLayout()
        self._time_label = QLabel()
        time_row.addWidget(self._time_label)
        self._time = DropdownBox(color=PALETTES.get(mode, PALETTES["dark"])["text_muted"])
        self._time.addItems(TIMES)
        self._time.setCurrentText(reminders.DEFAULT_TIME)
        self._time.setFixedWidth(110)
        time_row.addWidget(self._time)
        time_row.addStretch(1)
        layout.addLayout(time_row)

        layout.addSpacing(SPACING["xs"])

        buttons = QHBoxLayout()
        buttons.addStretch(1)
        self._no = QPushButton()
        self._no.setCursor(Qt.CursorShape.PointingHandCursor)
        self._no.clicked.connect(self._decline)
        buttons.addWidget(self._no)

        self._yes = QPushButton()
        self._yes.setProperty("variant", "primary")
        self._yes.setCursor(Qt.CursorShape.PointingHandCursor)
        self._yes.clicked.connect(self._accept)
        self._yes.setDefault(True)
        buttons.addWidget(self._yes)
        layout.addLayout(buttons)

        self.retranslate()

    def _accept(self) -> None:
        ok, error = reminder_service.enable(self._store, self._time.currentText())
        self.error = "" if ok else error
        self.accept()

    def _decline(self) -> None:
        reminder_service.decline(self._store)
        self.reject()

    def reject(self) -> None:  # noqa: D102 - pencere çarpıyla kapanırsa da "hayır"
        if not reminders.asked(self._store):
            reminder_service.decline(self._store)
        super().reject()

    def retranslate(self) -> None:
        t = self._language.t
        self.setWindowTitle(t("reminder.prompt_title"))
        self._heading.setText(t("reminder.prompt_heading"))
        self._body.setText(t("reminder.prompt_body"))
        self._how.setText(t("reminder.prompt_how"))
        self._settings.setText(t("reminder.prompt_settings"))
        self._time_label.setText(t("reminder.time_label"))
        self._yes.setText(t("reminder.prompt_yes"))
        self._no.setText(t("reminder.prompt_no"))
