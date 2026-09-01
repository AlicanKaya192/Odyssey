"""Tasarım belirteçleri: renkler, boşluklar, köşe yarıçapları, yazı tipleri.

Arayüzdeki hiçbir renk veya ölçü doğrudan widget'ın içine yazılmaz; hepsi
buradan gelir. Böylece tema değiştirmek veya boşlukları topluca ayarlamak
tek dosyayı düzenlemekle mümkün oluyor.

Değerler `Plan/tasarim/maket.html` maketiyle birebir aynı tutuluyor; maket
değişirse burası da değişir.
"""

from __future__ import annotations

# --- Boşluk ölçeği (8px tabanlı) -------------------------------------------
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
    # Segment düğmesi gibi kabın içine oturan küçük parçalar için.
    "xs": 6,
    "sm": 8,
    "md": 12,
    "lg": 18,
    "xl": 24,
    "pill": 999,
}

# --- Yazı tipleri ----------------------------------------------------------
FONTS = {
    # Sıra platforma göre çalışıyor: Windows ilk ikisini bulup duruyor,
    # macOS onları bulamayıp SF Pro'ya, Linux ise Inter/Ubuntu'ya düşüyor.
    # Sonda yalnızca `sans-serif` kalsaydı, Windows dışında Qt'nin varsayılan
    # yazı tipi çıkıyordu ve arayüz bambaşka görünüyordu.
    "ui": (
        '"Segoe UI Variable Text", "Segoe UI", '        # Windows
        '"SF Pro Text", "Helvetica Neue", '             # macOS
        '"Inter", "Ubuntu", "Noto Sans", '              # Linux
        "sans-serif"
    ),
    # Ligatürsüz yazı tipleri önde.
    #
    # "Cascadia Code" programcı ligatürleri taşıyor: `>=` ekranda tek bir `≥`
    # işareti olarak çiziliyor, `!=` `≠` oluyor. Deneyimli birine hoş
    # görünüyor ama burada Python'u yeni öğrenen biri var ve o işareti
    # klavyesinde bulamıyor. "Cascadia Mono" aynı yazı tipinin ligatürsüz
    # hâli; görünüm birebir aynı kalıyor, yalnızca işaretler yazıldığı gibi
    # görünüyor.
    "mono": (
        '"Cascadia Mono", "Consolas", '                   # Windows
        '"SF Mono", "Menlo", '                            # macOS
        '"DejaVu Sans Mono", "Liberation Mono", '         # Linux
        "monospace"
    ),
}

FONT_SIZES = {
    "xs": 12,
    "sm": 13,
    "md": 15,     # gövde metni
    "lg": 17,
    "xl": 20,
    "xxl": 24,
    "display": 31,  # ders başlığı
}

# Ders metninin en fazla kaç piksel genişleyebileceği. Yaklaşık 70 karaktere
# denk gelir; tipografi araştırmalarında rahat okuma aralığı 45-75 karakter.
READING_WIDTH = 680

# Sağdaki sayfa içi başlık listesinin genişliği.
TOC_WIDTH = 250

# Öğrenme yolu ve modül kartlarının kapladığı sütun genişliği. Maketteki
# ölçü; içerik ekranın ortasında toplanıyor, uçlara yayılmıyor.
CONTENT_WIDTH = 820

# Sol ikon şeridinin genişliği.
RAIL_WIDTH = 76

# --- Renk paletleri --------------------------------------------------------

# Açık tema, koyu temaya göre yorucu buluyordu ve ölçüm bunu doğruladı:
# sayfa parlaklığı 0.938, kartlar saf beyaz (1.000). Göz saatlerce en
# yüksek parlaklığa bakıyordu. Daha ağırı, soluk metin koyuda 7.2:1
# okunurken açıkta 4.8:1'de kalıyordu — süre, "Başlanmadı", sayfa içi
# başlık listesi hep o renkle yazılıyor.
#
# Değerler koyu temanın rakamlarına göre seçildi, göz kararıyla değil:
#
#                  önce      şimdi     koyu tema
#   sayfa L        0.938     0.836       0.006
#   gövde metni    17.2:1    15.4:1     15.9:1
#   soluk / yüzey   5.1:1     6.8:1      6.7:1
#
# Gövde metninin kontrastı biraz düştü ama 15:1 zaten fazlasıyla yeterli
# (AA eşiği 4.5:1); kazanç, parlaklığın gözü yormayan bir yere inmesi.
LIGHT = {
    "bg": "#E8ECF2",
    "surface": "#F8F9FC",
    "surface_alt": "#DDE3EC",
    # Sol şerit sayfadan bir ton daha derin duruyor; böylece
    # zeminden ayrılıyor ama ayrı bir yama gibi görünmüyor.
    "rail_bg": "#DFE4EC",
    "danger_hover": "#B91C1C",
    "surface_hover": "#DCE2EA",
    "border": "#CFD5E0",
    "border_strong": "#B7BFCD",

    "text": "#12151A",
    "text_muted": "#4E5867",
    "text_inverse": "#FFFFFF",

    "accent": "#4F46E5",
    "accent_hover": "#4338CA",
    "accent_soft": "#E4E7FC",
    "accent_second": "#7C3AED",   # karşılama kartındaki geçiş rengi

    "success": "#15803D",
    "success_soft": "#DFF5E8",
    "danger": "#B91C1C",
    "danger_soft": "#FBE4E4",
    "warning": "#B45309",
    "warning_soft": "#FBF1D9",

    "code_bg": "#E9EDF3",
    # Qt'nin stil dosyaları gölgeyi desteklemiyor; gölgeler
    # QGraphicsDropShadowEffect ile veriliyor, renkleri burada.
    "shadow": (16, 24, 40, 26),
    "shadow_strong": (16, 24, 40, 42),
}

DARK = {
    "bg": "#0F1116",
    "surface": "#171A21",
    "surface_alt": "#1D212A",
    "rail_bg": "#0A0C11",
    "danger_hover": "#F87171",
    "surface_hover": "#262B36",
    "border": "#272C36",
    "border_strong": "#39404E",

    "text": "#E9ECF1",
    "text_muted": "#98A1AF",
    "text_inverse": "#0F1116",

    "accent": "#8B84FF",
    "accent_hover": "#9E98FF",
    "accent_soft": "#221F3D",
    "accent_second": "#6D5BF5",

    "success": "#4ADE80",
    "success_soft": "#12251A",
    "danger": "#F87171",
    "danger_soft": "#2A1618",
    "warning": "#FBBF24",
    "warning_soft": "#2A2212",

    "code_bg": "#12151B",
    "shadow": (0, 0, 0, 90),
    "shadow_strong": (0, 0, 0, 140),
}

PALETTES = {
    "light": LIGHT,
    "dark": DARK,
}

# --- Kod renklendirme ------------------------------------------------------

SYNTAX_LIGHT = {
    "keyword": "#8B31C7",
    "constant": "#B45309",
    "builtin": "#1D4ED8",
    "string": "#15803D",
    "number": "#B45309",
    "comment": "#8A9099",
    "definition": "#B8860B",
    "decorator": "#0E7490",
    # Değer atanan değişken adı. Makette turuncu; kodun neresinde tanım
    # yapıldığı tek bakışta görünüyor.
    "variable": "#C2410C",
}

SYNTAX_DARK = {
    "keyword": "#C792EA",
    "constant": "#F78C6C",
    "builtin": "#82AAFF",
    "string": "#C3E88D",
    "number": "#F78C6C",
    "comment": "#5F6773",
    "definition": "#FFCB6B",
    "decorator": "#89DDFF",
    "variable": "#F78C6C",
}

SYNTAX = {
    "light": SYNTAX_LIGHT,
    "dark": SYNTAX_DARK,
}

# --- Şerit simgelerinin renkleri -------------------------------------------
# Makette her bölümün simgesi kendi renginde. Tek renk şeridi cansız
# bırakıyor; renkler ayrıca "hangi bölümdeyim" sorusunu simgeye bakmadan
# cevaplıyor. Koyu ve açık tema için ayrı tonlar, ikisinde de okunaklı olsun.
RAIL_COLORS = {
    "light": {
        "journey": "#4F46E5",
        "profile": "#0E7490",
        "about": "#B45309",
        "releases": "#BE185D",
        "settings": "#6B7280",
    },
    "dark": {
        "journey": "#8B84FF",
        "profile": "#22D3EE",
        "about": "#FBBF24",
        "releases": "#F472B6",
        "settings": "#98A1AF",
    },
}


# --- Bölüm durumları -------------------------------------------------------
# Yol ekranındaki düğümlerin görünümü. Renge ek olarak simge de var, çünkü
# durumu yalnızca renkle anlatmak renk körü kullanıcıyı dışarıda bırakır.
#
# `not_started` için simge yok: kilit kaldırıldığı için asma kilit yanıltıcı
# olurdu, boş yuvarlak da bomboş duruyordu. Onun yerine bölümün sıra numarası
# yazılıyor — hem doluluk veriyor hem "kaçıncı bölümdeyim" sorusunu cevaplıyor.
NODE_STATES = {
    "completed": {"symbol": "✓", "color": "success"},
    "current": {"symbol": "▶", "color": "accent"},
    "in_progress": {"symbol": "◐", "color": "warning"},
    "not_started": {"symbol": "", "color": "border_strong"},
    # Önündeki bölüm bitmeden açılmıyor. Simge yerine sıra numarası
    # duruyor; kilidi kesik çerçeve ve soluk renk anlatıyor, altındaki
    # açıklama da hangi bölümün beklendiğini yazıyor.
    "locked": {"symbol": "", "color": "border_strong"},
}


def build_variables(mode: str) -> dict[str, str]:
    """Seçilen temanın tüm belirteçlerini tek bir sözlükte toplar.

    QSS şablonundaki yer tutucular bu sözlükle doldurulur. Gölge renkleri
    demet olarak saklandığı için dışarıda bırakılıyor.
    """
    palette = PALETTES.get(mode, LIGHT)

    variables: dict[str, str] = {
        key: value for key, value in palette.items() if isinstance(value, str)
    }
    variables.update({f"space_{k}": str(v) for k, v in SPACING.items()})
    variables.update({f"radius_{k}": str(v) for k, v in RADIUS.items()})
    variables.update({f"font_{k}": str(v) for k, v in FONT_SIZES.items()})
    variables["font_ui"] = FONTS["ui"]
    variables["font_mono"] = FONTS["mono"]
    return variables


def shadow_color(mode: str, strong: bool = False) -> tuple[int, int, int, int]:
    """Gölge rengini (r, g, b, alfa) olarak döndürür."""
    palette = PALETTES.get(mode, LIGHT)
    return palette["shadow_strong"] if strong else palette["shadow"]
