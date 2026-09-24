**Ne soruluyor?** Tümleyenlerin kesişiminin ve birleşiminin eleman sayısı.

**Fikir:** Tümleyenlerle doğrudan çalışmak zor; De Morgan kuralları onları tek bir tümleyene çeviriyor. Bir kümenin tümleyeninin eleman sayısı, $50$'den o kümenin eleman sayısı çıkarılarak bulunur.

**Adım 1 — Birleşim.** $s(A \cup B) = 20 + 25 - 10 = 35$.

**Adım 2 — $A' \cap B'$.** De Morgan: $A' \cap B' = (A \cup B)'$:

$$
s(A' \cap B') = 50 - 35 = 15
$$

**Adım 3 — $A' \cup B'$.** De Morgan: $A' \cup B' = (A \cap B)'$:

$$
s(A' \cup B') = 50 - 10 = 40
$$

**Sonucu yorumla:** $A' \cap B'$ "ikisinde de olmayanlar" ($15$); $A' \cup B'$ "ikisinde birden olmayanlar", yani kesişim dışındaki herkes ($40$).

**Dikkat:** $s(A' \cup B')$'yi $s(A') + s(B') = 30 + 25 = 55$ diye hesaplamak ortakları iki kez sayar; $55$, $50$'yi bile geçiyor.

**Cevap:** $15$ ve $40$.
