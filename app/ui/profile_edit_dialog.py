"""Profil düzenleme penceresi.

**Neden ayrı bir pencere?** Ad, soyad ve fotoğraf alanları önce profil
kartının içinde açılıyordu. O kart sol sütunda dar duruyor ve alanlarla
düğmeler oraya sığmıyordu: "Fotoğrafı değiştir" düğmesi tek başına 278
piksel istiyor, kart ona 73 piksel veriyordu — yazı "ayde" gibi kırpılıyordu.
Kartı genişletmek de olmuyor, çünkü kart bir gösterge kartı; düzenleme
alanları oraya sığdıkça sığdırılıyordu.

Ayrı pencere bu sıkışmayı kökten kaldırıyor: alanlar istediği kadar yer
alıyor, kart da yalnızca gösterdiği şeye göre boyutlanıyor.

Arka plan pencere açıkken kararıyor (`Backdrop`), böylece odak nerede
olduğu belli oluyor. Pencerenin sabit boyutlu, ortada ve taşınmaz olması
`app/ui/modal.py` içinde, ayarlar penceresiyle ortak.
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ..core.avatar import IMAGE_SUFFIXES, clear_avatar, has_avatar, load_avatar, save_avatar
from ..core.language import LanguageManager
from ..resources.theme.tokens import PALETTES, SPACING
from ..widgets.avatar import AvatarView
from . import modal
from .modal import Backdrop  # noqa: F401  (dışarıdan buradan alınıyordu)

DIALOG_WIDTH = 500
AVATAR_SIZE = 112

class ProfileEditDialog(QDialog):
    """Ad, soyad ve fotoğrafı düzenler."""

    def __init__(
        self,
        language: LanguageManager,
        store,
        mode: str = "light",
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._language = language
        self._store = store
        self._mode = mode
        self._photo_changed = False

        modal.prepare(self)
        self.setFixedWidth(DIALOG_WIDTH)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            SPACING["xl"], SPACING["xl"], SPACING["xl"], SPACING["xl"]
        )
        layout.setSpacing(SPACING["md"])

        self._title = QLabel()
        self._title.setProperty("role", "subtitle")
        layout.addWidget(self._title)

        # --- fotoğraf -----------------------------------------------------
        foto = QHBoxLayout()
        foto.setSpacing(SPACING["lg"])

        self._avatar = AvatarView(AVATAR_SIZE)
        self._avatar.clicked.connect(self._choose_photo)
        foto.addWidget(self._avatar, 0, Qt.AlignmentFlag.AlignTop)

        foto_dugmeler = QVBoxLayout()
        foto_dugmeler.setSpacing(SPACING["sm"])
        self._photo_button = QPushButton()
        self._photo_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._photo_button.clicked.connect(self._choose_photo)
        foto_dugmeler.addWidget(self._photo_button)

        self._photo_clear = QPushButton()
        self._photo_clear.setProperty("variant", "ghost")
        self._photo_clear.setCursor(Qt.CursorShape.PointingHandCursor)
        self._photo_clear.clicked.connect(self._remove_photo)
        foto_dugmeler.addWidget(self._photo_clear)

        self._photo_note = QLabel()
        self._photo_note.setProperty("tone", "danger")
        self._photo_note.setWordWrap(True)
        self._photo_note.hide()
        foto_dugmeler.addWidget(self._photo_note)

        foto_dugmeler.addStretch(1)
        foto.addLayout(foto_dugmeler, 1)
        layout.addLayout(foto)
        layout.addSpacing(SPACING["sm"])

        # --- alanlar ------------------------------------------------------
        profil = store.profile()
        for anahtar, etiket_adi in (("first_name", "_first_label"), ("last_name", "_last_label")):
            etiket = QLabel()
            etiket.setProperty("role", "muted")
            setattr(self, etiket_adi, etiket)
            layout.addWidget(etiket)

            alan = QLineEdit(profil.get(anahtar, ""))
            alan.returnPressed.connect(self.accept)
            setattr(self, f"_{anahtar}", alan)
            layout.addWidget(alan)

        layout.addSpacing(SPACING["md"])

        # --- düğmeler -----------------------------------------------------
        dugmeler = QHBoxLayout()
        dugmeler.addStretch(1)
        self._cancel = QPushButton()
        self._cancel.setProperty("variant", "ghost")
        self._cancel.setCursor(Qt.CursorShape.PointingHandCursor)
        self._cancel.clicked.connect(self.reject)
        dugmeler.addWidget(self._cancel)

        self._save = QPushButton()
        self._save.setProperty("variant", "primary")
        self._save.setCursor(Qt.CursorShape.PointingHandCursor)
        self._save.clicked.connect(self.accept)
        self._save.setDefault(True)
        dugmeler.addWidget(self._save)
        layout.addLayout(dugmeler)

        self._refresh_avatar()
        self.retranslate()
        modal.freeze(self)

    def showEvent(self, event) -> None:  # noqa: N802
        super().showEvent(event)
        modal.center(self)

    # --- veri -------------------------------------------------------------

    @property
    def first_name(self) -> str:
        return self._first_name.text().strip()

    @property
    def last_name(self) -> str:
        return self._last_name.text().strip()

    @property
    def photo_changed(self) -> bool:
        return self._photo_changed

    # --- fotoğraf ---------------------------------------------------------

    def _refresh_avatar(self) -> None:
        harfler = "".join(
            parca[:1] for parca in (self.first_name, self.last_name) if parca
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

    def _choose_photo(self) -> None:
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
            self._photo_changed = True
            self._photo_note.hide()
            self._refresh_avatar()
        else:
            # Bozuk ya da okunamayan dosya. Sessizce yutmak yerine söylüyoruz.
            self._photo_note.setText(self._language.t("profile.photo_failed"))
            self._photo_note.show()

    def _remove_photo(self) -> None:
        clear_avatar()
        self._photo_changed = True
        self._refresh_avatar()

    # --- metinler ---------------------------------------------------------

    def retranslate(self) -> None:
        t = self._language.t
        self.setWindowTitle(t("profile.edit_title"))
        self._title.setText(t("profile.edit_title"))
        self._first_label.setText(t("profile.first_name"))
        self._last_label.setText(t("profile.last_name"))
        self._first_name.setPlaceholderText(t("profile.first_name"))
        self._last_name.setPlaceholderText(t("profile.last_name"))
        self._photo_clear.setText(t("profile.photo_remove"))
        self._cancel.setText(t("common.cancel"))
        self._save.setText(t("common.save"))
        self._refresh_avatar()
