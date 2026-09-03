Bir meslektaşın sana bir model veriyor ve **%100 doğruluk** aldığını
söylüyor. Sevinmeden önce ne yapman gerekiyor?

Bu alıştırmada aynı veriyi iki kez modelleyeceksin: bir kez bütün
sütunlarla, bir kez `followup_calls` sütunu olmadan.

**Yapman gerekenler:**

1. Veriyi oku ve ayır (`stratify=y`).
2. **Birinci model:** sayısal sütunlar `age`, `bmi`, `visits`,
   `followup_calls`. Pipeline ile `LogisticRegression(max_iter=1000)` eğit.
   Doğruluk, precision, recall'ü tek satırda yazdır.
3. Karışıklık matrisini yazdır.
4. Modelin toplam kaç hata yaptığını yazdır (köşegen dışındaki hücrelerin
   toplamı).
5. `followup_calls` sütununun **hedefe göre ortalamasını** yazdır (iki
   ondalık) — sızıntının kaynağı burada görünüyor.
6. **İkinci model:** `followup_calls` çıkarılmış hâliyle aynı üç sayıyı
   yazdır.
7. Son satırda iki doğruluk arasındaki farkı yazdır.

**Beklenen çıktı:**

```
1.0 1.0 1.0
[[161   0]
 [  0  39]]
0
{0: 0.48, 1: 3.43}
0.815 0.571 0.205
0.185
```

**Birinci satır: doğruluk, precision ve recall'ün üçü de 1.0.** Karışıklık
matrisinde tek bir hata yok. Model 200 hastanın 200'ünü doğru bilmiş.

**Bu bir başarı değil, bir alarm.** Gerçek veride mükemmel skor
neredeyse her zaman tek bir şey demek: **sızıntı.**

**Beşinci satır sebebi gösteriyor:** yeniden yatırılmayan hastalarda
`followup_calls` ortalaması 0.48, yatırılanlarda **3.43**. Sütun hedefi
neredeyse birebir kopyalıyor.

Peki neden? Çünkü **takip aramaları hasta taburcu olduktan sonra
yapılıyor.** Bu sütun, tahmin etmeye çalıştığımız olayın **sonucu** — sebebi
değil.

**Tahmin anında bu bilgi elinde olmayacak.** Hasta henüz taburcu olurken
kaç takip araması yapılacağını bilmiyorsun. Model, gerçekte asla sahip
olmayacağın bir bilgiyle çalışıyor.

**Bunu hiçbir araç yakalayamaz.** `train_test_split` yakalamıyor — sütun
her iki tarafta da var. Pipeline yakalamıyor — sızıntı ön işlemede değil,
sütunun kendisinde. Çapraz doğrulama yakalamıyor — her katta aynı şey
oluyor.

**Yakalayan tek şey şu soru:** *bu bilgi, tahmini yapacağım anda gerçekten
elimde olacak mı?*

Sütunları tek tek bu soruya sokmak, modülün otomatikleştirilemeyen tek
adımı.

**Son satır: 0.185.** Sütun çıkarılınca doğruluk 1.000'den 0.815'e
düşüyor — ve 0.815 zaten taban çizginin (0.805) hemen üstünde. Yani
gerçekte elinde çok zayıf bir model var; sızıntı onu mükemmel gösteriyordu.

**Gerçek hayatta bu model üretime alınsaydı** ilk günden itibaren
`followup_calls` sütunu boş gelecek ve model hiçbir işe yaramayacaktı.
