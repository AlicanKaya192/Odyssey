# Koşul Tuzakları

Yeni başlayanların koşullarda en sık düştüğü yerler. Hepsi gerçek hatalardan
derlendi; çoğu **hata vermiyor**, sessizce yanlış çalışıyor — asıl tehlikeli
olan da bu.

## 1. `=` yerine `==`

```python
if age = 18:
    print("adult")
```

```
SyntaxError: invalid syntax
```

`=` atama yapar, `==` karşılaştırır. Bu, hata verdiği için iyi bir tuzak —
fark etmemen mümkün değil.

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h5>ATAMA</h5>
<pre><code>age = 18</code></pre>
    </div>
    <div class="ok">
      <h5>KARŞILAŞTIRMA</h5>
<pre><code>age == 18</code></pre>
    </div>
  </div>
  <figcaption>Tek eşittir bir değer koyar, çift eşittir bir soru sorar.</figcaption>
</figure>

## 2. `if x == 1 or 2`

Bu satır hata vermiyor ama **her zaman doğru**:

```python
number = 7

if number == 1 or 2:
    print("matched")
```

```
matched
```

Python bunu `(number == 1) or (2)` diye okuyor. `2` boş olmayan bir sayı,
yani doğruluk değeri `True`. Sonuç: koşul hep tutuyor.

Doğrusu her ihtimali ayrı yazmak:

```python
if number == 1 or number == 2:
    print("matched")
```

Ya da daha kısası:

```python
if number in (1, 2):
    print("matched")
```

## 3. `== True` yazmak

```python
if is_ready == True:
    print("go")
```

Çalışıyor ama gereksiz. `is_ready` zaten `True` ya da `False`; onu tekrar
`True` ile karşılaştırmak "doğru mu doğru?" demek.

```python
if is_ready:
    print("go")
```

Tersi için `not`:

```python
if not is_ready:
    print("wait")
```

## 4. Ondalıklı sayıları `==` ile karşılaştırmak

```python
print(0.1 + 0.2 == 0.3)
```

```
False
```

Hata değil. Bilgisayar ondalıklı sayıları ikilik sistemde tuttuğu için
`0.1 + 0.2` tam olarak `0.30000000000000004` oluyor.

Ondalıklı sayılarda eşitlik yerine **yakınlık** sorulur:

```python
total = 0.1 + 0.2

if abs(total - 0.3) < 0.0001:
    print("close enough")
```

Tam sayılarda böyle bir sorun yok; `==` güvenle kullanılır.

## 5. `elif` yerine arka arkaya `if`

Bu ikisi aynı şey değil:

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h5>ARKA ARKAYA if</h5>
<pre><code>if score &gt;= 90:
    grade = "A"
if score &gt;= 80:
    grade = "B"</code></pre>
    </div>
    <div class="ok">
      <h5>elif</h5>
<pre><code>if score &gt;= 90:
    grade = "A"
elif score &gt;= 80:
    grade = "B"</code></pre>
    </div>
  </div>
  <figcaption>Soldaki 95 puan için önce "A" yazıp sonra "B" ile eziyor. Sağdaki ilk tutan koşulda duruyor.</figcaption>
</figure>

`score = 95` olduğunda soldaki kod `grade` değişkenine önce `"A"`, sonra
`"B"` koyuyor — çünkü 95 ikisinden de büyük ve iki `if` de ayrı ayrı
çalışıyor. Sonuç `"B"`, yani yanlış.

`elif` "önceki tutmadıysa buna bak" demek. İlk tutan koşulda zincir kapanıyor.

## 6. Sıralamayı ters yazmak

```python
if score >= 50:
    grade = "pass"
elif score >= 90:
    grade = "excellent"
```

`score = 95` için sonuç `"pass"`. Çünkü 95 önce `>= 50` koşuluna takılıyor
ve zincir orada bitiyor; `elif` satırına hiç gelinmiyor.

**Kural:** `elif` zincirinde koşullar **dardan genişe** sıralanır. En
seçici olan en üste yazılır.

```python
if score >= 90:
    grade = "excellent"
elif score >= 50:
    grade = "pass"
```

## 7. Girinti

Python'da girinti süs değil, kodun kendisi:

```python
if logged_in:
    print("welcome")
print("goodbye")
```

`print("goodbye")` girintili olmadığı için `if`'in **dışında**. Koşul
tutmasa bile çalışıyor. İçeride olmasını istiyorsan girintilemen gerekiyor.

Bir de karışık girinti sorunu var: bazı satırda boşluk, bazısında sekme
kullanırsan Python `TabError` veriyor. Düzenleyicini "sekmeyi boşluğa çevir"
olarak ayarla, dört boşluk kullan.

## 8. Boş kabı `len` ile sormak

Çalışıyor ama uzun:

```python
if len(items) > 0:
    print("has items")
```

Python'da boş liste, boş metin ve boş sözlük zaten `False` sayılıyor:

```python
if items:
    print("has items")
```

Aynı şey, daha kısa. Boşluk kontrolü için tercih edileni bu.

## Özet

- `=` atar, `==` karşılaştırır.
- `x == 1 or 2` her zaman doğrudur; her ihtimali ayrı yaz.
- `== True` gereksiz, koşulu doğrudan yaz.
- Ondalıklı sayılarda eşitlik değil yakınlık sor.
- Arka arkaya `if` ile `elif` farklı çalışır.
- `elif` zincirinde en seçici koşul en üste.
- Girinti kodun anlamını değiştirir.
- Boşluk kontrolü için `if items:` yeterli.
