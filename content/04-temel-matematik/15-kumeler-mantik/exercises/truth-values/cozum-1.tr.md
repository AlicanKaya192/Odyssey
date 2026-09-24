**Ne soruluyor?** Bağlaçlarla kurulmuş önermelerin doğru mu yanlış mı olduğu.

**Fikir:** Önce yalın önermelerin değerini bul, sonra her bağlacın tablosundaki ilgili satırı oku.

**Adım 1 — Yalın önermeler.** $3 > 2$ doğru: $p = 1$. $2 + 2 = 4 \neq 5$: $q = 0$.

**Adım 2 — "Ve".** $p \wedge q$: ikisi de doğru değil, $0$.

**Adım 3 — "Veya".** $p \vee q$: en az biri ($p$) doğru, $1$.

**Adım 4 — $p \Rightarrow q$.** Öncül doğru, sonuç yanlış: tablonun tek yanlış satırı, $0$.

**Adım 5 — $q \Rightarrow p$.** Öncül yanlış: "ise" önermesi doğru, $1$.

**Sonucu yorumla:** $p \Rightarrow q$ ile $q \Rightarrow p$'nin farklı çıkması, bir önermenin tersinin ayrı bir önerme olduğunu gösteriyor.

**Dikkat:** $q \Rightarrow p$'ye "öncül yanlış, o zaman bütünü yanlış" demek sık hata; yanlış bir öncülden her şey çıkar.

**Cevap:** $0$, $1$, $0$, $1$.
