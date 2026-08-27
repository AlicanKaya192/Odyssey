# Operatörler

Bu bölümde sayılarla işlem yapmayı ve değerleri karşılaştırmayı öğreneceksin. Bunlar sonraki her bölümde kullanacağın temel araçlar.

## Aritmetik operatörler

| Operatör | Ne yapar | Örnek | Sonuç |
|---|---|---|---|
| `+` | toplama | `7 + 3` | `10` |
| `-` | çıkarma | `7 - 3` | `4` |
| `*` | çarpma | `7 * 3` | `21` |
| `/` | bölme | `7 / 3` | `2.333…` |
| `//` | tam bölme | `7 // 3` | `2` |
| `%` | kalan | `7 % 3` | `1` |
| `**` | üs alma | `7 ** 3` | `343` |

`/` her zaman ondalıklı sayı (`float`) döndürür — `6 / 2` bile `3.0` verir, `3` değil. Tam sayı istiyorsan `//` kullan.

## Kalan operatörü

`%` bölmeden kalanı verir ve göründüğünden çok daha işe yarar.

```python
number = 14
print(number % 2)    # 0  -> sayı çift
```

Bir sayının çift olup olmadığını anlamanın standart yolu budur: `number % 2 == 0` ise çifttir.

Zaman hesaplarında da sık kullanılır:

```python
seconds = 100
print(seconds // 60)   # 1  -> tam dakika
print(seconds % 60)    # 40 -> artan saniye
```

## Kısaltılmış atama

Bir değişkenin üzerine ekleme yapmanın kısa yolu var:

```python
total = 0
total = total + 5    # uzun hâli
total += 5           # kısa hâli, aynı şey
```

Bütün aritmetik operatörlerin kısaltılmışı vardır: `-=`, `*=`, `/=`, `//=`, `%=`, `**=`.

> Bu kısaltma özellikle döngülerde işine yarayacak. Bir listedeki sayıları toplarken `total += number` yazmak, `total = total + number` yazmaktan hem kısa hem de niyeti daha açık.

## Karşılaştırma operatörleri

Bunlar bir soru sorar ve `True` ya da `False` döndürür:

```python
print(5 > 3)     # True
print(5 == 3)    # False
print(5 != 3)    # True
```

| Operatör | Sorusu |
|---|---|
| `==` | eşit mi? |
| `!=` | farklı mı? |
| `>` `<` | büyük mü, küçük mü? |
| `>=` `<=` | büyük/küçük veya eşit mi? |

## En sık yapılan hata

`=` ile `==` farklı şeyler ve bu ikisini karıştırmak yeni başlayanların en sık takıldığı yer:

```python
age = 18      # ATAMA: age değişkenine 18 koy
age == 18     # KARŞILAŞTIRMA: age 18'e eşit mi?
```

Biri değer yerleştirir, diğeri soru sorar.

## Mantıksal operatörler

Birden fazla koşulu birleştirmek için `and`, `or` ve `not` kullanılır:

```python
age = 25
has_ticket = True

print(age >= 18 and has_ticket)   # True  -> ikisi de doğru olmalı
print(age >= 65 or has_ticket)    # True  -> biri yeterli
print(not has_ticket)             # False -> tersini alır
```

Bunları asıl bir sonraki bölümde, `if` ile birlikte kullanacaksın.

## İşlem önceliği

Python matematikteki sırayı izler: önce `**`, sonra `*` `/` `//` `%`, en son `+` `-`.

```python
print(2 + 3 * 4)      # 14   (önce çarpma)
print((2 + 3) * 4)    # 20   (parantez öne alır)
```

Emin olmadığında parantez kullan. Fazladan parantez kodu okuyan kişiye ne demek istediğini anlatır.

---

## Özet

- `/` ondalıklı, `//` tam bölme yapar; `%` kalanı verir.
- `%` ile çift/tek kontrolü yapılır: `number % 2 == 0`.
- `total += 5`, `total = total + 5` demektir.
- `=` atar, `==` karşılaştırır — karıştırma.
- `and` ikisini birden, `or` birini, `not` tersini ister.
