Gerçek veri temiz gelmiyor. Yanına konan `data.txt` dosyasında hem geçerli
satırlar, hem boş satır, hem de bozuk satırlar var:

```
Ada,90
Brian,notanumber
Grace,75

Alan,60
Edith
```

**Yapman gerekenler:**

1. Dosyayı oku. `scores` adında bir sözlük kur: yalnızca **geçerli** satırları
   al, anahtar isim, değer sayı olarak not.
2. Boş satırları atla.
3. Notu sayıya çevrilemeyen satırları atla (`ValueError`).
4. Virgül içermeyen satırları da atla — bölme işlemi `ValueError` veriyor.
5. `skipped` adlı değişkende atlanan **bozuk** satır sayısını tut. Boş satır
   bozuk sayılmıyor.
6. Önce `scores`, sonra `skipped` yazdır.

**Beklenen çıktı:**

```
{'Ada': 90, 'Grace': 75, 'Alan': 60}
2
```

> `"Edith".split(",")` tek elemanlı liste veriyor; onu iki değişkene açmaya
> çalışmak `ValueError` çıkarıyor. Yani tek bir `except ValueError` iki
> durumu birden yakalıyor.
