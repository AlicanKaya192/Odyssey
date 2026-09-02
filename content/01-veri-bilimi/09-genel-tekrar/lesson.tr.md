# Genel Tekrar

Bu bölümde yeni bir şey öğrenmiyorsun. Öğrendiklerinin birbirine nasıl
bağlandığını görüyorsun.

Dokuz bölüm önce "veri bilimi nedir" diye soruyordun. Şimdi eline ham bir
tablo geldiğinde onu temizleyebiliyor, sorularını sorabiliyor, cevabı
grafiğe dökebiliyor ve — en önemlisi — verinin **söylemediği** şeyi
söylememeyi biliyorsun.

## Parçalar nasıl bağlanıyor?

<figure class="fig">
  <div class="flow">
    <span class="node"><b>NumPy</b><br>vektörel hesap</span>
    <span class="arrow">→</span>
    <span class="node"><b>Seri</b><br>etiketli veri</span>
    <span class="arrow">→</span>
    <span class="node"><b>DataFrame</b><br>tablo</span>
    <span class="arrow">→</span>
    <span class="node"><b>Seçim</b><br>ilgilendiğin kısım</span>
    <span class="arrow">→</span>
    <span class="node ok"><b>Grup</b><br>karşılaştırma</span>
  </div>
  <figcaption>Her adım bir öncekinin üstüne kuruluyor. DataFrame yan yana konmuş serilerden ibaret; seri de bir NumPy dizisi ve yanındaki etiketlerden.</figcaption>
</figure>

Temizleme, görselleştirme ve keşif bu zincirin üstünde duran işler:
temizlik zincire girmeden önce, grafik ve keşif zincirden çıktıktan sonra.

## Baştan sona bir analiz

Gerçek bir işin nasıl göründüğünü tek örnekte görelim. Elimizde ham bir
tablo var:

```python
import pandas as pd

raw = pd.DataFrame({
    "Name ": [" Ada", "Kerem", "Mina ", "Deniz", "Kerem"],
    "City": ["ankara", "Izmir ", "ANKARA", "Bursa", "Izmir "],
    "score": ["82", "74", "91", None, "74"],
    "hours": [10, 6, 12, 3, 6],
})
```

Bu tablo dört ayrı hastalık taşıyor. Hepsini önceki bölümlerde gördün.

### 1. Önce bak

```python
print(raw.shape)
print(raw.dtypes.astype(str).tolist())
```

```text
(5, 4)
['str', 'str', 'str', 'int64']
```

`score` sütunu `str`. Yani ortalama alamıyorsun — daha ilk adımda bir sorun
çıktı.

### 2. Sütun adları

```python
data = raw.copy()
data.columns = data.columns.str.strip().str.lower()
print(data.columns.tolist())
```

```text
['name', 'city', 'score', 'hours']
```

`"Name "` sonundaki boşluk yüzünden `data["name"]` çalışmıyordu. İlk
temizlenen şey her zaman sütun adları.

`copy()` de kasıtlı: ham veriyi elde tutmak, üç adım sonra bir hata fark
ettiğinde geri dönebilmek demek.

### 3. Metin ve tip

```python
data["name"] = data["name"].str.strip()
data["city"] = data["city"].str.strip().str.title()
data["score"] = pd.to_numeric(data["score"], errors="coerce")

print(data)
```

```text
    name    city  score  hours
0    Ada  Ankara   82.0     10
1  Kerem   Izmir   74.0      6
2   Mina  Ankara   91.0     12
3  Deniz   Bursa    NaN      3
4  Kerem   Izmir   74.0      6
```

`"ankara"`, `"Izmir "` ve `"ANKARA"` üç ayrı grup olacaktı; şimdi ikiye
indi. `to_numeric` ile `score` sayı oldu ve `None` düzgün bir `NaN`'a
dönüştü.

### 4. Tekrar ve eksik

```python
data = data.drop_duplicates()
print(len(data))
print(data.isna().sum().tolist())

data = data.dropna(subset=["score"])
print(len(data))
```

```text
4
[0, 0, 1, 0]
3
```

Kerem iki kez girilmişti, biri gitti. `score`'u boş olan Deniz de analiz
dışında kaldı.

**Bu bir karar**, sessiz bir adım değil: Deniz'in kaydı silindi ve bu
raporda yazılmalı. Beş kayıtlık veri üç kayda indi.

### 5. Sor

```python
print(data.groupby("city")["score"].agg(["count", "mean"]))
print(round(data["hours"].corr(data["score"]), 2))
```

```text
        count  mean
city
Ankara      2  86.5
Izmir       1  74.0
0.98
```

Ankara önde görünüyor. Ama `count` sütununa bak: 2 ve 1.

**Bu veriden şehir hakkında hiçbir sonuç çıkmıyor.** Korelasyon 0.98 de
üç kayıttan hesaplandı — üç noktadan geçen bir çizgi her zaman iyi uyuyor.

Analizin dürüst sonucu şu: *veri temizlendi, elde üç kullanılabilir kayıt
kaldı, bu sayıyla bir sonuç çıkarılamıyor.* Bu bir başarısızlık değil,
bulgunun kendisi.

## Bölüm bölüm ne öğrendin?

| Bölüm | Anahtar fikir |
|---|---|
| Veri Bilimi Nedir | Veri bilimi soru sormakla başlıyor, veriyle değil |
| NumPy | Döngü yerine vektörel işlem; dizi tek tip tutuyor |
| Seriler | Değerlerin yanına **etiket** geliyor; işlemler etikete göre hizalanıyor |
| DataFrame | Yan yana konmuş seriler; sütunlar farklı tiplerde olabiliyor |
| Seçim ve Filtreleme | `loc` etiketle, `iloc` sırayla; koşullar `&` ve <code>&#124;</code> ile |
| Gruplama | Böl, hesapla, birleştir — `agg` ile birden çok özet |
| Veri Temizleme | Adlar → metin → tip → tekrar → eksik |
| Görselleştirme | Bir grafik bir şey anlatıyor; eksen sıfırdan başlıyor |
| Keşifçi Analiz | Soru → bak → bulgu → yeni soru |

## En sık düşülen tuzaklar

Bu modülde defalarca karşına çıkan hatalar, tek listede:

| Tuzak | Doğrusu |
|---|---|
| `mean()`'i eksik değerlerle almak | Önce `isna().sum()` ile kaç tane olduğuna bakmak |
| Grup ortalamasını `count` olmadan okumak | `agg(["count", "mean"])` |
| Korelasyonu nedensellik sanmak | "Birlikte hareket ediyor" demek |
| Zincirleme atama (`data[...][...] = ...`) | `loc` ile tek adımda yazmak |
| Çubuk grafikte ekseni sıfırdan başlatmamak | `ax.set_ylim(0, ...)` |
| Aykırı değeri düşünmeden silmek | Önce "hata mı, gerçek mi" diye sormak |
| `inplace=True` beklentisiyle sonucu kaybetmek | Sonucu bir değişkene almak |
| Ham veriyi üzerine yazmak | `copy()` ve ayrı bir çıktı dosyası |

## Bir sonraki adım

Bu modül **bir veriyle çalışmayı** öğretti. Sırada tahmin var: geçmiş
veriye bakıp gelecek hakkında bir şey söylemek — makine öğrenmesi.

Ama oraya geçmeden önce bir şeyi bilmekte fayda var: **bir makine öğrenmesi
projesinin zamanının çoğu bu modülde öğrendiğin işlerle geçiyor.** Model
kurmak birkaç satır; veriyi anlamak, temizlemek ve doğru soruyu bulmak
haftalar.

Bu yüzden buradaki her bölüm oraya taşınıyor.

## Özet

- **NumPy → Seri → DataFrame** zinciri: her katman bir öncekinin üstünde.
- Gerçek bir analiz: bak → temizle → sor → göster → cümleye çevir.
- **Temizlik bir karar dizisi**, mekanik bir adım değil; ne yaptığın
  raporda yazılıyor.
- **Ham veri korunuyor**, kopyayla çalışılıyor.
- Grup ortalaması `count`'suz, korelasyon nedensellik iddiasıyla, grafik
  başlıksız okunmuyor.
- Bir analizin dürüst sonucu bazen **"bu veriyle bu soru cevaplanamıyor"**
  oluyor. Bunu söyleyebilmek, uydurmaktan iyidir.
