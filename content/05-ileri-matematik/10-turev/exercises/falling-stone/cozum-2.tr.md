**Fikir:** Limiti hesaplamadan önce sayılarla görmek: $[3, 3 + h]$ aralığındaki ortalama hızı küçülen $h$'ler için hesapla, sayıların nereye gittiğine bak.

**Adım 1 — Ortalama.** Birinci çözümdeki gibi $20$.

**Adım 2 — Tablo.**

| $h$ | $s(3 + h)$ | ortalama hız |
|---|---|---|
| $1$ | $80$ | $35$ |
| $0{,}1$ | $48{,}05$ | $30{,}5$ |
| $0{,}01$ | $45{,}3005$ | $30{,}05$ |

**Adım 3 — Sol taraftan.** $h = -0{,}01$: $s(2{,}99) = 44{,}7005$, ortalama $\frac{44{,}7005 - 45}{-0{,}01} = 29{,}95$. İki yandan da $30$.

**Neden aynı sonuç?** Tablodaki her satır $30 + 5h$ formülünün bir değeri; limit, tablonun "sonsuz küçük $h$" satırı. Sayılar yöntemi yönü gösterir, limit kesin değeri verir.

**Cevap:** $20$ ve $30$.
