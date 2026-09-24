**Ne soruluyor?** Bir noktanın iki dönüşümden sonra vardığı yer. Sıra önemli: önce döndürme, sonra esnetme.

**Fikir:** Her dönüşümün matrisini yaz, noktayı önce birinciyle, çıkan sonucu ikinciyle çarp. Matrisleri sütun kuralıyla kurarız: 1. sütun $\mathbf{e}_1$'in, 2. sütun $\mathbf{e}_2$'nin gittiği yer.

**Adım 1 — Döndürme matrisi.** $90°$ dönünce $\mathbf{e}_1 = (1, 0)$ yukarı, $(0, 1)$'e; $\mathbf{e}_2 = (0, 1)$ sola, $(-1, 0)$'a gidiyor:

$$
R = \begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix}
$$

**Adım 2 — Noktayı döndür.**

$$
\begin{aligned}
R \begin{bmatrix} 3 \\ 1 \end{bmatrix} &= \begin{bmatrix} 0 \cdot 3 + (-1) \cdot 1 \\ 1 \cdot 3 + 0 \cdot 1 \end{bmatrix} \\
&= \begin{bmatrix} -1 \\ 3 \end{bmatrix}
\end{aligned}
$$

**Adım 3 — Esnetme matrisi.** $\mathbf{e}_1$ iki katına, $(2, 0)$'a; $\mathbf{e}_2$ yerinde:

$$
S = \begin{bmatrix} 2 & 0 \\ 0 & 1 \end{bmatrix}
$$

**Adım 4 — Döndürülmüş noktayı esnet.** $x$ iki katına çıkıyor, $y$ aynı:

$$
S \begin{bmatrix} -1 \\ 3 \end{bmatrix} = \begin{bmatrix} 2 \cdot (-1) \\ 3 \end{bmatrix} = \begin{bmatrix} -2 \\ 3 \end{bmatrix}
$$

**Dikkat:** Sırayı ters çevirip önce esnetseydin $(6, 1)$, sonra döndürünce $(-1, 6)$ bulurdun. Başka bir nokta.

**Cevap:** $(-2, 3)$.
