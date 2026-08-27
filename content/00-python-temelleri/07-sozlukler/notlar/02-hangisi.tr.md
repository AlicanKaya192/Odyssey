Artık dört veri yapısı biliyorsun. Hangisini ne zaman seçeceğin, kod yazarken
sürekli önüne gelecek bir karar. Bu not o kararı kolaylaştırmak için.

## Dördü bir arada

| | Liste | Demet | Sözlük | Küme |
|---|---|---|---|---|
| Yazımı | `[1, 2]` | `(1, 2)` | `{"a": 1}` | `{1, 2}` |
| Sıralı mı | evet | evet | ekleme sırasını korur | hayır |
| Değişir mi | evet | **hayır** | evet | evet |
| Tekrar tutar mı | evet | evet | anahtarlar tekrar edemez | **hayır** |
| Erişim | `x[0]` | `x[0]` | `x["ad"]` | erişim yok |

## Karar için üç soru

**1. Bir şeyi adıyla mı arayacaksın?** Öyleyse sözlük. "Kullanıcı adına göre
puanı bul" gibi bir iş listede yapılırsa her seferinde baştan sona bakılır.

**2. Sıra önemli mi?** Önemliyse liste ya da demet. Bir sınavdaki soruların
sırası önemlidir, bir ürünün etiketleri önemli değildir.

**3. Tekrarlar sorun mu?** Sorunsa küme. "Bu metinde hangi kelimeler geçiyor"
sorusunun cevabı kümedir; "kaç kere geçiyor" sorusunun cevabı sözlüktür.

## Sık karşılaşılan durumlar

**Bir listedeki tekrarları atmak:**

```python
names = ["Ada", "Bob", "Ada", "Cem"]
unique = list(set(names))
```

Dikkat: küme sırasız olduğu için sonuç listesinin sırası bozulabilir. Sıra
önemliyse bu yöntem uygun değil.

**Bir şeyin kaç kere geçtiğini saymak:**

```python
votes = ["python", "go", "python"]

counts = {}
for vote in votes:
    counts[vote] = counts.get(vote, 0) + 1

print(counts)     # {'python': 2, 'go': 1}
```

`counts.get(vote, 0)` kalıbı burada çok işe yarıyor: anahtar yoksa sıfırdan
başlıyor, varsa üzerine ekliyor. `if` yazmaya gerek kalmıyor.

**İki listeyi eşleştirmek:**

```python
names = ["Ada", "Bob"]
scores = [90, 85]

pairs = dict(zip(names, scores))
print(pairs)     # {'Ada': 90, 'Bob': 85}
```

## İç içe yapılar

Bunlar birbirinin içine girebilir ve gerçek programlarda sürekli girer:

```python
students = [
    {"name": "Ada", "grades": [90, 85]},
    {"name": "Bob", "grades": [70, 75]},
]

print(students[0]["name"])         # Ada
print(students[0]["grades"][1])    # 85
```

Okurken soldan sağa gidiyorsun: `students[0]` birinci sözlüğü verir,
`["name"]` onun adını verir. Karmaşık görünse de kural hep aynı.
