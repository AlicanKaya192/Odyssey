Sınıflarda hataların çoğu aynı birkaç yerden çıkıyor. Hepsi burada.

## 1. `self.` unutmak

```python
class Student:
    def __init__(self, name):
        self.name = name

    def greet(self):
        return "hello " + name
```

```
NameError: name 'name' is not defined
```

`name` diye serbest bir değişken yok. O değer nesnenin içinde duruyor ve
oraya `self.name` ile ulaşılıyor.

Kural: **metot içinde nesnenin verisine her erişimde `self.` yazılır.**

## 2. `__init__` içinde `self.` unutmak

Bu daha sinsi, çünkü **hata vermiyor**:

```python
class Student:
    def __init__(self, name):
        name = name          # self. yok
```

Bu satır bir şey yapmıyor: yerel parametreyi kendisine atıyor ve fonksiyon
bitince kayboluyor. Sonra:

```python
ada = Student("Ada")
print(ada.name)
```

```
AttributeError: 'Student' object has no attribute 'name'
```

Hata `__init__`'te değil, çok sonra çıkıyor. Aramaya yanlış yerde
başlıyorsun.

## 3. Metotta `self` parametresini yazmamak

```python
class Student:
    def greet():
        return "hello"


Student().greet()
```

```
TypeError: Student.greet() takes 0 positional arguments but 1 was given
```

Mesaj kafa karıştırıcı: "hiç argüman almıyor ama bir tane verildi." Verilen
argüman nesnenin kendisi — Python onu otomatik gönderiyor.

Çözüm: `def greet(self):`

## 4. Paylaşılan sınıf değişkeni

Bu, listenin başına yazılmayı hak eden tuzak. Hata vermiyor ve bulunması çok
zor:

```python
class Basket:
    items = []                    # sinif seviyesinde

    def add(self, item):
        self.items.append(item)


first = Basket()
second = Basket()

first.add("apple")
print(second.items)
```

```
['apple']
```

`second` sepetine hiçbir şey eklemedin ama içinde elma var. Sebebi: `items`
sınıfın kendisine ait, nesnelere değil. **Bütün nesneler aynı listeyi
paylaşıyor.**

Doğrusu listeyi `__init__` içinde kurmak:

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h5>PAYLAŞILAN — YANLIŞ</h5>
<pre><code>class Basket:
    items = []</code></pre>
    </div>
    <div class="ok">
      <h5>NESNEYE AİT — DOĞRU</h5>
<pre><code>class Basket:
    def __init__(self):
        self.items = []</code></pre>
    </div>
  </div>
  <figcaption>Soldaki liste bir kez, sınıf tanımlanırken oluşuyor. Sağdaki her nesne kurulduğunda yeniden oluşuyor.</figcaption>
</figure>

Sınıf değişkeni yanlış bir şey değil — ama **değişebilen** bir şey (liste,
sözlük) için kullanılmıyor. Sabitler için uygun:

```python
class Circle:
    PI = 3.14159        # herkes icin ayni, degismiyor
```

## 5. `__str__` içinde `print` yazmak

```python
class Student:
    def __str__(self):
        print(self.name)      # yanlis
```

```python
print(Student("Ada"))
```

```
Ada
None
```

İki satır çıktı: biri `__str__` içindeki `print`'ten, biri de `__str__`
hiçbir şey döndürmediği için `None`'dan.

`__str__` metin **döndürür**:

```python
    def __str__(self):
        return self.name
```

## 6. Nesneleri `==` ile karşılaştırmak

```python
a = Student("Ada", 90)
b = Student("Ada", 90)

print(a == b)
```

```
False
```

Aynı veriyi taşıyorlar ama Python varsayılan olarak "aynı nesne mi" diye
bakıyor, "aynı değerler mi" diye değil. İkisi ayrı nesne.

Değere göre karşılaştırma istiyorsan `__eq__` yazman gerekiyor:

```python
    def __eq__(self, other):
        return self.name == other.name and self.grade == other.grade
```

## 7. `super().__init__()` çağırmamak

```python
class Shape:
    def __init__(self, name):
        self.name = name


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius        # super cagrilmadi


print(Circle(5).name)
```

```
AttributeError: 'Circle' object has no attribute 'name'
```

Alt sınıf kendi `__init__` metodunu yazdığında üst sınıfınki **kendiliğinden
çalışmıyor.** Çağırman gerekiyor:

```python
    def __init__(self, radius):
        super().__init__("circle")
        self.radius = radius
```

Alt sınıf hiç `__init__` yazmazsa üst sınıfınki olduğu gibi kullanılıyor; o
zaman sorun çıkmıyor.

## 8. Sınıf içine durumsuz fonksiyon koymak

```python
class MathHelper:
    def add(self, a, b):
        return a + b


MathHelper().add(2, 3)
```

Bu sınıfın hatırladığı hiçbir şey yok. Her seferinde boş bir nesne kurup tek
metodunu çağırıyorsun. Bu bir sınıf değil, süslenmiş bir fonksiyon:

```python
def add(a, b):
    return a + b
```

Ölçüt: **`self.` ile yazılmış bir şey yoksa o sınıf olmamalı.**

## Özet

| Tuzak | Belirtisi |
|---|---|
| Metotta `self.` unutmak | `NameError` |
| `__init__`'te `self.` unutmak | Çok sonra `AttributeError` |
| `self` parametresini yazmamak | "takes 0 positional arguments" |
| Sınıf seviyesinde liste | Nesneler veriyi paylaşıyor |
| `__str__` içinde `print` | Fazladan `None` yazılıyor |
| `==` ile nesne karşılaştırmak | Aynı veride bile `False` |
| `super().__init__()` yok | Üst sınıfın verisi kurulmuyor |
| Durumsuz sınıf | Gereksiz karmaşıklık |
