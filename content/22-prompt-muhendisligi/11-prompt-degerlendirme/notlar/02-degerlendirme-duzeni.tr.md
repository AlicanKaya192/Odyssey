Bir prompt değişikliğini değerlendirme düzeni:

| Adım | Ne yapılır? |
|---|---|
| 1 | Değerlendirme kümesini sabitle (girdiler + doğru cevaplar) |
| 2 | Eski ve yeni sürümü aynı kümede, aynı ayarlarla (sıcaklık, `max_tokens`) çalıştır |
| 3 | Cevapları kaydet: sürüm adı, girdi, cevap, token |
| 4 | Biçim, geçerlilik ve doğruluğu ayrı puanla |
| 5 | Hataları türlerine ayır (karışan çiftler, ayrıştırılamayanlar) |
| 6 | Sürümlerin farklı sonuç verdiği girdilere bak; farkın aralığını yeniden örneklemeyle bul |
| 7 | Kararı test kümesinde ver; geliştirme kümesindeki puan iyimserdir |

**Açık uçlu cevaplar için puanlama ölçütü (örnek):**

| Soru | Puan |
|---|---|
| Soruyu cevaplıyor mu? | 0 / 1 |
| Ürün adını doğru veriyor mu? | 0 / 1 |
| Vaat ya da yasak bir şey içeriyor mu? | 0 / 1 (içeriyorsa 0) |
| En fazla 3 cümle mi? | 0 / 1 (kodla) |

Kodla denetlenebilen sorular kodla puanlanır; kalanlar için puanlayan
model kullanılacaksa önce 30–50 cevapta insan puanlarıyla uyuşması
ölçülür.

**Sık hatalar:**

- **Tek bir toplam puana bakmak.** Biçim hatası ile yanlış kategori farklı
  düzeltmeler ister.
- **Küçük kümede küçük farka güvenmek.** Kırk mesajda beş mesajlık fark
  bile kesin değildi.
- **Aynı kümede hem iyileştirip hem karar vermek.** Puan iyimser olur.
- **Puanlayan modeli denetlemeden kullanmak.** Uzun cevabı kayırabilir.
