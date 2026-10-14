Bir üretken modelin iyi olup olmadığını tek bir sayı söylemez. Bu patika
boyunca aynı dört soruyu soracağız:

| Soru | Nasıl bakılır | Bu bölümde |
|---|---|---|
| **Benziyor mu?** | Üretilenlerin istatistiği (ortalama, yayılım, ilişki) gerçeğe yakın mı? | 1000 balığın ortalaması ve standart sapması |
| **Çeşitli mi?** | Model hep aynı birkaç örneği mi üretiyor, yoksa verinin bütününü mü kapsıyor? | Örneklerin yayılımı gerçeğinkiyle neredeyse aynı |
| **Kopya mı?** | Örnekler eğitim verisinin aynısı mı? | En yakın komşu uzaklığı |
| **İşe yarıyor mu?** | Asıl görevde (soru cevaplama, özet, sınıflandırma) başarı | Üretken sınıflandırıcının doğruluğu |

**Sık yapılan hatalar:**

- **Birkaç güzel örneğe bakıp karar vermek.** En iyi örnekleri seçip
  göstermek kolaydır; yüzlerce örneğin istatistiğine bakılır.
- **Yalnızca benzerliğe bakmak.** Eğitim verisini aynen geri veren bir
  "model" benzerlik ölçülerinde mükemmel çıkar. Kopya denetimi ayrıca
  yapılır.
- **Ölçekleri karıştırmak.** Santimetre ile gramı aynı uzaklıkta toplamak
  gramı baskın yapar; uzaklıktan önce ölçüler aynı ölçeğe getirilir.
- **Tohumu sabitlememek.** İki modeli farklı rastgele örneklerle
  karşılaştırmak, farkın modelden mi şanstan mı geldiğini gizler.
