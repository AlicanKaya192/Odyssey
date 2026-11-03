import numpy as np

RATES = np.array([0.04, 0.05])
VISITORS, BATCH = 10000, 250


def fixed_split(seed):
    rng = np.random.default_rng(seed)
    arm = rng.integers(0, 2, VISITORS)
    bought = rng.random(VISITORS) < RATES[arm]
    return np.bincount(arm, minlength=2), np.bincount(arm, bought, 2)


def thompson(seed):
    rng = np.random.default_rng(seed)
    n = np.zeros(2)
    k = np.zeros(2)
    for _ in range(VISITORS // BATCH):
        draws = rng.beta(1 + k, 1 + n - k, (BATCH, 2))
        arm = draws.argmax(axis=1)
        bought = rng.random(BATCH) < RATES[arm]
        n += np.bincount(arm, minlength=2)
        k += np.bincount(arm, bought, 2)
    return n, k

# İki yöntem için (önce fixed_split, sonra thompson) 100 koşu (seed 0..99)
# yap. Her koşuda pişmanlığı (en iyi kolla beklenen satış - gerçek satış) ve
# iyi kolun (1. kol) aldığı trafik payını hesapla. Her yöntem için iki
# ortalamayı aynı satırda yaz (1 ve 3 basamak).
