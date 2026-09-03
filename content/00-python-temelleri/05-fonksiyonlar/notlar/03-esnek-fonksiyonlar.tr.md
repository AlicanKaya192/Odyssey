Fonksiyonların üç ileri özelliği. Yazman nadiren gerekiyor ama **okuman**
sürekli gerekecek — kütüphanelerin imzalarında hepsi var.

## `sorted` ve `key` — neye göre sıralanacak?

`sorted` bir listeyi sıralıyor:

```python
print(sorted([3, 1, 2]))
print(sorted(["banana", "apple"]))
```

```
[1, 2, 3]
['apple', 'banana']
```

Peki elemanlar sözlükse? Python "hangisi büyük" sorusunu cevaplayamıyor:

```python
people = [
    {"name": "Ada", "grade": 90},
    {"name": "Brian", "grade": 40},
]

sorted(people)
```

```
TypeError: '<' not supported between instances of 'dict' and 'dict'
```

`key` tam bu soruyu cevaplıyor: **her eleman için karşılaştırılacak değeri
üreten bir fonksiyon.**

```python
def by_grade(person):
    return person["grade"]


print(sorted(people, key=by_grade))
```

```
[{'name': 'Brian', 'grade': 40}, {'name': 'Ada', 'grade': 90}]
```

Büyükten küçüğe için `reverse=True`:

```python
sorted(people, key=by_grade, reverse=True)
```

`key`'e verilen şeyin **çağrılmadığına** dikkat et: `key=by_grade` yazılıyor,
`key=by_grade()` değil. Fonksiyonun kendisini veriyorsun, sonucunu değil.

## `lambda` — adı olmayan fonksiyon

Yukarıdaki `by_grade` fonksiyonu tek satır ve başka hiçbir yerde
kullanılmıyor. Böyle durumlar için kısa yazım var:

```python
print(sorted(people, key=lambda person: person["grade"]))
```

<figure class="fig anat">
  <div class="sig"><u class="m1">lambda</u> <u class="m2">person</u>: <u class="m3">person["grade"]</u></div>
  <ul class="legend">
    <li class="m1"><b>Anahtar kelime</b> — <code>def</code> yerine geçiyor, ad verilmiyor.</li>
    <li class="m2"><b>Parametre</b> — parantez yok, virgülle çoğaltılabiliyor.</li>
    <li class="m3"><b>Dönen değer</b> — <code>return</code> yazılmıyor, ifade zaten sonuç.</li>
  </ul>
</figure>

`lambda` **tek bir ifade** taşıyabiliyor. `if` bloğu, döngü, birden fazla
satır giremiyor. Girmesi gerekiyorsa `def` yazılıyor.

Sık kullanıldığı yerler:

```python
sorted(words, key=len)                        # uzunluga gore
sorted(people, key=lambda p: p["name"])       # ada gore
sorted(scores.items(), key=lambda pair: pair[1])   # sozlugu degere gore
```

Üçüncüsü işe yarıyor: sözlüğü **değerine göre** sıralamanın standart yolu bu.

**Yapma:** `lambda`ya isim verme. `topla = lambda a, b: a + b` yazmak yerine
`def topla(a, b):` yaz — ikisi aynı işi yapıyor ama ikincisi hata
mesajlarında fonksiyonun adını gösteriyor.

## `*args` — kaç tane olacağı belli değilse

Bir fonksiyonun kaç argüman alacağı önceden bilinmiyorsa:

```python
def total(*numbers):
    result = 0
    for number in numbers:
        result = result + number
    return result


print(total(1, 2))
print(total(1, 2, 3, 4))
```

```
3
10
```

Yıldız "gelen argümanları bir **demette** topla" demek. `numbers` fonksiyonun
içinde `(1, 2, 3, 4)` oluyor.

Adı `args` olmak zorunda değil ama gelenek bu; kütüphanelerde hep öyle
göreceksin.

## `**kwargs` — adlı argümanlar

İki yıldız, adıyla verilen argümanları bir **sözlükte** topluyor:

```python
def describe(**details):
    for key in details:
        print(key, "=", details[key])


describe(name="Ada", city="London")
```

```
name = Ada
city = London
```

Üçü bir arada kullanılabiliyor ve **sırası sabit**:

```python
def report(title, *values, **options):
    ...
```

Önce normal parametreler, sonra `*args`, en sonda `**kwargs`.

## Nerede karşına çıkacak?

Kütüphane imzalarında. Örneğin bir grafik fonksiyonu:

```python
def plot(x, y, *args, **kwargs):
    ...
```

Bu imza "iki zorunlu değer al, sonra ne verirsen ver" demek. Belgelerde
`**kwargs` gördüğünde "buraya adıyla ek ayar yazabilirim" diye okuyacaksın.

## Özet

- `sorted(items, key=...)` — neye göre sıralanacağını söyler; `key`'e
  fonksiyonun **kendisi** verilir.
- `lambda x: ifade` — adı olmayan, tek ifadelik fonksiyon. İsim vermek için
  kullanılmaz.
- `*args` argümanları demette, `**kwargs` adlı argümanları sözlükte toplar.
- Sıra sabittir: normal parametreler → `*args` → `**kwargs`.
