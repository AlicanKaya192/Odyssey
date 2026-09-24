**Ne soruluyor?** İki vektörün aynı doğru üzerinde olması için $k$'nin değeri ve aralarındaki kat.

**Fikir:** İki vektörü bir $2 \times 2$ matrisin sütunları yaparsak, bağımlı olmaları determinantın sıfır olması demek (birim kare bir doğru parçasına eziliyor, alan sıfır).

**Adım 1 — Matris ve determinant.**

$$
\det \begin{bmatrix} 2 & 3 \\ k & 6 \end{bmatrix} = 2 \cdot 6 - 3 \cdot k = 12 - 3k
$$

**Adım 2 — Sıfıra eşitle.**

$$
\begin{aligned}
12 - 3k &= 0 \\
k &= 4
\end{aligned}
$$

**Adım 3 — Katı bul.** $\mathbf{u} = (2, 4)$ ve $\mathbf{v} = (3, 6)$. İlk bileşenlerden $3 = c \cdot 2$, yani $c = 1.5$. İkinci bileşenle sınayalım: $1.5 \cdot 4 = 6$ ✓.

**Sonucu yorumla:** $k = 4$ iken iki vektör aynı doğrultuda; birlikte yalnızca bir doğruyu geriyorlar. $k$ başka herhangi bir değer olsaydı bağımsız olup bütün düzlemi gereceklerdi.

**Cevap:** $k = 4$, $c = 1.5$.
