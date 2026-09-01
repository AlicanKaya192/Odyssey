Bir fonksiyonun kaç argüman alacağı önceden bilinmiyorsa `*` kullanılıyor.

**Yapman gerekenler:**

1. `total` adında bir fonksiyon yaz: **kaç tane olursa olsun** sayı alsın ve
   toplamlarını döndürsün. Hiç argüman verilmezse `0` döndürsün.

2. `describe` adında bir fonksiyon yaz: bir `label` metni ve ardından
   **adıyla verilen** herhangi bir sayıda ek bilgi alsın. Geriye şu biçimde
   bir metin döndürsün:

```
report: name=Ada, city=London
```

   Yani önce `label`, iki nokta ve boşluk, sonra `anahtar=deger` çiftleri
   virgül ve boşlukla ayrılmış. Hiç ek bilgi yoksa yalnızca `report:`
   döndürsün.

3. Şunları sırayla yazdır:
   - `total(1, 2, 3)`
   - `total()`
   - `describe("report", name="Ada", city="London")`
   - `describe("empty")`

**Beklenen çıktı:**

```
6
0
report: name=Ada, city=London
empty:
```

> `*numbers` gelen argümanları bir demette, `**details` adıyla verilenleri
> bir sözlükte topluyor. Parçaları birleştirmek için
> `", ".join(parcalar)` kullanabilirsin.
