Bir program çalışırken olmayan bir dosyayla karşılaşabiliyor. İyi bir program
bu yüzden çökmüyor; varsayılana düşüyor.

Yanına `settings.txt` konuldu ama `profile.txt` **yok**.

**Yapman gerekenler:**

1. `load_settings` adında bir fonksiyon yaz. Bir dosya adı alsın.
   - Dosya varsa: her satırı `anahtar=deger` diye bölüp bir sözlük döndürsün.
   - Dosya **yoksa**: `FileNotFoundError` yakalanıp **boş sözlük** dönsün.
2. Fonksiyonu iki dosyayla dene:
   - `load_settings("settings.txt")`
   - `load_settings("profile.txt")`
3. `found` ve `missing` adlı değişkenlerde sonuçları tut, sırayla yazdır.

**Beklenen çıktı:**

```
{'theme': 'dark', 'lang': 'en'}
{}
```

Program hata vermeden bitmeli. Olmayan dosya burada bir sorun değil, beklenen
bir durum.

> Dosya adı `open` çağrısına gitmeden hata çıkmıyor; bu yüzden `try` bloğu
> `with` satırını da kapsamalı.
