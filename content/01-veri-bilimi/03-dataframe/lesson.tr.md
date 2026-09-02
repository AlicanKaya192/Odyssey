# DataFrame Temelleri

Seri tek bir sütundu: notlar, fiyatlar, şehirler. Gerçek veri ise **birden
fazla sütun**: kim, nerede, kaç, ne zaman.

**DataFrame**, yan yana dizilmiş serilerden oluşan tablo. Bu patikanın geri
kalanında çalışacağın yapı bu.

```python
import pandas as pd
```

## İlk tablo

En yaygın yol bir sözlükten kurmak — **anahtarlar sütun adı**, değerler
sütunun içeriği:

```python
data = pd.DataFrame({
    "name": ["Ada", "Kerem", "Mina", "Deniz"],
    "city": ["Ankara", "Izmir", "Ankara", "Bursa"],
    "score": [82, 74, 91, 68],
})

print(data)
```

```text
    name    city  score
0    Ada  Ankara     82
1  Kerem   Izmir     74
2   Mina  Ankara     91
3  Deniz   Bursa     68
```

Solda index, üstte sütun adları. İlk bölümdeki sözlük listesi tam olarak
buydu; artık onu döngüyle işlemek zorunda değilsin.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">satır</span><span class="anat-body">bir kayıt; index onu adlandırıyor</span></div>
    <div class="anat-row"><span class="anat-label">sütun</span><span class="anat-body">bir özellik; her sütun aslında bir <b>seri</b></span></div>
    <div class="anat-row"><span class="anat-label">index</span><span class="anat-body">satır etiketleri — bütün sütunlar bunu paylaşıyor</span></div>
    <div class="anat-row"><span class="anat-label">columns</span><span class="anat-body">sütun etiketleri; kendisi de bir index</span></div>
  </div>
</figure>

Sözlük listesinden de kurulabiliyor — CSV ya da API'den gelen veri genelde
bu biçimde:

```python
rows = [{"a": 1, "b": 2}, {"a": 3, "b": 4}]
print(pd.DataFrame(rows))
```

```text
   a  b
0  1  2
1  3  4
```

## Tabloya ilk bakış

Bir veriyi ilk açtığında sorulan dört soru var ve dördünün de tek satırlık
cevabı var:

```python
print(data.shape)
print(list(data.columns))
print(data.dtypes)
print(data.head(2))
```

```text
(4, 3)
['name', 'city', 'score']
name       str
city       str
score    int64
dtype: object
    name    city  score
0    Ada  Ankara     82
1  Kerem   Izmir     74
```

- `shape` → **(satır, sütun)**. Kaç kaydın var, kaç özelliğin.
- `columns` → sütun adları. Yazım hatası aramanın en hızlı yolu.
- `dtypes` → her sütunun tipi. Sayı olması gereken bir sütun `str`
  görünüyorsa orada bir sorun var.
- `head()` → ilk satırlar. Veriye bakmadan hakkında konuşma.

`dtypes` çıktısında metin sütunları `str` yazıyor. Eski belgelerde bunun
yerine `object` göreceksin; pandas 3.0'da değişti.

## Sütun seçmek

Tek sütun istediğinde geriye bir **seri** dönüyor:

```python
print(data["score"])
```

```text
0    82
1    74
2    91
3    68
Name: score, dtype: int64
```

Serinin `name` özelliği sütunun adını taşıyor — geçen bölümde bahsi geçen
bağ buydu.

Birden fazla sütun istediğinde geriye bir **DataFrame** dönüyor. Dikkat:
**iç içe köşeli parantez**.

```python
print(data[["name", "score"]])
```

```text
    name  score
0    Ada     82
1  Kerem     74
2   Mina     91
3  Deniz     68
```

<figure class="fig">
  <div class="versus">
    <div class="versus-side">
      <h4>data["score"]</h4>
      <p>Tek sütun → <b>Seri</b>. Üzerinde <code>mean()</code>, <code>value_counts()</code> gibi seri metotları çalışıyor.</p>
    </div>
    <div class="versus-side">
      <h4>data[["score"]]</h4>
      <p>Liste verildi → <b>DataFrame</b>. Tek sütunlu bir tablo; hâlâ tablo.</p>
    </div>
  </div>
  <figcaption>Aradaki fark tek bir köşeli parantez. Hangisini aldığını bilmek gerekiyor, çünkü metotları farklı.</figcaption>
</figure>

## Sütun eklemek

Yeni sütun, var olanlardan hesaplanıyor:

```python
data["bonus"] = data["score"] + 5
data["passed"] = data["score"] >= 75

print(data[["name", "score", "bonus", "passed"]])
```

```text
    name  score  bonus  passed
0    Ada     82     87    True
1  Kerem     74     79   False
2   Mina     91     96    True
3  Deniz     68     73   False
```

Döngü yok. Sütun bir seri olduğu için vektörel işlemler aynen geçerli;
karşılaştırma da `True`/`False` sütunu üretiyor.

Sütun silmek:

```python
print(list(data.drop(columns=["bonus"]).columns))
```

```text
['name', 'city', 'score', 'passed']
```

`drop` **yeni bir tablo** döndürüyor; özgün `data` değişmiyor. pandas'ın
genel kuralı burada da geçerli.

## Sıralamak

```python
print(data.sort_values("score", ascending=False)[["name", "score"]])
```

```text
    name  score
2   Mina     91
0    Ada     82
1  Kerem     74
3  Deniz     68
```

Index'e dikkat: `2, 0, 1, 3` sırasında. Satırlar yer değiştirdi ama
**etiketleri onlarla birlikte taşındı** — hangi satırın nereden geldiğini
kaybetmiyorsun.

## Index'i değiştirmek

Varsayılan index sayılar; ama bir sütunu index yapabiliyorsun:

```python
by_name = data.set_index("name")
print(by_name.loc["Mina", "score"])
```

```text
91
```

Artık satırı adıyla çağırıyorsun: `loc[satır, sütun]`.

Geri almak için `reset_index()`. Index seçimi bir sonraki bölümün ana
konusu; şimdilik bilmen gereken, index'in **satırların adı** olduğu.

## Sayısal özet

```python
print(data.describe())
```

```text
           score
count   4.000000
mean   78.750000
std     9.979145
min    68.000000
25%    72.500000
50%    78.000000
75%    84.250000
max    91.000000
```

`describe()` **yalnızca sayısal sütunları** alıyor; `name` ve `city`
çıktıda yok. Bu bilinçli: metin sütununun ortalaması diye bir şey yok.

Aynı sebeple toplulaştırma çağrılarında da söylemen gerekiyor:

```python
print(data.mean(numeric_only=True))
```

```text
score    78.75
dtype: float64
```

`numeric_only=True` demezsen metin sütunları yüzünden hata alıyorsun.

## Seri ile DataFrame

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">Seri</span><span class="anat-body">tek sütun + index. <code>mean()</code>, <code>value_counts()</code>, <code>str</code></span></div>
    <div class="anat-row"><span class="anat-label">DataFrame</span><span class="anat-body">çok sütun + ortak index. <code>shape</code>, <code>columns</code>, <code>describe()</code></span></div>
  </div>
</figure>

Bir DataFrame'den sütun çektiğinde seri alıyorsun; serinin üzerinde
öğrendiğin her şey burada da geçerli. DataFrame yeni bir dünya değil,
serilerin bir arada durduğu yer.

## Özet

- **DataFrame** = yan yana seriler + ortak index.
- Sözlükten kurulur: **anahtarlar sütun adı**.
- İlk dört bakış: `shape`, `columns`, `dtypes`, `head()`.
- `data["x"]` **seri**, `data[["x"]]` **DataFrame**. Fark tek bir köşeli
  parantez.
- Yeni sütun atamayla ekleniyor: `data["bonus"] = data["score"] + 5`.
- `drop`, `sort_values`, `set_index` — hepsi **yeni tablo** döndürüyor.
- `describe()` yalnızca sayısal sütunlara bakıyor; toplulaştırmalarda
  `numeric_only=True` gerekiyor.
- Metin sütunları pandas 3.0'da `str` tipinde; eski belgelerdeki `object`
  yerine bu geçti.
