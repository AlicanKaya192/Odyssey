"""Uygulamanın kendi simgesi.

Pencere başlığında, görev çubuğunda ve paketlenmiş `.exe` dosyasında görünen
simge. Varsayılan bırakılırsa Python'un logosu ya da Windows'un boş belge
simgesi çıkıyor; ikisi de uygulamanın kendisini anlatmıyor.

**Tasarım fikri:** yükselen bir yol üzerinde düğümler, en tepede bir yıldız.

Odysseus yolunu yıldızlara bakarak bulurdu; yıldız varılacak yeri gösteriyor.
Dolu düğümler geride kalan bölümleri, aralarındaki çizgi de yolu anlatıyor —
uygulamanın ana ekranı zaten bu. Yükselen çizgi ayrıca bir veri grafiğine
benziyor; konu veri bilimi.

Harf kullanılmadı: bir harf uygulamanın ne yaptığını söylemiyor.

Renkler `tokens.py`'den geliyor, elle yazılmıyor.
"""

from __future__ import annotations

from .theme.tokens import LIGHT

# Simge 512x512 tuval üzerine çiziliyor, küçük boyutlara oradan ölçekleniyor.
CANVAS = 512

# Yolun düğümleri: soldan sağa yükseliyor. Sonuncusu yıldızın yeri.
NODES = [(146, 380), (256, 306)]
STAR_CENTER = (372, 176)

NODE_RADIUS = 40
LINE_WIDTH = 28
STAR_RADIUS = 78


def _star_points(cx: float, cy: float, outer: float, inner_ratio: float = 0.42) -> str:
    """Dört uçlu bir yıldızın köşe noktalarını üretir.

    Dört uç bilinçli: beş ya da altı uçlu yıldız 16 piksele indiğinde
    bulanıklaşıyor, dört uçlu olan keskin kalıyor.
    """
    inner = outer * inner_ratio
    points = [
        (cx, cy - outer),
        (cx + inner, cy - inner),
        (cx + outer, cy),
        (cx + inner, cy + inner),
        (cx, cy + outer),
        (cx - inner, cy + inner),
        (cx - outer, cy),
        (cx - inner, cy - inner),
    ]
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in points)


def icon_svg(
    accent: str | None = None,
    second: str | None = None,
    radius: int = 112,
) -> str:
    """Uygulama simgesini SVG olarak üretir."""
    accent = accent or LIGHT["accent"]
    second = second or LIGHT["accent_second"]

    path_points = [*NODES, STAR_CENTER]
    path = " ".join(
        f"{'M' if index == 0 else 'L'}{x} {y}"
        for index, (x, y) in enumerate(path_points)
    )

    circles = "".join(
        f'<circle cx="{x}" cy="{y}" r="{NODE_RADIUS}" fill="#FFFFFF"/>'
        for x, y in NODES
    )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CANVAS} {CANVAS}">
  <defs>
    <linearGradient id="zemin" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{accent}"/>
      <stop offset="1" stop-color="{second}"/>
    </linearGradient>
  </defs>

  <rect width="{CANVAS}" height="{CANVAS}" rx="{radius}" fill="url(#zemin)"/>

  <!-- Yol: düğümleri yıldıza bağlayan yükselen çizgi. -->
  <path d="{path}" fill="none" stroke="#FFFFFF" stroke-width="{LINE_WIDTH}"
        stroke-linecap="round" stroke-linejoin="round" stroke-opacity="0.5"/>

  <!-- Geride kalan bölümler. -->
  {circles}

  <!-- Varılacak yer: yolu gösteren yıldız. -->
  <polygon points="{_star_points(*STAR_CENTER, STAR_RADIUS)}" fill="#FFFFFF"/>
</svg>"""
