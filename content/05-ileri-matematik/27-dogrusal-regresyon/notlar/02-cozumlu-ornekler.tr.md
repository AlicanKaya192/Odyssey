Dersteki yöntemlerin her biri için adım adım çözülmüş bir örnek. Önce soruyu kendin çözmeye çalış, sonra çözümü oku.

## 1. Eğim ve kesişim

**Soru:** $\bar{x} = 4$, $\bar{y} = 10$, $s_{xy} = 6$, $s_x^2 = 3$. Doğru?

$w = \frac{6}{3} = 2$, $b = 10 - 2 \cdot 4 = 2$: $\hat{y} = 2 + 2x$.

## 2. Korelasyondan eğim

**Soru:** $r = 0{,}5$, $s_y = 10$, $s_x = 2$. Eğim?

$w = 0{,}5 \cdot \frac{10}{2} = 2{,}5$.

## 3. Kalıntılar ve SSE

**Soru:** $\hat{y} = 1 + 2x$; veri $(1, 3)$, $(2, 6)$, $(3, 7)$. SSE?

Tahminler $3, 5, 7$; kalıntılar $0, 1, 0$; $\text{SSE} = 1$.

## 4. R²

**Soru:** $\text{SSE} = 20$, $\text{SST} = 80$. $R^2$?

$1 - \frac{20}{80} = 0{,}75$.

## 5. R²'den r

**Soru:** Tek özellikli bir regresyonda $R^2 = 0{,}81$ ve eğim negatif.
$r$?

$r = -\sqrt{0{,}81} = -0{,}9$.

## 6. Normal denklemler

**Soru:** $x = 1, 2, 3$, $y = 2, 4, 5$; kesişimli model. $w$?

$X^\mathsf{T}X = \begin{pmatrix} 3 & 6 \\ 6 & 14 \end{pmatrix}$,
$X^\mathsf{T}y = \begin{pmatrix} 11 \\ 25 \end{pmatrix}$, determinant $6$.

$$
w = \frac{1}{6}\begin{pmatrix} 14 \cdot 11 - 6 \cdot 25 \\ -6 \cdot 11 + 3 \cdot 25 \end{pmatrix} = \frac{1}{6}\begin{pmatrix} 4 \\ 9 \end{pmatrix}
$$

Kesişim $\approx 0{,}667$, eğim $1{,}5$.

## 7. Kesişimsiz model

**Soru:** $x = 1, 2$, $y = 2, 5$; $\hat{y} = wx$. $w$?

$\frac{\sum xy}{\sum x^2} = \frac{2 + 10}{1 + 4} = 2{,}4$.

## 8. Diklik kontrolü

**Soru:** $x = 1, 2, 3$ için kalıntılar $0{,}2$, $-0{,}4$, $0{,}2$ çıktı.
Bir en küçük kareler çözümüyle tutarlı mı?

$\sum e = 0$ ve $\sum x e = 0{,}2 - 0{,}8 + 0{,}6 = 0$: iki sütuna da dik,
tutarlı.

## 9. Ridge

**Soru:** Kesişimsiz, $\sum x^2 = 5$, $\sum xy = 10$. En küçük kareler ve
$\lambda = 5$ ile ridge?

En küçük kareler $\frac{10}{5} = 2$; ridge $\frac{10}{5 + 5} = 1$.

## 10. Gürültü varyansı

**Soru:** $n = 8$ gözlem, $1$ özellik ve kesişim, $\text{SSE} = 12$.
$\sigma^2$'nin MLE'si ve yansız tahmini?

MLE $\frac{12}{8} = 1{,}5$; yansız $\frac{12}{8 - 2} = 2$.
