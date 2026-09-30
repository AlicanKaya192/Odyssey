Mevsimsel naif mi, son dört haftanın ortalaması mı? Aynı 13 deneyde ikisini
karşılaştır ve farkın gerçek olup olmadığına karar ver.

Başlangıç kodunda `snaive(train, h)`, `weeks_mean(train, h, k)` ve `cuts`
(13 kesim günü) hazır.

**Yapman gerekenler:**

1. `errors(forecast)` adında bir fonksiyon yaz: 13 deneyin her birinde
   28 günlük **mutlak hataları** hesaplasın ve hepsini 13 × 28'lik bir numpy
   dizisi olarak döndürsün. `forecast`, `(train, h)` alan bir fonksiyon.
2. İki yöntem için çalıştır: `snaive` ve
   `lambda train, h: weeks_mean(train, h, 4)`.
3. Her yöntemin deney başına MAE'sini al (`axis=1` ortalaması) ve iki
   yöntemin genel ortalamasını iki ondalıkla aynı satıra yazdır (önce
   mevsimsel naif).
4. Deney deney farkı hesapla (`snaive − weeks`). Farkın ortalamasını,
   standart sapmasını (`ddof=1`, iki ondalık) ve mevsimsel naifin kazandığı
   deney sayısını aynı satıra yazdır.
5. Yalnızca 12. deneye (5 Kasım kesimi, dizideki konumu 11) bakan biri ne
   görürdü? İki yöntemin o deneydeki MAE'sini iki ondalıkla aynı satıra
   yazdır.
6. Her yöntemin hatasını ufkun haftasına göre ortala (sütunları 7'şerlik dört
   parçaya böl) ve bir ondalıkla iki liste olarak alt alta yazdır.

**Beklenen çıktı:**

```
17.95 17.2
0.75 2.84 5
11.64 14.84
[15.9, 17.0, 18.2, 20.7]
[13.9, 16.4, 17.9, 20.6]
```

Ortalamada dört haftalık yöntem biraz önde, ama fark (0.75) deneyler arası
oynaklığının (2.8) çok altında ve mevsimsel naif 13 deneyin 5'ini kazanıyor.
Tek bir deneye bakan, tam tersi sonuca varırdı. Dürüst karar: berabere.
Son iki satır küçük bir ayrıntı veriyor: dört haftalık ortalama yakın ufukta
biraz daha iyi, uzak ufukta fark kapanıyor.
