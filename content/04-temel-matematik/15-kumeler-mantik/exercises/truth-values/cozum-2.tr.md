**Fikir:** "İse" alt küme demek: $p \Rightarrow q$ doğruysa "$p$ doğru olan durumlar" "$q$ doğru olan durumlar"ın içinde. Burada tek bir durum var ve $p$ doğru, $q$ yanlış.

**Adım 1 — Durum kümeleri.** Tek durumumuz: $p$'nin kümesinde var, $q$'nunkinde yok.

**Adım 2 — Kesişim ve birleşim.** Durum ikisinde birden değil: $p \wedge q = 0$. En az birinde: $p \vee q = 1$.

**Adım 3 — Alt küme.** $p$'nin kümesi $\{\text{durum}\}$, $q$'nunki boş: $\{\text{durum}\} \subseteq \emptyset$ yanlış, $p \Rightarrow q = 0$. Ters yönde $\emptyset \subseteq \{\text{durum}\}$ doğru (boş küme her kümenin alt kümesi): $q \Rightarrow p = 1$.

**Neden aynı sonuç?** Mantık ve kümeler aynı dil: "ve" kesişim, "veya" birleşim, "ise" alt küme. Yanlış öncülün her şeyi doğurması, boş kümenin her kümenin alt kümesi olmasının mantıktaki karşılığı.

**Cevap:** $0$, $1$, $0$, $1$.
