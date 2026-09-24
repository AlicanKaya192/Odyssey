Dersteki her şeyin kısa hâli. Bir soruda takıldığında buraya dön.

## Tanımlar

| Kavram | Formül | Geometri |
|---|---|---|
| ortalama değişim hızı | $\dfrac{f(b) - f(a)}{b - a}$ | kesenin eğimi |
| türev | $f'(x) = \lim_{h \to 0} \dfrac{f(x + h) - f(x)}{h}$ | teğetin eğimi |
| teğet doğru | $y - f(a) = f'(a)(x - a)$ | noktaya en iyi uyan doğru |

Yazımlar: $f'(x)$, $\dfrac{df}{dx}$, $\dfrac{dy}{dx}$, $y'$.

## Tanımla türev almak

1. $f(x + h)$'yi aç.
2. $f(x)$'i çıkar; $h$'siz terimler gider.
3. $h$'ye böl (sadeleştir).
4. $h \to 0$ koy.

## Temel türevler

| $f(x)$ | $f'(x)$ |
|---|---|
| $c$ | $0$ |
| $x^n$ | $n x^{n-1}$ |
| $\dfrac{1}{x}$ | $-\dfrac{1}{x^2}$ |
| $\sqrt{x}$ | $\dfrac{1}{2\sqrt{x}}$ |
| $e^x$ | $e^x$ |
| $\ln x$ | $\dfrac{1}{x}$ |
| $a f(x) + b g(x)$ | $a f'(x) + b g'(x)$ |

## Türevin işareti

| $f'(a)$ | Anlamı |
|---|---|
| $> 0$ | artıyor |
| $< 0$ | azalıyor |
| $= 0$ | yatay teğet: tepe, dip ya da düz |

## Türevin olmadığı yerler

| Durum | Örnek |
|---|---|
| köşe | $\lvert x \rvert$, ReLU; $x = 0$'da |
| süreksizlik | basamak fonksiyonu |
| dikey teğet | $\sqrt[3]{x}$, $x = 0$'da |

## Sayısal türev

| Yöntem | Formül | Hata |
|---|---|---|
| ileri fark | $\dfrac{f(x + h) - f(x)}{h}$ | $h$ ile orantılı |
| merkezi fark | $\dfrac{f(x + h) - f(x - h)}{2h}$ | $h^2$ ile orantılı |

## Öğrenme adımı

$w \leftarrow w - \eta \, L'(w)$: eğim pozitifse $w$ azalır, negatifse artar.
