# Temizlik Tuzakları

## 1. `dropna()` düşündüğünden çok satır atıyor

```python
d = pd.DataFrame({"a": [1, None, 3], "b": [None, 2, 3]})
print(d.dropna().shape)
print(d.dropna(subset=["a"]).shape)
```

```text
(1, 2)
(2, 2)
```

Çıplak `dropna()` **herhangi bir** sütunu boş olan satırı atıyor. Üç
satırdan biri kaldı.

Yirmi sütunlu bir tabloda bu, verinin yarısını kaybetmek demek — hem de
ilgilenmediğin sütunlar yüzünden.

**Doğrusu:** hangi sütunun dolu olması gerektiğini söyle.

```python
data.dropna(subset=["score"])
```

## 2. Sıfırla doldurmak ortalamayı bozuyor

```python
s = pd.Series([1.0, None, 3.0])
print(s.mean())
print(s.fillna(0).mean())
```

```text
2.0
1.3333333333333333
```

Eksik değeri sıfır saymak "ölçüm sıfırdı" demek. Ortalama düşüyor ve veri
olduğundan kötü görünüyor.

Sıfır **gerçekten** doğru cevapsa (satış yok = 0 satış) doldur. "Bilinmiyor"
demekse doldurma ya da ortalamayla doldur.

## 3. Ortalama ile doldurmak yayılımı azaltıyor

Ortalamayla doldurmak ortalamayı korumuyor mu? Koruyor. Ama **standart
sapmayı düşürüyor**: eklediğin her değer tam ortada duruyor ve veri
olduğundan daha uyumlu görünüyor.

Az sayıda eksikte sorun değil; çoksa modelin ya da raporun yanıltıcı
oluyor.

Uç değer varsa **medyanla** doldurmak daha güvenli:

```python
s = pd.Series([1, 2, 3, 100])
print(s.mean())      # 26.5
print(s.median())    # 2.5
```

## 4. `astype(int)` eksik değerle çalışmıyor

```python
pd.Series([1.0, None]).astype(int)
```

```text
IntCastingNaNError
```

Tamsayı tipi `NaN` tutamıyor. Önce boşlukları halletmen gerekiyor:

```python
s.fillna(0).astype(int)
s.dropna().astype(int)
```

Bir de `astype(int)` **kırpıyor**, yuvarlamıyor: `1.9` → `1`. Yuvarlamak
istiyorsan önce `round()`.

## 5. `to_numeric` olmadan tek bir bozuk hücre programı durduruyor

```python
data["score"].astype(float)     # "abc" varsa ValueError
pd.to_numeric(data["score"], errors="coerce")   # "abc" -> NaN
```

Gerçek veride her zaman bir bozuk hücre oluyor. `errors="coerce"` sorunu tek
bir hücreye hapsediyor.

Sonrasında kaç tane bozulduğunu görebiliyorsun:

```python
temiz = pd.to_numeric(data["score"], errors="coerce")
print(temiz.isna().sum() - data["score"].isna().sum())
```

Aynı argüman `pd.to_datetime` için de var.

## 6. Sahte eksik değerler

Gerçek veride "eksik" çoğu zaman `NaN` değil: `-1`, `0`, `999`,
`"bilinmiyor"`, `"N/A"`, boş metin.

```python
print(pd.Series([1, -1, 3]).mean())    # 1.0 -- yanlis
```

`-1` "bilinmiyor" demekse ortalamaya karışıyor ve sonucu bozuyor.

**İlk işlerden biri** bunları gerçek `NaN`'a çevirmek:

```python
data["score"] = data["score"].replace(-1, np.nan)
data["city"] = data["city"].replace(["", "N/A", "bilinmiyor"], np.nan)
```

`isna().sum()` sıfır çıkıyor diye veri temiz sanma; önce hangi değerlerin
"eksik" anlamına geldiğine bak.

## 7. Metin temizlemeden gruplamak

```python
data.groupby("city").size()
```

`"Ankara"`, `"ankara"` ve `"Ankara "` **üç ayrı grup** oluyor. Sayılar
bölünüyor ve hiçbiri doğru olmuyor.

Gruplamadan önce:

```python
data["city"] = data["city"].str.strip().str.title()
```

Kontrol etmenin yolu: `data["city"].nunique()` beklediğinden büyükse
tutarsız yazım var demektir.

## 8. `str` metotları `.str` olmadan çalışmıyor

```python
data["city"].lower()        # AttributeError
data["city"].str.lower()    # dogru
```

`data["city"]` bir metin değil, **metinlerden oluşan bir seri**.

Aynı yapı tarihlerde `.dt`, kategorilerde `.cat` olarak var.

## 9. Sütun adındaki görünmez boşluk

```python
list(pd.DataFrame({" a ": [1]}).columns)
```

```text
[' a ']
```

Ekranda `a` görünüyor ama gerçek ad `" a "`. `data["a"]` yazınca `KeyError`
alıyorsun ve sebebini göremiyorsun.

**İlk iş:**

```python
data.columns = data.columns.str.strip().str.lower()
```

## 10. `drop_duplicates` hangisini tutuyor?

```python
pd.DataFrame({"a": [1, 1, 2]}).drop_duplicates().index.tolist()
```

```text
[0, 2]
```

Varsayılan olarak **ilk** kayıt tutuluyor. Güncellenmiş kaydı korumak
istiyorsan `keep="last"` demen gerekiyor.

Hangisinin doğru olduğu veriye bağlı: tarih sırasıyla gelen bir kayıtta
genelde sonuncusu güncel olanı.

Silmeden önce bakmak iyi bir alışkanlık:

```python
data[data.duplicated(keep=False)]   # tekrarlarin hepsini gosterir
```

## 11. `duplicated()` bütün sütunlara bakıyor

```python
data.duplicated()                    # butun sutunlar ayni olmali
data.duplicated(subset=["id"])       # yalnizca kimlik
```

Aynı öğrenci iki kez girilmiş ama notlardan biri farklıysa çıplak
`duplicated()` bunu tekrar saymıyor.

Gerçek veride genelde bir **kimlik sütununa** bakılıyor: aynı numara iki
kez varsa diğer sütunlar farklı olsa bile o bir tekrar.

## 12. Aykırı değeri sebebini bilmeden silmek

Aykırı değer bulduğunda soru şu: **gerçek bir uç değer mi, giriş hatası mı?**

- 100 puanlık bir sınavda 1000 → giriş hatası, düzelt ya da at.
- Maaş listesinde 900 bin → gerçek olabilir; CEO da bir çalışan.

Sebebini bilmeden silmek veriyi **güzelleştirmek** oluyor, temizlemek değil.
Ve sildiğini raporunda söylemen gerekiyor.

`clip` bir orta yol: kaydı kaybetmeden değeri sınıra çekiyor.

## 13. Temizliği ham dosyanın üzerine yazmak

```python
data.to_csv("veri.csv", index=False)    # ham veri gitti
data.to_csv("temiz.csv", index=False)   # dogrusu
```

Temizlik adımlarındaki bir hatayı günler sonra fark ediyorsun. Ham veri
duruyorsa baştan başlıyorsun; yoksa yapacak bir şey yok.

Aynı sebeple bellekte de kopyayla çalış: `data = raw.copy()`.
