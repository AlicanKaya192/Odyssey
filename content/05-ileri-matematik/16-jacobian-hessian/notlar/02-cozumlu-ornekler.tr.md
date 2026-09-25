Dersteki yöntemlerin her biri için adım adım çözülmüş bir örnek. Önce soruyu kendin çözmeye çalış, sonra çözümü oku.

## 1. Jacobian

**Soru:** $F(x, y) = (xy, \ x - y^2)$'nin Jacobian'ı nedir?

$\begin{bmatrix} y & x \\ 1 & -2y \end{bmatrix}$.

## 2. Doğrusal yaklaşım

**Soru:** Aynı $F$ için $F(2{,}1; \ 1)$'i $(2, 1)$ çevresinde yaklaşık bul.

$F(2, 1) = (2, 1)$, $J = \begin{bmatrix} 1 & 2 \\ 1 & -2 \end{bmatrix}$, $\mathbf{h} = (0{,}1; 0)$: $(2{,}1; \ 1{,}1)$. (Gerçeği de aynı.)

## 3. Zincir kuralı

**Soru:** $z = x + y^2$, $x = t^3$, $y = 2t$ ise $t = 1$'de $\frac{dz}{dt}$?

$1 \cdot 3t^2 + 2y \cdot 2 = 3 + 8 = 11$.

## 4. Doğrusal katmanın Jacobian'ı

**Soru:** $\mathbf{z} = W\mathbf{x} + \mathbf{b}$, $W$ $4 \times 3$. Jacobian'ın boyutu?

$4 \times 3$; Jacobian $W$'nun kendisi.

## 5. Hessian

**Soru:** $f = x^2 y + y^3$'ün Hessian'ı nedir?

$f_{xx} = 2y$, $f_{xy} = 2x$, $f_{yy} = 6y$: $\begin{bmatrix} 2y & 2x \\ 2x & 6y \end{bmatrix}$.

## 6. Sınıflandırma

**Soru:** $f = x^2 + 4xy + y^2$'nin $(0, 0)$'daki kritik noktası nedir?

$H = \begin{bmatrix} 2 & 4 \\ 4 & 2 \end{bmatrix}$, $\det H = 4 - 16 = -12 < 0$: eyer.

## 7. Özdeğerlerle

**Soru:** Bir kritik noktada Hessian'ın özdeğerleri $3$ ve $0{,}5$. Nokta nedir?

İkisi de pozitif: yerel en küçük.

## 8. Öğrenme oranı sınırı

**Soru:** Kaybın Hessian'ının en büyük özdeğeri $20$. Kararlı öğrenme oranı için üst sınır yaklaşık kaç?

$\frac{2}{20} = 0{,}1$.
