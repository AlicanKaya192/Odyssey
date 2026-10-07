# API Nedir?

Telefonundaki hava durumu uygulaması havayı kendisi ölçmüyor. Bir termometresi,
bir uydusu yok. Yaptığı tek şey **başka bir programa sormak**: "İstanbul'da
hava kaç derece?" O program da cevabı geri gönderiyor.

Programların birbirine soru sorup cevap almasını sağlayan bu kapının adı
**API**. Bu patikada önce başkasının API'sinden veri istemeyi (API 1),
sonra kendi API'ni yazmayı (API 2) öğreneceksin.

Bu bölümde henüz internete bağlanmıyoruz. Önce kavramları oturtacağız:
kim soruyor, kim cevaplıyor, aradaki kurallar ne.

## Bir benzetme: restoran

Bir restorana gittiğini düşün.

- **Sen** yemek istiyorsun ama mutfağa girmiyorsun.
- **Mutfak** yemeği yapıyor ama seninle doğrudan konuşmuyor.
- **Menü** neleri isteyebileceğini söylüyor.
- **Garson** siparişini mutfağa götürüyor, tabağı sana getiriyor.

API, garson ile menünün toplamı gibi. Neyi isteyebileceğin belli (menü), nasıl
isteyeceğin belli (garsona söylemek) ve mutfağın içi senden gizli. Mutfakta
aşçı değişse, ocak değişse bile sen aynı menüden aynı şekilde sipariş
vermeye devam ediyorsun.

<figure class="fig">
  <div class="flow">
    <span class="node">Müşteri<br><small>istemci</small></span><span class="arrow">→</span>
    <span class="node acc">Garson + menü<br><small>API</small></span><span class="arrow">→</span>
    <span class="node">Mutfak<br><small>sunucu</small></span>
  </div>
  <figcaption>Müşteri mutfağa girmiyor; yalnızca menüdekini garsona söylüyor. API de istemciye sunucunun içini değil, yalnızca kapısını gösteriyor.</figcaption>
</figure>

Bu son cümle API'nin en önemli fikri: **içerisi değişebilir, kapı aynı
kalır.** Hava durumu şirketi ölçüm sistemini baştan yazsa bile, senin
uygulaman aynı soruyu aynı biçimde sormaya devam eder.

## Kelimenin açılımı

API, **A**pplication **P**rogramming **I**nterface: Uygulama Programlama
Arayüzü.

- **Uygulama:** bir program.
- **Programlama:** onu kullanan da bir program; insan değil.
- **Arayüz:** iki şeyin buluştuğu yüzey. Duvardaki priz bir arayüz: fişin
  biçimi belli, arkadaki kabloları bilmen gerekmiyor.

Yani API, **bir programın başka programlara açtığı kapı.** Kapının biçimini
programı yazan belirliyor.

## İstemci ve sunucu

Bir API konuşmasında iki taraf var:

- **İstemci** (client): soruyu soran program. Hava durumu uygulaması,
  tarayıcın, birazdan senin yazacağın Python kodu.
- **Sunucu** (server): soruyu cevaplayan program. Genellikle başka bir
  bilgisayarda, hep açık bekliyor.

İstemcinin gönderdiği soruya **istek** (request), sunucunun geri gönderdiği
cevaba **yanıt** (response) deniyor. Her konuşma bir istek ve bir yanıttan
oluşuyor; sunucu kendiliğinden konuşmuyor, hep sorulmayı bekliyor.

<figure class="fig">
  <div class="flow">
    <span class="node">İstemci</span><span class="arrow">→ istek →</span>
    <span class="node acc">Sunucu</span><span class="arrow">→ yanıt →</span>
    <span class="node">İstemci</span>
  </div>
  <figcaption>Her konuşma bir istek ve bir yanıttan oluşuyor. Konuşmayı her zaman istemci başlatıyor.</figcaption>
</figure>

"Sunucu" kelimesi seni korkutmasın. Sunucu özel bir makine olmak zorunda
değil; isteği bekleyen ve cevaplayan **her program** sunucu. API 2'de kendi
bilgisayarında bir sunucu çalıştıracaksın.

## Bir isteğin ve yanıtın görünüşü

İleride parçalarını tek tek öğreneceğiz; şimdilik bir göz at. Hava durumu
API'sine giden bir istek kabaca şöyle:

```text
GET /weather?city=Istanbul
```

"`/weather` adresinden, `city` değeri `Istanbul` olan bilgiyi **getir** (GET)"
demek. Sunucunun yanıtı:

```text
200 OK

{"city": "Istanbul", "temp": 18, "sky": "cloudy"}
```

`200 OK` "her şey yolunda" demek. Altındaki satır verinin kendisi; bu yazım
biçiminin adı **JSON** ve Python sözlüğüne çok benziyor. İkisini de ayrı
bölümlerde göreceğiz.

## Uç nokta: API'nin tek bir kapısı

Bir API'nin genellikle birden çok kapısı var. Hava durumu API'si şunları
sunabilir:

- `/weather`: şu anki hava
- `/forecast`: önümüzdeki günler
- `/cities`: bilinen şehirlerin listesi

Bunların her birine **uç nokta** (endpoint) deniyor. Uç nokta, API'nin belli
bir işi yapan tek kapısı. Menüdeki her yemek gibi.

Menüde olmayan bir şeyi istersen ne olur? Garson "bizde yok" der. API de
öyle: var olmayan bir uç noktaya istek atarsan sunucu **404 Not Found**
("bulunamadı") diye cevap verir. Bu sayıyı birçok web sitesinde de
görmüşsündür.

## Belgeler: API'nin menüsü

Bir API'yi kullanmak için önce **belgelerini** (documentation) okursun.
Belgeler şunları söyler:

- hangi uç noktalar var,
- her birine ne gönderilmesi gerekiyor (örneğin `city`),
- yanıtın neye benzediği,
- hangi hataların gelebileceği.

İyi bir API'nin belgesi menü kadar açıktır. Bu patikada okuduğun her API
için ilk iş belgeye bakmak olacak.

## Web sitesi ile API arasındaki fark

Aynı veri iki farklı biçimde sunulabilir:

<figure class="fig">
  <div class="versus">
    <div class="dim"><h4>Web sitesi (insan için)</h4><pre><code class="language-text">&lt;h1&gt;İstanbul&lt;/h1&gt;
&lt;p class="big"&gt;18°&lt;/p&gt;
&lt;p&gt;Bulutlu&lt;/p&gt;</code></pre><p>Renkler, yazı tipleri, düzen. Bilgi süslerin arasında.</p></div>
    <div class="ok"><h4>API (program için)</h4><pre><code class="language-json">{"city": "Istanbul",
 "temp": 18,
 "sky": "cloudy"}</code></pre><p>Süs yok. Her bilginin bir adı var; program doğrudan okuyor.</p></div>
  </div>
  <figcaption>Aynı bilgi, iki biçim. Programla bilgi çekmek gerekiyorsa API kullanılır.</figcaption>
</figure>

Web sitesi **insan için**: renkler, düzen, düğmeler. İçindeki bilgiyi bir
programla çekmek zor, çünkü bilgi süslerin arasına dağılmış. API **program
için**: süs yok, yalnızca düzenli veri. Bu yüzden bir programın başka bir
programdan bilgi alması gerekiyorsa API kullanılıyor.

## API neden var?

- **Güncel veri:** Döviz kuru, hava durumu, borsa her dakika değişiyor.
  Herkes ölçmek yerine kaynağa soruyor.
- **Başkasının işini kullanmak:** Harita, ödeme, çeviri gibi zor işleri
  sıfırdan yazmak yerine onları yapan servise sormak.
- **Kontrol:** Sunucu neyi, kime, ne kadar vereceğini kendisi seçiyor.
  Veritabanının kapısını herkese açmak yerine yalnızca menüdekileri sunuyor.
- **Dilden bağımsızlık:** Sunucu Java ile, istemci Python ile yazılmış
  olabilir. Kapının kuralları ortak olduğu sürece ikisi anlaşıyor.

## Veri bilimcisi neden bilmeli?

Veri her zaman hazır bir CSV dosyası olarak gelmiyor. Çoğu zaman bir
API'den çekiliyor:

- açık veri portalları (nüfus, trafik, hava kalitesi),
- şirketin kendi servisleri (satışlar, kullanıcı olayları),
- GitHub, döviz kuru, hava durumu gibi genel servisler.

Bir de öbür yönü var: eğittiğin bir modeli başkalarının kullanması için en
yaygın yol, onu bir API'nin arkasına koymak. "Bu evin fiyatı ne olur?" diye
soran bir uygulama, cevabı senin modelinin API'sinden alır. Bunu API 2'de
yapacaksın.

## REST: en yaygın API tarzı

API'ler farklı tarzlarda tasarlanabiliyor. Bugün en yaygını **REST**. Şimdilik
iki fikrini bilmen yeter:

- Her şey bir **kaynak** (resource): kitaplar, kullanıcılar, siparişler.
  Her kaynağın bir adresi var: `/books`, `/books/42`.
- Kaynakla ne yapacağını **HTTP yöntemi** söylüyor: getir (GET), ekle
  (POST), değiştir (PUT), sil (DELETE).

"REST API" dendiğinde bu kurallara uyan bir API kastediliyor. Patikanın
sonuna doğru REST'i ayrıntısıyla okuyacağız.

## Bu bölümün alıştırmaları

Henüz gerçek bir sunucuya bağlanmıyoruz. Alıştırmalarda sunucuyu **Python
sözlükleri ve fonksiyonlarıyla taklit edeceksin**: bir fonksiyon sunucu
olacak, istek alıp yanıt döndürecek; başka bir parça istemci olup onu
çağıracak. Gerçek API'ler de tam olarak bu fikrin üstüne kurulu, yalnızca
araya internet giriyor.

## Özet

- API, bir programın başka programlara açtığı kapı: neyin istenebileceği ve
  nasıl isteneceği belli, içerisi gizli.
- Soran **istemci**, cevaplayan **sunucu**. Her konuşma bir **istek** ve bir
  **yanıt**.
- **Uç nokta** API'nin tek bir kapısı (`/weather`). Olmayan kapı → **404**.
- **Belgeler** API'nin menüsü; kullanmadan önce okunur.
- Web sitesi insan için, API program için.
- **REST** en yaygın tarz: kaynaklar ve onlara uygulanan HTTP yöntemleri.
