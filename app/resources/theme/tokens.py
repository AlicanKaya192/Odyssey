"""Tasarım belirteçleri: renkler, boşluklar, köşe yarıçapları, yazı tipleri.

Arayüzdeki hiçbir renk veya ölçü doğrudan widget'ın içine yazılmaz; hepsi
buradan gelir. Böylece tema değiştirmek veya boşlukları topluca ayarlamak
tek dosyayı düzenlemekle mümkün oluyor.

Ferahlığın büyük kısmı SPACING ölçeğinden geliyor. Qt'nin varsayılan kenar
boşlukları çok dar; burada 8px tabanlı bir ölçek kullanıp ekranlarda bilinçli
olarak büyük değerleri tercih ediyoruz.
"""

from __future__ import annotations

# --- Boşluk ölçeği (8px tabanlı) -------------------------------------------
# Ara değer gerektiğinde 4 kullanılabilir ama kural 8'in katlarıdır.
SPACING = {
    "xs": 4,
    "sm": 8,
    "md": 16,
    "lg": 24,
    "xl": 32,
    "xxl": 48,
}

# --- Köşe yarıçapları ------------------------------------------------------
RADIUS = {
    "sm": 6,
    "md": 10,
    "lg": 14,
    "pill": 999,
}

# --- Yazı tipleri ----------------------------------------------------------
FONTS = {
    # Windows 11'de Segoe UI Variable var, yoksa Segoe UI'a düşer.
    "ui": '"Segoe UI Variable Text", "Segoe UI", "Inter", sans-serif',
    "mono": '"Cascadia Code", "Cascadia Mono", "Consolas", monospace',
}

FONT_SIZES = {
    "xs": 12,
    "sm": 13,
    "md": 14,     # gövde metni
    "lg": 16,
    "xl": 20,
    "xxl": 26,    # sayfa başlığı
}

# Ders metninin en fazla kaç piksel genişleyebileceği. Satırlar ekran boyunca
# uzarsa göz satır başını kaybediyor; bu sınır yaklaşık 75 karaktere denk gelir.
READING_WIDTH = 760

# --- Renk paletleri --------------------------------------------------------
# Nötr bir zemin ve tek bir vurgu rengi. Doğru/yanlış geri bildirimi renkle
# birlikte ikonla da veriliyor, sadece renge güvenmiyoruz.

LIGHT = {
    "bg": "#FBFBFD",            # pencere zemini
    "surface": "#FFFFFF",       # kartlar, içerik alanı
    "surface_alt": "#F4F5F7",   # kenar çubuğu, ikincil yüzeyler
    "surface_hover": "#EDEFF3",
    "border": "#E4E6EB",
    "border_strong": "#D0D4DB",

    "text": "#1A1D21",
    "text_muted": "#6B7280",
    "text_inverse": "#FFFFFF",

    "accent": "#4F46E5",
    "accent_hover": "#4338CA",
    "accent_soft": "#EEF0FE",

    "success": "#15803D",
    "success_soft": "#ECFDF3",
    "danger": "#B91C1C",
    "danger_soft": "#FEF2F2",
    "warning": "#B45309",
    "warning_soft": "#FFFBEB",

    "code_bg": "#F6F7F9",
    "shadow": "rgba(16, 24, 40, 0.06)",
}

DARK = {
    "bg": "#16181D",
    "surface": "#1C1F26",
    "surface_alt": "#22262E",
    "surface_hover": "#2A2F38",
    "border": "#2E333D",
    "border_strong": "#3C424E",

    "text": "#E8EAED",
    "text_muted": "#9AA0AA",
    "text_inverse": "#16181D",

    "accent": "#7C74F0",
    "accent_hover": "#8F88F5",
    "accent_soft": "#262640",

    "success": "#4ADE80",
    "success_soft": "#16281E",
    "danger": "#F87171",
    "danger_soft": "#2A1A1C",
    "warning": "#FBBF24",
    "warning_soft": "#2A2314",

    "code_bg": "#181B21",
    "shadow": "rgba(0, 0, 0, 0.35)",
}

PALETTES = {
    "light": LIGHT,
    "dark": DARK,
}


def build_variables(mode: str) -> dict[str, str]:
    """Seçilen temanın tüm belirteçlerini tek bir sözlükte toplar.

    QSS şablonundaki ``{isim}`` yer tutucuları bu sözlükle doldurulur.
    """
    palette = PALETTES.get(mode, LIGHT)

    variables: dict[str, str] = dict(palette)
    variables.update({f"space_{k}": str(v) for k, v in SPACING.items()})
    variables.update({f"radius_{k}": str(v) for k, v in RADIUS.items()})
    variables.update({f"font_{k}": str(v) for k, v in FONT_SIZES.items()})
    variables["font_ui"] = FONTS["ui"]
    variables["font_mono"] = FONTS["mono"]
    return variables
