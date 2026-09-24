**Ne soruluyor?** İki kümenin birleşiminin, kesişiminin ve farkının eleman sayıları.

**Fikir:** Küçük kümelerde en güvenli yol işlemleri doğrudan yazmak: birleşim "ikisinden birinde", kesişim "ikisinde birden", fark "$A$'da ama $B$'de değil".

**Adım 1 — Kesişim.** İki listede de olanlar:

$$
A \cap B = \{4, 5, 6\}, \quad s = 3
$$

**Adım 2 — Birleşim.** Hepsi, tekrar etmeden:

$$
A \cup B = \{1, 2, 3, 4, 5, 6, 7, 8\}, \quad s = 8
$$

**Adım 3 — Fark.** $A$'dan ortakları çıkar:

$$
A \setminus B = \{1, 2, 3\}, \quad s = 3
$$

**Sağlama:** $s(A \cup B) = 6 + 5 - 3 = 8$ ✓.

**Dikkat:** Birleşimi $6 + 5 = 11$ diye saymak ortak üç elemanı iki kez saymak demek.

**Cevap:** $8$, $3$, $3$.
