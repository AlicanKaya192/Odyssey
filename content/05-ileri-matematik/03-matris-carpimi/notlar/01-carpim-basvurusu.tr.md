Dersteki her şeyin kısa hâli. Bir soruda takıldığında buraya dön.

## Boyut kuralı

$$
(m \times n)(n \times p) = m \times p
$$

İçteki iki sayı eşit olmalı; dıştaki iki sayı sonucun boyutu.

| Çarpım | Sonuç | Adı |
|---|---|---|
| $(1 \times n)(n \times 1)$ | $1 \times 1$ | nokta çarpımı $\mathbf{a}^\mathsf{T}\mathbf{b}$ |
| $(m \times n)(n \times 1)$ | $m \times 1$ | matris–vektör çarpımı |
| $(n \times 1)(1 \times p)$ | $n \times p$ | dış çarpım $\mathbf{a}\mathbf{b}^\mathsf{T}$ |

## Eleman kuralı

$$
c_{ij} = \sum_{k=1}^{n} a_{ik}\, b_{kj} = (A \text{'nın } i. \text{ satırı}) \cdot (B \text{'nin } j. \text{ sütunu})
$$

Sütun bakışı: $AB$'nin $j$. sütunu $= A\mathbf{b}_j$.

## Kurallar

| Geçerli | Geçersiz |
|---|---|
| $(AB)C = A(BC)$ | $AB = BA$ (genelde) |
| $A(B + C) = AB + AC$ | $(AB)^\mathsf{T} = A^\mathsf{T}B^\mathsf{T}$ |
| $(A + B)C = AC + BC$ | $(A + B)^2 = A^2 + 2AB + B^2$ |
| $AI = IA = A$ | $A^2$ = elemanların karesi |
| $(AB)^\mathsf{T} = B^\mathsf{T}A^\mathsf{T}$ | |

$(A + B)^2 = A^2 + AB + BA + B^2$; $AB \ne BA$ olduğu için ortadaki iki
terim birleşmiyor.

## Dönüşüm olarak matris

- $A\mathbf{e}_1$ = 1. sütun, $A\mathbf{e}_2$ = 2. sütun.
- Dönüşümün matrisini yazmak: $\mathbf{e}_1$ ve $\mathbf{e}_2$'nin gideceği yerleri sütun yap.
- $A(B\mathbf{x}) = (AB)\mathbf{x}$: önce $B$, sonra $A$ (sağdan sola).

| Dönüşüm | Matris | $(x, y) \to$ |
|---|---|---|
| Ölçekleme | $\begin{bmatrix} s_1 & 0 \\ 0 & s_2 \end{bmatrix}$ | $(s_1 x,\ s_2 y)$ |
| $90°$ döndürme | $\begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix}$ | $(-y,\ x)$ |
| $180°$ döndürme | $\begin{bmatrix} -1 & 0 \\ 0 & -1 \end{bmatrix}$ | $(-x,\ -y)$ |
| $\theta$ döndürme | $\begin{bmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{bmatrix}$ | |
| $x$ eksenine yansıma | $\begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix}$ | $(x,\ -y)$ |
| $y$ eksenine yansıma | $\begin{bmatrix} -1 & 0 \\ 0 & 1 \end{bmatrix}$ | $(-x,\ y)$ |
| $y = x$ doğrusuna yansıma | $\begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}$ | $(y,\ x)$ |
| Yatay kaydırma | $\begin{bmatrix} 1 & k \\ 0 & 1 \end{bmatrix}$ | $(x + ky,\ y)$ |
| $x$ eksenine izdüşüm | $\begin{bmatrix} 1 & 0 \\ 0 & 0 \end{bmatrix}$ | $(x,\ 0)$ |

Döndürme ve yansıma uzunlukları ve açıları korur; ölçekleme ve kaydırma
korumaz. Öteleme ($\mathbf{x} + \mathbf{t}$) doğrusal değil, matrisle
yazılamaz.

## Pratik ipuçları

- Çarpmadan önce boyutları yaz: $(2 \times 3)(3 \times 2) = 2 \times 2$.
  Boş sonuç tablosunu çiz, sonra doldur.
- Her elemanı hesapladıktan sonra hangi satır ve hangi sütunu
  kullandığını bir kez daha kontrol et.
- Bir dönüşümün sırası sorulduğunda cümleyi sağdan sola çevir: "önce
  $B$, sonra $A$" $\Rightarrow AB$.
- Sonucu kontrol etmek için birim vektörleri dene: $AB\mathbf{e}_1$,
  $AB$'nin 1. sütunu olmalı.
