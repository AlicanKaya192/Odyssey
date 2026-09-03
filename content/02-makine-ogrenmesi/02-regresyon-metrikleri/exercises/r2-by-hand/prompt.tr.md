R² tek satırlık bir çağrı, ama içinde önceki bölümün taban çizgisi
saklı. Formülü açınca bu görünüyor.

```
R² = 1 - (modelin hatasi) / (taban cizginin hatasi)
```

**Yapman gerekenler:**

1. `homes.csv`'yi oku, `area` ile `price`'ı al, alışıldık şekilde ayır
   (dörtte biri test, `random_state=42`) ve modeli eğit.
2. **`ss_res`**'i hesapla: kalıntıların karelerinin **toplamı** (ortalaması
   değil). İki ondalıkla yazdır.
3. **`ss_tot`**'u hesapla: her gerçek değerin **test ortalamasından**
   farkının karesi, toplanmış. İki ondalıkla yazdır.
4. R²'yi `1 - ss_res / ss_tot` ile hesapla.
5. Kendi sonucunu ve `r2_score`'un verdiğini **yan yana** yazdır (üç
   ondalık).

**Beklenen çıktı:**

```
5225.02
91593.28
0.943 0.943
```

**İki sayının anlamı:**

- `ss_res` **5225** — modelin toplam kare hatası.
- `ss_tot` **91593** — her şeye ortalamayı diyen taban çizginin toplam kare
  hatası.

Model, taban çizginin hatasının yalnızca **%5.7**'sini bırakmış. R² 0.943
tam olarak bunu söylüyor: `1 - 5225/91593`.

**Buradan çıkan üç okuma:**

- R² **1** ise `ss_res` sıfır: hiç hata yok.
- R² **0** ise `ss_res` ile `ss_tot` eşit: model taban çizgi kadar.
- R² **negatif** ise `ss_res` daha büyük: model ortalamadan kötü tahmin
  ediyor.

**Bir ayrıntı:** buradaki taban çizgi **test** kümesinin ortalaması; sen
önceki bölümde **eğitim** ortalamasını kullanmıştın. İkisi yakın çıkıyor
ama aynı değil, ve R²'nin sıfır noktası bu olan.
