Yolcu serisini mevsim etkisinden arındır ve 2024 yazının sonunu ham ve
arındırılmış hâliyle karşılaştır.

**Yapman gerekenler:**

1. Çarpımsal ayrıştırmayı yap (`period=12`).
2. Arındırılmış seriyi hesapla: `adjusted = p / mul.seasonal`.
3. Haziran–Eylül 2024 için ham değerleri liste olarak yazdır.
4. Aynı aylar için arındırılmış değerleri bir ondalığa yuvarlayıp liste olarak
   yazdır.
5. Eylül 2024'ün bir önceki aya göre yüzde değişimini ham ve arındırılmış
   seri için hesapla (`pct_change() * 100`, bir ondalık) ve aynı satıra
   yazdır.
6. Aylık yüzde değişimin standart sapmasını ham ve arındırılmış seri için bir
   ondalığa yuvarlayıp aynı satıra yazdır.

**Beklenen çıktı:**

```
[432, 487, 480, 430]
[385.8, 393.3, 382.6, 408.2]
-10.4 6.7
9.6 2.2
```

Ham seri Eylül'de %10 düşüş gösteriyor, arındırılmış seri artış: Eylül düşüşü
her yıl olan bir şey, bu yıl beklenenden küçük olmuş. Son satır aynı şeyi
bütün seri için söylüyor: aydan aya oynamanın çoğu mevsimden geliyor;
arındırılınca geriye çok daha sakin bir seri kalıyor.
