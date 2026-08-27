# Döngüler

Bir listedeki her elemana aynı işlemi yapmak istediğinde döngü kullanırsın. Döngü olmadan on elemanlı bir liste için on satır yazman gerekir; yüz elemanlı için yüz satır. Döngü bu tekrarı ortadan kaldırır.

## for döngüsü

Bir listenin elemanları üzerinde tek tek gezmek için `for` kullanılır:

```python
numbers = [1, 2, 3, 4, 5]

for number in numbers:
    print(number)
```

Burada `number` her turda listenin bir sonraki elemanını tutar. İsmini sen seçersin; `for item in numbers` de yazabilirdin.

Döngünün gövdesi **girintili** yazılır. Python'da girinti süslü parantezin yerini tutar, bu yüzden isteğe bağlı değil — girintiyi unutursan `IndentationError` alırsın.

## Toplam almak

Bir listedeki sayıları toplamak, döngünün en sık kullanıldığı örnektir. Önce bir **birikeç** değişkeni tanımlanır, sonra döngüde üzerine eklenir:

```python
numbers = [1, 2, 3, 4, 5]
total = 0

for number in numbers:
    total += number

print(total)   # 15
```

Sıralama önemli: `total = 0` satırı döngüden **önce** olmalı. Döngünün içine koyarsan her turda sıfırlanır ve sonuç yanlış çıkar.

> Bir önceki bölümde öğrendiğin `+=` burada işini görüyor. `total += number` ile `total = total + number` aynı şey, ama kısası niyeti daha net anlatıyor.

## range ile sayı üretmek

Elinde bir liste yoksa ve sadece belirli sayıda tekrar istiyorsan `range()` kullanılır:

```python
for i in range(5):
    print(i)
```

Bu `0, 1, 2, 3, 4` yazdırır — **beş sayı, sıfırdan başlayarak**. Üst sınır dahil değildir; bu Python'da her yerde geçerli bir kuraldır ve alışması zaman alır.

`range()` üç şekilde kullanılır:

```python
range(5)         # 0, 1, 2, 3, 4
range(2, 6)      # 2, 3, 4, 5
range(0, 10, 2)  # 0, 2, 4, 6, 8   -> ikişer atlayarak
```

## while döngüsü

`for` belirli sayıda tekrar için, `while` ise **bir koşul doğru olduğu sürece** tekrar için kullanılır:

```python
count = 3

while count > 0:
    print(count)
    count -= 1

print("Bitti")
```

Bu `3, 2, 1, Bitti` yazdırır.

`while` yazarken dikkat edilmesi gereken tek şey var: **koşulun bir gün yanlış olması gerekir.** Yukarıdaki örnekte `count -= 1` satırını unutursan `count` hep 3 kalır ve döngü hiç bitmez. Buna sonsuz döngü denir.

> Bu uygulamada sonsuz döngü yazarsan program 10 saniye sonra kodunu durdurup seni uyarır. Uygulama donmaz.

## Hangisini ne zaman?

Basit bir kural: **kaç kere döneceğini biliyorsan `for`, bilmiyorsan `while`.**

Bir listenin elemanları üzerinde geziyorsan sayı bellidir — `for`. Kullanıcı doğru cevabı verene kadar sormak istiyorsan kaç tur süreceği belli değildir — `while`.

Pratikte `for` çok daha sık kullanılır.

---

## Özet

- `for eleman in liste:` bir listenin elemanları üzerinde gezer.
- Döngü gövdesi girintili yazılır; girinti isteğe bağlı değildir.
- Toplam alırken birikeç değişkeni döngüden **önce** sıfırlanır.
- `range(5)` sıfırdan dörde kadar sayar — üst sınır dahil değildir.
- `while` koşul doğru olduğu sürece döner; koşulu değiştirmeyi unutursan sonsuza kadar döner.
