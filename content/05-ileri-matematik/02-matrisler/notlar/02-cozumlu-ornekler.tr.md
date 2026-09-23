Dersteki yöntemlerin her biri için adım adım çözülmüş bir örnek. Önce soruyu kendin çözmeye çalış, sonra çözümü oku.

## 1. Boyut ve eleman okumak

**Soru:** Aşağıdaki matrisin boyutu nedir? $b_{12}$ ve $b_{23}$ kaçtır?

$$
B = \begin{bmatrix} 4 & -1 & 0 \\ 2 & 6 & 3 \end{bmatrix}
$$

2 satır, 3 sütun: boyut $2 \times 3$.

- $b_{12}$: 1. satır, 2. sütun $\Rightarrow -1$
- $b_{23}$: 2. satır, 3. sütun $\Rightarrow 3$

$b_{32}$ diye bir eleman **yok**: 3. satır yok.

## 2. Eşitlikten bilinmeyen bulmak

**Soru:** $x$ ve $y$ kaçtır?

$$
\begin{bmatrix} x + 1 & 4 \\ 3 & 2y \end{bmatrix} = \begin{bmatrix} 5 & 4 \\ 3 & -6 \end{bmatrix}
$$

Karşılıklı elemanlar eşit olmalı:

$$
x + 1 = 5 \;\Rightarrow\; x = 4
$$

$$
2y = -6 \;\Rightarrow\; y = -3
$$

## 3. Doğrusal kombinasyon

**Soru:** $A = \begin{bmatrix} 1 & 0 \\ 2 & -1 \end{bmatrix}$ ve $B = \begin{bmatrix} 0 & 1 \\ 1 & 1 \end{bmatrix}$ için $2A - 3B$ nedir?

Önce ölçekle:

$$
2A = \begin{bmatrix} 2 & 0 \\ 4 & -2 \end{bmatrix}
\qquad
3B = \begin{bmatrix} 0 & 3 \\ 3 & 3 \end{bmatrix}
$$

Sonra eleman eleman çıkar:

$$
2A - 3B = \begin{bmatrix} 2 & -3 \\ 1 & -5 \end{bmatrix}
$$

## 4. Devrik

**Soru:** $C = \begin{bmatrix} 1 & 2 \\ 3 & 4 \\ 5 & 6 \end{bmatrix}$ ise $C^\mathsf{T}$ nedir?

$C$ $3 \times 2$, öyleyse $C^\mathsf{T}$ $2 \times 3$. $C$'nin sütunları
$C^\mathsf{T}$'nin satırları oluyor:

$$
C^\mathsf{T} = \begin{bmatrix} 1 & 3 & 5 \\ 2 & 4 & 6 \end{bmatrix}
$$

Sağlama: $(C^\mathsf{T})_{13} = 5$ ve $c_{31} = 5$. ✓

## 5. Simetrik yapan değerler

**Soru:** Matris simetrik olsun. $x$ ve $y$ kaçtır?

$$
S = \begin{bmatrix} 1 & x & 4 \\ 3 & 2 & y \\ 4 & 5 & 0 \end{bmatrix}
$$

Simetrikte $s_{ij} = s_{ji}$:

- $s_{12} = s_{21}$: $x = 3$
- $s_{23} = s_{32}$: $y = 5$
- $s_{13} = s_{31}$: $4 = 4$ ✓ (zaten sağlanıyor)

## 6. Matris ile vektör çarpımı, iki bakışla

**Soru:** $\begin{bmatrix} 3 & 0 & -1 \\ 1 & 2 & 2 \end{bmatrix} \begin{bmatrix} 2 \\ 1 \\ 4 \end{bmatrix}$ nedir?

Boyut: $(2 \times 3)$ çarpı 3 bileşen, sonuç 2 bileşenli.

**Satır bakışı:**

$$
\begin{bmatrix} 3 \cdot 2 + 0 \cdot 1 + (-1) \cdot 4 \\ 1 \cdot 2 + 2 \cdot 1 + 2 \cdot 4 \end{bmatrix}
= \begin{bmatrix} 2 \\ 12 \end{bmatrix}
$$

**Sütun bakışı:**

$$
2 \begin{bmatrix} 3 \\ 1 \end{bmatrix} + 1 \begin{bmatrix} 0 \\ 2 \end{bmatrix} + 4 \begin{bmatrix} -1 \\ 2 \end{bmatrix}
= \begin{bmatrix} 6 + 0 - 4 \\ 2 + 2 + 8 \end{bmatrix}
= \begin{bmatrix} 2 \\ 12 \end{bmatrix}
$$

## 7. Bütün tahminler tek çarpımda

**Soru:** İki öğrencinin (çalışma saati, uyku saati) bilgisi ve bir modelin
ağırlıkları:

$$
X = \begin{bmatrix} 5 & 7 \\ 2 & 8 \end{bmatrix}
\qquad
\mathbf{w} = \begin{bmatrix} 10 \\ 2 \end{bmatrix}
$$

Modelin iki öğrenci için puan tahmini nedir?

$$
X\mathbf{w} = \begin{bmatrix} 5 \cdot 10 + 7 \cdot 2 \\ 2 \cdot 10 + 8 \cdot 2 \end{bmatrix} = \begin{bmatrix} 64 \\ 36 \end{bmatrix}
$$

Her satır bir öğrenci, her tahmin o satırla $\mathbf{w}$'nin nokta çarpımı.

## 8. Çarpım tanımlı mı?

**Soru:** $A$ $3 \times 2$ bir matris, $\mathbf{x}$ 3 bileşenli bir vektör.
$A\mathbf{x}$ ve $A^\mathsf{T}\mathbf{x}$ tanımlı mı?

- $A\mathbf{x}$: $A$'nın 2 sütunu var, $\mathbf{x}$'in 3 bileşeni. **Tanımsız.**
- $A^\mathsf{T}$ $2 \times 3$: 3 sütunu var, $\mathbf{x}$'in 3 bileşeni. **Tanımlı**, sonuç 2 bileşenli.

Makine öğrenmesinde $X^\mathsf{T}$ tam bu yüzden sık görünüyor: veri
matrisini "özellik başına" okumak gerektiğinde devriği alınıyor.
