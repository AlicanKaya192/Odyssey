Patikanın model bölümleri burada bitiyor. Dört aile gördün; hangisinin ne zaman
işe yaradığını tek yerde topluyoruz.

## Dört aile

| | Temel yöntemler | Üstel düzleştirme | ARIMA | Makine öğrenmesi |
|---|---|---|---|---|
| Bölüm | 14 | 16 | 17–18 | 19 |
| Seriyi nasıl anlatır | Kopyalar | Düzey, eğim, mevsim | Geçmiş değerler ve sürprizler | Özellik tablosu |
| Gereken veri | Bir mevsim | İki mevsim | 50–100 gözlem | Yüzlerce–binlerce satır |
| Dış değişken | Yok | Yok | Var (`exog`) | Var, çok sayıda |
| Birden çok mevsim | Yok | Yok | Fourier ile | Özelliklerle |
| Çok seri | Seri başına | Seri başına | Seri başına | Tek modelle |
| Yorumlanabilirlik | Tam | Yüksek | Orta | Düşük–orta |
| Bakım | Yok | Az | Orta | Çok |

## Bu patikadaki sonuçlar

Günlük mağaza satışı, 13 deney, 28 günlük ufuk:

| Yöntem | MAE |
|---|---|
| Mevsimsel naif | 17.95 |
| Holt–Winters | 15.91 |
| ARIMA | 15.94 |
| Doğrudan gradyan artırma + takvim | 13.80 |
| Doğrudan doğrusal + takvim | 10.64 |
| ARIMA + takvim | 10.23 |

Üç basamak görülüyor: kopyalamak (18), seriyi modellemek (16), takvimi bilmek
(10). Her basamağı bir **bilgi** atlattı, bir model değil.

## Karar sırası

```text
1. Temel yontemlerin tablosu                        -> cita
2. Seride belirgin trend / mevsim var mi?           -> ustel duzlestirme
3. Kalintida kisa hafiza var mi?                    -> ARIMA
4. En kotu deneyler takvimde toplaniyor mu?         -> dis degiskenler
5. Cok seri, cok degisken, dogrusal olmayan etki?   -> makine ogrenmesi
6. Her adimda: ayni duzenek, citaya karsi
```

Bir adım kazanç getirmiyorsa orada dur. Berabere kalan iki yöntemden basit
olanı seç.

## Birleştirmek

Farklı yöntemlerin tahminlerinin **ortalaması** çoğu zaman tek tek her birinden
iyidir: biri yüksek kaçırırken öteki düşük kaçırır ve hatalar kısmen birbirini
götürür.

```python
combined = (forecast_hw + forecast_arima + forecast_ml) / 3
```

Koşul: yöntemler gerçekten **farklı** olmalı (aynı bilgiyle aynı hatayı yapan
iki model ortalanınca bir şey kazanılmaz) ve hiçbiri çok kötü olmamalı.
Ağırlıkları doğrulamada seç, testte değil.

## Ağaçlar için üç kural

1. **Düzeyi değil değişimi tahmin et.** Hedef fark ya da oran.
2. **Az veriyle küçük model.** Sığ ağaçlar, güçlü düzenlileştirme;
   erken durdurmayı zamana göre ayrılmış bir doğrulama parçasıyla yap.
3. **Özellik sayısını satır sayısına göre tut.** Bin satırda elli özellik,
   ezbere davettir.

## Sık sorulanlar

**Derin öğrenme?** Çok sayıda uzun seri ve çok veri olduğunda güçlü. Tek bir
kısa seride bu patikadaki yöntemleri nadiren geçer ve bakımı pahalıdır. Aynı
düzenek, aynı çıta geçerli.

**Hazır otomatik araçlar?** Mertebeyi, bileşenleri ya da özellikleri kendisi
seçen kütüphaneler var. İçinde bu patikanın adımları çalışır; ne yaptıklarını
bilirsen sonuçlarını denetleyebilirsin. Denetlemeden kullanma.

**Model sürekli kötüleşiyor.** Veri değişmiştir (Bölüm 21). Düzenli yeniden
eğit, beceriyi izle, temel yöntemin altına inince alarm ver.
