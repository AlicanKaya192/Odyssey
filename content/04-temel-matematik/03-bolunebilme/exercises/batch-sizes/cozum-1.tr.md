**Ne soruluyor?** $360$'ı tam bölen sayıların kaç tane olduğu ve bunlardan belli bir aralıkta kalanlar.

**Fikir:** Yığın boyutu $k$ ise $360 = k \cdot (\text{yığın sayısı})$; yani $k$, $360$'ın böleni. Bölenlerin sayısı asal çarpanlardan hesaplanır; aralıktakiler için bölenleri çift çift listeleriz.

**Adım 1 — Asal çarpanlar.**

$$
360 = 2^3 \cdot 3^2 \cdot 5
$$

**Adım 2 — Bölen sayısı.** Her bölen $2^a \cdot 3^b \cdot 5^c$ biçiminde; $a$ için $4$, $b$ için $3$, $c$ için $2$ seçenek:

$$
(3 + 1)(2 + 1)(1 + 1) = 24
$$

**Adım 3 — Bölenleri çift çift yaz.**

| Küçük | Büyük |
|---|---|
| $1$ | $360$ |
| $2$ | $180$ |
| $3$ | $120$ |
| $4$ | $90$ |
| $5$ | $72$ |
| $6$ | $60$ |
| $8$ | $45$ |
| $9$ | $40$ |
| $10$ | $36$ |
| $12$ | $30$ |
| $15$ | $24$ |
| $18$ | $20$ |

$12$ çift, $24$ bölen ✓.

**Adım 4 — $10$ ile $50$ arası.** Soldan $10, 12, 15, 18$; sağdan $45, 40, 36, 30, 24, 20$:

$$
4 + 6 = 10
$$

**Dikkat:** Çift çift ararken $7$ ($360 = 7 \cdot 51 + 3$) ve $11$ gibi bölmeyenleri atla, ama $8$ ve $9$'u unutma.

**Cevap:** $24$ seçenek; bunlardan $10$ tanesi $10$ ile $50$ arasında.
