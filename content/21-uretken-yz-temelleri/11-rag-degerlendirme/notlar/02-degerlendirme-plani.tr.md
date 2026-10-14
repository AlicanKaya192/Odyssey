Bir RAG sistemi için değerlendirme planı:

1. **Kümeyi kur.** Gerçek kullanıcı sorularından en az birkaç yüz tane
   seç; her birine doğru belgeyi ve doğru cevabı yaz. Cevabı belgelerde
   olmayan sorular da ekle.
2. **Getirmeyi ölç.** recall@k ve MRR. Doğru parça ilk k'da değilse model
   ne yaparsa yapsın cevap veremez.
3. **Cevabı ölç.** Doğru, yanlış, kaçırılan. Serbest cevaplarda ifade
   eşleşmesi yetmeyebilir; kurallı denetim, insan ve model ile
   değerlendirmeyi birlikte kullan.
4. **Çekimser kalmayı ölç.** Kesinlik ve duyarlılık birlikte.
5. **Hatayı yerleştir.** Her hatayı getirme ya da okuma diye ayır; yüzdesi
   büyük olanı önce düzelt.
6. **Farkı sına.** İki ayarı karşılaştırırken yeniden örnekleme ile aralığa
   bak; aralık sıfırı içeriyorsa fark güvenilir değil.
7. **Kayıt tut.** Her ölçümü ayarlarıyla (parçalama, k, eşik, prompt)
   birlikte yaz; değişiklik sonrası aynı kümeyle yeniden ölç.

**Sık hatalar:**

- **Tek bir doğruluk sayısı:** hatanın yerini göstermez.
- **Kümeyi ayarlara bakarak değiştirmek:** sayılar iyileşir ama gerçek
  kullanıcıda değil.
- **Yalnızca cevaplanabilir sorular:** sistemin "bilmiyorum" deme
  becerisi ölçülmez.
- **Küçük farklara güvenmek:** 24 soruda bir soru 4 puan eder.
