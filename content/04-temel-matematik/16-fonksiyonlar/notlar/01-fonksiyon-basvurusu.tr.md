Dersteki her şeyin kısa hâli. Bir soruda takıldığında buraya dön.

## Temel kavramlar

| Kavram | Anlamı |
|---|---|
| $f(x)$ | $f$ kuralının $x$'e uygulanmışı |
| tanım kümesi | kabul edilen girdiler |
| değer kümesi | çıkabilen çıktılar |
| grafik | $(x, f(x))$ noktaları |
| fonksiyon koşulu | her girdiye tek çıktı (dikey doğru testi) |

## Tanım kümesi bulmak

| İfade | Koşul |
|---|---|
| $\dfrac{p(x)}{q(x)}$ | $q(x) \neq 0$ |
| $\sqrt{g(x)}$ | $g(x) \ge 0$ |
| polinom | koşul yok |

## Bileşke ve ters

| İşlem | Nasıl |
|---|---|
| $(g \circ f)(x) = g(f(x))$ | önce $f$, çıktısını $g$'ye ver |
| $f^{-1}$ | $y = f(x)$ yaz, $x$'i çek, harfleri değiştir |
| kontrol | $f(f^{-1}(x)) = x$ ve $f^{-1}(f(x)) = x$ |

## Temel grafikler

| Fonksiyon | Şekil | Değer kümesi |
|---|---|---|
| $ax + b$ | doğru | bütün sayılar ($a \neq 0$) |
| $x^2$ | parabol | $y \ge 0$ |
| $\lvert x \rvert$ | V | $y \ge 0$ |
| $\sqrt{x}$ | yarım eğri | $y \ge 0$ |
| $\dfrac{1}{x}$ | iki kollu eğri | $y \neq 0$ |

## Pratik ipuçları

- Değer koyarken **her** $x$'i parantezli girdiyle değiştir.
- Bileşkede içten dışa hesapla.
- $f^{-1}(x)$ ile $\dfrac{1}{f(x)}$ farklı şeyler.
- ReLU: $\max(0, x)$; sigmoid: $\dfrac{1}{1 + e^{-x}}$, çıktı $0$ ile $1$ arası.
