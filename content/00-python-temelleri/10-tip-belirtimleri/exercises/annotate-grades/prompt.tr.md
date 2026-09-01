Bu alıştırmada kapların içinde ne olduğunu yazacaksın.

**Yapman gerekenler:**

1. İki değişkeni belirtimleriyle birlikte tanımla:
   - `grades` — metin anahtarlı, tam sayı değerli bir sözlük. Başlangıç
     değeri: `{"Ada": 90, "Alan": 70}`
   - `passed` — metinlerden oluşan **boş** bir liste.

2. `average` adında bir fonksiyon yaz:
   - Parametresi `values`, metin anahtarlı tam sayı değerli bir sözlük.
   - Geriye bir tam sayı döndürüyor.
   - Değerlerin ortalamasını **tam bölme** ile hesaplıyor: `sum(...) // len(...)`

3. `grades` içinde dolaş; notu **80 veya üstü** olan ismi `passed` listesine ekle.

4. Önce ortalamayı, sonra `passed` listesini yazdır.

**Beklenen çıktı:**

```
80
['Ada']
```

> `passed` boş bir listeyle başlıyor. İçine ne konacağı koda bakılarak
> anlaşılmadığı için belirtim tam da burada gerekiyor.
