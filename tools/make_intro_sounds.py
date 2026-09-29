"""Açılış animasyonunun sesini üretir: `app/resources/sounds/intro.wav`.

Üç ses var, hepsi animasyonun kendi zamanlarına oturuyor (`app/ui/intro.py`):

- **Nal sesleri:** toprakta dörtnal; her vuruş dörtnal döngüsünün bir
  toynağın yere bastığı ana denk geliyor. Uzaktan yaklaşıyor, ok atılıp
  kamera uzaklaşınca sönüyor.
- **Rüzgâr:** ok uçarken yumuşak, hafif esintili bir hava sesi; hedefe
  yaklaşırken çekiliyor ki vuruş net duyulsun.
- **Vuruş:** ok tahta hedefe saplanınca kısa, kuru bir "tık".

İlk sürümde lir notaları, kiriş sesi, gümbürtü ve geçiş hışırtısı da vardı;
Alican "birbirine uyumu yok" dedi, sade üçlüye inildi. Sesler sentezleniyor:
tonal (sinüs) bir gövde yerine süzülmüş gürültü ve tahtanın doğal
titreşimleri kullanılıyor, yapay "bip" hissi buradan geliyordu.

`winsound` aynı anda tek ses çaldığı için sahnenin sesi tek kayıt. Animasyonun
zamanlaması değişirse bu araç yeniden çalıştırılır.

Kullanım: `.venv\\Scripts\\python tools\\make_intro_sounds.py`
"""

from __future__ import annotations

import sys
import wave
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.ui import intro as I  # noqa: E402
from app.widgets import centaur as C  # noqa: E402

RATE = 44100
PEAK = 0.34
OUT = ROOT / "app" / "resources" / "sounds"
rng = np.random.default_rng(5)


def t_axis(seconds: float) -> np.ndarray:
    return np.arange(int(seconds * RATE)) / RATE


def place(track: np.ndarray, sound: np.ndarray, at: float, gain: float = 1.0) -> None:
    start = int(at * RATE)
    if start >= len(track):
        return
    end = min(len(track), start + len(sound))
    track[start:end] += sound[: end - start] * gain


def lowpass(x: np.ndarray, cutoff: float, poles: int = 1) -> np.ndarray:
    a = np.exp(-2 * np.pi * cutoff / RATE)
    for _ in range(poles):
        y = np.empty_like(x)
        acc = 0.0
        for i, v in enumerate(x):
            acc = (1 - a) * v + a * acc
            y[i] = acc
        x = y
    return x


def bandpass(x: np.ndarray, centre: float, q: float) -> np.ndarray:
    w0 = 2 * np.pi * centre / RATE
    alpha = np.sin(w0) / (2 * q)
    b0, a0, a1, a2 = alpha, 1 + alpha, -2 * np.cos(w0), 1 - alpha
    y = np.zeros_like(x)
    x1 = x2 = y1 = y2 = 0.0
    for i, v in enumerate(x):
        out = (b0 * v - b0 * x2 - a1 * y1 - a2 * y2) / a0
        x2, x1, y2, y1 = x1, v, y1, out
        y[i] = out
    return y


def env(t: np.ndarray, attack: float, decay: float) -> np.ndarray:
    return np.clip(t / attack, 0, 1) * np.exp(-np.clip(t - attack, 0, None) / decay)


def norm(x: np.ndarray) -> np.ndarray:
    return x / (np.max(np.abs(x)) or 1.0)


def hoof() -> np.ndarray:
    """Toprakta bir toynak: boğuk güm, gövde tınısı, toprak serpintisi."""
    t = t_axis(0.14)
    noise = rng.uniform(-1, 1, len(t))
    thump = norm(lowpass(noise, 140, poles=2)) * env(t, 0.0015, 0.030)
    body = norm(bandpass(noise, 300 * rng.uniform(0.9, 1.1), 1.3)) * env(t, 0.001, 0.020)
    grit = norm(bandpass(rng.uniform(-1, 1, len(t)), 2300, 0.8)) * env(t, 0.0005, 0.009)
    return thump * 1.0 + body * 0.45 + grit * 0.16


def gallop(total: float) -> np.ndarray:
    track = np.zeros(int(total * RATE))
    end = I.T_RELEASE + 0.7
    n = 0
    while n * I.GALLOP_PERIOD < end:
        for key in ("hf", "hn", "ff", "fn"):
            kind = "f" if key[0] == "f" else "h"
            at = (n + (C.STANCE[kind][0] - C.OFFSET[key]) % 1.0) * I.GALLOP_PERIOD
            at += rng.uniform(-0.005, 0.005)
            if not 0.05 < at < end:
                continue
            # Uzaktan yaklaşıyor; ok atılınca kamera uzaklaşıyor.
            near = min(1.0, 0.3 + 0.7 * at / 0.9)
            away = 1.0 if at < I.T_RELEASE else max(0.0, 1 - (at - I.T_RELEASE) / 0.6)
            weight = 1.0 if kind == "f" else 0.85  # ön ayaklar biraz daha tok
            place(track, hoof(), at, near * away * weight * rng.uniform(0.85, 1.0))
        n += 1
    return track


def wind(total: float) -> np.ndarray:
    """Ok uçarken hava: yumuşak, hafif esintili; hedefe yaklaşırken çekiliyor."""
    t = t_axis(total)
    noise = rng.uniform(-1, 1, len(t))
    air = norm(lowpass(noise, 850, poles=2)) * 0.8 + norm(bandpass(noise, 520, 0.6)) * 0.35
    gust = 1 + 0.16 * np.sin(2 * np.pi * 2.3 * t + 1.0) + 0.08 * np.sin(2 * np.pi * 5.1 * t)
    on = np.clip((t - I.T_RELEASE) / 0.18, 0, 1)
    off = np.clip((I.T_HIT - t) / 0.22, 0, 1)
    shape = on * off * (0.8 + 0.2 * np.sin(np.pi * np.clip((t - I.T_RELEASE) / (I.T_HIT - I.T_RELEASE), 0, 1)))
    return air * gust * shape


def hit() -> np.ndarray:
    """Oka saplanan tahta: kısa, kuru bir tık; tahtanın birkaç doğal titreşimi."""
    t = t_axis(0.3)
    knock = np.zeros_like(t)
    for freq, decay, amp in ((540, 0.055, 1.0), (1180, 0.032, 0.55), (2070, 0.018, 0.32), (3350, 0.010, 0.18)):
        knock += amp * np.sin(2 * np.pi * freq * t + rng.uniform(0, 6.28)) * env(t, 0.0008, decay)
    click = norm(bandpass(rng.uniform(-1, 1, len(t)), 4200, 0.9)) * env(t, 0.0002, 0.0025)
    thud = np.sin(2 * np.pi * 105 * t) * env(t, 0.001, 0.03)
    return knock * 0.8 + click * 0.45 + thud * 0.4


def room(x: np.ndarray) -> np.ndarray:
    """Çok hafif bir oda yansıması: sesler birbirine yapışsın, kuru durmasın."""
    y = x.copy()
    for delay, gain in ((0.019, 0.16), (0.031, 0.11), (0.047, 0.08), (0.071, 0.05)):
        d = int(delay * RATE)
        y[d:] += lowpass(x[:-d], 2500) * gain
    return y


def write(name: str, x: np.ndarray) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    x = x - np.mean(x)
    x = x / (np.max(np.abs(x)) or 1.0) * PEAK
    fade = int(0.04 * RATE)
    x[-fade:] *= np.linspace(1, 0, fade)
    x[:64] *= np.linspace(0, 1, 64)
    path = OUT / name
    with wave.open(str(path), "wb") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(RATE)
        f.writeframes((np.clip(x, -1, 1) * 32767).astype("<i2").tobytes())
    print(f"{path.name}: {len(x) / RATE:.2f} sn, {path.stat().st_size // 1024} KB")


def main() -> None:
    total = I.T_HIT + 0.45
    mix = gallop(total) * 0.95 + wind(total) * 0.36
    place(mix, hit(), I.T_HIT, 1.0)
    write("intro.wav", room(mix))
    # Eski sürümün dosyaları (lir, geçiş) artık kullanılmıyor.
    for old in ("intro_title.wav", "intro_out.wav"):
        (OUT / old).unlink(missing_ok=True)


if __name__ == "__main__":
    main()
