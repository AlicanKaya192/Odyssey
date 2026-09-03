Şimdiye kadar modeli sayılarla ölçtün. Bu kez **göreceksin.**

Tek özellikli model bir doğru öğreniyor. Test noktalarını ve o doğruyu aynı
grafiğe koyduğunda modelin nerede tuttuğu, nerede kaçırdığı ortaya çıkıyor.

**Yapman gerekenler:**

1. Dosyayı oku, `area` ile `price`'ı al, aynı şekilde ayır
   (`random_state=42`), modeli eğit ve test tahminlerini üret.
2. Test noktalarını **saçılım** olarak çiz: yatayda `X_test`, dikeyde
   `y_test`.
3. Modelin doğrusunu üstüne çiz: yatayda `X_test`, dikeyde **tahminler**.
   Rengini kırmızı yap ki noktalardan ayrılsın.
4. Eksenleri `area` ve `price` diye adlandır, bir de başlık koy.
5. Grafiği **`chart.png`** adıyla kaydet.
6. Modelin **R²** değerini üç ondalıkla yazdır.

**Beklenen çıktı:**

```
0.943
```

Çalıştırdıktan sonra grafiğin **sonuç panelinde** görünecek.

**Grafikte göreceğin şey:** noktalar kırmızı doğrunun etrafında dağılmış.
Doğrunun üstünde duran noktalarda model isabet etmiş, uzaktakilerde
yanılmış. R² 0.943, bu dağılımın sayıya çevrilmiş hâli.

Bazı noktaların uzak kalmasının bir sebebi var: fiyat yalnızca metrekareye
bağlı değil, yaşa da bağlı — ama bu model yaşı bilmiyor. Önceki
alıştırmada yaşı ekleyince hata 18.5'ten 7.13'e inmişti. **Bu grafik o
eksikliğin resmi.**

**Not:** `plt.show()` yazmana gerek yok; burada ekran yok, dosyaya
kaydediyorsun.
