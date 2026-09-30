## Hangi soruya hangi araç

| Aradığın | Araç | Puan neye verilir |
|---|---|---|
| Nokta anomalisi | Kalıntının dayanıklı puanı | Tek gözlem |
| Bağlamsal anomali | Aynısı; beklenen, bağlama göre (saat, haftanın günü) | Tek gözlem |
| Takılı sensör | Tekrar uzunluğu | Blok |
| Düz çizgi, donmuş seri | Pencere standart sapması sıfıra yakın | Pencere |
| Düzey kayması (canlı) | CUSUM; aynı yönde alarm dizisi | Birikim |
| Düzey kayması (geriye dönük) | En iyi kesim ve kazancı | Bütün seri |
| Eğim değişimi | Parçalı doğru; tek doğrunun kalıntısında ters V | Bütün seri |
| Oynaklık değişimi | Pencere ölçeğinin referansa oranı | Pencere |

## "Beklenen"i kurmanın yolları

| Beklenen | Artısı | Eksisi |
|---|---|---|
| Saat / gün ortancası (profil) | Basit, dayanıklı | Trendi ve düzey kaymasını izlemez |
| Son `n` aynı günün ortancası | Canlı çalışır, kendini yeniler | Kaymayı birkaç haftada "olağan" sayar |
| Mevsimsel naif | Tek satır | Önceki haftanın anomalisi yankı yapar |
| STL kalıntısı (`robust=True`) | Trend ve mevsimi birlikte çıkarır | Geriye dönük; canlıda kullanılmaz |
| Tahmin modeli + aralık (Bölüm 20) | Dış değişkenleri bilir | Model eğitimi anomalilerden etkilenir |

Canlı dedektörde beklenti için her zaman `shift`: bugünün değeri bugünün
beklentisine girmemeli.

## Dayanıklı puan

```python
def robust_score(resid):
    center = resid.median()
    mad = (resid - center).abs().median()
    return 0.6745 * (resid - center) / mad
```

Canlı sürümü, ölçeği de yalnızca geçmişten alır:

```python
def mad(x):
    return np.median(np.abs(x - np.median(x)))


scale = 1.4826 * resid.shift(1).rolling(56, min_periods=28).apply(mad, raw=True)
score = resid / scale
```

`1.4826 × MAD`, normal dağılımda standart sapmaya denk gelir (`0.6745`'in
tersi).

Oransal mı, mutlak mı? Gürültü düzeyle birlikte büyüyorsa (satış, trafik)
**oransal** sapma (`gerçek / beklenen − 1`); sabitse (sıcaklık, basınç) fark.

## Tekrar uzunluğu

```python
same = s.diff() == 0
block = (~same).cumsum()
length = same.groupby(block).transform("sum") + 1     # her satira blogunun boyu
stuck = length >= 3
```

Ondalık sayısı az olan seride eşiği yükselt; tam sayı sayan bir sayaçta (günlük
sipariş) tekrar olağandır, bu kural kullanılmaz.

## CUSUM

```python
def cusum(z, k=1.0, h=8.0):
    up = down = 0.0
    alarms = []
    for when, value in z.items():
        up = max(0.0, up + value - k)
        down = max(0.0, down - value - k)
        if up > h or down > h:
            alarms.append((when, "up" if up > h else "down"))
            up = down = 0.0
    return alarms
```

| Ayar | Büyütünce |
|---|---|
| `k` (pay) | Küçük kaymalara sağırlaşır; yanlış alarm azalır |
| `h` (eşik) | Alarm gecikir; yanlış alarm azalır |
| Kırpma (`clip`) | Küçültünce tek günlük sıçramalar sayılmaz |

Başlangıç için: `k`, yakalamak istediğin kaymanın yarısı (standart sapma
biriminde); `h`, 4–8 arası. Sonra geçmişte dene.

`d` büyüklüğünde bir kayma yaklaşık `h / (d − k)` adımda yakalanır: `k = 1`,
`h = 8` ile 3'lük kayma 4 adımda, 1.5'lik kayma 16 adımda.

## En iyi kesim

```python
def best_split(x, margin=14):
    x = np.asarray(x, dtype=float)
    total = ((x - x.mean()) ** 2).sum()
    best_k, best_sse = None, None
    for k in range(margin, len(x) - margin):
        left, right = x[:k], x[k:]
        sse = ((left - left.mean()) ** 2).sum()
        sse += ((right - right.mean()) ** 2).sum()
        if best_sse is None or sse < best_sse:
            best_k, best_sse = k, sse
    return best_k, 1 - best_sse / total
```

- `margin`: uçlara çok yakın kesimleri dışarıda bırakır; üç günlük bir "parça"
  değişim değil, gürültüdür.
- Önce mevsimi çıkar, anomalileri onar.
- Kazanç küçükse (bu seride değişimsiz parçalarda 0.01–0.02) değişim yok de.
- Eğim için ortalama yerine `np.polyfit(t, x, 1)` kalıntısı.

Çok sayıda değişim için `ruptures` kütüphanesi (`Pelt`, `Binseg`); uygulamayla
birlikte gelmiyor, kendi ortamına `pip install ruptures` ile kurulur.

## Oynaklık

```python
def robust_sd(x):
    return 1.4826 * np.median(np.abs(x - np.median(x)))


spread = resid.rolling(72).apply(robust_sd, raw=True)
ratio = spread / spread.loc[:reference_end].median()
```

Oran 1.5–2'yi kalıcı olarak aşıyorsa gürültü değişmiştir. Düz standart sapma
burada yanıltır: pencereye düşen tek bir anomali onu şişirir.

## Eşiği seçmek

| Durum | Eşik |
|---|---|
| Kaçan olay çok pahalı (güvenlik, arıza) | Düşük; yanlış alarmı kabul et |
| Her alarm bir insanı meşgul ediyor | Yüksek |
| Etiketli olay var | Kesinlik–duyarlılık tablosu çıkar, maliyete göre seç |
| Etiket yok | Puanları sırala, kopmanın olduğu yere koy; geçmişte kaç alarm verdiğini say |

Beklenen yanlış alarm sayısı = gözlem sayısı × eşiğin dışına düşme olasılığı.
Saatlik veride 3 eşiği yılda 24, dakikalık veride 1400 yanlış alarm demek.
