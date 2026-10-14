Bir sohbet API'sine yapılan tek bir çağrının yolu, bölümde kurduğumuz
parçalarla:

1. **Program mesaj listesini hazırlar.** Sistem mesajı, önceki bütün
   kullanıcı ve asistan mesajları ve yeni soru. API durumsuz olduğu için
   geçmiş her seferinde baştan gönderilir.
2. **Şablon uygulanır.** Liste rol işaretleriyle tek bir token dizisine
   çevrilir ve sona asistan işareti eklenir.
3. **Model token token üretir.** Her adımda sıradaki token'ın dağılımı
   hesaplanır ve sıcaklık gibi ayarlara göre bir token seçilir.
4. **Üretim durur.** Durma işareti gelirse `stop`, `max_tokens` dolarsa
   `length`.
5. **Cevap döner.** Metin, bitiş nedeni ve kaç token işlendiği.

**Program tarafında yapılacaklar:**

- Bitiş nedenine bak: `length` ise cevap eksik; ya sınırı büyüt ya da
  cevabı eksik diye işaretle.
- Cevabı **doğrula**: model akıcı ama yanlış bir cevap verebilir. Bir
  kaynakla, bir kuralla ya da bir testle karşılaştır.
- Tekrarlanabilirlik gerekiyorsa sıcaklığı düşük tut; ama doğruluk için
  sıcaklığa değil doğrulamaya güven.
- Aynı soruyu birkaç kez sormak, cevabın tutarlı olup olmadığını gösterir;
  tutarsızlık dayanağın zayıf olduğuna işarettir.

**Sık hatalar:**

- **Önceki mesajları göndermemek** ve modelin "hatırlamasını" beklemek.
- **`length`'i görmezden gelmek:** yarım bir cevap tamammış gibi kullanılır.
- **Sıcaklık 0'ı doğrulukla karıştırmak.** Oyuncak model sıcaklık 0'da da
  yanlış ülkenin başkentini söyledi.
- **Şablonu elle yanlış kurmak:** asistan işareti olmadan model cevap
  vermek yerine diyaloğu sürdürür.
