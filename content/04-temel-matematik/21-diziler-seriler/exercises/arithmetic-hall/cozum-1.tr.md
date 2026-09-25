**Ne soruluyor?** Aritmetik bir dizinin son terimi, toplamı ve bir sınırı ilk aştığı yer.

**Fikir:** Sıralar $a_1 = 12$, $d = 3$ olan bir aritmetik dizi. Genel terim $a_n = 12 + 3(n - 1)$, toplam $\frac{n(a_1 + a_n)}{2}$.

**Adım 1 — Son sıra.** $a_{20} = 12 + 19 \cdot 3 = 69$.

**Adım 2 — Toplam.**

$$
S_{20} = \frac{20 \cdot (12 + 69)}{2} = 10 \cdot 81 = 810
$$

**Adım 3 — $50$'yi geçen sıra.**

$$
\begin{aligned}
12 + 3(n - 1) &> 50 \\
3(n - 1) &> 38 \\
n - 1 &> 12{,}67
\end{aligned}
$$

En küçük tam sayı $n - 1 = 13$, yani $n = 14$. $a_{13} = 48$, $a_{14} = 51$.

**Sağlama:** $a_{14} = 12 + 13 \cdot 3 = 51 > 50$ ✓ ve $a_{13} = 48 \leq 50$ ✓.

**Dikkat:** Yirminci sıraya $19$ adımda varılır. $12 + 20 \cdot 3 = 72$ yazmak bir sıra fazlasını hesaplamak olur.

**Cevap:** $69$ koltuk, toplam $810$, $14.$ sıra.
