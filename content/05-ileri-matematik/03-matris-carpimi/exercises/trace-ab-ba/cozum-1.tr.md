**Ne soruluyor?** İki çarpımın izi. İz yalnızca köşegen elemanlarından oluştuğu için çarpımların tamamını hesaplamaya gerek yok.

**Fikir:** $c_{ii}$ = soldaki matrisin $i$. satırı · sağdaki matrisin $i$. sütunu. Her iz için yalnızca bu elemanları hesaplayacağız.

**Adım 1 — Boyutlar.** $AB$: $(2 \times 3)(3 \times 2) = 2 \times 2$, köşegende 2 eleman. $BA$: $(3 \times 2)(2 \times 3) = 3 \times 3$, köşegende 3 eleman.

**Adım 2 — $AB$'nin köşegeni.** $A$'nın satırları $(1, 0, 2)$ ve $(-1, 3, 1)$; $B$'nin sütunları $(3, 2, 1)$ ve $(1, 1, 0)$.

$$
\begin{aligned}
(AB)_{11} &= 1 \cdot 3 + 0 \cdot 2 + 2 \cdot 1 = 5 \\
(AB)_{22} &= -1 \cdot 1 + 3 \cdot 1 + 1 \cdot 0 = 2
\end{aligned}
$$

$$
\operatorname{tr}(AB) = 5 + 2 = 7
$$

**Adım 3 — $BA$'nın köşegeni.** $B$'nin satırları $(3, 1)$, $(2, 1)$, $(1, 0)$; $A$'nın sütunları $(1, -1)$, $(0, 3)$, $(2, 1)$.

$$
\begin{aligned}
(BA)_{11} &= 3 \cdot 1 + 1 \cdot (-1) = 2 \\
(BA)_{22} &= 2 \cdot 0 + 1 \cdot 3 = 3 \\
(BA)_{33} &= 1 \cdot 2 + 0 \cdot 1 = 2
\end{aligned}
$$

$$
\operatorname{tr}(BA) = 2 + 3 + 2 = 7
$$

**Sonucu yorumla:** $AB$ ile $BA$ farklı boyutta, bambaşka matrisler; ama izleri aynı. Bu tesadüf değil: her zaman $\operatorname{tr}(AB) = \operatorname{tr}(BA)$. İkinci yol bunun nedenini gösteriyor.

**Cevap:** $\operatorname{tr}(AB) = 7$, $\operatorname{tr}(BA) = 7$.
