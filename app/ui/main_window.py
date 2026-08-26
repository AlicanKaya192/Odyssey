"""Ana pencere: kenar çubuğu, içerik sekmeleri ve gezinme.

Yerleşim üç sütun: solda bölüm ağacı, ortada içerik, üstte ince bir başlık
şeridi. Üstte kalabalık bir araç çubuğu yok — bölüm başlığı, ilerleme ve
ayarlar dışında bir şey durmuyor.
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSplitter,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from ..core.catalog import Catalog, Section
from ..core.language import LanguageManager
from ..core.theme import ThemeManager
from ..paths import content_dir
from ..resources.theme.tokens import SPACING
from .exercise_view import ExerciseView
from .lesson_view import LessonView
from .pdf_view import PdfView
from .quiz_view import QuizView
from .settings_dialog import SettingsDialog
from .sidebar import Sidebar


class MainWindow(QMainWindow):
    """Uygulamanın ana penceresi."""

    def __init__(self, language: LanguageManager, theme: ThemeManager) -> None:
        super().__init__()
        self._language = language
        self._theme = theme
        self._catalog = Catalog.load(content_dir())
        self._current: Section | None = None
        self._solved: set[tuple[str, str, str]] = set()

        self.resize(1360, 880)
        self.setMinimumSize(1040, 680)

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addWidget(self._build_header())
        layout.addWidget(self._build_body(), 1)

        self._sidebar.set_catalog(self._catalog)
        self._install_shortcuts()

        language.language_changed.connect(self._on_language_changed)
        theme.theme_changed.connect(self._on_theme_changed)

        # İlk açılışta ilk alt bölümü göster.
        first = self._catalog.all_sections
        if first:
            self._open(first[0].chapter_id, first[0].id)

        self.retranslate()

    # --- yerleşim ---------------------------------------------------------

    def _build_header(self) -> QWidget:
        header = QFrame()
        header.setProperty("surface", "alt")
        header.setFixedHeight(72)

        layout = QHBoxLayout(header)
        layout.setContentsMargins(SPACING["lg"], SPACING["md"], SPACING["lg"], SPACING["md"])
        layout.setSpacing(SPACING["md"])

        titles = QVBoxLayout()
        titles.setSpacing(0)

        self._section_title = QLabel()
        self._section_title.setProperty("role", "subtitle")
        titles.addWidget(self._section_title)

        self._chapter_title = QLabel()
        self._chapter_title.setProperty("role", "muted")
        titles.addWidget(self._chapter_title)

        layout.addLayout(titles)
        layout.addStretch(1)

        self._previous_button = QPushButton()
        self._previous_button.clicked.connect(self._go_previous)
        layout.addWidget(self._previous_button)

        self._next_button = QPushButton()
        self._next_button.setProperty("variant", "primary")
        self._next_button.clicked.connect(self._go_next)
        layout.addWidget(self._next_button)

        self._settings_button = QPushButton("⚙")
        self._settings_button.setProperty("variant", "ghost")
        self._settings_button.setFixedWidth(44)
        self._settings_button.clicked.connect(self._open_settings)
        layout.addWidget(self._settings_button)

        return header

    def _build_body(self) -> QWidget:
        self._splitter = QSplitter(Qt.Orientation.Horizontal)

        self._sidebar = Sidebar(self._language)
        self._sidebar.section_selected.connect(self._open)
        self._splitter.addWidget(self._sidebar)

        self._tabs = QTabWidget()
        self._tabs.setDocumentMode(True)

        self._lesson_view = LessonView(self._language)
        self._pdf_view = PdfView(self._language)
        self._quiz_view = QuizView(self._language)
        self._exercise_view = ExerciseView(self._language)
        self._exercise_view.solved.connect(self._on_exercise_solved)

        self._splitter.addWidget(self._tabs)
        self._splitter.setSizes([300, 1060])
        self._splitter.setCollapsible(0, True)
        self._splitter.setStretchFactor(1, 1)

        return self._splitter

    def _install_shortcuts(self) -> None:
        QShortcut(QKeySequence("Ctrl+B"), self, self._toggle_sidebar)
        QShortcut(QKeySequence("Ctrl+Right"), self, self._go_next)
        QShortcut(QKeySequence("Ctrl+Left"), self, self._go_previous)
        QShortcut(QKeySequence("Ctrl+,"), self, self._open_settings)

    # --- gezinme ----------------------------------------------------------

    def _open(self, chapter_id: str, section_id: str) -> None:
        """Bir alt bölümü açar ve sekmeleri içeriğine göre kurar."""
        section = self._catalog.section(chapter_id, section_id)
        if section is None:
            return

        self._current = section
        self._tabs.clear()
        language_code = self._language.language

        for block in section.blocks:
            if block.type == "lesson":
                resolved = block.file_for(language_code)
                self._lesson_view.show_lesson(
                    resolved.path if resolved else None,
                    resolved.is_fallback if resolved else False,
                )
                self._tabs.addTab(self._lesson_view, self._language.t("tabs.lesson"))

            elif block.type == "pdf":
                resolved = block.file_for(language_code)
                self._pdf_view.show_pdf(
                    resolved.path if resolved else None,
                    self._language.pick(block.title),
                )
                self._tabs.addTab(self._pdf_view, self._language.t("tabs.pdf"))

            elif block.type == "quiz":
                resolved = block.file_for(language_code)
                if resolved and resolved.exists:
                    self._quiz_view.show_quiz(resolved.path, block.pass_score)
                    self._tabs.addTab(self._quiz_view, self._language.t("tabs.quiz"))

        exercises = section.exercises
        if exercises:
            self._exercise_view.show_exercise(exercises[0])
            label = self._language.t("tabs.exercise")
            if len(exercises) > 1:
                label = f"{label} (1/{len(exercises)})"
            self._tabs.addTab(self._exercise_view, label)

        self._sidebar.select(chapter_id, section_id)
        self._update_header()

    def _update_header(self) -> None:
        if self._current is None:
            return

        chapter = self._catalog.chapter(self._current.chapter_id)
        self._section_title.setText(self._language.pick(self._current.title))
        self._chapter_title.setText(
            self._language.pick(chapter.title) if chapter else ""
        )

        previous, following = self._catalog.neighbours(
            self._current.chapter_id, self._current.id
        )
        self._previous_button.setEnabled(previous is not None)
        self._next_button.setEnabled(following is not None)

    def _go_next(self) -> None:
        if self._current is None:
            return
        _, following = self._catalog.neighbours(self._current.chapter_id, self._current.id)
        if following:
            self._open(following.chapter_id, following.id)

    def _go_previous(self) -> None:
        if self._current is None:
            return
        previous, _ = self._catalog.neighbours(self._current.chapter_id, self._current.id)
        if previous:
            self._open(previous.chapter_id, previous.id)

    def _toggle_sidebar(self) -> None:
        sizes = self._splitter.sizes()
        if sizes[0] > 0:
            self._sidebar_width = sizes[0]
            self._splitter.setSizes([0, sum(sizes)])
        else:
            width = getattr(self, "_sidebar_width", 300)
            self._splitter.setSizes([width, sum(sizes) - width])

    # --- olaylar ----------------------------------------------------------

    def _on_exercise_solved(self, exercise_id: str) -> None:
        """Alıştırma çözüldüğünde kenar çubuğundaki durumu güncelle.

        Kalıcı ilerleme kaydı M3'te veritabanına bağlanacak; şimdilik yalnızca
        bu oturum boyunca tutuluyor.
        """
        if self._current is None:
            return

        key = (self._current.chapter_id, self._current.id, exercise_id)
        self._solved.add(key)

        total = len(self._current.exercises)
        done = sum(
            1 for c, s, _ in self._solved
            if c == self._current.chapter_id and s == self._current.id
        )
        status = "completed" if done >= total else "in_progress"
        self._sidebar.set_status(self._current.chapter_id, self._current.id, status)

    def _open_settings(self) -> None:
        dialog = SettingsDialog(self._language, self._theme, self)
        self._language.language_changed.connect(dialog.retranslate)
        dialog.exec()

    def _on_language_changed(self, _code: str) -> None:
        self.retranslate()
        if self._current is not None:
            self._open(self._current.chapter_id, self._current.id)

    def _on_theme_changed(self, mode: str) -> None:
        self._lesson_view.set_mode(mode)
        self._exercise_view.set_mode(mode)
        self._quiz_view.set_mode(mode)

    def retranslate(self) -> None:
        self.setWindowTitle(self._language.t("app.title"))
        self._previous_button.setText(self._language.t("nav.previous"))
        self._next_button.setText(self._language.t("nav.next"))
        self._settings_button.setToolTip(self._language.t("settings.title"))
        self._sidebar.retranslate()
        self._exercise_view.retranslate()
        self._quiz_view.retranslate()
        self._lesson_view.retranslate()
        self._update_header()
