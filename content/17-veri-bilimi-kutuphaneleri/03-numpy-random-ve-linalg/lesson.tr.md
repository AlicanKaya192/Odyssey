# numpy.random ve linalg

Veri biliminde iki iş sürekli tekrar eder: **rastgele sayı üretmek** (veri
bölmek, benzetim yapmak, model başlatmak) ve **doğrusal cebir** (matris
çarpımı, denklem çözmek, en küçük kareler). NumPy'nin bunlar için iki alt
modülü var: `numpy.random` ve `numpy.linalg`. Bu bölüm ikisinin de doğru
kullanımını ve sık yapılan hatalarını anlatıyor. Matematiğin kendisi
Matematik patikasında; burada kodu var.

## Generator: tekrarlanabilir rastgelelik

```python
import numpy as np

rng = np.random.default_rng(42)
print(rng.integers(1, 7, size=5))
print(rng.random(3).round(3), rng.normal(0, 1, 2).round(3))
first = np.random.default_rng(42).integers(1, 7, size=5)
again = np.random.default_rng(42).integers(1, 7, size=5)
print((first == again).all())
```

```text
[1 5 4 3 3]
[0.697 0.094 0.976] [ 0.128 -0.316]
True
```

- **`np.random.default_rng(tohum)`** bir **üreteç** (Generator) kurar. Sayılar
  onun metotlarından gelir: `integers` (bitiş dahil değil: 1–6 zar),
  `random` (0–1 ondalık), `normal(ortalama, sapma, adet)`.
- Aynı tohum → aynı sayılar. Bir deneyin, bir veri bölmenin
  tekrarlanabilmesi bu sayede.
- Eski yazım `np.random.seed(42)` + `np.random.rand()` **küresel** bir durum
  kullanır: programın başka yerindeki bir çağrı sırayı kaydırır. Yeni kodda
  her iş kendi üretecini kullanır (Python Başlangıç'taki `random.Random`
  ile aynı fikir).

## Seçmek, karıştırmak, bağımsız akışlar

```python
import numpy as np

rng = np.random.default_rng(0)
print(rng.choice(["a", "b", "c"], size=5, p=[0.6, 0.3, 0.1]))
print(rng.choice(10, size=4, replace=False))
rng = np.random.default_rng(0)
x = np.arange(6)
print(rng.permutation(x), x)
rng.shuffle(x)
print(x)
child1, child2 = np.random.default_rng(5).spawn(2)
print(child1.integers(100), child2.integers(100))
```

```text
['b' 'a' 'a' 'a' 'b']
[4 7 8 6]
[3 2 5 4 0 1] [0 1 2 3 4 5]
[4 5 1 2 0 3]
22 53
```

- **`choice(..., p=...)`** olasılıklarla seçer; **`replace=False`** tekrarsız
  (bir kişi iki kez seçilmez).
- **`permutation(x)`** karışık bir **kopya** döndürür, `x`'e dokunmaz;
  **`shuffle(x)`** `x`'in **kendisini** karıştırır.
- **`spawn(n)`** bir üreteçten birbirinden bağımsız n üreteç türetir: paralel
  işlerin her biri kendi akışını alır, çakışma olmaz.

## Matris çarpımı ve denklem çözmek

```python
import numpy as np

A = np.array([[2.0, 1], [1, 3]])
b = np.array([3.0, 5])
print(A @ np.array([1, 2]), A * np.array([1, 2]))
x = np.linalg.solve(A, b)
print(x.round(3), np.allclose(A @ x, b))
print(np.linalg.inv(A).round(3).tolist(), round(float(np.linalg.det(A)), 6))
```

```text
[4. 7.] [[2. 2.]
 [1. 6.]]
[0.8 1.4] True
[[0.6, -0.2], [-0.2, 0.4]] 5.0
```

- **`@`** matris çarpımıdır (`np.matmul`): `[2·1 + 1·2, 1·1 + 3·2] = [4, 7]`.
  **`*`** eleman eleman çarpar: vektörü her satıra yayıp 2 × 2 bir matris
  verdi. İkisi çok farklı sonuç; karıştırmak sessiz bir hatadır.
- **`np.linalg.solve(A, b)`** `A x = b` denklemini çözer: `2x + y = 3`,
  `x + 3y = 5` → `x = 0.8`, `y = 1.4`. `np.allclose` ile doğrulama.
- `np.linalg.inv(A) @ b` de aynı sonucu verir ama **daha yavaş ve daha az
  kesin**; tersi açıkça gerekmiyorsa `solve` kullanılır.
- `det` sıfırsa (ya da çok küçükse) matrisin tersi yoktur.

## Tekil matris ve koşul sayısı

```python
import numpy as np

S = np.array([[1.0, 2], [2, 4]])
try:
    np.linalg.solve(S, [1, 2])
except np.linalg.LinAlgError as error:
    print("LinAlgError:", error)
print(np.linalg.matrix_rank(S))
A = np.array([[2.0, 1], [1, 3]])
almost = np.array([[1, 1], [1, 1.0001]])
print(round(float(np.linalg.cond(A)), 3), np.linalg.cond(almost) > 1e4)
```

```text
LinAlgError: Singular matrix
1
2.618 True
```

- `S`'nin ikinci satırı birincinin iki katı: denklemler aynı şeyi söylüyor,
  tek çözüm yok. NumPy **`LinAlgError: Singular matrix`** verir; rank 1.
- Daha sinsi olanı **neredeyse** tekil matris: hata vermez ama sonuç
  girdideki küçük değişikliklere çok duyarlıdır. **`np.linalg.cond`** (koşul
  sayısı) bunu ölçer: 2,6 sağlıklı, 10 000'in üstü tehlikeli. Regresyonda
  birbirine çok benzeyen iki özellik (çoklu doğrusallık) tam olarak budur.

## Uzunluk, özdeğer, en küçük kareler

```python
import numpy as np

print(np.linalg.norm([3, 4]))
print(np.linalg.eigvalsh(np.array([[2.0, 1], [1, 2]])))
X = np.array([[1, 1], [1, 2], [1, 3], [1, 4]], dtype=float)
y = np.array([2.1, 3.9, 6.2, 7.8])
coef, residuals, rank, _ = np.linalg.lstsq(X, y, rcond=None)
print(coef.round(3), rank)
```

```text
5.0
[1. 3.]
[0.15 1.94] 2
```

- **`norm`** vektörün uzunluğu (`√(3² + 4²) = 5`).
- **`eigvalsh`** simetrik bir matrisin özdeğerleri (gerçek sayılar, sıralı).
  Genel matris için `eig`; simetrik matriste `eigh` / `eigvalsh` hem daha
  hızlı hem sonuçlar karmaşık sayı tipine düşmez.
- **`lstsq(X, y)`** denklemlerin tam çözümü yokken (4 nokta, 2 bilinmeyen)
  hatayı en küçük yapan çözümü bulur: en küçük kareler. Birinci sütunu 1
  olan `X` ile bu, doğru uydurmanın ta kendisi: `y ≈ 0,15 + 1,94 x`.
  Doğrusal regresyonun içi budur (ML Kütüphaneleri modülünde scikit-learn ile).

## Özet

- `rng = np.random.default_rng(tohum)`; `integers`, `random`, `normal`,
  `choice(p=, replace=)`, `permutation` (kopya) / `shuffle` (yerinde),
  `spawn`.
- Küresel `np.random.seed` yerine kendi üretecin.
- `@` matris çarpımı, `*` eleman eleman.
- `solve(A, b)` (tersini almaktan iyi), `inv`, `det`, `matrix_rank`.
- Tekil matris `LinAlgError`; neredeyse tekili `cond` söyler.
- `norm`, simetrikte `eigvalsh`, en küçük kareler `lstsq`.
