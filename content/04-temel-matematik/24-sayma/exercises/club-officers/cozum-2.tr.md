**Fikir:** Heyet sayısını permütasyondan, Ayşe'li heyetleri de "her kişi eşit sıklıkta" düşüncesinden bul.

**Adım 1 — Görevler.** Başkana $9$, yardımcıya $8$, saymana $7$ aday: $504$.

**Adım 2 — Heyet.** Aynı üç kişi $3! = 6$ farklı görev dağılımıyla $504$'te altı kez sayıldı: $504 / 6 = 84$.

**Adım 3 — Ayşe.** $84$ heyette toplam $84 \cdot 3 = 252$ koltuk var ve $9$ kişi simetrik; her kişi $\frac{252}{9} = 28$ heyette yer alır.

**Neden aynı sonuç?** $\frac{3}{9} \binom{9}{3} = \binom{8}{2}$ eşitliği, "bir kişiyi sabitle, kalanlardan seç" ile "koltukları eşit paylaştır" düşüncelerinin aynı sayıya çıktığını söyler.

**Cevap:** $504$, $84$ ve $28$.
