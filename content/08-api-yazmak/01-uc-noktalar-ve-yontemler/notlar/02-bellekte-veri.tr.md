Veritabanına geçmeden önce (Veritabanı bölümü) veriyi bellekte tutmanın
kalıpları ve tuzakları.

## Kalıplar

```python
state = {"count": 0}          # tek bir değer
notes = []                     # kayıt listesi
books = {}                     # kimliğe göre kayıtlar: {1: {...}, 2: {...}}
next_id = {"value": 1}         # sıradaki kimlik
```

Hepsi işlevlerin **dışında**, dosyanın üstünde. İçlerini işlevden
değiştirmek serbest: `notes.append(...)`, `books[3] = ...`,
`state["count"] += 1`.

## Tuzaklar

**Veriyi işlevin içinde tanımlamak.**

```python
@app.post("/counter")
def increase():
    state = {"count": 0}   # her istekte baştan 0
    state["count"] += 1
    return state           # hep {"count": 1}
```

**Düz değişkeni değiştirmek.**

```python
count = 0


@app.post("/counter")
def increase():
    count += 1   # UnboundLocalError: cannot access local variable 'count'
```

Python işlevin içinde atanan adı yerel sayıyor. Ya sözlük/liste kullan ya
da işlevin başına `global count` yaz; sözlük daha az şaşırtıyor.

**Sunucu yeniden başlayınca her şeyin silinmesi.** `--reload` her
kayıtta yeniden başlattığı için veri sık sık sıfırlanır; bu bir hata değil,
belleğin doğası.

**Birden çok işçi.** Üretimde sunucu bazen birkaç süreçle (`--workers 4`)
çalıştırılır; her sürecin **kendi** belleği olur ve iki istek iki farklı
sayaca gidebilir. Paylaşılan veri bu yüzden veritabanında tutulur.
