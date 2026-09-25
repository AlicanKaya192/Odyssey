**Ne soruluyor?** Aynı $9$ kişiden sıralı ve sırasız üçlü seçimler, bir de belli bir kişiyi içeren seçimler.

**Fikir:** Görevler farklıysa kimin hangi görevi aldığı önemli (permütasyon); aynıysa yalnızca kimlerin seçildiği önemli (kombinasyon).

**Adım 1 — Üç görev.** $P(9, 3) = 9 \cdot 8 \cdot 7 = 504$.

**Adım 2 — Heyet.** $\binom{9}{3} = \frac{504}{3!} = \frac{504}{6} = 84$.

**Adım 3 — Ayşe'li heyetler.** Ayşe'nin yeri garanti; kalan $2$ kişi öteki $8$ kişiden: $\binom{8}{2} = 28$.

**Sağlama:** Ayşe'siz heyetler $\binom{8}{3} = 56$; $28 + 56 = 84$ ✓.

**Dikkat:** Üçüncü soruda $\binom{9}{2}$ yazmak Ayşe'yi yeniden seçilebilir saymak olur; Ayşe zaten yerleşti, $8$ kişi kaldı.

**Cevap:** $504$, $84$, $28$.
