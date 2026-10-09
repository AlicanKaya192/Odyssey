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
sonucu verir. Uygulamada dil modeli bulunmaz ve dışarıdaki bir servise
istek gönderilmez; API alıştırmalarının sunucusu da programın içinde çalışır.
Yalnızca Docker Desktop'ın taban imajları indirmesi ve FastAPI sunucusunun
tarayıcıda açılan belge sayfası internete çıkar.

**Verileriniz cihazınızda kalır.** İlerleme, yazdığınız kod ve ayarlar
`%APPDATA%\Odyssey` klasöründeki yerel bir veritabanında tutulur. Hiçbir veri
dışarı aktarılmaz. Yeni sürüme geçildiğinde bu klasöre dokunulmaz; ilerleme
korunur.

**Açık kaynaktır.** Uygulama MIT lisansıyla dağıtılır; kaynak kodu
incelenebilir, değiştirilebilir ve yeniden dağıtılabilir.

## Şu an nerede?

1.0 sürümüyle açık beta dönemi bitti; uygulama uçtan uca çalışır: öğrenme yolu, konu
anlatımı, ders notları, sınavlar, kod alıştırmaları, kademeli ipuçları,
alıştırma ve sınavlarda geçmiş denemeler, ilerleme kaydı, profil, rozetler,
XP, seviyeler ve unvanlar, çalışma zamanlayıcısı, önerilen rotalar, kendi
notlarınız, genel arama, tanıtım turu, Türkçe/İngilizce arayüz, açık/koyu
tema ve uygulama içi güncelleme hazırdır.

On patika tamamlanmıştır: **Python Temelleri**, **Git**, **Veri Bilimi**,
**Makine Öğrenmesi**, **SQL**, **Zaman Serileri**, **Matematik**, **API**,
**Docker** ve **Büyük Veri**. Matematik patikası iki modülden oluşur:
sıfırdan başlayan biri için temel matematik ve makine öğrenmesinin dayandığı
doğrusal cebir, kalkülüs, olasılık ve istatistik. API patikası da iki
modüldür: REST API kullanmak ve FastAPI ile API yazmak. Toplamda 227 bölüm,
6194 sınav sorusu, 879 alıştırma ve 300 matematik problemi bulunur. Doğal
Dil İşleme ve diğer patikalar hazırlanmaktadır.

Programı ilk kez kullanıyorsanız **Ayarlar › Öğrenme › Tanıtım turu**
bütün ekranları sırayla gösterir.

macOS sürümü yol haritasındadır.

Hangi değişikliğin hangi sürümde geldiğini **Sürüm Notları** ekranından
izleyebilirsiniz.
