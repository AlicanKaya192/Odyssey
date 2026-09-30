Bir sunucu logu olayların zamanını Unix zamanı olarak yazmış. Ama iki
farklı servisten geldiği için bazıları saniye, bazıları milisaniye:

```python
stamps = [1710000000, 1710003600123, 1710009000, 1710012345000]
```

**Yapman gerekenler:**

1. Her sayıya bak: `1e12`'den büyükse milisaniyedir, `1000`'e böl.
2. `datetime.fromtimestamp(saniye, tz=timezone.utc)` ile UTC zamanına çevir.
3. Her olayı `"%Y-%m-%d %H:%M:%S"` biçiminde alt alta yazdır.
4. İlk olay ile son olay arasında geçen süreyi **dakika** olarak yazdır (bir
   ondalık).

**Beklenen çıktı:**

```
2024-03-09 16:00:00
2024-03-09 17:00:00
2024-03-09 18:30:00
2024-03-09 19:25:45
205.8
```

Bölmeyi unutsaydın milisaniyeli satırlar on binlerce yıl sonrasına gidip
hata verecekti. `tz=timezone.utc` yazmasaydın aynı kod başka bir bilgisayarda
başka saatler basacaktı.
