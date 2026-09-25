**Fikir:** Gauss'un yolu: ilk sırayı sonuncuyla, ikinciyi sondan ikinciyle eşleştir. Her çift aynı toplamı verir.

**Adım 1 — Son sıra.** Her sıra $3$ ekliyor, ilk sıradan sonra $19$ sıra daha var: $12 + 57 = 69$.

**Adım 2 — Çiftler.** $12 + 69 = 81$, $15 + 66 = 81$, $18 + 63 = 81$… Biri yukarı çıkarken öteki aynı miktar iniyor, toplam hep $81$. $20$ sıra $10$ çift eder: $10 \cdot 81 = 810$.

**Adım 3 — $50$'yi geçmek.** $50 - 12 = 38$ koltuk eklenmeli. $3$'erli eklemelerle $12$ ekleme $36$ eder ($48$ koltuk, yetmez), $13$ ekleme $39$ eder ($51$ koltuk). $13$ ekleme, ilk sıradan $13$ sonrası, yani $14.$ sıra.

**Neden aynı sonuç?** Toplam formülündeki $\frac{n}{2}$ çift sayısı, $(a_1 + a_n)$ de her çiftin toplamı. Üçüncü adımdaki "kaç ekleme" sayısı formüldeki $n - 1$.

**Cevap:** $69$, $810$ ve $14$.
