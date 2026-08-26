"""Ders metnini gösteren görünüm.

Markdown dosyası HTML'e çevrilip `QTextBrowser` içinde gösterilir. Metnin
genişliği `READING_WIDTH` ile sınırlanır: tam ekranda satırlar uçtan uca
uzarsa göz satır başını kaybediyor.

Ders seçili dilde yoksa Türkçesi gösterilir ve üstte bunu belirten bir şerit
çıkar. Bu bir hata değil, bilinen bir durum — içerik önce Türkçe yazılıyor.
"""

from __future__ import annotations

from pathlib import Path

import markdown

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QSizePolicy,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

from ..core.language import LanguageManager
from ..resources.theme.tokens import FONT_SIZES, FONTS, PALETTES, READING_WIDTH, SPACING

MARKDOWN_EXTENSIONS = ["fenced_code", "tables", "sane_lists"]


def build_document_css(mode: str) -> str:
    """Ders metninin stili.

    Qt'nin zengin metin motoru CSS'in yalnızca bir alt kümesini destekliyor,
    o yüzden burada sade kalıyoruz.
    """
    palette = PALETTES.get(mode, PALETTES["light"])
    return f"""
    body {{
        color: {palette['text']};
        font-family: {FONTS['ui']};
        font-size: {FONT_SIZES['md']}pt;
        line-height: 160%;
    }}
    h1 {{ font-size: {FONT_SIZES['xxl']}pt; color: {palette['text']}; margin-bottom: 4px; }}
    h2 {{ font-size: {FONT_SIZES['xl']}pt; color: {palette['text']}; margin-top: 28px; }}
    h3 {{ font-size: {FONT_SIZES['lg']}pt; color: {palette['text']}; margin-top: 20px; }}
    p  {{ margin: 12px 0; }}
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
        padding: 14px;
        margin: 14px 0;
    }}
    pre code {{ background-color: transparent; color: {palette['text']}; }}
    table {{
        border-collapse: collapse;
        margin: 16px 0;
        background-color: {palette['surface']};
    }}
    th {{
        background-color: {palette['surface_alt']};
        padding: 10px 14px;
        text-align: left;
        border: 1px solid {palette['border']};
    }}
    td {{ padding: 10px 14px; border: 1px solid {palette['border']}; }}
    blockquote {{
        color: {palette['text_muted']};
        border-left: 3px solid {palette['accent']};
        padding-left: 14px;
        margin-left: 0;
    }}
    """


def render_markdown(text: str, mode: str) -> str:
    """Markdown metnini, temaya uygun stille birlikte HTML'e çevirir."""
    body = markdown.markdown(text, extensions=MARKDOWN_EXTENSIONS)
    return f"<html><head><style>{build_document_css(mode)}</style></head><body>{body}</body></html>"


class TranslationBanner(QFrame):
    """"Bu bölüm henüz çevrilmedi" uyarı şeridi."""

    def __init__(self, language: LanguageManager, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._language = language
        self.setProperty("banner", "warning")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(SPACING["md"], SPACING["sm"], SPACING["md"], SPACING["sm"])

        self._label = QLabel()
        self._label.setWordWrap(True)
        self._label.setProperty("tone", "warning")
        layout.addWidget(self._label)

        self.retranslate()

    def retranslate(self) -> None:
        self._label.setText(self._language.t("content.translation_missing"))


class LessonView(QWidget):
    """Bir dersin metnini gösterir."""

    def __init__(
        self,
        language: LanguageManager,
        parent: QWidget | None = None,
        compact: bool = False,
    ) -> None:
        """`compact`, dar bir panelde (alıştırma yönergesi gibi) kullanılır.

        Ders sayfasında metni ortalayıp geniş boşluk bırakmak okumayı
        kolaylaştırıyor; ama 400 piksellik bir yan panelde aynı boşluklar
        metni iki kelimelik sütuna sıkıştırıyor. O yüzden orada dar kenar
        boşlukları kullanılıyor ve ortalama yapılmıyor.
        """
        super().__init__(parent)
        self._language = language
        self._mode = "light"
        self._source = ""
        self._compact = compact

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        container = QWidget()
        # Metni ortalayıp genişliğini sınırlamak için üç sütun: boşluk,
        # içerik, boşluk. Ferahlığın önemli bir kısmı buradan geliyor.
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
        # Genişlik hem sınırlı hem esnek olmalı: üst sınır okuma rahatlığı
        # için, esneklik ise dar pencerede sütunun daralabilmesi için.
        column.setMaximumWidth(READING_WIDTH)
        if not compact:
            column.setMinimumWidth(320)
        column.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self._column_layout = QVBoxLayout(column)
        self._column_layout.setContentsMargins(0, 0, 0, 0)
        self._column_layout.setSpacing(SPACING["md"])

        self._banner = TranslationBanner(language)
        self._banner.hide()
        self._column_layout.addWidget(self._banner)

        self._browser = QTextBrowser()
        self._browser.setOpenExternalLinks(False)
        self._browser.setFrameShape(QFrame.Shape.NoFrame)
        self._browser.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._browser.document().setDocumentMargin(0)
        self._column_layout.addWidget(self._browser)

        # Esneme oranları: sütun kenar boşluklarından çok daha hızlı büyür,
        # üst sınıra ulaşınca artan yer iki yana eşit dağılır ve sütun ortada kalır.
        row.addWidget(column, 8)
        if not compact:
            row.addStretch(1)

        scroll.setWidget(container)
        outer.addWidget(scroll)

    def _fit_height(self) -> None:
        """İçerik yüksekliğini belgeye göre ayarlar.

        QTextBrowser kendi kaydırma çubuğunu kullanmıyor; sayfanın tamamı
        dıştaki QScrollArea ile kaydırılıyor, böylece iç içe iki kaydırma
        çubuğu olmuyor.
        """
        document = self._browser.document()
        document.setTextWidth(self._browser.viewport().width())
        self._browser.setMinimumHeight(int(document.size().height()) + SPACING["lg"])

    def resizeEvent(self, event) -> None:  # noqa: N802
        super().resizeEvent(event)
        self._fit_height()

    def show_lesson(self, path: Path | None, is_fallback: bool = False) -> None:
        """Ders dosyasını yükler."""
        if path is None or not path.exists():
            self._source = f"*{self._language.t('content.not_found', path=path or '-')}*"
        else:
            self._source = path.read_text(encoding="utf-8")

        self._banner.setVisible(is_fallback)
        self._render()

    def show_text(self, text: str) -> None:
        """Hazır markdown metnini gösterir (alıştırma yönergesi gibi)."""
        self._source = text
        self._banner.hide()
        self._render()

    def _render(self) -> None:
        self._browser.setHtml(render_markdown(self._source, self._mode))
        self._fit_height()

    def set_mode(self, mode: str) -> None:
        self._mode = mode
        self._render()

    def retranslate(self) -> None:
        self._banner.retranslate()
