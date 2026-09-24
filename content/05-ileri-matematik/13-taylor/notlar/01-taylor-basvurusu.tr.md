Dersteki her şeyin kısa hâli. Bir soruda takıldığında buraya dön.

## Yaklaşımlar

| Derece | Formül |
|---|---|
| 1 (doğrusal) | $f(a + h) \approx f(a) + f'(a) h$ |
| 2 | $f(a + h) \approx f(a) + f'(a) h + \dfrac{f''(a)}{2} h^2$ |
| $n$ | $P_n(x) = \sum_{k=0}^{n} \dfrac{f^{(k)}(a)}{k!} (x - a)^k$ |

$k! = 1 \cdot 2 \cdots k$, $0! = 1$: $1, 1, 2, 6, 24, 120, \ldots$

## Açılımlar (x = 0 çevresinde)

| Fonksiyon | Açılım |
|---|---|
| $e^x$ | $1 + x + \dfrac{x^2}{2} + \dfrac{x^3}{6} + \dfrac{x^4}{24} + \cdots$ |
| $\ln(1 + x)$ | $x - \dfrac{x^2}{2} + \dfrac{x^3}{3} - \dfrac{x^4}{4} + \cdots$ |
| $\dfrac{1}{1 - x}$ | $1 + x + x^2 + x^3 + \cdots$ |
| $\dfrac{1}{1 + x}$ | $1 - x + x^2 - x^3 + \cdots$ |
| $\sqrt{1 + x}$ | $1 + \dfrac{x}{2} - \dfrac{x^2}{8} + \cdots$ |
| $(1 + x)^n$ | $1 + nx + \dfrac{n(n - 1)}{2} x^2 + \cdots$ |

## Hata

| Kural | Açıklama |
|---|---|
| büyüklük | kabaca atılan ilk terim kadar |
| $h$ ile değişim | $n$'inci derecede $h^{n+1}$ ile orantılı |
| yer | kurulduğu noktanın yakınında geçerli |

## Makine öğrenmesi

| Yöntem | Dayandığı yaklaşım | Adım |
|---|---|---|
| gradyan inişi | doğrusal | $\Delta = -\eta L'(w)$ |
| Newton | ikinci derece | $\Delta = -\dfrac{L'(w)}{L''(w)}$ |

## Pratik ipuçları

- Kök ve kuvvetlerde önce $1 + x$ biçimine getir: $\sqrt{4{,}1} = 2\sqrt{1{,}025}$.
- Katsayıları bulmak için türevleri $a$'da hesapla, $k!$'e böl.
- Newton ikinci dereceden bir fonksiyonun en küçüğünü tek adımda bulur.
