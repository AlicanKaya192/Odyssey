Bir tahminin yanılmasının dört ayrı nedeni var. Modelin verdiği aralık bunların
çoğu zaman yalnızca **birini** sayıyor.

## Dört kaynak

| Kaynak | Ne | Modelin aralığında var mı |
|---|---|---|
| Gürültü | Serinin öngörülemeyen günlük oynaması | Evet |
| Katsayı belirsizliği | Katsayılar sınırlı veriden tahmin edildi | Kısmen |
| Model belirsizliği | Seçilen model yanlış ya da eksik olabilir | Hayır |
| Gelecek değişir | Yeni bir rejim, eğitimde görülmemiş bir olay | Hayır |

Bu yüzden formülden çıkan aralıklar pratikte neredeyse her zaman **fazla
dardır**. Derste "%95" aralığın %87 tutması tipik bir sonuç.

Bilinmeyen dış değişken de bir kaynak: gelecekteki sıcaklığı mevsim normaliyle
doldurduysan (Bölüm 18), o tahminin hatası satış aralığını genişletmeli. Model
bunu bilmez; değişkeni kesin bilinen bir sayı sanar.

## Aralığı genişleten durumlar

- **Uzun ufuk.** Hatalar birikir.
- **Kısa eğitim verisi.** Katsayılar güvenilmez.
- **Rejim değişimi.** Geçmiş hatalar geleceği temsil etmez.
- **Seyrek olaylar.** Yılda bir kez olan şeyin belirsizliği üç gözlemle
  ölçülemez.
- **Büyüyen seri.** Hatanın boyu düzeyle birlikte büyür; mutlak aralık yerine
  yüzde aralık (logaritmalı model) daha dürüst.

## Dürüst aralık için

1. Aralığı **örnek dışı** hatalardan kur (kayan başlangıç), eğitim
   kalıntısından değil.
2. Kapsamayı ölç; tutmuyorsa **ölçekle**: "%95" aralığın genişliğini,
   geçmişte %95 kapsayacak kadar büyüt.
3. Kapsamanın çöktüğü dönemleri bul; bir değişken eksikse ekle.
4. Düzenli olarak yeniden ölç: seri değiştikçe aralık da değişir.

## Basit bir ölçekleme

```python
ratio = np.abs(errors) / half_width           # |hata| / aralik yari genisligi
factor = np.quantile(ratio, 0.95)             # gecmisin %95'ini kapsayan carpan
calibrated_low = point - factor * half_width
calibrated_high = point + factor * half_width
```

`errors` ve `half_width`, geçmiş deneylerdeki hatalar ve modelin o günler için
verdiği yarı genişlik. `factor` 1'in üstündeyse model fazla güvenli; aralığı o
kadar büyütürsün. Modelin **şeklini** (ufka göre genişleme) koruyup **boyunu**
veriye göre düzeltmiş olursun.

## Senaryolar

Aralık, "her şey eskisi gibi giderse" belirsizliğini verir. Eskisi gibi
gitmeyebilecek şeyler için senaryo kurulur:

| Senaryo | Nasıl |
|---|---|
| Kampanya yapılırsa / yapılmazsa | Dış değişkeni iki değerle çalıştır (Bölüm 18) |
| Soğuk kış / ılık kış | Sıcaklık için iki farklı vekil |
| Yeni rakip | Düzeyi elle bir yüzde düşür |

Senaryo bir olasılık taşımaz; "şu olursa şu" der. Aralık ile senaryo birbirinin
yerine geçmez, birlikte sunulur.

## Yanlış okumalar

| Söylenen | Doğrusu |
|---|---|
| "Gerçek değer aralığın içinde olacak." | %95 olasılıkla. Yirmide bir dışarı düşmesi beklenir |
| "Aralık dar, o hâlde tahmin iyi." | Dar ve kapsaması düşükse kötü |
| "Dışarı düştü, model bozuk." | Tek bir gün bir şey söylemez; oranına bak |
| "%95 her zaman %80'den iyidir." | Daha geniş, daha az bilgi verici. Karara göre seç |
| "Aralığın ortası en olası değer." | Çarpık dağılımda (logaritmalı model) değil |

## Güven aralığı ile tahmin aralığı

İkisi karıştırılır:

- **Güven aralığı**, bir **katsayının** ya da ortalamanın belirsizliği: "kampanya
  etkisi 46 ile 52 arasında". Veri arttıkça daralır.
- **Tahmin aralığı**, gelecekteki bir **gözlemin** belirsizliği: "yarınki satış
  267 ile 319 arasında". Veri ne kadar artarsa artsın gürültü kadar geniş kalır.

statsmodels'in yöntem adı `conf_int` olsa da `get_forecast` üzerinde çağrıldığında
dönen şey tahmin aralığıdır.
