Denetimli öğrenmede bu soru yok: modelin doğru mu diye test kümesine
bakıyorsun. Kümelemede bakılacak bir test kümesi yok, dolayısıyla soru
tamamen sana kalıyor.

Bu not, o soruyu cevaplamanın beş yolunu topluyor.

## 1. Gürültü karşılığını ölç

Silüet tek başına okunamıyor. 0.52 iyi mi? Bilinmiyor — neye göre?

Aynı boyutta, aynı sütun sayısında rastgele bir veri üretip aynı `k` ile
kümele:

```python
import numpy as np
rng = np.random.default_rng(0)
noise = rng.normal(0, 1, X_scaled.shape)
```

Ölçülen: gerçek veride 0.517, gürültüde 0.181. **Üç kat fark** asıl bilgi.

İki değer birbirine yakınsa kümeler muhtemelen algoritmanın verdiği
keyfi bölmeler.

## 2. Tabloyu oku, sayıya bakma

Kümeleme sonucu bir sayı değil, bir tablo:

| Küme | `spend` | `visits` | `items` | `returns` |
|---|---|---|---|---|
| 0 | 428.2 | 15.2 | 23.4 | 3.3 |
| 1 | 45.8 | 3.2 | 4.2 | 0.3 |
| 2 | 63.9 | 19.3 | 6.4 | 2.6 |
| 3 | 180.2 | 8.4 | 11.3 | 1.1 |

Sorulacak soru: **her satıra bir isim verebiliyor musun?**

- 0 → "büyük müşteri"
- 1 → "nadir uğrayan"
- 2 → "çok bakan, az alan"
- 3 → "düzenli orta"

Verebiliyorsan kümeler bir şey anlatıyor. Satırların ortalamaları
birbirine benziyorsa ve isim uyduramıyorsan, ortada yapı yok.

**Bu göz kararı değil.** İsim verememek, kümelerin birbirinden ayrılmadığı
anlamına geliyor; sayısal ölçüler bunu bazen kaçırıyor.

## 3. Tohumu değiştir

```python
for seed in (0, 1, 2, 3):
    labels = KMeans(n_clusters=4, random_state=seed, n_init=10).fit_predict(X_scaled)
```

**Küme numaralarının değişmesi normal.** Bakılacak şey gruplamanın kendisi:

```python
from sklearn.metrics import adjusted_rand_score
print(adjusted_rand_score(labels_0, labels_1))
```

Farklı tohumlarda ARI 1.0'a yakınsa yapı sağlam. 0.6-0.7 civarındaysa
algoritma her seferinde başka bir bölme buluyor — bu kararsızlık, yapının
zayıf olduğunun işareti.

## 4. Veriyi sars

Bölüm 08'deki yöntemin aynısı: kayıtların %10'unu çıkarıp yeniden kümele.
Kalan kayıtların grupları değişmiyorsa yapı gerçek.

```python
sample = df.sample(frac=0.9, random_state=seed)
```

Kümeleme kararsızsa aynı müşteri turdan tura farklı gruplara düşüyor.

## 5. Dışarıdan bir şeye bağla

En güçlü test. Kümelemede kullanmadığın bir bilgi varsa — kayıt tarihi,
şehir, sonraki ay ne yaptığı — kümeler o bilgiye göre farklılaşıyor mu
diye bak.

Küme 2 ("çok bakan, az alan") gerçekten varsa, o gruptaki müşterilerin
sonraki ay iade oranı da yüksek çıkmalı. Çıkıyorsa küme bir şeyi
yakalamış demektir.

**Bu bilgi kümelemeye sokulmaz**, yoksa test anlamını kaybediyor.

## Kümeleme ne zaman yanlış araç

| Belirti | Muhtemelen gereken |
|---|---|
| Etiketin zaten var | Sınıflandırma |
| Aradığın "sıra dışı" kayıtlar | Anomali tespiti |
| Gruplar iş kuralıyla tanımlı | `groupby`, kümeleme değil |
| Kümeler hilal/halka biçimli | DBSCAN |
| Her tohumda başka sonuç | Yapı yok; soru yanlış |

**Dördüncü satır k-ortalamaların en bilinen sınırı.** Yuvarlak, benzer
boyutlu kümeler arıyor. İç içe iki halka verirsen ikisini de ortadan
keser — matematiksel olarak doğru, iş olarak saçma.

## Sonucu sunmak

Kümelemeyi bir paydaşa anlatırken:

- **Küme numaralarını değil, isimleri kullan.** "Küme 2" hiçbir şey
  söylemiyor; "sık gelen, az alan grup" söylüyor.
- **Boyutları ver.** 70 kişilik bir küme ile 200 kişilik bir küme farklı
  kararlar gerektiriyor.
- **Belirsizliği söyle.** "Silüet `k=3`'ü, dirsek 3-4 arasını gösteriyor;
  dördü seçtik çünkü dördüncü grup iş açısından ayrı davranıyor" cümlesi
  dürüst ve savunulabilir.
- **"%X doğrulukta" deme.** Böyle bir sayı yok ve sorulursa cevap
  verememek daha kötü.

## Tek cümle

**Kümeleme bir keşif aracı, bir kanıt aracı değil.** Sana bakılacak yeri
gösteriyor; oraya bakıp karar veren sensin.
