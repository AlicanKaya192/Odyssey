Küçük bir fiş yazdıracaksın: kalemler, ara toplam, indirim ve toplam.

Elindeki veri:

```python
order_no = 7
items = [("Keyboard", 1, 450.0), ("Mouse", 2, 175.5), ("Cable", 3, 39.9)]
discount = 0.1
```

**Yapman gerekenler:**

1. Sipariş numarasını **üç basamaklı**, başı sıfırlı yaz.
2. Döngüyle her kalemi yaz: ad sola yaslı **12**, adet sağa yaslı **4**,
   satır tutarı (`count * price`) sağa yaslı **10** ve iki basamaklı.
3. `subtotal` — kalemlerin toplamı.
4. `saving` — indirim tutarı (`subtotal * discount`).
5. `total` — indirim sonrası tutar.
6. Son üç satırı yaz: etiket sola yaslı **16**, tutar sağa yaslı **10** ve
   iki basamaklı. İndirim satırındaki tutar **eksi** işaretli.

**Beklenen çıktı:**

```
Order 007
Keyboard       1    450.00
Mouse          2    351.00
Cable          3    119.70
Subtotal            920.70
Discount (10%)      -92.07
Total               828.63
```

> İndirim etiketinde yüzde de var: `f"Discount ({discount:.0%})"`.
