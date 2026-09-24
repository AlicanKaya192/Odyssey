**Ne soruluyor?** Bir vektörü aynı matrisle beş kez çarpmanın sonucu. Beş matris çarpımı yerine özvektörleri kullanacağız.

**Fikir:** Özvektörler üzerinde $A$ yalnızca bir sayıyla çarpmak: $A^5\mathbf{v} = \lambda^5\mathbf{v}$. Vektörü özvektörlere ayırırsak her parçayı kendi özdeğerinin kuvvetiyle çarpar, sonra toplarız.

**Adım 1 — $(3, 1)$'i özvektörlere ayır.** $c_1(1, 1) + c_2(1, -1) = (3, 1)$:

$$
\begin{aligned}
c_1 + c_2 &= 3 \\
c_1 - c_2 &= 1
\end{aligned}
$$

Toplayınca $2c_1 = 4$, $c_1 = 2$; sonra $c_2 = 1$.

$$
\begin{bmatrix} 3 \\ 1 \end{bmatrix} = 2 \begin{bmatrix} 1 \\ 1 \end{bmatrix} + 1 \begin{bmatrix} 1 \\ -1 \end{bmatrix}
$$

**Adım 2 — Her parçaya $A^5$ uygula.** $(1, 1)$ parçası $3^5 = 243$ ile, $(1, -1)$ parçası $1^5 = 1$ ile çarpılır:

$$
A^5 \begin{bmatrix} 3 \\ 1 \end{bmatrix} = 2 \cdot 243 \begin{bmatrix} 1 \\ 1 \end{bmatrix} + 1 \cdot 1 \begin{bmatrix} 1 \\ -1 \end{bmatrix}
$$

**Adım 3 — Topla.**

$$
\begin{bmatrix} 486 + 1 \\ 486 - 1 \end{bmatrix} = \begin{bmatrix} 487 \\ 485 \end{bmatrix}
$$

**Sonucu yorumla:** Sonuç $(1, 1)$ doğrultusuna çok yakın: $\lambda = 3$'lü parça her adımda üç katına çıkarken $\lambda = 1$'li parça yerinde duruyor. Birkaç adım sonra vektör neredeyse tamamen baskın özvektör doğrultusunda.

**Cevap:** $(487, 485)$.
