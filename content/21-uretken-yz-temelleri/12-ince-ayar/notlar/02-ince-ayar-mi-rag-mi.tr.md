Bir modele yeni bir şey "öğretmenin" iki yolu var ve çoğu zaman
karıştırılıyor:

| | RAG | İnce ayar |
|---|---|---|
| Neyi değiştirir? | Modelin o çağrıda gördüğü metni | Modelin ağırlıklarını |
| Ne için iyi? | Bilgi: belgeler, kurallar, güncel veriler | Davranış: biçim, ton, görev, kısa cevap |
| Güncellemek | Belgeyi değiştirmek yeter | Yeniden eğitim gerekir |
| Kaynak göstermek | Kolay | Zor; bilgi ağırlıklara dağılır |
| Riskler | Yanlış getirme, uzun prompt | Unutma, ödülü kandırma, eğitim maliyeti |

**Kural olarak:** model bir bilgiyi bilmiyorsa önce RAG; model bilgiyi
biliyor ama istenen biçimde ya da tonda kullanmıyorsa ince ayar. Çoğu
gerçek sistem ikisini birlikte kullanır: ince ayarla "kaynaklardan cevap
ver, bulamazsan söyle" davranışı, RAG ile bilginin kendisi.

**İnce ayardan önce sorulacaklar:**

1. Aynı sonucu iyi bir prompt ya da RAG veriyor mu? Daha ucuz yolu önce dene.
2. Elimde kaç tane kaliteli örnek var? Az ve gürültülü veri modeli bozar.
3. Eski becerileri nasıl koruyacağım? Genel amaçlı örnekleri karıştır.
4. Başarıyı neyle ölçeceğim? Ödül modelinden bağımsız, etiketlenmiş bir
   değerlendirme kümesiyle.

**Sık hatalar:**

- **Bilgiyi ince ayarla öğretmeye çalışmak:** belgeler değişince model eski
  bilgiyi söylemeye devam eder.
- **Yalnızca yeni veriyle eğitmek:** bölümde eski görev %6,5'e düştü.
- **Ödülü başarı sanmak:** yanlı ödül uzun cevapları seçti, doğruluk
  düşük kaldı.
