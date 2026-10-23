"""Kodun ürettiği PDF'in ilk sayfası, resim olarak.

Çıktı sekmesi bir sayfa (Chromium) ve PDF'i kendi görüntüleyicisiyle açmak
yerine ilk sayfayı PNG'ye çeviriyor: grafikler gibi tam genişlikte
görünüyor, tema ve kaydırma aynı. CS50'nin Shirtificate problemi bunun
için geldi (B-200): kişi ürettiği sertifikayı göremiyordu.

Çeviri `QtPdf` ile (PySide6 içinde, pakette de var). Dosya bozuksa ya da
sayfası yoksa `None`; çağıran yalnızca dosyanın adını gösterir.
"""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QSize
from PySide6.QtPdf import QPdfDocument

# Çıktı sekmesi ~400–900 piksel genişlikte; 2 kat ölçekte keskin kalsın.
PREVIEW_WIDTH = 1200


def first_page(pdf: Path, width: int = PREVIEW_WIDTH) -> Path | None:
    """İlk sayfayı `<ad>.pdf.png` olarak PDF'in yanına yazar; olmazsa None."""
    document = QPdfDocument()
    try:
        if document.load(str(pdf)) != QPdfDocument.Error.None_ or document.pageCount() < 1:
            return None
        page = document.pagePointSize(0)
        if page.width() <= 0 or page.height() <= 0:
            return None
        size = QSize(width, round(width * page.height() / page.width()))
        image = document.render(0, size)
        if image.isNull():
            return None
        target = pdf.with_name(pdf.name + ".png")
        return target if image.save(str(target), "PNG") else None
    finally:
        document.close()
