Dersteki her şeyin kısa hâli. Bir soruda takıldığında buraya dön.

## Adımlar

1. Merkezle: $x \leftarrow x - \bar{x}$ (birimler farklıysa standartlaştır).
2. Kovaryans matrisi $\Sigma = \frac{1}{n - 1}X^\mathsf{T}X$.
3. Özdeğer ve özvektörler: $\Sigma u = \lambda u$; büyükten küçüğe sırala.
4. İlk $k$ özvektörü $U_k$'ye koy; $z = U_k^\mathsf{T}(x - \bar{x})$.

## Formüller

| Ne | Formül |
|---|---|
| $u$ yönündeki varyans | $u^\mathsf{T}\Sigma u$ |
| toplam varyans | $\operatorname{iz}(\Sigma) = \sum\lambda_j$ |
| açıklanan varyans payı | $\frac{\lambda_j}{\sum_i\lambda_i}$ |
| bileşen skoru | $z = U_k^\mathsf{T}(x - \bar{x})$ |
| geri çatma | $\hat{x} = \bar{x} + U_k z$ |
| geri çatma hatası (tek nokta) | $\lVert x - \bar{x}\rVert^2 - \lVert z\rVert^2$ |
| SVD ile özdeğer | $\lambda_j = \frac{s_j^2}{n - 1}$ |

## 2 × 2 simetrik matris

$\begin{pmatrix} a & b \\ b & c \end{pmatrix}$: $\lambda_1 + \lambda_2 = a + c$,
$\lambda_1\lambda_2 = ac - b^2$. $a = c$ ise özvektörler
$\frac{1}{\sqrt{2}}(1, 1)$ ve $\frac{1}{\sqrt{2}}(1, -1)$, özdeğerler
$a \pm b$.

## Pratik ipuçları

- Özvektörler birim uzunlukta olmalı; skoru hesaplamadan önce normalleştir.
- Bir özdeğer $0$ ise veri daha düşük boyutlu bir alt uzayda yatıyor.
- PCA hedefi görmez; en büyük varyans, tahmin için en yararlı yön
  olmayabilir.
