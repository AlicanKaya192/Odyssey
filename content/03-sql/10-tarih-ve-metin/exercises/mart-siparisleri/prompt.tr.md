Mart 2026'da verilen siparişleri getir.

Sütunlar: `id`, `order_date`. `id`'ye göre sırala. Sonuç üç satır.

**`MONTH()` kullanma** — kontrol buna bakıyor. Bir tarih aralığıyla süz:
ay başı **dahil**, bir sonraki ayın başı **hariç**.

```sql
WHERE order_date >= '2026-03-01' AND order_date < '2026-04-01'
```

Buna yarı açık aralık deniyor. `MONTH(order_date) = 3` her yılın Mart'ını
getirir ve sütuna işlev uyguladığı için ileride dizinlerden
yararlanamaz; `BETWEEN ... '2026-03-31'` ise sütunda saat olsaydı 31 Mart
öğleden sonrasını kaçırırdı (ölçüldü: dört olaydan biri dışarıda kaldı).
