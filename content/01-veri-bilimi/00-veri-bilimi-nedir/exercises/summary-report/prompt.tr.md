Gerçek veri sana hazır sözlükler olarak gelmiyor; genelde bir dosyadan
satır satır metin olarak geliyor. Bu alıştırmada baştan sona bir mini analiz
yapacaksın: **ayrıştır, tabloya çevir, özetle.**

`raw_lines` içindeki her satır bir CSV satırı: `ad,şehir,not`.

**Yapman gerekenler:**

1. Her satırı virgülden böl ve `{"name": ..., "city": ..., "score": ...}`
   biçiminde bir sözlüğe çevir. Bunları `records` listesinde topla.
   **Not sayı olmalı**, metin değil.
2. Notları `scores` adlı bir listeye çıkar.
3. Ortalamayı hesapla ve `average` değişkeninde tut.
4. Şu dört satırı yazdır:

```
Records: 5
Lowest: 68
Highest: 91
Average: 80.6
```

**Dikkat:** notu `int()` ile çevirmezsen `max` metinleri alfabetik
karşılaştırır ve `"91"` yerine `"88"` en büyük çıkabilir. Bu, gerçek veri
işlerinde en sık yapılan hatalardan biri.
