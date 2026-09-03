```python
import matplotlib
matplotlib.use("Agg")     # Odyssey icinde gerekli; kendi bilgisayarinda degil
import matplotlib.pyplot as plt
```

## Tuval ve eksen

| Yazım | Ne yapar |
|---|---|
| `fig, ax = plt.subplots()` | Tek çizim alanlı tuval |
| `plt.subplots(1, 2)` | Yan yana iki alan |
| `plt.subplots(2, 1)` | Alt alta iki alan |
| `plt.subplots(figsize=(10, 4))` | Tuval boyutu (inç) |
| `fig.axes` | Tuvaldeki bütün çizim alanları |
| `plt.close(fig)` | Tuvali kapatır (bellek için) |

Çok grafik çizen döngülerde `plt.close(fig)` gerekiyor; yoksa açık tuvaller
birikiyor.

## Grafik türleri

| Yazım | Ne çizer |
|---|---|
| `ax.bar(x, y)` | Dikey çubuk |
| `ax.barh(x, y)` | Yatay çubuk — uzun kategori adlarında |
| `ax.plot(x, y)` | Çizgi |
| `ax.plot(x, y, marker="o")` | Noktalı çizgi |
| `ax.scatter(x, y)` | Dağılım |
| `ax.hist(values, bins=10)` | Histogram |
| `ax.pie(values, labels=names)` | Pasta — üçten fazla dilimde okunmuyor |
| `ax.boxplot(values)` | Kutu grafiği — medyan, çeyrekler, aykırılar |

## Etiketleme

| Yazım | Ne yapar |
|---|---|
| `ax.set_title("...")` | Başlık |
| `ax.set_xlabel("...")` / `ax.set_ylabel("...")` | Eksen etiketleri |
| `ax.legend()` | Açıklama kutusu (birden fazla seri varsa) |
| `ax.set_xlim(0, 100)` / `ax.set_ylim(0, 100)` | Eksen aralığı |
| `ax.set_xticks([...])` | Hangi değerler işaretlensin |
| `ax.tick_params(axis="x", rotation=45)` | Etiketleri döndür |
| `ax.grid(True, alpha=0.3)` | Izgara çizgileri |

Başlık ve eksen etiketleri **zorunlu**. Birim yazmak da öyle: "Satış" değil
"Satış (bin TL)".

## Okuma bilgileri

| Yazım | Ne verir |
|---|---|
| `ax.get_title()` | Başlık metni |
| `ax.get_xlabel()` / `ax.get_ylabel()` | Eksen etiketleri |
| `ax.patches` | Çubuklar (`len` ile sayılabiliyor) |
| `ax.lines` | Çizgiler |
| `ax.get_ylim()` | Eksen aralığı |
| `p.get_height()` | Bir çubuğun yüksekliği |

Bunlar test yazarken ve bir grafiğin doğru çizildiğini doğrulamak için işe
yarıyor.

## Birden fazla seri

```python
fig, ax = plt.subplots()
ax.plot(months, ankara, marker="o", label="Ankara")
ax.plot(months, izmir, marker="s", label="Izmir")
ax.legend()
```

`label` vermeden `legend()` çağırmak boş bir kutu üretiyor.

## Renk ve biçim

| Yazım | Ne yapar |
|---|---|
| `ax.bar(x, y, color="steelblue")` | Tek renk |
| `ax.bar(x, y, color=["red", "gray", "gray"])` | Çubuk başına renk |
| `ax.plot(x, y, linestyle="--")` | Kesik çizgi |
| `ax.plot(x, y, linewidth=2)` | Kalınlık |
| `ax.scatter(x, y, alpha=0.5)` | Saydamlık — üst üste binen noktalarda |
| `ax.axhline(y=50, color="red")` | Yatay referans çizgisi |

**Bir vurgu rengi ve gerisi gri** çoğu grafikte en okunaklı seçim: göz
nereye bakacağını biliyor.

## Kaydetmek

| Yazım | Ne yapar |
|---|---|
| `fig.savefig("chart.png")` | Kaydeder |
| `fig.savefig("chart.png", dpi=150)` | Çözünürlük |
| `fig.savefig("chart.png", bbox_inches="tight")` | Fazla kenar boşluğunu kırpar |
| `fig.savefig("chart.svg")` | Vektör — ölçeklenince bulanmıyor |

Rapora koyacaksan `dpi=150` ve `bbox_inches="tight"` iyi bir varsayılan.

## pandas ile kısayol

| Yazım | Ne çizer |
|---|---|
| `data.plot(kind="bar", x="city", y="score")` | Çubuk |
| `data.plot(kind="line", x="month", y="sales")` | Çizgi |
| `data["score"].plot(kind="hist", bins=10)` | Histogram |
| `data.plot(kind="scatter", x="hours", y="score")` | Dağılım |
| `data["city"].value_counts().plot(kind="bar")` | Sayım grafiği |

Hızlı bakış için pratik. `ax=ax` argümanıyla kendi eksenine de
çizdirebiliyorsun:

```python
fig, ax = plt.subplots()
data.plot(kind="bar", x="city", y="score", ax=ax)
ax.set_title("...")
```

## Sık kullanılan kalıplar

```python
# Gruplama sonucunu cubukla
ortalama = data.groupby("city")["score"].mean()

fig, ax = plt.subplots()
ax.bar(ortalama.index, ortalama.values)
ax.set_ylim(0, 100)
ax.set_title("Sehirlere gore ortalama not")

# Dagilim ve ortalama cizgisi
fig, ax = plt.subplots()
ax.hist(data["score"], bins=10)
ax.axvline(data["score"].mean(), color="red", linestyle="--")

# Iki grafigi yan yana
fig, (sol, sag) = plt.subplots(1, 2, figsize=(10, 4))
sol.bar(...)
sag.hist(...)
fig.tight_layout()
```

`fig.tight_layout()` çizim alanlarının birbirine girmesini engelliyor; çok
alanlı tuvallerde neredeyse her zaman gerekiyor.
