# Liste Üreteçleri

Bir listeden başka bir liste üretmek en sık yaptığın işlerden biri. Şu ana
kadar döngüyle yaptın:

```python
numbers = [1, 2, 3, 4]
doubled = []

for number in numbers:
    doubled.append(number * 2)

print(doubled)
```

```
[2, 4, 6, 8]
```

Python'da bunun tek satırlık bir yazımı var ve **gerçek kodda çok
yaygın** — okuyabilmen gerekiyor.

## İlk üretecin

```python
doubled = [number * 2 for number in numbers]
```

Aynı sonuç, dört satır yerine bir satır.

<figure class="fig anat">
  <div class="sig">[<u class="m1">number * 2</u> <u class="m2">for number in numbers</u>]</div>
  <ul class="legend">
    <li class="m1"><b>Ne üretilecek</b> — her eleman için hesaplanan değer. Listeye bu giriyor.</li>
    <li class="m2"><b>Nereden geliyor</b> — normal bir <code>for</code> döngüsünün başlığı, aynı yazım.</li>
  </ul>
</figure>

Okuma sırası tersten: **önce sağdaki döngüyü oku, sonra soldaki ifadeyi.**
"numbers içindeki her number için, number çarpı iki."

Köşeli parantez sonucun bir **liste** olduğunu söylüyor.

## Süzmek: `if` eklemek

Sonuna koşul eklenebiliyor:

```python
scores = [90, 40, 75, 30, 65]
passed = [score for score in scores if score >= 50]

print(passed)
```

```
[90, 75, 65]
```

Döngü karşılığı:

```python
passed = []
for score in scores:
    if score >= 50:
        passed.append(score)
```

Sondaki `if` bir **süzgeç**: koşul tutmayan eleman listeye hiç girmiyor.

İkisini birlikte de kullanabiliyorsun:

```python
names = ["ada", "alan", "grace"]
short = [name.upper() for name in names if len(name) < 5]

print(short)
```

```
['ADA', 'ALAN']
```

## Sözlük ve küme üreteci

Aynı yazım süslü parantezle sözlük üretiyor:

```python
names = ["Ada", "Alan"]
lengths = {name: len(name) for name in names}

print(lengths)
```

```
{'Ada': 3, 'Alan': 4}
```

İki nokta olmadan küme üretiyor:

```python
unique = {len(name) for name in names}
```

Sözlüğün üzerinde de dönebiliyorsun:

```python
scores = {"Ada": 90, "Alan": 40}
passed = {name: value for name, value in scores.items() if value >= 50}

print(passed)
```

```
{'Ada': 90}
```

## Ne zaman kullanılır, ne zaman kullanılmaz?

Üreteç her döngünün yerini almıyor. Ölçüt: **tek bir liste üretiyorsan
kullan.**

<figure class="fig">
  <div class="versus">
    <div class="ok">
      <h5>UYGUN</h5>
<pre><code>squares = [n * n for n in numbers]</code></pre>
    </div>
    <div class="no">
      <h5>UYGUN DEĞİL</h5>
<pre><code>[print(n) for n in numbers]</code></pre>
    </div>
  </div>
  <figcaption>Sağdaki bir liste üretmiyor, ekrana yazdırıyor — ve sonuçta işe yaramaz bir <code>None</code> listesi bırakıyor. İş yapan döngüler normal <code>for</code> ile yazılır.</figcaption>
</figure>

**Kullanma:**

- İçinde birden fazla iş varsa. Üreteç tek ifade taşıyabiliyor.
- İç içe iki döngü ve koşul varsa. Okunmuyor; normal döngü daha açık.
- Yan etki için (`print`, dosyaya yazma, listeye ekleme). Üretecin işi
  değer üretmek.

Uzunluk sınırı basit: **bir satıra sığmıyorsa döngü yaz.**

## Karşılaştırma tablosu

| Döngü | Üreteç |
|---|---|
| `result = []`<br>`for x in items:`<br>`    result.append(x * 2)` | `result = [x * 2 for x in items]` |
| `for x in items:`<br>`    if x > 0:`<br>`        result.append(x)` | `result = [x for x in items if x > 0]` |
| `for k, v in d.items():`<br>`    out[k] = v * 2` | `out = {k: v * 2 for k, v in d.items()}` |

## Nerede karşına çıkacak?

Her yerde. Bir kütüphane belgesine baktığında, bir örnek koda baktığında,
Stack Overflow cevabında. Veri biliminde de yaygın:

```python
columns = [name.strip().lower() for name in header]
```

Bu satır bir CSV başlığını temizliyor. Öğrendiğin şey tam olarak bu satırı
okuyabilmek.
