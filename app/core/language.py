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
import os
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


# Python'un `upper()` metodu Türkçede yanlış sonuç veriyor: `i` harfini `I`
# yapıyor, oysa Türkçede karşılığı `İ`. "Öğrenme patikaları" başlığı ekranda
# "ÖĞRENME PATIKALARI" diye çıkıyordu. Çeviri tablosu bunu düzeltiyor;
# `ı` -> `I` dönüşümünü Python zaten doğru yapıyor ama açıkça yazmak
# okuyanın kafasını karıştırmıyor.
TURKISH_UPPERCASE = str.maketrans({"i": "İ", "ı": "I"})


def upper(text: str, language: str) -> str:
    """Metni seçili dilin kurallarına göre büyütür."""
    if language == "tr":
        return text.translate(TURKISH_UPPERCASE).upper()
    return text.upper()


# Windows'un dil kimliklerinde **birincil dil** alt on bitte duruyor:
# 0x041F (Türkçe-Türkiye) → 0x1F. Alt bölge (Türkiye, Almanya…) bizi
# ilgilendirmiyor, dilin kendisi yeter.
WINDOWS_PRIMARY_LANGUAGES = {
    0x1F: "tr",
    0x09: "en",
}


def _windows_ui_language() -> str:
    """Windows'un **ekran diline** göre seçim. Sorulamazsa boş metin.

    Türkçe ise `tr`, **başka herhangi bir dilse** `en` döndürüyor.
    Desteklemediğimiz bir dili görünce Qt'nin listesine düşmek yanlış
    olurdu: ekran dili Almancaysa kullanıcı Türkçe bilmiyor demektir, ama
    Qt'nin tercih listesinde Türkçe ikinci sırada duruyorsa uygulama
    Türkçe açılırdı (ölçüldü).

    Neden ayrıca soruluyor: bu makinede ekran dili Türkçe (0x041F) ama
    bölgesel biçim İngilizce (0x0409) — ikisi ayrı ayarlar ve sık
    ayrışıyor. Qt'nin `uiLanguages()` çağrısı çoğu zaman doğru olanı
    veriyor ama bazı kurulumlarda biçim ayarına kayıyor; o zaman Türkçe
    bir Windows'ta uygulama İngilizce açılıyor.

    `GetUserDefaultUILanguage` doğrudan ekran dilini veriyor, yani
    kullanıcının menüleri hangi dilde gördüğünü. Sorulacak doğru soru bu.
    """
    if os.name != "nt":
        return ""
    try:
        import ctypes

        kimlik = ctypes.windll.kernel32.GetUserDefaultUILanguage()
    except (OSError, AttributeError):
        return ""

    kod = WINDOWS_PRIMARY_LANGUAGES.get(kimlik & 0x3FF, "")
    if kod in AVAILABLE_LANGUAGES:
        return kod
    # Windows cevap verdi ama dili desteklemiyoruz: İngilizce.
    return "en" if kimlik else ""


def system_language() -> str:
    """İşletim sisteminin dili.

    İlk açılışta hangi dille başlanacağını belirliyor. Bilgisayarı Türkçe olan
    biri uygulamayı da Türkçe görsün diye. Desteklemediğimiz bir dilse
    İngilizceye düşülüyor — Türkçe bilmeyen birine Türkçe arayüz açmak,
    ayarları bulup değiştirmesini bile zorlaştırıyor.

    Kullanıcı ayarlardan bir dil seçtiği anda bu algılama devre dışı kalıyor;
    seçim veritabanına yazılıyor ve bundan sonra o geçerli oluyor.

    **Önce Windows'un ekran diline bakılıyor**, sonra Qt'nin listesine.
    İkisi de cevap vermezse İngilizce.

    **`uiLanguages()` kullanılıyor, `name()` değil.** İkisi farklı şeyler:
    `name()` bölgesel biçimi veriyor (tarih ve sayı yazımı), `uiLanguages()`
    ise Windows'un arayüz dilini. Bu ikisi sık sık ayrışıyor — bu proje
    geliştirilen makinede `name()` `en_US` derken arayüz dili Türkçeydi.
    `name()` kullanılsaydı Türkçe bir Windows'ta uygulama İngilizce açılırdı.

    Liste tercih sırasında geliyor; desteklediğimiz ilk dil seçiliyor.
    """
    dogrudan = _windows_ui_language()
    if dogrudan:
        return dogrudan

    from PySide6.QtCore import QLocale

    for tag in QLocale.system().uiLanguages():
        code = tag.replace("_", "-").split("-")[0].lower()
        if code in AVAILABLE_LANGUAGES:
            return code
    return "en"


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

    def t_upper(self, key: str, **kwargs) -> str:
        """Çeviriyi alıp seçili dilin kurallarına göre büyütür."""
        return upper(self.t(key, **kwargs), self._language)

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
