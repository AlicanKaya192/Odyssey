Şimdiye kadar hep test skoruna baktın. Bu alıştırmada **eğitim skorunu da**
yanına koyacaksın — ve model hakkında bambaşka bir şey göreceksin.

Karar ağacının `max_depth` değeri karmaşıklığı doğrudan ayarlıyor.

**Yapman gerekenler:**

1. Veriyi hazırla: oku, eksik satırları at, kategorileri kodla, ayır
   (`random_state=42`).
2. Şu derinlikleri sırayla dene: **1, 2, 3, 5, 8 ve `None`** (sınırsız).
3. Her derinlik için modeli eğit ve **iki** hata ölç: eğitim kümesinde ve
   test kümesinde.
4. Her derinlik için tek satır yazdır: **derinlik, eğitim hatası, test
   hatası** — üçü yan yana, hatalar iki ondalık. `None` yerine `none`
   yazdır.

**Beklenen çıktı:**

```
1 99.68 96.65
2 72.72 58.47
3 51.34 65.3
5 18.25 53.83
8 0.19 56.83
none 0.0 59.06
```

**İki sütuna ayrı ayrı bak.**

**Eğitim sütunu sıfıra iniyor.** Derinlik sınırı kalkınca ağaç her kaydı
ayrı bir dalda ezberliyor ve eğitim verisinde hiç hata yapmıyor. Bu bir
başarı değil: model veriyi **hatırlıyor**, kuralı öğrenmiyor.

**Test sütunu inmiyor.** 53 ile 96 arasında geziniyor, hiç 50'nin altına
düşmüyor. Aradaki uçurum derinlik 1'de -3.03, sınırsızda **59.06** — aşırı
öğrenmenin kendisi bu.

**Şimdi test sütununa dikkatlice bak:** 96.65 → 58.47 → 65.30 → 53.83 →
56.83 → 59.06. Düzgün bir eğri değil, **zıplıyor**.

Hangi derinlik en iyi? Tabloya bakıp "5" demek kolay. Ama test kümesinde 27
kayıt var; aradaki 5 birimlik farklar gerçek bir üstünlük mü, yoksa hangi 27
aracın teste düştüğüyle ilgili bir tesadüf mü?

Sonraki alıştırma tam olarak bunu ölçüyor.
