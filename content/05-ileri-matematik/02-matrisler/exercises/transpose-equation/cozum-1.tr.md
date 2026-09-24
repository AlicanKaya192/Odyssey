**Ne soruluyor?** Soldaki ilk matriste iki bilinmeyen ($x$, $y$), ikincisinde bir bilinmeyen ($z$) var. Eşitliği sağlayan üç sayıyı arıyoruz.

**Fikir:** İki işlem sırayla yapılıyor: önce devrik ($^\mathsf{T}$), sonra toplama. Devrikte satırlar sütun olur. Toplama eleman eleman. Sonunda iki matris eşitse **her elemanları** eşittir; bu da bize basit denklemler verir.

**Adım 1 — Devriği al.** 1. satır $(x,\ 2)$ 1. sütun olur, 2. satır $(y,\ 5)$ 2. sütun olur:

$$
\begin{bmatrix} x & 2 \\ y & 5 \end{bmatrix}^\mathsf{T} = \begin{bmatrix} x & y \\ 2 & 5 \end{bmatrix}
$$

Dikkat: $2$ ile $y$ yer değiştirdi; köşegendeki $x$ ve $5$ yerinde kaldı.

**Adım 2 — İkinci matrisle topla.** Aynı yerdeki elemanları topla:

$$
\begin{aligned}
\begin{bmatrix} x & y \\ 2 & 5 \end{bmatrix} + \begin{bmatrix} 1 & 3 \\ 0 & z \end{bmatrix} &= \begin{bmatrix} x + 1 & y + 3 \\ 2 + 0 & 5 + z \end{bmatrix}
\end{aligned}
$$

**Adım 3 — Sağ tarafla eleman eleman eşitle.** Sağ taraf $\begin{bmatrix} 4 & 7 \\ 2 & 9 \end{bmatrix}$:

$$
\begin{aligned}
x + 1 &= 4 \quad \Rightarrow \quad x = 3 \\
y + 3 &= 7 \quad \Rightarrow \quad y = 4 \\
5 + z &= 9 \quad \Rightarrow \quad z = 4
\end{aligned}
$$

**Sağlama:** Sol alt köşede bilinmeyen yok: $2 + 0 = 2$ ve sağ tarafta da $2$. Soru kendi içinde tutarlı. ✓

**Dikkat:** Devriği almayı unutursan $y$, $2$'nin yerinde kalır ve $y + 0 = 2$ gibi yanlış bir denklem kurarsın.

**Cevap:** $x = 3$, $y = 4$, $z = 4$.
