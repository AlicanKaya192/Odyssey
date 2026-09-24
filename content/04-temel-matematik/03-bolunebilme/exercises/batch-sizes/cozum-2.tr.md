**Fikir:** Yığın boyutu $k$ ise yığın sayısı $360 \div k$. Boyut $10$ ile $50$ arasındaysa yığın sayısı $360 \div 50 = 7{,}2$ ile $360 \div 10 = 36$ arasında olur. Yani aralıktaki boyutları saymak, $8$ ile $36$ arasındaki bölenleri saymakla aynı.

**Adım 1 — Toplam seçenek.** Her bölen bir yığın boyutu verir: $360 = 2^3 \cdot 3^2 \cdot 5$'ten $4 \cdot 3 \cdot 2 = 24$ seçenek.

**Adım 2 — Yığın sayısının aralığı.** $10 \le k \le 50$ ise yığın sayısı $m = 360 \div k$ için

$$
7{,}2 \le m \le 36
$$

$m$ de $360$'ın bir böleni ve tam sayı, yani $8 \le m \le 36$.

**Adım 3 — Bu aralıktaki bölenler.** $360$'ın bölenlerinden $8$ ile $36$ arasında olanlar:

$$
8, 9, 10, 12, 15, 18, 20, 24, 30, 36
$$

$10$ tane. Her biri bir yığın boyutuna karşılık geliyor: $m = 8 \to k = 45$, $m = 36 \to k = 10$, …

**Neden aynı sonuç?** Bölenler çift çift geliyor: $k$ bir bölense $360 \div k$ de bölen. Bu eşleme, $10$–$50$ arasındaki boyutları $8$–$36$ arasındaki yığın sayılarına birebir götürüyor; ikisini saymak aynı sonucu veriyor.

**Cevap:** $24$ ve $10$.
