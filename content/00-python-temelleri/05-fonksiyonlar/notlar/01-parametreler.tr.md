Fonksiyona değer geçirmenin birkaç yolu var. Hepsi aynı fonksiyonla çalışıyor;
fark, çağırırken nasıl yazdığında.

## Konumsal argümanlar

En sık kullanılan biçim. Değerler **sırayla** yerleşir:

```python
def describe(name, age):
    return name + " is " + str(age)

print(describe("Ada", 36))     # Ada is 36
```

Sıra önemli. `describe(36, "Ada")` yazarsan Python itiraz etmez ama sonuç saçma
olur — hatta bu örnekte `TypeError` alırsın, çünkü sayıyı metinle birleştirmeye
çalışırsın.

## İsimli argümanlar

Parametre adını yazarak sırayı önemsiz hâle getirebilirsin:

```python
print(describe(age=36, name="Ada"))     # Ada is 36
```

Bu, parametre sayısı arttığında okumayı ciddi biçimde kolaylaştırır. Şu ikisini
karşılaştır:

```python
create_user("Ada", "Lovelace", True, False, 30)
create_user(name="Ada", surname="Lovelace", active=True, admin=False, age=30)
```

İkincisinde `True` ile `False`'un ne anlama geldiğini fonksiyona bakmadan
anlıyorsun.

İkisini karıştırabilirsin, ama **konumsal olanlar önce** gelmek zorunda:

```python
describe("Ada", age=36)      # calisir
describe(name="Ada", 36)     # SyntaxError
```

## Varsayılan değerler

```python
def power(base, exponent=2):
    return base ** exponent

print(power(5))        # 25   -> exponent 2 sayilir
print(power(5, 3))     # 125
```

Varsayılan değerli parametreler listenin **sonunda** durur. Sebebi basit: Python
konumsal değerleri baştan yerleştiriyor, boşluk ortada olamaz.

```python
def wrong(a=1, b):     # SyntaxError
    return a + b
```

## Kaç argüman verdiğine dikkat

Eksik verirsen:

```python
def add(a, b):
    return a + b

add(5)
# TypeError: add() missing 1 required positional argument: 'b'
```

Fazla verirsen:

```python
add(1, 2, 3)
# TypeError: add() takes 2 positional arguments but 3 were given
```

Bu iki mesaj çok net konuşuyor: kaç tane beklediğini ve kaç tane verdiğini
söylüyor. Hata metnini okumak, tahmin etmekten hızlı.

## Küçük bir tuzak

Varsayılan değer olarak **liste** verme:

```python
def add_item(item, basket=[]):     # boyle yapma
    basket.append(item)
    return basket
```

Varsayılan değer fonksiyon tanımlanırken bir kez oluşturuluyor ve her çağrıda
**aynı liste** kullanılıyor. Bu yüzden ikinci çağrıda eski eleman hâlâ orada
duruyor. Doğrusu:

```python
def add_item(item, basket=None):
    if basket is None:
        basket = []
    basket.append(item)
    return basket
```

Şimdilik aklında bir yerde dursun; listelerle çalışmaya başlayınca bu tuzağa
düşenler çok oluyor.
