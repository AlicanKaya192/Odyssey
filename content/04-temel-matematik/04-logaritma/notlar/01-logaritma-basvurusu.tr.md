Dersteki her şeyin kısa hâli. Bir formül okurken ya da problem çözerken takıldığında buraya dön.

## Tanım

$$
\log_b x = y \quad\Longleftrightarrow\quad b^y = x
$$

- $b > 0$ ve $b \neq 1$ olmalı.
- $x > 0$ olmalı. **Sıfırın ve negatif sayıların logaritması yok.**
- $y$ her değeri alabilir: negatif, sıfır, ondalıklı.

## Her tabanda aynı olan değerler

| İfade | Değer | Sebep |
|---|---|---|
| $\log_b 1$ | $0$ | $b^0 = 1$ |
| $\log_b b$ | $1$ | $b^1 = b$ |
| $\log_b b^k$ | $k$ | Tanımın kendisi |
| $b^{\log_b x}$ | $x$ | Üs ile logaritma birbirini siler |
| $\log_b \frac{1}{b}$ | $-1$ | $b^{-1} = \frac{1}{b}$ |

## Kurallar

| Kural | Örnek |
|---|---|
| $\log_b (xy) = \log_b x + \log_b y$ | $\log_{10} 200 = \log_{10} 2 + \log_{10} 100 = 0.301 + 2$ |
| $\log_b \frac{x}{y} = \log_b x - \log_b y$ | $\ln \frac{e^5}{e^2} = 5 - 2 = 3$ |
| $\log_b x^k = k \log_b x$ | $\log_2 8^{10} = 10 \cdot 3 = 30$ |
| $\log_b \sqrt[n]{x} = \frac{1}{n} \log_b x$ | $\log_{10} \sqrt{1000} = \frac{3}{2}$ |
| $\log_b x = \dfrac{\ln x}{\ln b}$ | $\log_5 20 = \frac{2.996}{1.609} = 1.861$ |
| $\log_b \frac{1}{x} = -\log_b x$ | $\ln 0.5 = -\ln 2 = -0.693$ |

**Açılmayanlar:** $\log (x + y)$ ve $\log (x - y)$. Toplamın ve farkın
logaritmasının kuralı yok.

## Akılda tutmaya değer sayılar

| | Değer |
|---|---|
| $\log_{10} 2$ | $0.301$ |
| $\log_{10} 3$ | $0.477$ |
| $\ln 2$ | $0.693$ |
| $\ln 10$ | $2.303$ |
| $e$ | $2.718$ |
| $\log_2 1000$ | $\approx 10$ ($2^{10} = 1024$) |
| $\log_2 10^6$ | $\approx 20$ |
| $\log_2 10^9$ | $\approx 30$ |

## Hesap makinesi olmadan logaritma

$\log_{10} 2 \approx 0.301$ ve $\log_{10} 3 \approx 0.477$ bilinince,
kurallarla daha birçok değer bulunabiliyor:

| Aranan | Yazılışı | Sonuç |
|---|---|---|
| $\log_{10} 4$ | $\log_{10} 2^2 = 2 \cdot 0.301$ | $0.602$ |
| $\log_{10} 5$ | $\log_{10} \frac{10}{2} = 1 - 0.301$ | $0.699$ |
| $\log_{10} 6$ | $\log_{10} (2 \cdot 3) = 0.301 + 0.477$ | $0.778$ |
| $\log_{10} 8$ | $\log_{10} 2^3 = 3 \cdot 0.301$ | $0.903$ |
| $\log_{10} 9$ | $\log_{10} 3^2 = 2 \cdot 0.477$ | $0.954$ |
| $\log_{10} 0.004$ | $\log_{10} (4 \cdot 10^{-3}) = 0.602 - 3$ | $-2.398$ |

Son satır önemli bir alışkanlık: sayıyı **"bir sayı çarpı 10'un kuvveti"**
olarak yaz. 10'un kuvveti logaritmanın tam kısmını, kalan çarpan ondalık
kısmını veriyor.

## İşaretten ne anlaşılır?

Taban 1'den büyükken ($b > 1$, pratikte hep böyle):

| $x$ aralığı | $\log_b x$ |
|---|---|
| $0 < x < 1$ | negatif |
| $x = 1$ | $0$ |
| $x > 1$ | pozitif |
| $x \to 0$ | $-\infty$'a gider |

Olasılıklar $0$ ile $1$ arasında; logaritmaları hep negatif. Kayıp
formüllerindeki eksi işareti bunu pozitife çeviriyor.

Taban büyüdükçe, 1'den büyük bir sayının logaritması **küçülür**:
$\log_2 10 \approx 3.32$ ama $\log_3 10 \approx 2.10$. Büyük taban aynı
sayıya daha küçük bir üsle ulaşıyor.

## Denklem türleri ve yöntemleri

| Denklem | Yöntem |
|---|---|
| $b^{f(x)} = b^{g(x)}$ (tabanlar aynı) | Üsleri eşitle: $f(x) = g(x)$. Logaritmaya gerek yok. |
| $a \cdot b^{x} = c$ | Böl: $b^x = \frac{c}{a}$, sonra $x = \frac{\ln (c/a)}{\ln b}$ |
| $b^{f(x)} = d^{g(x)}$ (tabanlar farklı) | İki tarafın $\ln$'ini al, üsleri indir, doğrusal denklemi çöz |
| $\log_b f(x) = k$ | Tanıma çevir: $f(x) = b^k$ |
| $\log_b f(x) + \log_b g(x) = k$ | Birleştir: $f(x)\,g(x) = b^k$ |
| $\log_b f(x) = \log_b g(x)$ | İçleri eşitle: $f(x) = g(x)$ |

**Logaritmalı denklemlerin hepsinde son adım aynı:** bulduğun her değeri
orijinal denklemdeki her logaritmanın içine koy, pozitif olduğunu kontrol et.
