`range()`, sayı üretmek için kullanılan bir fonksiyondur. Elinde bir liste olmadığında ve sadece belirli sayıda tekrar istediğinde işini görür.

## Üç kullanımı

```python
range(5)          # 0, 1, 2, 3, 4
range(2, 6)       # 2, 3, 4, 5
range(0, 10, 2)   # 0, 2, 4, 6, 8
```

| Yazılışı | Anlamı |
|---|---|
| `range(bitis)` | 0'dan başlar, `bitis`'e **kadar** |
| `range(baslangic, bitis)` | `baslangic`'tan `bitis`'e kadar |
| `range(baslangic, bitis, adim)` | belirtilen adımlarla |

## Üst sınır neden dahil değil?

`range(5)` beş sayı üretir ama 5'i içermez. Bu ilk başta ters gelir. Sebebi şu: Python'da sayma sıfırdan başlar, bu yüzden "beş tane" demek "0'dan 4'e kadar" demektir.

Bunun pratik bir faydası var — bir listenin uzunluğuyla doğrudan çalışabiliyorsun:

```python
names = ["Ada", "Alan", "Grace"]

for i in range(len(names)):
    print(i, names[i])
```

`len(names)` üç verir, `range(3)` de 0, 1, 2 üretir — listenin geçerli sıra numaraları tam olarak bunlar.

## Geriye saymak

Adım negatif olursa geriye sayar:

```python
for i in range(3, 0, -1):
    print(i)      # 3, 2, 1
```

## range bir liste değildir

`range(5)` yazıp yazdırmayı denersen liste göremezsin:

```python
print(range(5))         # range(0, 5)
print(list(range(5)))   # [0, 1, 2, 3, 4]
```

`range` sayıları önceden üretip bellekte tutmaz; istendikçe üretir. Bu yüzden `range(1000000)` bile neredeyse hiç bellek harcamaz. Listeye çevirmek istersen `list()` kullanman gerekir.

## Sıra numarasıyla birlikte gezmek

Hem elemanı hem sırasını istiyorsan `range(len(...))` yerine `enumerate()` daha temizdir:

```python
names = ["Ada", "Alan", "Grace"]

for i, name in enumerate(names):
    print(i, name)
```

İkisi de aynı sonucu verir ama `enumerate` niyeti daha açık anlatır ve hata yapma ihtimalin daha düşüktür.
