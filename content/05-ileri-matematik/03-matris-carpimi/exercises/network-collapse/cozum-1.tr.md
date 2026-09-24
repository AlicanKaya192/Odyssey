**Ne soruluyor?** İki doğrusal katmanın tek bir matrise indiğini göstermek: önce o matrisi bulacağız, sonra bir girdinin çıktısını hesaplayacağız.

**Fikir:** Birleşme kuralı: $W_2(W_1\mathbf{x}) = (W_2 W_1)\mathbf{x}$. Arada doğrusal olmayan bir işlem yoksa iki katman, çarpımları olan tek bir katmanla aynı işi yapar.

**Adım 1 — Boyut.** $(1 \times 3)(3 \times 2) = 1 \times 2$: $W$ tek satırlı, iki sayılı bir matris.

**Adım 2 — $W$'nin 1. elemanı.** $W_2$'nin satırı $(1, 0, 2)$ ile $W_1$'in 1. sütunu $(1, 0, 1)$:

$$
w_1 = 1 \cdot 1 + 0 \cdot 0 + 2 \cdot 1 = 3
$$

**Adım 3 — $W$'nin 2. elemanı.** Aynı satır ile 2. sütun $(2, 1, -1)$:

$$
\begin{aligned}
w_2 &= 1 \cdot 2 + 0 \cdot 1 + 2 \cdot (-1) \\
&= 2 + 0 - 2 = 0
\end{aligned}
$$

$$
W = \begin{bmatrix} 3 & 0 \end{bmatrix}
$$

**Adım 4 — Çıktı.** Tek matrisi girdiye uygula:

$$
y = W\mathbf{x} = 3 \cdot 2 + 0 \cdot 1 = 6
$$

**Sonucu yorumla:** $W$'nin 2. elemanı $0$: bu ağ girdinin 2. bileşenine **hiç** bakmıyor. Ara katmanda 2. bileşenin etkisi bir nörondan artı, bir nörondan eksi olarak geçiyor ve sonunda birbirini götürüyor. Üç nöronlu ara katmana rağmen bütün ağ "girdinin ilk bileşeninin 3 katı" kadar basit.

**Cevap:** $W = (3, 0)$, $y = 6$.
