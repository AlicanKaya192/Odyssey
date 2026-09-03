Veri Bilimi modülü bitti. Bu not, "şimdi ne yapayım" sorusunun cevabı.

## Önce dürüst bir değerlendirme

Bölümleri bitirmek, öğrenmiş olmak demek değil. Şunları **bakmadan**
yapabiliyor musun?

- Bir CSV'yi okuyup boyutuna, tiplerine ve eksik değerlerine bakmak
- İki koşulu birleştirip tabloyu filtrelemek
- Bir sütuna göre gruplayıp sayı ve ortalamayı birlikte almak
- Sütun adlarını ve metin sütunlarını temizlemek
- Etiketli bir çubuk grafik çizip dosyaya kaydetmek
- `describe()` çıktısına bakıp dağılım hakkında bir şey söylemek

Bir tanesinde takılıyorsan o bölüme geri dön. Temel eksik kalırsa üstüne
konan her şey sallanıyor.

## Asıl öğrenilen şey araç değildi

`groupby` yazmayı bir haftada unutabilirsin; başvuru notuna bakıp
hatırlarsın. Unutulmaması gereken şey şu alışkanlıklar:

- Ortalama almadan önce **kaç kayıttan** hesaplandığına bakmak.
- Bir fark bulduğunda **başka neyin farklı olduğunu** sormak.
- "Birlikte hareket ediyor" ile "sebep oluyor" arasındaki farkı korumak.
- Temizlik sırasında **ne attığını** yazmak.
- Bir soruya bu veriyle cevap verilemiyorsa **bunu söyleyebilmek.**

Araçlar değişiyor, bunlar değişmiyor.

## Nasıl pratik yapılır?

**Kendi verinle çalış.** En iyi alıştırma gerçekten merak ettiğin bir soru.
Örnekler:

- Aylık harcamalarını bir CSV'ye yazıp kategoriye göre gruplamak
- Bir klasördeki dosyaların boyut ve tarihlerini tabloya çevirip en büyük
  dosyaları bulmak
- Bir dersin not listesini alıp dağılımını çıkarmak
- Bir yıl boyunca tuttuğun bir kaydı (kitap, egzersiz, uyku) analiz etmek

Kendi verinde bir tuhaflık gördüğünde **niye öyle olduğunu biliyorsun** —
öğrenme tam orada oluyor. Hazır bir veri setinde bu bağ yok.

**Küçük başla ve bitir.** Yarım kalan büyük analiz, biten küçük analizden
daha az öğretiyor.

**Sonucu birine anlat.** Bir bulguyu tek cümleye indiremiyorsan analiz
bitmemiş demektir.

## Bir analizi bitirdiğinde kontrol listesi

- [ ] Ham veriyi bozmadan sakladım mı?
- [ ] Attığım satırların sayısını ve sebebini yazdım mı?
- [ ] Her grup ortalamasının yanında grup büyüklüğü var mı?
- [ ] Grafiklerin başlığı, eksen etiketi ve birimi var mı?
- [ ] Çubuk grafikte eksen sıfırdan başlıyor mu?
- [ ] Nedensellik iddia eden bir cümle yazdım mı?
- [ ] Bulgunun sınırlarını yazdım mı?
- [ ] Kodu baştan çalıştırınca aynı sonucu veriyor mu?

Son madde önemli: elle yaptığın küçük düzeltmeler analizi **tekrarlanamaz**
hâle getiriyor. Her adım kodda olmalı.

## Sırada ne var?

<figure class="fig">
  <div class="flow">
    <span class="node ok"><b>Veri Bilimi</b><br>bitti</span>
    <span class="arrow">→</span>
    <span class="node acc"><b>İstatistik</b><br>ne kadar güvenilir</span>
    <span class="arrow">→</span>
    <span class="node"><b>Makine Öğrenmesi</b><br>tahmin</span>
  </div>
  <figcaption>Sıra kesin değil; istatistik ve makine öğrenmesi birbirine paralel de öğrenilebiliyor. Ama ikisi de bu modülün üstüne kuruluyor.</figcaption>
</figure>

**İstatistik** şu soruya cevap veriyor: gördüğün fark gerçek mi, yoksa
rastlantı mı? Bu modülde "iki kişilik grup bir sonuç değil" dedik ama kaç
kişi yeterli, onu söylemedik. Cevabı orada.

**Makine öğrenmesi** geçmiş veriye bakıp gelecek hakkında bir şey söylemek.
Bilmekte fayda var: bir makine öğrenmesi projesinin zamanının çoğu bu
modülde öğrendiğin işlerle geçiyor. Model kurmak birkaç satır; veriyi
anlamak, temizlemek ve doğru soruyu bulmak haftalar.

**SQL** de sırada bekleyen bir araç. Veri çoğu zaman bir dosyada değil, bir
veritabanında duruyor; `groupby` ile yaptığın işin aynısı orada başka bir
dille yazılıyor. Mantığı öğrendiğin için geçişi kolay olacak.

## Bu arada

Bu modülün alıştırmalarını bir kez daha çözmek, yeni bir konuya geçmekten
daha yararlı olabiliyor — özellikle çözümüne baktıkların. İkinci seferde
kodu yazmak değil, **neden öyle yazıldığı** kalıyor akılda.
