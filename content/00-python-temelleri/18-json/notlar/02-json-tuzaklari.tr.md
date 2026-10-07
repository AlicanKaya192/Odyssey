JSON'la ilgili hataların çoğu birkaç kalıptan çıkıyor. Hata mesajını tanırsan
sebebi hemen bulursun.

## 1. `loads` ile `load`'u karıştırmak

```python
json.loads(file)            # dosya verdin, metin bekliyordu
json.load('{"a": 1}')       # metin verdin, dosya bekliyordu
```

```text
TypeError: the JSON object must be str, bytes or bytearray, not TextIOWrapper
AttributeError: 'str' object has no attribute 'read'
```

`s` varsa metin, yoksa dosya.

## 2. Python sözlüğü gibi yazmak

| Yazılan | Mesaj |
|---|---|
| `{'name': 'Ada'}` | `Expecting property name enclosed in double quotes` |
| `{"a": 1,}` | `Illegal trailing comma before end of object` |
| `{"a": True}` | `Expecting value` |

Hepsi `json.JSONDecodeError`. Mesajın sonundaki `line` ve `column` bozuk
yeri gösteriyor.

## 3. Boş dosya

İçi boş bir dosyayı `json.load` ile okumak da hata:

```text
Expecting value: line 1 column 1 (char 0)
```

"Daha hiç kayıt yok" durumu için dosyayı hiç oluşturmamak ve
`FileNotFoundError`'ı yakalamak, ya da ilk seferde `[]` yazmak gerekiyor.

## 4. `"a"` kipiyle sona eklemek

```python
with open("log.json", "a", encoding="utf-8") as file:
    json.dump({"run": 1}, file)
```

İki kez çalışınca dosyada `{"run": 0}{"run": 1}` duruyor: iki ayrı JSON
metni yan yana. Okumaya çalışınca:

```text
Extra data: line 1 column 11 (char 10)
```

JSON dosyası bir bütün: **oku → değiştir → `"w"` ile baştan yaz.**

## 5. `str()` ile yazmak

`file.write(str(data))` dosyaya Python'un görüntüsünü yazıyor (tek tırnak,
`True`, `None`); bu geçerli JSON değil ve `json.load` okuyamıyor. Her zaman
`json.dump`.

## 6. Sayı anahtarın metne dönmesi

```python
back = json.loads(json.dumps({1: "one"}))
back[1]       # KeyError: 1
back["1"]     # "one"
```

Sayıyı anahtar değil **değer** olarak tut (`{"id": 1}`), ya da geri
okuyunca `int(...)` ile çevir.

## 7. Küme ve başka türler

```text
TypeError: Object of type set is not JSON serializable
```

Küme, demet dışındaki özel nesneler (tarih gibi) JSON'a doğrudan gitmiyor.
Yazmadan önce JSON'un tanıdığı bir türe çevir: küme → `sorted(...)` liste.

## 8. Olmayan alanı köşeli parantezle istemek

Dışarıdan gelen veride bir alan eksik olabilir. `user["email"]` `KeyError`
verir; `user.get("email", varsayılan)` vermez.
