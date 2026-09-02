# Veri Temizleme

İlk bölümde şöyle demiştik: **zamanın büyük kısmı ortadaki iki kutuda
geçiyor.** Bu bölüm o kutulardan ikincisi.

Gerçek veri temiz gelmiyor. Sütun adlarında boşluk, aynı şehrin üç farklı
yazımı, sayı olması gereken sütunda metin, tekrar eden satırlar, boş
hücreler. "Temiz veri" diye bir şey yok; **temizlenmiş veri** var.

Bu bölümün örnekleri şu tabloyla çalışıyor — bilerek berbat:

```python
raw = pd.DataFrame({
    " Name ": [" Ada ", "kerem", "MINA", "Ada ", "Deniz"],
    "city": ["Ankara", "izmir ", "ANKARA", "Ankara", None],
    "score": ["82", "74", None, "82", "abc"],
})
```

Beş satırda beş ayrı sorun var. Sırayla çözeceğiz.

## Önce bak, sonra dokun

```python
print(raw.shape)
print(list(raw.columns))
print(raw.dtypes)
print(raw.isna().sum())
```

```text
(5, 3)
[' Name ', 'city', 'score']
Name      str
city      str
score     str
dtype: object
 Name     0
city      1
score     1
dtype: int64
```

Daha ilk bakışta iki sorun görünüyor: sütun adı `" Name "` (başında ve
sonunda boşluk) ve `score` sütunu **metin** tipinde — sayı olması gerekirken.

`info()` de aynı bilgiyi tek ekranda veriyor. Bir veriyi açtığında ilk
yazılan şey bu.

## 1. Sütun adları

```python
data = raw.copy()
data.columns = data.columns.str.strip().str.lower()
print(list(data.columns))
```

```text
['name', 'city', 'score']
```

`" Name "` ile `"name"` farklı iki ad; ekranda ikisi de aynı görünüyor ve
`data["name"]` yazınca `KeyError` alıyorsun — sebebi görünmüyor.

Bu yüzden **ilk iş sütun adlarını temizlemek** oluyor: boşlukları at, hepsini
küçük harfe çevir. Sonrasında ne yazacağını düşünmek zorunda kalmıyorsun.

## 2. Metin sütunları

```python
data["name"] = data["name"].str.strip().str.title()
data["city"] = data["city"].str.strip().str.title()
print(data[["name", "city"]])
```

```text
    name    city
0    Ada  Ankara
1  Kerem   Izmir
2   Mina  Ankara
3    Ada  Ankara
4  Deniz     NaN
```

`"izmir "`, `"ANKARA"` ve `"Ankara"` artık tek bir yazıma indi. Bunu
yapmadan gruplarsan **üç ayrı şehir** çıkıyor.

- `str.strip()` baştaki ve sondaki boşlukları atıyor.
- `str.title()` her kelimenin ilk harfini büyütüyor.
- `str.lower()` / `str.upper()` de var; hangisini seçtiğin önemli değil,
  **tutarlı olman** önemli.

Eksik değer (`None`) olduğu gibi kalıyor — `str` metotları onlara
dokunmuyor.

## 3. Tipleri düzeltmek

```python
data["score"] = pd.to_numeric(data["score"], errors="coerce")
print(data["score"].tolist())
print(data["score"].dtype)
```

```text
[82.0, 74.0, nan, 82.0, nan]
float64
```

`"abc"` sayıya çevrilemedi ve `NaN` oldu. `errors="coerce"` tam olarak bunu
söylüyor: **çeviremediğini patlatma, boş bırak.**

`astype(int)` deneseydin bütün program hata verirdi. `to_numeric` sorunu
tek bir hücreye hapsediyor ve sen sonra o hücreyle ne yapacağına karar
ediyorsun.

Sonucun `float64` olduğuna dikkat: tamsayı tipi `NaN` tutamıyor.

## 4. Eksik değerler

```python
print(data.isna().sum())
```

```text
name     0
city     1
score    2
dtype: int64
```

Artık iki eksik not var — biri baştan boştu, biri `"abc"` yüzünden oluştu.

Üç seçeneğin var ve **hiçbiri her zaman doğru değil**:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">Atmak</span><span class="anat-body"><code>dropna()</code> — kaydı tamamen kaybediyorsun. Az sayıdaysa makul</span></div>
    <div class="anat-row"><span class="anat-label">Doldurmak</span><span class="anat-body"><code>fillna(ortalama)</code> — kayıt kalıyor ama uydurma bir değerle</span></div>
    <div class="anat-row"><span class="anat-label">Bırakmak</span><span class="anat-body">Hesaplar zaten atlıyor; ama kaç tane olduğunu bilmen gerekiyor</span></div>
  </div>
</figure>

```python
print(data.dropna().shape)
print(data.dropna(subset=["score"]).shape)
print(data["score"].fillna(data["score"].mean()).round(1).tolist())
```

```text
(3, 3)
(3, 3)
[82.0, 74.0, 79.3, 82.0, 79.3]
```

`dropna()` **herhangi bir** sütunu boş olan satırı atıyor — çok agresif.
`dropna(subset=["score"])` yalnızca ilgilendiğin sütuna bakıyor; genelde
istediğin bu.

Ortalamayla doldurmak ortalamayı değiştirmiyor ama **yayılımı azaltıyor**:
veriyi olduğundan daha uyumlu gösteriyor. Karar senin ve raporunda bunu
söylemen gerekiyor.

## 5. Tekrar eden satırlar

```python
print(data.duplicated().sum())
print(data.drop_duplicates(subset=["name"]).shape)
```

```text
1
(4, 3)
```

`Ada` iki kez var. `duplicated()` **ikinci ve sonraki** kopyaları işaretliyor;
ilki tutuluyor.

`subset` vermezsen bütün sütunların aynı olması gerekiyor. Gerçek veride
genelde bir kimlik sütununa bakılıyor: aynı öğrenci numarası iki kez
girilmişse notlar farklı olsa bile o bir tekrar.

`keep="last"` ile son kaydı tutabiliyorsun — güncellenmiş kaydı korumak
istediğinde.

## 6. Aykırı değerler

```python
scores = pd.Series([10, 12, 11, 13, 100])
q1 = scores.quantile(0.25)
q3 = scores.quantile(0.75)
iqr = q3 - q1

print(q1, q3, iqr)
print(scores[(scores < q1 - 1.5 * iqr) | (scores > q3 + 1.5 * iqr)].tolist())
```

```text
11.0 13.0 2.0
[100]
```

**IQR yöntemi:** çeyrekler arası açıklığın 1.5 katından uzaktakiler aykırı
sayılıyor. Yaygın, basit ve çoğu durumda yeterli bir kural.

Aykırı değer bulunca ne yapılır? **Önce sebebini sor.** 100 gerçek bir not
mu, yoksa 10 yazılırken fazladan sıfır mı basıldı? Sebebini bilmeden silmek
veriyi güzelleştirmek olur, temizlemek değil.

Sınırlamak için `clip` var:

```python
print(pd.Series([-5, 50, 150]).clip(0, 100).tolist())
```

```text
[0, 50, 100]
```

## Sırayla

Temizlik adımlarının sırası önemli:

<figure class="fig">
  <div class="flow">
    <span class="node acc"><b>Bak</b><br>shape, dtypes, isna</span>
    <span class="arrow">→</span>
    <span class="node"><b>Adlar</b><br>sütun adlarını düzelt</span>
    <span class="arrow">→</span>
    <span class="node"><b>Metin</b><br>boşluk ve harf</span>
    <span class="arrow">→</span>
    <span class="node"><b>Tip</b><br>sayıya çevir</span>
    <span class="arrow">→</span>
    <span class="node"><b>Tekrar</b><br>kopyaları at</span>
    <span class="arrow">→</span>
    <span class="node ok"><b>Eksik</b><br>karar ver</span>
  </div>
  <figcaption>Metni tipten önce temizliyorsun: " 82 " metni sayıya çevrilebiliyor ama tutarsız yazımlar tip dönüşümünden sonra düzeltilemiyor.</figcaption>
</figure>

Eksik değerleri **en sona** bırakmanın sebebi şu: tip dönüşümü yeni eksikler
üretiyor (`"abc"` → `NaN`). Önce doldurup sonra çevirirsen o hücreleri
kaçırıyorsun.

## Temizlik geri alınamaz

Bütün bu adımlar veriyi **değiştiriyor**. Ham veriyi kaybetmemek için
kopyayla çalışmak iyi bir alışkanlık:

```python
data = raw.copy()
```

Bir de dosyayı asla üzerine yazma: `temiz.csv` diye ayrı bir dosyaya yaz.
Temizlik adımlarında bir hata olduğunu üç gün sonra fark ediyorsun ve ham
veriye dönmen gerekiyor.

## Özet

- **Önce bak:** `shape`, `dtypes`, `isna().sum()`, `head()`.
- **Sütun adları** ilk temizlenen şey: `str.strip().str.lower()`.
- **Metin sütunlarında** boşluk ve harf tutarsızlığı gruplamayı bozuyor.
- **`pd.to_numeric(..., errors="coerce")`** çeviremediğini `NaN` yapıyor,
  programı durdurmuyor.
- **Eksik değerde üç seçenek var** ve hiçbiri her zaman doğru değil; kararı
  raporunda söylemen gerekiyor.
- `dropna(subset=[...])` genelde çıplak `dropna()`'dan iyi.
- **Tekrar** `duplicated` ve `drop_duplicates(subset=...)` ile bulunuyor.
- **Aykırı değeri silmeden önce sebebini sor.**
- Sıra önemli: adlar → metin → tip → tekrar → eksik.
- Ham veriyi sakla, kopyayla çalış.
