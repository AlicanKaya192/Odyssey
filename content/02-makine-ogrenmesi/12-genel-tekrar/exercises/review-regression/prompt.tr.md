Bölüm 05'te tanıdığın araba verisi: 120 ilan, `age`, `km`, `engine`
(sayısal, 14 eksik), `fuel`, `gearbox` (metin) ve hedef `price`.

Bu alıştırma bir regresyon projesini **baştan sona** yaptırıyor.

**Yapman gerekenler:**

1. Veriyi oku, `X` olarak beş sütunu, `y` olarak `price`'ı al. Ayır
   (`test_size=0.25`, `random_state=42` — regresyonda `stratify` yok).
2. Ön işleyici kur: sayısal sütunlara medyan + ölçekleme, metin sütunlarına
   `OneHotEncoder(handle_unknown="ignore")`.
3. **Taban çizgiyi** ölç: her şeye eğitim ortalamasını tahmin et. MAE,
   RMSE ve R² değerlerini tek satırda yazdır (MAE/RMSE bir ondalık, R² üç).
4. Üç modeli sırayla ele al: `linear` (`LinearRegression`), `tree`
   (`DecisionTreeRegressor(max_depth=3, random_state=42)`), `forest`
   (`RandomForestRegressor(n_estimators=200, random_state=42)`).
   Her biri için tek satır yazdır: **ad, çapraz doğrulama MAE'si, CV
   yayılımı, test MAE'si, test R²'si**.
5. Son satırda **CV kazananını** ve **test kazananını** yan yana yazdır
   (en düşük MAE kazanıyor).

**Beklenen çıktı:**

```
137.3 154.7 -0.02
linear 16.6 2.8 16.2 0.984
tree 69.3 10.2 65.7 0.746
forest 42.3 15.1 44.2 0.883
linear linear
```

**Birinci satır neden yazılıyor:** taban çizginin MAE'si 137.3 ve R²'si
−0.02. Negatif R² "ortalamadan bile kötü" demek — beklenen bir sonuç,
çünkü taban çizgi zaten ortalamanın kendisi ve test kümesindeki küçük
sapma onu sıfırın altına indiriyor.

**Şimdi asıl derse bak: en basit model kazanıyor.**

Doğrusal regresyonun MAE'si **16.2**; ormanınki 44.2, ağacınki 65.7. En
basit model, en karmaşığını **dört kat** geçiyor.

Bu, "daha karmaşık model daha iyidir" sezgisinin tersine bir sonuç ve
sebebi bölüm 07'de ölçülmüştü: **ilişki gerçekten doğrusalsa** ağaçlar onu
basamaklarla taklit etmeye çalışıyor ve kaybediyor. Topluluk kurmak da
kurtarmıyor — orman ağacı iyileştiriyor (65.7 → 44.2) ama doğrusalın
yanına yaklaşamıyor. Sorun ağaç sayısında değil, ağacın veriye
uymamasında.

**Yayılımlara da bak:** ormanınki 15.1, doğrusalınki 2.8. Orman yalnızca
daha kötü değil, aynı zamanda **daha kararsız** — 90 satırlık bir eğitim
kümesi için beklenen bir durum.

**Son satır:** bu veride CV ve test aynı kazananı gösteriyor. Bölüm 08'de
göstermemişti. İkisinin uyuşması güven veriyor; uyuşmaması ise **tek bir
sayıya güvenme** uyarısı.
