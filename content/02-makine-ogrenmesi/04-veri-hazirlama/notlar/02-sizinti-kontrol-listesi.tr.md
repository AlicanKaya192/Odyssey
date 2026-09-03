Veri sızıntısı, modelin tahmin anında elinde **olmayacak** bir bilgiyi
eğitimde görmesi. Sonuç her zaman aynı: test skoru olduğundan yüksek çıkıyor
ve model gerçek hayatta o kadar iyi olmuyor.

En kötü tarafı sessiz olması. Hata mesajı yok, uyarı yok — yalnızca beklenenden
güzel bir sayı.

## Dört sızıntı türü

### 1. Hazırlığı ayırmadan önce yapmak

En sık görüleni. Ölçekleme, doldurma, kodlama — hepsi veriden bir şey
öğreniyor.

```python
scaler.fit_transform(X)                   # SIZINTI: butun veri
X_train, X_test = train_test_split(X)
```

Etkisi genelde küçük ama gerçek. Kural, farkın büyüklüğüyle değil ölçümün
dürüstlüğüyle ilgili.

### 2. Özellik seçimini bütün veride yapmak

Bu türün etkisi **büyük** olabiliyor.

```python
correlations = X.apply(lambda c: abs(c.corr(y)))    # SIZINTI
best = correlations.nlargest(5).index
```

Yüzlerce sütun arasından hedefle en ilişkili olanları bütün veriye bakarak
seçmek, test verisiyle rastlantısal olarak uyuşanları seçmek demek.

Ölçüldü: 80 satır, 300 sütun, **hepsi rastgele** (hedefle hiçbir ilişki
yok). Sızıntılı seçim R² **0.442** veriyor — yani var olmayan bir modeli
var gösteriyor. Doğru yapıldığında R² **-0.273** çıkıyor, yani "burada
öğrenilecek bir şey yok."

### 3. Zamanı karıştırmak

Geleceği geçmişe sızdırmak.

- Zaman serisinde rastgele bölme: modele yarını gösterip dünü tahmin
  ettirmek.
- "Toplam sipariş sayısı" gibi sonradan hesaplanan bir sütunu kullanmak.
- Ortalamayı bütün dönem üzerinden alıp geçmiş satırlara yazmak.

Zaman verisinde bölme **tarihe göre** yapılıyor: geçmiş eğitim, gelecek
test. `shuffle=False` gerekiyor.

### 4. Hedefi taşıyan sütun

Cevabı doğrudan söyleyen bir sütun.

| Sütun | Neden sızıntı |
|---|---|
| "Hastaneye yatış tarihi" ile hastalık tahmini | Yatış teşhisten sonra oluyor |
| "İptal sebebi" ile iptal tahmini | Sebep ancak iptal olunca yazılıyor |
| "Toplam ödeme" ile satın alma tahmini | Ödeme satın almanın kendisi |
| Hedeften türetilmiş herhangi bir sütun | Cevabın kopyası |

Bu tür sızıntı en kolay yakalananı: **başarı beklenenden çok yüksekse önce
buraya bakılıyor.**

## Kontrol listesi

Model kurmadan önce her sütun için sor:

1. **Bu sütun tahmin anında elimde olacak mı?**
   Hayırsa çıkar.
2. **Bu sütun hedeften sonra mı oluşuyor?**
   Evetse çıkar.
3. **Bu sütun hedeften türetilmiş olabilir mi?**
   Şüphedeysen korelasyona bak; 0.99 gibi bir sayı alarm.

Model kurduktan sonra sor:

4. **Sonuç beklenenden çok mu iyi?**
   R² 0.99, accuracy %100 — genelde sızıntı işareti, başarı değil.
5. **Hazırlığın her adımı ayırmadan sonra mı yapıldı?**
   Ölçekleme, doldurma, kodlama, özellik seçimi.
6. **Ayarları test kümesine bakarak mı seçtim?**
   Evetse test skoru dürüst değil.

## Sızıntıyı yapısal olarak engellemek

Elle yapılan hazırlıkta bir adımı unutmak kolay. `Pipeline` bütün adımları
modelle birlikte tek nesnede topluyor:

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsRegressor

pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("model", KNeighborsRegressor()),
])

pipe.fit(X_train, y_train)
pipe.predict(X_test)
```

`pipe.fit` ölçekleyiciyi **yalnızca eğitimde** öğreniyor, `pipe.predict`
öğrenileni uyguluyor. Sızıntı yapmak için özel çaba göstermek gerekiyor.

11. bölümün konusu; burada yalnızca çözümün var olduğunu bilmek yeterli.

## Şüphelenmenin işaretleri

| İşaret | Ne düşünmeli |
|---|---|
| R² 0.99'un üstünde | Muhtemelen sızıntı |
| Accuracy %100 | Neredeyse kesin sızıntı |
| Bir özelliğin önemi ezici derecede yüksek | O sütun cevabı taşıyor olabilir |
| Test skoru eğitim skorundan yüksek | Bir yerde bir şey ters |
| Gerçek kullanımda başarı çöküyor | Sızıntı zaten olmuştu |

Son satır en pahalısı: sızıntı ancak model kullanıma girdiğinde ortaya
çıkıyor ve o noktada güven de kaybedilmiş oluyor.
