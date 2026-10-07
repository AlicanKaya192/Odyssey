Aylık ciroyu ödeme türüne göre DuckDB ile özetle, payları pandas ile
hesapla.

**Yapman gerekenler:**

1. Başlangıç kodu 200 000 siparişi `orders.parquet` olarak yazıyor.
2. DuckDB ile ay (`strftime(order_time, '%Y-%m')`) ve ödeme türü başına
   ciroyu (`quantity * unit_price` toplamı) bul ve `.df()` ile pandas'a al.
3. `pivot` ile ay × ödeme türü tablosu kur; her ayın içinde payları yüzde
   olarak hesapla.
4. İlk üç ay için ayı ve kart (`card`) payını (bir ondalık) yazdır.
5. Son satıra nakit (`cash`) payının on iki aylık ortalamasını (bir
   ondalık) yazdır.

**Beklenen çıktı:**

```
2024-01 71.5
2024-02 72.7
2024-03 71.1
8.1
```
