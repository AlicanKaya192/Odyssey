Bir istek göndermeden önce belgeye bakıp "bu istek doğru mu?" diye sormak,
birçok hatayı daha istek gitmeden yakalar. `docs` sözlüğü hayali bir API'nin
belgesi: her uç noktanın **zorunlu** (`required`) ve **isteğe bağlı**
(`optional`) bilgileri.

**Yapman gerekenler:** `check(path, params)` fonksiyonunu yaz. `params`
gönderilecek bilgilerin adlarından oluşan bir liste. Şu sırayla denetle:

1. Uç nokta belgede yoksa `"404 unknown endpoint"` döndür.
2. Zorunlu bilgilerden biri `params` içinde yoksa, **belgedeki sırayla ilk
   eksik olanı** `"missing: days"` biçiminde döndür.
3. `params` içinde belgede hiç geçmeyen bir ad varsa, **ilk bulunanı**
   `"unknown: color"` biçiminde döndür.
4. Hepsi yerindeyse `"ok"` döndür.

Sonra aşağıdaki beş isteği denetleyip sonuçları sırayla yazdır.

**Beklenen çıktı:**

```
/weather ['city'] -> ok
/news [] -> 404 unknown endpoint
/forecast ['city'] -> missing: days
/weather ['city', 'color'] -> unknown: color
/cities [] -> ok
```
