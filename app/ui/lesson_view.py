"""Ders metnini gösteren görünüm.

Yerleşim üç sütun: solda boşluk, ortada metin, sağda sayfa içi başlık listesi.
Metnin genişliği `READING_WIDTH` ile sınırlı çünkü satırlar uçtan uca uzarsa
göz satır başını kaybediyor. Sağ sütun hem o boşluğu değerlendiriyor hem de
uzun derslerde nerede olduğunu gösteriyor.

Ders seçili dilde yoksa Türkçesi gösterilir ve üstte bunu belirten bir şerit
çıkar. Bu bir hata değil; içerik önce Türkçe yazılıyor.
"""

from __future__ import annotations

import re
from pathlib import Path

import markdown

from PySide6.QtCore import Qt
from PySide6.QtGui import QFontMetrics, QTextCursor, QTextDocument
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

from ..core.language import LanguageManager
from ..resources.theme.tokens import (
    FONT_SIZES,
    FONTS,
    PALETTES,
    READING_WIDTH,
    SPACING,
    TOC_WIDTH,
)
from ..widgets.common import Banner, section_label
from ..widgets.effects import repolish

MARKDOWN_EXTENSIONS = ["fenced_code", "tables", "sane_lists"]

# Sayfa içi başlık listesine yalnızca ikinci seviye başlıklar giriyor;
# üçüncü seviyeye kadar inince liste kalabalıklaşıyor.
HEADING_PATTERN = re.compile(r"^##\s+(.+)$", re.MULTILINE)


def build_document_css(mode: str) -> str:
    """Ders metninin stili.

    Qt'nin zengin metin motoru CSS'in bir alt kümesini destekliyor, o yüzden
    burada sade kalıyoruz.
    """
    palette = PALETTES.get(mode, PALETTES["light"])
    return f"""
    body {{
        color: {palette['text']};
        font-family: {FONTS['ui']};
        font-size: {FONT_SIZES['md']}pt;
        line-height: 165%;
    }}
    h1 {{ font-size: {FONT_SIZES['display']}pt; font-weight: 700;
          color: {palette['text']}; margin-bottom: 6px; }}
    h2 {{ font-size: {FONT_SIZES['xl']}pt; font-weight: 660;
          color: {palette['text']}; margin-top: 32px; }}
    h3 {{ font-size: {FONT_SIZES['lg']}pt; font-weight: 640;
          color: {palette['text']}; margin-top: 22px; }}
    p  {{ margin: 14px 0; color: {palette['text']}; }}
    li {{ color: {palette['text']}; }}
    a  {{ color: {palette['accent']}; }}
    hr {{ border: 1px solid {palette['border']}; }}
    code {{
        font-family: {FONTS['mono']};
        font-size: {FONT_SIZES['sm']}pt;
        background-color: {palette['code_bg']};
        color: {palette['accent']};
    }}
    pre {{
        font-family: {FONTS['mono']};
        font-size: {FONT_SIZES['sm']}pt;
        background-color: {palette['code_bg']};
        color: {palette['text']};
        border: 1px solid {palette['border']};
        padding: 16px 18px;
        margin: 16px 0;
    }}
    pre code {{ background-color: transparent; color: {palette['text']}; }}
    table {{
        border-collapse: collapse;
        margin: 18px 0;
        background-color: {palette['surface']};
    }}
    th {{
        background-color: {palette['surface_alt']};
        padding: 11px 15px;
        text-align: left;
        border: 1px solid {palette['border']};
    }}
    td {{ padding: 11px 15px; border: 1px solid {palette['border']}; }}
    blockquote {{
        background-color: {palette['accent_soft']};
        color: {palette['text']};
        border-left: 3px solid {palette['accent']};
        padding: 14px 18px;
        margin: 20px 0;
    }}
    """


def render_markdown(text: str, mode: str) -> str:
    """Markdown metnini, temaya uygun stille birlikte HTML'e çevirir."""
    body = markdown.markdown(text, extensions=MARKDOWN_EXTENSIONS)
    return (
        f"<html><head><style>{build_document_css(mode)}</style></head>"
        f"<body>{body}</body></html>"
    )


class TableOfContents(QWidget):
    """Sağdaki sayfa içi başlık listesi ve bölüm ilerlemesi."""

    def __init__(self, language: LanguageManager, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._language = language
        self._buttons: list[QPushButton] = []
        self._on_click = None

        self.setFixedWidth(TOC_WIDTH)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(SPACING["xl"], 0, 0, 0)
        layout.setSpacing(SPACING["sm"])

        self._heading = section_label("")
        layout.addWidget(self._heading)

        self._links = QVBoxLayout()
        self._links.setSpacing(0)
        layout.addLayout(self._links)

        layout.addSpacing(SPACING["md"])

        self._progress_box = QFrame()
        self._progress_box.setProperty("surface", "alt")
        box_layout = QVBoxLayout(self._progress_box)
        box_layout.setContentsMargins(
            SPACING["md"], SPACING["md"], SPACING["md"], SPACING["md"]
        )
        box_layout.setSpacing(SPACING["sm"])

        self._progress_title = QLabel()
        self._progress_title.setProperty("role", "muted")
        box_layout.addWidget(self._progress_title)

        self._bar = QProgressBar()
        self._bar.setTextVisible(False)
        box_layout.addWidget(self._bar)

        self._progress_caption = QLabel()
        self._progress_caption.setProperty("role", "muted")
        self._progress_caption.setWordWrap(True)
        box_layout.addWidget(self._progress_caption)

        layout.addWidget(self._progress_box)
        layout.addStretch(1)

        self.retranslate()

    def set_headings(self, headings: list[str], on_click) -> None:
        """Başlıkları yeniden kurar."""
        self._on_click = on_click

        while self._links.count():
            item = self._links.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self._buttons = []

        for index, heading in enumerate(headings):
            button = QPushButton()
            button.setProperty("variant", "toc")
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.setToolTip(heading)
            # Uzun başlıklar sütunu taşırmasın: sığmayanı üç noktayla kısalt.
            # QPushButton metni satıra bölemediği için tek çare bu.
            metrics = QFontMetrics(button.font())
            button.setText(
                metrics.elidedText(
                    heading, Qt.TextElideMode.ElideRight, TOC_WIDTH - SPACING["xxl"] - 20
                )
            )
            button.clicked.connect(lambda _=False, t=heading, i=index: self._go(t, i))
            self._links.addWidget(button)
            self._buttons.append(button)

        self.set_active(0)

    def _go(self, heading: str, index: int) -> None:
        self.set_active(index)
        if self._on_click:
            self._on_click(heading)

    def set_active(self, index: int) -> None:
        for position, button in enumerate(self._buttons):
            button.setProperty("active", "true" if position == index else "false")
            repolish(button)

    def set_progress(self, percent: int, caption: str) -> None:
        self._bar.setRange(0, 100)
        self._bar.setValue(percent)
        self._progress_caption.setText(caption)

    def retranslate(self) -> None:
        self._heading.setText(self._language.t("section.on_this_page").upper())
        self._progress_title.setText(self._language.t("section.section_progress"))


class LessonView(QWidget):
    """Bir dersin metnini gösterir."""

    def __init__(
        self,
        language: LanguageManager,
        parent: QWidget | None = None,
        compact: bool = False,
        show_toc: bool = True,
    ) -> None:
        """`compact`, dar bir panelde (alıştırma yönergesi gibi) kullanılır.

        Ders sayfasında metni ortalayıp geniş boşluk bırakmak okumayı
        kolaylaştırıyor; 400 piksellik bir yan panelde ise aynı boşluklar
        metni iki kelimelik sütuna sıkıştırıyor.
        """
        super().__init__(parent)
        self._language = language
        self._mode = "light"
        self._source = ""
        self._compact = compact
        self._show_toc = show_toc and not compact
        self._headings: list[str] = []
        self._meta: list[str] = []

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)
        self._scroll.setFrameShape(QFrame.Shape.NoFrame)
        self._scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        container = QWidget()
        row = QHBoxLayout(container)

        if compact:
            row.setContentsMargins(
                SPACING["lg"], SPACING["lg"], SPACING["md"], SPACING["lg"]
            )
        else:
            row.setContentsMargins(
                SPACING["xl"], SPACING["xl"], SPACING["xl"], SPACING["xxl"]
            )
            row.addStretch(1)

        column = QWidget()
        column.setMaximumWidth(READING_WIDTH)
        if not compact:
            column.setMinimumWidth(320)
        column.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        self._column_layout = QVBoxLayout(column)
        self._column_layout.setContentsMargins(0, 0, 0, 0)
        self._column_layout.setSpacing(SPACING["md"])

        self._completed_banner = Banner("", "success", "✓")
        self._completed_banner.hide()
        self._column_layout.addWidget(self._completed_banner)

        self._translation_banner = Banner("", "warning", "!")
        self._translation_banner.hide()
        self._column_layout.addWidget(self._translation_banner)

        self._browser = QTextBrowser()
        self._browser.setOpenExternalLinks(False)
        self._browser.setFrameShape(QFrame.Shape.NoFrame)
        self._browser.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._browser.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._browser.document().setDocumentMargin(0)
        self._column_layout.addWidget(self._browser)

        self._footer = QHBoxLayout()
        self._footer.setSpacing(SPACING["sm"])
        self._column_layout.addLayout(self._footer)

        row.addWidget(column, 8)

        # Ebeveyn her durumda veriliyor. Ebeveynsiz bir widget Qt'de üst
        # seviye pencere sayılıyor; kullanılmadığı ekranlarda görünür
        # yapıldığı anda ayrı bir pencere olarak açılıyordu.
        self._toc = TableOfContents(language, container)
        if self._show_toc:
            row.addWidget(self._toc, 0, Qt.AlignmentFlag.AlignTop)
        else:
            self._toc.hide()

        if not compact:
            row.addStretch(1)

        self._scroll.setWidget(container)
        outer.addWidget(self._scroll)

        self._column = column

    # --- içerik -----------------------------------------------------------

    def set_meta(self, items: list[str]) -> None:
        """Başlığın altındaki bilgi satırı: süre, alıştırma ve sınav sayısı.

        Markdown'ın içine yerleştiriliyor ki başlıkla aynı akışta dursun ve
        metinle birlikte kaysın.
        """
        self._meta = [item for item in items if item]
        if self._source:
            self._render()

    def show_lesson(
        self,
        path: Path | None,
        is_fallback: bool = False,
        completed: bool = False,
    ) -> None:
        """Ders dosyasını yükler."""
        if path is None or not path.exists():
            self._source = f"*{self._language.t('content.not_found', path=path or '-')}*"
        else:
            self._source = path.read_text(encoding="utf-8")

        self._translation_banner.setVisible(is_fallback)
        if is_fallback:
            self._translation_banner.set_text(
                self._language.t("content.translation_missing")
            )

        self._completed_banner.setVisible(completed)
        if completed:
            self._completed_banner.set_text(
                self._language.t("section.completed_banner")
            )

        self._render()

    def show_text(self, text: str) -> None:
        """Hazır markdown metnini gösterir (alıştırma yönergesi gibi)."""
        self._source = text
        self._translation_banner.hide()
        self._completed_banner.hide()
        self._render()

    def set_progress(self, percent: int, caption: str) -> None:
        if self._show_toc:
            self._toc.set_progress(percent, caption)

    def footer_layout(self) -> QHBoxLayout:
        """Ders metninin altındaki düğme sırası."""
        return self._footer

    # --- çizim ------------------------------------------------------------

    def _meta_html(self) -> str:
        """Bilgi satırını, ilk başlığın hemen altına girecek HTML olarak üretir."""
        if not self._meta:
            return ""
        palette = PALETTES.get(self._mode, PALETTES["light"])
        birlesik = "&nbsp;&nbsp;·&nbsp;&nbsp;".join(self._meta)
        return (
            f'<p style="color:{palette["text_muted"]}; '
            f'font-size:{FONT_SIZES["sm"]}pt; margin-top:0;">{birlesik}</p>'
        )

    def _with_meta(self, source: str) -> str:
        """Bilgi satırını ilk başlıktan sonraya yerleştirir."""
        meta = self._meta_html()
        if not meta:
            return source

        lines = source.splitlines()
        for index, line in enumerate(lines):
            if line.startswith("# "):
                lines.insert(index + 1, f"\n{meta}\n")
                return "\n".join(lines)

        return f"{meta}\n\n{source}"

    def _render(self) -> None:
        self._browser.setHtml(render_markdown(self._with_meta(self._source), self._mode))
        self._headings = HEADING_PATTERN.findall(self._source)
        if self._show_toc:
            self._toc.set_headings(self._headings, self._scroll_to_heading)
        self._fit_height()

    def _fit_height(self) -> None:
        """Metin yüksekliğini belgeye göre ayarlar.

        QTextBrowser kendi kaydırma çubuğunu kullanmıyor; sayfanın tamamı
        dıştaki QScrollArea ile kaydırılıyor, böylece iç içe iki kaydırma
        çubuğu olmuyor.
        """
        document = self._browser.document()
        document.setTextWidth(self._browser.viewport().width())
        self._browser.setMinimumHeight(int(document.size().height()) + SPACING["lg"])

    def _scroll_to_heading(self, heading: str) -> None:
        """Sayfayı ilgili başlığa kaydırır."""
        document = self._browser.document()
        cursor = document.find(heading, 0, QTextDocument.FindFlag.FindCaseSensitively)
        if cursor.isNull():
            return

        cursor.movePosition(QTextCursor.MoveOperation.StartOfBlock)
        top = self._browser.cursorRect(cursor).top()
        offset = self._browser.mapTo(self._scroll.widget(), self._browser.rect().topLeft()).y()

        bar = self._scroll.verticalScrollBar()
        bar.setValue(max(0, top + offset - SPACING["lg"]))

    def resizeEvent(self, event) -> None:  # noqa: N802
        super().resizeEvent(event)
        self._fit_height()

    # --- tema ve dil ------------------------------------------------------

    def set_mode(self, mode: str) -> None:
        self._mode = mode
        self._render()

    def retranslate(self) -> None:
        if self._show_toc:
            self._toc.retranslate()
        if self._translation_banner.isVisible():
            self._translation_banner.set_text(
                self._language.t("content.translation_missing")
            )
        if self._completed_banner.isVisible():
            self._completed_banner.set_text(
                self._language.t("section.completed_banner")
            )
