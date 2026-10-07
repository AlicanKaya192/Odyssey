Bir hava durumu API'sinden JSON metni geldi. Onu Python sözlüğüne çevirip
içinden değerleri okuyacaksın.

**Yapman gerekenler:**

1. `json.loads` ile `text`'i `data` adlı bir sözlüğe çevir.
2. Şehri, sıcaklığı, yağmur durumunu ve rüzgârı aşağıdaki biçimde yazdır.
3. Son satırda sıcaklığın Python türünün adını yazdır
   (`type(...).__name__`).

**Beklenen çıktı:**

```
city: Istanbul
temp: 18.5
rain: False
wind: None
temp type: float
```

JSON'daki `false` ve `null`, Python'da `False` ve `None` olarak geliyor.
