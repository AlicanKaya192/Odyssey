Parçalamayı seçerken sorulacaklar:

| Soru | Küçük parça | Büyük parça |
|---|---|---|
| Bir bilgi kaç cümleye yayılıyor? | Tek cümlelik bilgide iyi | Birkaç cümlelik açıklamada iyi |
| Token bütçesi ne kadar? | Ucuz | Pahalı |
| Belgeler ne kadar uzun? | Uzun belgede gerekli | Kısa belgede makalenin tamamı yeter |
| Arama ne kadar isabetli? | Az gürültü | Parçada ilgisiz metin de var |

**Adım adım:**

1. Gerçek kullanıcı sorularından küçük bir değerlendirme kümesi kur: soru,
   doğru belge ve doğru cevapta geçmesi gereken ifade.
2. Birkaç parçalamayı dene (cümle, 2–3 farklı pencere boyu, örtüşmeli ve
   örtüşmesiz, başlıklı ve başlıksız).
3. Her biri için key@k ve ortalama token'ı ölç; ikisini birlikte değerlendir.
4. Kaçan soruları tek tek oku: bilgi bölündü mü, yoksa soru başka
   kelimelerle mi sorulmuş?
5. Bölünme varsa örtüşmeyi ya da pencereyi büyüt; kelime uyuşmazlığı varsa
   gömme ya da karma arama dene.

**Sık hatalar:**

- **Örtüşmesiz küçük pencere:** bölümde 12 kelimelik pencere 0,42'de kaldı;
  sınırda bölünen bilgi kayboldu.
- **Yalnızca doğru belgeyi ölçmek:** doğru makalenin cevabı içermeyen bir
  parçası bulunmuş olabilir; ölçü cevap ifadesi olmalı.
- **Token'ı hesaba katmamak:** makalenin tamamı en isabetliydi ama dört kat
  pahalıydı.
- **Tek bir soruyla karar vermek:** bir ayar bir soruda iyi, ötekilerde kötü
  olabilir.
