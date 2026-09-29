"""Hareket belirteçleri: süreler, eğriler, mesafeler.

Arayüzdeki hiçbir animasyon süresini ya da eğrisini kendisi seçmez; hepsi
buradan gelir. Değerler `Plan/tasarim/ui-taslak.md` §2 ile birebir aynı ve
prototip (`Plan/tasarim/prototip.html`) de aynı değerleri kullanıyor.

İki yay eğrisi var. Qt'nin hazır eğrileri (`OutBack` gibi) hedefi aşıp bir
kez geri dönüyor; yay ise yumuşakça salınıp oturuyor ve bu, "esnek" hissini
veren şey. Eğri sönümlü salınımın kapalı çözümü:

    x(t) = 1 − e^(−ζωt) · (cos ω_d t + (ζω / ω_d) · sin ω_d t)

`ω = ln(500) / ζ` seçildiği için süre bitince hedefin %0,2 içinde oluyor;
son karede 1'e sabitleniyor.
"""

from __future__ import annotations

import math

# --- Süreler (ms) ----------------------------------------------------------
DURATION = {
    "micro": 120,      # üzerine gelme rengi, basma geri bildirimi
    "short": 180,      # açılır panel, sekme içeriği, liste seçimi
    "base": 240,       # sayfa geçişi (eski sayfanın sönmesi), kart kalkması
    "long": 360,       # başlık çizgisi, yol çizgisinin dolması
    "count": 700,      # sayı sayma, ilerleme çubuğu dolması
    "celebrate": 900,  # halka dalgası, parıltı
    "spring": 420,     # yayla yerine oturan girişler
    "bounce": 560,     # esneyerek beliren "pop" anları
}

# Sıralı girişte iki öğe arası; en fazla `STAGGER_CAP` öğe gecikir.
STAGGER_MS = 40
STAGGER_CAP = 8

# --- Mesafeler (px) --------------------------------------------------------
DISTANCE = {
    "rise": 8,    # liste ve kart girişi
    "page": 16,   # sayfa geçişinde yeni sayfanın kayması
    "depth": 24,  # ileri / geri gezinmede yatay kayma
    "shake": 4,   # yanlış cevap sallanması
}

# --- Yay eğrileri ----------------------------------------------------------
# ζ (sönüm): küçüldükçe daha çok salınır.
SPRING_DAMPING = 0.72   # en fazla %3,8 taşma: yumuşak iniş
BOUNCE_DAMPING = 0.50   # en fazla %16 taşma: esnek zıplama


def spring_curve(t: float, damping: float) -> float:
    """Sönümlü yay: 0 → 1, aradaki taşma `damping`'e bağlı."""
    if t <= 0.0:
        return 0.0
    if t >= 1.0:
        return 1.0
    omega = math.log(500) / damping
    omega_d = omega * math.sqrt(1 - damping * damping)
    zarf = math.exp(-damping * omega * t)
    return 1 - zarf * (math.cos(omega_d * t) + damping * omega / omega_d * math.sin(omega_d * t))


def spring(t: float) -> float:
    return spring_curve(t, SPRING_DAMPING)


def bounce(t: float) -> float:
    return spring_curve(t, BOUNCE_DAMPING)


def out_cubic(t: float) -> float:
    return 1 - (1 - t) ** 3


def in_cubic(t: float) -> float:
    return t ** 3


def in_out_cubic(t: float) -> float:
    return 4 * t ** 3 if t < 0.5 else 1 - (-2 * t + 2) ** 3 / 2


EASING = {
    "out": out_cubic,
    "in": in_cubic,
    "inout": in_out_cubic,
    "spring": spring,
    "bounce": bounce,
    "linear": lambda t: t,
}
