Bu kez tersini yapıyorsun: parametrelerden adres kuruyorsun. Değerlerin
içinde boşluk ve `&` var; elle yapıştırırsan adres bozulur.

**Yapman gerekenler:**

1. `forecast_base` ile `forecast_params`'tan `url` değişkenini kur:
   taban + `?` + `urlencode(...)`.
2. `search_base` ile `{"q": "fish & chips", "lang": "en"}` sözlüğünden
   `search_url` değişkenini aynı yolla kur.
3. İkisini sırayla yazdır.

**Beklenen çıktı:**

```
https://api.example.com/v1/forecast?city=New+York&units=metric&days=3
https://api.example.com/v1/search?q=fish+%26+chips&lang=en
```

Çıktıda boşluğun `+`, `&` işaretinin ise değerin içindeyken `%26` olduğuna
bak. Parametreleri ayıran `&` olduğu gibi kalıyor.
