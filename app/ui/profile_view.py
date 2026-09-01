"""Profil ekranı.

Ad, soyad ve istatistikler. Bütün bilgiler kullanıcının kendi bilgisayarında,
`%APPDATA%\\Odyssey\\progress.db` içinde duruyor — sunucu yok, hesap yok,
hiçbir veri dışarı çıkmıyor.

Rozet duvarı bu ekrana M4 aşamasında eklenecek.
"""

from __future__ import annotations

from PySide6.QtCore import QTimer, Qt, Signal
from PySide6.QtWidgets import (
    QFileDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from ..core.avatar import IMAGE_SUFFIXES, clear_avatar, has_avatar, load_avatar, save_avatar
from ..core.catalog import Catalog
from ..core.language import LanguageManager
from ..core.progress import ProgressStore
from ..resources.theme.tokens import PALETTES, READING_WIDTH, SPACING
from ..widgets.avatar import AvatarView
from ..widgets.common import Card, StatBlock, section_label
from ..widgets.effects import repolish

STAT_KEYS = ("progress", "sections", "exercises", "quiz_average", "streak")

# Profil ekranındaki fotoğrafın çapı.
AVATAR_SIZE = 96


class ProfileView(QWidget):
    """Kullanıcının profili ve ilerleme özeti."""

    saved = Signal()

    def __init__(
        self,
        catalog: Catalog,
        language: LanguageManager,
        store: ProgressStore,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._catalog = catalog
        self._language = language
        self._store = store
        self._mode = "light"

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        container = QWidget()
        row = QHBoxLayout(container)
        row.setContentsMargins(
            SPACING["xl"], SPACING["xl"], SPACING["xl"], SPACING["xxl"]
        )
        row.addStretch(1)

        column = QWidget()
        column.setMaximumWidth(READING_WIDTH + 80)
        column.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self._column = QVBoxLayout(column)
        self._column.setContentsMargins(0, 0, 0, 0)
        self._column.setSpacing(SPACING["lg"])

        self._column.addWidget(self._build_identity())
        self._column.addWidget(self._build_stats())
        self._column.addStretch(1)

        row.addWidget(column, 8)
        row.addStretch(1)
        scroll.setWidget(container)
        layout.addWidget(scroll)

        self.refresh()

    def _build_identity(self) -> QWidget:
        card = Card(mode=self._mode, padding=SPACING["lg"])
        self._identity_card = card

        self._identity_title = QLabel()
        self._identity_title.setProperty("role", "subtitle")
        card.body.addWidget(self._identity_title)

        self._identity_help = QLabel()
        self._identity_help.setProperty("role", "muted")
        self._identity_help.setWordWrap(True)
        card.body.addWidget(self._identity_help)
        card.body.addSpacing(SPACING["md"])

        # Fotoğraf solda, ad alanları sağda. Fotoğrafı ad alanlarının altına
        # koymak kartı gereksiz uzatıyordu; ikisi aynı satırda "kimlik"
        # bilgisi olarak birlikte okunuyor.
        kimlik = QHBoxLayout()
        kimlik.setSpacing(SPACING["lg"])

        self._avatar = AvatarView(AVATAR_SIZE)
        self._avatar.clicked.connect(self._choose_photo)
        kimlik.addWidget(self._avatar, 0, Qt.AlignmentFlag.AlignTop)

        sag = QVBoxLayout()
        sag.setSpacing(SPACING["sm"])

        fields = QHBoxLayout()
        fields.setSpacing(SPACING["sm"])

        self._first_name = QLineEdit()
        self._last_name = QLineEdit()
        fields.addWidget(self._first_name)
        fields.addWidget(self._last_name)
        sag.addLayout(fields)

        foto = QHBoxLayout()
        foto.setSpacing(SPACING["sm"])
        self._photo_button = QPushButton()
        self._photo_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._photo_button.clicked.connect(self._choose_photo)
        foto.addWidget(self._photo_button)

        self._photo_clear = QPushButton()
        self._photo_clear.setProperty("variant", "ghost")
        self._photo_clear.setCursor(Qt.CursorShape.PointingHandCursor)
        self._photo_clear.clicked.connect(self._remove_photo)
        foto.addWidget(self._photo_clear)
        foto.addStretch(1)
        sag.addLayout(foto)
        sag.addStretch(1)

        kimlik.addLayout(sag, 1)
        card.body.addLayout(kimlik)

        buttons = QHBoxLayout()

        # Kaydedildi bilgisi düğmenin yanında beliriyor. Hiçbir geri bildirim
        # vermeyince kullanıcı kaydın işleyip işlemediğini anlayamıyordu.
        self._saved_note = QLabel()
        self._saved_note.setProperty("tone", "success")
        self._saved_note.hide()
        buttons.addWidget(self._saved_note)

        buttons.addStretch(1)
        self._save_button = QPushButton()
        self._save_button.setProperty("variant", "primary")
        self._save_button.clicked.connect(self._save)
        buttons.addWidget(self._save_button)
        card.body.addLayout(buttons)

        self._started = QLabel()
        self._started.setProperty("role", "muted")
        card.body.addWidget(self._started)

        return card

    def _build_stats(self) -> QWidget:
        holder = QWidget()
        layout = QVBoxLayout(holder)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(SPACING["sm"])

        self._stats_title = section_label("")
        layout.addWidget(self._stats_title)

        card = Card(mode=self._mode, padding=SPACING["lg"])
        self._stats_card = card

        grid = QGridLayout()
        grid.setSpacing(SPACING["lg"])
        self._stats = {key: StatBlock("—", "") for key in STAT_KEYS}
        for index, key in enumerate(STAT_KEYS):
            grid.addWidget(self._stats[key], index // 3, index % 3)
        card.body.addLayout(grid)

        layout.addWidget(card)
        return holder

    # --- veri -------------------------------------------------------------

    def refresh(self) -> None:
        profile = self._store.profile()
        self._first_name.setText(profile.get("first_name", ""))
        self._last_name.setText(profile.get("last_name", ""))

        self._refresh_avatar()

        started = profile.get("started_at", "")
        self._started.setText(
            self._language.t("profile.member_since", date=started[:10]) if started else ""
        )

        total = 0
        completed = 0
        for chapter in self._catalog.chapters:
            for section in chapter.sections:
                total += 1
                state = self._store.section_state(
                    chapter.id, section.id, len(section.exercises)
                )
                if state.status(section.requires_quiz, section.requires_exercises) == "completed":
                    completed += 1

        average = self._store.quiz_average()
        values = {
            "progress": f"%{round(completed * 100 / total) if total else 0}",
            "sections": str(completed),
            "exercises": str(self._store.solved_exercise_count()),
            "quiz_average": f"{average}" if average is not None else "—",
            "streak": str(self._store.streak()),
        }
        for key, value in values.items():
            self._stats[key].set_value(value)

        self.retranslate()

    def _save(self) -> None:
        self._store.set_profile(
            self._first_name.text().strip(), self._last_name.text().strip()
        )
        self._show_saved()
        self.saved.emit()

    # --- fotoğraf ---------------------------------------------------------

    def _refresh_avatar(self) -> None:
        """Fotoğrafı, baş harfleri ve düğme yazılarını günceller."""
        profile = self._store.profile()
        harfler = "".join(
            part[:1]
            for part in (profile.get("first_name", ""), profile.get("last_name", ""))
            if part
        )
        self._avatar.set_initials(harfler)
        self._avatar.set_photo(load_avatar())

        palette = PALETTES.get(self._mode, PALETTES["light"])
        self._avatar.set_colors(palette["accent"], "#FFFFFF")

        var = has_avatar()
        self._photo_button.setText(
            self._language.t("profile.photo_change" if var else "profile.photo_add")
        )
        self._photo_clear.setVisible(var)
        self._photo_clear.setText(self._language.t("profile.photo_remove"))

    def _choose_photo(self) -> None:
        """Dosya seçtirip fotoğrafı veri klasörüne kopyalar."""
        desenler = " ".join(f"*{uzanti}" for uzanti in IMAGE_SUFFIXES)
        yol, _ = QFileDialog.getOpenFileName(
            self,
            self._language.t("profile.photo_pick_title"),
            "",
            f"{self._language.t('profile.photo_filter')} ({desenler})",
        )
        if not yol:
            return

        if save_avatar(yol):
            self._refresh_avatar()
            self.saved.emit()
        else:
            # Bozuk ya da okunamayan dosya. Sessizce yutmak yerine söylüyoruz.
            self._saved_note.setProperty("tone", "danger")
            self._saved_note.setText(self._language.t("profile.photo_failed"))
            self._saved_note.show()
            repolish(self._saved_note)
            QTimer.singleShot(4000, self._reset_note)

    def _remove_photo(self) -> None:
        clear_avatar()
        self._refresh_avatar()
        self.saved.emit()

    def _reset_note(self) -> None:
        self._saved_note.hide()
        self._saved_note.setProperty("tone", "success")
        repolish(self._saved_note)

    def _show_saved(self) -> None:
        """Kaydedildi bilgisini gösterir, birkaç saniye sonra gizler."""
        self._saved_note.setText(f"✓  {self._language.t('profile.saved')}")
        self._saved_note.show()
        QTimer.singleShot(3000, self._saved_note.hide)

    # --- tema ve dil ------------------------------------------------------

    def set_mode(self, mode: str) -> None:
        self._mode = mode
        self._identity_card.set_mode(mode)
        self._stats_card.set_mode(mode)
        self._refresh_avatar()

    def retranslate(self) -> None:
        self._identity_title.setText(self._language.t("profile.welcome_title"))
        self._identity_help.setText(self._language.t("profile.welcome_text"))
        self._first_name.setPlaceholderText(self._language.t("profile.first_name"))
        self._last_name.setPlaceholderText(self._language.t("profile.last_name"))
        self._save_button.setText(self._language.t("common.save"))
        self._refresh_avatar()
        self._stats_title.setText(self._language.t_upper("profile.title"))

        for key in STAT_KEYS:
            self._stats[key].set_label(self._language.t(f"profile.stats.{key}"))
