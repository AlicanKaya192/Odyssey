**Ne soruluyor?** Bir modelin kare hatasını, öğrenilen ağırlık $w$'ye bağlı bir ifade olarak açmak.

**Fikir:** $x$ ve $y$ bilinen sayılar; bilinmeyen yalnızca $w$. Sayıları koyup $(a - b)^2$ özdeşliğiyle açarız.

**Adım 1 — Sayıları koy.**

$$
E(w) = (7 - 2w)^2
$$

**Adım 2 — Özdeşlik.** $a = 7$, $b = 2w$:

$$
\begin{aligned}
(7 - 2w)^2 &= 7^2 - 2 \cdot 7 \cdot 2w + (2w)^2 \\
&= 49 - 28w + 4w^2
\end{aligned}
$$

**Adım 3 — Sırala.** $E(w) = 4w^2 - 28w + 49$.

**Sağlama:** $w = 3$ için doğrudan: $(7 - 6)^2 = 1$. Açılımla: $36 - 84 + 49 = 1$ ✓.

**Sonucu yorumla:** Hata, $w$'nin ikinci dereceden bir ifadesi: grafiği aşağıdan bir çanak (parabol). Hatayı en küçük yapan $w$ bu çanağın dibinde; $w = 3{,}5$ için $7 - 7 = 0$, hata sıfır. Model eğitimi, bu dibi aramak demek.

**Dikkat:** $(2w)^2 = 2w^2$ yazmak sık hata; kare hem $2$'ye hem $w$'ye gider: $4w^2$.

**Cevap:** $a = 4$, $b = -28$, $c = 49$.
