# Nesne Tabanlı Programlama

Bir öğrencinin adını, notunu ve şehrini tutmak istiyorsun. Bugünkü araçlarınla
şöyle yapardın:

```python
student = {"name": "Ada", "grade": 90, "city": "London"}


def is_passing(record):
    return record["grade"] >= 50


print(is_passing(student))
```

Çalışıyor. Ama üç sorun var:

- `student` sözlüğü ile `is_passing` fonksiyonu birbirine **bağlı değil.**
  Yanlışlıkla başka bir sözlük verirsen `KeyError` alıyorsun.
- Anahtar adını yanlış yazarsan (`"grades"`) hata çalışma anında çıkıyor.
- Yüz tane öğrenci olduğunda her birinin aynı anahtarları taşıdığından emin
  olmanın bir yolu yok.

**Sınıf** bu üç sorunu birden çözüyor: veriyi ve o veriyle çalışan
fonksiyonları tek bir yerde topluyor.

## İlk sınıfın

```python
class Student:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade

    def is_passing(self):
        return self.grade >= 50


ada = Student("Ada", 90)

print(ada.name)
print(ada.is_passing())
```

```
Ada
True
```

<figure class="fig anat">
  <div class="sig">class <u class="m1">Student</u>:
    def <u class="m2">__init__</u>(<u class="m3">self</u>, name, grade):
        <u class="m4">self.name</u> = name</div>
  <ul class="legend">
    <li class="m1"><b>Sınıf adı</b> — büyük harfle başlar. Bir kalıp, henüz bir nesne değil.</li>
    <li class="m2"><b>Kurucu</b> — <code>Student(...)</code> yazdığın anda çalışır. Adı sabittir.</li>
    <li class="m3"><b>self</b> — kurulan nesnenin kendisi. İlk parametre her zaman budur.</li>
    <li class="m4"><b>Nesnenin özelliği</b> — <code>self.</code> ile yazılan şey nesnede kalıcı olur.</li>
  </ul>
</figure>

## Sınıf ile nesne farkı

`Student` bir **kalıp**. Ondan istediğin kadar nesne üretebiliyorsun ve her
biri kendi verisini taşıyor:

```python
ada = Student("Ada", 90)
brian = Student("Brian", 40)

print(ada.grade)
print(brian.grade)
```

```
90
40
```

<figure class="fig">
  <div class="flow">
    <span class="node acc"><b>Student</b><br>kalıp</span>
    <span class="arrow">→</span>
    <span class="node"><b>ada</b><br>name: Ada<br>grade: 90</span>
    <span class="node"><b>brian</b><br>name: Brian<br>grade: 40</span>
  </div>
  <figcaption>Tek kalıp, iki nesne. İkisi de aynı metotları taşıyor ama verileri ayrı; birini değiştirmek diğerini etkilemiyor.</figcaption>
</figure>

Kalıba **sınıf**, ondan üretilen her şeye **nesne** deniyor.

## `self` gerçekte ne?

En çok kafa karıştıran yer burası, ama aslında basit.

Bir metodu çağırdığında Python nesneyi **ilk argüman olarak** metoda
gönderiyor. Yani şu ikisi aynı şey:

```python
ada.is_passing()
Student.is_passing(ada)
```

`self` o gönderilen nesnenin metot içindeki adı. Bu yüzden:

- Her metodun ilk parametresi `self` olmak zorunda.
- Nesnenin verisine erişmek için `self.grade` yazıyorsun, düz `grade` değil.

Metot içinde `self.` yazmayı unutmak en sık yapılan hata:

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h5>self YOK</h5>
<pre><code>def is_passing(self):
    return grade &gt;= 50</code></pre>
    </div>
    <div class="ok">
      <h5>self VAR</h5>
<pre><code>def is_passing(self):
    return self.grade &gt;= 50</code></pre>
    </div>
  </div>
  <figcaption>Soldaki <code>NameError</code> veriyor: <code>grade</code> diye serbest bir değişken yok, o değer nesnenin içinde duruyor.</figcaption>
</figure>

## Nesnenin durumu değişebilir

Metotlar yalnızca hesap yapmıyor, nesnenin verisini de değiştirebiliyor:

```python
class Counter:
    def __init__(self):
        self.count = 0

    def increase(self):
        self.count = self.count + 1
        return self.count


clicks = Counter()
clicks.increase()
clicks.increase()

print(clicks.count)
```

```
2
```

Sözlükle de yapılabilirdi ama fark şu: `Counter` nesnesi kendi sayacını
kendisi yönetiyor. Dışarıdan yanlış bir anahtar yazma ihtimali yok.

## Nesneyi yazdırmak: `__str__`

Bir nesneyi doğrudan yazdırmayı denersen:

```python
ada = Student("Ada", 90)
print(ada)
```

```
<__main__.Student object at 0x000001F3A2B4C110>
```

Okunmuyor. `__str__` metodu bunu düzeltiyor:

```python
class Student:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade

    def __str__(self):
        return self.name + ": " + str(self.grade)


print(Student("Ada", 90))
```

```
Ada: 90
```

`__str__` bir metin **döndürüyor**, yazdırmıyor. İçinde `print` yazmak sık
yapılan bir hata.

## Kalıtım

İki sınıfın ortak yanı varsa, ortak kısmı bir kez yazıp diğerlerine
devredebiliyorsun:

```python
class Shape:
    def __init__(self, name):
        self.name = name

    def describe(self):
        return self.name + " has area " + str(self.area())


class Rectangle(Shape):
    def __init__(self, width, height):
        super().__init__("rectangle")
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height


class Square(Rectangle):
    def __init__(self, side):
        super().__init__(side, side)
        self.name = "square"


print(Rectangle(3, 4).describe())
print(Square(5).describe())
```

```
rectangle has area 12
square has area 25
```

İki parça var:

- `class Rectangle(Shape):` — "Rectangle bir Shape'tir" demek. `Shape`'in
  bütün metotları `Rectangle`'da da var.
- `super().__init__(...)` — üst sınıfın kurucusunu çağırıyor. Yazmazsan
  `self.name` hiç kurulmuyor.

Dikkat: `Shape` sınıfının kendisinde `area` metodu yok, ama `describe` onu
çağırıyor. Bu kasıtlı — her şeklin alanı farklı hesaplanıyor ve bunu alt
sınıflar dolduruyor.

## Ne zaman sınıf yazılır?

Sınıf her sorunun cevabı değil. İşe yaradığı yerler:

- **Veri ve davranış birlikte gidiyorsa.** Bir öğrencinin notu ve "geçti mi"
  sorusu aynı yere ait.
- **Aynı yapıdan çok sayıda üretilecekse.** Yüz öğrenci, her biri aynı
  kalıptan.
- **Nesnenin bir durumu varsa ve o durum zamanla değişiyorsa.** Sayaç,
  sepet, bağlantı.

Gereksiz olduğu yerler:

- **Tek bir değer taşıyorsa.** Bunun için değişken var.
- **Sadece hesap yapıyorsa.** Durumu olmayan bir işlem fonksiyondur, sınıf
  değil. `def average(values):` bir sınıfın içine konmamalı.
- **Yalnızca veri tutuyorsa ve davranışı yoksa.** Sözlük yeterli olabilir.

Ölçüt: **nesnenin hatırlaması gereken bir şey var mı?** Varsa sınıf, yoksa
fonksiyon.

## Özet

- Sınıf bir kalıptır; ondan üretilen her şey bir nesnedir.
- `__init__` nesne kurulurken çalışır ve başlangıç verisini yerleştirir.
- Her metodun ilk parametresi `self`, yani nesnenin kendisidir.
- Nesnenin verisine `self.ad` ile ulaşılır; `self.` unutmak `NameError`
  verir.
- Metotlar nesnenin verisini okuyabilir ve **değiştirebilir**.
- `__str__` nesnenin yazdırıldığında nasıl görüneceğini belirler; metin
  döndürür, yazdırmaz.
- `class Alt(Ust):` kalıtımdır; `super().__init__(...)` üst sınıfın
  kurucusunu çağırır.
- Durumu olmayan bir işlem için sınıf değil fonksiyon yazılır.
