# HTTP Yanıtı ve Durum Kodları

İsteği gönderdin. Sunucu ne derse desin, cevabı aynı biçimde gelir: bir
**HTTP yanıtı**. Yanıtın ilk satırındaki üç haneli sayı, bütün yanıtın en
önemli bilgisi: **durum kodu** (status code). İsteğin işe yarayıp
yaramadığını, yaramadıysa kimin hatası olduğunu bu sayı söyler.

Bir API ile çalışırken her yanıtta ilk iş durum koduna bakmak. Gövdeyi
okumadan önce "istek başarılı mı?" diye sormayan kod, bir gün hata mesajını
veri sanıp yanlış bir sonuç üretir.

## Bir yanıt da düz bir metin

Hava durumu isteğine gelen yanıt yolda şöyle görünüyor:

```text
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 49

{"city": "Istanbul", "temp": 18, "sky": "cloudy"}
```

Yapı isteğe çok benziyor:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>Durum satırı</span><span><code>HTTP/1.1 200 OK</code>: sürüm, durum kodu, açıklama</span></div>
    <div class="anat-row"><span>Başlıklar</span><span><code>Content-Type</code>, <code>Content-Length</code>: yanıt hakkında bilgiler</span></div>
    <div class="anat-row"><span>Boş satır</span><span>Başlıkların bittiğini söyler</span></div>
    <div class="anat-row"><span>Gövde</span><span>Asıl veri ya da hatanın açıklaması</span></div>
  </div>
  <figcaption>İstekle aynı dört parça; tek fark ilk satır. İstekte "ne istiyorum", yanıtta "ne oldu".</figcaption>
</figure>

Tek fark ilk satırda: istekte **istek satırı** (yöntem, hedef, sürüm) vardı,
yanıtta **durum satırı** var.

## Durum satırı

```text
HTTP/1.1  200  OK
│         │    │
sürüm     kod  açıklama
```

- **Sürüm:** isteğinkiyle aynı.
- **Kod:** üç haneli sayı. Programın baktığı şey bu.
- **Açıklama** (reason phrase): kodun insan için yazılmış adı. Sunucudan
  sunucuya değişebilir, hatta HTTP/2'de hiç gönderilmez. **Programında
  açıklamaya değil koda bak.**

## İlk hane her şeyi söyler

Durum kodunun ilk hanesi bir **sınıf**:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>1xx</span><span>Bilgi: "devam et". Nadiren görürsün.</span></div>
    <div class="anat-row"><span>2xx</span><span><b>Başarı.</b> İstek yerine getirildi.</span></div>
    <div class="anat-row"><span>3xx</span><span>Yönlendirme: aradığın başka bir adreste.</span></div>
    <div class="anat-row"><span>4xx</span><span><b>İstemci hatası:</b> isteğinde bir yanlış var.</span></div>
    <div class="anat-row"><span>5xx</span><span><b>Sunucu hatası:</b> istek doğru olabilir, sunucuda sorun var.</span></div>
  </div>
  <figcaption>Kodun ilk hanesi sınıfı söyler. 404'ü hiç görmemiş olsan bile 4 ile başladığı için "benim isteğimde sorun var" dersin.</figcaption>
</figure>

En kullanışlı ayrım 4 ile 5 arasında:

- **4xx:** "Sen yanlış bir şey istedin." Adres yanlış, anahtar eksik, gövde
  bozuk. Aynı isteği değiştirmeden tekrar gönderirsen aynı hatayı alırsın;
  **isteği düzeltmen** gerekiyor.
- **5xx:** "Bende bir sorun var." Sunucu çöktü, bakımda, aşırı yüklü. İstek
  doğru olabilir; **bir süre bekleyip yeniden denemek** işe yarayabilir.

Python'da ilk haneyi almak için tam sayı bölmesi yeter: `404 // 100` → `4`.

## Sık göreceğin kodlar

| Kod | Adı | Ne zaman |
|---|---|---|
| `200` | OK | İstek başarılı, gövdede yanıt var |
| `201` | Created | `POST` ile yeni kayıt oluşturuldu |
| `204` | No Content | Başarılı, ama gövde boş (çoğu `DELETE`) |
| `301` | Moved Permanently | Kaynak kalıcı olarak başka adrese taşındı |
| `304` | Not Modified | Sende olan kopya hâlâ güncel |
| `400` | Bad Request | İstek bozuk: eksik ya da yanlış biçimli bilgi |
| `401` | Unauthorized | Kim olduğunu söylemedin ya da anahtar geçersiz |
| `403` | Forbidden | Kim olduğunu biliyorum ama buna iznin yok |
| `404` | Not Found | Böyle bir adres ya da kayıt yok |
| `405` | Method Not Allowed | Bu adreste bu yöntem kullanılamaz |
| `409` | Conflict | Kaynağın şu anki hâliyle çakışıyor (aynı ad zaten var) |
| `422` | Unprocessable Content | Biçim doğru ama değerler geçersiz (yaş −5) |
| `429` | Too Many Requests | Çok sık istek attın; biraz bekle |
| `500` | Internal Server Error | Sunucunun kodunda bir hata oluştu |
| `502` | Bad Gateway | Aradaki sunucu arkadakinden bozuk yanıt aldı |
| `503` | Service Unavailable | Sunucu şu an hizmet veremiyor (bakım, yük) |
| `504` | Gateway Timeout | Aradaki sunucu arkadakinden zamanında yanıt alamadı |

Bunları ezberlemen gerekmiyor. Sınıfı (ilk hane) her zaman bil; ayrıntısı
gerektiğinde bu tabloya ya da API'nin belgesine bakılır.

## Karıştırılan çiftler

**401 ile 403.** Adları yanıltıcı. `401` "seni tanımıyorum": anahtar yok ya
da yanlış. `403` "seni tanıyorum ama bu kapı sana kapalı". 401'de anahtarına
bakarsın; 403'te başka bir anahtar ya da izin gerekir.

**400 ile 422.** `400` isteğin kendisi okunamıyor (bozuk JSON gibi). `422`
okunuyor ama içindeki değerler kurallara uymuyor (boş başlık, negatif
fiyat). Bazı API'ler ikisi için de `400` kullanır.

**404 her zaman "adres yanlış" değil.** `/books/9999` adresi doğru yazılmış
olabilir; yalnızca 9999 numaralı kitap yoktur. Sunucu iki durumda da `404`
der.

## Yanıt başlıkları

İstekteki gibi, yanıtta da başlıklar yanıt **hakkında** bilgi taşır:

| Başlık | Ne söyler |
|---|---|
| `Content-Type` | Gövdenin biçimi: `application/json; charset=utf-8` |
| `Content-Length` | Gövdenin bayt sayısı |
| `Location` | `201`'de yeni kaydın adresi, `3xx`'te gidilecek yeni adres |
| `Retry-After` | `429` ve `503`'te: kaç saniye sonra yeniden denenebileceği |

`Content-Type` değerinin sonunda `; charset=utf-8` gibi bir ek olabilir;
metnin hangi kodlamayla yazıldığını söyler. Biçimi sorarken noktalı virgülden
önceki kısma bakarsın.

## Hata yanıtlarının gövdesi

İyi bir API hata verdiğinde gövdede nedenini de yazar:

```text
HTTP/1.1 422 Unprocessable Content
Content-Type: application/json

{"error": "validation", "detail": "price must be positive"}
```

Durum kodu "ne tür bir sorun", gövde "tam olarak ne" sorusunu cevaplıyor.
Hata aldığında gövdeyi okumak çoğu zaman düzeltmeyi doğrudan söyler.

## Ne zaman ne yapılır?

| Gelen | Yapılacak |
|---|---|
| `2xx` | Gövdeyi kullan (`204`'te gövde yok) |
| `3xx` | `Location`'daki adrese git (istek kütüphaneleri bunu kendisi yapar) |
| `401` / `403` | Anahtarına ve iznine bak |
| `404` | Adresi ve kaydın kimliğini denetle |
| `429` | `Retry-After` kadar bekle, sonra yeniden dene |
| Diğer `4xx` | İsteği düzelt; aynısını tekrar gönderme |
| `5xx` | Bir süre bekleyip yeniden dene; sürerse sunucunun sahibine bildir |

Bu tablo, Bölüm 11'de yazacağın hata yönetiminin iskeleti.

## Python'da durum kodları

Python'un hazır `http` modülünde bütün kodların adları var:

```python
from http import HTTPStatus

print(HTTPStatus(404).phrase)   # Not Found
print(HTTPStatus(429).phrase)   # Too Many Requests
print(HTTPStatus.OK.value)      # 200
```

Kodu sınıfına ayırmak:

```python
code = 503
kind = code // 100
if kind == 2:
    print("success")
elif kind == 4:
    print("my request is wrong")
elif kind == 5:
    print("the server has a problem")
```

## Özet

- Yanıt dört parça: **durum satırı** (sürüm, kod, açıklama), **başlıklar**,
  **boş satır**, **gövde**.
- Programda **koda** bak, açıklamaya değil.
- İlk hane sınıfı söyler: `2xx` başarı, `3xx` yönlendirme, `4xx` senin
  hatan, `5xx` sunucunun hatası.
- `4xx`'te isteği düzelt; `5xx`'te ve `429`'da bekleyip yeniden dene.
- `401` tanınmıyorsun, `403` izin yok, `404` böyle bir şey yok, `422`
  değerler geçersiz.
- Hata yanıtının gövdesi çoğu zaman nedenini yazar; oku.
