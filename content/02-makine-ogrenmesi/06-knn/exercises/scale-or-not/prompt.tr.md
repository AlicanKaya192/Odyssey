Bölüm 04'te ölçeklemenin KNN'i etkilediğini görmüştün. Bu alıştırmada
etkinin ne kadar büyük olduğunu ölçeceksin — ve sonuç muhtemelen
beklediğinden sert.

`customers.csv` dosyasında 200 müşteri var: `age` (18-70), `income`
(12.000-200.000), `visits` (1-50) ve hedef `churn` (ayrıldı mı).

**Yapman gerekenler:**

1. Dosyayı oku, üç sütunu `X`'e, `churn`'ü `y`'ye al.
2. Ayır: dörtte biri test, `random_state=42`, **`stratify=y`**.
3. Eğitim ve test kayıt sayılarını yan yana yazdır.
4. **Taban çizgiyi** kur: en sık sınıfı her test kaydı için tahmin et,
   doğruluğunu üç ondalıkla yazdır.
5. İki KNN eğit (`n_neighbors=5`): biri **ham** veriyle, öteki
   **ölçeklenmiş** veriyle. İki doğruluğu yan yana yazdır.
6. Ham KNN taban çizginin **altındaysa** `worse`, değilse `better` yazdır.

**Beklenen çıktı:**

```
150 50
0.7
0.64 0.92
worse
```

**Son satır bu alıştırmanın asıl bulgusu.**

Ölçeklemesiz KNN **0.64** veriyor. Taban çizgi **0.70**. Yani model,
"herkese en sık sınıfı de" diyen tek satırlık kuraldan **daha kötü**.

Ölçeklendikten sonra aynı model **0.92**.

**Neden bu kadar sert:** uzaklık hesabında `income` sütunundaki iki müşteri
arasındaki fark 100.000 olabiliyor, `visits` sütunundaki fark en fazla 49.
Kareleri toplandığında ikincisi görünmüyor bile. Ölçeklemesiz KNN aslında
**yalnızca gelire bakıyor**; öteki iki sütun modele verilmiş ama
kullanılmıyor.

**Alınacak ders:** KNN'de ölçekleme bir iyileştirme değil, **zorunlu bir
adım**. Atlandığında model kurmamış olmaktan daha kötü bir sonuç
çıkabiliyor — ve bunu taban çizgiye bakmadan fark etmen mümkün değil.
