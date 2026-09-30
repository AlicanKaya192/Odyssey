# Odyssey nedir?

Odyssey, veri bilimi ve makine öğrenmesini yapılandırılmış bir müfredat
üzerinden öğreten, çevrimdışı çalışan bir masaüstü uygulamasıdır.

Amacı, dağınık kaynaklar arasında gezinmek yerine tek bir yerde ilerleyen ve
ölçülebilir bir öğrenme akışı sunmaktır: her konunun nerede başlayıp nerede
bittiği bellidir, ilerleme kaydedilir, öğrenilenin sınandığı bir adım vardır.

## Nasıl işliyor?

Her bölüm dört parçadan oluşur: konu anlatımı, ders notları, sınav ve kod
alıştırmaları. Bölüm ancak sınav geçildiğinde ve alıştırmalar çözüldüğünde
tamamlanmış sayılır.

Bölümler sırayla açılır. Bir bölüme geçebilmek için bir öncekinin
tamamlanmış olması gerekir; böylece müfredat, üzerine inşa edildiği temel
olmadan ilerlemez.

Kodu uygulamanın içinde yazarsınız. Çalıştırdığınızda program kodu kendi
ortamında yürütür, çıktısını ve ürettiği değişkenleri denetler, hangi
koşulun sağlandığını ve hangisinin sağlanmadığını tek tek gösterir.

## İlkeler

**Değerlendirme deterministiktir.** Alıştırmalar önceden tanımlanmış
kurallarla denetlenir: çıktı karşılaştırması, değişken ve fonksiyon
denetimleri, kodun yapısına bakan kontroller. Aynı kod her çalıştırmada aynı
sonucu verir. Uygulamada dil modeli ya da API çağrısı bulunmaz; öğrenmeyle
ilgili hiçbir işlem ağa çıkmaz.

**Verileriniz cihazınızda kalır.** İlerleme, yazdığınız kod ve ayarlar
`%APPDATA%\Odyssey` klasöründeki yerel bir veritabanında tutulur. Hiçbir veri
dışarı aktarılmaz. Yeni sürüme geçildiğinde bu klasöre dokunulmaz; ilerleme
korunur.

**Açık kaynaktır.** Uygulama MIT lisansıyla dağıtılır; kaynak kodu
incelenebilir, değiştirilebilir ve yeniden dağıtılabilir.

## Şu an nerede?

Uygulama açık beta sürümündedir ve uçtan uca çalışır: öğrenme yolu, konu
anlatımı, ders notları, sınavlar, kod alıştırmaları, kademeli ipuçları,
alıştırma ve sınavlarda geçmiş denemeler, ilerleme kaydı, profil, rozetler,
XP, seviyeler ve unvanlar, çalışma zamanlayıcısı, önerilen rotalar, kendi
notlarınız, genel arama, tanıtım turu, Türkçe/İngilizce arayüz, açık/koyu
tema ve uygulama içi güncelleme hazırdır.

Altı patika tamamlanmıştır: **Python Temelleri**, **Veri Bilimi**, **Makine
Öğrenmesi**, **SQL**, **Zaman Serileri** ve **Matematik**. Matematik
patikası iki modülden oluşur: sıfırdan başlayan biri için temel matematik ve
makine öğrenmesinin dayandığı doğrusal cebir, kalkülüs, olasılık ve
istatistik. Toplamda 140 bölüm, 4026 sınav sorusu, 420 kod alıştırması ve
300 matematik problemi bulunur. API, Docker ve diğer ileri patikalar
hazırlanmaktadır.

Programı ilk kez kullanıyorsanız **Ayarlar › Öğrenme › Tanıtım turu**
bütün ekranları sırayla gösterir.

Alıştırmaya bağlı olmayan serbest bir çalışma alanı ve macOS sürümü yol
haritasındadır.

Hangi değişikliğin hangi sürümde geldiğini **Sürüm Notları** ekranından
izleyebilirsiniz.
