Bir sınıfın notları elinde:

```python
scores = [70, 85, 90, 60, 95, 80]
```

İki sayı hesaplayacaksın: **ortalama** ve **medyan**. İkisi de `statistics`
modülünde hazır duruyor.

Bu alıştırmada `import statistics` yazmayacaksın. Fonksiyonları **doğrudan**
alacaksın, yani `from ... import ...` biçimini kullanacaksın.

**Yapman gerekenler:**

1. `statistics` modülünden `mean` ve `median` fonksiyonlarını doğrudan al.
2. İki değişken oluştur:

| Değişken | İçinde ne olacak |
|---|---|
| `average` | Notların ortalaması |
| `middle` | Notların medyanı |

3. İkisini **alt alta** yazdır.

**Beklenen çıktı:**

```
80
82.5
```

Medyan `82.5` çıkıyor çünkü altı not var; sıralayınca ortada tek bir sayı
kalmıyor, ortadaki iki sayının ortası alınıyor.
