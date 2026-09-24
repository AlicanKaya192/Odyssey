**Fikir:** $(A - \lambda I)$ kurmadan, $\mathbf{v} = (1, y)$'yi doğrudan $B\mathbf{v} = \lambda\mathbf{v}$'ye koy. İki bileşen iki denklem verir; biri $y$'yi bulur, öteki sağlama olur.

**Adım 1 — $B(1, y)$'yi hesapla.**

$$
B \begin{bmatrix} 1 \\ y \end{bmatrix} = \begin{bmatrix} 4 + y \\ 2 + 3y \end{bmatrix}
$$

**Adım 2 — $\lambda = 2$: $\,(4 + y,\ 2 + 3y) = (2,\ 2y)$.**

İlk bileşenden $4 + y = 2$, yani $y = -2$. İkinci bileşenle sına: $2 + 3 \cdot (-2) = -4$ ve $2y = -4$ ✓.

**Adım 3 — $\lambda = 5$: $\,(4 + y,\ 2 + 3y) = (5,\ 5y)$.**

İlk bileşenden $4 + y = 5$, yani $y = 1$. İkinci bileşen: $2 + 3 = 5$ ve $5y = 5$ ✓.

**Neden işe yarar?** Birinci bileşen denklemi, $(B - \lambda I)$'nın ilk satırının yeniden düzenlenmiş hâli ($4 + y = \lambda \iff (4 - \lambda) + y = 0$). İkinci bileşenin de tutması, $\lambda$'nın gerçekten bir özdeğer olduğunun sağlaması.

**Dikkat:** Özdeğer olmayan bir sayı denersen (örneğin $\lambda = 3$), ilk bileşen $y = -1$ verir ama ikinci bileşen tutmaz: $2 - 3 = -1 \ne -3$.

**Cevap:** $-2$ ve $1$.
