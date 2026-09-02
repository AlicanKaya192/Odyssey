# Seçim ve Filtreleme

Bir tablon var ve ondan **bir parça** istiyorsun: belli satırlar, belli
sütunlar, ya da bir koşula uyanlar. Veri işlerinin en sık yaptığı iş bu.

pandas'ta üç yol var ve üçünü ayırt etmek gerekiyor: **`iloc`** (sıra),
**`loc`** (etiket) ve **koşul**.

Bu bölümün örneklerinde şu tablo kullanılıyor:

```python
data = pd.DataFrame({
    "name": ["Ada", "Kerem", "Mina", "Deniz", "Efe", "Sila"],
    "city": ["Ankara", "Izmir", "Ankara", "Bursa", "Ankara", "Izmir"],
    "score": [82, 74, 91, 68, 88, 76],
    "age": [21, 23, 22, 25, 21, 24],
})
```

## iloc: sıraya göre

`iloc` **konum** kullanıyor — tıpkı bir listedeki gibi, sıfırdan başlayarak.

```python
print(data.iloc[0, 2])
print(data.iloc[1:3])
```

```text
82
    name    city  score  age
1  Kerem   Izmir     74   23
2   Mina  Ankara     91   22
```

`iloc[satır, sütun]` — virgülün solu satır, sağı sütun. Dilim alırken
**bitiş dâhil değil**, Python kuralı geçerli: `1:3` iki satır veriyor.

Sütunları da sırayla seçebiliyorsun:

```python
print(data.iloc[:, [0, 2]].head(2))
```

```text
    name  score
0    Ada     82
1  Kerem     74
```

`:` "bütün satırlar" demek.

## loc: etikete göre

`loc` **etiket** kullanıyor. Index sayıysa satır numarasına benziyor ama
aslında etiketle çalışıyor. Farkı görmek için index'i adlara çevirelim:

```python
by_name = data.set_index("name")

print(by_name.loc["Mina", "score"])
print(by_name.loc["Ada":"Mina"])
```

```text
91
         city  score  age
name                     
Ada    Ankara     82   21
Kerem   Izmir     74   23
Mina   Ankara     91   22
```

**Dikkat: `loc` dilimlerinde bitiş dâhil.** `"Ada":"Mina"` üç satır
veriyor, Mina da içeride.

Bu, Python'dan ayrıldığı yer ve şaşırtıyor. Sebebi mantıklı: etiketlerle
çalışırken "Mina'dan bir önceki" demek anlamsız — etiketlerin sayısal bir
sırası olmayabiliyor.

<figure class="fig">
  <div class="versus">
    <div class="versus-side">
      <h4>iloc[1:3]</h4>
      <p>Konum. <b>Bitiş hariç</b> — iki satır. Python dilimi gibi.</p>
    </div>
    <div class="versus-side">
      <h4>loc["a":"c"]</h4>
      <p>Etiket. <b>Bitiş dâhil</b> — üç satır. Etiketlerde "bir öncesi" tanımlı değil.</p>
    </div>
  </div>
</figure>

## Koşulla filtreleme

En çok kullanacağın yol bu. Bir karşılaştırma `True`/`False` sütunu
üretiyor; onu köşeli parantezin içine koyunca satırlar süzülüyor:

```python
print(data[data["score"] >= 80])
```

```text
   name    city  score  age
0   Ada  Ankara     82   21
2  Mina  Ankara     91   22
4   Efe  Ankara     88   21
```

Index'e dikkat: `0, 2, 4`. Seçilmeyen satırların numaraları **atlanıyor**,
yeniden numaralanmıyor. Filtre sonrası delikli index normal.

## Birden fazla koşul

`&` (ve), `|` (veya), `~` (değil). **Her koşul parantez içinde.**

```python
print(data[(data["score"] >= 80) & (data["city"] == "Ankara")])
```

```text
   name    city  score  age
0   Ada  Ankara     82   21
2  Mina  Ankara     91   22
4   Efe  Ankara     88   21
```

`and` / `or` **çalışmıyor** — NumPy'daki sebebin aynısı: elinde tek bir
doğruluk değeri değil, satır sayısı kadar var.

Parantezi unutmak daha sinsi: `&` karşılaştırmadan önce çalışıyor ve hata
vermeden bambaşka bir şey hesaplıyor.

## Hazır yardımcılar

Uzun koşulları kısaltan üç metot:

```python
print(data[data["city"].isin(["Izmir", "Bursa"])][["name", "city"]])
print(data[data["age"].between(21, 22)][["name", "age"]])
print(data[data["name"].str.contains("a")][["name"]])
```

```text
    name   city
1  Kerem  Izmir
3  Deniz  Bursa
5   Sila  Izmir
   name  age
0   Ada   21
2  Mina   22
4   Efe   21
   name
0   Ada
2  Mina
5  Sila
```

- `isin` — birçok değeri `|` ile bağlamanın kısa yolu.
- `between` — iki uç **dâhil**.
- `str.contains` — metinde arama; `.str` olmadan çalışmıyor.

Tersini almak için başına `~`:

```python
print(data[~data["city"].isin(["Ankara"])][["name", "city"]])
```

```text
    name   city
1  Kerem  Izmir
3  Deniz  Bursa
5   Sila  Izmir
```

## query: koşulu metin olarak yazmak

Uzun koşullar okunmaz hâle geldiğinde:

```python
print(data.query("score > 80 and city == 'Ankara'"))
```

```text
   name    city  score  age
0   Ada  Ankara     82   21
2  Mina  Ankara     91   22
4   Efe  Ankara     88   21
```

`query` içinde `and` / `or` **çalışıyor**, çünkü orası Python değil,
pandas'ın kendi küçük dili. Sütun adlarını tırnaksız yazıyorsun.

İşe yaradığı yer: üç dört koşullu ifadeler. Az koşulda normal yazım daha
açık.

## En büyükler

```python
print(data.nlargest(2, "score")[["name", "score"]])
```

```text
   name  score
2  Mina     91
4   Efe     88
```

`sort_values(...).head(2)` ile aynı sonuç ama tek çağrı ve büyük veride daha
hızlı: hepsini sıralamak yerine yalnızca en büyük ikiyi buluyor.

## Filtreye göre değer değiştirmek

**Burada dikkatli olman gerekiyor.** Seçip sonra atamak işe yaramıyor:

```python
data[data["score"] < 75]["score"] = 0     # HICBIR SEY OLMAZ
```

Doğrusu tek adımda `loc` ile — solda satır koşulu, sağda sütun:

```python
data.loc[data["score"] < 75, "score"] = 0
print(data[["name", "score"]])
```

```text
    name  score
0    Ada     82
1  Kerem      0
2   Mina     91
3  Deniz      0
4    Efe     88
5   Sila     76
```

**Kural:** tabloyu değiştirecekseniz köşeli parantezi iki kez üst üste
kullanmayın. Seçim ve atama tek bir `loc` çağrısında olmalı.

## Hangisini ne zaman?

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">iloc</span><span class="anat-body">"ilk satır", "son üç satır" — sıra gerçekten önemliyse</span></div>
    <div class="anat-row"><span class="anat-label">loc</span><span class="anat-body">etiket anlamlıysa (ad, tarih, ürün kodu) ve <b>atama yaparken</b></span></div>
    <div class="anat-row"><span class="anat-label">koşul</span><span class="anat-body">"notu 80'in üstünde olanlar" — en sık kullanılan</span></div>
  </div>
</figure>

Pratikte %80 koşullu filtreleme, %15 `loc`, %5 `iloc` kullanıyorsun.

## Özet

- **`iloc`** sıraya bakıyor, **bitiş hariç**.
- **`loc`** etikete bakıyor, **bitiş dâhil**. Bu Python kuralından ayrılıyor.
- Koşullu filtreleme en yaygın yol; sonuç **delikli index** bırakıyor.
- Koşulları `&`, `|`, `~` ile birleştir ve **parantezi unutma**. `and`
  çalışmıyor.
- `isin`, `between`, `str.contains` uzun koşulları kısaltıyor.
- `query` içinde `and`/`or` çalışıyor; çok koşullu ifadelerde okunaklı.
- **Değer değiştirirken her zaman tek bir `loc` çağrısı.** Zincirli atama
  sessizce hiçbir şey yapmıyor.
