Üç gece vardiyasının başlangıcı ve süresi belli:

```python
shifts = [
    ("2024-03-08 22:15", 7, 50),   # baslangic, saat, dakika
    ("2024-03-09 23:40", 6, 30),
    ("2024-03-10 21:05", 9, 0),
]
```

**Yapman gerekenler:**

1. Listeyi dolaş. Her vardiya için başlangıcı `fromisoformat` ile oku, süreyi
   `timedelta(hours=..., minutes=...)` ile kur, bitişi hesapla.
2. Her vardiya için bitişi `"%Y-%m-%d %H:%M"` biçiminde ve bittiği günün
   adını (`%A`) aynı satıra yazdır.
3. Üç vardiyanın toplam süresini **saat** olarak yazdır (bir ondalık).
   Toplamı `timedelta` olarak biriktir, sonunda `total_seconds() / 3600`.

**Beklenen çıktı:**

```
2024-03-09 06:05 Saturday
2024-03-10 06:10 Sunday
2024-03-11 06:05 Monday
23.3
```

Gece yarısını geçen her vardiya ertesi güne düştü; tarih kendiliğinden
değişti. Elle "22 + 7 = 29" diye hesaplayan kod burada çoktan
yanılmıştı.
