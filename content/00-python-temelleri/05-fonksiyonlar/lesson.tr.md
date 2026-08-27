# Fonksiyonlar

Şimdiye kadar yazdığın her şey yukarıdan aşağı bir kez çalıştı. Aynı işi ikinci
kez yapman gerektiğinde tek çaren kodu kopyalamaktı. Fonksiyonlar tam olarak bu
sorunu çözüyor: bir işi **bir kez** tarif ediyorsun, sonra istediğin kadar
çağırıyorsun.

## Neden gerek var?

İki sayıyı toplamak istediğini düşün:

```python
a = 5
b = 3
print(a + b)
```

Şimdi başka iki sayıyı daha toplaman gerekti. Aynı satırları tekrar yazıyorsun.
Sonra bir tane daha. Üç kopya oldu bile — ve toplama biçimini değiştirmen
gerekirse üç yeri birden düzeltmen gerekecek.

Fonksiyon bu tekrarı ortadan kaldırıyor. Bunun yanında iki şey daha getiriyor:
koda **isim** veriyor (`calculate_total` ne yaptığını anlatır, üç satır kod
anlatmaz) ve programı **parçalara** ayırıyor.

## def ile tanımlamak

```python
def add(a, b):
    return a + b
```

Satır satır bakalım:

- `def` — "yeni bir fonksiyon tanımlıyorum" demek.
- `add` — fonksiyonun adı. Bu adla çağıracaksın.
- `(a, b)` — **parametreler**. Fonksiyonun dışarıdan aldığı değerler.
- `:` — başlıktan sonra iki nokta. Koşullarda ve döngülerde de böyleydi.
- Girintili satırlar — fonksiyonun **gövdesi**. Sadece burası fonksiyona ait.

Tanımlamak fonksiyonu **çalıştırmaz**. Sadece "böyle bir şey var" der. Yukarıdaki
kodu çalıştırırsan ekranda hiçbir şey görmezsin.

## Çağırmak

Fonksiyonu çalıştırmak için adını yazıp parantez açarsın:

```python
def add(a, b):
    return a + b

result = add(5, 3)
print(result)     # 8
```

`add(5, 3)` yazdığın anda `a` yerine 5, `b` yerine 3 konuyor ve gövde çalışıyor.
Parantez içine yazdığın bu değerlere **argüman** deniyor.

Bir kez tanımlayıp defalarca çağırabilirsin:

```python
print(add(5, 3))      # 8
print(add(10, 20))    # 30
print(add(-4, 4))     # 0
```

## return — değeri geri vermek

`return`, fonksiyonun sonucunu dışarı veren şey:

```python
def double(number):
    return number * 2

x = double(21)
print(x)     # 42
```

`return` çalıştığı anda fonksiyon **biter**. Altındaki satırlar çalışmaz:

```python
def test():
    return "birinci"
    return "ikinci"     # buraya hiç gelinmez

print(test())     # birinci
```

`return` yazmazsan fonksiyon `None` döndürür. Bu bir hata değil, Python'un
"geriye verecek bir şey yok" deme biçimi:

```python
def greet(name):
    print("Hello,", name)

x = greet("Ada")
print(x)     # None
```

## return ile print aynı şey değil

Yeni başlayanların en sık takıldığı yer burası. İkisi bambaşka işler yapıyor:

- **`print`** metni **ekrana yazar.** Program dışına bir şey vermez.
- **`return`** değeri **koda geri verir.** Ekranda hiçbir şey görünmez.

```python
def add_print(a, b):
    print(a + b)

def add_return(a, b):
    return a + b

x = add_print(2, 3)      # ekrana 5 yazar
print(x)                 # None  <- x'in içinde bir şey yok

y = add_return(2, 3)     # ekrana hiçbir şey yazmaz
print(y)                 # 5     <- ama y'nin içinde sonuç var
```

Ölçüt basit: sonucu **başka bir hesapta kullanacaksan** `return` gerekir.
`add_print(2, 3) * 10` yazamazsın, çünkü elinde `None` var.

## Varsayılan değerler

Bir parametreye önceden değer verebilirsin. O parametre artık isteğe bağlı olur:

```python
def greet(name, greeting="Hello"):
    return greeting + ", " + name

print(greet("Ada"))            # Hello, Ada
print(greet("Ada", "Hi"))      # Hi, Ada
```

Varsayılan değeri olan parametreler, olmayanlardan **sonra** yazılmak zorunda.
`def greet(greeting="Hello", name)` yazarsan Python hata verir — hangi değerin
nereye gittiğini anlayamaz.

## İsimlendirme

Fonksiyon bir **iş yapar**, o yüzden adı çoğunlukla bir fiille başlar:
`calculate_total`, `send_email`, `get_user`. Kelimeler alt çizgiyle ayrılır.

Adı iyi seçersen fonksiyonun içine bakmadan ne yaptığını anlarsın. `hesapla`
değil `calculate_average`; `f1` hiç değil.

---

## Özet

- Fonksiyon, bir işi bir kez tarif edip defalarca çağırmanı sağlar.
- `def ad(parametreler):` ile tanımlanır, gövdesi girintilidir.
- Tanımlamak çalıştırmak değildir; `ad(...)` yazınca çalışır.
- `return` sonucu koda geri verir ve fonksiyonu bitirir.
- `return` yoksa fonksiyon `None` döndürür.
- `print` ekrana yazar, `return` değer verir — ikisi farklı şeydir.
- Varsayılan değerli parametreler sona yazılır ve isteğe bağlı olur.
