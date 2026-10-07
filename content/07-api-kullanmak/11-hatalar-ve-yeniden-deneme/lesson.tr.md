# Hatalar, Zaman Aşımı ve Yeniden Deneme

Şimdiye kadarki istekler hep yolunda gitti: sunucu ayaktaydı, hızlı cevap
verdi, bağlantı kopmadı. Gerçek hayatta öyle olmuyor. Sunucu bakımdadır,
aşırı yüklüdür, ağ bir an kopar, yanıt hiç gelmez. API'yle çalışan bir
programın asıl sınavı, işler ters gittiğinde ne yaptığıdır.

Bu bölümde üç şeyi öğreneceksin: **zaman aşımı** koymak, hataları **türüne
göre** yakalamak ve geçici hatalarda **akıllıca yeniden denemek**.

## İki tür hata

API ile çalışırken karşına iki ayrı tür sorun çıkar:

<figure class="fig">
  <div class="versus">
    <div class="dim"><h4>Yanıt geldi, kötü haber</h4><p><code>404</code>, <code>500</code>, <code>503</code>...<br>Bağlantı çalıştı, sunucu konuştu.<br>requests hata fırlatmaz; <b>koda bakarsın</b> ya da <code>raise_for_status()</code>.</p></div>
    <div class="no"><h4>Yanıt hiç gelmedi</h4><p>Zaman aşımı, bağlantı kurulamadı.<br>Konuşulacak bir sunucu yok.<br>requests <b>istisna fırlatır</b>; <code>try</code>/<code>except</code> ile yakalarsın.</p></div>
  </div>
  <figcaption>İkisini ayırmak, hangi durumda ne yapacağını belirliyor.</figcaption>
</figure>

- **Yanıt geldi ama kötü haber:** `404`, `500`, `503`. Bağlantı çalıştı,
  sunucu konuştu. requests bunları hata saymaz (Bölüm 06); koda bakarsın.
- **Yanıt hiç gelmedi:** sunucuya ulaşılamadı ya da sunucu zamanında cevap
  vermedi. Burada requests bir **istisna** fırlatır; yakalamazsan program
  durur.

## Zaman aşımı: her isteğe süre koy

requests varsayılan olarak **sonsuza kadar bekler.** Sunucu cevap vermezse
programın donar kalır. Bu yüzden altın kural: **her isteğe `timeout=` ver.**

```python
import requests

BASE = "http://api.odyssey.test"
try:
    requests.get(BASE + "/slow", timeout=1)
except requests.Timeout as error:
    print("Timeout:", type(error).__name__)   # Timeout: ReadTimeout
```

Alıştırma sunucusunun `/slow` uç noktası 3 saniye sonra cevap veriyor; 1
saniye beklemeye razı olan istek `requests.Timeout` fırlattı. Süreyi
artırınca cevap geliyor:

```python
r = requests.get(BASE + "/slow", timeout=5)
print(r.status_code)   # 200
```

Kaç saniye? İşe göre değişir; sık kullanılan bir başlangıç 5–10 saniye.
Önemli olan bir değer **koymak**.

## Bağlantı hatası

Sunucuya hiç ulaşılamıyorsa (ad çözülemedi, makine kapalı, ağ yok)
`requests.ConnectionError` gelir:

```python
try:
    requests.get("http://offline.odyssey.test/books", timeout=3)
except requests.ConnectionError as error:
    print("ConnectionError:", type(error).__name__)
```

## İstisna ailesi

requests'in hataları bir aile: hepsi `requests.RequestException`'dan türüyor.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span><code>RequestException</code></span><span>Hepsinin atası: "istekle ilgili bir sorun"</span></div>
    <div class="anat-row"><span>├ <code>Timeout</code></span><span>Yanıt zamanında gelmedi (<code>ConnectTimeout</code>, <code>ReadTimeout</code>)</span></div>
    <div class="anat-row"><span>├ <code>ConnectionError</code></span><span>Sunucuya ulaşılamadı</span></div>
    <div class="anat-row"><span>├ <code>HTTPError</code></span><span><code>raise_for_status()</code> 4xx/5xx gördü</span></div>
    <div class="anat-row"><span>└ <code>JSONDecodeError</code>, <code>MissingSchema</code>...</span><span>Diğerleri</span></div>
  </div>
  <figcaption><code>except requests.RequestException</code> hepsini yakalar; özel olanları önce yazarsan her birine ayrı tepki verebilirsin.</figcaption>
</figure>

Bu, yakalarken iki seçenek veriyor:

```python
try:
    r = requests.get(BASE + "/books/1", timeout=5)
    r.raise_for_status()
except requests.Timeout:
    print("too slow")
except requests.ConnectionError:
    print("cannot reach the server")
except requests.HTTPError:
    print("bad status:", r.status_code)
except requests.RequestException as error:
    print("other request problem:", error)
```

Özelden genele doğru yazılır: önce `Timeout`, sonra `ConnectionError`, en
sonda hepsini yakalayan `RequestException`. Sıra ters olursa genel olan her
şeyi yakalar ve özel durumlara hiç sıra gelmez.

## Hangi hata yeniden denenir?

Yeniden denemek yalnızca **geçici** sorunlarda işe yarar. Bölüm 03'ün kuralı
burada karara dönüşüyor:

| Durum | Geçici mi? | Yeniden dene? |
|---|---|---|
| `Timeout`, `ConnectionError` | Çoğu zaman | Evet |
| `500`, `502`, `503`, `504` | Çoğu zaman | Evet |
| `429` | Evet | Evet, ama `Retry-After` kadar bekleyerek (Bölüm 12) |
| `400`, `401`, `403`, `404`, `422` | Hayır | **Hayır**: isteği düzelt |

Ve Bölüm 02'nin uyarısı: yeniden denenen istek **tekrarlanabilir** olmalı.
`GET`, `PUT`, `DELETE` güvenle tekrarlanır; `POST`'u tekrar göndermek kopya
kayıt oluşturabilir.

## Basit yeniden deneme

Alıştırma sunucusunun `/flaky` uç noktası ilk iki istekte `503` (meşgul)
veriyor, üçüncüde cevap veriyor:

```python
import time

for attempt in range(1, 6):
    r = requests.get(BASE + "/flaky", timeout=5)
    print("attempt", attempt, r.status_code)
    if r.status_code == 200:
        break
    time.sleep(1)
# attempt 1 503
# attempt 2 503
# attempt 3 200
```

Üç önemli parça var:

1. **Üst sınır:** `range(1, 6)` en fazla 5 deneme. Sonsuz deneme, sorunu
   sunucuya taşır.
2. **Bekleme:** `time.sleep(1)`. Beklemeden yeniden denemek, zaten zorlanan
   sunucuya daha çok yük bindirir.
3. **Başarıda çıkış:** `break`.

## Üstel geri çekilme (exponential backoff)

Her denemede **aynı** süre beklemek yerine süreyi katlamak daha iyi bir
alışkanlık: 1 saniye, 2 saniye, 4 saniye... Sunucu kısa bir aksaklık
yaşıyorsa hızla toparlanırsın; uzun bir sorun varsa onu boşuna yormazsın.
Buna **üstel geri çekilme** deniyor.

```python
def get_with_retry(url, attempts=4):
    delay = 1
    for attempt in range(attempts):
        try:
            r = requests.get(url, timeout=5)
            if r.status_code < 500:
                return r                 # başarı ya da düzeltilmesi gereken 4xx
        except (requests.Timeout, requests.ConnectionError):
            pass                         # geçici: yeniden dene
        if attempt < attempts - 1:
            time.sleep(delay)
            delay *= 2                   # 1, 2, 4, ...
    return None                          # bütün denemeler bitti
```

Fonksiyon `4xx`'i hemen döndürüyor: o hatayı beklemek düzeltmez. `5xx` ve
bağlantı sorunlarında bekleyip yeniden deniyor; son denemeden sonra
beklemiyor. Hiçbiri tutmazsa `None` döndürüyor ve karar çağırana kalıyor.

Gerçek sistemlerde bekleme süresine küçük bir rastgelelik de eklenir
(jitter): aynı anda düşen bin istemci aynı saniyede geri dönüp sunucuyu
yeniden boğmasın.

## Vazgeçmeyi bilmek

`/broken` her zaman `500` veriyor; kaç kez denersen dene düzelmeyecek.
Yeniden deneme bir **umut** değil bir **plan**: belli sayıda dene, sonra
vazgeç ve durumu açıkça bildir.

```python
r = get_with_retry(BASE + "/broken", attempts=3)
if r is None or r.status_code >= 500:
    print("the service is down; try again later")
```

İyi bir program vazgeçtiğinde ne olduğunu söyler: hangi adres, kaç deneme,
son hata. "Bir şeyler ters gitti" yetmez.

## Özet

- Hatalar iki türlü: **kötü yanıt** (4xx/5xx, koda bakarsın) ve **yanıt
  yok** (istisna: `Timeout`, `ConnectionError`).
- **Her isteğe `timeout=` ver**; requests varsayılan olarak sonsuza kadar
  bekler.
- Hepsi `requests.RequestException` ailesinden; özelden genele yakala.
- Yalnızca geçici hataları (`Timeout`, `ConnectionError`, `5xx`, `429`) ve
  yalnızca tekrarlanabilir istekleri yeniden dene; `4xx`'i düzelt.
- Yeniden denemede üst sınır ve bekleme olsun; **üstel geri çekilme** (1, 2,
  4 sn) iyi bir varsayılan.
- Denemeler bitince vazgeç ve durumu açıkça bildir.
