**Fikir:** Soru yalnızca $z = 1$ olan çözümü istiyor. $z$'yi baştan yerine koyarsak bilinmeyen sayısı ikiye iner; geriye iki bilinmeyenli üç denklem kalır. Sistem gerçekten sonsuz çözümlüyse bu üç denklem **tutarlı** olmalı.

**Adım 1 — $z = 1$'i koy ve sabitleri sağa at.**

$$
\begin{aligned}
x + y + 2 = 5 \;&\Rightarrow\; x + y = 3 \\
2x + 3y + 3 = 13 \;&\Rightarrow\; 2x + 3y = 10 \\
x + 2y + 1 = 8 \;&\Rightarrow\; x + 2y = 7
\end{aligned}
$$

**Adım 2 — İlk ikisini çöz.** Birinciden $x = 3 - y$; ikinciye koy:

$$
\begin{aligned}
2(3 - y) + 3y &= 10 \\
6 + y &= 10 \\
y &= 4
\end{aligned}
$$

ve $x = 3 - 4 = -1$.

**Adım 3 — Üçüncü denklemle sına.** $x + 2y = -1 + 8 = 7$ ✓. Üçüncü denklem de sağlanıyor; sistem tutarlı.

**Neden işe yarıyor?** Serbest değişkene bir değer vermek, sonsuz çözüm kümesinden tek bir noktayı seçmek demek. $z$'ye başka bir değer (örneğin $0$) verseydin başka bir nokta, $(2, 3, 0)$, bulurdun; o da bir çözüm.

**Dikkat:** Bu kısayol yalnızca $z$ gerçekten serbestse işe yarar. Tek çözümlü bir sistemde $z$'ye keyfî bir değer verirsen kalan üç denklem çelişir.

**Cevap:** $x = -1$, $y = 4$.
