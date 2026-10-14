Üretken model kullanan bir sistemi yayına almadan önce:

**Önyargı**

1. Sonuçları gruplara göre ayrı ayrı ölç (seçilme oranı, fırsat eşitliği,
   hata oranı). Genel doğruluk farkları gizler.
2. Vekil değişkenleri ara: korunan özelliği çıkarmak yetmez.
3. Bir düzeltme seçersen bedelini yaz ve kararı teknik ekibin tek başına
   değil, kurumun vermesini sağla.

**Kişisel veri**

1. Görevin gerçekten hangi kişisel veriye ihtiyacı var? Gerekmeyeni toplama.
2. Kalanı modele ve kayıtlara gitmeden maskele.
3. Maskeleyiciyi örnek cümlelerle ölç; kaçırdığı biçimleri listele.
4. Saklama süresini sınırla.

**Güvenlik ve şeffaflık**

1. Kullanıcıya bir modelle konuştuğunu ve hata yapabileceğini söyle.
2. Kişiyi etkileyen kararlarda son sözü insana bırak.
3. Hatalı ya da zararlı çıktıları bildirme yolu aç; kayıt tut.
4. Prompt injection gibi saldırılara karşı Modül 2'deki önlemleri al.

**Sık hatalar:**

- **"Grup bilgisini kullanmıyoruz, adiliz" demek:** bölümde vekil
  değişken önyargıyı taşıdı.
- **Tek bir adalet ölçüsüne bakmak:** eşit seçilme oranı ile fırsat eşitliği
  birbirini tutmayabilir.
- **Maskeleyiciyi ölçmemek:** harflerle yazılmış e-posta kaçtı.
- **Sorumluluğu modele bırakmak:** model öneri verir, karar insanın.
