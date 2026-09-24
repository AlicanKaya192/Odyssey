Dersteki her şeyin kısa hâli. Bir soruda takıldığında buraya dön.

## Kurallar

| Kural | Formül |
|---|---|
| kuvvet | $(x^n)' = n x^{n-1}$ |
| toplam, sabit kat | $(af + bg)' = af' + bg'$ |
| çarpım | $(fg)' = f'g + fg'$ |
| bölüm | $\left(\dfrac{f}{g}\right)' = \dfrac{f'g - fg'}{g^2}$ |
| zincir | $\big(f(g(x))\big)' = f'(g(x)) \cdot g'(x)$ |

## Temel türevler

| $f(x)$ | $f'(x)$ |
|---|---|
| $e^x$ | $e^x$ |
| $e^{kx}$ | $k e^{kx}$ |
| $a^x$ | $a^x \ln a$ |
| $\ln x$ | $\dfrac{1}{x}$ |
| $\ln g(x)$ | $\dfrac{g'(x)}{g(x)}$ |
| $\sqrt{g(x)}$ | $\dfrac{g'(x)}{2\sqrt{g(x)}}$ |
| $\sigma(x)$ | $\sigma(x)\big(1 - \sigma(x)\big)$ |
| $\max(0, x)$ | $0$ ($x < 0$), $1$ ($x > 0$) |

## Zincir kuralını uygulamak

1. Dış ve iç fonksiyonu ayır: $y = f(u)$, $u = g(x)$.
2. Dıştakinin türevini al, içi olduğu gibi bırak: $f'(u)$.
3. İçtekinin türevini çarp: $f'(u) \cdot g'(x)$.
4. $u$'nun yerine $g(x)$'i geri yaz.

## Hangi kural?

| İfade | Kural |
|---|---|
| $x^3 e^x$ | çarpım |
| $\dfrac{x^2}{x + 1}$ | bölüm (ya da çarpım + zincir) |
| $(x^2 + 1)^7$ | zincir |
| $e^{x^2} \ln x$ | çarpım, içinde zincir |

## Pratik ipuçları

- Kök ve kesirli kuvvetleri üslü yaz.
- Bölüm kuralında paydaki sıra: önce payın türevi.
- Karmaşık bir çarpım ya da bölümde önce $\ln$ almak (logaritmik türev) işi kolaylaştırabilir.
