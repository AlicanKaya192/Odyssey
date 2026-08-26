# Operatörler ve Döngüler

Bu bölümde sayılarla işlem yapmayı, değerleri karşılaştırmayı ve bir listenin elemanları üzerinde tek tek gezmeyi öğreneceksin. Bunlar sonraki her bölümde kullanacağın temel araçlar.

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

`/` her zaman ondalıklı sayı (`float`) döndürür, `7 / 1` bile `7.0` verir. Tam sayı istiyorsan `//` kullan.

`%` operatörü özellikle bir sayının çift mi tek mi olduğunu anlamak için işe yarar: `number % 2 == 0` ise sayı çifttir.

## Karşılaştırma operatörleri

Bunlar `True` veya `False` döndürür:

```python
print(5 > 3)    # True
print(5 == 3)   # False
print(5 != 3)   # True
```

Dikkat: `=` atama yapar, `==` karşılaştırır. Bu ikisini karıştırmak en sık yapılan hatalardan biridir.

## for döngüsü

Bir listenin elemanları üzerinde tek tek gezmek için `for` kullanırız:

```python
numbers = [1, 2, 3, 4, 5]

for number in numbers:
    print(number)
```

Döngünün gövdesi **girintili** yazılır. Python'da girinti süslü parantezin yerini tutar, bu yüzden isteğe bağlı değildir.

## Döngüyle toplam almak

Bir listedeki sayıları toplamak istersek, önce boş bir birikeç değişkeni tanımlar, sonra döngüde üzerine ekleriz:

```python
numbers = [1, 2, 3, 4, 5]
total = 0

for number in numbers:
    total = total + number

print(total)   # 15
```

`total = total + number` yerine kısaca `total += number` da yazabilirsin, ikisi aynı şeydir.

Python'da hazır bir `sum()` fonksiyonu da var ve aynı işi tek satırda yapar. Ama döngünün nasıl çalıştığını anlamadan `sum()` kullanmak, sonraki bölümlerde işini zorlaştırır. Bu yüzden alıştırmada `sum()` kullanmanı istemiyorum.

---

## Özet

- `/` ondalıklı, `//` tam bölme yapar; `%` kalanı verir.
- `=` atar, `==` karşılaştırır.
- `for` ile liste elemanları üzerinde gezilir, gövde girintili yazılır.
- Toplam alırken önce birikeç değişkeni sıfırlanır, sonra döngüde üzerine eklenir.
