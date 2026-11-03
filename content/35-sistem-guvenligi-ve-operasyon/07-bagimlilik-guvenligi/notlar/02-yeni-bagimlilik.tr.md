Bir pakete eklenen her satır, başka birinin kodunu programına almaktır.
Çoğu paket güvenilirdir ve tekerleği yeniden icat etmemek doğru bir
karardır. Ama bu karar bir kez ve bilinçli verilir; "kurdum, çalıştı"
yetmez.

## Yeni bir paketi eklemeden önce

| Soru | Neden? |
|---|---|
| Gerçekten gerekli mi? Birkaç satırla yazılabilir mi? | Her paket bir risk ve bir bakım yüküdür |
| Adı doğru yazılmış mı? | Benzer adlı zararlı paketler var |
| Bakımı sürüyor mu? Son sürüm ne zaman? | Terk edilmiş paketin açığı kapanmaz |
| Kaç kişi kullanıyor, kim geliştiriyor? | Topluluk sorunları görür |
| Kaç dolaylı bağımlılık getiriyor? | Tek paket onlarca paket olabilir |
| Lisansı projeye uygun mu? | Hukuki risk de bir risktir |
| Bilinen açığı var mı? | Bağımlılık taramasına bak |

## Güncelleme politikası

Sabitlenmiş sürümler kendiliğinden güncellenmez; bu yüzden bir politika
gerekir:

- **Güvenlik güncellemeleri hemen:** kritik bir duyuru geldiğinde ilgili
  paket öncelikle güncellenir (Yama Yönetimi notu).
- **Diğer güncellemeler düzenli:** örneğin ayda bir, testler eşliğinde,
  küçük adımlarla.
- **Kilit dosyası her güncellemede yeniden üretilir** ve değişiklik kod
  incelemesinden geçer: hangi paket, hangi sürümden hangisine.

## Derleme hattında

1. Kurulum kilit dosyasından ve özet doğrulamayla yapılır.
2. Bağımlılık taraması her değişiklikte çalışır; kritik bulgu birleştirmeyi
   engeller.
3. SBOM her sürümle birlikte üretilir ve saklanır: yeni bir açık
   duyurulduğunda "hangi sürümlerimiz etkileniyor?" sorusu dakikalar
   içinde cevaplanır.
4. İç paketlerin hangi depodan geldiği yapılandırmada açıkça yazılır.

## Güvenmek ama doğrulamak

Popüler bir paketin geliştiricisinin hesabı ele geçirilebilir ve zararlı
bir sürüm yayımlanabilir. Bu yüzden en güvenilir pakette bile yeni sürüme
geçmek, kör bir işlem değil incelenen bir değişikliktir. Kurulum
betiklerini çalıştıran paketler ve beklenmedik yeni dolaylı bağımlılıklar
özellikle dikkat ister.
