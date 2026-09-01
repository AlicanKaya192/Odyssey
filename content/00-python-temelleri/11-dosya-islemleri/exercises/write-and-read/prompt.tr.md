İlk dosyanı yazacak, sonra aynı dosyayı geri okuyacaksın.

**Yapman gerekenler:**

1. `names.txt` adında bir dosya aç ve içine üç satır yaz:

```
Ada
Alan
Grace
```

2. Aynı dosyayı geri aç ve satırları bir listeye al.
3. Listeyi `names` adında bir değişkende tut.
4. Önce kaç satır olduğunu, sonra listenin kendisini yazdır.

**Beklenen çıktı:**

```
3
['Ada', 'Alan', 'Grace']
```

Dikkat: `write` alt satıra kendiliğinden geçmiyor, `\n` yazman gerekiyor.

> Dosyayı her zaman `with open(...) as file:` ile aç ve
> `encoding="utf-8"` yazmayı unutma. Satır listesi için
> `file.read().splitlines()` kullanabilirsin.
