"""Kutlama kartlarının seslerini üretir: `app/resources/sounds/*.wav`.

Sesler hazır bir dosyadan alınmıyor, burada sentezleniyor: lisans sorunu
yok, istenirse tonu değiştirip yeniden üretmek tek komut.

- `section.wav` — bölüm tamamlandı: yükselen iki notalı yumuşak çan.
- `badge.wav` — yeni rozet: dört notalı parlak bir arpej.
- `level.wav` — seviye atlandı: üç notalık kısa bir çıkış ve uzun tınlayan bir akor.
- `timer.wav` — zamanlayıcıda evre bitti: yumuşak, inen iki nota (irkiltmesin).

Kullanım: `.venv\\Scripts\\python tools\\make_sounds.py`
"""

from __future__ import annotations

import math
import struct
import wave
from pathlib import Path

RATE = 44100
PEAK = 0.32  # tam ölçeğin ~%32'si (yaklaşık -10 dBFS): duyulur ama irkiltmez
OUT = Path(__file__).resolve().parent.parent / "app" / "resources" / "sounds"


def bell(freq: float, start: float, length: float, decay: float, total: float) -> list[float]:
    """Tek bir çan notası: temel ton + birkaç üst ton, hızlı giriş, üstel sönüm."""
    samples = [0.0] * int(total * RATE)
    first = int(start * RATE)
    count = min(int(length * RATE), len(samples) - first)
    partials = ((1.0, 1.0), (2.0, 0.28), (3.0, 0.10), (4.2, 0.05))
    for i in range(count):
        t = i / RATE
        attack = min(1.0, t / 0.004)
        env = attack * math.exp(-t / decay)
        value = 0.0
        for ratio, amp in partials:
            # Üst tonlar daha çabuk sönüyor; ses tınlıyor ama cızırdamıyor.
            value += amp * math.exp(-t * ratio / (decay * 2.2)) * math.sin(2 * math.pi * freq * ratio * t)
        samples[first + i] = value * env
    return samples


def mix(*tracks: list[float]) -> list[float]:
    length = max(len(t) for t in tracks)
    out = [0.0] * length
    for track in tracks:
        for i, v in enumerate(track):
            out[i] += v
    return out


def finish(samples: list[float]) -> list[float]:
    """Tepeyi PEAK'e ölçekler, sonda 30 ms'de sıfıra iner (tık sesi olmasın)."""
    peak = max(abs(v) for v in samples) or 1.0
    scaled = [v / peak * PEAK for v in samples]
    fade = int(0.03 * RATE)
    for i in range(fade):
        scaled[-1 - i] *= i / fade
    return scaled


def write(name: str, samples: list[float]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    with wave.open(str(path), "wb") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(RATE)
        f.writeframes(b"".join(struct.pack("<h", int(max(-1.0, min(1.0, v)) * 32767)) for v in samples))
    print(f"{path.name}: {len(samples) / RATE:.2f} sn, {path.stat().st_size // 1024} KB")


def main() -> None:
    # Bölüm: Sol5 → Do6, ikincisi biraz uzun kalıyor.
    total = 0.9
    write("section.wav", finish(mix(
        bell(783.99, 0.00, 0.6, 0.18, total),
        bell(1046.50, 0.12, 0.78, 0.26, total),
    )))
    # Rozet: Do6 Mi6 Sol6 Do7 arpeji, sonuncusu tınlıyor.
    total = 1.1
    notes = ((1046.50, 0.00, 0.14), (1318.51, 0.07, 0.14), (1567.98, 0.14, 0.16), (2093.00, 0.21, 0.32))
    write("badge.wav", finish(mix(*(bell(f, s, total - s, d, total) for f, s, d in notes))))
    # Seviye: Sol5 Do6 Mi6 hızlı çıkış, ardından Do6 + Sol6 + Do7 akoru tınlıyor.
    # Rozet arpejinden ayrılsın diye daha pes başlıyor ve akorla bitiyor.
    total = 1.5
    rise = ((783.99, 0.00, 0.12), (1046.50, 0.09, 0.12), (1318.51, 0.18, 0.14))
    chord = ((1046.50, 0.30, 0.50), (1567.98, 0.30, 0.46), (2093.00, 0.32, 0.40))
    write("level.wav", finish(mix(*(bell(f, s, total - s, d, total) for f, s, d in rise + chord))))
    # Zamanlayıcı: Mi6 → Si5, yavaş sönen iki yumuşak nota. Kutlama değil,
    # bir haber; o yüzden inen ve daha alçak.
    total = 1.4
    write("timer.wav", finish(mix(
        bell(1318.51, 0.00, 1.0, 0.30, total),
        bell(987.77, 0.28, 1.1, 0.40, total),
    )))


if __name__ == "__main__":
    main()
