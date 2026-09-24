Dersteki yöntemlerin her biri için adım adım çözülmüş bir örnek. Önce soruyu kendin çözmeye çalış, sonra çözümü oku.

## 1. Çarpım tanımlı mı, sonuç hangi boyutta?

**Soru:** $A$ $3 \times 2$, $B$ $2 \times 4$, $C$ $4 \times 3$ olsun.
$AB$, $BA$, $BC$ ve $ABC$'nin boyutları nedir?

- $AB$: $(3 \times 2)(2 \times 4)$, içteki sayılar $2 = 2$. Sonuç $3 \times 4$.
- $BA$: $(2 \times 4)(3 \times 2)$, içteki sayılar $4 \ne 3$. **Tanımsız.**
- $BC$: $(2 \times 4)(4 \times 3)$, sonuç $2 \times 3$.
- $ABC$: $AB$ $3 \times 4$, çarpı $C$ ($4 \times 3$): sonuç $3 \times 3$.

## 2. Bir çarpımı eleman eleman hesaplamak

**Soru:** $AB$ nedir?

$$
A = \begin{bmatrix} 1 & -1 & 2 \\ 0 & 3 & 1 \end{bmatrix}
\qquad
B = \begin{bmatrix} 2 & 1 \\ 1 & 0 \\ -1 & 4 \end{bmatrix}
$$

$(2 \times 3)(3 \times 2)$: sonuç $2 \times 2$. Her eleman bir satır ile
bir sütunun nokta çarpımı:

$$
\begin{aligned}
c_{11} &= 1 \cdot 2 + (-1) \cdot 1 + 2 \cdot (-1) = 2 - 1 - 2 = -1 \\
c_{12} &= 1 \cdot 1 + (-1) \cdot 0 + 2 \cdot 4 = 1 + 0 + 8 = 9 \\
c_{21} &= 0 \cdot 2 + 3 \cdot 1 + 1 \cdot (-1) = 0 + 3 - 1 = 2 \\
c_{22} &= 0 \cdot 1 + 3 \cdot 0 + 1 \cdot 4 = 4
\end{aligned}
$$

$$
AB = \begin{bmatrix} -1 & 9 \\ 2 & 4 \end{bmatrix}
$$

## 3. $AB$ ile $BA$'yı karşılaştırmak

**Soru:** $A = \begin{bmatrix} 1 & 1 \\ 0 & 1 \end{bmatrix}$ ve
$B = \begin{bmatrix} 1 & 0 \\ 1 & 1 \end{bmatrix}$ için $AB$ ve $BA$ nedir?

$$
AB = \begin{bmatrix} 1 + 1 & 0 + 1 \\ 0 + 1 & 0 + 1 \end{bmatrix} = \begin{bmatrix} 2 & 1 \\ 1 & 1 \end{bmatrix}
$$

$$
BA = \begin{bmatrix} 1 + 0 & 1 + 0 \\ 1 + 0 & 1 + 1 \end{bmatrix} = \begin{bmatrix} 1 & 1 \\ 1 & 2 \end{bmatrix}
$$

Farklılar. İki kaydırma dönüşümü (biri yatay, biri dikey) art arda
yapılınca sıra sonucu değiştiriyor.

## 4. Çarpımın devriği

**Soru:** 2. örnekteki $A$ ve $B$ için $B^\mathsf{T} A^\mathsf{T}$ nedir?

Kuralla hiç hesap yapmadan: $B^\mathsf{T} A^\mathsf{T} = (AB)^\mathsf{T}$.
$AB$'yi 2. örnekte bulduk; devriğini almak yeterli:

$$
B^\mathsf{T} A^\mathsf{T} = \begin{bmatrix} -1 & 2 \\ 9 & 4 \end{bmatrix}
$$

## 5. İstenen dönüşümün matrisini yazmak

**Soru:** $\mathbf{e}_1$'i $(1, 1)$'e, $\mathbf{e}_2$'yi $(-1, 1)$'e götüren
matris nedir? $(2, 0)$ nereye gider?

Gidilecek yerler matrisin sütunları:

$$
M = \begin{bmatrix} 1 & -1 \\ 1 & 1 \end{bmatrix}
$$

$$
M \begin{bmatrix} 2 \\ 0 \end{bmatrix} = \begin{bmatrix} 2 \\ 2 \end{bmatrix}
$$

Bu matris her şeyi $45°$ döndürüp $\sqrt{2}$ katına büyütüyor:
$(2, 0)$'ın uzunluğu $2$, $(2, 2)$'ninki $2\sqrt{2}$.

## 6. Art arda iki dönüşüm

**Soru:** Önce $x$ yönünde 3 katına ölçekle ($S$), sonra $90°$ döndür
($R$). Tek matris nedir? $(1, 2)$ nereye gider?

"Önce $S$, sonra $R$" $\Rightarrow RS$:

$$
RS = \begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix} \begin{bmatrix} 3 & 0 \\ 0 & 1 \end{bmatrix} = \begin{bmatrix} 0 & -1 \\ 3 & 0 \end{bmatrix}
$$

$$
RS \begin{bmatrix} 1 \\ 2 \end{bmatrix} = \begin{bmatrix} -2 \\ 3 \end{bmatrix}
$$

Adım adım sağlama: $S(1, 2) = (3, 2)$, sonra $R(3, 2) = (-2, 3)$. ✓

## 7. Kuvvet almak

**Soru:** $A = \begin{bmatrix} 1 & 1 \\ 0 & 1 \end{bmatrix}$ için $A^2$ ve
$A^3$ nedir?

$$
A^2 = \begin{bmatrix} 1 & 1 \\ 0 & 1 \end{bmatrix} \begin{bmatrix} 1 & 1 \\ 0 & 1 \end{bmatrix} = \begin{bmatrix} 1 & 2 \\ 0 & 1 \end{bmatrix}
$$

$$
A^3 = A^2 A = \begin{bmatrix} 1 & 2 \\ 0 & 1 \end{bmatrix} \begin{bmatrix} 1 & 1 \\ 0 & 1 \end{bmatrix} = \begin{bmatrix} 1 & 3 \\ 0 & 1 \end{bmatrix}
$$

Kaydırmayı üç kez yapmak, üç kat kaydırmak. Elemanların karesini alsaydık
$A^2$ yine $A$ çıkardı; yanlış olurdu.
