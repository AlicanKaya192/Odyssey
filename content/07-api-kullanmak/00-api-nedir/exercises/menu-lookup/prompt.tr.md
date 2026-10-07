İlk sunucunu yazıyorsun; çok küçük bir sunucu. Elinde bir **menü** var:
her uç noktanın yanıtı bir sözlükte duruyor.

**Yapman gerekenler:**

1. `request(path)` adında bir fonksiyon yaz. `path` menüde varsa yanıtını
   döndürsün, yoksa `"404 Not Found"` döndürsün.
2. `"/weather"`, `"/cities"` ve `"/news"` için istek gönder ve yanıtları
   sırayla yazdır.

**Beklenen çıktı:**

```
18 degrees, cloudy
Istanbul, Ankara, Izmir
404 Not Found
```

Burada `request` fonksiyonu sunucu, onu çağıran satırlar istemci. Gerçek bir
API'de aradaki tek fark, isteğin internet üzerinden gitmesi.
