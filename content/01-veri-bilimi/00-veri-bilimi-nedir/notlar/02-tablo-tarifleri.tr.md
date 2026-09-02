# Tablo Tarifleri (kütüphanesiz)

Sözlük listesi üzerinde en sık gereken altı işlemin düz Python karşılığı.
Alıştırmaları çözerken buraya bakabilirsin.

Bütün örneklerde şu veri kullanılıyor:

```python
students = [
    {"name": "Ada", "city": "Ankara", "score": 82},
    {"name": "Kerem", "city": "Izmir", "score": 74},
    {"name": "Mina", "city": "Ankara", "score": 91},
    {"name": "Deniz", "city": "Izmir", "score": 68},
]
```

## 1. Sütun çıkarmak

Bir sütunun bütün değerlerini liste hâlinde almak:

```python
scores = [student["score"] for student in students]
print(scores)
```

```text
[82, 74, 91, 68]
```

pandas'ta bu `data["score"]` olacak.

## 2. Ortalama

```python
scores = [student["score"] for student in students]
average = sum(scores) / len(scores)
print(average)
```

```text
78.75
```

**Tuzak:** liste boşsa `len(scores)` sıfır ve `ZeroDivisionError` alıyorsun.
Gerçek veride bu sık oluyor — filtreledikten sonra hiçbir satır kalmayabilir.

```python
average = sum(scores) / len(scores) if scores else 0
```

pandas'ta bu `data["score"].mean()` olacak.

## 3. Filtreleme

Koşula uyan satırları seçmek:

```python
high = [student for student in students if student["score"] >= 80]
for student in high:
    print(student["name"])
```

```text
Ada
Mina
```

Birden fazla koşul:

```python
selected = [
    student
    for student in students
    if student["city"] == "Ankara" and student["score"] >= 80
]
```

pandas'ta bu `data[data["score"] >= 80]` olacak.

## 4. Sıralama

```python
by_score = sorted(students, key=lambda student: student["score"])
print(by_score[0]["name"])
```

```text
Deniz
```

Büyükten küçüğe:

```python
by_score = sorted(students, key=lambda student: student["score"], reverse=True)
```

`sorted` **yeni bir liste** döndürüyor, özgün liste bozulmuyor.

pandas'ta bu `data.sort_values("score")` olacak.

## 5. Gruplama

Satırları bir sütuna göre kümelere ayırmak:

```python
groups = {}
for student in students:
    city = student["city"]
    if city not in groups:
        groups[city] = []
    groups[city].append(student)

print(list(groups))
```

```text
['Ankara', 'Izmir']
```

Aynısını `setdefault` ile daha kısa yazabilirsin:

```python
groups.setdefault(city, []).append(student)
```

pandas'ta bu `data.groupby("city")` olacak.

## 6. Grup başına hesap

Gruplama ile toplulaştırmayı birleştirmek — en sık gereken şey:

```python
totals = {}
counts = {}

for student in students:
    city = student["city"]
    totals[city] = totals.get(city, 0) + student["score"]
    counts[city] = counts.get(city, 0) + 1

averages = {city: totals[city] / counts[city] for city in totals}
print(averages)
```

```text
{'Ankara': 86.5, 'Izmir': 71.0}
```

`dict.get(key, 0)` burada işi kolaylaştırıyor: anahtar yoksa sıfırdan
başlıyor, `if city not in totals` yazmaya gerek kalmıyor.

pandas'ta bu `data.groupby("city")["score"].mean()` olacak.

## Yan yana

| İş | Düz Python | pandas (ilerideki bölümler) |
|---|---|---|
| Sütun al | `[s["score"] for s in students]` | `data["score"]` |
| Ortalama | `sum(scores) / len(scores)` | `data["score"].mean()` |
| Filtrele | `[s for s in students if ...]` | `data[data["score"] >= 80]` |
| Sırala | `sorted(students, key=...)` | `data.sort_values("score")` |
| Grupla + hesapla | 8 satır | `data.groupby("city")["score"].mean()` |

Sağdaki sütun kısa ama soldakini bilmeden yazılmıyor. `groupby` bir hata
verdiğinde ne yapmaya çalıştığını bilmen gerekiyor.

## Sayı biçimlendirme

Ortalamalar genelde uzun ondalıklar veriyor:

```python
average = 78.75333333333333
print(round(average, 2))
print(f"{average:.2f}")
```

```text
78.75
78.75
```

`round()` bir **sayı** döndürüyor, f-string ile biçimlendirme bir **metin**.
Karşılaştırma yapacaksan `round`, ekrana yazdıracaksan f-string.

**Tuzak:** `round(2.5)` sonucu `2`, `round(3.5)` sonucu `4`. Python tam
yarımlarda en yakın **çift** sayıya yuvarlıyor. Bu bir hata değil, bilinçli
bir seçim (bankacı yuvarlaması); toplamda sapmayı azaltıyor.
