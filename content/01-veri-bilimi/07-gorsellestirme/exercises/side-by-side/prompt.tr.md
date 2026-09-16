Bir tuvale **iki grafik** koyacaksın: solda şehir ortalamaları, sağda
çalışma saati ile not arasındaki ilişki.

Veri `students.csv`:

```text
name,city,age,hours,score
Ada,Ankara,21,12,82
Kerem,Izmir,23,6,74
Mina,Ankara,22,14,91
Deniz,Bursa,25,4,68
Efe,Ankara,21,11,88
Sila,Izmir,24,8,76
...
```

**Yapman gerekenler:**

1. İçe aktarmaları yaz, dosyayı oku, şehre göre not ortalamasını hesapla.
2. Yan yana iki çizim alanı olan bir tuval oluştur; boyutu `(10, 4)`.
3. **Solda** ortalamaları çubuk olarak çiz, ekseni 0–100 arasına aç,
   başlığı `Average score` yap.
4. **Sağda** `hours` ile `score`'u **dağılım grafiği** olarak çiz; başlık
   `Hours vs score`, x ekseni `Hours`, y ekseni `Score`.
5. Alanlar birbirine girmesin diye düzeni sıkılaştır ve **`panels.png`**
   olarak kaydet.
6. Sırayla yazdır: tuvaldeki alan sayısı, iki başlık (aralarında ` | `),
   saat ile not arasındaki korelasyon (iki ondalık).

**Beklenen çıktı:**

```
2
Average score | Hours vs score
0.96
```

Çalıştırdıktan sonra grafiğin **sonuç panelinde** görünecek.

**Üç şey öğreniyorsun:**

- **Bir grafik bir şey anlatır.** İki şey anlatacaksan iki grafik
  çiziyorsun, hepsini tek grafiğe tıkmıyorsun.
- **Dağılım grafiğinde her nokta bir öğrenci.** Sağdaki noktalar sağa doğru
  yükselen bir çizgi oluşturuyor; korelasyonun 1'e yakın çıkması bunun
  sayıya çevrilmiş hâli. Ama bu **birinin ötekine sebep olduğunu
  göstermez.**
- `fig.tight_layout()` çok alanlı tuvallerde neredeyse her zaman gerekiyor;
  yoksa etiketler birbirine giriyor.
