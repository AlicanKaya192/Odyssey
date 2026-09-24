**Fikir:** Vektör işlemleri bileşenleri birbirine karıştırmaz. Sonucun $x$ bileşeni yalnızca $\mathbf{u}$ ve $\mathbf{v}$'nin $x$ bileşenlerinden gelir, $y$ bileşeni de yalnızca $y$'lerden. O yüzden aynı ifadeyi iki ayrı sayı problemi gibi çözebiliriz.

**Adım 1 — $x$ bileşeni.** $\mathbf{u}$'nun $x$'i $2$, $\mathbf{v}$'nin $x$'i $-3$. İfadede $\mathbf{u}$ ve $\mathbf{v}$ yerine bu iki sayıyı koy:

$$
\begin{aligned}
x &= 3 \cdot 2 - 2 \cdot (-3) \\
&= 6 - (-6) \\
&= 6 + 6 = 12
\end{aligned}
$$

**Adım 2 — $y$ bileşeni.** $\mathbf{u}$'nun $y$'si $-1$, $\mathbf{v}$'nin $y$'si $4$:

$$
\begin{aligned}
y &= 3 \cdot (-1) - 2 \cdot 4 \\
&= -3 - 8 = -11
\end{aligned}
$$

**Neden aynı sonuç?** Birinci yoldaki her adım zaten bileşen bileşen yapılıyordu. Burada yalnızca sırayı değiştirdik: önce bütün vektörü değil, tek bir bileşeni sonuna kadar götürdük.

**Ne işe yarar?** Boyut büyüdüğünde (örneğin 784 bileşenli bir görüntü vektörü) bu bakış çok daha pratik: her bileşende aynı küçük hesap tekrarlanıyor. Bilgisayar da vektör işlemlerini tam böyle yapar.

**Cevap:** $(12, -11)$.
