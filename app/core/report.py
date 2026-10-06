""""Bu sayfada sorun mu var?": önceden doldurulmuş GitHub hata bildirimi.

Ders, sınav ya da alıştırmada bir yanlış gören kişi, sayfanın hangisi
olduğunu tarif etmeden bildirebilsin. Bağlantı GitHub'ın "yeni issue"
formunu `.github/ISSUE_TEMPLATE/bug_report.yml` ile açıyor ve alanlara
bölümü, sekmeyi, alıştırmayı, sürümü ve Windows'u yazıyor.

Program hiçbir şey göndermiyor: form kişinin kendi tarayıcısında açılıyor,
göndermek ona kalıyor. Adreste kişisel bilgi yok (yalnızca içerik
kimlikleri ve sürüm).
"""

from __future__ import annotations

import platform
from urllib.parse import urlencode

from ..version import APP_VERSION

NEW_ISSUE = "https://github.com/AlicanKaya192/Odyssey/issues/new"
TEMPLATE = "bug_report.yml"


def issue_url(chapter_id: str, section_id: str, section_title: str, pane: str,
              exercise_id: str = "", language: str = "tr") -> str:
    """Formu dolduran adres. Alan adları şablondaki `id`'ler."""
    yer = f"{chapter_id}/{section_id}"
    if pane:
        yer += f" · {pane}"
    if exercise_id:
        yer += f" · {exercise_id}"
    if language == "tr":
        giris = f"Sayfa: {section_title} ({yer})\n\nNe gördüm:\n"
    else:
        giris = f"Page: {section_title} ({yer})\n\nWhat I saw:\n"
    alanlar = {
        "template": TEMPLATE,
        "title": f"[Hata]: {section_title} — {pane or 'lesson'}",
        "ne-oldu": giris,
        "surum": APP_VERSION,
        "ortam": f"{platform.system()} {platform.release()}",
    }
    return f"{NEW_ISSUE}?{urlencode(alanlar)}"
