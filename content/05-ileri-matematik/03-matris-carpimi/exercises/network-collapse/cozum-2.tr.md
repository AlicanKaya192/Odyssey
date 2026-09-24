**Fikir:** Önce ağı gerçekten çalıştıralım (katman katman), sonra $W$'yi başka bir bakışla bulalım: $1 \times 3$ bir satır ile bir matrisin çarpımı, o matrisin **satırlarının** ağırlıklı toplamı.

**Adım 1 — 1. katman.** $W_1\mathbf{x}$, her nöron için bir nokta çarpımı:

$$
W_1 \begin{bmatrix} 2 \\ 1 \end{bmatrix} = \begin{bmatrix} 1 \cdot 2 + 2 \cdot 1 \\ 0 \cdot 2 + 1 \cdot 1 \\ 1 \cdot 2 - 1 \cdot 1 \end{bmatrix} = \begin{bmatrix} 4 \\ 1 \\ 1 \end{bmatrix}
$$

**Adım 2 — 2. katman.** Ara katmanın çıktısı $W_2$ ile:

$$
y = 1 \cdot 4 + 0 \cdot 1 + 2 \cdot 1 = 6
$$

**Adım 3 — $W$'yi satırlardan kur.** $W_2 = (1, 0, 2)$ olduğu için $W_2 W_1$, $W_1$'in 1. satırının 1 katı, 2. satırının 0 katı ve 3. satırının 2 katının toplamı:

$$
\begin{aligned}
W &= 1 \cdot (1, 2) + 0 \cdot (0, 1) + 2 \cdot (1, -1) \\
&= (1, 2) + (2, -2) \\
&= (3, 0)
\end{aligned}
$$

**Sağlama:** Tek matrisle çıktı $3 \cdot 2 + 0 \cdot 1 = 6$, katman katman bulduğumuzla aynı. ✓

**Ne işe yarar?** Bir milyon girdi olsaydı katman katman yolda her girdi için 6 + 3 = 9 çarpma, tek matrisle 2 çarpma gerekirdi. Ama bedeli de var: bu ağ tek matristen daha fazlasını hiç öğrenemez. Katmanlar arasına ReLU gibi eğri bir fonksiyon konmasının nedeni bu.

**Cevap:** $W = (3, 0)$, $y = 6$.
