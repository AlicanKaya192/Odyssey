**Fikir:** "En az bir kadın", "tam $1$, tam $2$, tam $3$ ya da tam $4$ kadın" demek. Bu durumlar ayrık; toplama ilkesiyle toplanır.

**Adım 1 — Bütün ekipler.** $\binom{12}{4} = 495$.

**Adım 2 — Durumlar.**

| Kadın | Erkek | Sayı |
|---|---|---|
| $1$ | $3$ | $\binom{5}{1}\binom{7}{3} = 5 \cdot 35 = 175$ |
| $2$ | $2$ | $\binom{5}{2}\binom{7}{2} = 10 \cdot 21 = 210$ |
| $3$ | $1$ | $\binom{5}{3}\binom{7}{1} = 10 \cdot 7 = 70$ |
| $4$ | $0$ | $\binom{5}{4} = 5$ |

**Adım 3 — Topla.** $175 + 210 + 70 + 5 = 460$.

**Neden aynı sonuç?** Bütün ekipler $0$'dan $4$'e kadın sayısına göre ayrık parçalara bölünüyor; "$0$ kadın" parçası dışındakilerin toplamı, bütünden o parçayı çıkarmakla aynı. Tümleyen yolu tek bir hesapla bitiriyor.

**Cevap:** $495$, $210$ ve $460$.
