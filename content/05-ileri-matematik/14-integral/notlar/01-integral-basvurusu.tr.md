Dersteki her şeyin kısa hâli. Bir soruda takıldığında buraya dön.

## Tanımlar

| Kavram | Formül |
|---|---|
| belirli integral | $\int_a^b f(x) \, dx = \lim_{n \to \infty} \sum f(x_i) \Delta x$ |
| ters türev | $\int f(x) \, dx = F(x) + C$, $F' = f$ |
| temel teorem | $\int_a^b f(x) \, dx = F(b) - F(a)$ |
| alanın türevi | $\dfrac{d}{dx} \int_a^x f(t) \, dt = f(x)$ |

## Ters türev tablosu

| $f(x)$ | $\int f(x) \, dx$ |
|---|---|
| $k$ (sabit) | $kx + C$ |
| $x^n$, $n \neq -1$ | $\dfrac{x^{n+1}}{n + 1} + C$ |
| $\dfrac{1}{x}$ | $\ln \lvert x \rvert + C$ |
| $e^{kx}$ | $\dfrac{e^{kx}}{k} + C$ |
| $\dfrac{1}{\sqrt{x}}$ | $2\sqrt{x} + C$ |

## Özellikler

| Özellik | Formül |
|---|---|
| doğrusallık | $\int (af + bg) = a \int f + b \int g$ |
| aralık birleşimi | $\int_a^b f + \int_b^c f = \int_a^c f$ |
| sınır değişimi | $\int_b^a f = -\int_a^b f$ |
| işaret | eksenin altındaki alan eksi sayılır |

## Değişken değiştirme

1. İçteki fonksiyona $u$ de; $du = u' \, dx$.
2. İntegrali tamamen $u$ cinsinden yaz.
3. Belirli integralde sınırları da $u$'ya çevir.
4. Bitir ya da $x$'e geri dön.

## Sayısal integral

| Yöntem | Formül |
|---|---|
| sağ uç dikdörtgen | $h \sum_{i=1}^{n} f(x_i)$ |
| yamuk | $\dfrac{h}{2}\big(f_0 + 2f_1 + \cdots + 2f_{n-1} + f_n\big)$ |

## Olasılık

| Kavram | Formül |
|---|---|
| aralık olasılığı | $P(a \le X \le b) = \int_a^b f(x) \, dx$ |
| toplam | $\int_{-\infty}^{\infty} f = 1$ |
| beklenen değer | $E[X] = \int x f(x) \, dx$ |
| ortalama değer | $\dfrac{1}{b - a} \int_a^b f(x) \, dx$ |
