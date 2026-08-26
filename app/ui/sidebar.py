"""Sol kenar çubuğu: bölüm ağacı ve arama.

Bölümler ve alt bölümler ağaç hâlinde listelenir. Her alt bölümün yanında
durumu görünür: tamamlandı, yarım kaldı veya başlanmadı. Yarım kalanı da
göstermek bilinçli bir tercih — nerede bıraktığını görmek dönmeyi
kolaylaştırıyor.
"""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QLabel,
    QLineEdit,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from ..core.catalog import Catalog
from ..core.language import LanguageManager
from ..resources.theme.tokens import SPACING

# İlerleme durumunu renkten bağımsız olarak da ayırt edebilmek için simge.
STATUS_MARKS = {
    "completed": "●",
    "in_progress": "◐",
    "not_started": "○",
}

ROLE_CHAPTER = Qt.ItemDataRole.UserRole
ROLE_SECTION = Qt.ItemDataRole.UserRole + 1


class Sidebar(QWidget):
    """Bölüm ağacı."""

    section_selected = Signal(str, str)  # bölüm id, alt bölüm id

    def __init__(self, language: LanguageManager, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._language = language
        self._catalog: Catalog | None = None
        self._statuses: dict[tuple[str, str], str] = {}

        layout = QVBoxLayout(self)
        layout.setContentsMargins(SPACING["md"], SPACING["md"], SPACING["sm"], SPACING["md"])
        layout.setSpacing(SPACING["sm"])

        self._title = QLabel()
        self._title.setProperty("role", "section")
        layout.addWidget(self._title)

        self._search = QLineEdit()
        self._search.textChanged.connect(self._filter)
        layout.addWidget(self._search)

        self._tree = QTreeWidget()
        self._tree.setHeaderHidden(True)
        self._tree.setIndentation(SPACING["md"])
        self._tree.setAnimated(True)
        self._tree.itemClicked.connect(self._on_clicked)
        layout.addWidget(self._tree, 1)

        self.retranslate()

    def set_catalog(self, catalog: Catalog) -> None:
        """Müfredatı yükler ve ağacı kurar."""
        self._catalog = catalog
        self._rebuild()

    def set_status(self, chapter_id: str, section_id: str, status: str) -> None:
        """Bir alt bölümün durumunu günceller."""
        self._statuses[(chapter_id, section_id)] = status
        self._rebuild()

    def _rebuild(self) -> None:
        if self._catalog is None:
            return

        expanded = {
            self._tree.topLevelItem(i).data(0, ROLE_CHAPTER)
            for i in range(self._tree.topLevelItemCount())
            if self._tree.topLevelItem(i).isExpanded()
        }
        selected = self._selected_ids()

        self._tree.clear()

        for chapter in self._catalog.chapters:
            parent = QTreeWidgetItem(self._tree)
            parent.setText(0, self._language.pick(chapter.title))
            parent.setData(0, ROLE_CHAPTER, chapter.id)
            parent.setFlags(parent.flags() & ~Qt.ItemFlag.ItemIsSelectable)

            for section in chapter.sections:
                status = self._statuses.get((chapter.id, section.id), "not_started")
                child = QTreeWidgetItem(parent)
                child.setText(
                    0,
                    f"{STATUS_MARKS.get(status, '○')}  {self._language.pick(section.title)}",
                )
                child.setData(0, ROLE_CHAPTER, chapter.id)
                child.setData(0, ROLE_SECTION, section.id)
                child.setToolTip(0, self._language.t(f"status.{status}"))

                if selected == (chapter.id, section.id):
                    self._tree.setCurrentItem(child)

            # İlk açılışta her şey açık olsun; kullanıcı kapatırsa öyle kalır.
            parent.setExpanded(chapter.id in expanded or not expanded)

    def _selected_ids(self) -> tuple[str, str] | None:
        item = self._tree.currentItem()
        if item is None:
            return None
        section_id = item.data(0, ROLE_SECTION)
        if not section_id:
            return None
        return item.data(0, ROLE_CHAPTER), section_id

    def select(self, chapter_id: str, section_id: str) -> None:
        """Belirtilen alt bölümü ağaçta seçili hâle getirir."""
        for index in range(self._tree.topLevelItemCount()):
            parent = self._tree.topLevelItem(index)
            for child_index in range(parent.childCount()):
                child = parent.child(child_index)
                if (
                    child.data(0, ROLE_CHAPTER) == chapter_id
                    and child.data(0, ROLE_SECTION) == section_id
                ):
                    parent.setExpanded(True)
                    self._tree.setCurrentItem(child)
                    return

    def _on_clicked(self, item: QTreeWidgetItem, _column: int) -> None:
        section_id = item.data(0, ROLE_SECTION)
        if not section_id:
            item.setExpanded(not item.isExpanded())
            return
        self.section_selected.emit(item.data(0, ROLE_CHAPTER), section_id)

    def _filter(self, text: str) -> None:
        needle = text.strip().lower()

        for index in range(self._tree.topLevelItemCount()):
            parent = self._tree.topLevelItem(index)
            visible_children = 0

            for child_index in range(parent.childCount()):
                child = parent.child(child_index)
                matches = not needle or needle in child.text(0).lower()
                child.setHidden(not matches)
                visible_children += int(matches)

            # Bölüm başlığı eşleşiyorsa altındakileri de göster.
            title_matches = not needle or needle in parent.text(0).lower()
            if title_matches and needle:
                for child_index in range(parent.childCount()):
                    parent.child(child_index).setHidden(False)
                visible_children = parent.childCount()

            parent.setHidden(visible_children == 0 and not title_matches)
            if needle:
                parent.setExpanded(True)

    def retranslate(self) -> None:
        self._title.setText(self._language.t("sidebar.title"))
        self._search.setPlaceholderText(self._language.t("sidebar.search"))
        self._rebuild()
