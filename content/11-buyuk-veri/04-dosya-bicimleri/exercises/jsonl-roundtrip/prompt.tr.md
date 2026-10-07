Siparişleri JSON Lines olarak yaz, dosyanın içine bak, geri oku ve
CSV'yle boyut karşılaştır.

**Yapman gerekenler:**

1. `small = make_orders(4)[["order_id", "quantity"]]` tablosunu
   `orders.jsonl` dosyasına JSON Lines olarak yaz
   (`orient="records", lines=True`).
2. Dosyayı `open` ile oku; satır sayısını ve ilk satırı yazdır.
3. Dosyayı `pd.read_json(..., lines=True)` ile geri oku; satır ve sütun
   sayısını (`shape`) ve `quantity` toplamını aynı satıra yazdır.
4. `big = make_orders(50_000)` tablosunu hem `big.jsonl` hem `big.csv`
   (`index=False`) olarak yaz; JSON boyutunun CSV boyutuna oranını iki
   ondalığa yuvarlayıp yazdır.

**Beklenen çıktı:**

```
4
{"order_id":1,"quantity":2}
(4, 2) 15
2.61
```
