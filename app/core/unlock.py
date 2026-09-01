"""Bölüm kilidi.

Bir modülün bölümleri sırayla açılıyor: ilk bölüm hep açık, sonrakiler bir
öncekini tamamlayınca açılıyor. Tamamlanmak, bölümün kendi şartlarını
karşılamak demek — sınavı geçmek ve alıştırmaları çözmek (hangisi
`section.json`'da isteniyorsa).

**Kural burada, tek yerde.** Yol ekranı, ders altındaki ileri düğmesi ve
bölümü doğrudan açan çağrı üçü de buraya soruyor; yoksa biri kilidi
uygularken diğeri arka kapı bırakıyor.

Zincir kırılırsa: yalnızca **bir önceki** bölüme bakılıyor, hepsine değil.
Bu güncellemeden önce ilerlemiş bir kullanıcının kayıtları sırasız olabilir
(2'yi atlayıp 3'ü bitirmiş olabilir); ona "geri dön ve 2'yi de yap" demek
yerine kaldığı yerden devam etmesine izin veriliyor.

Ayarlardan **kilit kaldırılabiliyor**. O ayar açıkken bu modül her bölüm
için "açık" diyor. Kontrol burada yapılıyor, çağıran yerlerde değil: üç
çağrı noktası var ve biri ayarı unutursa o ekran kilidi uygulamaya devam
ederdi.
"""

from __future__ import annotations

# Ayarlar penceresindeki "kilidi kaldır" anahtarının veritabanı anahtarı.
UNLOCK_ALL_KEY = "unlock_all"


def unlock_all(store) -> bool:
    """Kullanıcı kilidi kaldırmayı seçmiş mi?"""
    return store.setting(UNLOCK_ALL_KEY, "") == "1"


def _completed(store, chapter_id: str, section) -> bool:
    state = store.section_state(chapter_id, section.id, len(section.exercises))
    return (
        state.status(section.requires_quiz, section.requires_exercises) == "completed"
    )


def blocking_section(catalog, store, chapter_id: str, section_id: str):
    """Bu bölümün önünü kapatan bölümü döndürür; kilit yoksa `None`.

    Dönen nesne bölümün kendisi; çağıran adını mesajda kullanıyor.
    """
    if unlock_all(store):
        return None

    chapter = catalog.chapter(chapter_id)
    if chapter is None:
        return None

    sections = chapter.sections
    for index, section in enumerate(sections):
        if section.id != section_id:
            continue
        if index == 0:
            return None
        onceki = sections[index - 1]
        return None if _completed(store, chapter_id, onceki) else onceki

    # Bilinmeyen bölüm: kilitlemiyoruz, kilit bir güvenlik önlemi değil.
    return None


def is_unlocked(catalog, store, chapter_id: str, section_id: str) -> bool:
    """Bölüme girilebilir mi?"""
    return blocking_section(catalog, store, chapter_id, section_id) is None
