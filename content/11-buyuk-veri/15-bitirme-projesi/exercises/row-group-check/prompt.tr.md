Ödeme türüne göre sipariş sayısını ve ciroyu iki yoldan hesapla: satır
gruplarından kısmi toplamlarla ve DuckDB ile.

**Yapman gerekenler:**

1. `orders.parquet` hazır (500 000 satır, 100 000'lik satır grupları).
2. Her satır grubunu (`read_row_group`, yalnızca `payment`, `quantity`,
   `unit_price`) oku; ödeme türü başına sipariş sayısını ve ciroyu kısmi
   olarak çıkar ve `counts`, `revenue` sözlüklerinde birleştir.
3. Ödeme türlerini abece sırasıyla, her satıra tür, sayı ve ciro (iki
   ondalık) olacak şekilde yazdır.
4. DuckDB ile aynı sayıları dosyadan hesapla; sayılar birebir, cirolar
   0,01'den az farkla tutuyor mu, yazdır.

**Beklenen çıktı:**

```
card 359248 589500728.87
cash 40550 66462584.76
transfer 100202 164306286.55
True
```
