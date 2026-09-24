**Fikir:** $y$ değerlerinin ardışık farklarına bak. Denklemleri birbirinden çıkarmak $a$'yı yok eder; farkların farkını almak $b$'yi de yok eder ve doğrudan $c$ kalır. Bu, eleme işlemlerini başka bir sırayla yapmak.

**Adım 1 — Ardışık denklemleri çıkar.**

$$
\begin{aligned}
(a + 2b + 4c) - (a + b + c) &= 11 - 6 \\
b + 3c &= 5
\end{aligned}
$$

$$
\begin{aligned}
(a + 3b + 9c) - (a + 2b + 4c) &= 18 - 11 \\
b + 5c &= 7
\end{aligned}
$$

**Adım 2 — Bu ikisini de çıkar.**

$$
\begin{aligned}
(b + 5c) - (b + 3c) &= 7 - 5 \\
2c &= 2 \;\Rightarrow\; c = 1
\end{aligned}
$$

**Adım 3 — Geri git.** $b + 3 = 5 \Rightarrow b = 2$; $a + 2 + 1 = 6 \Rightarrow a = 3$.

**Adım 4 — Tahmin için yine farklar.** $y$'lerin farkları $5, 7$; farkların farkı $2$ ve her adımda sabit (parabolde hep öyle). Sonraki fark $7 + 2 = 9$, sonraki değer $18 + 9 = 27$. Formülle de $3 + 8 + 16 = 27$. ✓

**Neden işe yarar?** $\hat{y} = a + bx + cx^2$'de $x$ birer birer artarken ardışık farklar doğrusal büyür ve farkların farkı her zaman $2c$. Buradaki $2$, $c = 1$ demek.

**Makine öğrenmesiyle bağı:** Burada veri modeldeki parametre sayısı kadar (3 nokta, 3 parametre) ve tam uyuyor. Gerçek veride nokta sayısı çok daha fazla ve gürültülü; o zaman sistem tutarsız olur ve hatayı en küçük yapan parametreler aranır (en küçük kareler).

**Cevap:** $3$, $2$, $1$ ve $27$.
