**Ne soruluyor?** Üslü büyüyen bir niceliğin belli bir süre sonraki değeri ve belli bir değere ulaşma süresi.

**Fikir:** $k$ kez iki katına çıkan bir sayı $2^k$ ile çarpılır. Önce süreyi katlanma sayısına çevir, sonra $100 \cdot 2^k$ yaz.

**Adım 1 — Katlanma sayısı.** $2$ saat $= 120$ dakika; $120 \div 20 = 6$ katlanma.

**Adım 2 — $2$ saat sonra.**

$$
100 \cdot 2^6 = 100 \cdot 64 = 6\,400
$$

**Adım 3 — $51\,200$ için gereken katlanma.** $100 \cdot 2^k = 51\,200$ ise

$$
2^k = 512 = 2^9 \quad\Rightarrow\quad k = 9
$$

**Adım 4 — Süre.** $9$ katlanma $\cdot\, 20$ dakika $= 180$ dakika ($3$ saat).

**Sağlama:** $100 \to 200 \to 400 \to 800 \to 1\,600 \to 3\,200 \to 6\,400$ (6 adım) $\to 12\,800 \to 25\,600 \to 51\,200$ (9 adım) ✓.

**Dikkat:** $2$ saatte "$\cdot 6$" ya da "$+ 6 \cdot 100$" yazmak, iki katına çıkmayı toplama sanmak demek. Her katlanma bir önceki sayıyı ikiyle çarpar.

**Cevap:** $6\,400$ bakteri; $180$ dakika.
