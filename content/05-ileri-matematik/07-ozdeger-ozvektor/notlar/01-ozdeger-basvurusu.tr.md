Dersteki her şeyin kısa hâli. Bir soruda takıldığında buraya dön.

## Tanım

$$
A\mathbf{v} = \lambda\mathbf{v}, \qquad \mathbf{v} \ne \mathbf{0}
$$

| $\lambda$ | Özvektöre ne oluyor? |
|---|---|
| $\lambda > 1$ | aynı yönde uzuyor |
| $0 < \lambda < 1$ | aynı yönde kısalıyor |
| $\lambda = 1$ | değişmiyor |
| $\lambda < 0$ | ters dönüyor (aynı doğruda) |
| $\lambda = 0$ | sıfıra gidiyor (çekirdekte) |

## Hesap

1. Özdeğerler: $\det(A - \lambda I) = 0$.
2. $2 \times 2$: $\lambda^2 - (\operatorname{tr} A)\,\lambda + \det A = 0$.
3. Her $\lambda$ için $(A - \lambda I)\mathbf{v} = \mathbf{0}$; satırlardan biri yeter, bir çözüm seç.
4. Sağlama: $A\mathbf{v} = \lambda\mathbf{v}$ mi?

## Kurallar

| Kural | Sonuç |
|---|---|
| $\sum \lambda_i$ | $\operatorname{tr} A$ |
| $\prod \lambda_i$ | $\det A$ |
| Üçgen / köşegen matris | özdeğerler = köşegen |
| $A^k$ | $\lambda^k$, aynı özvektörler |
| $A^{-1}$ | $1 / \lambda$, aynı özvektörler |
| $A + cI$ | $\lambda + c$, aynı özvektörler |
| $cA$ | $c\lambda$ |
| $A^\mathsf{T}$ | aynı özdeğerler |
| $\det A = 0$ | $0$ bir özdeğer |

## Özel matrisler

| Matris | Özdeğerler |
|---|---|
| $I$ | hepsi $1$ |
| $\begin{bmatrix} s_1 & 0 \\ 0 & s_2 \end{bmatrix}$ | $s_1, s_2$ (özvektörler $\mathbf{e}_1, \mathbf{e}_2$) |
| $90°$ döndürme | gerçel özdeğer yok ($\pm i$) |
| $x$ eksenine yansıma | $1$ ($\mathbf{e}_1$) ve $-1$ ($\mathbf{e}_2$) |
| $x$ eksenine izdüşüm | $1$ ve $0$ |
| Markov geçiş matrisi | $1$ her zaman bir özdeğer |

## Köşegenleştirme

$$
A = P D P^{-1}, \qquad A^k = P D^k P^{-1}
$$

$P$'nin sütunları özvektörler, $D$'nin köşegeni özdeğerler (aynı sırada).
$n$ bağımsız özvektör gerekiyor.

Kısa yol: $\mathbf{x} = c_1\mathbf{v}_1 + c_2\mathbf{v}_2$ ise
$A^k\mathbf{x} = c_1\lambda_1^k\mathbf{v}_1 + c_2\lambda_2^k\mathbf{v}_2$.

## Simetrik matris (A^ᵀ = A)

- Özdeğerler gerçel.
- Farklı özdeğerlerin özvektörleri dik.
- $A = Q\Lambda Q^\mathsf{T}$, $Q^{-1} = Q^\mathsf{T}$.

## Uzun vade

- $|\lambda_1|$ en büyükse $A^k\mathbf{x}$ yönü $\mathbf{v}_1$'e yaklaşır (kuvvet yöntemi).
- Markov: kararlı dağılım $M\mathbf{p} = \mathbf{p}$ (özdeğer 1); bileşenler toplamı 1 olacak şekilde ölçekle.

## Pratik ipuçları

- $2 \times 2$'de önce toplamı iz, çarpımı determinant olan iki sayıyı ara.
- Özvektör ararken $(A - \lambda I)$'nın **tek** satırı yeter; ikinci satır aynı bilgiyi verir.
- Yalnızca $\mathbf{0}$ çözümü çıkıyorsa özdeğer yanlış.
- Üçgen matriste hesap yapma; köşegeni oku.
