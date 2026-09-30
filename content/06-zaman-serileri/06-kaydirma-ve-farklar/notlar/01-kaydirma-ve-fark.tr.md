## Dört araç

| Araç | Eşdeğeri | Verdiği |
|---|---|---|
| `s.shift(k)` | — | k satır önceki değer |
| `s.diff(k)` | `s - s.shift(k)` | Mutlak fark |
| `s.pct_change(k)` | `s / s.shift(k) - 1` | Oransal değişim (0.05 = %5) |
| `s.cumsum()` | — | Baştan bugüne toplam |
| `s.cumprod()` | — | Baştan bugüne çarpım |
| `s.cummax()`, `s.cummin()` | — | Bugüne kadarki en yüksek / en düşük |

`k` verilmezse 1. Hepsi **satır** sayıyor; takvim günü değil.

## Hangi `k`?

| Veri | Dün | Geçen haftanın aynı günü | Geçen yıl |
|---|---|---|---|
| Saatlik | `24` | `168` | `8736` (52 hafta) |
| Günlük | `1` | `7` | `364` |
| İş günü | `1` | `5` | yaklaşık `252` |
| Haftalık | — | `1` | `52` |
| Aylık | — | — | `12` |
| Çeyreklik | — | — | `4` |

## Değişimin adları

| Ad | Kısaltma | Neyi gösterir |
|---|---|---|
| Günden güne | DoD | Çoğunlukla haftalık deseni |
| Haftadan haftaya | WoW | Kısa vadeli değişim; haftalık desen dışarıda |
| Aydan aya | MoM | Mevsimselliği içerir; ay uzunluğundan etkilenir |
| Çeyrekten çeyreğe | QoQ | Mevsimselliği içerir |
| Yıldan yıla | YoY | Mevsimsellik dışarıda; trendi gösterir |
| Yıl başından bugüne | YTD | Birikim; `cumsum` |

## Yüzde ve yüzde puan

Bir oran %10'dan %12'ye çıkarsa:

- **2 yüzde puan** arttı (12 - 10).
- **Yüzde 20** arttı (12 / 10 - 1).

"Yüzde 2 arttı" demek yanlış. Oran serilerinde (dönüşüm oranı, faiz, pay)
`diff` puanı, `pct_change` yüzdeyi veriyor; hangisini raporladığını yaz.

## Baz etkisi

Yıldan yıla değişim iki şeye bağlı: bu yıl ve **geçen yıl.** Geçen yılın aynı
dönemi olağandışı düşükse (kapanma, stok sorunu) bu yılın büyümesi abartılı
görünür; olağandışı yüksekse bu yıl "düşüş" görünür. Buna baz etkisi deniyor.

Sıfıra yakın bazlarda yüzde değişim anlamını yitiriyor: 2'den 6'ya çıkmak
"%200 büyüme". Küçük sayılarda mutlak farkı da yaz.

## Gecikme tablosu kurmak

```python
lags = pd.DataFrame({"y": s})
for k in (1, 7, 14, 364):
    lags[f"lag{k}"] = s.shift(k)

lags = lags.dropna()          # en buyuk gecikme kadar satir gidiyor
```

En büyük gecikme 364 ise ilk 364 satır atılıyor. Üç yıllık veride bir yılı
kaybediyorsun; gecikme seçerken bunu hesaba kat.

## Hedef kurmak

"Bugünün bilgisiyle h adım sonrasını tahmin et":

```python
h = 7
data = pd.DataFrame({
    "lag0": s,                 # bugun
    "lag7": s.shift(7),        # gecen hafta
    "target": s.shift(-h),     # 7 gun sonrasi: CEVAP
}).dropna()
```

`shift(-h)` yalnızca `target` sütununda. Özellik sütunlarının hiçbirinde eksi
kaydırma olmamalı.

## Eksik günlerde zamanla kaydırmak

```python
s.shift(1)               # bir SATIR asagi: degerler kayar, indeks ayni
s.shift(freq="D")        # bir GUN ileri: indeks kayar, degerler ayni
s - s.shift(freq="D")    # tarihe gore hizalanir: dunu olmayan gunler NaN
```

`shift(freq=...)` satır saymıyor, zamanı kaydırıyor. Eksik günlü bir seride
gerçek "dünle fark" için bu ya da önce `asfreq("D")`.

## Fark almak neyi değiştiriyor

| İşlem | Çıkardığı |
|---|---|
| `s.diff()` | Düzeyi ve doğrusal trendi |
| `s.diff(7)` | Haftalık mevsimselliği (ve trendi) |
| `s.diff(7).diff()` | İkisini birden |
| `np.log(s).diff()` | Yüzde değişime yakın; büyüyen oynaklığı da dengeliyor |

Her fark alma **gürültüyü büyütüyor** ve baştan satır götürüyor. Gerektiği
kadar fark al, fazlasını değil (Bölüm 11).
