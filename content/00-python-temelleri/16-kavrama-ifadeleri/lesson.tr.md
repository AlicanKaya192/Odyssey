# Kavrama İfadeleri

Bir listeden başka bir liste üretmek, bir listeden sözlük kurmak, bir
listeyi süzmek — yazdığın kodun büyük kısmı bunlar. Python'da bu işlerin
tek satırlık bir yazımı var: **kavrama ifadesi** (İngilizcesi
*comprehension*).

Listeler bölümünde liste hâlini görmüştün: dönüştürme ve süzme. Burada
dört soruyu kapatıyoruz: sözlük ve küme nasıl üretilir, süzgeç ile koşullu
değer nasıl ayrılır, iç içe nasıl yazılır ve belleği doldurmadan nasıl
hesaplanır.

## Hatırlatma: liste kavraması

```python
numbers = [1, 2, 3, 4, 5]

squares = []
for number in numbers:
    squares.append(number * number)
```

Aynı iş tek satırda:

```python
squares = [number * number for number in numbers]
```

<figure class="fig anat">
  <div class="sig">[<u class="m1">number * number</u> <u class="m2">for number in numbers</u> <u class="m3">if number % 2 == 0</u>]</div>
  <ul class="legend">
    <li class="m1"><b>Üretilecek değer</b> — listeye bu giriyor.</li>
    <li class="m2"><b>Kaynak</b> — sıradan bir <code>for</code> başlığı.</li>
    <li class="m3"><b>Süzgeç</b> — isteğe bağlı; koşulu geçmeyen eleman alınmıyor.</li>
  </ul>
</figure>

Okuma sırası: **önce ortadaki döngü, sonra sağdaki koşul, en sonda soldaki
ifade.** "numbers içindeki her number için, çiftse, karesini al."

## Sözlük kavraması

Süslü parantez ve `anahtar: değer` yazımı sözlük üretiyor:

```python
names = ["ada", "alan", "grace"]

lengths = {name: len(name) for name in names}
print(lengths)
```

```
{'ada': 3, 'alan': 4, 'grace': 5}
```

Elinde zaten bir sözlük varsa `items()` ile dönülüyor:

```python
scores = {"ada": 90, "alan": 45, "grace": 72}

passed = {name: score for name, score in scores.items() if score >= 50}
print(passed)
```

```
{'ada': 90, 'grace': 72}
```

Anahtarla değeri yer değiştirmek de aynı yolla oluyor:

```python
flipped = {score: name for name, score in scores.items()}
```

## Küme kavraması

Süslü parantez ama `anahtar: değer` yok — sonuç küme, yani **tekrarsız**:

```python
words = ["elma", "armut", "erik", "ayva"]

initials = {word[0] for word in words}
print(initials)
```

```
{'a', 'e'}
```

Dört kelimeden iki harf çıktı; küme tekrarı kendiliğinden atıyor.

## Koşullu değer: `if ... else`

Süzgeç ile karıştırılıyor ama farklı bir şey. Süzgeç **eleman alır ya da
almaz**; koşullu değer **her elemana bir şey yazar**:

```python
scores = [90, 45, 72]

labels = ["passed" if score >= 50 else "failed" for score in scores]
print(labels)
```

```
['passed', 'failed', 'passed']
```

Yeri de farklı: süzgeç **sonda**, koşullu değer **başta** duruyor.

<figure class="fig versus">
  <div class="ok">
    <h4>Süzgeç (sonda)</h4>
    <p><code>[s for s in scores if s &gt;= 50]</code></p>
    <p>Üç elemandan ikisi kalır. Uzunluk değişir.</p>
  </div>
  <div class="dim">
    <h4>Koşullu değer (başta)</h4>
    <p><code>["ok" if s &gt;= 50 else "no" for s in scores]</code></p>
    <p>Üç eleman üç eleman kalır, değerleri değişir.</p>
  </div>
</figure>

## İç içe kavrama

İki kat derin bir listeyi düzleştirmek:

```python
rows = [[1, 2], [3, 4], [5]]

flat = [value for row in rows for value in row]
print(flat)
```

```
[1, 2, 3, 4, 5]
```

Sıra, iç içe yazılmış `for` satırlarının sırasıyla aynı:

```python
flat = []
for row in rows:
    for value in row:
        flat.append(value)
```

Soldan sağa okunuyor: önce dış döngü, sonra iç döngü. İkiden fazla
katmanda okunurluk hızla düşüyor; orada normal döngü yazmak daha iyi.

## Üreteç ifadesi: köşeli parantez yerine parantez

```python
numbers = [1, 2, 3, 4, 5]

total = sum(number * number for number in numbers)
any_big = any(number > 4 for number in numbers)
all_positive = all(number > 0 for number in numbers)

print(total, any_big, all_positive)
```

```
55 True True
```

Buradaki ifade listeyi **kurmuyor**; elemanları tek tek üretip
`sum()`'a veriyor. Milyonluk bir dosyada bu, belleği doldurmakla
doldurmamak arasındaki fark.

## Ne zaman kullanılmaz

<figure class="fig anat">
  <div class="anat-row"><span>Yan etki varsa</span><span>Dosyaya yazmak, ekrana basmak için kavrama kullanılmaz; sonucu kullanılmayan bir liste üretmiş olursun.</span></div>
  <div class="anat-row"><span>Satır uzuyorsa</span><span>Bir satıra sığmayan kavrama, döngü hâlinde daha okunur.</span></div>
  <div class="anat-row"><span>İç içe üç kat</span><span>İki kata kadar okunuyor; fazlası için normal döngü.</span></div>
  <div class="anat-row"><span>Karmaşık koşul</span><span><code>if</code> içinde üç koşul birleşiyorsa, döngü ve <code>continue</code> daha anlaşılır.</span></div>
</figure>

Şu **kullanılmaz**:

```python
[print(name) for name in names]
```

Ekrana yazıyor ama bir de `[None, None, None]` listesi üretip atıyor.
Doğrusu sıradan bir döngü.

## Özet

- `[ifade for eleman in kaynak if koşul]` — liste üretir.
- `{anahtar: değer for ...}` sözlük, `{değer for ...}` küme üretir.
- Süzgeç sonda, koşullu değer (`x if c else y`) başta durur.
- `for` satırları iç içe yazılabilir; iki kattan fazlası okunmaz.
- Parantezle yazılan üreteç ifadesi liste kurmaz; `sum`, `any`, `all` ile
  birlikte belleği doldurmadan çalışır.
- Yan etki için, uzun satırda ve karmaşık koşulda normal döngü yazılır.
