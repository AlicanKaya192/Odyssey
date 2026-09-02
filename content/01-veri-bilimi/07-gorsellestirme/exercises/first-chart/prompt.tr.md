İlk çubuk grafiğini çizeceksin — ve **etiketleyeceksin**.

**Yapman gerekenler:**

1. Bir tuval ve bir çizim alanı oluştur (`fig`, `ax`).
2. Şehirleri x ekseninde, notları y ekseninde gösteren bir **çubuk grafik**
   çiz.
3. Başlığı `Average score by city` yap.
4. X eksenini `City`, y eksenini `Score` diye etiketle.
5. Sırayla yazdır: çubuk sayısı, başlık, x etiketi, y etiketi.

**Beklenen çıktı:**

```
4
Average score by city
City
Score
```

**Etiketler neden bu alıştırmanın parçası:** bir grafik başkasına
gösterilmek için çiziliyor. Başlıksız ve eksen etiketsiz bir grafik eksik
bir cümledir — onu gören kişi neye baktığını bilmiyor.

Çizim alanına ne çizdiğini `ax.patches` (çubuklar) ve `ax.get_title()` gibi
çağrılarla geri okuyabiliyorsun. Bu, bir grafiğin doğru çizildiğini
doğrulamanın yolu.
