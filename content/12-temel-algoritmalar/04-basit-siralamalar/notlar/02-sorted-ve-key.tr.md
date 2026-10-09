## `sorted` mı `list.sort` mu?

| | `sorted(items)` | `items.sort()` |
|---|---|---|
| Ne döndürür | yeni bir liste | `None` |
| Asıl liste | değişmez | yerinde sıralanır |
| Ne alır | her yinelenebilir (liste, demet, metin, küme…) | yalnızca liste |

Sık hata: `items = items.sort()` yazmak. `sort` `None` döndürdüğü için
`items` artık `None` olur.

## `key=` ile anahtar

```python
people = [("Ada", 36), ("Bora", 25), ("Cem", 36)]

sorted(people, key=lambda p: p[1])          # yaşa göre
# [('Bora', 25), ('Ada', 36), ('Cem', 36)]

from operator import itemgetter
sorted(people, key=itemgetter(1))            # aynısı, lambda'sız
```

`key` fonksiyonu her eleman için **bir kez** çağrılır; karşılaştırmalar
anahtarlar üstünden yapılır.

## Çok ölçütlü sıralama

Demet anahtar soldan sağa karşılaştırılır:

```python
sorted(people, key=lambda p: (p[1], p[0]))   # önce yaş, eşitse ad
# [('Bora', 25), ('Ada', 36), ('Cem', 36)]
```

**Biri artan biri azalan** isteniyorsa sayısal ölçütün eksisini al:

```python
sorted(people, key=lambda p: (-p[1], p[0]))  # yaş büyükten küçüğe, ad A-Z
# [('Ada', 36), ('Cem', 36), ('Bora', 25)]
```

Ölçüt metinse eksi alınamaz; o zaman kararlılıktan yararlanıp **iki
geçiş** yapılır: önce ikinci ölçüte, sonra birinci ölçüte göre sırala.

```python
step1 = sorted(people, key=lambda p: p[0], reverse=True)   # ad Z-A
step2 = sorted(step1, key=lambda p: p[1])                  # yaş artan
# [('Bora', 25), ('Cem', 36), ('Ada', 36)]
```

İkinci sıralama kararlı olduğu için aynı yaştakiler birinci geçişin sırasını
(ad Z-A) korur.

## Büyük-küçük harf

Metinler karakter koduna göre karşılaştırılır: bütün büyük harfler
küçüklerden önce gelir. Harf duyarsız sıralama için `key=str.lower`.
(Türkçe harflerin doğru sırası için `locale` ya da özel bir anahtar gerekir;
`"ç"`, kodu `"z"`'den büyük olduğu için en sona düşer.)
