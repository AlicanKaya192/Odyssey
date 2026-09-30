## İki test, iki varsayım

| | ADF | KPSS |
|---|---|---|
| Açılımı | Augmented Dickey–Fuller | Kwiatkowski–Phillips–Schmidt–Shin |
| Başlangıç varsayımı | Durağan **değil** (birim kök var) | Durağan |
| Küçük p (< 0.05) | Durağan | Durağan değil |
| Büyük p | Karar yok: durağan olmadığı reddedilemedi | Karar yok: durağanlık reddedilemedi |
| İstatistik | Ne kadar eksi, o kadar durağan | Ne kadar büyük, o kadar durağan değil |

Bir test varsayımını **reddedemediğinde** onu kanıtlamış olmuyor. ADF'in
büyük p-değeri "durağan değil" demek değil, "durağan olduğunu gösteremedim"
demek. İki testi birlikte kullanmanın nedeni bu: biri bir yönden, öteki ters
yönden bakıyor.

## Dönen değerler

```python
from statsmodels.tsa.stattools import adfuller, kpss

stat, pvalue, used_lags, n_obs, critical, icbest = adfuller(x)
stat, pvalue, used_lags, critical = kpss(x, regression="c", nlags="auto")
```

- `stat`: test istatistiği.
- `pvalue`: p-değeri.
- `used_lags`: testin hesaba kattığı gecikme sayısı.
- `critical`: `{"1%": ..., "5%": ..., "10%": ...}` kritik değerler. ADF'te
  istatistik kritik değerden **küçükse** (daha eksi) durağan; KPSS'te
  **büyükse** durağan değil.

Seride `NaN` olmamalı: farktan sonra `dropna()`.

## İkisini birlikte okumak

| ADF | KPSS | Yorum | Ne yap |
|---|---|---|---|
| Durağan | Durağan | Durağan | Devam et |
| Durağan değil | Durağan değil | Durağan değil | Fark al |
| Durağan değil | Durağan | Düz bir doğru etrafında durağan olabilir (trend-durağan) | Trendi çıkar ya da fark al; çiz |
| Durağan | Durağan değil | Fark alınca durağan olabilir | Fark al; çiz |

Son iki satır "testler çelişiyor" durumu. Çoğu zaman dönüşümün eksik olduğunu
gösteriyor: mevsim, büyüyen varyans ya da bir seviye kayması.

## `regression` seçeneği

| Değer | Test neye göre durağanlık arıyor |
|---|---|
| `"c"` (varsayılan) | Sabit bir düzeyin etrafında |
| `"ct"` | Düz bir trend doğrusunun etrafında |

`"ct"` ile "durağan" çıkan seri **trend-durağan**: düzey kayıyor ama kayma
düz bir doğru ve sapmalar ona geri dönüyor. Pratikte farkı bilmek yeterli;
çoğu iş serisi için fark almak güvenli yol.

## KPSS'in p-değeri

KPSS p-değerini bir tablodan okuyor ve tablo yalnızca 0.01–0.10 arasını
kapsıyor. İstatistik tablonun dışındaysa:

- p = 0.01 "en çok 0.01" demek (güçlü ret),
- p = 0.10 "en az 0.10" demek (ret yok),

ve statsmodels `InterpolationWarning` basıyor. Bu bir hata değil. Susturmak
için:

```python
import warnings

warnings.simplefilter("ignore")
```

## Testler ne zaman yanılır

**Mevsim.** İkisi de mevsimi aramıyor. Mevsimsel bir seri "durağan" çıkabilir.
Çizime ve mevsim grafiğine bak.

**Seviye kayması.** Bir günde başka bir düzeye geçen ama iki dönemde de durağan
olan seri (web trafiğindeki 2 Eylül gibi) ADF'e rastgele yürüyüş gibi
görünebilir. Fark almak yerine kaymayı modellemek gerekir (Bölüm 21).

**Kısa seri.** 30–40 gözlemle testlerin gücü düşük: ADF neredeyse her şeye
"reddedemedim" der. Aylık 3 yıllık veriyle test sonucuna fazla yaslanma.

**Çok uzun seri.** Binlerce gözlemde en küçük sapma bile "anlamlı" çıkar. p
çok küçük olsa da etkinin boyuna bak.

**Yavaşça geri dönen seri.** Ortalamaya dönüyor ama çok yavaş: ADF rastgele
yürüyüşten ayıramaz. Daha uzun veri gerekir.

**Aykırı değerler.** Birkaç büyük sıçrama sonucu iki yöne de çekebilir. Önce
temizle (Bölüm 13).

## p-değeri nedir, ne değildir

p-değeri: **varsayım doğru olsaydı**, bu kadar uç bir sonucu görme olasılığı.

- p = 0.03 "seri %97 olasılıkla durağan" demek **değil**.
- 0.05 sihirli bir sınır değil; 0.049 ile 0.051 aynı bilgi.
- Test bir karar aracı, bir ölçüm değil. "Ne kadar durağan" sorusunu
  cevaplamaz.

Sağlam yol: çizim + iki yarının ortalaması ve standart sapması + iki test.
Dördü aynı şeyi söylüyorsa karar net.
