`predict` sana `0` ya da `1` veriyor. Ama modelin içinde bir **olasılık**
var ve `predict` onu **0.5'e** göre kesiyor.

0.5 bir hesap sonucu değil, bir varsayılan. Bu alıştırmada onu
değiştireceksin — modeli yeniden eğitmeden.

**Yapman gerekenler:**

1. Aynı akışı kur ve modeli eğit.
2. Test kümesi için **pozitif sınıfın olasılığını** al.
3. Üç eşiği sırayla dene: **0.3, 0.5, 0.7**.
4. Her eşik için olasılığı o eşiğe göre kesip tahmin üret.
5. Her eşik için tek satır yazdır: **eşik, precision, recall** — üçü yan
   yana, oranlar üç ondalık.

**Beklenen çıktı:**

```
0.3 0.818 1.0
0.5 0.839 0.963
0.7 0.889 0.889
```

**Tabloyu yukarıdan aşağı oku:** eşik yükseldikçe precision artıyor
(0.818 → 0.889), recall düşüyor (1.0 → 0.889).

**0.3'te recall 1.000.** Model geçen tek bir öğrenciyi bile kaçırmıyor.
Bedeli precision'ın 0.818'e düşmesi: daha çok kalacak öğrenciye "geçti"
diyor.

**0.7'de precision 0.889.** Model artık daha temiz konuşuyor ama üç geçen
öğrenciyi kaçırıyor.

**Bu bir takas, iyileşme değil.** Eşiği oynatmak bir hatayı azaltırken
ötekini artırıyor; toplamda kazanılan bir şey yok. Gerçek iyileşme ancak
daha iyi bir model ya da daha iyi özelliklerle geliyor.

**Peki hangisi seçilir?** Probleme göre:

- Destek dersine kimin ihtiyacı olduğunu bulmak → eşiği **düşür**,
  kimseyi kaçırma.
- Otomatik burs onayı → eşiği **yükselt**, yanlış onay verme.

**Önemli:** eşik de bir hiperparametre. **Doğrulama** kümesinde seçiliyor,
test kümesinde değil — burada üçünü test kümesinde görüyoruz çünkü konu
takasın kendisi, seçim değil.
