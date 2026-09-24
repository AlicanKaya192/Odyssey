**Ne soruluyor?** $\mathbf{v}_3$'ün ilk iki vektörden kurulup kurulamayacağı; kurulabiliyorsa üç vektör aslında yalnızca iki bağımsız yön taşıyor.

**Fikir:** $a\,\mathbf{v}_1 + b\,\mathbf{v}_2$'yi bileşenlerine aç ve $\mathbf{v}_3$'e eşitle. İki bilinmeyenli üç denklem: iki denklem $a$ ile $b$'yi verir, üçüncüsü sağlama.

**Adım 1 — Kombinasyonu aç.**

$$
\begin{aligned}
a(1, 0, 2) + b(0, 1, 1) &= (a,\ b,\ 2a + b)
\end{aligned}
$$

**Adım 2 — Eşitle.**

$$
\begin{aligned}
a &= 2 \\
b &= 3 \\
2a + b &= 7
\end{aligned}
$$

**Adım 3 — Üçüncü denklemle sına.** $2 \cdot 2 + 3 = 7$ ✓. Üç denklemin üçü de tutuyor: $\mathbf{v}_3 = 2\mathbf{v}_1 + 3\mathbf{v}_2$.

**Adım 4 — Rank.** $\mathbf{v}_1$ ve $\mathbf{v}_2$ bağımsız (biri ötekinin katı değil), $\mathbf{v}_3$ ise onların kombinasyonu. Bağımsız sütun sayısı $2$: $\operatorname{rank} = 2$.

**Dikkat:** Üçüncü denklem tutmasaydı (örneğin $\mathbf{v}_3 = (2, 3, 8)$ olsaydı) $\mathbf{v}_3$ ilk ikisinin germesinde olmazdı ve rank $3$ olurdu.

**Cevap:** $a = 2$, $b = 3$, rank $2$.
