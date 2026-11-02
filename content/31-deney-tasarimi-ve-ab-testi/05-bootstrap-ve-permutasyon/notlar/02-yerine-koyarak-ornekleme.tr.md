Bootstrap'in iki ayrıntısı sık karıştırılır.

## Neden yerine koyarak?

Yerine koymadan, aynı büyüklükte bir örneklem çekersek her seferinde
**aynı** satırları farklı sırada alırız ve istatistik hiç değişmez.
Yerine koyunca bazı satırlar iki üç kez seçilir, bazıları hiç seçilmez;
böylece "başka bir örneklem gelseydi" durumu taklit edilir. Büyük bir
örneklemde her yeni örneklemde satırların yaklaşık %37'si hiç seçilmez:
$(1 - 1/n)^n \approx e^{-1}$.

## Neden aynı büyüklükte?

Standart hata örneklem büyüklüğüne bağlıdır (Tahmin ve Standart Hata
bölümü: $s/\sqrt{n}$). Daha küçük yeniden örneklemler aralığı yapay olarak
genişletir, daha büyükleri daraltır.

## Yüzdelik aralığı ve diğerleri

Bu bölümde en basit yolu, **yüzdelik aralığını** (percentile interval)
kullandık. Çarpık istatistiklerde daha iyi davranan sürümler de var
(BCa gibi); `scipy.stats.bootstrap` bunları hazır sunar. Fikir aynı:
yeniden örnekleme ile istatistiğin dağılımını kurmak.

## Permütasyon ile bootstrap farkı

- **Bootstrap** "tahmin ne kadar oynar?" sorusunu cevaplar: aralık verir.
- **Permütasyon** "etki yoksa bu fark ne kadar şaşırtıcı?" sorusunu
  cevaplar: p verir.
