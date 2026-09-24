**Fikir:** Hataların toplamı için hataları tek tek bulmaya gerek yok: $\sum (y - \hat{y}) = \sum y - \sum \hat{y}$. Mutlak değer ve kare için ise her hatayı ayrı ele almak şart.

**Adım 1 — Toplamlar.** Gerçek değerlerin toplamı ve tahminlerin toplamı:

$$
\begin{aligned}
10 + 7 + 12 + 5 &= 34 \\
13 + 6 + 9 + 8 &= 36
\end{aligned}
$$

**Adım 2 — Hataların toplamı.**

$$
34 - 36 = -2
$$

Model toplamda $2$ bin fazla tahmin etmiş.

**Adım 3 — Mutlak değer ve kare.** Bunlar için kısayol yok, çünkü $|a + b|$ genelde $|a| + |b|$'ye eşit değil. Hataların büyüklükleri $3, 1, 3, 3$:

$$
3 + 1 + 3 + 3 = 10, \qquad 9 + 1 + 9 + 9 = 28
$$

**Neden aynı sonuç?** Çıkarma, zıttını eklemek olduğu için dört farkın toplamı, toplamların farkına eşit. Mutlak değer ve kare ise işareti "sildiği" için bu yeniden düzenleme onlarda işe yaramıyor; ilk yoldaki gibi tek tek hesaplamak gerekiyor.

**Cevap:** $-2$, $10$ ve $28$.
