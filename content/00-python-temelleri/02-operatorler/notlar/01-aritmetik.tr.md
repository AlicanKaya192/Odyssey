Operatörler, değerler üzerinde işlem yapan sembollerdir. En sık kullandıkların aritmetik olanlar.

## Tablo

| Operatör | Ne yapar | Örnek | Sonuç |
|---|---|---|---|
| `+` | toplama | `7 + 3` | `10` |
| `-` | çıkarma | `7 - 3` | `4` |
| `*` | çarpma | `7 * 3` | `21` |
| `/` | bölme | `7 / 3` | `2.333…` |
| `//` | tam bölme | `7 // 3` | `2` |
| `%` | kalan (mod) | `7 % 3` | `1` |
| `**` | üs alma | `7 ** 3` | `343` |

## İki bölme arasındaki fark

Bu ikisini karıştırmak sık yapılan bir hata:

```python
print(7 / 3)    # 2.3333333333333335  -> float
print(7 // 3)   # 2                   -> int
```

`/` **her zaman** ondalıklı sayı döndürür. Bölme tam bölünse bile:

```python
print(6 / 2)    # 3.0  (3 değil!)
print(6 // 2)   # 3
```

Bir sayının tam bölüm sonucunu istiyorsan `//` kullan. Örneğin 100 saniyenin kaç tam dakika ettiğini bulurken:

```python
seconds = 100
minutes = seconds // 60
print(minutes)   # 1
```

## Kalan operatörü ne işe yarar?

`%` bölme işleminden kalanı verir. İlk bakışta işe yaramaz görünür ama üç yerde çok kullanılır.

**Çift mi tek mi?** Bir sayının 2'ye bölümünden kalan 0 ise çifttir:

```python
number = 14
print(number % 2)    # 0  -> çift
```

**Artan kısmı bulmak:** 100 saniye 1 dakika ve 40 saniyedir:

```python
seconds = 100
print(seconds // 60)   # 1  -> dakika
print(seconds % 60)    # 40 -> artan saniye
```

**Belirli aralıklarla bir şey yapmak:** Bir sayacın her 5 adımda bir bir şey yapmasını istiyorsan `sayac % 5 == 0` kontrolü işini görür.

## Üs alma

`**` sayının kuvvetini alır:

```python
print(2 ** 10)    # 1024
print(9 ** 0.5)   # 3.0  -> karekök
```

Kesirli üs karekök verir. `9 ** 0.5` ile `math.sqrt(9)` aynı sonucu üretir; ikincisi için bir modül içe aktarmak gerekir.

## İşlem önceliği

Python matematikteki sırayı izler: önce `**`, sonra `*` `/` `//` `%`, en son `+` `-`.

```python
print(2 + 3 * 4)      # 14   (önce çarpma)
print((2 + 3) * 4)    # 20   (parantez öne alır)
```

Emin olmadığında parantez kullan. Parantez fazladan olsa bile kodu okuyan kişi ne demek istediğini anlar; bu, tasarruf edilecek bir şey değil.
