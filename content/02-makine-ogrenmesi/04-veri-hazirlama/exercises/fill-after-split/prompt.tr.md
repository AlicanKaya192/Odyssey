Eksik değerleri dolduracaksın — ama **ayırdıktan sonra**. Bu bölümün
kuralı bu ve alıştırmanın tamamı onun etrafında.

**Yapman gerekenler:**

1. Dosyayı oku. `X`'e üç **sayısal** sütunu al (`age`, `km`, `engine`),
   `y`'ye `price`'ı.
2. **Önce ayır**: dörtte biri test, `random_state=42`. Eksik değerler
   hâlâ yerinde; ayırma bundan rahatsız olmuyor.
3. Doldurma değerini **yalnızca eğitim** verisinden hesapla: `engine`
   sütununun ortalaması.
4. Bu değeri ve **bütün verinin** `engine` ortalamasını yan yana yazdır
   (üç ondalık).
5. **Aynı değeri** hem eğitime hem teste uygulayarak eksikleri doldur.
6. İki kümede kalan eksik sayısını yan yana yazdır.
7. Modeli eğit ve MAE'yi yazdır (iki ondalık).

**Beklenen çıktı:**

```
1.458 1.457
0 0
32.58
```

**Birinci satır bu alıştırmanın konusu.** İki ortalama neredeyse aynı:
**1.458** ve **1.457**. Fark binde bir.

O zaman neden uğraşıyoruz?

**Çünkü kural farkın büyüklüğüyle ilgili değil.** Bütün veriden hesaplanan
bir ortalama, test satırlarının bilgisini taşıyor. Bugün fark 0.001;
başka bir veride, aykırı bir değer test tarafına düşerse 0.3 olabilir.

Kuralı "fark küçükse gerek yok" diye uygularsan, farkın büyük olduğu günü
göremezsin — çünkü farkı ölçmek için zaten iki hesabı da yapmış olman
gerekiyor.

**Beşinci adımdaki "aynı değer" de önemli.** Test kümesini kendi
ortalamasıyla doldurmak, iki kümeyi farklı dünyalara taşırdı; model
eğitimde gördüğünden başka bir şeyle sınanmış olurdu.
