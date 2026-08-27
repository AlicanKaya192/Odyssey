Sözlüklerin de kendi metotları var. Beş tanesini bilmen yeter.

## get — hata vermeden okur

```python
prices = {"apple": 12, "banana": 8}

print(prices.get("apple"))       # 12
print(prices.get("cherry"))      # None   <- hata vermez
```

Köşeli parantezle okumakla farkı burada: `prices["cherry"]` yazarsan `KeyError`
alırsın, `get` ise sessizce `None` verir.

İkinci bir değer verirsen, anahtar yoksa onu döndürür:

```python
print(prices.get("cherry", 0))     # 0
```

Bu kalıp çok işine yarayacak: "varsa değerini al, yoksa sıfır say".

## keys, values, items

```python
prices = {"apple": 12, "banana": 8}

print(list(prices.keys()))       # ['apple', 'banana']
print(list(prices.values()))     # [12, 8]
print(list(prices.items()))      # [('apple', 12), ('banana', 8)]
```

`items()` her çifti bir **demet** olarak veriyor. Döngüde en çok kullanacağın
biçim bu:

```python
for key, value in prices.items():
    print(key, "->", value)
```

## update — toplu ekler ve günceller

```python
prices = {"apple": 12}
prices.update({"banana": 8, "apple": 15})

print(prices)     # {'apple': 15, 'banana': 8}
```

Var olan anahtarı günceller, olmayanı ekler. Tek tek atama yapmak yerine birden
fazla çifti bir seferde vermek istediğinde kullanılır.

## setdefault — sadece yoksa ekler

```python
prices = {"apple": 12}

prices.setdefault("apple", 99)     # apple zaten var, DOKUNMAZ
prices.setdefault("cherry", 45)    # cherry yok, ekler

print(prices)     # {'apple': 12, 'cherry': 45}
```

`update` ile karıştırılır. Farkı tek cümle: **`update` üzerine yazar,
`setdefault` yazmaz.**

## Bir uyarı

Kaynak metinlerde bazen "setdefault ile eklediğin kalıcı olmaz" gibi ifadeler
görürsün. Bu doğru ama yanıltıcı — sözlüğe **hiçbir** yolla eklediğin şey
kalıcı değildir. Program kapandığında bellekteki her şey gider. Kalıcılık
istiyorsan dosyaya ya da veritabanına yazman gerekir; bu `setdefault` ile ilgili
bir sınırlama değil.

## Sözlük mü liste mi?

Bir şeyi ararken aradaki fark önemli:

```python
# listede arama: bastan sona bakar
if "apple" in fruit_list:
    ...

# sozlukte arama: dogrudan gider
if "apple" in prices:
    ...
```

Liste büyüdükçe arama yavaşlar; sözlükte boyut ne olursa olsun arama hızı
değişmez. Elinde "şunu ada göre bul" gibi bir iş varsa sözlük doğru seçim.
