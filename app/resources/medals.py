"""Rozet madalyaları.

Her rozet bir madalya olarak çiziliyor. Katmanlar alttan üste: gölge
elipsi, (efsanevide) kurdele ve defne dalı, dış şekil (kenar degradesi), iç
şekil (kademe degradesi), ince iç halka, işaretin koyu gölgesi, beyaz
işaret, üst parlama. Kazanılmamış rozet gri, işareti soluk ve sağ altında
kilit var.

- **Şekil** rozetin türünü söyler: alıştırma daire, bölüm/modül altıgen,
  sınav kalkan, seri/zaman tırtıklı daire, bilgi (okuma, not, veri) baklava.
- **Kademe** emeği söyler: ilk adım bronz, alışkanlık gümüş-mavi, emek
  altın, patika ustalığı efsanevi (mor, kurdele, defne, yıldız).

Şekil ve kademe `content/badges.json` içinde (`medal`), işaret yine
rozetin `icon` alanı. Her rozetin işareti eşsiz (rozet kuralı).

Yalnızca QSvgRenderer'ın çizebildiği öğeler kullanılıyor (path, circle,
rect, ellipse, linear/radialGradient, opacity, transform).
"""

from __future__ import annotations

import math
from functools import lru_cache

from PySide6.QtCore import QByteArray, QRectF, Qt
from PySide6.QtGui import QPainter, QPixmap
from PySide6.QtSvg import QSvgRenderer

from .theme.tokens import mix

TIERS = {
    "bronze": {"rim": ("#FDBA74", "#7C2D12"), "in": ("#EA7A3B", "#8A2E0B"), "ring": "#FFEDD5"},
    "silver": {"rim": ("#F8FAFC", "#64748B"), "in": ("#38BDF8", "#1D4ED8"), "ring": "#E0F2FE"},
    "gold": {"rim": ("#FEF9C3", "#A16207"), "in": ("#FDE047", "#D97706"), "ring": "#FEFCE8"},
    "legendary": {"rim": ("#F5D0FE", "#6D28D9"), "in": ("#A78BFA", "#4C1D95"), "ring": "#F3E8FF"},
    "locked": {"rim": ("#4B5563", "#1F2937"), "in": ("#374151", "#1F2937"), "ring": "#6B7280"},
}

# Kutlama kartında kademenin iki vurgu rengi (ışıma ve süre çizgisi).
TIER_ACCENTS = {
    "bronze": ("#FB923C", "#FDBA74"),
    "silver": ("#38BDF8", "#93C5FD"),
    "gold": ("#FBBF24", "#FDE68A"),
    "legendary": ("#A78BFA", "#F0ABFC"),
}


def _round_poly(pts: list[tuple[float, float]], r: float) -> str:
    """Köşeleri `r` kadar yuvarlatılmış kapalı çokgen yolu."""
    d = []
    n = len(pts)
    for i in range(n):
        p0, p1, p2 = pts[i - 1], pts[i], pts[(i + 1) % n]
        v1 = (p0[0] - p1[0], p0[1] - p1[1])
        v2 = (p2[0] - p1[0], p2[1] - p1[1])
        l1, l2 = math.hypot(*v1), math.hypot(*v2)
        k = min(r, l1 / 2, l2 / 2)
        a = (p1[0] + v1[0] / l1 * k, p1[1] + v1[1] / l1 * k)
        b = (p1[0] + v2[0] / l2 * k, p1[1] + v2[1] / l2 * k)
        d.append(f"{'L' if i else 'M'}{a[0]:.2f} {a[1]:.2f}Q{p1[0]:.2f} {p1[1]:.2f} {b[0]:.2f} {b[1]:.2f}")
    return "".join(d) + "Z"


def _shape(kind: str, s: float) -> str:
    """Madalyanın gövdesi; `s` ölçek (1 dış şekil, 0.8 iç şekil)."""
    if kind == "hex":
        r = 25 * s
        pts = [(32 + r * math.cos(math.pi / 3 * i - math.pi / 2), 30 + r * math.sin(math.pi / 3 * i - math.pi / 2)) for i in range(6)]
        return f'<path d="{_round_poly(pts, 5 * s)}"/>'
    if kind == "shield":
        return (f'<path transform="translate(32 30) scale({s}) translate(-32 -30)" '
                'd="M32 5c7 4.5 13 5.5 21 5.5v18c0 13-9.5 20-21 25.5C20.5 48.5 11 41.5 11 28.5v-18C19 10.5 25 9.5 32 5z"/>')
    if kind == "burst":
        pts = []
        for i in range(24):
            r = (22.5 if i % 2 else 25.5) * s
            a = math.pi / 12 * i - math.pi / 2
            pts.append((32 + r * math.cos(a), 30 + r * math.sin(a)))
        return f'<path d="{_round_poly(pts, 1.6 * s)}"/>'
    if kind == "square":
        return (f'<rect x="{32 - 22 * s:.2f}" y="{30 - 22 * s:.2f}" width="{44 * s:.2f}" height="{44 * s:.2f}" '
                f'rx="{12 * s:.2f}" transform="rotate(45 32 30)"/>')
    return f'<circle cx="32" cy="30" r="{24 * s:.2f}"/>'


# Rozet işaretleri: beyaz çizgi (2.2), 24'lük ızgara. Anahtar badges.json'daki `icon`.
GLYPHS: dict[str, str] = {
    "play": '<path fill="#fff" stroke="none" d="M9 6.2v11.6a1 1 0 0 0 1.5.9l9-5.8a1 1 0 0 0 0-1.8l-9-5.8A1 1 0 0 0 9 6.2z"/>',
    "code": '<path d="m8.5 7-5 5 5 5M15.5 7l5 5-5 5M13.5 5l-3 14"/>',
    "layers": '<path d="m12 3 9 4.5-9 4.5-9-4.5z" fill="#fff" fill-opacity=".35"/><path d="m3 12 9 4.5 9-4.5M3 16.5 12 21l9-4.5"/>',
    "check": '<path d="m5 12.5 4.5 4.5L19 7.5" stroke-width="3"/>',
    "star": '<path fill="#fff" stroke="none" d="m12 3 2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9z"/>',
    "flag": '<path d="M5 21V4"/><path fill="#fff" fill-opacity=".9" d="M5 4.5h12l-2.5 4 2.5 4H5z"/>',
    "target": '<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="4.5"/><circle cx="12" cy="12" r="1.4" fill="#fff"/>',
    "trophy": ('<path fill="#fff" fill-opacity=".35" d="M7 4h10v6a5 5 0 0 1-10 0z"/>'
               '<path d="M7 4h10v6a5 5 0 0 1-10 0zM7 6H4.5v1.5A3 3 0 0 0 7.5 10.5M17 6h2.5v1.5a3 3 0 0 1-3 3M12 15v3M8.5 20.5h7"/>'),
    "folder": ('<path fill="#fff" fill-opacity=".35" d="M3 7.5A1.5 1.5 0 0 1 4.5 6h4.3l2 2h8.7A1.5 1.5 0 0 1 21 9.5v8a1.5 1.5 0 0 1-1.5 1.5h-15A1.5 1.5 0 0 1 3 17.5z"/>'
               '<path d="M3 7.5A1.5 1.5 0 0 1 4.5 6h4.3l2 2h8.7A1.5 1.5 0 0 1 21 9.5v8a1.5 1.5 0 0 1-1.5 1.5h-15A1.5 1.5 0 0 1 3 17.5zM8 13.5h8M12 11v5"/>'),
    "flame": ('<path fill="#fff" stroke="none" d="M12 21.5c-4 0-7-2.8-7-6.7 0-3.5 2.5-5.6 3.9-7.5.3 2 1.3 3.4 2.6 3.9C11.1 7.8 12.2 4.6 15 2.5c.2 3.4 4 6.3 4 11.3 0 4.3-3 7.7-7 7.7z"/>'
              '<path fill="#000" fill-opacity=".18" stroke="none" d="M12 21c-1.9 0-3.3-1.3-3.3-3.2 0-2 1.6-3 2.4-4.4.5 1.2 1.3 1.9 2.2 2.1.3-1.5.9-2.8 2-3.6.4 2 1.3 3 1.3 5.2 0 2.2-2 3.9-4.6 3.9z"/>'),
    "calendar": '<rect x="3.5" y="5" width="17" height="15.5" rx="2.5"/><path d="M3.5 10h17M8 3v4M16 3v4"/><path d="m8.5 14.5 2.2 2.2 4.3-4.2" stroke-width="2.2"/>',
    "zap": '<path fill="#fff" stroke="none" d="M13.5 2.5 4.5 13.5h6.5l-1 8 9-11h-6.5z"/>',
    "book": ('<path fill="#fff" fill-opacity=".3" d="M3 5.5c3-1 6-1 9 1 3-2 6-2 9-1V19c-3-1-6-1-9 1-3-2-6-2-9-1z"/>'
             '<path d="M3 5.5c3-1 6-1 9 1 3-2 6-2 9-1V19c-3-1-6-1-9 1-3-2-6-2-9-1zM12 6.5V20"/>'),
    "notebook-pen": '<rect x="4" y="3" width="12" height="18" rx="2"/><path d="M7.5 8h5M7.5 12h3"/><path fill="#fff" d="m18.5 8.5 2 2-6 6-2.6.6.6-2.6z"/>',
    "repeat": '<path d="M17 3l3.5 3.5L17 10M3.5 11.5V10A3.5 3.5 0 0 1 7 6.5h13.5M7 21l-3.5-3.5L7 14M20.5 12.5V14a3.5 3.5 0 0 1-3.5 3.5H3.5"/>',
    "wrench": ('<path fill="#fff" fill-opacity=".3" d="M14.7 6.3a4 4 0 0 0 5 5L21 10a6 6 0 0 1-7.3 7.3L7 24 3.9 20.9l6.8-6.7A6 6 0 0 1 18 7l-1.3 1.3z"/>'
               '<path d="M14.5 5.5a4.5 4.5 0 0 0 4 6.8l1.8-1.8a5.8 5.8 0 0 1-6.9 6.9L6.3 20.5a2 2 0 0 1-2.8-2.8l3.1-3.1 4-4a5.8 5.8 0 0 1 6.9-6.9z"/>'),
    "shapes": ('<path fill="#fff" fill-opacity=".85" stroke="none" d="M7.5 3.5 12 11H3z"/><rect x="13.5" y="13.5" width="7" height="7" rx="1.5"/>'
               '<circle cx="7.5" cy="17" r="3.5"/><path d="M14 4h6v6h-6z" fill="#fff" fill-opacity=".35"/>'),
    "graduation-cap": '<path fill="#fff" fill-opacity=".9" stroke="none" d="m12 4 10 5-10 5L2 9z"/><path d="M6 11v5c3.5 2.7 8.5 2.7 12 0v-5M22 9v6"/>',
    "database": '<ellipse cx="12" cy="6" rx="7.5" ry="3" fill="#fff"/><path d="M4.5 6v12c0 1.7 3.4 3 7.5 3s7.5-1.3 7.5-3V6M4.5 12c0 1.7 3.4 3 7.5 3s7.5-1.3 7.5-3"/>',
    "chart": ('<path d="M4 20h16"/><rect x="5.5" y="12" width="3" height="6" rx="1" fill="#fff"/>'
              '<rect x="10.5" y="8" width="3" height="10" rx="1" fill="#fff"/><rect x="15.5" y="4.5" width="3" height="13.5" rx="1" fill="#fff"/>'),
    "search": '<circle cx="10.5" cy="10.5" r="6.5" fill="#fff" fill-opacity=".3"/><circle cx="10.5" cy="10.5" r="6.5"/><path d="m20 20-4.8-4.8" stroke-width="2.8"/>',
    "box": '<path fill="#fff" fill-opacity=".3" d="m12 3 8 4.5v9L12 21l-8-4.5v-9z"/><path d="m12 3 8 4.5v9L12 21l-8-4.5v-9zM4 7.5l8 4.5 8-4.5M12 12v9"/>',
    "shield": ('<path fill="#fff" fill-opacity=".3" d="M12 3c2.6 1.7 5 2.2 8 2.2V12c0 5-3.6 7.6-8 9.5C7.6 19.6 4 17 4 12V5.2c3 0 5.4-.5 8-2.2z"/>'
               '<path d="M12 3c2.6 1.7 5 2.2 8 2.2V12c0 5-3.6 7.6-8 9.5C7.6 19.6 4 17 4 12V5.2c3 0 5.4-.5 8-2.2zM8.5 12l2.5 2.5 4.5-5"/>'),
    "anchor": '<circle cx="12" cy="5" r="2.2"/><path d="M12 7.2V21M8 11h8M4.5 13.5A7.5 7.5 0 0 0 12 21a7.5 7.5 0 0 0 7.5-7.5"/>',
    "filter": '<path fill="#fff" fill-opacity=".35" d="M3.5 4.5h17l-6.5 8v6l-4 2v-8z"/><path d="M3.5 4.5h17l-6.5 8v6l-4 2v-8z"/>',
    "link-rings": '<circle cx="9" cy="12" r="5.5"/><circle cx="15" cy="12" r="5.5"/>',
    "frame": '<rect x="3.5" y="3.5" width="17" height="17" rx="2.5"/><path d="M3.5 9h17M9 9v11.5"/><rect x="11" y="11" width="7.5" height="7.5" rx="1" fill="#fff" fill-opacity=".45" stroke="none"/>',
    "crown": '<path fill="#fff" stroke="none" d="m3 8 4.5 3.5L12 4l4.5 7.5L21 8l-2 10.5H5z"/><path d="M5 21h14"/>',
    "network": ('<g stroke-width="1.4" stroke-opacity=".7"><path d="M5 7l7 5M5 17l7-5M12 12l7-5M12 12l7 5"/></g>'
                '<g fill="#fff" stroke="none"><circle cx="5" cy="7" r="2.3"/><circle cx="5" cy="17" r="2.3"/>'
                '<circle cx="12" cy="12" r="2.8"/><circle cx="19" cy="7" r="2.3"/><circle cx="19" cy="17" r="2.3"/></g>'),
    "wave": ('<path d="M3 19.5h18" stroke-width="1.4" stroke-opacity=".6"/>'
             '<path d="M3 12c1.5-6 3-6 4.5 0s3 6 4.5 0 3-6 4.5 0 3 6 4.5 0"/>'),
    "forecast": ('<path d="M3 17.5l4-4.5 3.5 2.5 3.5-6"/><path d="m14 9.5 6.5-5" stroke-dasharray="2 2.8"/>'
                 '<circle cx="14" cy="9.5" r="2.3" fill="#fff" stroke="none"/><path d="M3 21h18" stroke-width="1.4" stroke-opacity=".6"/>'),
    "hourglass": ('<path d="M6 3h12M6 21h12"/><path fill="#fff" fill-opacity=".3" d="M7.5 3v3.5L12 12l4.5-5.5V3z"/>'
                  '<path d="M7.5 3v3.5L12 12l-4.5 5.5V21M16.5 3v3.5L12 12l4.5 5.5V21"/>'
                  '<path fill="#fff" stroke="none" d="m9.2 20.2 2.8-3.6 2.8 3.6z"/>'),
    "cargo": ('<path d="M12 2v3" stroke-width="1.8"/><path d="M12 5 4.5 10M12 5l7.5 5" stroke-width="1.5"/>'
              '<rect x="3" y="10" width="18" height="10" rx="1.2" fill="#fff" fill-opacity=".3"/>'
              '<rect x="3" y="10" width="18" height="10" rx="1.2"/><path d="M7.5 12.5v5M12 12.5v5M16.5 12.5v5"/>'),
    "baton": ('<path d="M3.5 20.5 12.5 11.5" stroke-width="2.6"/><circle cx="4" cy="20" r="2.4" fill="#fff" stroke="none"/>'
              '<g fill="#fff" fill-opacity=".85" stroke-width="1.6"><rect x="11" y="2" width="6" height="6" rx="1.2"/>'
              '<rect x="16" y="9" width="6" height="6" rx="1.2"/><rect x="13" y="16" width="6" height="6" rx="1.2"/></g>'),
    "plane": ('<path fill="#fff" fill-opacity=".35" d="M21 3 2.5 10.5l7.5 3 3 7.5z"/>'
              '<path d="M21 3 2.5 10.5l7.5 3 3 7.5zM21 3 10 13.5"/>'
              '<path d="M3 17.5 6 14.5M5.5 20.5l3-3" stroke-width="1.6" stroke-opacity=".75"/>'),
    "braces-table": ('<path d="M6.5 4.5C5 4.5 4.5 5.3 4.5 6.5V10c0 1-.6 1.8-2 2 1.4.2 2 1 2 2v3.5c0 1.2.5 2 2 2"/>'
                     '<path d="M8.5 12h4.5m-2-2.3 2.3 2.3-2.3 2.3" stroke-width="2"/>'
                     '<rect x="15" y="5" width="7" height="14" rx="1.3" fill="#fff" fill-opacity=".35"/>'
                     '<rect x="15" y="5" width="7" height="14" rx="1.3"/><path d="M15 9.7h7M15 14.3h7M18.5 5v14" stroke-width="1.5"/>'),
    "plug": ('<path d="M9 2.5v4.5M15 2.5v4.5"/>'
             '<path fill="#fff" fill-opacity=".35" d="M6 7h12v3.5a6 6 0 0 1-12 0z"/>'
             '<path d="M6 7h12v3.5a6 6 0 0 1-12 0zM12 16.5v5"/>'),
    "ship": ('<g fill="#fff" fill-opacity=".9" stroke="none"><rect x="5.5" y="9" width="4" height="3.4" rx=".5"/>'
             '<rect x="10" y="9" width="4" height="3.4" rx=".5"/><rect x="14.5" y="9" width="4" height="3.4" rx=".5"/>'
             '<rect x="7.8" y="5.1" width="4" height="3.4" rx=".5"/><rect x="12.3" y="5.1" width="4" height="3.4" rx=".5"/></g>'
             '<path fill="#fff" fill-opacity=".35" d="M2.5 13.5h19l-2.5 5h-14z"/><path d="M2.5 13.5h19l-2.5 5h-14z"/>'
             '<path d="M2.5 21.5c1.6-1.2 3.1-1.2 4.7 0s3.1 1.2 4.7 0 3.1-1.2 4.7 0 3.1 1.2 4.7 0" stroke-width="1.6"/>'),
    "commit-dot": ('<path d="M2 12h5.5M16.5 12H22" stroke-width="2.2"/>'
                   '<circle cx="12" cy="12" r="4.5" fill="#fff" fill-opacity=".35"/><circle cx="12" cy="12" r="4.5"/>'
                   '<circle cx="12" cy="12" r="1.6" fill="#fff" stroke="none"/>'),
    "merge-join": ('<path d="M6 6.5c0 4.5 6 4.5 6 8.5M18 6.5c0 4.5-6 4.5-6 8.5M12 15v6"/>'
                   '<g fill="#fff" stroke="none"><circle cx="6" cy="4.5" r="2.4"/><circle cx="18" cy="4.5" r="2.4"/>'
                   '<circle cx="12" cy="15" r="3"/></g>'),
    "cloud-up": ('<path fill="#fff" fill-opacity=".35" d="M7 17.5a4.5 4.5 0 0 1-.6-9 6 6 0 0 1 11.4 1.1 4 4 0 0 1-.3 7.9z"/>'
                 '<path d="M7 17.5a4.5 4.5 0 0 1-.6-9 6 6 0 0 1 11.4 1.1 4 4 0 0 1-.3 7.9"/>'
                 '<path d="M12 21.5v-9m-3.2 3.2L12 12.5l3.2 3.2" stroke-width="2"/>'),
    "server-up": ('<rect x="4" y="13.5" width="16" height="7" rx="1.6" fill="#fff" fill-opacity=".3"/>'
                  '<rect x="4" y="13.5" width="16" height="7" rx="1.6"/><circle cx="8" cy="17" r="1.2" fill="#fff" stroke="none"/>'
                  '<path d="M16.5 17h-3" stroke-width="1.6"/><path d="M12 10.5V2.5m-3.5 3.5L12 2.5l3.5 3.5" stroke-width="2"/>'),
    "crud-grid": ('<rect x="3.5" y="3.5" width="7.5" height="7.5" rx="1.6" fill="#fff" stroke="none"/>'
                  '<rect x="13" y="3.5" width="7.5" height="7.5" rx="1.6" fill="#fff" fill-opacity=".6" stroke="none"/>'
                  '<rect x="3.5" y="13" width="7.5" height="7.5" rx="1.6" fill="#fff" fill-opacity=".6" stroke="none"/>'
                  '<rect x="13" y="13" width="7.5" height="7.5" rx="1.6" fill="#fff" fill-opacity=".25"/>'
                  '<rect x="13" y="13" width="7.5" height="7.5" rx="1.6"/>'),
    "model-serve": ('<rect x="2.5" y="4.5" width="12" height="15" rx="2" fill="#fff" fill-opacity=".3"/>'
                    '<rect x="2.5" y="4.5" width="12" height="15" rx="2"/>'
                    '<path d="M6.5 8.5l4 3.5-4 3.5M10.5 12H6.5" stroke-width="1.3" stroke-opacity=".8"/>'
                    '<g fill="#fff" stroke="none"><circle cx="6.5" cy="8.5" r="1.4"/><circle cx="10.5" cy="12" r="1.4"/>'
                    '<circle cx="6.5" cy="15.5" r="1.4"/></g><path d="M15 12h6.5m-2.5-2.5 2.5 2.5-2.5 2.5" stroke-width="1.9"/>'),
    "gateway": ('<path fill="#fff" fill-opacity=".3" d="M8 21v-8.5a4 4 0 0 1 8 0V21z"/>'
                '<path d="M4 21V10a8 8 0 0 1 16 0v11M8 21v-8.5a4 4 0 0 1 8 0V21M2.5 21h19"/>'),
    "git-graph": ('<path d="M6.5 3.5v17"/><path d="M6.5 6c0 3.5 11 2 11 5.5v1c0 3.5-11 2-11 5.5" stroke-width="1.6"/>'
                  '<g fill="#fff" stroke="none"><circle cx="6.5" cy="3.5" r="2.3"/><circle cx="6.5" cy="20.5" r="2.3"/>'
                  '<circle cx="17.5" cy="12" r="2.6"/><circle cx="6.5" cy="12" r="1.8"/></g>'),
    "parquet-columns": ('<g fill="#fff" fill-opacity=".3" stroke="none"><rect x="3.5" y="3.5" width="4.5" height="17" rx="1"/>'
                        '<rect x="16" y="3.5" width="4.5" height="17" rx="1"/></g>'
                        '<rect x="3.5" y="3.5" width="4.5" height="17" rx="1"/><rect x="16" y="3.5" width="4.5" height="17" rx="1"/>'
                        '<rect x="9.75" y="3.5" width="4.5" height="17" rx="1" fill="#fff" stroke="none"/>'
                        '<path d="M3.5 9.5H8M3.5 15H8M16 9.5h4.5M16 15h4.5" stroke-width="1.3"/>'),
    "file-query": ('<path d="M5 21.5v-19h8.5l4 4V11"/><path d="M13.5 2.5v4h4" stroke-width="1.5"/>'
                   '<path d="M8 9h6M8 12.5h3.5" stroke-width="1.4" stroke-opacity=".8"/>'
                   '<circle cx="15.5" cy="16" r="3.8" fill="#fff" fill-opacity=".35"/><circle cx="15.5" cy="16" r="3.8"/>'
                   '<path d="m18.3 18.8 3 3" stroke-width="2.2"/>'),
    "spark-burst": ('<path fill="#fff" stroke="none" d="M12 2.5l2.3 7.2 7.2 2.3-7.2 2.3L12 21.5l-2.3-7.2L2.5 12l7.2-2.3z"/>'
                    '<path d="M4.5 4.5l2 2M19.5 4.5l-2 2M4.5 19.5l2-2M19.5 19.5l-2-2" stroke-width="1.6"/>'),
    "data-pyramid": ('<g fill="#fff" stroke="none"><rect x="9" y="3" width="6" height="3.4" rx=".8"/>'
                     '<rect x="6.5" y="7.6" width="11" height="3.4" rx=".8" fill-opacity=".85"/>'
                     '<rect x="4" y="12.2" width="16" height="3.4" rx=".8" fill-opacity=".7"/>'
                     '<rect x="1.5" y="16.8" width="21" height="3.4" rx=".8" fill-opacity=".55"/></g>'),
    "growth-curve": ('<path d="M3.5 3v17.5H21" stroke-width="1.6"/>'
                     '<path d="M6 18.5c5.5 0 9.5-4 12-14.5" stroke-width="2.2"/>'
                     '<path d="M6 18.5c3-3.2 7-4.8 13.5-5" stroke-width="1.5" stroke-dasharray="2 2.4" stroke-opacity=".8"/>'
                     '<circle cx="18" cy="4" r="2.1" fill="#fff" stroke="none"/>'),
    "split-merge": ('<rect x="7" y="2.5" width="10" height="4" rx="1" fill="#fff" stroke="none"/>'
                    '<path d="M9.5 6.5 6 10.5M14.5 6.5l3.5 4M6 14l3.5 4M18 14l-3.5 4" stroke-width="1.6"/>'
                    '<rect x="2.5" y="10.5" width="7" height="3.5" rx="1"/><rect x="14.5" y="10.5" width="7" height="3.5" rx="1"/>'
                    '<rect x="5.5" y="18" width="13" height="3.5" rx="1" fill="#fff" fill-opacity=".55"/>'),
    "binary-tree": ('<path d="M12 5 6.5 12M12 5l5.5 7M6.5 12l-3 7M6.5 12l3 7" stroke-width="1.6"/>'
                    '<g fill="#fff" stroke="none"><circle cx="12" cy="4.5" r="2.7"/><circle cx="6.5" cy="12" r="2.3"/></g>'
                    '<circle cx="17.5" cy="12" r="2.3" fill="#fff" fill-opacity=".35"/>'
                    '<circle cx="3.5" cy="19.5" r="2" fill="#fff" fill-opacity=".35"/>'
                    '<circle cx="9.5" cy="19.5" r="2" fill="#fff" fill-opacity=".35"/>'),
    "chip": ('<rect x="6" y="6" width="12" height="12" rx="2" fill="#fff" fill-opacity=".3"/>'
             '<rect x="6" y="6" width="12" height="12" rx="2"/>'
             '<rect x="9.5" y="9.5" width="5" height="5" rx="1" fill="#fff" stroke="none"/>'
             '<path d="M9.5 2.5V6M14.5 2.5V6M9.5 18v3.5M14.5 18v3.5M2.5 9.5H6M2.5 14.5H6M18 9.5h3.5M18 14.5h3.5" stroke-width="1.6"/>'),
    "dp-grid": ('<rect x="3" y="3" width="18" height="18" rx="1.5"/>'
                '<path d="M9 3v18M15 3v18M3 9h18M3 15h18" stroke-width="1.2"/>'
                '<rect x="9" y="15" width="6" height="6" fill="#fff" fill-opacity=".45" stroke="none"/>'
                '<rect x="15" y="9" width="6" height="6" fill="#fff" fill-opacity=".45" stroke="none"/>'
                '<rect x="15" y="15" width="6" height="6" fill="#fff" stroke="none"/>'),
    "route-graph": ('<path d="M4.5 18.5 10 6M10 6l10 -1M10 6l5 9" stroke-width="1.2" stroke-opacity=".5"/>'
                    '<path d="M4.5 18.5 15 15l5-10" stroke-width="2.4"/>'
                    '<g fill="#fff" stroke="none"><circle cx="4.5" cy="18.5" r="2.4"/><circle cx="20" cy="5" r="2.4"/>'
                    '<circle cx="15" cy="15" r="2"/></g>'
                    '<circle cx="10" cy="6" r="2" fill="#fff" fill-opacity=".35"/>'),
    "bloom-bits": ('<circle cx="12" cy="4.5" r="2.4" fill="#fff" stroke="none"/>'
                   '<path d="M11 6.8 5 13.5M12 7v6.5M13 6.8l6 6.7" stroke-width="1.4"/>'
                   '<rect x="2" y="15" width="20" height="5" rx="1"/>'
                   '<path d="M6 15v5M10 15v5M14 15v5M18 15v5" stroke-width="1"/>'
                   '<g fill="#fff" stroke="none"><rect x="2" y="15" width="4" height="5"/><rect x="10" y="15" width="4" height="5"/>'
                   '<rect x="18" y="15" width="4" height="5"/></g>'),
    "network-star": ('<path d="M12 4l6.9 4v8L12 20l-6.9-4V8z" stroke-width="1.2" stroke-opacity=".55"/>'
                     '<path d="M12 12V4M12 12l6.9-4M12 12l6.9 4M12 12v8M12 12l-6.9 4M12 12 5.1 8" stroke-width="1.5"/>'
                     '<g fill="#fff" stroke="none"><circle cx="12" cy="12" r="3"/><circle cx="12" cy="4" r="1.7"/>'
                     '<circle cx="18.9" cy="8" r="1.7"/><circle cx="18.9" cy="16" r="1.7"/><circle cx="12" cy="20" r="1.7"/>'
                     '<circle cx="5.1" cy="16" r="1.7"/><circle cx="5.1" cy="8" r="1.7"/></g>'),
    "descent-steps": ('<path d="M2.5 4.5C5 14 8.5 19.5 12 19.5S19 14 21.5 4.5" stroke-width="1.6"/>'
                      '<g fill="#fff" stroke="none"><circle cx="4" cy="9" r="1.6" fill-opacity=".35"/>'
                      '<circle cx="6.6" cy="14.6" r="1.7" fill-opacity=".55"/><circle cx="9.2" cy="18.2" r="1.8" fill-opacity=".8"/>'
                      '<circle cx="12" cy="19.5" r="2.3"/></g>'),
    "centroid-rings": ('<g fill="#fff" stroke="none" fill-opacity=".6"><circle cx="3.5" cy="5" r="1.1"/><circle cx="8" cy="4" r="1.1"/>'
                       '<circle cx="5" cy="9.5" r="1.1"/><circle cx="16" cy="3.5" r="1.1"/><circle cx="20.5" cy="6" r="1.1"/>'
                       '<circle cx="17" cy="9.5" r="1.1"/><circle cx="8.5" cy="16.5" r="1.1"/><circle cx="13" cy="21" r="1.1"/>'
                       '<circle cx="15" cy="15.5" r="1.1"/></g>'
                       '<circle cx="5.6" cy="6.2" r="3.2" stroke-width="1.3"/><circle cx="17.8" cy="6.3" r="3.2" stroke-width="1.3"/>'
                       '<circle cx="12.1" cy="17.7" r="3.2" stroke-width="1.3"/>'
                       '<g fill="#fff" stroke="none"><circle cx="5.6" cy="6.2" r="1.3"/><circle cx="17.8" cy="6.3" r="1.3"/>'
                       '<circle cx="12.1" cy="17.7" r="1.3"/></g>'),
    "neural-layers": ('<path d="M4.5 8 12 4.5M4.5 8 12 12M4.5 8 12 19.5M4.5 16 12 4.5M4.5 16 12 12M4.5 16 12 19.5'
                      'M12 4.5 19.5 12M12 12h7.5M12 19.5l7.5-7.5" stroke-width="1" stroke-opacity=".6"/>'
                      '<g fill="#fff" stroke="none"><circle cx="4.5" cy="8" r="2"/><circle cx="4.5" cy="16" r="2"/>'
                      '<circle cx="12" cy="4.5" r="2"/><circle cx="12" cy="12" r="2"/><circle cx="12" cy="19.5" r="2"/>'
                      '<circle cx="19.5" cy="12" r="2.4"/></g>'),
    "sigmoid-split": ('<rect x="2.5" y="2.5" width="19" height="19" rx="2" stroke-width="1.2" stroke-opacity=".55"/>'
                      '<path d="M4 17.5C10 17.5 9.5 6.5 20 6.5" stroke-width="2"/>'
                      '<g fill="#fff" stroke="none"><circle cx="6" cy="8" r="1.4"/><circle cx="9" cy="5.5" r="1.4"/>'
                      '<circle cx="5.5" cy="12" r="1.4"/></g>'
                      '<g fill="#fff" stroke="none" fill-opacity=".55"><circle cx="15" cy="13" r="1.4"/>'
                      '<circle cx="18.5" cy="17" r="1.4"/><circle cx="14" cy="18.5" r="1.4"/></g>'),
    "folder-tree": ('<rect x="2.5" y="3" width="8" height="5.5" rx="1.2" stroke-width="1.5"/>'
                    '<path d="M6 8.5v10h5M6 13h5" stroke-width="1.4"/>'
                    '<rect x="11" y="10.3" width="10" height="5.2" rx="1.2" stroke-width="1.5"/>'
                    '<rect x="11" y="15.9" width="10" height="5.2" rx="1.2" stroke-width="1.5"/>'
                    '<g fill="#fff" stroke="none"><rect x="2.5" y="3" width="4" height="2" rx=".8"/></g>'),
    "regex-pattern": ('<path d="M7.5 3.5H4.5v17h3M16.5 3.5h3v17h-3" stroke-width="1.7"/>'
                      '<path d="M12 7v10M7.7 9.5l8.6 5M16.3 9.5l-8.6 5" stroke-width="1.8"/>'),
    "battery-pack": ('<rect x="2" y="6.5" width="17.5" height="11" rx="2.2" stroke-width="1.6"/>'
                     '<path d="M21.6 10.2v3.6" stroke-width="2.2"/>'
                     '<g fill="#fff" stroke="none"><rect x="4.6" y="9" width="3.4" height="6" rx=".7"/>'
                     '<rect x="9.1" y="9" width="3.4" height="6" rx=".7"/><rect x="13.6" y="9" width="3.4" height="6" rx=".7"/></g>'),
    "parallel-lanes": ('<path d="M5 6h12.5M5 12h12.5M5 18h12.5" stroke-width="1.8"/>'
                       '<path d="M15 3.5 18.5 6 15 8.5M15 9.5 18.5 12 15 14.5M15 15.5 18.5 18 15 20.5" stroke-width="1.6"/>'
                       '<g fill="#fff" stroke="none"><circle cx="3.5" cy="6" r="1.5"/><circle cx="3.5" cy="12" r="1.5"/>'
                       '<circle cx="3.5" cy="18" r="1.5"/></g>'),
    "bug-check": ('<ellipse cx="9.5" cy="13" rx="3.6" ry="4.6" stroke-width="1.6"/>'
                  '<path d="M9.5 8.6v8.8M5.9 11 3 9.5M5.9 15 3 16.5M13.1 11 15.5 10M7.8 8.7 6.5 6M11.2 8.7 12.5 6"'
                  ' stroke-width="1.4"/>'
                  '<path d="M14.5 18l2.3 2.3 4.7-5.3" stroke-width="2"/>'),
    "leak-drop": ('<path d="M12 2.5C9 7 6 10.5 6 14a6 6 0 0 0 12 0c0-3.5-3-7-6-11.5z" stroke-width="1.6"/>'
                  '<circle cx="12" cy="14" r="2.6" stroke-width="1.3"/>'
                  '<path d="M12 9.6v1.8M12 16.6v1.8M7.6 14h1.8M14.6 14h1.8" stroke-width="1.3"/>'),
    "gear-pair": ('<circle cx="9" cy="9.5" r="3.6" stroke-width="1.5"/>'
                  '<path d="M12.6 9.5L14.6 9.5M11.5 12L13 13.5M9 13.1L9 15.1M6.5 12L5 13.5M5.4 9.5L3.4 9.5'
                  'M6.5 7L5 5.5M9 5.9L9 3.9M11.5 7L13 5.5" stroke-width="2.1"/>'
                  '<circle cx="16.8" cy="16.6" r="2.5" stroke-width="1.3"/>'
                  '<path d="M19.3 16.6L20.8 16.6M18.1 18.8L18.8 20.1M15.6 18.8L14.8 20.1M14.3 16.6L12.8 16.6'
                  'M15.5 14.4L14.8 13.1M18.1 14.4L18.8 13.1" stroke-width="1.9"/>'
                  '<g fill="#fff" stroke="none"><circle cx="9" cy="9.5" r="1.3"/><circle cx="16.8" cy="16.6" r="0.9"/></g>'),
    "broadcast-grid": ('<rect x="3" y="2.5" width="18" height="4.5" rx="1" stroke-width="1.5"/>'
                       '<path d="M5.5 9.6 7 11.1l1.5-1.5M10.5 9.6 12 11.1l1.5-1.5M15.5 9.6 17 11.1l1.5-1.5"'
                       ' stroke-width="1.3"/>'
                       '<rect x="3" y="13" width="18" height="8.5" rx="1" stroke-width="1.5"/>'
                       '<path d="M9 13v8.5M15 13v8.5M3 17.25h18" stroke-width="1.1"/>'
                       '<g fill="#fff" stroke="none"><circle cx="6" cy="4.75" r="0.9"/><circle cx="12" cy="4.75" r="0.9"/>'
                       '<circle cx="18" cy="4.75" r="0.9"/></g>'),
    "pivot-arrows": ('<rect x="2.5" y="3.5" width="6" height="17" rx="1" stroke-width="1.5"/>'
                     '<path d="M2.5 9.2h6M2.5 14.8h6" stroke-width="1.1"/>'
                     '<rect x="11.5" y="13.5" width="10" height="6.5" rx="1" stroke-width="1.5"/>'
                     '<path d="M14.8 13.5v6.5M18.2 13.5v6.5" stroke-width="1.1"/>'
                     '<path d="M10.5 6c4.2 0 6.3 1.7 6.3 4.6" stroke-width="1.6"/>'
                     '<path d="M14.8 9.2l2 2 2-2" stroke-width="1.6"/>'),
    "bell-check": ('<path d="M2 19C6.5 19 8.2 5.5 12 5.5S17.5 19 22 19" stroke-width="1.6"/>'
                   '<path d="M2 19.5h20" stroke-width="1.2"/>'
                   '<path d="M17 15.4c1.1 2.2 2.4 3.6 4.5 3.6v.5H17z" fill="#fff" stroke="none"/>'
                   '<path d="M8.2 13.2l2.2 2.2 4.2-4.8" stroke-width="1.9"/>'),
    "array-chart": ('<rect x="3" y="3" width="18" height="18" rx="2" stroke-width="1.5"/>'
                    '<path d="M3 9h18M3 15h18M9 3v18M15 3v18" stroke-width="0.8"/>'
                    '<path d="M5.5 18l4.5-5 3.5 2.5 5-8" stroke-width="2.1"/>'
                    '<g fill="#fff" stroke="none"><circle cx="18.5" cy="7.5" r="1.6"/></g>'),
    "sealed-pipe": ('<rect x="2" y="13" width="20" height="5" rx="1" stroke-width="1.5"/>'
                    '<path d="M6 11v9M18 11v9" stroke-width="2"/>'
                    '<path d="M9.6 8V6a2.4 2.4 0 0 1 4.8 0v2" stroke-width="1.5"/>'
                    '<rect x="8.6" y="8" width="6.8" height="4.6" rx="0.8" fill="#fff" stroke="none"/>'),
    "fold-split": ('<rect x="2.5" y="5" width="19" height="14" rx="1.5" stroke-width="1.5"/>'
                   '<path d="M6.3 5v14M10.1 5v14M13.9 5v14M17.7 5v14" stroke-width="1"/>'
                   '<rect x="13.9" y="5" width="3.8" height="14" fill="#fff" stroke="none"/>'
                   '<path d="M15.8 2v2M15.8 20v2" stroke-width="1.4"/>'),
    "open-box": ('<path d="M4 12h16v8.5H4z" stroke-width="1.5"/>'
                 '<path d="M4 12 8.5 4.5h7" stroke-width="1.5"/>'
                 '<path d="M8 18v-2.5M12 18v-6.5M16 18v-4" stroke-width="2"/>'
                 '<g fill="#fff" stroke="none"><circle cx="12" cy="8.3" r="1.2"/></g>'),
    "model-stack": ('<path d="M12 3 21 7.5 12 12 3 7.5z" stroke-width="1.5"/>'
                    '<path d="M3 12l9 4.5 9-4.5M3 16.5l9 4.5 9-4.5" stroke-width="1.5"/>'
                    '<g fill="#fff" stroke="none"><circle cx="12" cy="7.5" r="1.5"/></g>'),
}


def _shadowed(glyph: str) -> str:
    """İşaretin 1 px aşağıdaki koyu kopyası (gölge)."""
    return glyph.replace('fill="#fff"', 'fill="#000"')


def medal_svg(shape: str, tier: str, glyph: str, earned: bool = True) -> str:
    """Madalyayı tam bir SVG belgesi olarak üretir (64x64 tuval)."""
    t = TIERS[tier if earned else "locked"]
    legendary = tier == "legendary" and earned
    g = GLYPHS.get(glyph, GLYPHS["star"])
    rim_mid = mix(t["rim"][1], "#FFFFFF", 0.25)

    ribbon = laurel = ""
    if legendary:
        ribbon = ('<path d="M20 40 14 60l7-3.5 4 6 5-19z" fill="url(#r)"/>'
                  '<path d="M44 40l6 20-7-3.5-4 6-5-19z" fill="url(#r)"/>')
        # Her kolda bir sap (yay) ve sapın dışına doğru eğik yapraklar.
        R = 28.0

        def nokta(derece: float, r: float = R) -> tuple[float, float]:
            a = math.radians(derece)
            return 32 + r * math.cos(a), 30 + r * math.sin(a)

        sx, sy = nokta(100)
        ex, ey = nokta(205)
        rx2, ry2 = nokta(80)
        fx, fy = nokta(-25)
        saplar = (f'<path d="M{sx:.2f} {sy:.2f}A{R} {R} 0 0 1 {ex:.2f} {ey:.2f}'
                  f'M{rx2:.2f} {ry2:.2f}A{R} {R} 0 0 0 {fx:.2f} {fy:.2f}" '
                  'fill="none" stroke="#CA8A04" stroke-width="1.4" stroke-linecap="round"/>')
        yapraklar = []
        for i in range(7):
            for aci_derece, yon in ((108 + i * 15, -1), (72 - i * 15, 1)):
                x, y = nokta(aci_derece, R + 2.2)
                don = aci_derece + (90 if yon < 0 else -90) + yon * 32
                yapraklar.append(f'<ellipse cx="{x:.2f}" cy="{y:.2f}" rx="1.9" ry="4.2" transform="rotate({don:.1f} {x:.2f} {y:.2f})"/>')
        laurel = (f'{saplar}<g fill="url(#l)">{"".join(yapraklar)}</g>'
                  '<path d="M32 1.5l1.9 3.9 4.3.6-3.1 3 .7 4.3L32 11.3l-3.8 2 .7-4.3-3.1-3 4.3-.6z" '
                  'fill="#FDE68A" stroke="#B45309" stroke-width=".6"/>')

    kilit = "" if earned else (
        '<g transform="translate(42 38)"><circle cx="7" cy="7" r="8" fill="#1F2937" stroke="#4B5563"/>'
        '<rect x="3.8" y="6.5" width="6.4" height="5" rx="1.2" fill="#9CA3AF"/>'
        '<path d="M5 6.5V5.2a2 2 0 0 1 4 0v1.3" fill="none" stroke="#9CA3AF" stroke-width="1.4"/></g>'
    )
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><defs>'
        f'<linearGradient id="a" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{t["rim"][0]}"/>'
        f'<stop offset=".55" stop-color="{rim_mid}"/><stop offset="1" stop-color="{t["rim"][1]}"/></linearGradient>'
        f'<linearGradient id="b" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{t["in"][0]}"/>'
        f'<stop offset="1" stop-color="{t["in"][1]}"/></linearGradient>'
        '<linearGradient id="r" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#A78BFA"/><stop offset="1" stop-color="#5B21B6"/></linearGradient>'
        '<linearGradient id="l" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FDE68A"/><stop offset="1" stop-color="#CA8A04"/></linearGradient>'
        '<radialGradient id="s" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#000" stop-opacity=".35"/>'
        '<stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient></defs>'
        '<ellipse cx="32" cy="58" rx="20" ry="4" fill="url(#s)"/>'
        f'{ribbon}{laurel}'
        f'<g fill="url(#a)">{_shape(shape, 1)}</g>'
        f'<g fill="url(#b)">{_shape(shape, 0.8)}</g>'
        f'<g fill="none" stroke="{t["ring"]}" stroke-opacity=".35" stroke-width="1">{_shape(shape, 0.72)}</g>'
        '<g transform="translate(20 19)" fill="none" stroke-linecap="round" stroke-linejoin="round">'
        + (f'<g stroke="#000" stroke-opacity=".22" stroke-width="2.2" fill-opacity=".22" transform="translate(0 1)">{_shadowed(g)}</g>' if earned else "")
        + f'<g stroke="#fff" stroke-width="2.2" opacity="{1 if earned else .45}">{g}</g></g>'
        f'<path d="M15 22a17 12 0 0 1 34 0c-9-4-25-4-34 0z" fill="#fff" fill-opacity="{.28 if earned else .08}"/>'
        f'{kilit}</svg>'
    )


@lru_cache(maxsize=256)
def medal_pixmap(shape: str, tier: str, glyph: str, size: int, earned: bool = True, ratio: float = 2.0) -> QPixmap:
    """Madalyayı `size` piksel (mantıksal) boyutunda pixmap olarak verir."""
    renderer = QSvgRenderer(QByteArray(medal_svg(shape, tier, glyph, earned).encode("utf-8")))
    kenar = max(1, round(size * ratio))
    pix = QPixmap(kenar, kenar)
    pix.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pix)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    renderer.render(painter, QRectF(0, 0, kenar, kenar))
    painter.end()
    pix.setDevicePixelRatio(ratio)
    return pix


def tier_of(badge: dict) -> str:
    return (badge.get("medal") or ["circle", "bronze"])[1]
