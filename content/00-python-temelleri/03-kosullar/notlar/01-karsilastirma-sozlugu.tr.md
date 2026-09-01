# Karşılaştırma Sözlüğü

Bir koşulun içine ne yazabileceğinin listesi. Takıldığında buraya bak.

## Karşılaştırma operatörleri

| Operatör | Anlamı | Örnek | Sonuç |
|---|---|---|---|
| `==` | Eşit mi | `5 == 5` | `True` |
| `!=` | Eşit değil mi | `5 != 3` | `True` |
| `>` | Büyük mü | `5 > 3` | `True` |
| `<` | Küçük mü | `5 < 3` | `False` |
| `>=` | Büyük veya eşit mi | `5 >= 5` | `True` |
| `<=` | Küçük veya eşit mi | `3 <= 5` | `True` |

Hepsi geriye `True` ya da `False` veriyor. Yani bir karşılaştırma yazdığında
aslında bir değer üretiyorsun:

```python
result = 10 > 3
print(result)
```

```
True
```

## Zincirleme karşılaştırma

Python'da bir değeri iki sınır arasında test etmenin kısa yolu var:

```python
age = 25

if 18 <= age < 65:
    print("working age")
```

```
working age
```

Bu, `age >= 18 and age < 65` ile aynı şey ama daha okunur. Çoğu dilde bu
yazım yok; Python'da var ve kullanılıyor.

## Mantık operatörleri

| Operatör | Ne zaman `True` |
|---|---|
| `and` | **İkisi de** doğruysa |
| `or` | **En az biri** doğruysa |
| `not` | Tersini alır |

```python
temperature = 30
raining = False

if temperature > 25 and not raining:
    print("go outside")
```

```
go outside
```

### Öncelik sırası

`not` önce, sonra `and`, en son `or`. Yani şu ikisi aynı şey:

```python
a or b and c
a or (b and c)
```

Kafan karışıyorsa parantez koy. Parantez kod okuyanın işini kolaylaştırır,
yavaşlatmaz.

## `in` — içinde var mı

Bir şeyin bir kabın içinde olup olmadığını sorar:

```python
name = "Ada"
team = ["Ada", "Alan", "Grace"]

if name in team:
    print("found")
```

Metinde de çalışıyor, orada "alt metin geçiyor mu" demek:

```python
if "@" in email:
    print("looks like an address")
```

Tersi `not in`:

```python
if name not in team:
    print("missing")
```

## `==` ile `is` farkı

İkisi de "aynı mı" diye soruyor ama farklı şeyler soruyor:

- `==` → **değerleri** aynı mı?
- `is` → **aynı nesne** mi?

```python
a = [1, 2]
b = [1, 2]

print(a == b)
print(a is b)
```

```
True
False
```

İki liste aynı değerleri taşıyor ama bellekte iki ayrı liste. Bu yüzden
`==` doğru, `is` yanlış.

**Kural:** Değer karşılaştırırken `==` kullan. `is` yalnızca `None`, `True`
ve `False` ile kullanılır:

```python
if value is None:
    print("no value")
```

## Kısa devre

`and` ve `or` gereksiz yere çalışmıyor. Soldaki sonucu belirlediyse sağdaki
hiç değerlendirilmiyor:

```python
# ikinci kosul hic calismaz, cunku ilki zaten False
if False and expensive_check():
    ...
```

Bunun pratik bir faydası var — önce güvenlik kontrolü, sonra kullanım:

```python
if len(values) > 0 and values[0] == "start":
    print("ok")
```

Liste boşsa `values[0]` hata verirdi. Ama soldaki koşul `False` olduğu için
sağdakine hiç sıra gelmiyor.

## Karşılaştırmayı `if` olmadan kullanmak

Bir koşulun sonucu değer olduğu için doğrudan atanabiliyor:

```python
is_adult = age >= 18
print(is_adult)
```

Bu, şunu yazmaktan daha kısa ve daha okunur:

```python
if age >= 18:
    is_adult = True
else:
    is_adult = False
```

İkisi aynı işi yapıyor. Birincisi tercih edilir.
