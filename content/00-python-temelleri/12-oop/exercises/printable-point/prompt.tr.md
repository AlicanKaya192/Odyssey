Bir nesneyi doğrudan yazdırdığında okunmaz bir şey çıkıyor:

```
<__main__.Point object at 0x000001F3A2B4C110>
```

`__str__` metodu bunu düzeltiyor.

**Yapman gerekenler:**

1. `Point` adında bir sınıf yaz. Kurucusu `x` ve `y` alsın.
2. `__str__` metodu yaz: nesneyi `(3, 4)` biçiminde bir **metin olarak
   döndürsün.**
3. `distance` metodu yaz: noktanın başlangıç noktasına uzaklığını
   döndürsün — `x` ve `y` karelerinin toplamının karekökü, **iki basamağa
   yuvarlanmış.**
4. `Point(3, 4)` kur; önce nesnenin kendisini, sonra `distance` sonucunu
   yazdır.

**Beklenen çıktı:**

```
(3, 4)
5.0
```

Dikkat: `__str__` metin **döndürüyor**, yazdırmıyor. İçine `print` yazarsan
fazladan bir `None` satırı çıkıyor.

> Karekök için `math` modülünü kullan: `math.sqrt(...)`. Sayıyı metne
> katmak için `str(...)` gerekiyor.
