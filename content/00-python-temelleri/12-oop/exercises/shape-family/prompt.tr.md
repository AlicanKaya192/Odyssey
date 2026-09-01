İki şeklin ortak yanı var: ikisinin de bir adı var ve ikisi de kendini
tanıtabiliyor. Farkı, alanı nasıl hesapladıkları. Ortak kısmı bir kez yazıp
devredeceksin.

**Yapman gerekenler:**

1. `Shape` adında bir üst sınıf yaz:
   - Kurucusu `name` alsın.
   - `describe` metodu şu metni **döndürsün**:
     `ad has area SAYI` — örneğin `rectangle has area 12`

2. `Rectangle` sınıfı — `Shape`'ten türesin:
   - Kurucusu `width` ve `height` alsın.
   - Üst sınıfın kurucusunu `"rectangle"` adıyla çağırsın.
   - `area` metodu: genişlik çarpı yükseklik.

3. `Circle` sınıfı — `Shape`'ten türesin:
   - Kurucusu `radius` alsın.
   - Üst sınıfın kurucusunu `"circle"` adıyla çağırsın.
   - `area` metodu: `math.pi * radius * radius`, **iki basamağa yuvarlanmış.**

4. `Rectangle(3, 4)` ve `Circle(2)` kurup `describe` sonuçlarını yazdır.

**Beklenen çıktı:**

```
rectangle has area 12
circle has area 12.57
```

Dikkat: `describe` metodu yalnızca `Shape` içinde yazılıyor, ama `self.area()`
çağırıyor — ve çalışırken **nesnenin kendi** `area` metodu bulunuyor.

> Üst sınıfın kurucusu `super().__init__(...)` ile çağrılıyor. Yazmazsan
> `self.name` hiç oluşmuyor ve `describe` hata veriyor.
