## numpy.random

| Yazım | Ne verir |
|---|---|
| `rng = np.random.default_rng(42)` | tohumlu üreteç |
| `rng.integers(1, 7, size=5)` | 1–6 tam sayı (bitiş hariç) |
| `rng.random(3)` | 0–1 ondalık |
| `rng.normal(ort, sapma, adet)` | normal dağılım |
| `rng.choice(a, size=, p=, replace=)` | seçim |
| `rng.permutation(x)` | karışık kopya |
| `rng.shuffle(x)` | `x`'i yerinde karıştırır |
| `rng.spawn(n)` | bağımsız n üreteç |

## numpy.linalg

| Yazım | Ne yapar |
|---|---|
| `A @ B` | matris çarpımı (`*` eleman eleman) |
| `np.linalg.solve(A, b)` | `A x = b` |
| `np.linalg.inv(A)` | ters (gerekmedikçe `solve`) |
| `np.linalg.det(A)` | determinant |
| `np.linalg.matrix_rank(A)` | rank |
| `np.linalg.cond(A)` | koşul sayısı (büyükse tehlike) |
| `np.linalg.norm(v)` | uzunluk |
| `np.linalg.eigh(A)` / `eigvalsh` | simetrik matrisin özdeğer/vektörleri |
| `np.linalg.lstsq(X, y, rcond=None)` | en küçük kareler |

## Hatalar

| Belirti | Sebep |
|---|---|
| Sayılar her çalıştırmada farklı | tohum yok |
| Başka bir çağrı sırayı kaydırdı | küresel `np.random.seed` |
| `LinAlgError: Singular matrix` | satırlar birbirinin katı |
| Sonuç anlamsız büyük | neredeyse tekil (`cond` büyük) |
| Beklenmedik matris şekli | `*` yerine `@` gerekiyordu |
