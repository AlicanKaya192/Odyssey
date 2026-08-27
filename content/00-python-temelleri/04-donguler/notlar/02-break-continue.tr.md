Bazen döngünün akışına karışman gerekir: aradığını bulunca durmak, ya da bazı elemanları atlamak istersin. Bunun için iki anahtar kelime var.

## break — döngüyü bitirir

Aradığını bulduğunda geri kalanına bakmanın anlamı yoktur:

```python
numbers = [4, 8, 15, 16, 23, 42]

for number in numbers:
    if number > 10:
        print("İlk büyük sayı:", number)
        break
```

Çıktı: `İlk büyük sayı: 15`. Döngü 15'i bulunca durur; 16, 23 ve 42'ye hiç bakmaz.

`break` olmasaydı döngü sonuna kadar devam eder ve dört satır yazdırırdı.

## continue — bu turu atlar

Bazı elemanları işlemek istemiyorsan `continue` o turu kesip bir sonrakine geçer:

```python
numbers = [1, 2, 3, 4, 5, 6]

for number in numbers:
    if number % 2 != 0:
        continue
    print(number)
```

Çıktı: `2, 4, 6`. Tek sayılara denk gelince `continue` çalışır, `print` satırına hiç ulaşılmaz.

Aynı işi `if number % 2 == 0: print(number)` ile de yapabilirdin. `continue` özellikle atlanacak durum çok ve gövde uzunsa okunaklı kalmayı sağlar.

## İkisi arasındaki fark

| | Ne yapar |
|---|---|
| `break` | Döngüden tamamen çıkar |
| `continue` | Sadece bu turu atlar, döngü devam eder |

## Döngüye bağlı else

Python'da az bilinen bir yapı var: döngüye `else` eklenebilir.

```python
numbers = [4, 8, 15]

for number in numbers:
    if number > 100:
        print("Büyük sayı bulundu")
        break
else:
    print("Hiç büyük sayı yok")
```

Buradaki `else`, döngü **`break` ile kesilmeden** bittiğinde çalışır. Yukarıdaki örnekte 100'den büyük sayı olmadığı için `break` hiç çalışmaz ve `else` devreye girer.

Bu yapı "aradığımı bulamadım" durumunu ayrı bir bayrak değişkeni tutmadan yazmanı sağlar. Nadiren kullanılır ama karşına çıktığında ne olduğunu bilmen iyi olur.

## Sonsuz döngüden çıkmak

`break`, `while True` ile birlikte sık kullanılır:

```python
count = 0

while True:
    count += 1
    if count >= 3:
        break

print(count)   # 3
```

`while True` koşulu hep doğru olduğu için tek çıkış yolu `break`'tir. Bu yapıyı yazarken `break` satırını unutma — yoksa program sonsuza kadar döner.
