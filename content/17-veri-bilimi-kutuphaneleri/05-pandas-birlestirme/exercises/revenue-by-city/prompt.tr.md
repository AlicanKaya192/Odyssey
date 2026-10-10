`revenue_by_city(orders, cities)` her siparişi (`[order, customer, amount]`)
müşterinin şehriyle (`[customer, city]`) eşleştirip şehir başına ciroyu
`{şehir: toplam}` olarak döndürsün. Bir müşteri şehir tablosunda birden fazla
kez geçebilir; **ilk** kaydı geçerli (`drop_duplicates("customer")`).
Birleştirirken `validate="many_to_one"` ver. Başlangıç kodunda ciro iki
katına çıkıyor. **Döngü yazma.**

**Beklenen çıktı:**

```
{'Bursa': 90, 'Izmir': 360}
```
