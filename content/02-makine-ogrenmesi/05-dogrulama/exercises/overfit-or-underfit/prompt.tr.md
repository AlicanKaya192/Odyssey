Aşırı öğrenme ile yetersiz öğrenmenin **çözümleri birbirinin tersi**:
birinde modeli basitleştiriyorsun, ötekinde karmaşıklaştırıyorsun. Yanlış
teşhis seni ters yöne götürüyor.

Bu alıştırmada teşhisi koda döküyorsun.

**Yapman gerekenler:**

1. Veriyi her zamanki gibi hazırla ve ayır.
2. İki modeli eğit: **`simple`** (derinlik 1) ve **`complex`** (derinlik
   `None`).
3. Her biri için eğitim ve test hatasını ölç.
4. Teşhis koy:
   - Test hatası ile eğitim hatası arasındaki fark **20'den büyükse** →
     `overfit`
   - Değilse ve eğitim hatası **50'den büyükse** → `underfit`
   - İkisi de değilse → `ok`
5. Her model için tek satır yazdır: **ad, eğitim hatası, test hatası,
   teşhis**.

**Beklenen çıktı:**

```
simple 99.68 96.65 underfit
complex 0.0 59.06 overfit
```

**İki satır, iki farklı hastalık.**

`simple` modelde iki hata da yaklaşık 100 — model o kadar basit ki eğitim
verisini bile açıklayamıyor. Buna **yetersiz öğrenme** deniyor ve çözümü
modeli karmaşıklaştırmak.

`complex` modelde eğitim hatası **sıfır**, test hatası 59. Model veriyi
ezberledi ama hiçbir şey genelleyemedi. Buna **aşırı öğrenme** deniyor ve
çözümü modeli basitleştirmek.

**Dikkat et:** yalnızca test skoruna bakıyor olsaydın 96.65 ve 59.06
görecektin ve "ikincisi daha iyi" deyip geçecektin. Eğitim skoru yanına
gelince ortaya iki bambaşka sorun çıkıyor — ve ikisinin de tedavisi farklı.

Buradaki eşikler (20 ve 50) bu veriye göre seçilmiş sayılar; gerçek bir
projede sabit eşik yerine iki skorun **birbirine göre** durumuna
bakılıyor.
