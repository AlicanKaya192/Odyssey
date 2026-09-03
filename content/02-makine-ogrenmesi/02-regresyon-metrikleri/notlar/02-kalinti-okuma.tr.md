Kalıntı, tek bir kaydın hatası: `gerçek - tahmin`. Ölçüler bu sayıları tek
bir sayıya indiriyor; kalıntıların kendisi ise **nerede** yanıldığını
gösteriyor.

## Hesaplama

```python
residuals = y_test - prediction        # pandas Series ise dogrudan
residuals = [a - p for a, p in zip(y_test, prediction)]
```

| İşaret | Anlamı |
|---|---|
| Pozitif | Model **düşük** tahmin etmiş; gerçek daha yüksek |
| Negatif | Model **yüksek** tahmin etmiş |
| Sıfıra yakın | İsabet |

## Neye bakılır

| Bakılan | Ne anlatıyor |
|---|---|
| En büyük mutlak kalıntılar | Model en çok nerede yanılıyor |
| Pozitif/negatif dengesi | Sistematik bir sapma var mı |
| Kalıntı - tahmin grafiği | Hata büyüklüğü tahminle değişiyor mu |
| Kalıntı - özellik grafiği | Modelin kaçırdığı bir ilişki var mı |
| Kalıntı dağılımı | Birkaç aykırı değer mi, genel bir yayılma mı |

## Dört tipik desen

**1. Rastgele dağılım (istenen)**

Kalıntılar sıfırın etrafında, belirli bir yön olmadan. Model yakalanacak
olanı yakalamış; kalan gürültü.

**2. Eğimli desen**

Bir özellik büyüdükçe kalıntılar bir yöne kayıyor. **Model o özelliği ya
hiç görmüyor ya da doğrusal olmayan ilişkisini yakalayamıyor.**

Çözüm: eksik sütunu ekle, ya da eğri ilişki yakalayan bir modele geç.

**3. Huni (yelpaze) şekli**

Tahmin büyüdükçe kalıntılar da büyüyor. Küçük evlerde 5 birim, büyük
evlerde 50 birim yanılıyor.

Hata **oransal**, mutlak değil. Hedefin logaritmasını alarak modellemek ya
da MAPE'ye geçmek çözüm oluyor.

**4. Eğri (U ya da ters U) desen**

Kalıntılar ortada bir yöne, uçlarda öteki yöne kayıyor. **İlişki doğrusal
değil**, model düz bir çizgi çekmeye çalışıyor.

Çözüm: karesel terim eklemek ya da ağaç tabanlı bir modele geçmek.

## Grafiği çizmek

```python
import matplotlib.pyplot as plt

residuals = y_train - model.predict(X_train)

plt.scatter(train_ages, residuals)
plt.axhline(0, color="red")
plt.xlabel("age")
plt.ylabel("residual")
plt.savefig("chart.png")
```

`axhline(0)` sıfır çizgisini koyuyor; desen ancak o çizgiye göre okunuyor.

Yatay eksene ne konacağı sorulan soruya bağlı:

- **Tahmin** (`model.predict(...)`) → hata büyüklüğü tahminle değişiyor mu?
- **Bir özellik** → model o özelliği doğru kullanıyor mu?
- **Modelde olmayan bir sütun** → o sütunu eklemeli mi?

Sonuncusu en kullanışlısı: elindeki ama modele koymadığın bir sütuna karşı
kalıntıda desen çıkıyorsa, o sütunu eklemek modeli iyileştiriyor.

## Sayıyla ölçmek

Grafiğe bakmadan da desen aranabiliyor:

```python
correlation = residuals.corr(df.loc[residuals.index, "age"])
```

Sıfıra yakın bir korelasyon desen yok demek. `-0.937` gibi bir sayı ise
güçlü ve yönlü bir ilişki: yaş büyüdükçe model yüksek tahmin ediyor.

## İki uyarı

**Kalıntı ortalaması bir başarı ölçüsü değil.** Doğrusal regresyonun
kalıntılarının ortalaması eğitim verisinde her zaman sıfıra çok yakın
çıkıyor — yöntemin bir sonucu, modelin bir başarısı değil. Ortalamaya
değil **dağılıma** bakılıyor.

**Kalıntı incelemesi eğitim verisinde yapılabilir.** "Eğitimde ölçme"
kuralıyla çelişmiyor: orada ölçüm değil **teşhis** var. Test kümesi
ölçüm için ayrılmış durumda ve öyle kalıyor.

Test kümesinin kalıntılarına bakmak da mümkün ama iki sınırı var: az kayıt
olduğu için desen görmek zor, ve teste ne kadar bakarsan onu o kadar
tüketiyorsun.

## Kalıntıyla ne yapılır

Desen bulmak kötü haber değil, **yol haritası**:

| Görülen | Yapılacak |
|---|---|
| Bir sütuna karşı eğim | O sütunu modele ekle |
| Huni | Hedefi dönüştür ya da oransal ölçüye geç |
| Eğri desen | Doğrusal olmayan model dene |
| Birkaç uç kalıntı | O kayıtlara tek tek bak; veri hatası olabilir |
| Desen yok | Model bu veriden çıkarılabileni çıkarmış |

Son satır da bir sonuç: daha fazlasını istiyorsan yeni **veri** gerekiyor,
yeni model değil.
