# Temizlik Başvurusu

## Keşif

| Yazım | Ne gösterir |
|---|---|
| `data.shape` | Kaç satır, kaç sütun |
| `data.info()` | Sütun, tip, dolu sayısı — tek ekranda |
| `data.dtypes` | Sütun tipleri |
| `data.head()` / `data.sample(5)` | Veriye ilk bakış |
| `data.isna().sum()` | Sütun başına eksik sayısı |
| `data.duplicated().sum()` | Kaç tekrar eden satır |
| `data.nunique()` | Sütun başına farklı değer |
| `data.describe()` | Sayısal özet |
| `data.describe(include="all")` | Metin sütunları da dâhil |

`info()` ve `isna().sum()` bir veriyi açtığında yazılan ilk iki şey.

## Sütun adları

| Yazım | Ne yapar |
|---|---|
| `data.columns = data.columns.str.strip()` | Baştaki/sondaki boşlukları atar |
| `data.columns = data.columns.str.lower()` | Küçük harfe çevirir |
| `data.columns = data.columns.str.replace(" ", "_")` | Boşlukları alt çizgi yapar |
| `data.rename(columns={"eski": "yeni"})` | Tek tek yeniden adlandırır |
| `data.columns.duplicated().any()` | Aynı adlı sütun var mı |

Zincirlenebiliyor: `data.columns.str.strip().str.lower()`.

## Metin temizliği

| Yazım | Ne yapar |
|---|---|
| `s.str.strip()` | Baştaki ve sondaki boşluklar |
| `s.str.lower()` / `s.str.upper()` / `s.str.title()` | Harf düzeni |
| `s.str.replace("-", " ")` | Değiştirir |
| `s.str.replace(r"\s+", " ", regex=True)` | Çoklu boşluğu teke indirir |
| `s.str.contains("An")` | İçeriyor mu |
| `s.str.startswith("A")` | Baştan eşleşme |
| `s.str.len()` | Uzunluk |
| `s.str.split(",")` | Böler |
| `s.str.extract(r"(\d+)")` | Desene uyan parçayı çıkarır |

`.str` olmadan çalışmıyor. Eksik değerlere dokunmuyor.

## Tip dönüşümü

| Yazım | Ne yapar |
|---|---|
| `pd.to_numeric(s, errors="coerce")` | Çevrilemeyeni `NaN` yapar |
| `pd.to_datetime(s, errors="coerce")` | Tarihe çevirir |
| `s.astype(int)` | Tamsayıya **kırpar** — eksik varsa hata verir |
| `s.astype(float)` | Ondalığa çevirir |
| `s.astype(str)` | Metne çevirir |
| `s.round(2).astype(int)` | Önce yuvarla, sonra çevir |

`errors="coerce"` temizlik işlerinin en çok kullanılan argümanı: bozuk
değerleri programı durdurmadan işaretliyor.

## Eksik değerler

| Yazım | Ne yapar |
|---|---|
| `data.isna().sum()` | Sütun başına sayı |
| `data.isna().sum().sum()` | Tablo geneli |
| `data.isna().mean()` | Sütun başına **oran** |
| `data.dropna()` | Herhangi bir sütunu boş olan satırları atar |
| `data.dropna(subset=["score"])` | Yalnızca o sütuna bakar |
| `data.dropna(axis=1)` | Boş içeren **sütunları** atar |
| `data.dropna(thresh=3)` | En az üç dolu hücresi olanları tutar |
| `data.fillna(0)` | Hepsini doldurur |
| `data.fillna({"score": 0, "city": "Bilinmiyor"})` | Sütun sütun farklı değer |
| `s.fillna(s.mean())` | Ortalamayla |
| `s.fillna(s.median())` | Medyanla — uç değer varsa daha güvenli |
| `s.ffill()` / `s.bfill()` | Bir üstteki / alttaki değerle |

`isna().mean()` oran verdiği için karar vermeyi kolaylaştırıyor: %2 eksikse
atmak makul, %60 eksikse sütunu tamamen sorgulamak gerekiyor.

## Tekrar eden satırlar

| Yazım | Ne yapar |
|---|---|
| `data.duplicated()` | İkinci ve sonraki kopyaları işaretler |
| `data.duplicated().sum()` | Kaç tane |
| `data.duplicated(subset=["id"])` | Yalnızca o sütuna bakar |
| `data.drop_duplicates()` | İlkini tutar |
| `data.drop_duplicates(keep="last")` | Sonuncuyu tutar |
| `data.drop_duplicates(subset=["id"], keep="last")` | Kimliğe göre, güncel olanı |
| `data[data.duplicated(keep=False)]` | Tekrarların **hepsini** gösterir |

Son satır incelemek için: silmeden önce hangi kayıtların tekrar ettiğine
bakmak iyi bir alışkanlık.

## Değer düzeltme

| Yazım | Ne yapar |
|---|---|
| `s.replace({"evet": 1, "hayir": 0})` | Sözlükle değiştirir |
| `s.replace(-1, np.nan)` | Sahte eksik değerleri gerçek `NaN` yapar |
| `s.map({"a": 1, "b": 2})` | Değiştirir; eşleşmeyen `NaN` olur |
| `s.clip(0, 100)` | Sınırların dışını kırpar |
| `data.loc[maske, "sutun"] = deger` | Koşula göre atama |

`-1`, `999`, `"bilinmiyor"` gibi değerler genelde "eksik" demek. Onları
gerçek `NaN`'a çevirmek ilk işlerden biri — yoksa ortalamaya karışıyorlar.

## Aykırı değerler

```python
q1 = s.quantile(0.25)
q3 = s.quantile(0.75)
iqr = q3 - q1

alt = q1 - 1.5 * iqr
ust = q3 + 1.5 * iqr

aykiri = s[(s < alt) | (s > ust)]
temiz = s[(s >= alt) & (s <= ust)]
```

| Yol | Ne zaman |
|---|---|
| IQR (yukarıdaki) | Genel amaçlı, dağılım varsayımı yok |
| `s.clip(alt, ust)` | Değeri sınıra çekmek, kaydı kaybetmemek |
| Elle sınır | Alan bilgisi varsa (not 0-100, yaş 0-120) |

Aykırı değeri silmeden önce **sebebini sormak** gerekiyor: gerçek bir uç
değer mi, giriş hatası mı?

## Kaydetme

| Yazım | Ne yapar |
|---|---|
| `data.to_csv("temiz.csv", index=False)` | Temiz hâli ayrı dosyaya |
| `raw.copy()` | Ham veriyi bozmadan çalışmak |

**Ham dosyanın üzerine asla yazma.** Temizlik adımlarındaki bir hatayı
günler sonra fark ediyorsun.
