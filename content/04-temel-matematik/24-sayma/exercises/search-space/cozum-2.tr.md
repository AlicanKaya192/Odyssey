**Fikir:** Alt kümeleri boyutlarına göre ayır: $0$, $1$, …, $10$ özellikli. Her boyutun sayısı Pascal üçgeninin $10.$ satırındaki bir sayı.

**Adım 1 — Izgara.** Her ayarı bir yol gibi düşün: önce öğrenme oranı ($5$), sonra derinlik ($4$), sonra ağaç sayısı ($3$), sonra kat ($5$): $5 \cdot 4 \cdot 3 \cdot 5 = 300$.

**Adım 2 — Satır.** $10.$ satır: $1, 10, 45, 120, 210, 252, 210, 120, 45, 10, 1$. Dördüncü sayı ($k = 3$) $120$.

**Adım 3 — Toplam.** Satırın toplamı $1024$; boyutu $0$ olan tek alt kümeyi çıkar: $1023$.

**Neden aynı sonuç?** Pascal satırının toplamının $2^n$ olması, "her özelliği al ya da alma" sayımının boyutlara göre gruplanmış hâli. Kat sayısını ayar zincirine eklemek de $60 \cdot 5$ çarpımının aynısı.

**Cevap:** $300$, $120$ ve $1023$.
