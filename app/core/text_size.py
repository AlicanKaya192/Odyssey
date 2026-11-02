"""Yazı boyu ayarı (Ayarlar › Görünüm › Yazı boyu).

Ders, not, yönerge gibi okunan sayfaları, kod editörünü ve terminali birlikte
büyütüyor ya da küçültüyor. Menüler ve düğmeler aynı kalıyor: Windows'un
kendi ölçek ayarı onlar için var, burada değiştirilirse pencereler sığmazdı.

Kural burada; çağıran yerler anahtarı kendisi okumuyor.
"""

from __future__ import annotations

SETTING_KEY = "text_size"
DEFAULT = "normal"
SCALES = {"small": 0.9, "normal": 1.0, "large": 1.15, "xlarge": 1.3}


def current(store) -> str:
    """Seçili yazı boyunun adı; kayıt yoksa ya da bozuksa normal."""
    kayit = store.setting(SETTING_KEY, DEFAULT)
    return kayit if kayit in SCALES else DEFAULT


def set_size(store, name: str) -> None:
    if name not in SCALES:
        raise ValueError(f"bilinmeyen yazı boyu: {name!r}")
    store.set_setting(SETTING_KEY, name)


def scale(name: str) -> float:
    return SCALES.get(name, 1.0)
