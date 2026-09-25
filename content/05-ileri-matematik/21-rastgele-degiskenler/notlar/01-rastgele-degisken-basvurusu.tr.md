Dersteki her şeyin kısa hâli. Bir soruda takıldığında buraya dön.

## Kesikli ve sürekli

| | Kesikli | Sürekli |
|---|---|---|
| dağılım | $p(x) = P(X = x)$ | yoğunluk $f(x)$ |
| toplam | $\sum p(x) = 1$ | $\int f(x) \, dx = 1$ |
| olasılık | $P(X = a) = p(a)$ | $P(a \leq X \leq b) = \int_a^b f$; $P(X = a) = 0$ |
| $E[X]$ | $\sum x \, p(x)$ | $\int x \, f(x) \, dx$ |
| $E[g(X)]$ | $\sum g(x) \, p(x)$ | $\int g(x) \, f(x) \, dx$ |

Birikimli dağılım $F(x) = P(X \leq x)$.

## Kurallar

| Kural | Formül |
|---|---|
| doğrusallık | $E[aX + b] = aE[X] + b$ |
| toplam | $E[X + Y] = E[X] + E[Y]$ (her zaman) |
| varyans | $\operatorname{Var}(X) = E[(X - \mu)^2] = E[X^2] - \mu^2$ |
| kaydırma ve ölçek | $\operatorname{Var}(aX + b) = a^2 \operatorname{Var}(X)$ |
| bağımsız toplam | $\operatorname{Var}(X \pm Y) = \operatorname{Var}(X) + \operatorname{Var}(Y)$ |
| ortalama | $E[\bar{X}] = \mu$, $\operatorname{Var}(\bar{X}) = \frac{\sigma^2}{n}$ |

## Hazır değerler

| Değişken | $E[X]$ | $\operatorname{Var}(X)$ |
|---|---|---|
| zar | $3{,}5$ | $\frac{35}{12}$ |
| tekdüze $[0, 1]$ | $\frac{1}{2}$ | $\frac{1}{12}$ |
| tekdüze $[a, b]$ | $\frac{a + b}{2}$ | $\frac{(b - a)^2}{12}$ |

## Makine öğrenmesinde

- Eğitim kaybı, beklenen kaybın örneklem ortalamasıyla tahmini.
- Mini-yığın gradyanı yansız; varyansı yığın büyüdükçe azalır.
- Dropout: açık nöronu $\frac{1}{p}$ ile büyüt, beklenen çıkış korunur.

## Pratik ipuçları

- Önce dağılımın toplamının $1$ olduğunu sına.
- Varyans için $E[X^2]$'yi ayrı hesapla, sonra $\mu^2$'yi çıkar.
- Çarpanın varyansa karesiyle girdiğini unutma.
- Yoğunluk değeri olasılık değil; olasılık alan.
