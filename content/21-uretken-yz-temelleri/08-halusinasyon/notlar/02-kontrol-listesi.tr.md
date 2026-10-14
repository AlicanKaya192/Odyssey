Bir LLM cevabını kullanıcıya göstermeden önce sorulacaklar:

1. **Cevap bir kaynağa dayanıyor mu?** Cevap verilen belgelerden mi
   geliyor, yoksa modelin genel bilgisinden mi? Kaynak varsa ayrıntıları
   (sayı, tarih, ad) kaynağa karşı denetle.
2. **Kaynak numaraları doğru mu?** Gösterilen numara var mı ve o parça
   gerçekten iddiayı içeriyor mu?
3. **Model emin mi?** Önemli bir soruda birkaç cevap al ve örtüşmelerine
   bak. Dağınık cevaplar dayanağın zayıf olduğuna işarettir.
4. **Emin değilsen ne olacak?** "Bilmiyorum" ya da "kaynakta bulamadım"
   demek, yanlış bir cevap vermekten iyidir. Eşiği, verilen cevap sayısı ile
   doğruluk arasındaki dengeye göre seç.
5. **Denetçin ne kadar iyi?** Etiketlenmiş örneklerle kesinliğini ve
   duyarlılığını ölç; neyi kaçırdığına tek tek bak.

**Hangi denetim neyi yakalar?**

| Denetim | Yakalar | Kaçırır | Bedeli |
|---|---|---|---|
| Ayrıntı denetimi | Uydurma sayı, tarih, ad | Anlam değişikliği ("store credit") | Çok ucuz |
| Kaynak numarası denetimi | Var olmayan ya da yanlış kaynak | Kaynağı doğru ama yorumu yanlış cümle | Ucuz |
| Öz tutarlılık | Bilgi boşluğu | Tutarlı ama yanlış cevap | Soru başına çok çağrı |
| İnsan incelemesi | Çoğu hata | Yorgunluk, ölçek | Pahalı |

**Sık hatalar:**

- **Sıcaklık 0'ı güvenilirlik sanmak.** Cevap tekrarlanabilir olur, doğru
  değil.
- **Metin içinde arama yapıp kümeyle karşılaştırmamak.** "1" sayısı
  "17:00"ın içinde bulunur ve desteklenmiş sanılır.
- **Denetçiyi ölçmeden güvenmek.** Derste on iki örnekte bir uydurma kaçtı;
  gerçek veride oran farklı olabilir.
- **Çekimser kalmayı hiç planlamamak.** Arayüz "bilmiyorum" cevabını
  gösterebilmeli.
