Bir tuvale **iki farklı grafik** koyacaksın: solda çubuk, sağda dağılım.

**Yapman gerekenler:**

1. Yan yana iki çizim alanı olan bir tuval oluştur; boyutu `(10, 4)` olsun.
2. **Solda** şehir-not çubuk grafiği çiz, ekseni 0-100 arasına zorla,
   başlığı `Scores` yap.
3. **Sağda** çalışma saati ile notu karşılaştıran bir **dağılım grafiği**
   çiz; başlığı `Hours vs score`, x eksenini `Hours` yap.
4. Alanların birbirine girmemesi için düzeni sıkılaştır.
5. Sırayla yazdır: tuvaldeki alan sayısı, soldaki çubuk sayısı, iki başlık
   (aralarında ` | ` ile), ve sol eksenin üst sınırı.

**Beklenen çıktı:**

```
2
4
Scores | Hours vs score
100
```

**Üç şey öğreniyorsun:**

- **Bir tuvalde birden fazla çizim alanı olabiliyor.** Genel kural şu: bir
  grafik **bir şey** anlatıyor. İki şey anlatacaksan iki grafik çiziyorsun,
  hepsini tek grafiğe tıkmıyorsun.
- **Dağılım grafiği** iki sayısal sütun arasındaki ilişkiyi gösteriyor. Her
  nokta bir kayıt. Noktalar bir çizgi oluşturuyorsa iki değişken birlikte
  hareket ediyor demek — ama bu **birinin ötekine sebep olduğu anlamına
  gelmiyor.**
- `fig.tight_layout()` çok alanlı tuvallerde neredeyse her zaman gerekiyor;
  yoksa etiketler birbirine giriyor.
