Dersteki yöntemlerin her biri için adım adım çözülmüş bir örnek. Önce soruyu kendin çözmeye çalış, sonra çözümü oku.

## 1. Özvektör mü?

**Soru:** $A = \begin{bmatrix} 3 & 1 \\ 0 & 2 \end{bmatrix}$ için $(1, -1)$ ve $(1, 1)$ özvektör mü?

$$
A \begin{bmatrix} 1 \\ -1 \end{bmatrix} = \begin{bmatrix} 3 - 1 \\ -2 \end{bmatrix} = \begin{bmatrix} 2 \\ -2 \end{bmatrix} = 2 \begin{bmatrix} 1 \\ -1 \end{bmatrix}
$$

Evet, özdeğeri $2$.

$$
A \begin{bmatrix} 1 \\ 1 \end{bmatrix} = \begin{bmatrix} 4 \\ 2 \end{bmatrix}
$$

$(4, 2)$, $(1, 1)$'in katı değil: özvektör değil.

## 2. Özdeğer ve özvektörler

**Soru:** $A = \begin{bmatrix} 1 & 2 \\ 2 & 1 \end{bmatrix}$'nin özdeğerleri ve özvektörleri nedir?

$\operatorname{tr} A = 2$, $\det A = 1 - 4 = -3$:

$$
\lambda^2 - 2\lambda - 3 = (\lambda - 3)(\lambda + 1) = 0
$$

$\lambda = 3$ ve $\lambda = -1$.

- $\lambda = 3$: $A - 3I = \begin{bmatrix} -2 & 2 \\ 2 & -2 \end{bmatrix}$, $y = x$, $\mathbf{v} = (1, 1)$.
- $\lambda = -1$: $A + I = \begin{bmatrix} 2 & 2 \\ 2 & 2 \end{bmatrix}$, $y = -x$, $\mathbf{v} = (1, -1)$.

Negatif özdeğer: $(1, -1)$ doğrultusundaki vektörler ters dönüyor.

## 3. Üçgen matris

**Soru:** $\begin{bmatrix} 5 & 2 & 1 \\ 0 & -1 & 3 \\ 0 & 0 & 2 \end{bmatrix}$'nin özdeğerleri, izi ve determinantı nedir?

Üçgen matris: özdeğerler köşegen, $5, -1, 2$. Sağlama:
$\operatorname{tr} = 5 - 1 + 2 = 6$ ve $\det = 5 \cdot (-1) \cdot 2 = -10$;
özdeğerlerin toplamı ve çarpımıyla aynı.

## 4. Simetrik olmayan bir matriste özvektörler

**Soru:** $A = \begin{bmatrix} 6 & -2 \\ 2 & 1 \end{bmatrix}$'nin özvektörlerini bul.

$\operatorname{tr} = 7$, $\det = 6 + 4 = 10$: toplamı 7, çarpımı 10 olan
iki sayı $2$ ve $5$.

- $\lambda = 2$: $A - 2I = \begin{bmatrix} 4 & -2 \\ 2 & -1 \end{bmatrix}$, $2x - y = 0$, $\mathbf{v} = (1, 2)$.
- $\lambda = 5$: $A - 5I = \begin{bmatrix} 1 & -2 \\ 2 & -4 \end{bmatrix}$, $x = 2y$, $\mathbf{v} = (2, 1)$.

Sağlama: $A(1, 2) = (6 - 4,\ 2 + 2) = (2, 4)$ ✓; $A(2, 1) = (12 - 2,\ 4 + 1) = (10, 5)$ ✓.
Özvektörler dik değil ($1 \cdot 2 + 2 \cdot 1 = 4$): matris simetrik değil.

## 5. Özvektörlerle kuvvet

**Soru:** 2. örnekteki $A$ için $A^3\,(1, 0)$ nedir?

$(1, 0)$'ı özvektörlere ayır: $(1, 0) = \tfrac{1}{2}(1, 1) + \tfrac{1}{2}(1, -1)$.

$$
A^3 \begin{bmatrix} 1 \\ 0 \end{bmatrix} = \tfrac{1}{2} \cdot 3^3 \begin{bmatrix} 1 \\ 1 \end{bmatrix} + \tfrac{1}{2} \cdot (-1)^3 \begin{bmatrix} 1 \\ -1 \end{bmatrix} = \begin{bmatrix} 13.5 - 0.5 \\ 13.5 + 0.5 \end{bmatrix} = \begin{bmatrix} 13 \\ 14 \end{bmatrix}
$$

Doğrudan sağlama: $A^2 = \begin{bmatrix} 5 & 4 \\ 4 & 5 \end{bmatrix}$,
$A^3 = \begin{bmatrix} 13 & 14 \\ 14 & 13 \end{bmatrix}$; 1. sütun $(13, 14)$ ✓.

## 6. Kurallarla özdeğer

**Soru:** $A$'nın özdeğerleri $2$ ve $5$. $A^{-1}$, $A^2$ ve $A + 2I$'nın özdeğerleri nedir?

- $A^{-1}$: $\tfrac{1}{2}$ ve $\tfrac{1}{5}$
- $A^2$: $4$ ve $25$
- $A + 2I$: $4$ ve $7$

Üçünde de özvektörler $A$'nınkilerle aynı.

## 7. Markov zincirinin uzun vadesi

**Soru:** Bir müşteri her ay A ya da B markasını alıyor. A alan bir sonraki
ay %80, B alan %30 olasılıkla A alıyor. Uzun vadede müşterilerin ne kadarı
A alır?

$$
M = \begin{bmatrix} 0.8 & 0.3 \\ 0.2 & 0.7 \end{bmatrix}
$$

$M\mathbf{p} = \mathbf{p}$: $(M - I)\mathbf{p} = \mathbf{0}$, ilk satır
$-0.2x + 0.3y = 0$, yani $x = 1.5y$. Özvektör $(3, 2)$; toplamı 1
yapınca $(0.6, 0.4)$. Uzun vadede müşterilerin %60'ı A alıyor.

Öteki özdeğer $0.8 + 0.7 - 1 = 0.5$: başlangıç farkı her ay yarıya iniyor.
