Dersteki yöntemlerin her biri için adım adım çözülmüş bir örnek. Önce soruyu kendin çözmeye çalış, sonra çözümü oku.

## 1. Toplama kapısı

**Soru:** $f = a + b$, gelen gradyan $3$. $a$'ya ve $b$'ye ne gider?

İkisine de $3$.

## 2. Çarpma kapısı

**Soru:** $f = a \cdot b$, $a = 4$, $b = -2$, gelen gradyan $1$. Türevler?

$\frac{\partial f}{\partial a} = b = -2$, $\frac{\partial f}{\partial b} = a = 4$.

## 3. Max kapısı

**Soru:** $f = \max(a, b)$, $a = 1$, $b = 5$, gelen gradyan $2$. Türevler?

$a$'ya $0$, $b$'ye $2$.

## 4. Dallanma

**Soru:** $f = x \cdot x$, $x = 3$. Grafikte $x$ iki kez kullanılıyor. $\frac{df}{dx}$?

Çarpma her kopyaya öbürünü yollar: $3 + 3 = 6$; $(x^2)' = 2x$ ile aynı.

## 5. ReLU

**Soru:** $z = -1$, gelen gradyan $5$. ReLU'dan sonra $\frac{\partial L}{\partial z}$?

$z < 0$: $0$.

## 6. Sigmoid

**Soru:** $\sigma(z) = 0{,}5$, gelen gradyan $4$. $\frac{\partial L}{\partial z}$?

$4 \cdot 0{,}5 \cdot 0{,}5 = 1$.

## 7. Doğrusal katman

**Soru:** $W = \begin{bmatrix} 1 & 2 \\ 0 & 1 \end{bmatrix}$, $\frac{\partial L}{\partial \mathbf{z}} = (1, 3)$. $\frac{\partial L}{\partial \mathbf{x}}$?

$W^\mathsf{T}(1, 3) = (1 \cdot 1 + 0 \cdot 3, \ 2 \cdot 1 + 1 \cdot 3) = (1, 5)$.

## 8. Derinlik

**Soru:** Her katmanda çarpan $0{,}5$. $8$ katman sonra gradyan kaç katına iner?

$0{,}5^8 = \frac{1}{256}$.
