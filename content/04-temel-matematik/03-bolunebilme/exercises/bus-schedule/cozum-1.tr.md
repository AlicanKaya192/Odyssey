**Ne soruluyor?** İki farklı döngünün ne zaman çakıştığı ve belli bir süre içinde kaç kez çakıştığı.

**Fikir:** A hattı $0, 12, 24, 36, \dots$ dakikalarda; B hattı $0, 18, 36, \dots$ dakikalarda kalkıyor. Birlikte kalkış anları ikisinin de **ortak katları**. İlki EKOK, sonrakiler EKOK'un katları.

**Adım 1 — Asal çarpanlar.**

$$
12 = 2^2 \cdot 3, \qquad 18 = 2 \cdot 3^2
$$

**Adım 2 — EKOK: bütün asallar, büyük üsler.**

$$
\text{EKOK}(12, 18) = 2^2 \cdot 3^2 = 36
$$

İlk birlikte kalkıştan $36$ dakika sonra, yani $08{:}36$'da yeniden birlikte kalkarlar.

**Adım 3 — Süre.** $08{:}00$–$12{:}00$ arası $4 \cdot 60 = 240$ dakika.

**Adım 4 — $36$'nın katlarını say.** Birlikte kalkışlar $0, 36, 72, 108, 144, 180, 216$. dakikalarda. Bir sonraki $252 > 240$, $12{:}00$'den sonra. Kalanlı bölmeyle: $240 = 36 \cdot 6 + 24$; $6$ kat artı başlangıç ($0$):

$$
6 + 1 = 7
$$

**Dikkat:** $240 \div 36 \approx 6$ deyip $6$ yazmak sık bir hata; $08{:}00$'deki ilk kalkış da sayılıyor.

**Cevap:** $36$ dakika; $7$ kez.
