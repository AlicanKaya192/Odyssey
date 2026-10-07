# Hız Sınırı

Bir API'ye istediğin kadar hızlı istek atamazsın. Neredeyse her API bir
**hız sınırı** (rate limit) koyar: "dakikada 60 istek", "saniyede 3 istek",
"günde 10 000 istek". Sınırı aşan istemci `429 Too Many Requests` alır ve bir
süre bekletilir.

Bu sınır sana karşı değil, herkes için var. Tek bir istemcinin saniyede
binlerce isteği sunucuyu yavaşlatır ve öbür kullanıcıların işini bozar. Hız
sınırı sunucuyu korur ve kaynağı adil paylaştırır. Senin işin, sınıra
**saygılı** bir istemci yazmak.

## Sınırı aşınca ne olur?

Alıştırma sunucusunun `/limited` uç noktası saniyede 3 isteğe izin veriyor.
Beş isteği art arda gönderelim:

```python
import requests

BASE = "http://api.odyssey.test"
for i in range(5):
    r = requests.get(BASE + "/limited")
    left = r.headers.get("X-RateLimit-Remaining")
    print(i + 1, r.status_code, left, r.headers.get("Retry-After"))
# 1 200 2 None
# 2 200 1 None
# 3 200 0 None
# 4 429 0 1
# 5 429 0 1
```

İlk üçü geçti; dördüncü ve beşinci `429` aldı. Yanıtlar sana durumu her
adımda söylüyor:

<figure class="fig">
  <div class="flow">
    <span class="node">1. istek<br><small>200 · kalan 2</small></span><span class="arrow">→</span>
    <span class="node">2. istek<br><small>200 · kalan 1</small></span><span class="arrow">→</span>
    <span class="node">3. istek<br><small>200 · kalan 0</small></span><span class="arrow">→</span>
    <span class="node no">4. istek<br><small>429 · Retry-After: 1</small></span>
  </div>
  <figcaption>Sunucu her yanıtta kalan hakkını söylüyor; hak bitince 429 ve ne kadar bekleyeceğin geliyor.</figcaption>
</figure>

## Hız sınırı başlıkları

Birçok API kalan hakkını başlıklarda bildirir:

- `X-RateLimit-Limit`: penceredeki toplam hak (burada 3).
- `X-RateLimit-Remaining`: kalan hak. Sıfıra inince bir sonraki istek `429`
  alır.
- `X-RateLimit-Reset`: hakkın yenileneceği zaman (bazı API'lerde).
- `Retry-After`: `429` geldiğinde **kaç saniye** beklemen gerektiği.

Başlık adları API'den API'ye değişir (`RateLimit-Remaining`,
`X-Rate-Limit-Remaining`...); belgede yazar. `X-` ile başlayan adlar standart
olmayan, API'nin kendi koyduğu başlıklar.

## Yöntem 1: 429 gelince bekle

En temel davranış: `429` aldığında `Retry-After` kadar bekleyip **aynı
isteği** yeniden göndermek.

```python
import time

def get_politely(url):
    while True:
        r = requests.get(url, timeout=5)
        if r.status_code != 429:
            return r
        time.sleep(int(r.headers.get("Retry-After", 1)))
```

`Retry-After` yoksa makul bir varsayılan (1 saniye) bekle. Gerçek bir
programda bu döngüye de bir üst sınır koyarsın (Bölüm 11).

`429` diğer `4xx`'lerden farklı: istek **doğru**, yalnızca zamanı yanlış. Bu
yüzden düzeltmek değil beklemek gerekiyor.

## Yöntem 2: hızını ayarla

Daha iyisi sınıra hiç çarpmamak. Saniyede 3 istek hakkın varsa, istekleri
**aralıklı** gönder:

```python
codes = []
for i in range(6):
    r = requests.get(BASE + "/limited")
    codes.append(r.status_code)
    time.sleep(0.4)          # saniyede en fazla 2,5 istek
print(codes)   # [200, 200, 200, 200, 200, 200]
```

İsteklerin arasına 0,4 saniye koyunca sınırın altında kalıyoruz ve hiç
`429` almıyoruz. Bu yaklaşıma **hız ayarlama** (throttling) deniyor. Hesap
basit: sınır saniyede N istekse, istekler arasında en az `1 / N` saniye
olmalı; küçük bir pay bırakmak iyi olur.

## Yöntem 3: kalan hakkı izle

Başlıklar kalan hakkı söylüyorsa, sıfıra inince beklemek de bir yol:

```python
r = requests.get(BASE + "/limited")
if r.headers.get("X-RateLimit-Remaining") == "0":
    time.sleep(1)            # pencere yenilensin
```

Böylece hiç `429` almadan, hakkın bittiği anda durursun.

## Hangisi ne zaman

<figure class="fig">
  <div class="versus">
    <div class="dim"><h4>429 gelince bekle</h4><p>Kolay, her API'de çalışır.<br>Ama sınıra çarpıyorsun; her çarpışma boşa bir istek.</p></div>
    <div class="ok"><h4>Hızını ayarla</h4><p>İstekler arasında en az <code>1 / N</code> saniye.<br>Sınıra hiç çarpmazsın.<br>Yine de güvenlik ağı olarak 429'da beklemeyi koru.</p></div>
  </div>
  <figcaption>İyi bir istemci ikisini birlikte kullanır.</figcaption>
</figure>

Pratikte ikisi birlikte kullanılır: istekleri belli bir hızda gönderirsin
(ayar) **ve** yine de `429` gelirse beklersin (güvenlik ağı). Sınır değişebilir,
başka bir programın da aynı anahtarı kullanıyor olabilir; güvenlik ağı her
zaman olmalı.

## Sınırı aşmanın bedeli

Sınırı sürekli zorlayan istemcilere API'ler daha sert davranabilir: daha
uzun bekletme, geçici engel, hatta anahtarın iptali. Kurallara uyan bir
istemci:

- `Retry-After`'a uyar,
- isteklerini aralıklı gönderir,
- gereksiz istek atmaz (sonuçları saklar, süzmeyi sunucuya bırakır, büyük
  sayfa ister),
- birden çok programda aynı anahtarı kullanıyorsa toplam hızı hesaba katar.

## Özet

- API'ler hız sınırı koyar; aşan istemci `429 Too Many Requests` alır.
- `Retry-After` kaç saniye bekleneceğini, `X-RateLimit-Remaining` kalan
  hakkı söyler (adlar API'ye göre değişir).
- `429`'da **bekleyip aynı isteği** yeniden gönder; düzeltilecek bir şey yok.
- Daha iyisi sınıra çarpmamak: istekler arasında en az `1 / N` saniye bırak
  (hız ayarlama).
- Ayar ile güvenlik ağını birlikte kullan; gereksiz istek atma.
