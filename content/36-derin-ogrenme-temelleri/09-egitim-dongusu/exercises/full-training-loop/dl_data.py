"""Derin Öğrenme alıştırmalarının sabit tohumlu verisi (yalnızca NumPy).

Her fonksiyon aynı tohumla her makinede aynı diziyi verir (NumPy'nin
`default_rng`'si platformdan bağımsız). Görüntüler [0, 1] aralığında
float32, kanal önce: (adet, 1, yükseklik, genişlik).

Fonksiyonlar:
  make_table(n, seed)            tablo verisi: 6 özellik, 3 sınıf
  make_shapes(n, size, seed)     daire / kare / üçgen görüntüleri ve etiketleri
  make_scenes(n, size, seed)     birden çok şekilli sahne, kutular ve bölütleme maskesi
  make_series(n, seed)           mevsimli, eğilimli günlük seri
  make_sensor(n, length, seed)   sensör pencereleri; bir kısmında arıza deseni
  make_sequences(n, length, seed) sayı dizileri ve "içinde 3-5 var mı" etiketi
  TEXT                            karakter düzeyinde dil modeli için kısa metin
"""

import numpy as np

SHAPES = ("circle", "square", "triangle")


def make_table(n=600, seed=7):
    """6 özellik, 3 sınıf; sınıflar örtüşüyor (doğruluk %100 olmaz)."""
    rng = np.random.default_rng(seed)
    y = rng.integers(0, 3, n)
    centers = np.array([[0, 0, 1, 0, 0, 1], [1.5, 1, 0, 0, 1, 0], [0, 2, 0, 1.5, 0, 0]], dtype=np.float64)
    x = centers[y] + rng.normal(0, 0.9, (n, 6))
    return x.astype(np.float32), y.astype(np.int64)


def _draw(kind, size, cx, cy, r):
    yy, xx = np.mgrid[0:size, 0:size].astype(np.float32)
    if kind == "circle":
        return ((xx - cx) ** 2 + (yy - cy) ** 2 <= r * r).astype(np.float32)
    if kind == "square":
        return ((np.abs(xx - cx) <= r * 0.85) & (np.abs(yy - cy) <= r * 0.85)).astype(np.float32)
    # üçgen: tepe yukarıda, taban aşağıda
    top, bottom = cy - r, cy + r
    inside_y = (yy >= top) & (yy <= bottom)
    half = (yy - top) / (2 * r) * r
    return (inside_y & (np.abs(xx - cx) <= half)).astype(np.float32)


def make_shapes(n=300, size=16, seed=7, noise=0.1):
    """Tek şekilli görüntüler: (n, 1, size, size) float32 ve 0/1/2 etiketleri."""
    rng = np.random.default_rng(seed)
    images = np.zeros((n, 1, size, size), dtype=np.float32)
    labels = rng.integers(0, 3, n)
    for i, label in enumerate(labels):
        r = rng.uniform(size * 0.2, size * 0.32)
        cx = rng.uniform(r + 1, size - r - 1)
        cy = rng.uniform(r + 1, size - r - 1)
        img = _draw(SHAPES[label], size, cx, cy, r) * rng.uniform(0.6, 1.0)
        img += rng.normal(0, noise, (size, size))
        images[i, 0] = np.clip(img, 0, 1)
    return images, labels.astype(np.int64)


def make_scenes(n=100, size=32, seed=7, max_objects=3):
    """Sahneler: görüntüler, kutular ve maske.

    boxes[i] = [[x1, y1, x2, y2, sınıf], ...] (tam sayı piksel, x2/y2 dahil değil);
    masks[i] = (size, size) int64, 0 arka plan, 1 + sınıf şeklin pikselleri.
    """
    rng = np.random.default_rng(seed)
    images = np.zeros((n, 1, size, size), dtype=np.float32)
    masks = np.zeros((n, size, size), dtype=np.int64)
    boxes = []
    for i in range(n):
        scene = []
        for _ in range(rng.integers(1, max_objects + 1)):
            label = int(rng.integers(0, 3))
            r = rng.uniform(size * 0.1, size * 0.18)
            cx = rng.uniform(r + 1, size - r - 1)
            cy = rng.uniform(r + 1, size - r - 1)
            shape = _draw(SHAPES[label], size, cx, cy, r)
            ys, xs = np.nonzero(shape)
            if len(xs) == 0:
                continue
            images[i, 0] = np.maximum(images[i, 0], shape * rng.uniform(0.6, 1.0))
            masks[i][shape > 0] = label + 1
            scene.append([int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1, label])
        images[i, 0] = np.clip(images[i, 0] + rng.normal(0, 0.05, (size, size)), 0, 1)
        boxes.append(scene)
    return images, boxes, masks


def make_series(n=730, seed=7):
    """Günlük seri: eğilim + haftalık ve yıllık mevsim + gürültü (float32)."""
    rng = np.random.default_rng(seed)
    t = np.arange(n, dtype=np.float64)
    series = (50 + 0.02 * t + 8 * np.sin(2 * np.pi * t / 7) + 15 * np.sin(2 * np.pi * t / 365.25)
              + rng.normal(0, 2, n))
    return series.astype(np.float32)


def make_sensor(n=400, length=64, seed=7, fault_rate=0.3):
    """Sensör pencereleri (n, length) ve 0/1 arıza etiketi.

    Sağlam pencere: dalga + gürültü. Arızalı pencerede rastgele bir yerde
    kısa, sert bir sıçrama ve titreşim var.
    """
    rng = np.random.default_rng(seed)
    t = np.arange(length, dtype=np.float64)
    x = np.zeros((n, length), dtype=np.float32)
    y = (rng.random(n) < fault_rate).astype(np.int64)
    for i in range(n):
        wave = np.sin(2 * np.pi * t / rng.uniform(12, 20) + rng.uniform(0, 6.28)) + rng.normal(0, 0.2, length)
        if y[i]:
            start = rng.integers(5, length - 12)
            wave[start:start + 8] += rng.choice([-1, 1]) * rng.uniform(1.5, 2.5) + rng.normal(0, 0.6, 8)
        x[i] = wave
    return x, y


def make_sequences(n=500, length=12, seed=7):
    """0–9 arası sayı dizileri (n, length) int64 ve etiket: içinde art arda 3, 5 var mı."""
    rng = np.random.default_rng(seed)
    x = rng.integers(0, 10, (n, length))
    plant = rng.random(n) < 0.5
    for i in np.nonzero(plant)[0]:
        pos = rng.integers(0, length - 1)
        x[i, pos], x[i, pos + 1] = 3, 5
    y = np.array([any(a == 3 and b == 5 for a, b in zip(row[:-1], row[1:])) for row in x], dtype=np.int64)
    return x.astype(np.int64), y


TEXT = (
    "the cat sat on the mat. the dog sat on the log. the cat saw the dog. "
    "the dog saw the cat and the cat ran. a bird sat on the tree. the bird sang. "
    "the cat and the dog sat in the sun. the sun was warm and the day was long. "
    "a small cat ran to the tree. the bird flew from the tree to the log. "
)
