# Genel Tekrar

On iki bölüm önce "makine öğrenmesi nedir" diye başladık. Şimdi elinde
uçtan uca bir model kurma, dürüstçe ölçme ve kaydetme yeteneği var.

Bu bölüm yeni bir şey öğretmiyor. **Öğrendiklerini tek bir akışta
topluyor** ve en çok karıştırılan yerleri bir kez daha, ölçülmüş sayılarla
gösteriyor.

## Akış

Her problem aynı altı adımdan geçiyor:

<figure class="fig">
  <div class="flow">
    <span class="node"><b>1</b><br>oku,<br><code>X</code> ve <code>y</code></span>
    <span class="arrow">&rarr;</span>
    <span class="node"><b>2</b><br>ayır ve<br>testi kapat</span>
    <span class="arrow">&rarr;</span>
    <span class="node acc"><b>3</b><br>taban çizgiyi<br>ölç</span>
    <span class="arrow">&rarr;</span>
    <span class="node"><b>4</b><br>pipeline +<br>çapraz doğrulama</span>
    <span class="arrow">&rarr;</span>
    <span class="node"><b>5</b><br>testte<br>bir kez ölç</span>
    <span class="arrow">&rarr;</span>
    <span class="node"><b>6</b><br>kaydet ve<br>notunu yaz</span>
  </div>
  <figcaption>Üçüncü adımı atlayan her rapor eksik; beşinci adımı ikinci kez yapan her rapor yanlış.</figcaption>
</figure>

## Taban çizgi her şeyden önce

Modülün en çok tekrarlanan cümlesi. Ölçülen üç örnek:

| Problem | Taban çizgi | Model | Fark |
|---|---|---|---|
| Araba fiyatı (MAE) | 137.3 | **16.2** | 8 kat düşük hata |
| Abone kaybı | 0.573 | **0.793** | 22 puan |
| Dolandırıcılık | 0.944 | 0.955 | **1,1 puan** |

Üçüncü satır bu tablonun sebebi. **%95,5 doğruluk hiçbir şey ifade
etmiyor**, çünkü hiçbir şey yapmayan bir tahminci %94,4 alıyor. İlk iki
satırdaki modeller gerçekten iş görüyor; üçüncüsü ancak recall'e
bakılınca anlaşılıyor.

## Model seçimi bir ölçüm işi

"Hangi model en iyi?" sorusunun cevabı veriye bağlı ve **önceden
bilinmiyor.** Ölçülen iki örnek birbirinin tersi:

**Araba fiyatı (regresyon):**

| Model | Çapraz doğrulama MAE | Test MAE |
|---|---|---|
| **Doğrusal regresyon** | **16.6 ± 2.8** | **16.2** |
| Rastgele orman | 42.3 ± 15.1 | 44.2 |
| Karar ağacı | 69.3 ± 10.2 | 65.7 |

En basit model, en karmaşığını dört kat geçiyor. Sebebi bölüm 07'de
ölçülmüştü: ilişki gerçekten doğrusalsa ağaçlar onu basamaklarla taklit
etmeye çalışıyor ve kaybediyor. Topluluk kurmak da kurtarmıyor — sorun
ağaç sayısında değil, ağacın veriye uymamasında.

**Müşteri kaybı (sınıflandırma, bölüm 08):**

| Model | Tek ayrımda test | Çapraz doğrulama |
|---|---|---|
| Karar ağacı | **0.96** | 0.827 |
| Rastgele orman | 0.90 | 0.867 |
| Gradyan artırma | 0.88 | **0.873** |

Burada sıralama **ölçüye göre tersine dönüyor.** Tek bir test skoru ağacı
birinci gösteriyor; beş katın ortalaması sonuncu gösteriyor.

**İkisinden çıkan tek kural:** modeli seçen sen değilsin, ölçüm. Ve o
ölçüm **tek bir sayı olamaz.**

## Ölçüyü seçmek modeli seçmekten önce geliyor

Bölüm 09'un dersi bütün modüle uzanıyor. Aynı model, aynı veri, dört farklı
sayı:

```
dogruluk           0.955    <- taban 0.944, yani neredeyse hicbir sey
precision          0.750
recall             0.286    <- 21 dolandiriciligin 15'i kacti
ortalama precision 0.525    <- taban 0.056, yani tabanin dokuz kati
```

**Hangisini raporlayacağını seçmek, modeli seçmekten daha çok şeyi
değiştiriyor.**

Kaba bir rehber:

| Durum | Bakılacak |
|---|---|
| Regresyon | MAE ve R², yanında taban çizgi |
| Dengeli sınıflandırma | Doğruluk + karışıklık matrisi |
| Dengesiz sınıflandırma | Recall, F1, **ortalama precision** |
| Kaçırma pahalı | Recall öne |
| Yanlış alarm pahalı | Precision öne |
| Kümeleme | Silüet — **gürültü karşılığıyla birlikte** |

## Sızıntı: modülün en pahalı hatası

Üç ayrı bölümde üç farklı biçimde çıktı ve üçünde de **skoru yükseltti.**
Sızıntının işareti kötü bir sonuç değil, **fazla iyi** bir sonuç.

| Nerede | Ne oluyor | Ölçülen etki |
|---|---|---|
| Bölüm 04 | Ölçekleyici ayırmadan önce `fit` ediliyor | Rastgele veride "çalışan" model |
| Bölüm 11 | Özellik seçimi çapraz doğrulamanın dışında | 0.716 → **0.780** |
| Bu bölüm | Hedeften sonra kaydedilen bir sütun | 0.815 → **1.000** |

Sonuncusu üçüncü alıştırmada karşına çıkacak. Bir model **%100 doğruluk**
veriyor ve karışıklık matrisinde tek bir hata yok. Bu bir başarı değil, bir
alarm.

**Savunmalar sırayla:**

1. `train_test_split` — testi en başta kapat.
2. **Pipeline** — ön işlemeyi modele bağla; çapraz doğrulamada her kat
   kendi hazırlığını yapsın.
3. **Sütun sütun düşün:** bu bilgi, tahmini yapacağım anda gerçekten elimde
   olacak mı? `followup_calls` sütunu hasta taburcu olduktan **sonra**
   yazılıyor.

Üçüncüsünü hiçbir araç yapamıyor. O senin işin.

## Aşırı öğrenme ve kararsızlık

| Belirti | Teşhis | Çare |
|---|---|---|
| Eğitim 1.000, test 0.80 | Aşırı öğrenme (yüksek varyans) | Basitleştir, veri ekle, **torbalama** |
| Eğitim 0.70, test 0.70 | Yetersiz öğrenme (yüksek yanlılık) | Daha güçlü model, **artırma** |
| Aynı veriyle farklı sonuç | Kararsızlık | Orman; ölçüldü: 14 puan → 8 puan |
| CV yayılımı çok geniş | Az veri ya da az pozitif | Daha çok kat değil, daha çok veri |

**Ormanda eğitim 1.000 olması aşırı öğrenme değil.** Bölüm 08'de ölçüldü:
25 ağaçta eğitim 1.000, test 0.90; 300 ağaçta yine 0.90. Her ağaç farklı
şeyler ezberlediği için ortalama temiz kalıyor.

Bu, tek bir ağaçtaki aynı tabloyla **taban tabana zıt** ve bu yüzden
karıştırılıyor.

## Ölçekleme: nerede gerekli

| Model | Ölçekleme | Ölçülen |
|---|---|---|
| KNN | **Zorunlu** | 0.64 → 0.92 |
| K-ortalamalar | **Zorunlu** | 0.202 → 0.517 |
| PCA | **Zorunlu** | Varyansa bakıyor |
| Lojistik regresyon | Yararlı | Yakınsamayı hızlandırıyor |
| Karar ağacı | **Gereksiz** | 0.80 → 0.80 |
| Rastgele orman | **Gereksiz** | İçindekilerin hepsi ağaç |

Kural tek cümle: **uzaklık ya da varyans hesaplayan her şey ölçekleme
istiyor; sıralamaya bakan hiçbir şey istemiyor.**

## Pipeline neyi çözüyor

Bölüm 11'in kazancı kod kısaltmak değil:

- **Sızıntı yapısal olarak imkânsızlaşıyor.** `cross_val_score` her katta
  bütün adımları baştan eğitiyor.
- **Model eksiksiz kaydediliyor.** Medyanlar, mod, kodlayıcının
  kategorileri, ölçek değerleri ve katsayılar tek dosyada.
- **Ham veriyle tahmin edilebiliyor** — eksik değerli ham veriyle bile.

Ölçülen: `city` ve `monthly` sütunları boş olan bir satır için model 0.466
döndürüyor. Elle hazırlanmış bir modelde bu satır bir çökme olurdu.

## Neyi yapabiliyorsun

- Bir tabloyu alıp hedefi belirlemek, taban çizgiyi kurmak ve bir modelin
  gerçekten iş görüp görmediğine karar vermek
- Regresyon ve sınıflandırma problemlerini ayırt etmek, her birine uygun
  ölçüyü seçmek
- Kirli veriyi (eksik değer, metin sütunu, ölçek farkı) sızıntı yapmadan
  hazırlamak
- Aşırı öğrenmeyi teşhis etmek ve çapraz doğrulamayla dürüstçe ölçmek
- Beş model ailesini tanımak: doğrusal, KNN, ağaç, topluluk, kümeleme
- Dengesiz veride doğruluğun yalanını görmek ve eşiği bilinçli seçmek
- Etiketsiz veride grup aramak ve **bulunanların gerçek olup olmadığını
  sorgulamak**
- Bütün bunları tek bir nesneye bağlayıp kaydetmek

## Neyi yapamıyorsun

Dürüst olmak gerekirse bu liste daha uzun:

- **Derin öğrenme.** Görüntü, ses ve metin bu modülün dışında kaldı.
  Sinir ağları ayrı bir alan ve `torch` ile başlıyor.
- **Zaman serisi.** Sıralı veride `train_test_split` **yanlış** — geleceği
  görmüş oluyorsun. Zaman bazlı ayırma ve `TimeSeriesSplit` gerekiyor.
- **Metin ve gömme.** Bir cümleyi sayıya çevirmek ayrı bir konu
  (`TfidfVectorizer` başlangıç, gömmeler devamı).
- **Nedensellik.** Bu modül boyunca **hiçbir yerde** "şu sütun şuna sebep
  oluyor" demedik. Model korelasyon buluyor; sebep bulmak deney tasarımı
  işi.
- **Üretime almak.** Servis etmek, izlemek, sürümlemek — MLOps.
- **Veri toplamak.** En pahalı ve en atlanan kısım. Bu modülde veriler
  hazır geldi; gerçek hayatta gelmiyor.

## Son söz

Bu modül boyunca tekrarlanan tek bir alışkanlık var: **tahmin etme, ölç.**

Ağacın mı ormanın mı kazandığını, ölçeklemenin gerekip gerekmediğini,
`k`'nın kaç olması gerektiğini, eşiğin nereye konacağını — hiçbirini
bilmiyorduk. Hepsini ölçtük ve bazılarında sezgi yanıldı.

Aşağıdaki sınav on iki bölümün tamamını kapsıyor, alıştırmalar ise beş
uçtan uca proje. Üçüncüsünde sana **mükemmel çalışan** bir model verilecek.
Şüphelenmen bekleniyor.
