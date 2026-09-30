## Hangi soru, hangi grafik

| Soru | Grafik | Veriyi hazırlama |
|---|---|---|
| Genel şekil nasıl? | Çizgi | `ax.plot(s.index, s)` |
| Trend var mı? | Ham + hareketli ortalama | `s.rolling(n).mean()` |
| Desen yıldan yıla aynı mı? | Mevsim grafiği | `groupby([index.month, index.year]).mean().unstack()` |
| Desen neye benziyor? | Profil (çubuk) | `groupby(index.dayofweek).mean()` |
| Desenin yayılımı ne? | Kutu grafiği | Her gün / ay için ayrı liste |
| İki desen birlikte? | Isı haritası | `groupby([a, b]).mean().unstack()` |
| Seri kendini hatırlıyor mu? | Gecikme grafiği | `ax.scatter(s.shift(k), s)` |
| Birkaç seri nasıl gidiyor? | Küçük çoklu paneller | `plt.subplots(n, 1, sharex=True)` |
| Hangisi hızlı büyüyor? | Endeks (100 tabanlı) | `wide / wide.iloc[0] * 100` |
| Yıl içinde kim önde? | Birikimli çizgi | `s.groupby(index.year).cumsum()` |
| Değişimler nasıl dağılıyor? | Histogram | `ax.hist(s.pct_change().dropna(), bins=50)` |
| Ne zaman ne oldu? | Çizgi + işaretler | `axvline`, `axvspan`, `annotate` |

## Tarih ekseni

```python
import matplotlib.dates as mdates

ax.xaxis.set_major_locator(mdates.YearLocator())             # her yil
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))  # uc ayda bir
ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=0))   # her pazartesi
ax.xaxis.set_major_locator(mdates.HourLocator(interval=6))   # alti saatte bir

ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))  # Jan 2024
ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))  # 09 Mar
ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))  # 14:30

fig.autofmt_xdate()                  # etiketleri egip sigdirir
ax.set_xlim(pd.Timestamp("2024-03-01"), pd.Timestamp("2024-03-31"))
```

Kısa yol: `mdates.ConciseDateFormatter(ax.xaxis.get_major_locator())`
etiketleri kendisi kısaltıyor (yıl yalnızca değiştiğinde yazılıyor).

## Küçük çoklu paneller

Birden çok seriyi tek eksene koymak yerine alt alta paneller:

```python
fig, axes = plt.subplots(4, 1, figsize=(10, 8), sharex=True)
for ax, store in zip(axes, wide.columns):
    ax.plot(wide.index, wide[store])
    ax.set_ylabel(store)
```

`sharex=True` bütün panellerin aynı tarih aralığını göstermesini sağlıyor.
`sharey=True` düzeyleri karşılaştırmak için; desenleri karşılaştıracaksan
her panel kendi ölçeğinde kalsın.

## Eksikleri dürüst göstermek

```python
ax.plot(s.index, s)                      # NaN olan yerde cizgi kopuyor
ax.plot(s.index, s.interpolate(), linestyle=":")   # doldurulan kisim kesik cizgi
```

Çizginin kopması bilgi: orada veri yok. Boşluğu doldurduysan doldurulan
kısmı farklı bir çizgi türüyle göster.

Eksik günler satır olarak hiç yoksa matplotlib iki komşu noktayı düz çizgiyle
birleştiriyor ve boşluk görünmüyor. Çizmeden önce `asfreq`.

## Katmanlar

```python
ax.plot(s.index, s, color="lightgray", linewidth=0.8)      # arka plan
ax.plot(trend.index, trend, linewidth=2)                   # vurgu
ax.fill_between(s.index, low, high, alpha=0.2)             # aralik / belirsizlik
ax.axhline(s.mean(), linestyle="--")                       # referans cizgisi
ax.axvspan(start, end, alpha=0.15)                         # donem
```

`fill_between` ileride çok kullanılacak: tahmin aralıkları (Bölüm 20) böyle
çiziliyor.

## Kaydetmek

```python
fig.tight_layout()
fig.savefig("chart.png", dpi=110)
plt.close(fig)
```

`plt.show()` bir pencere açmaya çalışıyor; betik içinde ve alıştırmalarda
`savefig` kullan. Döngüde çok grafik üretiyorsan `plt.close(fig)` belleği
boşaltıyor.

## pandas kısa yolu

```python
ax = s.plot(figsize=(10, 4))                   # tarih ekseni hazir
wide.plot(subplots=True, figsize=(10, 8))      # seri basina panel
s.resample("ME").mean().plot(kind="bar")
```

Hızlı bakış için rahat. İnce ayar gerekince aynı `ax` nesnesi üzerinde
matplotlib komutlarıyla devam ediliyor.
