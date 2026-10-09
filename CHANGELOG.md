# Odyssey — Değişiklik Günlüğü

Uygulama içindeki Sürüm Notları ekranı bu dosyayı gösterir. Yeni bir sürüm
yayınlamadan önce buraya yazılır; hem GitHub'daki sürüm açıklaması hem
uygulamanın içindeki metin aynı kaynaktan gelir.

## Sürüm numaraları nasıl ilerliyor?

`BÜYÜK.ORTA.KÜÇÜK` — üç parça:

- **Küçük** (`1.0.0` → `1.0.1`): yalnızca hata düzeltmeleri.
- **Orta** (`1.0.x` → `1.1.0`): yeni bir patika ya da büyük bir özellik.
- **Büyük** (`1.x` → `2.0.0`): programın büyük ölçüde yeniden kurulduğu bir
  sürüm.

`0.x` sürümleri geliştirme dönemiydi: `0.7.1`'den `0.9.3`'e kadar açık beta,
öncesi alpha. `1.0.0` ilk tam sürüm.

Ders içeriğinin ayrı bir sürümü var (`content_version`). Sadece bir ders notu
düzeltildiğinde uygulamanın tamamı yeniden indirilmiyor.

---

## [1.0.0] — yayınlanmadı

### Eklendi
- **Algoritmalar patikası.** Kendi kodunda algoritma yazmayı ve bir çözümün
  veri büyüyünce nasıl davranacağını önceden söylemeyi öğretiyor. **ALG 1**
  (17 bölüm) temel algoritmalar ve veri yapıları: karmaşıklık, arama ve
  sıralama, hash, yığın, kuyruk, ağaç ve heap. **ALG 2** (17 bölüm) problem
  çözme teknikleri: böl ve fethet, geri izleme, açgözlü yöntemler, dinamik
  programlama, graflar ve en kısa yol, metin ve sayı algoritmaları, rastgele
  ve olasılıksal yöntemler, sezgisel optimizasyon. Derslerdeki her süre ve
  adım sayısı ölçülerek yazıldı; bazı alıştırmalar ancak verimli bir çözümle
  süre sınırına yetişiyor. Yeni rozetler, "Bulmaca Çözücü" ve "Stratejist"
  unvanları, sözlükte algoritma terimleri.

### Değişti
- **Odyssey artık açık beta değil.** 1.0 ilk tam sürüm: açılıştaki
  "Açık Beta" yazısı kalktı, ilk kez kuranlar beta uyarısı yerine kısa bir
  hoş geldiniz penceresi görüyor.
- **Seviyeler yeni patikalara göre genişletildi.** Bir sonraki seviye için
  gereken XP biraz arttı; mevcut seviyeniz birkaç basamak düşebilir.
  Kazandığınız unvanlar sizde kalıyor.

## [0.9.3] — 7 Ekim 2026

### Eklendi
- **API patikası.** İki modül: **API 1** (17 bölüm) REST API kullanmayı
  anlatıyor: adresler, HTTP, JSON, `requests`, kimlik doğrulama,
  sayfalama, hata ve yeniden deneme, bir API'den veri seti kurmak.
  Alıştırmalar programın içindeki bir alıştırma sunucusuna istek atıyor;
  internet gerekmiyor. **API 2** (18 bölüm) masanın öbür tarafı: FastAPI
  ile kendi API'nizi yazmak; doğrulama, CRUD, hata cevapları,
  bağımlılıklar, kimlik doğrulama, SQLite, testler, async ve bir
  makine öğrenmesi modelini sunmak. API 2'de yazdığınız sunucuyu tek
  düğmeyle başlatıp tarayıcıda deneyebiliyor, yan paneldeki **İstek**
  sekmesinden istek gönderebiliyorsunuz.
- **Git patikası.** On yedi bölümde sürüm kontrolü: ilk commit ve üç alan,
  değişikliklere bakmak ve geri almak, `.gitignore`, dallar, birleştirme ve
  çakışmalar, uzak depolar ve GitHub (pull request, fork), stash, geçmişi
  düzenlemek, etiketler, kaybolanı kurtarmak ve iyi alışkanlıklar.
  Alıştırmalar programın içindeki bir Git terminalinde yazılıyor; Git
  kurmanız ya da GitHub hesabı açmanız gerekmiyor, hedefler terminalin
  yanında tek tek işaretleniyor.
- **Docker patikası.** On yedi bölümde konteynerler: imajlar ve katmanlar,
  Dockerfile, önbellek ve `.dockerignore`, portlar, ortam değişkenleri,
  volume, Docker Compose ve çok servisli uygulamalar, imajı küçültmek,
  güvenlik, hata ayıklama ve bir Python API'sini paketlemek. Alıştırmalar
  Dockerfile'ınızı ve compose dosyanızı denetliyor; Docker Desktop açıksa
  imajı gerçekten derleyip çalıştırıyor. Alıştırmaların bıraktığı imajları
  ve SQL veritabanlarını Ayarlar'daki yeni **Depolama** sayfasından
  silebiliyorsunuz.
- **Büyük Veri patikası.** On yedi bölümde belleğe sığmayan veriyle
  çalışmak: belleği ölçmek, veri tipleriyle küçültmek, parça parça okumak,
  Parquet ve bölümlenmiş veri, DuckDB ile dosyada SQL, örnekleme, paralel
  işleme ve dask, MapReduce, Spark'ın mantığı, akan veri ve uçtan uca bir
  veri hattı. Alıştırmaların büyük veri dosyaları bilgisayarınızda
  üretiliyor; Spark ve Kafka bölümlerinde programla gelen küçük
  benzerleri kullanılıyor, kurulum gerekmiyor.
- **Python patikasında JSON bölümü.** Dosya İşlemleri'nin arkasına yeni bir
  bölüm: sözlükleri ve listeleri JSON olarak dosyaya yazıp geri okumak, iç
  içe veride adım adım gezinmek, eksik alanlar ve bozuk dosyalarla başa
  çıkmak; 24 soru ve 7 alıştırma.
- **Veri Mühendisi rotası.** Rotalar'da veriyi bir kaynaktan çekip
  temizleyen, saklayan ve sunan işler için yeni bir rota: Python, Git,
  SQL, pandas, Büyük Veri, API ve Docker, her adımda odaklanılacak
  bölümlerle. Büyük Veri patikası Veri Bilimci ve ML Mühendisi
  rotalarına da isteğe bağlı adım olarak eklendi.

### Düzeltildi
- **Adım adım izleme sınıfları doğru adlandırıyor.** Bir sınıfın gövdesi
  izlenirken panel onu "fonksiyonun içi" diye gösteriyor ve sınıf bitince
  bir değer "geri verdi" diyordu; artık "sınıfın gövdesi" yazıyor.
- **İngilizce arayüzde hata özeti tamamen İngilizce.** Kod hata verince
  özetteki satır bilgisi İngilizce arayüzde de "satır" diye yazılıyordu.

## [0.9.2] — 6 Ekim 2026

### Eklendi
- **Python Temelleri'ne 22 yeni alıştırma.** Başlangıç, Değişkenler,
  Operatörler, Koşullar, Döngüler ve Sözlükler bölümlerinde alıştırma
  sayısı yediye çıktı. Yeniler daha zor ve düşündürmeye yönelik: tırnak
  içinde tırnak, boşluğu boşluğuna hizalı çıktı, işlem önceliği tuzakları,
  artık yıl kuralı, koşulların sırası, asal ve ikiz asal sayılar, en uzun
  Collatz yolculuğu, ikili arama, yıldızdan elmas, kelime sayma, sipariş
  işleme ve sözlüğü ters çevirme gibi. Bu bölümleri daha önce bitirdiyseniz
  bitmiş sayılmaya devam ediyor; yeni alıştırmalar ek alıştırma olarak
  bekliyor.
- **Seviye tespit sınavı.** Bir modülün konularını zaten biliyorsanız
  baştan başlamak zorunda değilsiniz: yolun başındaki karttan isteğe bağlı
  sınava girilince her bölümden dört soru geliyor (en az üçü doğruysa o
  bölümü biliyor sayılıyorsunuz); bildiğiniz bölümler ve arkasındaki ilk
  bölüm açılıyor. Üst üste iki bölüm tutmazsa sınav
  kendiliğinden bitiyor; sonuçta hangi bölümleri bildiğiniz, hangilerini
  tekrar etmeniz gerektiği yazıyor. Açılan bölümler tamamlanmış sayılmıyor.
- **Kodu adım adım izleme.** Python alıştırmalarında **Adım adım**
  düğmesi kodu satır satır oynatıyor: editörde sıradaki satır
  işaretleniyor, altta her adımdaki değişkenler ve o ana kadarki çıktı
  görünüyor. Yeni gelen değişken yeşil, değeri değişen sarı; fonksiyonun
  içine girildiğinde kendi değişkenleri ayrı gösteriliyor, bitince ne
  döndürdüğü yazıyor. Oklarla ileri geri gidiliyor. Kodunuz boşsa ya da
  nereden başlayacağınızı bilmiyorsanız **Örnek çözüm**'e geçip doğru
  çözümün satır satır nasıl ilerlediğini izleyebilirsiniz (kendi kodunuz
  yerinde kalıyor). "Takıldın mı?" kartından da açılıyor.
- **Terimler sözlüğü.** Derslerde, ders notlarında ve alıştırma
  yönergelerinde terimler ilk geçtikleri yerde noktalı altı çizgiyle
  işaretli; üzerine gelince kısa açıklaması çıkıyor ("parametre neydi?"
  diye dersten çıkmaya gerek kalmıyor). Bütün terimler Hakkında'daki yeni
  **Sözlük** sekmesinde patikalara göre toplu; `Ctrl+K` ile de aranıyor.
- **Takıldığında dersin ilgili kısmına yönlendirme.** Bir alıştırmada üç
  kez üst üste olmayınca yönergenin altında "Takıldın mı?" kartı çıkıyor:
  alıştırmanın dersteki hangi başlığa dayandığını söylüyor ve **Derse git**
  o başlığı açıyor.
- **İlerlemeyi başka bir bilgisayara taşıma.** Ayarlar'daki yeni **Veri**
  sayfasından ilerlemeniz, notlarınız, ayarlarınız ve profil fotoğrafınız
  tek bir `.odyssey` dosyasına aktarılıyor; başka bir bilgisayarda aynı
  sayfadan içe aktarılınca Odyssey yeniden başlıyor ve kaldığınız yerden
  devam ediyorsunuz. O bilgisayardaki eski ilerleme silinmiyor, yedekte
  kalıyor. Otomatik yedeklerin klasörü de aynı sayfadan açılıyor.
- **Hatalı satır editörde işaretleniyor.** Kod hata verince o satır
  editörde kırmızımsı bir zeminle boyanıyor, numarası işaretleniyor ve
  satır görünmüyorsa oraya kaydırılıyor; kodu değiştirince işaret kalkıyor.
- **Daha fazla hata açıklaması.** Terminaldeki 💡 açıklamaları 28 yeni
  hatayı tanıyor: değeri olmayan (`None`) değişkenle işlem, ondalıkta
  virgül, bulunamayan dosya, kendini durmadan çağıran fonksiyon, tabloda
  olmayan sütun, değişken ve değer sayısının tutmaması, koşulda tek `=`,
  makine öğrenmesinde boş değer ve tablo boyutu hataları gibi. Windows'un
  Akıllı Uygulama Denetimi bir alıştırmanın kütüphanesini engellerse bunun
  kodla ilgisi olmadığı söyleniyor.
- **Sınavda klavye.** Şıkları 1–4 ya da A–D tuşlarıyla seçip Enter ile
  cevaplayabiliyor ve sonraki soruya geçebiliyorsunuz.
- **Okuma odağı.** Bölüm başlığındaki çerçeve düğmesi ya da `F11` dersi tam
  ekranda, sol menü ve şeritler olmadan açıyor. Çıkmak için `Esc` ya da
  `F11`; girerken ekranın üstünde bunu hatırlatan bir yazı çıkıyor.
- **Paylaşım kartı.** Profildeki "Paylaşım kartını kaydet" düğmesi
  seviyenizi, unvanınızı, ilerlemenizi, son kazandığınız rozetleri ve son
  bir yıldaki çalışma tablonuzu tek bir resimde kaydediyor; LinkedIn gibi
  yerlerde paylaşabilirsiniz. Profil düzenleme penceresine GitHub kullanıcı
  adınızı yazarsanız kartın köşesinde görünüyor.
- **Aramadan komut çalıştırma.** `Ctrl+K` artık yalnızca içerik bulmuyor:
  "tema", "dil", "zamanlayıcı", "tur", "kısayol" ya da "menü" yazınca
  o işi yapan komut çıkıyor.
- **"Bu sayfada sorun mu var?" düğmesi.** Bölüm başlığındaki bayrak
  simgesi, bu sayfanın bilgileri önceden yazılmış bir GitHub hata
  bildirimi açıyor; yanlış bir bilgiyi ya da çalışmayan bir alıştırmayı
  tarif etmeden bildirebiliyorsunuz. Program hiçbir şey göndermiyor.
- **İlerlemenizin günlük yedeği.** Program her gün açıldığında ilerleme
  dosyanızın bir kopyasını alıyor ve son üç günü saklıyor. Elektrik kesintisi
  ya da disk hatası yüzünden dosya bozulursa program bunu açılışta fark
  edip en yeni sağlam yedeği yerine koyuyor ve size söylüyor; bozuk dosya
  silinmiyor.
- **Günlük kaydı.** Bir şey ters gittiğinde sebebi `%APPDATA%\Odyssey\logs`
  klasöründeki bir dosyaya yazılıyor; hata bildirirken bu dosyayı
  ekleyebilirsiniz. Yazdığınız kod, notlarınız ve cevaplarınız kayda
  girmiyor, dosya hiçbir yere gönderilmiyor.

### Değişti
- **Güncellemeden sonra "Neler yeni?" penceresi.** Program güncellendikten
  sonraki ilk açılışta beta uyarısı yerine o sürümün en önemli beş
  yeniliği çıkıyor; "Tüm sürüm notları" Sürüm Notları ekranını açıyor.
- **Sınav ekranı yenilendi.** Başlangıç kartında daha önceki denemelerinizin
  özeti (en iyi puan, son puan, deneme sayısı) ve sınavın nasıl ilerlediği,
  soru kartında "Soru 3 / 10", sonuç kartında kaç doğru, yanlış ve boş
  bıraktığınız ve ne kadar sürdüğü görünüyor.
- **Tanıtım turu yeni özellikleri de gösteriyor:** seviye tespit sınavı,
  terimler sözlüğü, okuma odağı ve sorun bildirme, adım adım izleme ve
  paylaşım kartı. Turu Ayarlar › Öğrenme'den yeniden başlatabilirsiniz.
- **Güncelleme kurulurken ekranda pencere kalıyor.** İndirme bitip Odyssey
  kapandıktan sonra yeni sürüm açılana kadar ekranda hiçbir şey olmuyordu;
  program çöktü sanılabiliyordu. Artık bu arada küçültülebilen bir
  "Odyssey güncelleniyor" penceresi duruyor ve yeni sürüm açılınca
  kendiliğinden kapanıyor. Bu, 0.9.2'den sonraki güncellemelerde görünür.
- **Yarıda bırakılan sınavın cevapları kaybolmuyor.** Sınavdan bitirmeden
  çıktığınızda (ya da programı kapattığınızda) o ana kadar verdiğiniz
  cevaplar Geçmiş denemeler'e "yarıda bırakıldı" olarak kaydediliyor;
  yanlışlarınıza oradan bakabiliyorsunuz. Bu deneme puan sayılmıyor.
- **İpuçları yenilendi.** Bir rozetin, serinin alevinin, seviye çubuğunun ya
  da bir düğmenin üzerine gelince çıkan bilgi kartı artık programın
  temasında, beklemeden ve takılmadan açılıyor; başlık, renkli bir durum
  satırı (örneğin serinin ne zaman biteceği) ve açıklama olarak okunuyor.

### Düzeltildi
- Windows güncellemenin kurulum dosyasını engellediğinde (örneğin Akıllı
  Uygulama Denetimi) güncelleme penceresi "indirilemedi" diyordu. Artık
  gerçek sebebi ve ne yapılabileceğini söylüyor.

## [0.9.1] — 30 Eylül 2026

### Eklendi
- **Zaman Serileri patikası eklendi.** 23 bölüm, üç seviye: **Temel**
  tarihlerle ve zaman indeksiyle çalışmak, yeniden örnekleme, pencereler;
  **Orta** ayrıştırma, durağanlık, otokorelasyon, eksik ve aykırı değerler,
  taban çizgi ve tahmini doğrulamak; **İleri** üstel düzleştirme, ARIMA, dış
  değişkenler, makine öğrenmesiyle tahmin, tahmin aralıkları, anomali ve
  değişim noktası. Son bölüm hepsini tek bir işte birleştiriyor: dağınık
  bir dökümden aralığı olan 28 günlük tahmine. 153 alıştırma, 628 sınav
  sorusu ve üç yeni rozet.
- **Seviye ve unvanlar.** Tamamladığınız her bölüm ve kazandığınız her rozet
  XP kazandırıyor; rozetler bölümlerden fazla, zor rozetler daha da fazla
  veriyor. XP biriktikçe seviye atlıyorsunuz (50 seviye, her biri bir
  öncekinden daha çok XP istiyor) ve sağ altta kendi sesiyle bir kart
  çıkıyor. Profilde adınızın altında seviyeniz ve XP çubuğu var. Belirli
  seviyelerde, bir patikanın tamamını bitirince ve birkaç zor koşulda
  **unvan** kazanıyorsunuz; adınızın altındaki unvana tıklayıp
  kazandıklarınızdan birini seçebiliyorsunuz, kilitli olanların üzerine
  gelince nasıl kazanılacağı yazıyor. Daha önce bitirdiğiniz bölümler ve
  kazandığınız rozetler de sayılıyor.
- **Çalışma zamanlayıcısı.** Alt şeridin sağındaki saat simgesinden bir
  düzen seçip başlatabiliyorsunuz: Pomodoro (25 / 5, dört turda bir uzun
  mola), 52 / 17, derin çalışma (90 / 20), kısa adımlar (15 / 3) ya da
  kendi süreleriniz. Kalan süre alt şeritte küçük bir sayaç olarak akıyor
  ve yalnızca son saniyelerde hafifçe büyüyor; duraklatabilir, molayı
  atlayabilir ya da bitirebilirsiniz. Tur ya da mola bitince kısa bir sesle
  kart çıkıyor, program arkadaysa Windows bildirimi geliyor. Tamamlanan
  odak turları o günün çalışması sayılıyor, seriye ve etkinlik takvimine
  işleniyor.
- **Geçmiş denemeler.** Alıştırmalarda yeni **Denemelerim** sekmesi: son
  doğru çözümünüz ve yanlış denemeleriniz, her birinin neden geçmediğiyle
  birlikte; yanlış denemede doğru çözümünüzde olmayan satırlar kırmızıyla
  işaretli. Matematik problemlerinde denediğiniz cevaplar listeleniyor.
  Sınavda **Yanlışlarımı gör** ve **Geçmiş denemeler**: her denemede hangi
  soruya ne cevap verdiğiniz, doğrusu ve açıklaması. Bu sürümden sonraki
  denemeler kaydediliyor.
- **Tanıtım turu.** İlk açılışta (ve bu güncellemeden sonra bir kez)
  programı tanıtan kısa bir tur isteyip istemediğiniz soruluyor. Turda
  Odyssey'in sentoru rehberlik ediyor ve programın her parçasını sırayla
  gösteriyor: patikalar, bir bölümün sekmeleri, ders, not, sınav,
  alıştırma ekranı, profil, rozetler, rotalar, notlar, arama, çalışma
  zamanlayıcısı ve ayarlar. Tur her an bırakılabiliyor ve Ayarlar ›
  Öğrenme'den yeniden başlatılabiliyor.

### Değişti
- **Sınavdan yanlışlıkla çıkılmıyor.** Sınav sürerken başka bir sekmeye,
  bölüme ya da ekrana geçmek istediğinizde soruluyor; "Sınavdan çık"
  derseniz o deneme iptal oluyor ve sayılmıyor.
- **Güncellemeler artık yalnızca değişen dosyaları indiriyor.** Bir önceki
  sürümü kurulu olan, 233 MB'lık tam kurulum yerine yalnızca o sürümden bu
  yana değişen dosyaları içeren küçük bir güncelleme paketi alıyor (bu
  sürümden sonrakiler için). Paket kurulu sürümü denetliyor; uymazsa hiçbir
  dosyaya dokunmuyor ve program bir sonraki denemede tam kurulumu indiriyor.
  0.9.1'e geçiş son kez tam kurulumla oluyor.

### Düzeltildi
- Güncellemeden sonra masaüstü kısayolu eski simgeyi göstermeye devam
  ediyordu. Kurulum artık Windows'a simgeleri yeniletiyor.

## [0.9.0] — 29 Eylül 2026

### Eklendi
- **Python patikasına yeni ilk bölüm: Paketler ve Ortamlar.** pip ve
  `python -m pip`, sanal ortamlar (`venv`), `requirements.txt`, Anaconda ve
  conda, ikisinin farkı; VS Code ve Jupyter'i ortama bağlamak ve sık
  karşılaşılan kurulum hataları. Ezberlenecek komutlar bir komut kartında
  toplu, bölüm 24 soruluk bir sınavla bitiyor. Python'a daha önce başlamış
  olanların bölümleri açık kalıyor, kazanılmış rozetleri de korunuyor.

### Değişti
- **Arayüz yenilendi.** Ekranlar arasında yumuşak geçişler, yeni simgeler
  ve patika logoları, madalya biçiminde rozetler. Ayarlar › Görünüm ›
  Animasyonlar ile hareket azaltılabiliyor.
- **Yeni açılış.** Program açılırken yükleme kartı yerine kısa, sesli bir
  animasyon oynuyor: Odyssey'in maskotu, yay tutan bir sentor, dörtnala
  gelip okunu atıyor ve ok hedefi tam ortadan vuruyor. Tıklayınca ya da
  `Esc` ile geçilebiliyor; ses Ayarlar › Bildirimler › Sesler'den
  kapatılabiliyor. Sentor Öğrenme Yolu'ndaki karşılama kartında da duruyor
  ve genel ilerlemenizi gösteren hedefe nişan alıyor. Uygulama simgesi de
  artık o.
- **Güncelleme penceresi yenilendi.** İndirilen ve toplam boyut, hız ve
  kalan süre anlık görünüyor; pencere küçültülüp arka planda bırakılabiliyor,
  indirme sürerken Odyssey kullanılmaya devam edilebiliyor. İndirme bitince
  kurulum pencere açmadan yapılıyor ve Odyssey yeni sürümüyle açılıyor.
- **Rotalar daha açıklayıcı.** Her adımda o patikada neler olduğu, adımın
  sonunda neler yapabileceğiniz ve yaklaşık süresi yazıyor. Odaklanılacak
  bölümlerin her birinin neden önemli olduğu da yazıyor; açık bir bölüme
  tıklayınca doğrudan açılıyor.
- **Discord'da bulunduğunuz ekran görünüyor.** Rotalar'da seçili rota,
  Notlarım, Profilim, Hakkında ve Sürüm Notları da yazıyor; önce bölüm
  dışındaki her ekran "Öğrenme yolunda" görünüyordu. Notlarınızın adı ya da
  içeriği gönderilmiyor.
- **Seri daha anlaşılır.** Programı kapatırken çıkış penceresi serinizin
  bugün güvende olup olmadığını söylüyor. Alevin üzerine gelince serinin ne
  zaman biteceği geri sayımla yazıyor ve bir günün neyle sayıldığı
  görünüyor. Bir bölümde 2 dakika çalışmak da o günü sayıyor; önce yalnızca
  bir dersi sonuna kadar okumak, alıştırma çalıştırmak ya da sınava girmek
  sayılıyordu.

### Düzeltildi
- **Hatırlatmalar programı kullandığınız gün gelmiyor.** Programı sabah
  açıp konulara bakan birine akşam "seriniz tehlikede" ya da "3 gündür
  yoksunuz" bildirimi gidebiliyordu. "Yoksunuz" artık programın en son
  açıldığı günden sayılıyor.
- **Güncelleme sırasında masaüstü kilitlenmiyor.** "Güncelle"ye basınca açılan
  pencere başka pencerelere geçmeyi engelliyordu (Alt+Tab ve görev çubuğu
  cevap vermiyordu). Düzeltme 0.9.0'dan sonraki güncellemelerde geçerli:
  0.8.3'ten 0.9.0'a geçerken güncellemeyi hâlâ eski sürümün penceresi yapıyor.

## [0.8.3] — 26 Eylül 2026

### Eklendi
- **Matematik patikası eklendi.** İki modül var: **MAT 1 — Temel
  Matematik**, sıfırdan başlayan biri için sayılardan fonksiyonlara,
  geometri ve trigonometriye, olasılık ve istatistiğe kadar; **MAT 2 —
  Yapay Zekanın Matematiği**, makine öğrenmesinin dayandığı doğrusal cebir,
  kalkülüs, olasılık ve istatistik. Problemler çizim kâğıdında çözülüyor;
  yalnızca sonuç denetleniyor, çözüm yolları solda açılıyor.
- **Seri hatırlatmaları.** O gün çalışmadıysanız seçtiğiniz saatte esprili
  bir Windows bildirimi geliyor; seri tehlikedeyse 21:30'da son bir uyarı,
  uzun süre uğramazsanız giderek seyrekleşen ve iki ay sonra duran
  hatırlatmalar. Program kapalıyken de çalışıyor: bunun için Windows Görev
  Zamanlayıcı'ya günde birkaç saniye çalışan küçük bir görev ekleniyor,
  internete hiçbir şey gitmiyor. İlk açılışta isteyip istemediğiniz
  soruluyor; saat ve açma kapama Ayarlar › Bildirimler'de.
- **Sol menü gizlenebiliyor.** Şeridin kenarındaki küçük düğmeyle ya da
  `Ctrl+M` ile; içeriğe daha fazla yer kalıyor ve tercih hatırlanıyor.
- **Odyssey artık kurulum programıyla geliyor.** Uygulama kendi kullanıcı
  hesabınıza kuruluyor; Başlat menüsünde ve masaüstünde kısayolu oluyor,
  `_internal` klasörüyle uğraşmanız gerekmiyor. Çıkardığınız bir klasörden
  uygulamanın içinden güncellediğinizde yeni sürüm kurulur ve eski klasördeki
  program dosyaları kaldırılır; ilerlemeniz, notlarınız ve ayarlarınız
  korunur. Uygulama Ayarlar › Uygulamalar'dan kaldırılabiliyor.
- **Rotalar.** Sol şeritte, Notlarım'ın üstünde yeni bir ekran: hangi
  patikanın hangi sırayla çalışılacağını anlatıyor. Üç rota var — hiç kod
  yazmamış biri için, Python bilip veri bilimine geçmek isteyen biri için ve
  ML mühendisi olmak isteyen biri için. Her adımda neden o sırada olduğu,
  hangi bölümlere odaklanılacağı ve ne kadarını bitirdiğiniz yazıyor; henüz
  yazılmamış patikalar da "Yakında" diye yerinde duruyor.
- **Editörde yazma kolaylıkları.** Parantez ve tırnak kendiliğinden
  kapanıyor; kapatan karaktere basınca imleç üstünden geçiyor, boş bir çifti
  `Backspace` birlikte siliyor, seçili metin parantez ya da tırnak içine
  alınıyor. `Tab` ve `Shift+Tab` seçili satırların hepsine girinti ekleyip
  çıkarıyor; girintideki `Backspace` bir kademe siliyor. `Enter`, `(|)`
  arasında içeriği kendi satırına alıyor, `return` ya da `pass` sonrası
  girintiyi azaltıyor. `Ctrl+/` seçili satırları yoruma alıyor ya da
  yorumdan çıkarıyor. Girintiyi gösteren soluk dikey çizgiler blokların
  nerede başlayıp bittiğini gösteriyor. Aynı kolaylıklar Notlarım'daki kod
  bloklarının içinde de çalışıyor.
- **Seri alevi büyüyor.** Karşılama kartındaki seri sayısının yanında bir
  alev var; seriniz uzadıkça rengi ve boyu değişiyor, küçük sarı bir
  kıvılcımdan yüz günün sonunda altın bir aleve dönüşüyor. Üstüne
  gelince bir sonraki aşamaya kaç gün kaldığı yazıyor.
- **Alt şeritte GitHub yıldızı.** Sol altta Odyssey'in GitHub'daki yıldız
  sayısı duruyor; tıklayınca depo açılıyor, beğendiyseniz oradan yıldız
  verebilirsiniz. Sayı yeni sürüm denetimiyle birlikte güncelleniyor ve
  Ayarlar › Güncelleme'den denetim kapatılırsa ağa hiç çıkılmıyor.

### Değişti
- **Alıştırma sonuçları terminalde.** Kodu çalıştırınca açılan sonuç paneli
  yerine editörün altında her zaman duran bir terminal var: programınızın
  çıktısı, hatalar ve ne anlama geldikleri, geçti/geçmedi ve tutmayan
  çıktıda beklenenle sizinki alt alta, hizalı. Kodunuz grafik ürettiyse ya
  da çok satırlı bir tablo tutmadıysa soldaki **Çıktı** sekmesi açılıyor:
  grafik tam genişlikte, beklenen ve sizin çıktınız satır satır, tutmayan
  satırlar işaretli. Terminal ile editör arasındaki ayırıcı sürüklenerek
  büyütülüp küçültülebiliyor.
- **Veri Bilimi patikası yenilendi.** On üç alıştırma baştan yazıldı:
  artık içe aktarmaları siz yazıyor, veriyi alıştırmanın yanındaki bir CSV
  dosyasından okuyorsunuz ve çizdiğiniz grafik ekranda görünüyor.
  Görselleştirme bölümünün beş alıştırmasının beşi de yenilendi; yanıltıcı
  ve dürüst eksenli grafiği yan yana gördüğünüz bir alıştırma da var.
  DataFrame Temelleri, Seçim ve Filtreleme, Gruplama ve Toplulaştırma, Veri
  Temizleme, Keşifçi Veri Analizi ve Genel Tekrar bölümlerine de dosyadan
  başlayan alıştırmalar geldi. DataFrame konu anlatımına CSV dosyası okumayı
  anlatan bir kısım, sınavlara 55 yeni soru eklendi; Genel Tekrar dışındaki
  her bölümde artık 35 soru var. Bu bölümleri daha önce bitirdiyseniz yeni
  alıştırmaları çözene kadar bölüm "yarım kaldı" görünür.
- **Ayarlar penceresi yenilendi.** Ayarlar artık soldaki kategorilerde
  duruyor: Görünüm, Öğrenme, Bildirimler, SQL ve Güncelleme. Her sayfada
  ne işe yaradığını anlatan kısa bir açıklama var; pencere her sayfada aynı
  boyutta kalıyor. "Discord'da göster" Görünüm sayfasına taşındı.
- **Arama sol şeridin ortasında.** Şeridin ortasındaki genel ilerleme
  halkası kaldırıldı; aynı yüzde öğrenme yolu ekranında zaten yazıyor.
  Yerine arama düğmesi geldi.
- **Rozet ve bölüm kutlamaları sağ altta.** Alt şeritteki bildirim zili
  kaldırıldı. Bir bölümü bitirdiğinizde ya da rozet kazandığınızda sağ altta
  simgesiyle birlikte bir kart beliriyor ve birkaç saniye sonra kendiliğinden
  kapanıyor; üstüne gelince bekliyor, çarpıyla hemen kapatılabiliyor, rozet
  kartına tıklayınca profil açılıyor. Kartla birlikte kısa bir kutlama sesi
  çalıyor; Ayarlar › Bildirimler'den kapatılabiliyor. Kısayollar düğmesi
  zilin yerine, sağ alta geçti.

### Düzeltildi
- **Makine Öğrenmesi alıştırmalarında zorluk yazısı boş kalmıyor.** Yirmi
  alıştırmada "Zorluk:" yazısının yanı boştu; artık zorluk noktaları
  görünüyor.
- **Ayarları açıp kapatınca program çökmüyor.** Ayarlar kapanırken arka
  planda SQL veritabanlarını sayan iş yarıda kesiliyor ve program
  beklenmedik şekilde kapanıyordu.
- **Program kapanırken çökmüyor.** Açılıştaki güncelleme denetimi sürerken
  ya da bir alıştırma çalışırken programı kapatmak onu çökertebiliyordu.
- **Geri alma ilk basışta çalışıyor.** Bir alıştırma ya da not açıldıktan
  sonra `Ctrl+Z`'nin ilk birkaç basışı görünür hiçbir şey yapmıyordu.
  Artık doğrudan son yaptığınız değişikliği geri alıyor.
- **İpucu açınca ekran zıplamıyor.** Bir ipucunu açmak yönergenin tamamını
  yeniden yüklüyordu; sayfa bir an en başa gidip eski yerine dönüyordu.
  Artık yalnızca ipucu kutusu değişiyor, okuduğunuz yer kıpırdamıyor.
  Açtığınız ipucu "Gizle" ile yeniden kapatılabiliyor.
- **SQL kodu her yerde renkli.** SQL patikasının konu anlatımlarında, ders
  notlarında ve Notlarım'daki SQL kod blokları renksizdi; sınav sorularındaki
  ve alıştırma editöründeki SQL ise Python kurallarıyla renkleniyordu
  (`SELECT` renksiz, `--` yorumu yorum gibi görünmüyordu). Artık SQL her
  yerde kendi kurallarıyla renkleniyor.
- **Değişen alıştırmalar bölümü tamamlanmış göstermiyor.** Bir alıştırma
  yenisiyle değiştirildiğinde eskisini çözmüş olmak, yenisi çözülmemişken
  bölümü "tamamlandı" gösteriyordu. Artık yalnızca bölümdeki güncel
  alıştırmalar sayılıyor.
- **Doğru ama farklı yazılmış çözümler kabul ediliyor.** "Döngü ile yaz"
  ya da "koşul kullan" diyen alıştırmalarda liste kavraması
  (`[x for x in liste if ...]`) veya tek satırlık koşul
  (`a if koşul else b`) yazınca, sonuç doğru olsa bile alıştırma geçmiyordu.
  Artık bunlar da döngü ve koşul sayılıyor. Alıştırma gerçekten başka bir
  yöntem istiyorsa sonuç da "yanlış" yerine "Sonucun doğru, ama bu
  alıştırma şu yöntemin pratiği için" diye açıklanıyor.

---

## [0.8.2.1] — 16 Eylül 2026

### Değişti
- **Güncelleme sistemi kurulum programına hazırlandı.** Bir sonraki sürüm
  bir kurulum dosyası olarak gelecek: güncellemeye bastığınızda Odyssey
  kendini kurar, masaüstüne kısayol bırakır ve eski klasördeki program
  dosyalarını kaldırır. İlerlemeniz, notlarınız ve ayarlarınız korunur. Bu
  sürüm yalnızca o geçişi mümkün kılıyor; başka bir değişiklik yok.

---

## [0.8.2] — 16 Eylül 2026

### Eklendi
- **Python Temelleri'ne iki yeni bölüm.** **Metinleri Biçimlendirme:**
  f-string biçim belirteçleri — ondalık basamak sayısı, binlik ayırıcı,
  yüzde, hizalama ve sütun genişliği, sayıların hizalı tablo hâlinde
  yazdırılması. **Kavrama İfadeleri:** liste, sözlük ve küme kavramaları,
  süzgeç ile koşullu değer ayrımı, iç içe kavrama ve üreteç ifadeleri.
  Her bölümde konu anlatımı, iki ders notu, on beş soruluk sınav ve beş
  alıştırma var.
- **Notlarım.** Sol şeritteki defter simgesi kendi notlarınızı açıyor. Notlar
  patikalara göre klasörleniyor; her nota bir ad veriyorsunuz ve isterseniz
  bir derse bağlıyorsunuz, o zaman notun üstünden o derse dönebiliyorsunuz.
  Kendi klasörlerinizi de açabilir, notları klasörler arasında
  taşıyabilirsiniz; bir klasörü silmek içindeki notları silmiyor.
  Notlar markdown ile yazılıyor: araç çubuğundaki Kod düğmesi Python ya da
  SQL kod bloğu ekliyor ve kod, konu anlatımındaki gibi renkli görünüyor.
  Bir dersin içindeyken başlıktaki "Not al" düğmesi (`Ctrl+N`) notu dersin
  yanında açıyor: dersten seçtiğiniz bir yeri sağ tıklayıp nota
  ekleyebiliyor, alıştırmada yazdığınız kodu tek düğmeyle nota
  koyabiliyorsunuz. Yazdıklarınız kendiliğinden kaydediliyor. Notlarınızı
  tek tek (`.md`) ya da klasör klasör (`.zip`) indirebilir, başkasından
  aldığınız notları yükleyebilirsiniz; yüklenen not hiçbir notunuzun
  üstüne yazılmıyor.
- **Genel arama.** `Ctrl+K` ya da sol şeritteki büyüteç ekranın ortasında
  bir arama kutusu açıyor; yazdıkça altında öneriler çıkıyor. Bölümler,
  konu anlatımlarının başlıkları ve metni, ders notları, alıştırmalar,
  kendi notlarınız ve ekranlar aranıyor. Bir sonuca basınca doğrudan
  oraya gidiliyor: konu anlatımında ilgili başlığa kaydırılıyor, ders
  notunda o not, alıştırmada o alıştırma açılıyor. Türkçe harfler olmadan
  yazılan arama da buluyor ("dongu" → "Döngüler").
- **Klavye kısayolları listesi.** Alt şeritteki klavye simgesi ya da `F1`
  kısayolların listesini açıyor: arama, not alma, kodu çalıştırma ve
  diğerleri. Kısayollar hiçbir yerde yazmıyordu.
- **Alıştırmalarda bellek sınırı.** Durmadan büyüyen bir liste ya da çok
  büyük bir dizi artık bilgisayarınızın belleğini tüketmiyor: kod 3 GB'ı
  geçince durduruluyor ve sonuç alanında sebebi yazıyor. Eskiden böyle bir
  kod, süre sınırı dolana kadar belleğin tamamını bitirip bilgisayarı
  yavaşlatabiliyordu.

---

## [0.8.1] — 15 Eylül 2026

### Eklendi
- **SQL patikasının 2. kısmı.** İçindeki bölümler — **Orta Seviye:** Tablo
  Tasarımı, Tarih ve Metin. **İleri Seviye:** Pencere Fonksiyonları, WITH ve
  Özyineleme, Dizinler, Görünümler ve Saklı Yordamlar, Genel Tekrar. Her
  bölümün kendi notları, sınavı, alıştırmaları ve rozeti var; patikanın
  tamamını bitirene de ayrı bir rozet.
- **Bildirimler.** Alt şeridin sağındaki zil kazandığınız rozetleri
  listeliyor; okunmamışların sayısı zilin üstünde duruyor. Her birini okundu
  sayabilir ya da hepsini temizleyebilirsiniz.

---

## [0.8.0] — 10 Eylül 2026

### Eklendi
- **SQL patikasının 1. kısmı eklendi.** Sorguları Odyssey'in içinde
  yazıyorsunuz, kendi bilgisayarınızdaki SQL Server çalıştırıyor. İçindeki
  bölümler — **Başlangıç:** Kurulum, SELECT ve WHERE, Sıralama ve Sınırlama,
  Filtreleme Desenleri, Hesaplanan Sütunlar, Gruplama. **Orta Seviye:**
  Tabloları Birleştirmek, Alt Sorgular, Veri Değiştirmek. Her bölümün kendi
  notları, sınavı, alıştırmaları ve rozeti var. Alıştırmalarda tabloları
  ayrı bir pencerede görebiliyor, açılan veritabanlarını Ayarlar'dan
  silebiliyorsunuz.

### Düzeltildi
- **Sınavdan ve alıştırmadan sonra ilerlemenin yolu yoktu.** Ders ve not
  sayfalarının altında "ileri" düğmesi varken sınav sonucunda ve
  alıştırmada yoktu; devam etmek için sağ üstteki sekmeleri ya da
  alıştırma numaralarını aramak gerekiyordu. Artık sınav bitince
  "Alıştırma →", her alıştırmanın altında "Sonraki alıştırma →", sonuncuda
  da bölüm bittiyse "Sonraki →" duruyor.
- **Ders notlarındaki dış bağlantılar açılmıyordu.** Python kurulum
  notundaki indirme adresine tıklandığında hiçbir şey olmuyordu; artık
  tarayıcıda açılıyor.
- **Derslerdeki terim tabloları yapışık çıkıyordu.** "Sözlük" gibi
  bölümlerde terim ile açıklaması arada boşluk olmadan tek satırda
  akıyordu: "örnek (sample)tablodaki bir satır". Artık iki sütun hâlinde,
  aralarında ayraçla duruyor.
- **Discord'daki yazı geç çıkıyordu.** Uygulama açıldığında görünmüyor,
  ancak bir bölüme girdiğinizde ya da bir dakika sonra beliriyordu.

---

## [0.7.5] — 7 Eylül 2026

### Eklendi
- **Sırada ne var, yol ekranında görünüyor.** Hazırlanmakta olan patikalar
  ana ekrana eklendi: Zaman Serileri, Doğal Dil İşleme, Üretken Yapay Zekâ,
  Algoritmalar, Yapay Zekâ Matematiği, Temel Kütüphaneler ve Sistem
  Tasarımı.

### Düzeltildi
- **Alıştırma editöründe Enter iki adımda çalışıyordu.** Yeni satır
  açmadan önce bulunduğunuz satırla bir sonraki birbirine yapışıyor, ikinci
  Enter'da yerine oturuyordu.
- **Sınav ilk sorudan değil, sayfanın ortasından başlıyordu.**

---

## [0.7.4] — 4 Eylül 2026

### Eklendi
- **Makine Öğrenmesi patikası tamamlandı.** İçindeki bölümler: Makine
  Öğrenmesi Nedir?, İlk Model, Regresyon Metrikleri, Sınıflandırma, Modele
  Veri Hazırlamak, Doğrulama ve Aşırı Öğrenme, KNN, Karar Ağaçları, Topluluk
  Yöntemleri, Dengesiz Veri, Denetimsiz Öğrenme, Pipeline ve Modeli
  Kaydetmek, Genel Tekrar. On üç bölümde yirmi altı not, 513 sınav sorusu,
  altmış beş alıştırma ve beş uçtan uca proje var; alıştırmalarda
  scikit-learn ile kendi modellerinizi eğitip ölçüyorsunuz.
- **Discord'da görünüyor.** Discord açıkken profilinizde Odyssey'i
  kullandığınız, hangi modül ve bölümde olduğunuz ve ne kadar süredir
  çalıştığınız görünüyor; altındaki iki düğme projenin sayfasına ve son
  sürüme gidiyor.
  Yazı sizin seçtiğiniz dilde. Ayarlardan kapatılabiliyor.
  Discord kurulu değilse ya da kapalıysa hiçbir şey değişmiyor: uygulama
  bunu fark etmiyor bile, sonradan açarsanız kendiliğinden bağlanıyor.
- **Alıştırmalar uzadı.** Makine Öğrenmesi alıştırmalarında başlangıç kodu
  artık hazır `import` satırları vermiyor; hangi aracın nereden geldiğini
  sen yazıyorsun.
- **On dört yeni rozet:** *Modele İlk Adım*, *İlk Model*, *Hata Okuyucu*,
  *Sınıflandırıcı*, *Sızıntı Avcısı*, *Dürüst Ölçüm*, *Komşuluk*,
  *Kural Okuyucu*, *Orman Bekçisi*, *Nadir Sinyal*, *Grup Bulucu*,
  *Tek Parça*, *Tekrarcı* ve *Makine Öğrenmesi Ustası*.
- **Çizdiğin grafik artık ekranda görünüyor.** Bir alıştırma grafik
  kaydediyorsa, çalıştırdıktan sonra sonuç panelinde grafiğin kendisi
  çıkıyor. Önceden dosya üretiliyor, doğru olup olmadığı söyleniyor ve
  siliniyordu; ne çizdiğini göremiyordun.
- **Makine Öğrenmesi için scikit-learn de pakete girdi.** NumPy, pandas ve
  matplotlib gibi o da uygulamanın içinde geliyor; ayrıca bir şey kurmak
  gerekmiyor. İndirilen dosya bu yüzden büyüdü.

### Düzeltildi
- **İpuçları artık tek tek açılıyor.** Alıştırmalarda son ipucuna basmak
  öndeki bütün ipuçlarını da açıyordu; kademeli yardım fikri tek tıklamayla
  ortadan kalkıyordu. Artık hangisine basarsan yalnızca o açılıyor.
- **Son ipucu her alıştırmada çözümü veriyor.** Bazı alıştırmalarda son
  kademe "çözümün tamamı" diyor ama yalnızca bir parçasını gösteriyordu.

---

## [0.7.3.1] — 3 Eylül 2026

### Değişti
- **Güncelleme kutusuna her yerden ulaşılıyor.** Pencerenin altındaki
  "Yeni sürüm" yazısına tıklamak artık tarayıcıyı açmak yerine güncelleme
  kutusunu açıyor; oradan ister kurabiliyor, ister sürüm sayfasına
  gidebiliyorsunuz.
- **Ayarlardaki "Şimdi denetle" düğmesi, güncelleme bulunca "Güncelle"ye
  dönüşüyor.** Önceden yalnızca "yeni sürüm var" yazıyor ama kurmanın bir
  yolunu vermiyordu.

- **Modülün yol ekranı tepeden başlıyor.** Bölümlerin üstünde modülün adı
  ve açıklaması ikinci kez yazıyordu; ekranın başlığı zaten modülün adını
  taşıyor, açıklaması da bir önceki ekrandaki kartta duruyor.

### Düzeltildi
- **Bir kez kapatılan güncelleme duyurusu bir daha hiç çıkmıyordu.** Duyuru
  "şu sürüm için gösterildi" diye kaydediliyordu; eski bir sürüme dönen ya
  da uygulamayı yeniden kuran biri, kayıt kullanıcı verisinde durduğu için
  aynı güncellemeyi bir daha görmüyordu. Kayıt artık kurulu sürümü de
  içeriyor.
- **Profildeki yıl seçicisinin arkasındaki koyu leke.** Etkinlik
  takviminin yanındaki yıl düğmesi kartın içinde bir delik gibi
  duruyordu; arkasındaki alan kart rengi yerine sayfa zeminini
  gösteriyordu. Tek yıl varken düğmenin etrafındaki gereksiz çerçeve de
  kaldırıldı.

---

## [0.7.2] — 3 Eylül 2026

### Düzeltildi
- **Alıştırma editöründe boş satırda Enter çalışmıyordu.** Kodun arasına
  fazladan boş satır bırakmak mümkün değildi; satır aralığı ayarı, metin
  değişiminin tam ortasında uygulandığı için tuşu yutuyordu.
- **Konu anlatımı, dil değiştirildiğinde eski dilde kalıyordu.** Ayarlardan
  dili değiştirdiğinizde etiketler çevriliyor ama ders metni aynı kalıyor,
  bölümden çıkıp girmeniz gerekiyordu. Artık ders anında çevriliyor.

---

## [0.7.1] — 2 Eylül 2026

### Eklendi
- **Güncelleme artık uygulamanın içinden yapılıyor.** Yeni sürüm
  bildiriminde "Güncelle" düğmesi var: dosya indiriliyor (ilerleme
  görünüyor), denetleniyor, uygulama kapanıyor, dosyalar değiştiriliyor ve
  yeni sürüm kendiliğinden açılıyor. Elle indirip klasör değiştirmeye
  gerek kalmıyor.
- **İndirme iptal edilebiliyor** ve yarıda kalan dosya siliniyor.
- **Bir şey ters giderse eski sürüm geri geliyor.** Değişim sırasında
  eski kurulum yedekte tutuluyor; kopyalama tamamlanamazsa geri alınıyor,
  yani en kötü ihtimalle eski sürümünüzle kalıyorsunuz.
- Güncelleme yapılamayacak bir durumda (klasöre yazılamıyor, disk yeri
  yetmiyor) düğme yerine sebebi yazıyor ve sürüm sayfasına yönlendiriyor.

### Düzeltildi
- **Yeni sürüm denetimi hiçbir zaman sonuç vermiyordu.** Sürümler ön sürüm
  (pre-release) olarak yayınlandığı için denetimin baktığı adres "yayın
  yok" diyordu; artık sürüm listesine bakılıyor ve en yenisi bulunuyor.

---

## [0.7.0] — 2 Eylül 2026

### Eklendi
- **Yeni sürüm denetimi.** Uygulama her açılışta yeni bir sürüm yayınlanıp
  yayınlanmadığına bakıyor; açık kalan bir oturumda üç saatte bir yeniden
  bakıyor. Yeni sürüm varsa pencerenin altındaki şeritte sürüm sayfasının
  bağlantısı duruyor.
- **Yeni sürüm çıktığında bir bilgilendirme penceresi açılıyor.** Sürüm
  başına bir kez ve yalnızca açılışta: ders okurken ya da sınav çözerken
  önünüze kutu çıkmıyor. Pencerede yeni sürümün numarası, sürüm sayfasını
  açan bir düğme ve güncellemenin nasıl yapıldığı yazıyor.
- **Uygulama kendini güncellemiyor**, indirmeyi siz yapıyorsunuz: dosyayı
  indirip eskisinin yerine açmanız yeterli. İlerlemeniz, profiliniz ve
  rozetleriniz ayrı bir yerde durduğu için korunuyor.
- **Denetim ayarlardan kapatılabiliyor.** Ayarlar penceresine "Güncelleme"
  bölümü eklendi: anahtarla kapatılıyor ve "Şimdi denetle" düğmesiyle o an
  bakılabiliyor. Kapalıyken uygulama ağa hiç çıkmıyor.
- Sorguda hiçbir bilgi gönderilmiyor: kimlik, ilerleme ve kullanım verisi
  yok. Denetim başarısız olduğunda ekranda bir şey görünmüyor — internetin
  olmaması bu uygulamada olağan bir durum.

---

## [0.6.0] — 2 Eylül 2026

### Eklendi
- **Veri Bilimi patikası açıldı.** İlk bölümü "Veri Bilimi Nedir?": bir veri
  işinin baştan sona nasıl yürüdüğü, verinin neden hep tablo olduğu ve
  NumPy ile pandas'ın hangi soruna cevap verdiği. Yirmi sınav sorusu ve beş
  alıştırma var.
- **Bu bölümün alıştırmalarında kütüphane yok.** Ortalama alıyorsun, satır
  filtreliyorsun, sütun çıkarıyorsun, şehre göre grupluyorsun ve ham
  metinden bir özet rapor üretiyorsun — hepsi düz Python'la. Amaç, sonraki
  bölümde `groupby` yazdığında onun neyin yerine geçtiğini biliyor olman.
- **İki ders notu:** *Veri Sözlüğü* (kayıt, değişken, ortalama-medyan farkı,
  eksik değer, dosya biçimleri) ve *Tablo Tarifleri* (aynı altı işlemin düz
  Python karşılığı, yanında pandas'taki hâliyle).
- **NumPy bölümü.** Dizilerle döngü yazmadan hesap: vektörel işlemler,
  `shape` ve `dtype`, yeniden şekillendirme, dilim ve fancy index, koşulla
  seçme, `axis` ile satır/sütun ayrımı, yayılma ve eksik değerler
  (`np.nan`). Yirmi sınav sorusu ve beş alıştırma.
- **NumPy tuzakları ayrı bir ders notunda.** Dilimin özgün diziyi
  değiştirmesi, tamsayı diziye ondalık yazınca sessizce kırpılması,
  `and` yerine `&`, tek bir `nan`'ın bütün ortalamayı bozması,
  `axis`'in ters anlaşılması ve yedi tanesi daha. Bu hataların çoğu
  **hata vermiyor** — program çalışıyor ve yanlış sayıyı veriyor.
- **Pandas Serileri bölümü.** Değerlerin yanında **etiket** taşıyan yapı:
  seri kurmak, etikete göre seçmek, koşulla filtrelemek, eksik değerleri
  görüp doldurmak, `value_counts` ile saymak ve `describe` ile tek bakışta
  özet almak. Yirmi sınav sorusu ve beş alıştırma.
- **Hizalama anlatıldı.** İki seri toplanırken pandas sıraya değil etikete
  bakıyor; iki farklı kaynaktan gelen veri karışık sırada olsa bile doğru
  eşleşiyor. NumPy'ın sessizce yanlış sonuç verdiği yer tam burası.
- **DataFrame Temelleri bölümü.** Asıl tablo yapısı: sözlükten tablo
  kurmak, `shape` / `columns` / `dtypes` / `head` ile ilk bakış, sütun
  seçmek ve eklemek, sıralamak, bir sütunu index yapmak ve `describe` ile
  özet almak. Otuz sınav sorusu ve beş alıştırma.
- **Seçim ve Filtreleme bölümü.** Tablodan ilgilendiğin kısmı almak:
  `loc` etiketle, `iloc` sırayla, koşullardan üretilen maskeler, `&` ve `|`
  ile birden çok koşul, `isin` ve `str.contains`, sıralama ve `nlargest`.
  Otuz sınav sorusu ve beş alıştırma.
- **Gruplama bölümü.** Böl, hesapla, birleştir: `groupby`, `agg` ile birden
  çok özet, `transform` ile her satıra kendi grup ortalaması, iki sütuna
  göre kırılım ve `pivot_table` ile `crosstab`. Otuz sınav sorusu ve beş
  alıştırma.
- **Veri Temizleme bölümü.** Gerçek verinin hâli: sütun adlarındaki
  boşluklar, tutarsız yazılmış metinler, metin gelen sayı sütunları,
  tekrar eden kayıtlar ve eksik değerler. Temizliğin bir sırası var ve
  bölüm o sırayı öğretiyor. Otuz sınav sorusu ve beş alıştırma.
- **Görselleştirme bölümü.** Çubuk, çizgi, histogram ve dağılım grafiği;
  hangi soruya hangi grafiğin cevap verdiği, başlık ve eksen etiketinin
  neden zorunlu olduğu, grafiği dosyaya kaydetmek ve bir tuvale iki grafik
  koymak. Otuz sınav sorusu ve beş alıştırma.
- **Keşifçi Veri Analizi bölümü.** Eline yeni bir veri geldiğinde ne
  yapacağın: bakılacak sıra, `describe` çıktısını okumak, grup ortalamasını
  büyüklüğüyle birlikte değerlendirmek, korelasyon, IQR kuralıyla aykırı
  değer bulmak ve bulguyu dürüst bir cümleye çevirmek. Otuz sınav sorusu ve
  beş alıştırma.
- **Genel Tekrar bölümü.** Ham bir tabloyu baştan sona temizleyip
  analiz eden tek bir örnek, bölüm bölüm anahtar fikirler ve en sık düşülen
  tuzakların tek listesi. Elli sınav sorusu ve beş alıştırma; ayrıca
  modülün tamamını kapsayan bir hızlı başvuru notu.
- **Her bölümde iki ders notu var:** biri o konunun başvuru tablosu, öteki
  o konuda düşülen tuzaklar. Tuzak notlarının çoğu **hata vermeyen**
  hatalar üzerine: program çalışıyor, sayı çıkıyor ve sonuç yanlış oluyor.
- **Veri Bilimi sınavları otuz soru.** Giriş bölümü dışındaki her bölümde
  otuz soru var, Genel Tekrar'da elli; bu konular Python temellerine göre
  daha çok tekrar istiyor.
- **Yedi yeni rozet:** Veri Bilimi patikasında bir bölüm tamamlamak, iki
  farklı modülde birer bölüm tamamlamak, NumPy, DataFrame, Veri Temizleme
  ve Görselleştirme bölümlerini bitirmek, ve patikanın tamamını
  tamamlamak.

### Değişti
- **NumPy, pandas ve matplotlib artık uygulamanın içinde geliyor.** Veri
  Bilimi alıştırmaları bu kütüphaneleri kullanıyor; ayrıca bir şey kurman
  gerekmiyor, internet bağlantısı da gerekmiyor. Paket bu yüzden büyüdü.

### Düzeltildi
- **Alıştırmanın başlangıç kodundaki yorum satırları dil değişince
  çevrilmiyordu.** Dili değiştirdiğinde yönerge çevriliyor ama editördeki
  kod eski dilde kalıyordu; bir kez çalıştırdıysan bir daha hiç
  değişmiyordu. Artık koda dokunmadıysan yorumlar seçtiğin dile geçiyor.
  Yazdığın kod olduğu gibi duruyor.

---

## [0.5.0] — 2 Eylül 2026

### Eklendi
- **Rozetler geldi.** On iki rozet var: ilk programını çalıştırmak, bir
  sınavı hatasız bitirmek, üst üste yedi gün çalışmak gibi. Kazanılmayanlar
  da profilde duruyor ve üstlerine gelince nasıl kazanıldıkları yazıyor —
  neyin mümkün olduğunu görmek için.
- **Etkinlik takvimi geldi.** Bir yılın bütün günleri kare kare duruyor; bir
  günün karesi o gün ne kadar çalıştığına göre koyulaşıyor. Bir günün
  üstüne gelince o gün ne yaptığın yazıyor. Sağdaki listeden yıl
  seçilebiliyor; yeni bir yıla girildiğinde o yıl kendiliğinden ekleniyor.
  Takvim geriye dönük olarak da dolu: daha önce okuduğun dersler ve
  çözdüğün alıştırmalar kendi tarihlerine yerleşti.

### Değişti
- **Ayarlarda tema seçimi artık iki düğme.** Ay koyu temayı, güneş açık
  temayı seçiyor; hangisinin açık olduğu tek bakışta belli oluyor.
  Önceden aç/kapa anahtarıydı ve "kapalı"nın koyu tema demek olduğu ancak
  açıklamayı okuyunca anlaşılıyordu.
- **Ayarlar ve profil düzenleme pencereleri ekranın ortasında sabit
  duruyor.** Taşınamıyor, boyutları değiştirilemiyor.
- **Profil sayfası yeniden düzenlendi.** Solda fotoğraf, ad ve genel
  ilerleme; sağda rozet duvarı; altta etkinlik takvimi. Rozetler bir
  sayfaya sığmadığında oklarla ileri geri geçiliyor. Eskiden sayfanın
  yarısı boştu ve uzun yazılar kırpılıyordu.
- **Öğrenme yolundaki sayılar kesir gösteriyor.** "13" yerine "13/65",
  "3" yerine "3/15" — kaç tanesinden kaçının bittiği görünüyor. Profilde
  aynı dört sayı ikinci kez yazıyordu, oradan kaldırıldı.
- **Profil düzenleme ayrı bir pencerede açılıyor.** "Düzenle" dendiğinde
  arka plan kararıyor ve ad, soyad, fotoğraf tek bir pencerede
  dolduruluyor. Alanlar dar bir sütuna sıkıştığı için yazılar
  okunmuyordu.

### Düzeltildi
- **Sınav süresi ayarı artık o an uygulanıyor.** Sınav açıkken ayarlardan
  süreyi kaldırdığında sayaç anında duruyor, geri açtığında sayaç yeniden
  başlıyor. Eskiden sınavdan çıkıp yeniden girmek gerekiyordu.
- **Tema değiştirirken ekranın bir an bozulması giderildi.** Açıktan koyuya
  geçerken arada stilsiz bir kare görünebiliyordu.
- **İpuçları daha çabuk çıkıyor.** Bir şeyin üstüne geldiğinde açıklamanın
  görünmesi için beklenen süre kısaldı.

---

## [0.4.0] — 1 Eylül 2026

### Eklendi
- **Sınavlar büyütüldü: 150 → 250 soru.** Modüller bölümünden itibaren her
  bölümde **20 soru** var. Genel Tekrar sınavı **50 soruya** çıktı ve on
  dört bölümün tamamını kapsıyor — `print` ayrıntılarından veritabanı
  işlemlerine kadar. Süreler de soru sayısına göre yeniden ayarlandı.
- **Liste üreteçleri, `lambda` ve `sorted(key=...)` eklendi.** Bunlar gerçek
  Python kodunun her yerinde olduğu hâlde müfredatta hiç geçmiyordu:
  `[x * 2 for x in items]` yazımı, süzme, sözlük üreteci; bir listeyi neye
  göre sıralayacağını söylemek; kaç argüman geleceği belli olmayan
  fonksiyonlar (`*args` / `**kwargs`). Listeler ve Fonksiyonlar bölümlerine
  birer ders notu ve ikişer alıştırma olarak girdi.
- **Kütüphane kurmak** anlatıldı: `pip install`, sanal ortam neden gerekiyor,
  `requirements.txt` ve `ModuleNotFoundError` neden çıkıyor. Veri Bilimi
  patikasına geçildiğinde ilk gereken şey buydu ve yalnızca iki cümlede
  geçiyordu.
- **Başlangıç ve Değişkenler bölümlerine zor alıştırma eklendi.** İki bölümde
  de en zor alıştırma orta seviyede kalıyordu.
- **Demetlerle çalışma alıştırması** eklendi. Bölümün adı "Listeler ve
  Demetler" olmasına rağmen hiçbir alıştırma demet istemiyordu.
- **Python Temelleri tamamlandı.** Dört bölüm daha yazıldı ve modül bitti:
  **Dosya İşlemleri** (`with`, kipler, `encoding`, satır sonları, veri
  dosyası okuma), **Nesne Tabanlı Programlama** (`class`, `__init__`,
  `self`, `__str__`, kalıtım), **Veritabanı İşlemleri** (`sqlite3`, tablo
  kurma, `?` yer tutucusu, `SELECT`/`WHERE`/`GROUP BY`, `commit`) ve
  **Genel Tekrar** (öğrenilenlerin birbirine nasıl bağlandığı, hızlı
  başvuru sayfası, buradan sonrası). On beş bölümün tamamı artık açık.
- **Modüller bölümünden itibaren alıştırma sayısı beşe çıktı.** Her bölümde
  bir kolay, iki orta, iki zor alıştırma var. Zor olanlar tek bir konuyu
  değil, birden fazla bölümü aynı anda kullanıyor.
- **Koşul Durumları bölümüne iki ders notu eklendi** — karşılaştırma
  sözlüğü ve koşul tuzakları. O bölümün hiç ders notu yoktu.
- **Başlangıç bölümüne ikinci ders notu eklendi:** veri biliminde Python
  ekosistemi, hangi kütüphanenin ne işe yaradığı ve nerede öğrenileceği.
- **Tip Belirtimleri bölümü.** Bir fonksiyonun ne beklediğini ve ne
  döndürdüğünü yazma biçimi: `text: str`, `-> int`, `list[str]`,
  `dict[str, int]`, değer olmayabildiğinde `int | None`, değer döndürmeyen
  fonksiyonlar için `-> None` ve eski kodda karşına çıkan `Optional[str]`
  yazımı. Belirtimlerin çalışma anında **kontrol edilmediği**, yani bir
  kural değil bir not oldukları ayrıca anlatılıyor. İki ders notu (tip
  sözlüğü, uzun belirtimleri çözme rehberi), on soruluk sınav ve üç
  alıştırma.
- **Konu anlatımlarında şemalar.** Anlatılan şeyin çizimle daha çabuk
  oturduğu yerlerde artık şema var: bir fonksiyon imzasının hangi parçası
  ne demek, `dict[str, int]` içindeki iki tipin hangisinin anahtar hangisinin
  değer olduğu, belirtimin çalışma anında ne olduğu. Şemalar sayfanın
  kendisiyle çiziliyor; temayla birlikte renk değiştiriyor ve metinle
  birlikte büyüyüp küçülüyor.
- **Hata Yakalama bölümü.** İki tür hata, traceback okumak, `try` / `except`,
  hangi hatayı yakalayacağın, çıplak `except` neden kötü, `as error`, `else`
  ve `finally`, `raise` ile hatayı kendin çıkarmak. İki ders notu (hata
  türleri sözlüğü, traceback okuma rehberi), on soruluk sınav ve üç alıştırma.
- **Sınavlar yeniden yazıldı.** Her bölümde artık **10 soru** var (önce 4'tü,
  bir bölümde 3). Modülün tamamında artık 150 soru var. Konu ilerledikçe sorular
  zorlaşıyor, kod okumaya dayanan soruların payı artıyor ve her bölümün
  sonunda bir tane düşündüren soru duruyor.
- **Modüller bölümü.** `import`, `from ... import ...`, `as` ile takma ad,
  kendi dosyanı modül olarak kullanmak ve `if __name__ == "__main__"`.
  İki ders notu (standart kütüphane turu, import biçimleri ve sık yapılan
  hatalar), on soruluk sınav ve üç alıştırma. Son alıştırmada yanına
  konan gerçek bir modül dosyasını import ediyorsun.
- **API ve Docker öğrenme patikaları** eklendi. İçerikleri henüz
  hazırlanmadı, ikisi de kilitli görünüyor.
- **Ayarlara kilidi kaldırma seçeneği geldi.** Açtığında bölümler sırayla
  açılmıyor; istediğin bölüme istediğin an girebiliyorsun.
- **Ayarlara sınav süresini kaldırma seçeneği geldi.** Açtığında sınavlarda
  süre sınırı olmuyor.
- **Sınav başlangıç ekranı.** Sekmeye dokununca sorular hemen açılmıyor;
  önce kaç soru olduğu, ne kadar süre tanındığı ve **önceki denemenin notu**
  görünüyor. Hazır olduğunda başlatıyorsun.
- **Sınavlarda süre.** Konu zorlaştıkça soru başına tanınan süre artıyor.
  Süre dolunca sınav kendiliğinden gönderiliyor. Sayaç sağ üst köşede,
  kaydırmayla kaymıyor ve metnin üstünü örtmüyor.
- **Her denemede sorular ve şıklar karışıyor.** Aynı sırada üst üste
  ikiden fazla doğru cevap gelmiyor.
- **Hakkında ekranı.** Bilgi, Sık Sorulanlar, Bağlantılarım, Ekstra İçerikler
  ve Lisans tek ekranda toplandı; aralarında üstteki sekmelerle geçiliyor.
- **Sık Sorulanlar sayfası.** Uygulama hakkında en sık sorulan sorular;
  başlığa tıklayınca cevabı açılıyor.
- **Bilgi sayfası.** Uygulamanın ne olduğunu, nasıl çalıştığını ve hangi
  ilkelere göre kurulduğunu anlatıyor.
- **Profil fotoğrafı.** Profil ekranından kendi fotoğrafını seçebiliyorsun;
  şeritteki profil düğmesinde de görünüyor. Görsel bilgisayarındaki veri
  klasörüne kopyalanıyor, hiçbir yere gönderilmiyor.
- **Bölümler sırayla açılıyor.** Bir bölüm, önündeki bölüm tamamlanmadan
  açılmıyor; kilitli halkanın altında hangi bölümü bitirmen gerektiği
  yazıyor. Tamamladığın bölümlere istediğin zaman geri dönebiliyorsun.
- Ekstra İçerikler'e `CS_Complete_Terminology_Guide` projesi eklendi.
- Alıştırmada istenen değişken adını kullanmadıysan ama doğru değeri başka
  bir adla tuttuysan, uygulama artık bunu söylüyor: "`second` adında bir
  değişkenin var ve değeri doğru, ama alıştırma bunu `seconds` adıyla
  istiyor." Önceden yalnızca "böyle bir değişken tanımlamamışsın" diyordu.

### Değişti
- **Ayarlarda dil seçimi TR / EN düğmeleriyle yapılıyor.** Aç/kapa anahtarı
  iki seçenek arasında seçim için uygun değildi; hangi tarafın hangi dil
  olduğu ancak açıklama okununca anlaşılıyordu.
- **Ayarlar ekranı yeniden düzenlendi.** Dil ve tema açılır kutulardaydı;
  ayar sayısı artınca bu düzen dağılıyordu. Artık her ayar tek bakışta
  okunuyor: solda adı ve ne işe yaradığı, sağda açık mı kapalı mı olduğunu
  konumuyla gösteren bir anahtar. Ayarlar Görünüm ve Öğrenme diye ikiye
  ayrıldı.
- **Program artık koyu temayla açılıyor.**
- **Sol şerit yediden beş simgeye indi.** Bağlantılarım, Ekstra İçerikler ve
  Lisans artık Hakkında ekranının sekmeleri.
- **Şeridin tepesinde genel ilerleme halkası var.** Yüzde ortasında yazıyor;
  ders okurken de, alıştırma çözerken de ne kadarını bitirdiğin ekranda
  kalıyor. Tıklayınca öğrenme yoluna dönüyor.
- **Ekran başlıkları ortalandı** ve altlarına ince bir vurgu çizgisi geldi;
  geri düğmesi en sola alındı.
- **Modül yolu sayfanın ortasına hizalandı.** Sola yaslanmış duruyordu.
- **Şerit simgeleri iki tonlu çizildi.** Yalnız çizgiden oluşan hâlleri
  cansız duruyordu; gövdeleri kendi renginde hafifçe dolduruldu.
- **Açık tema yumuşatıldı.** Sayfa fazla parlaktı ve uzun metin okurken
  gözü yoruyordu; kartlar saf beyazdı. Soluk yazılar da (süre,
  "Başlanmadı", sayfa içi başlık listesi) koyu temadakinden belirgin
  şekilde daha zor okunuyordu. İkisi de koyu temanın seviyesine çekildi.

### Düzeltildi
- **Alıştırmayı geçince alt alta birden fazla "Geçti" satırı çıkıyordu.**
  Bir alıştırmada altıya kadar kontrol olduğu için panel bunlarla doluyor,
  çıktı aşağı itiliyordu. Artık geçince tek satır yazıyor; bir şey
  tutmadığında da yalnızca tutmayan satırlar görünüyor. Boşalan yer
  çıktıya verildi, kutu iki katına yakın büyüdü.
- **Kod hata verdiğinde panel yanıltıcı şeyler söylüyordu.** İki nokta
  unutulmuş bir sınıf için "Book adında bir sınıf tanımlamamışsın"
  yazıyordu — oysa sınıf yazılmıştı, sorun söz dizimindeydi. Kod hiç
  çalışmadığında artık yalnızca hatanın kendisi ve satır numarası
  gösteriliyor.
- **Sayfalara ilk girişte ekran bir an siyah kalıyordu.** Ders anlatımı,
  ders notu, Hakkında ve Sürüm Notları ekranları tarayıcı motoruyla
  çiziliyor; her biri ilk kez açıldığında ilk kare gelene kadar siyah
  görünüyordu. Bu ilk çizim artık açılışta, pencere daha görünmeden
  yapılıyor.
- **Konu anlatımında sayfa kayarken sıçrıyordu.** Metnin sonuna inince
  "okundu" işareti konuyor, o da sağdaki ilerleme kutusunu güncelliyordu;
  kutu güncellenirken sayfanın tamamı yeniden yükleniyor ve okuduğun yer
  kayıyordu. Kutu artık sayfa yeniden yüklenmeden yerinde değişiyor.
- **Konu anlatımında sağdaki başlık listesi.** Sayfanın sonuna inince
  işaret yukarı fırlıyordu ve son başlığa ("Özet") hiç gelmiyordu.
- **Sınav sorularındaki kod düz metin olarak görünüyordu.** Renk yoktu ve
  daha kötüsü **girinti kayboluyordu** — Python'da girinti kodun kendisi.
  Artık ders anlatımındaki kod blokları gibi görünüyor.
- `>=` ekranda tek bir `≥` işareti olarak çiziliyordu; yazı tipinin
  ligatürleri yüzünden. Artık yazıldığı gibi görünüyor.
- Sınav metinlerinde `**kalın**` yazım ham görünüyordu.
- Yeni bir konu anlatımına geçince sayfa baştan değil, bir önceki konuda
  kalınan yerden açılabiliyordu.
- **Sayfalara ve ayarlara ilk girişte beyaz parlama** oluyordu.
- Uygulama, açılış ekranı hâlâ ekrandayken arkasında beliriyordu; ikisi
  bir süre aynı anda duruyordu. Artık açılış ekranı kaybolurken geliyor.
- Sürüm notlarında uzun maddeler yarıda kesiliyordu; artık tamamı görünüyor.
- Sürüm notlarındaki başlıklar Türkçede "EKLENDI" yazıyordu, artık "EKLENDİ".

## [0.3.0] — 28 Ağustos 2026

### Eklendi
- Ana ekran artık öğrenme patikalarıyla açılıyor: Python, Veri Bilimi, Makine Öğrenmesi ve SQL, 2x2 dizilmiş dört kart. İçeriği hazır olmayan üçü kilit simgesiyle ve soluk görünüyor; Veri Bilimi ile Makine Öğrenmesi kartlarında önce Python patikasının bitirilmesi öneriliyor. İlerleme çubuğu patika kartının üzerinde duruyor.
- Patikada tek modül varsa modül listesi atlanıyor ve doğrudan konulara gidiliyor; tek kartlık bir ekrana ikinci kez tıklatmanın faydası yoktu. Geri dönüş de aynı yolu izliyor.
- Açılış ekranı: uygulama simgesi ve adı, ana pencere kurulurken görünüyor. Önceden Chromium yüklenene kadar ekranda hiçbir belirti yoktu.
- Öğrenme yolunda henüz yazılmamış bölümler de görünüyor: soluk, tıklanmayan halkalar ve "Yakında" yazısı. Python Temelleri'nin geri kalanı (modüller, hata yakalama, dosya işlemleri, OOP, SQLite, genel tekrar) böyle listelendi.

### Değişti
- Ders notu ekranı yeniden tasarlandı. Soldaki 270 piksellik liste paneli kaldırıldı; bir bölümde en çok üç not olduğu için o panel hem ağır duruyor hem de metni sağa itiyordu. Notlar artık metnin üstünde ince bir sekme sırası ve tek not varsa sıra hiç çizilmiyor.
- Ekran başlıkları yeniden tasarlandı. Şerit sayfa içeriğiyle aynı sütuna hizalandı: başlık pencerenin en solunda, içerik ise ortada duruyordu ve ikisi birbirine bağlı görünmüyordu. Şeridin ayrı zemin rengi kaldırıldı; sayfanın üstünde kopuk bir blok gibi duruyordu, artık aynı zeminde ve yalnızca ince bir çizgiyle ayrılıyor. Başlık büyüdü (17px → 26px), üstüne ekranın bağlamını söyleyen küçük bir satır ve solundaki renkli çubuk geldi; renk sol şeritteki simgeyle aynı. Yazılar şeridin dikeyde tam ortasında.
- Windows başlık çubuğu artık uygulamanın rengini alıyor. Koyu temada pencere koyu, çubuk açık kalıyor ve ekran ikiye bölünmüş gibi duruyordu. Ayarlar ve açılış uyarısı pencereleri de aynı renge uyuyor.

### Düzeltildi
- Ders metninde aşağı inince sayfa aniden başa dönüyordu. Sona ulaşınca "okundu" işaretleniyor, bu da ilerleme kutusunu güncelliyor ve belge baştan yükleniyordu. Aynı şey alıştırma yönergesinde ipucu açılınca da oluyordu. Belge yeniden çizilirken okunan yer artık korunuyor.
- Alıştırmayı doğru çözünce numarasındaki onay işareti hemen belirmiyordu; ancak başka bir alıştırmaya geçince ya da bölüm yeniden açılınca görünüyordu.
- Konu ekranındaki sekmelerin arkasındaki dolu kutu kaldırıldı; şerit sayfayla aynı zemine geçince üstte yamalı duruyordu. Seçili sekme artık altındaki çizgiyle belli oluyor ve sekmeler birbirine yapışmıyor.
- Bölüm başlığındaki süre birimi İngilizcede de "dk" yazıyordu; artık çevirilerden geliyor.
- Karşılama kartındaki sayaç etiketleri artık baş harfleri büyük yazılıyor: "Tamamlanan Bölüm", "Çözülen Alıştırma".
- Büyük harfle yazılan başlıklarda Türkçe `i` harfi yanlış dönüşüyordu: "ÖĞRENME PATIKALARI" çıkıyordu, doğrusu "ÖĞRENME PATİKALARI". Python'un `upper()` metodu `i` harfini `I` yapıyor; artık dile göre dönüştürülüyor.

## [0.2.0] — 27 Ağustos 2026

### Eklendi
- Her bölümde artık **en az üç alıştırma** var; toplam 6'dan 18'e çıktı. Yeni alıştırmalar kolaydan zora sıralı ve yalnızca o bölüme kadar anlatılmış kavramları kullanıyor.
- Uygulama ilk açılışta bilgisayarın arayüz diline göre açılıyor: Windows'u Türkçe olan Türkçe, başka bir dilde olan İngilizce görüyor. Ayarlardan bir dil seçildiği anda bu devreye girmiyor, seçim geçerli oluyor.
- Açılışta kapalı beta uyarısı: uygulamanın kararsız çalışabileceği, hata ve çökme görülebileceği ve geri bildirimin nasıl iletileceği yazıyor. Sürüm başına bir kez çıkıyor.
- Lisans ekranı artık seçili dilde: Türkçede MIT Lisansı'nın Türkçe çevirisi, İngilizcede özgün metin görünüyor. İki dilde de ekranda tek bir lisans metni var.
- **Başlangıç** bölümü: Python nedir, ilk program, uygulamanın nasıl çalıştığı ve kurulum notu.
- **Koşul Durumları** bölümü: if / elif / else, koşul sırası, doğruluk değerleri.
- **Döngüler** bölümü: for, while, range, break ve continue notlarıyla.
- **Sözlükler ve Kümeler** bölümü: anahtar-değer mantığı, `in` ile anahtar sorgulama, ekleme ve güncelleme, `items()` ile döngü, kümelerin tekrar tutmaması ve `{}` tuzağı. Ders notlarında sözlük metotları ile dört veri yapısını karşılaştıran bir seçim rehberi var.
- **Listeler ve Demetler** bölümü: liste oluşturma, sıra numarası, negatif numara, dilimleme, `append`/`remove`/`pop`, `len` ve `in`, demetlerin değiştirilemezliği. Ders notlarında liste metotları ve dilimleme ayrıntısı var; kopya tuzağı da anlatılıyor.
- **Fonksiyonlar** bölümü: `def`, parametreler, `return`, varsayılan değerler. Ders notlarında konumsal/isimli argümanlar ve değişken kapsamı (yerel, global) var. `return` ile `print` farkı hem derste hem sınavda ayrıca ele alınıyor.
- Operatörler bölümüne iki ders notu: aritmetik operatörler, atama ve karşılaştırma.

### Değişti
- Sınav sorularındaki, şıklardaki ve açıklamalardaki kod parçaları artık kod olarak çiziliyor: tek aralıklı yazı ve zemin. Düz metin hâlinde `[20, 30]` ile bir cümleyi ayırt etmek zordu.
- Alıştırma şeridi belirginleşti: sayı kalın yazılıyor ve yanında numara düğmeleri duruyor. Bölümde kaç alıştırma olduğu ve hangilerinin çözüldüğü bakar bakmaz görünüyor; istediğine doğrudan atlanabiliyor. Önceki/Sonraki düğmeleri kaldırıldı.
- Sürüm notlarındaki sayfa numaraları ortalandı; "Sayfa 1 / 2" yazısı kaldırıldı, numaralar zaten aynı bilgiyi veriyordu.
- Sol şerit ikiye ayrıldı: üstte her gün girilen ekranlar (Öğrenme Yolu, Profilim, Ekstra İçerikler), altta ayar simgesinin hemen üstünde ara sıra açılanlar (Sürüm Notları, Bağlantılarım, Lisans).
- Sürüm numaralarının yanında kırmızı **ALPHA** rozeti çıkıyor. 1.0 öncesi her sürüm alpha sayılıyor; 1.0 çıktığında rozet kendiliğinden kalkacak.
- Sürüm notları sayfalara bölündü; bir sayfada en fazla üç sürüm görünüyor, altta sayfa düğmeleri var. Önceden bütün sürümler alt alta dizildiği için ekran uzayıp gidiyordu.
- Python Temelleri modülü yeniden düzenlendi. Sıra artık: Başlangıç, Değişkenler, Operatörler, Koşullar, Döngüler.
- Döngüler operatörlerden ayrılıp kendi bölümü oldu; ikisi tek bölüme sığmıyordu.
- Operatörler bölümünün ders notu PDF yerine metin olarak açılıyor.
- Sınavlardaki açıklamalar artık ders anlatımındaki ipucu kutusuyla aynı görünümde.
- Başlangıç sınavının son sorusu uygulamanın arayüzünü soruyordu; yerine dersin anlattığı bir konu kondu: Python'un yorumlanan bir dil olması ne demek.

### Düzeltildi
- Değişkenler bölümünün ikinci alıştırması fonksiyon yazmayı istiyordu, ama fonksiyonlar o noktada henüz anlatılmamıştı. Alıştırma o dersin gerçekten öğrettiği şeyle değiştirildi: metinden sayıya dönüşüm.
- Sürüm notlarındaki kalın yazı ve kod işaretleri ekranda ham görünüyordu; artık biçimlendirilmiş olarak çiziliyor.
- Paketlenmiş uygulamada Windows görev çubuğunda ve pencere başlığında uygulamanın simgesi yerine genel bir program simgesi çıkıyordu. Simge dosyası paketin içinde duruyordu ama uygulama onu yanlış klasörde arıyordu.
- Ders metnini sonuna kadar okumak "okundu" olarak işaretlenmiyordu. Sayfanın kendisi haber vermeye çalışıyordu ama tarayıcı motoru, kullanıcı tıklaması olmadan uygulamaya haber gönderilmesine izin vermiyor; bu yüzden bildirim sessizce düşüyordu. Artık uygulama sayfaya kendisi soruyor.
- Ders metninin altındaki ileri düğmesi, bölümde ders notu olsa bile doğrudan sınava atlıyordu. Artık sırayla gidiyor: konu anlatımı, ders notu, sınav, alıştırma.
- Ders notlarının sonuncusunda ileri düğmesi yoktu, okuyan kişi sınava geçmek için sekmelere dönmek zorundaydı. Son notun altında artık sınava götüren bir düğme var.
- Yeniden düzenleme sırasında iki alıştırma, içeriği tamamen değişmesine rağmen eski kimliğini korumuştu. Bu yüzden açtığınızda önceki alıştırmada yazdığınız kod karşınıza geliyordu. Kimlikler ayrıştırıldı, alıştırmalar artık boş başlıyor.

## [0.1.2] — 27 Ağustos 2026

### Eklendi
- Bağlantılar ve Projeler bölümü: GitHub, LinkedIn, portfolyo, Medium ve açık kaynak projeler.
- Lisans ekranı: MIT metni ve ders içeriğinin lisansı.
- Alıştırmalarda kademeli ipucu; kullanıcı ihtiyacı kadarını açıyor.
- Hata mesajlarının altında ne anlama geldikleri yazıyor.
- Windows için hazır paket: Python kurmadan çalışan `Odyssey.exe`.
- Uygulamanın kendi adı ve simgesi.

### Değişti
- Alıştırma kodu artık tamamen ASCII. İngilizce klavyede Türkçe karakter olmadığı için önceki alıştırmalar İngilizce kullananlar tarafından çözülemiyordu.
- İlerleme göstergesi gerçek durumu yansıtıyor; bölümü açmak artık "okundu" saymıyor.
- Sol şeritteki simgeler koyu temada daha okunaklı.

### Düzeltildi
- Son ders notundayken "Sonraki not" tıklanamaz hâlde görünüyordu, artık hiç çıkmıyor.
- Sürüm notlarında her başlık ayrı bir kart olarak çiziliyordu.

## [0.1.1] — 26 Ağustos 2026

### Eklendi
- Öğrenme yolu ekranı: modül kartları ve bölüm düğümleri.
- Profil ekranı: ad, soyad ve ilerleme istatistikleri.
- Ders notları PDF yerine metin olarak açılıyor; aranabiliyor ve kopyalanabiliyor.

### Değişti
- Ders metinleri Chromium ile çiziliyor: kod blokları renkli, köşeler yuvarlak, sayfa içi başlık listesi kaydırırken yerinde kalıyor.
- Bölümler kilitli değil; tamamlananlara istenildiğinde dönülebiliyor.

### Düzeltildi
- Ayarlar penceresi açılmıyordu.
- Ders notlarına geçince ikinci bir pencere açılıyordu.

## [0.1.0] — 26 Ağustos 2026

### Eklendi
- İlk çalışan sürüm: Python Temelleri modülü, konu anlatımı, sınav ve kod alıştırmaları.
- Kod çalıştırma motoru: beş kontrol tipi, zaman aşımı, anlaşılır hata mesajları.
- Türkçe ve İngilizce arayüz; yeniden başlatmadan değişiyor.
- İlerleme kalıcı olarak saklanıyor.
