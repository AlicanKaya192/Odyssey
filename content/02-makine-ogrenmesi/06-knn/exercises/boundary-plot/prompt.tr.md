`k`'nın ne yaptığını sayılarla gördün. Şimdi **göreceksin.**

Modelin çizdiği **karar sınırı**, düzlemin hangi bölgesine hangi sınıfın
söylendiğini gösteriyor. Bunu çizmek için iki özellik kullanıyoruz
(`income` ve `visits`) — üç boyut çizilemez.

Izgara ve ölçekleme başlangıç kodunda hazır; senin işin modelleri kurup
çizmek.

**Yapman gerekenler:**

1. Yan yana iki panel aç (`plt.subplots(1, 2, figsize=(11, 4.5))`).
2. Sol panel **`k=1`**, sağ panel **`k=15`** için:
   - modeli ölçeklenmiş eğitim verisiyle eğit
   - hazır `grid` için tahmin üret ve `grid_x` şekline getir
   - bölgeleri `contourf` ile boya (`alpha=0.25`, `levels=1`)
   - eğitim noktalarını `scatter` ile üstüne koy, rengi `y_train` olsun
   - başlık `k = 1` / `k = 15`, eksenler `income (scaled)` ve
     `visits (scaled)`
   - test doğruluğunu tek satır yazdır: **k, doğruluk**
3. `fig.tight_layout()` çağır ve `chart.png` olarak kaydet.

**Beklenen çıktı:**

```
1 0.9
15 0.9
```

Grafiğin çalıştırma sonrası **sonuç panelinde** görünecek.

**İki sayı aynı. İki grafik hiç aynı değil.**

**Sol panelde (`k=1`)** sınır parçalı: tek tek noktaların etrafında küçük
adacıklar var. Model her aykırı kaydı ciddiye almış ve onun çevresine kendi
bölgesini oymuş.

**Sağ panelde (`k=15`)** sınır tek bir düzgün eğri. Aykırı kayıtlar
çoğunluğun içinde erimiş.

**Bu, tek bir ölçüye bakmanın neden yetmediğinin görsel kanıtı.** İkisinin
de test doğruluğu 0.90; ama biri gürültüyü ezberlemiş, öteki genel eğilimi
yakalamış. Yeni bir müşteri geldiğinde ikisi çok farklı davranacak — ve
soldaki, eğitim verisindeki tesadüflere göre karar verecek.

Bölüm 02'de "bir modelin nerede yanıldığı ne kadar doğru olduğu kadar
önemli" demiştik. Bu grafik aynı cümlenin başka bir hâli: **bir modelin
nasıl karar verdiği, ne kadar doğru olduğu kadar önemli.**
