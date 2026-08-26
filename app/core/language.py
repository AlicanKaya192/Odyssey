"""Dil yönetimi.

Arayüz metinleri `app/i18n/` altındaki JSON dosyalarından okunur. Qt'nin
`.ts`/`.qm` sistemi yerine düz JSON kullanıyorum: derleme adımı gerekmiyor ve
dosyalar git'te elle okunup düzenlenebiliyor.

Dil değiştiğinde `language_changed` sinyali yayılır. Her ekran kendi
`retranslate()` metodunu bu sinyale bağlar, böylece uygulamayı yeniden
başlatmaya gerek kalmadan metinler değişir.

Bir anahtarın karşılığı seçili dilde yoksa Türkçesine düşülür; o da yoksa
anahtarın kendisi gösterilir (eksik çeviri sessizce boş metne dönüşmez,
geliştirirken hemen göze çarpar).
"""

from __future__ import annotations

import json
from pathlib import Path

from PySide6.QtCore import QObject, Signal

I18N_DIR = Path(__file__).resolve().parent.parent / "i18n"

DEFAULT_LANGUAGE = "tr"
FALLBACK_LANGUAGE = "tr"

# Ayarlar ekranında gösterilecek diller. Her dil kendi adıyla yazılır.
AVAILABLE_LANGUAGES = {
    "tr": "Türkçe",
    "en": "English",
}


def _load_catalog(language: str) -> dict[str, str]:
    path = I18N_DIR / f"{language}.json"
    if not path.exists():
        return {}
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


class LanguageManager(QObject):
    """Seçili dili tutar ve metin karşılıklarını sağlar."""

    language_changed = Signal(str)

    def __init__(self, language: str = DEFAULT_LANGUAGE) -> None:
        super().__init__()
        self._language = language if language in AVAILABLE_LANGUAGES else DEFAULT_LANGUAGE
        self._catalogs: dict[str, dict[str, str]] = {}
        self._load(self._language)
        self._load(FALLBACK_LANGUAGE)

    def _load(self, language: str) -> None:
        if language not in self._catalogs:
            self._catalogs[language] = _load_catalog(language)

    @property
    def language(self) -> str:
        return self._language

    def set_language(self, language: str) -> None:
        """Dili değiştirir ve arayüze haber verir."""
        if language not in AVAILABLE_LANGUAGES or language == self._language:
            return
        self._load(language)
        self._language = language
        self.language_changed.emit(language)

    def t(self, key: str, **kwargs: object) -> str:
        """Anahtarın seçili dildeki karşılığını döndürür.

        Metinde ``{isim}`` biçiminde yer tutucular varsa ``kwargs`` ile
        doldurulur.
        """
        text = self._catalogs.get(self._language, {}).get(key)

        if text is None:
            text = self._catalogs.get(FALLBACK_LANGUAGE, {}).get(key)

        if text is None:
            # Eksik çeviri: anahtarı olduğu gibi göster ki gözden kaçmasın.
            return key

        if kwargs:
            try:
                return text.format(**kwargs)
            except (KeyError, IndexError):
                # Yer tutucusu eşleşmiyorsa ham metni döndür, çökme.
                return text

        return text

    def pick(self, values: dict[str, str] | None, default: str = "") -> str:
        """İçerik dosyalarındaki ``{"tr": ..., "en": ...}`` alanlarını çözer.

        Seçili dil yoksa Türkçeye, o da yoksa varsayılana düşer.
        """
        if not values:
            return default
        return (
            values.get(self._language)
            or values.get(FALLBACK_LANGUAGE)
            or default
        )

    def has_translation(self, values: dict[str, str] | None) -> bool:
        """İçeriğin seçili dilde gerçekten karşılığı var mı?

        Yoksa arayüzde "bu bölüm henüz çevrilmedi" şeridi gösterilir.
        """
        if not values:
            return False
        return bool(values.get(self._language))


# Uygulama genelinde tek bir örnek kullanılır.
_manager: LanguageManager | None = None


def manager() -> LanguageManager:
    """Uygulamanın dil yöneticisini döndürür."""
    global _manager
    if _manager is None:
        _manager = LanguageManager()
    return _manager


def t(key: str, **kwargs: object) -> str:
    """Kısayol: ``language.t("sidebar.chapters")``."""
    return manager().t(key, **kwargs)
