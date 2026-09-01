`datetime` modülü tarihlerle çalışmak için. Bu alıştırmada iki tarih
arasındaki gün sayısını bulacaksın.

**Yapman gerekenler:**

1. `datetime` modülünden `date` sınıfını al: `from datetime import date`
2. İki tarih tanımla:
   - `start` — 1 Ocak 2026
   - `end` — 1 Mart 2026
3. `gap` adında bir değişkende aradaki **gün sayısını** tut.
4. `label` adında bir değişkende `start` tarihinin metin hâlini tut.
5. Önce `gap`, sonra `label` yazdır.

**Beklenen çıktı:**

```
59
2026-01-01
```

> İki tarihi çıkarınca bir `timedelta` çıkıyor; gün sayısı onun `.days`
> özelliğinde. Tarihin metin hâlini `.isoformat()` veriyor.
