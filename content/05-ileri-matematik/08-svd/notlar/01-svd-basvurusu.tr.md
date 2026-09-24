Dersteki her şeyin kısa hâli. Bir soruda takıldığında buraya dön.

## Ayrışım

$$
A = U\Sigma V^\mathsf{T}, \qquad A\mathbf{v}_i = \sigma_i\mathbf{u}_i
$$

| Parça | Boyut ($A$: $m \times n$) | Özellik |
|---|---|---|
| $U$ | $m \times m$ | Dik: $U^\mathsf{T}U = I$; sütunları sol tekil vektörler |
| $\Sigma$ | $m \times n$ | Köşegeninde $\sigma_1 \ge \sigma_2 \ge \cdots \ge 0$ |
| $V$ | $n \times n$ | Dik: $V^\mathsf{T}V = I$; sütunları sağ tekil vektörler |

Geometri: $V^\mathsf{T}$ döndürür, $\Sigma$ eksenler boyunca esnetir, $U$ döndürür.
Birim çember, yarı eksenleri $\sigma_i$ olan bir elipse gider.

## Elle hesap

1. $A^\mathsf{T}A$'yı hesapla (simetrik, $n \times n$).
2. Özdeğerleri $\lambda_i \ge 0$; tekil değerler $\sigma_i = \sqrt{\lambda_i}$, büyükten küçüğe.
3. Özvektörleri, birim uzunlukta: $\mathbf{v}_i$.
4. $\mathbf{u}_i = A\mathbf{v}_i / \sigma_i$ (yalnızca $\sigma_i \ne 0$ için).

$2 \times 2$ kısayol: $\sigma_1^2 + \sigma_2^2 = \operatorname{tr}(A^\mathsf{T}A)$ = bütün elemanların kareleri toplamı; $\sigma_1\sigma_2 = |\det A|$.

## Tekil değerlerin söyledikleri

| Nicelik | Değer |
|---|---|
| Rank | sıfır olmayan $\sigma_i$ sayısı |
| Norm $\|A\|$ | $\sigma_1$ |
| $\lvert\det A\rvert$ (kare) | $\prod \sigma_i$ |
| Elemanların kareleri toplamı | $\sum \sigma_i^2$ |
| Koşul sayısı | $\sigma_1 / \sigma_n$ |
| Simetrik, özdeğerleri $\ge 0$ | $\sigma_i = \lambda_i$, $U = V$ |

## Katmanlar ve düşük ranklı yaklaşım

$$
A = \sum_{i=1}^{r} \sigma_i \mathbf{u}_i \mathbf{v}_i^\mathsf{T}
\qquad
A_k = \sum_{i=1}^{k} \sigma_i \mathbf{u}_i \mathbf{v}_i^\mathsf{T}
$$

- $A_k$, rankı $k$ olan en yakın matris (Eckart–Young).
- Hata: $\|A - A_k\| = \sqrt{\sigma_{k+1}^2 + \cdots + \sigma_r^2}$.
- Korunan enerji: $\dfrac{\sigma_1^2 + \cdots + \sigma_k^2}{\sigma_1^2 + \cdots + \sigma_r^2}$.
- Saklama: $k\,(m + n + 1)$ sayı (orijinal $m \cdot n$).

## Rank-1 matris

$A = \mathbf{a}\mathbf{b}^\mathsf{T}$ ise tek tekil değer $\sigma_1 = \|\mathbf{a}\|\,\|\mathbf{b}\|$,
$\mathbf{u}_1 = \mathbf{a} / \|\mathbf{a}\|$, $\mathbf{v}_1 = \mathbf{b} / \|\mathbf{b}\|$.

## Pratik ipuçları

- Tekil değerler hiçbir zaman negatif değil; köşegen matriste mutlak değerleri al.
- $A^\mathsf{T}A$ yerine $AA^\mathsf{T}$'yi de kullanabilirsin (hangisi küçükse): sıfır olmayan özdeğerleri aynı, özvektörleri $\mathbf{u}_i$.
- $\mathbf{u}_i$'ler birbirine dik çıkmalı; çıkmıyorsa bir hata var.
- Enerji hesabında **kareleri** topla, tekil değerleri değil.
