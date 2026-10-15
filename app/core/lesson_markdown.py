"""Ders okuyucusunun markdown ayarları.

Ayrı modülde: arama dizini aynı ayarlarla çapa üretiyor ve ders okuyucusunu
(`app/ui/lesson_view.py`) içe aktarırsa tarayıcı bileşenini (QtWebEngine)
de yüklemiş oluyor.
"""

MARKDOWN_EXTENSIONS = ["fenced_code", "tables", "sane_lists", "toc"]
