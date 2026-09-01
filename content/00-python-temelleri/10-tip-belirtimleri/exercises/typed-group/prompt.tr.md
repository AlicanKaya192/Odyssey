Gerçek veri işlerinde en sık karşılaşacağın biçim bu: bir tablonun satırları,
sözlüklerden oluşan bir liste olarak duruyor. Bu alıştırmada hem onu
gruplayacak hem de belirtimlerini yazacaksın.

Elindeki veri:

```python
people = [
    {"name": "Ada", "city": "London"},
    {"name": "Alan", "city": "London"},
    {"name": "Grace", "city": "New York"},
]
```

**Yapman gerekenler:**

1. `group_by_city` adında bir fonksiyon yaz:
   - Parametresi `rows` — sözlüklerden oluşan bir liste.
   - Geriye şehir adına göre **isim listesi** tutan bir sözlük döndürür.

2. `first_name` adında bir fonksiyon yaz:
   - Parametreleri `rows` ve `city`.
   - O şehirdeki **ilk** ismi döndürür. Şehir hiç yoksa `None` döndürür.
   - Dönüş belirtimi bu iki ihtimali de anlatmalı.

3. Sırayla şunları yazdır:
   - `group_by_city(people)`
   - `first_name(people, "New York")`
   - `first_name(people, "Paris")`

**Beklenen çıktı:**

```
{'London': ['Ada', 'Alan'], 'New York': ['Grace']}
Grace
None
```

> Bir anahtar sözlükte yoksa önce boş liste koyman gerekiyor:
> `if city not in result: result[city] = []`
