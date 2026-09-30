Dört farklı sistemden gelen dört tarih var; her biri başka biçimde:

| Metin | Nereden | Biçim |
|---|---|---|
| `09.03.2024` | Türkiye'deki bir form | gün.ay.yıl |
| `12/25/2023` | ABD'deki bir sistem | ay/gün/yıl |
| `2024-07-01 08:15` | Bir veritabanı | ISO 8601 |
| `1 February 2024` | Bir e-posta | gün, ayın adı, yıl |

**Yapman gerekenler:**

1. Her metni `datetime`'a çevir: ilk ikisi ve sonuncusu için `strptime` ile
   doğru biçimi yaz, ISO olan için `fromisoformat` kullan.
2. Dördünü bir listeye koy ve **sırala**.
3. Sıralanmış listedeki her tarihi `isoformat()` ile alt alta yazdır.

**Beklenen çıktı:**

```
2023-12-25T00:00:00
2024-02-01T00:00:00
2024-03-09T00:00:00
2024-07-01T08:15:00
```

Hepsi aynı dile, ISO 8601'e çevrildi ve artık doğru sıralanıyor. Farklı
kaynaklardan gelen tarihleri birleştirmenin yolu bu: önce hepsini tek bir
türe çevir, sonra karşılaştır.
