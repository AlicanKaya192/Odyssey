## `pd.to_datetime` parametreleri

| Parametre | Ne yapıyor | Ne zaman |
|---|---|---|
| `format="%d.%m.%Y"` | Biçimi açıkça söylüyor | Tarih ISO değilse **her zaman** |
| `dayfirst=True` | Belirsiz tarihte günü öne alıyor | Biçim tek değilse; `format` varken gereksiz |
| `errors="coerce"` | Okunamayanı `NaT` yapıyor | Bozuk satır beklendiğinde; sonra say |
| `errors="raise"` | Okunamayanda hata (varsayılan) | Verinin temiz olması gerekiyorsa |
| `utc=True` | Sonucu UTC dilimli yapıyor | Farklı farklar karışık geliyorsa, Unix zamanında |
| `unit="s"` / `"ms"` | Sayıyı Unix zamanı olarak okuyor | Sütun sayıysa |
| `format="ISO8601"` | ISO'nun her türünü kabul ediyor | Bazı satırda saat var, bazısında yok |
| `format="mixed"` | Her satırın biçimini ayrı tahmin ediyor | Son çare; aşağıdaki uyarıya bak |

## `format="mixed"` uyarısı

Her satır ayrı tahmin edildiği için yavaş ve **güvenilmez**. `dayfirst=True`
ile birlikte ISO tarihi bile çeviriyor:

```python
pd.to_datetime(pd.Series(["2024-03-09", "09.03.2024"]),
               format="mixed", dayfirst=True)
# 2024-09-03, 2024-03-09    ISO olan satir yanlis okundu
```

Karışık biçimli bir sütunda daha güvenli yol, satırları biçimine göre ayırıp
her grubu kendi `format`'ıyla okumak:

```python
iso = dates.str.match(r"\d{4}-\d{2}-\d{2}")
result = pd.Series(pd.NaT, index=dates.index)
result[iso] = pd.to_datetime(dates[iso], format="%Y-%m-%d")
result[~iso] = pd.to_datetime(dates[~iso], format="%d.%m.%Y")
```

## Dosyayı okurken

```python
pd.read_csv("f.csv", parse_dates=["date"])                       # ISO sutun
pd.read_csv("f.csv", parse_dates=["date"], date_format="%d.%m.%Y")   # bicimli
pd.read_csv("f.csv", parse_dates=["date"], index_col="date")     # dogrudan indeks
```

`read_csv` okuyamazsa **hata vermiyor**, sütunu metin bırakıyor. Okuduktan
sonra `df.dtypes`.

## Çevirmeden sonra kontrol listesi

```python
df["date"].dtype                 # datetime64[...] mi?
df["date"].isna().sum()          # kac NaT?
df["date"].min(), df["date"].max()   # aralik mantikli mi?
df["date"].dt.month.value_counts().sort_index()   # aylar dengeli mi?
df["date"].is_monotonic_increasing   # sirali mi?
df["date"].duplicated().sum()    # tekrar eden var mi?
```

Aylara bakmak gün-ay karışıklığını ele veriyor: gerçek veri dört aya
yayılmışken sonuç on iki aya dağılmışsa gün ile ay yer değiştirmiş demek.

## `NaT` ile çalışmak

| İşlem | Sonuç |
|---|---|
| `pd.NaT == pd.NaT` | `False` |
| `pd.NaT > pd.Timestamp("2024-01-01")` | `False` |
| `pd.isna(pd.NaT)` | `True` |
| `s.min()`, `s.max()`, `s.mean()` | `NaT` atlanıyor |
| tarih - `NaT` | `NaT` |
| `s.dt.month` (NaT satırı) | `NaN`; sütun ondalıklı oluyor |

Son satır sık şaşırtıyor: `NaT` içeren bir sütunda `dt.month` `3.0` gibi
ondalıklı sayılar veriyor. `dropna()` sonrası tam sayıya dönüyor.

## Yazarken

```python
df.to_csv("out.csv", index=False)                          # ISO yaziyor
df.to_csv("out.csv", index=False, date_format="%Y-%m-%d")  # saatsiz
df["date"].dt.strftime("%d.%m.%Y")                         # metne (rapor icin)
```

`strftime` sonucu **metindir**; ondan sonra tarih işlemi yapılamıyor. Rapora
yazmadan hemen önce, en son adım olarak kullan.
