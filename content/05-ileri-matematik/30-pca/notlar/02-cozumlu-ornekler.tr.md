Dersteki yöntemlerin her biri için adım adım çözülmüş bir örnek. Önce soruyu kendin çözmeye çalış, sonra çözümü oku.

## 1. Merkezlemek

**Soru:** Noktalar $(1, 2)$, $(3, 4)$, $(5, 9)$. Merkezlenmiş hâlleri?

Ortalama $(3, 5)$. Merkezlenmiş: $(-2, -3)$, $(0, -1)$, $(2, 4)$.

## 2. Bir yöndeki varyans

**Soru:** $\Sigma = \begin{pmatrix} 4 & 1 \\ 1 & 2 \end{pmatrix}$. $u = (1, 0)$
ve $u = (0, 1)$ yönlerindeki varyanslar?

$u^\mathsf{T}\Sigma u$: $4$ ve $2$; köşegen elemanları, yani özelliklerin
kendi varyansları.

## 3. Özdeğer ve özvektör

**Soru:** $\Sigma = \begin{pmatrix} 3 & 1 \\ 1 & 3 \end{pmatrix}$. Özdeğerler ve
özvektörler?

$a = c = 3$, $b = 1$: özdeğerler $4$ ve $2$; özvektörler
$\frac{1}{\sqrt{2}}(1, 1)$ ve $\frac{1}{\sqrt{2}}(1, -1)$.

## 4. Açıklanan varyans

**Soru:** Aynı matriste 1. bileşenin payı?

$\frac{4}{4 + 2} \approx 0{,}667$.

## 5. Toplam varyans

**Soru:** Üç özellikte kovaryans matrisinin köşegeni $2$, $1$, $3$. Toplam
varyans?

İz: $6$. Özdeğerlerin toplamı da $6$.

## 6. Bileşen skoru

**Soru:** $u_1 = (0{,}6; \ 0{,}8)$, $x - \bar{x} = (5, 5)$. $z_1$?

$0{,}6 \cdot 5 + 0{,}8 \cdot 5 = 7$.

## 7. Geri çatma

**Soru:** $\bar{x} = (1, 1)$, $z_1 = 7$, $u_1 = (0{,}6; \ 0{,}8)$. $\hat{x}$?

$(1, 1) + 7 \cdot (0{,}6; \ 0{,}8) = (5{,}2; \ 6{,}6)$.

## 8. Geri çatma hatası

**Soru:** Aynı noktada hatanın karesi?

$\lVert(5, 5)\rVert^2 - z_1^2 = 50 - 49 = 1$.

## 9. Kaç bileşen?

**Soru:** Özdeğerler $5, 3, 1, 1$. Yüzde $90$ için kaç bileşen?

Birikimli paylar $0{,}5$; $0{,}8$; $0{,}9$: $3$ bileşen.

## 10. SVD'den özdeğer

**Soru:** $n = 6$ gözlemli merkezlenmiş verinin en büyük tekil değeri $10$.
En büyük özdeğer?

$\frac{10^2}{6 - 1} = 20$.
