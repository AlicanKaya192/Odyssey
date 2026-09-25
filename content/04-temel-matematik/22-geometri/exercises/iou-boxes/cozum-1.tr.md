**Ne soruluyor?** İki dikdörtgenin örtüşen alanı, birleşimi ve oranları.

**Fikir:** Eksenlere paralel iki dikdörtgenin kesişimi, $x$ aralıklarının ortak kısmı ile $y$ aralıklarının ortak kısmının oluşturduğu dikdörtgen.

**Adım 1 — Kesişim.** $x$: $[1, 5]$ ve $[3, 7]$'nin ortağı $[3, 5]$, genişlik $2$. $y$: $[1, 4]$ ve $[2, 6]$'nın ortağı $[2, 4]$, yükseklik $2$. Kesişim $2 \cdot 2 = 4$.

**Adım 2 — Birleşim.** Gerçek kutu $4 \cdot 3 = 12$, tahmin $4 \cdot 4 = 16$.

$$
12 + 16 - 4 = 24
$$

**Adım 3 — IoU.** $\frac{4}{24} = \frac{1}{6} \approx 0{,}17$.

**Sağlama:** IoU $0$ ile $1$ arasında olmalı ✓; $0{,}5$'in altında, yani bu tahmin genellikle "doğru tespit" sayılmaz.

**Dikkat:** Birleşimde kesişimi çıkarmayı unutursan $28$ bulursun; ortak bölge iki kez sayılmış olur.

**Cevap:** Kesişim $4$, birleşim $24$, $\text{IoU} = \frac{1}{6}$.
