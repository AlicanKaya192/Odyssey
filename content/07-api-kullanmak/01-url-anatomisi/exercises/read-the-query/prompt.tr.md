Sunucunun kaydından bir isteğin sorgu dizesi geldi. İçinde aynı ad birden
çok kez geçiyor (`tag`).

**Yapman gerekenler:**

1. `parse_qs` ile `query`'yi bir sözlüğe çevir.
2. `city` ve `units` değişkenlerine **düz metin** olarak şehri ve birimi
   koy (liste değil).
3. `tags` değişkenine etiketlerin **listesini** koy.
4. Aşağıdaki gibi yazdır; son satırda etiketler virgül ve boşlukla
   birleşik.

**Beklenen çıktı:**

```
Ankara
imperial
3 tags: sea, museum, castle
```

`parse_qs` her değeri listeye koyar: şehir için `[0]` ile ilk öğeyi alman
gerekiyor, etiketler için listenin tamamını.
