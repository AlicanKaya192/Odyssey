Dersteki her şeyin kısa hâli. Bir soruda takıldığında buraya dön.

## Doğrusal mı, üstel mi?

| | Doğrusal | Üstel |
|---|---|---|
| biçim | $a + mx$ | $a \cdot b^x$ |
| her adımda | $m$ eklenir | $b$ ile çarpılır |
| sabit olan | ardışık farklar | ardışık oranlar |
| uzun vadede | yavaş | her doğrusalı geçer |

## Üstel fonksiyon

$f(x) = a \cdot b^x$, $a \neq 0$, $b > 0$, $b \neq 1$.

| Özellik | $b^x$ için |
|---|---|
| $f(0)$ | $1$ (genelde $a$) |
| tanım kümesi | bütün gerçek sayılar |
| değer kümesi | $y > 0$ |
| asimptot | $y = 0$ |
| $b > 1$ | artan |
| $0 < b < 1$ | azalan |

$\left( \frac{1}{b} \right)^x = b^{-x}$: $y$ eksenine göre ayna.
$b^x + k$: asimptot $y = k$.

## Formüller

| Durum | Formül |
|---|---|
| yüzde $r$ büyüme | $A_0 (1 + r)^t$ |
| yüzde $r$ azalma | $A_0 (1 - r)^t$ |
| iki katına çıkma süresi $T$ | $N_0 \cdot 2^{t / T}$ |
| yarı ömür $h$ | $N_0 \cdot \left( \frac{1}{2} \right)^{t / h}$ |
| yılda $n$ kez faiz | $A_0 \left( 1 + \frac{r}{n} \right)^{nt}$ |
| sürekli büyüme | $A_0 \, e^{rt}$ |

$e \approx 2{,}71828$. 72 kuralı: yüzde $r$ ile yaklaşık $\frac{72}{r}$
dönemde iki kat.

## Üstel denklem

Aynı tabana getir, üsleri eşitle: $4^x = 8$ ⇒ $2^{2x} = 2^3$ ⇒
$x = \frac{3}{2}$. Ortak taban yoksa logaritma.

## Makine öğrenmesinde

| Nerede | Formül |
|---|---|
| sigmoid | $\sigma(z) = \dfrac{1}{1 + e^{-z}}$, $\sigma(0) = 0{,}5$ |
| softmax | $p_i = \dfrac{e^{z_i}}{\sum_j e^{z_j}}$ |
| öğrenme oranı azaltma | $\eta_0 \cdot c^t$, $0 < c < 1$ |
| gradyan | $0{,}9^{100} \approx 0$, $1{,}1^{100} \approx 13\,781$ |

## Pratik ipuçları

- Azalmada çarpan $1 - r$: yüzde $20$ azalma $0{,}8$.
- Yüzdeler toplanmaz, çarpılır.
- Süre verilmişse üste $\frac{t}{T}$ ya da $\frac{t}{h}$ yazılır.
- $2^x$ ile $x^2$'yi karıştırma: üs mü değişiyor, taban mı?
