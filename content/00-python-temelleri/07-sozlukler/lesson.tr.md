# Sözlükler ve Kümeler

Listede her elemana **sıra numarasıyla** ulaşıyordun. Peki elindeki şey bir sıra
değil de bir eşleşmeyse? Ülke ve başkenti, ürün ve fiyatı, kullanıcı adı ve
puanı gibi.

Sözlük tam bunun için: değerleri numarayla değil, **kendi seçtiğin bir adla**
saklıyorsun.

## Sözlük oluşturmak

Süslü parantez açıyorsun, her çifti `anahtar: değer` biçiminde yazıyorsun:

```python
capitals = {"Turkey": "Ankara", "France": "Paris", "Japan": "Tokyo"}
```

Uzun sözlükleri alt alta yazmak okumayı kolaylaştırır:

```python
prices = {
    "apple": 12,
    "banana": 8,
    "cherry": 45,
}
```

Sondaki virgül fazlalık değil, kasıtlı: yeni satır eklerken önceki satıra
dokunmuyorsun.

## Anahtar ve değer

Her çiftin sol tarafına **anahtar** (key), sağ tarafına **değer** (value)
deniyor. Anahtar genelde metin olur ama sayı da olabilir. Değer her şey
olabilir — sayı, metin, hatta bir liste:

```python
student = {
    "name": "Ada",
    "age": 20,
    "grades": [90, 85, 78],
}
```

## Değere ulaşmak

Köşeli parantez kullanıyorsun, ama içine sıra numarası değil **anahtar**
yazıyorsun:

```python
capitals = {"Turkey": "Ankara", "France": "Paris"}

print(capitals["Turkey"])     # Ankara
```

Olmayan bir anahtar istersen hata alırsın:

```python
print(capitals["Spain"])
# KeyError: 'Spain'
```

## Anahtar var mı?

`in` listede olduğu gibi burada da çalışıyor — ama **anahtarlara** bakıyor,
değerlere değil:

```python
print("Turkey" in capitals)     # True
print("Ankara" in capitals)     # False   <- bu bir deger, anahtar degil
```

Bu yüzden güvenli okuma şöyle yapılır:

```python
if "Spain" in capitals:
    print(capitals["Spain"])
else:
    print("bulunamadi")
```

## Eklemek ve değiştirmek

İkisi de aynı satırla yapılıyor. Anahtar yoksa **eklenir**, varsa **değeri
değişir**:

```python
capitals = {"Turkey": "Ankara"}

capitals["Japan"] = "Tokyo"       # yeni cift eklendi
capitals["Turkey"] = "ANKARA"     # var olanin degeri degisti

print(capitals)     # {'Turkey': 'ANKARA', 'Japan': 'Tokyo'}
```

Listedeki `append` gibi ayrı bir metot yok; atama yeterli.

## Silmek

```python
del capitals["Japan"]
```

## Uzunluk ve döngü

`len()` **çift sayısını** verir:

```python
print(len(capitals))     # 1
```

Bir sözlük üzerinde döndüğünde eline **anahtarlar** geçer:

```python
prices = {"apple": 12, "banana": 8}

for key in prices:
    print(key, prices[key])

# apple 12
# banana 8
```

Hem anahtarı hem değeri daha temiz almanın yolu `items()`:

```python
for key, value in prices.items():
    print(key, value)
```

## Kümeler

Küme (set) de süslü parantezle yazılır ama içinde çift değil, **tek tek
değerler** vardır:

```python
tags = {"python", "data", "python", "web"}

print(tags)          # {'python', 'data', 'web'}
print(len(tags))     # 3
```

İki özelliği var: **tekrar tutmaz** ve **sırasızdır**. Yukarıda "python" iki
kez yazılmasına rağmen bir kez duruyor. Sırasız olduğu için `tags[0]` diye bir
şey yok — sıra numarasıyla erişemezsin.

En sık kullanım şekli, bir listedeki tekrarları atmak:

```python
numbers = [1, 2, 2, 3, 3, 3]
unique = set(numbers)

print(unique)     # {1, 2, 3}
```

## Boş olanın tuzağı

Burada dikkat edilecek bir şey var:

```python
empty_dict = {}          # bu BOS SOZLUK
empty_set = set()        # bos kume boyle yazilir
```

`{}` boş küme değil, **boş sözlük** demek. Boş küme için `set()` yazman
gerekiyor. Python'da süslü parantez öncelikle sözlüğün.

## Hangisini ne zaman?

| İhtiyaç | Yapı |
|---|---|
| Sıralı bir topluluk, değişebilir | **liste** `[ ]` |
| Sıralı bir topluluk, değişmemeli | **demet** `( )` |
| Ad–değer eşleşmesi | **sözlük** `{a: d}` |
| Tekrarsız topluluk | **küme** `{a, b}` |

---

## Özet

- Sözlük değerleri sıra numarasıyla değil **anahtarla** saklar.
- `sozluk[anahtar]` ile okunur; olmayan anahtar `KeyError` verir.
- `in` **anahtarlara** bakar, değerlere değil.
- Atama hem ekler hem günceller: `sozluk[anahtar] = deger`.
- Sözlük üzerinde dönmek anahtarları verir; `items()` ikisini birden verir.
- Küme tekrar tutmaz ve sırasızdır; `set(liste)` tekrarları atmanın kısa yolu.
- `{}` boş **sözlüktür**; boş küme `set()` ile yazılır.
