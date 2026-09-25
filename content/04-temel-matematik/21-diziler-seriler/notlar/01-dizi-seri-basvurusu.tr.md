Dersteki her şeyin kısa hâli. Bir soruda takıldığında buraya dön.

## İki dizi

| | Aritmetik | Geometrik |
|---|---|---|
| adım | $d$ eklenir | $r$ ile çarpılır |
| genel terim | $a_1 + (n - 1)d$ | $a_1 r^{n-1}$ |
| $d$ ya da $r$ | sonraki eksi önceki | sonraki bölü önceki |
| ilk $n$ terimin toplamı | $\dfrac{n(a_1 + a_n)}{2}$ | $a_1 \dfrac{1 - r^n}{1 - r}$ |
| akrabası | doğru | üstel fonksiyon |

İki terimden: $a_m$ ile $a_k$ arasında $m - k$ adım var.
Aritmetikte $d = \dfrac{a_m - a_k}{m - k}$, geometrikte
$r^{m - k} = \dfrac{a_m}{a_k}$.

## Σ gösterimi

$\displaystyle \sum_{i=a}^{b} t_i$: sayaç $a$'dan $b$'ye, terim sayısı
$b - a + 1$.

| Kural | Yazılışı |
|---|---|
| toplam | $\sum (a_i + b_i) = \sum a_i + \sum b_i$ |
| sabit çarpan | $\sum c \, a_i = c \sum a_i$ |
| sabit terim | $\sum_{i=1}^{n} c = nc$ |
| çarpım (böyle bir kural yok) | $\sum a_i b_i \neq \sum a_i \cdot \sum b_i$ |

## Hazır toplamlar

| Toplam | Sonuç |
|---|---|
| $\sum_{i=1}^{n} i$ | $\dfrac{n(n + 1)}{2}$ |
| $\sum_{i=1}^{n} i^2$ | $\dfrac{n(n + 1)(2n + 1)}{6}$ |
| $\sum_{k=0}^{n-1} r^k$ | $\dfrac{1 - r^n}{1 - r}$ |
| $\sum_{k=0}^{\infty} r^k$, $-1 < r < 1$ | $\dfrac{1}{1 - r}$ |

## Makine öğrenmesinde

| Ne | Formül |
|---|---|
| ortalama | $\frac{1}{n} \sum x_i$ |
| MSE | $\frac{1}{n} \sum (y_i - \hat{y}_i)^2$ |
| ağırlıklı toplam | $\sum w_i x_i + b$ |
| indirgenmiş ödül | $\sum \gamma^t r_t$ |

## Pratik ipuçları

- $n.$ terime $n - 1$ adımda varılır.
- Terim sayısını bul: $\frac{\text{son} - \text{ilk}}{d} + 1$.
- Σ'yi anlamadıysan ilk üç terimi açıp yaz.
- Sonsuz toplam formülünden önce $r$'nin $-1$ ile $1$ arasında olduğuna bak.
