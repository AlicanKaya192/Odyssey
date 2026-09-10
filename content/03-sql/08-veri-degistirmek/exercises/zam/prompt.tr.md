`ACC` kategorisindeki ürünlerin fiyatını **%10 arttır**.

Diğer kategorilerin fiyatı değişmemeli — kontrol ikisine birden bakıyor.

**Fiyatları elle hesaplama.** Altı ürünün yeni fiyatını hesap makinesiyle
bulup tek tek yazabilirsin ama bu, bir sonraki `ACC` ürünü eklendiğinde
işe yaramayan bir çözüm olur.

`SET` içinde sütunun kendisini kullanabiliyorsun:

```sql
SET price = price * 1.10
```

Sunucu bunu her satır için ayrı ayrı yapıyor: o satırın kendi eski
fiyatını okuyup yenisini yazıyor.

`WHERE` yazmayı unutma. Unutursan on iki ürünün on ikisi birden zamlanır
ve sunucu bunu hata saymaz.
