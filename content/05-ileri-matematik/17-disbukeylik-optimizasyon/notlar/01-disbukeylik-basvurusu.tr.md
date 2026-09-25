Dersteki her şeyin kısa hâli. Bir soruda takıldığında buraya dön.

## Tanımlar

| Kavram | Tanım |
|---|---|
| dışbükey küme | iki noktayı birleştiren parça kümede kalır |
| dışbükey fonksiyon | $f(ta + (1 - t)b) \le t f(a) + (1 - t) f(b)$ |
| içbükey | $-f$ dışbükey |
| kesin dışbükey | kiriş tam üstte; en küçük nokta tek |

## Testler

| Durum | Dışbükeylik koşulu (her yerde) |
|---|---|
| tek değişken | $f''(x) \ge 0$ |
| çok değişken | Hessian pozitif yarı tanımlı: özdeğerler $\ge 0$ |
| $2 \times 2$ Hessian | $f_{xx} \ge 0$, $f_{yy} \ge 0$, $\det H \ge 0$ |
| teğet | $f(y) \ge f(x) + \nabla f(x) \cdot (y - x)$ |

## Dışbükey yapı taşları

| Fonksiyon | Dışbükey mi? |
|---|---|
| $x^2$, $\lvert x \rvert$, $e^x$, $\max(0, x)$ | evet |
| $-\ln x$, $x \ln x$ ($x > 0$) | evet |
| $\ln x$, $\sqrt{x}$ | hayır (içbükey) |
| $ax + b$ | hem dışbükey hem içbükey |
| $x^3$ | hayır |

## Korunan işlemler

- Negatif olmayan katsayılı toplam.
- Doğrusal ifadeyle bileşke: $f(A\mathbf{x} + \mathbf{b})$.
- En büyük alma: $\max(f_1, f_2)$.

## Lagrange

| Adım | Yapılacak |
|---|---|
| 1 | $\nabla f = \lambda \nabla g$ denklemlerini yaz |
| 2 | kısıt $g = c$'yi ekle |
| 3 | sistemi çöz; adayların değerlerini karşılaştır |

$\lambda$: kısıt bir birim gevşerse en iyi değerin yaklaşık değişimi.

## Makine öğrenmesi

| Kayıp | Dışbükey mi? |
|---|---|
| doğrusal regresyon (MSE) | evet |
| lojistik regresyon (log-kaybı) | evet |
| sinir ağı | hayır |
| + L2 cezası | kesin dışbükey yapar |
