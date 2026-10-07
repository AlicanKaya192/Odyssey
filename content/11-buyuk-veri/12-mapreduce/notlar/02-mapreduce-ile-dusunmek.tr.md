Bir soruyu MapReduce'a çevirmek, "map ne yayacak, anahtar ne olacak, reduce
ne birleştirecek?" sorularını cevaplamak demek. Sık karşılaşılan işlerin
kalıpları.

## Ortalama

Ortalama doğrudan birleşmiyor (Bölüm 3); map `(toplam, sayı)` yaysın:

```python
def mapper(row):
    yield row["city"], (row["unit_price"], 1)

def reducer(key, values):
    total = sum(v[0] for v in values)
    count = sum(v[1] for v in values)
    return key, total / count
```

Birleştirici de aynı ikiliyi toplayabiliyor.

## Farklı değer sayısı

"Her şehirde kaç farklı müşteri var?" İki adım:

1. Map `((şehir, müşteri), None)` yaysın; reduce her anahtarı bir kez
   yazsın → tekrarlar gider.
2. İkinci MapReduce: map `(şehir, 1)` yaysın; reduce toplasın.

## İlk N

"En pahalı 10 sipariş." Her parça kendi ilk 10'unu çıkarsın (birleştirici),
tek bir reduce bunların arasından ilk 10'u seçsin. Bölüm 3'teki
`nlargest` kalıbı.

## Birleştirme (JOIN)

Siparişler ile müşteri tablosunu `customer_id` üzerinden birleştirmek:

```python
def mapper(record, source):
    yield record["customer_id"], (source, record)

def reducer(key, values):
    customers = [r for s, r in values if s == "customer"]
    orders = [r for s, r in values if s == "order"]
    for c in customers:
        for o in orders:
            yield {**c, **o}
```

Her kayıt hangi tablodan geldiğini bir etiketle taşıyor; aynı müşterinin
bütün kayıtları aynı reduce'a geldiği için orada eşleştiriliyor. SQL'de tek
satır olan iş burada bir MapReduce adımı; Spark ve Hive bunu senin yerine
kuruyor.

## Ters dizin (inverted index)

Arama motorlarının temeli: "her kelime hangi belgelerde geçiyor?"

```python
def mapper(doc_id, text):
    for word in set(text.split()):
        yield word, doc_id

def reducer(word, doc_ids):
    return word, sorted(doc_ids)
```

## Kontrol soruları

- Anahtar ne? Aynı anahtarın değerleri reduce'ta buluşacak.
- Reduce'un yaptığı birleşebilir mi? Evetse birleştirici kullan.
- Bir anahtar çok mu büyük? Çarpıklık var; tuzlamayı düşün.
- Tek adım yetiyor mu? Farklı değer sayısı ve birleştirme gibi işler iki adım
  istiyor.
