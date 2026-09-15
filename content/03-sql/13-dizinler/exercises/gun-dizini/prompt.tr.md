Bir günün olaylarını getiren bu sorgu doğru sonucu veriyor ama
`events` tablosunun **tamamını** okuyor:

```sql
SELECT id, created_at FROM events
WHERE created_at >= '2025-06-01' AND created_at < '2025-06-02';
```

Ölçüldü: 58 satır için 150 okuma — tablonun bütün sayfaları. `created_at`
üzerine bir dizin kur. Aynı sorgu dizinle **2 okumaya** iniyor.

Bu alıştırmada bir sonuç tablosu yok; yazdığın `CREATE INDEX` denetleniyor.
Denetim dizinin **adına** bakmıyor, yapısına bakıyor: hangi sütun(lar)
üzerinde kurulduğuna. `events` üzerinde birincil anahtar dışında tek bir
dizin olmalı.

Her çalıştırma sonunda geri alındığı için dizini istediğin kadar yeniden
kurabilirsin.
