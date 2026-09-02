Üç takımın bir işi kaç dakikada bitirdiği elimizde. Sorulan soru:
**hangi takım yavaş?**

**Yapman gerekenler:**

1. IQR kuralıyla aykırı değerleri bul ve **liste hâlinde** yazdır.
2. Bütün verinin ortalamasını (iki ondalık) ve medyanını **yan yana**
   yazdır.
3. Takıma göre sayı ve ortalamayı, tek ondalığa yuvarlayarak yazdır.

**Beklenen çıktı:**

```
[240]
51.5 30.5
      count  mean
team
A         4  31.0
B         4  82.2
C         2  31.0
```

**Şimdi çıktıyı oku — asıl alıştırma bu.**

İlk bakışta B takımı berbat görünüyor: ortalaması 82, diğerleri 31.

Ama birinci satıra bak: veride **240 dakikalık tek bir kayıt** var ve o
kayıt B takımına ait. Onu çıkarınca B'nin diğer üç değeri 27, 33 ve 29 —
yani diğer takımlardan farksız.

Ortalama 51.5 ama medyan 30.5. Aradaki uçurum tek bir değerden geliyor.

**C takımına da dikkat:** ortalaması 31 ama yalnızca iki kayıt var.

Dürüst bulgu şu: *B takımının ortalamasını tek bir 240 dakikalık kayıt
yükseltiyor; o kayıt çıkarıldığında üç takım da benzer. O 240'ın ne olduğu
araştırılmalı — ölçüm hatası da olabilir, gerçekten uzun süren bir iş de.*

"B takımı yavaş" demek, bu verinin söylemediği bir şey.
