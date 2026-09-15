"""Yeni not penceresi: ad, klasör ve (isteğe bağlı) ders.

Klasör ya bir patika ya da kullanıcının kendi açtığı bir klasör. Patika
seçiliyse ders de seçilebiliyor; "Derse bağlı değil" seçilirse not
yalnızca klasörde duruyor ("Python'da en çok karıştırdıklarım" gibi).
Kendi klasörüne açılan not bir derse bağlanmıyor; bir dersin notunu kendi
klasörüne koymak için not dersten alınıp taşınıyor ("Taşı" bağlantıyı
koruyor).

Ad boşken "Oluştur" basılmıyor: ağaçta adsız notlar ayırt edilemiyor.
Pencerenin görünümü ve davranışı profil düzenleme penceresiyle ortak
(`modal.py`).
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ..core.catalog import Catalog
from ..core.language import LanguageManager
from ..core.user_notes import TITLE_MAX_LENGTH
from ..resources.theme.tokens import PALETTES, SPACING
from ..widgets.common import DropdownBox
from . import modal

DIALOG_WIDTH = 480

# Klasör kutusundaki anahtarlar `NotebookView` ile aynı: patikanın id'si ya
# da "folder:<id>".
FOLDER_PREFIX = "folder:"


class NewNoteDialog(QDialog):
    """Yeni bir notun adını ve yerini sorar."""

    def __init__(
        self,
        catalog: Catalog,
        language: LanguageManager,
        folders: list[dict] | None = None,
        folder_key: str = "",
        section_id: str = "",
        title: str = "",
        mode: str = "light",
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._catalog = catalog
        self._language = language
        t = language.t
        ok_rengi = PALETTES.get(mode, PALETTES["light"])["text_muted"]

        modal.prepare(self)
        self.setFixedWidth(DIALOG_WIDTH)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(SPACING["xl"], SPACING["xl"], SPACING["xl"], SPACING["xl"])
        layout.setSpacing(SPACING["sm"])

        heading = QLabel(t("notebook.dialog_title"))
        heading.setProperty("role", "subtitle")
        layout.addWidget(heading)
        layout.addSpacing(SPACING["sm"])

        layout.addWidget(self._label(t("notebook.name")))
        self._name = QLineEdit(title)
        self._name.setMaxLength(TITLE_MAX_LENGTH)
        self._name.setPlaceholderText(t("notebook.name_placeholder"))
        self._name.textChanged.connect(self._validate)
        self._name.returnPressed.connect(self._accept_if_valid)
        layout.addWidget(self._name)

        layout.addSpacing(SPACING["xs"])
        layout.addWidget(self._label(t("notebook.folder")))
        self._folder = DropdownBox(color=ok_rengi)
        for chapter in catalog.chapters:
            if chapter.sections:
                self._folder.addItem(language.pick(chapter.title), chapter.id)
        for folder in folders or []:
            self._folder.addItem(folder["name"], f"{FOLDER_PREFIX}{folder['id']}")
        self._folder.currentIndexChanged.connect(self._fill_lessons)
        layout.addWidget(self._folder)

        layout.addSpacing(SPACING["xs"])
        layout.addWidget(self._label(t("notebook.lesson")))
        self._lesson = DropdownBox(color=ok_rengi)
        layout.addWidget(self._lesson)

        layout.addSpacing(SPACING["md"])
        buttons = QHBoxLayout()
        buttons.setSpacing(SPACING["sm"])
        buttons.addStretch(1)

        cancel = QPushButton(t("common.cancel"))
        cancel.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel.clicked.connect(self.reject)
        buttons.addWidget(cancel)

        self._create = QPushButton(t("notebook.create"))
        self._create.setProperty("variant", "primary")
        self._create.setCursor(Qt.CursorShape.PointingHandCursor)
        self._create.clicked.connect(self._accept_if_valid)
        buttons.addWidget(self._create)
        layout.addLayout(buttons)

        # Açılışta verilen klasör ve ders seçili gelsin.
        index = self._folder.findData(folder_key)
        self._folder.setCurrentIndex(index if index >= 0 else 0)
        self._fill_lessons()
        index = self._lesson.findData(section_id)
        self._lesson.setCurrentIndex(index if index >= 0 else 0)

        self._validate()
        self._name.setFocus()
        self._name.selectAll()
        modal.freeze(self)

    def _label(self, text: str) -> QLabel:
        label = QLabel(text)
        label.setProperty("role", "muted")
        return label

    def _fill_lessons(self) -> None:
        """Seçili patikanın dersleri; kendi klasöründe yalnızca "Derse bağlı değil"."""
        self._lesson.clear()
        self._lesson.addItem(self._language.t("notebook.general"), "")
        key = self._folder.currentData() or ""
        chapter = None if key.startswith(FOLDER_PREFIX) else self._catalog.chapter(key)
        self._lesson.setEnabled(chapter is not None)
        if chapter is None:
            return
        for section in chapter.sections:
            self._lesson.addItem(self._language.pick(section.title), section.id)

    def _validate(self) -> None:
        self._create.setEnabled(bool(self._name.text().strip()))

    def _accept_if_valid(self) -> None:
        if self._name.text().strip():
            self.accept()

    def values(self) -> tuple[str, str, str, int | None]:
        """(patika, ders, ad, kullanıcının klasörü). Kendi klasöründe patika boş."""
        key = self._folder.currentData() or ""
        if key.startswith(FOLDER_PREFIX):
            return "", "", self._name.text().strip(), int(key[len(FOLDER_PREFIX):])
        return key, self._lesson.currentData() or "", self._name.text().strip(), None
