Bir hata yanıtı geldiğinde hangi sırayla bakılacağı, örneklerle.

## Sıra

1. **Durum kodu:** hangi sınıf? `4xx` mı `5xx` mi?
2. **Gövde:** API nedenini yazmış mı? (`error`, `detail`, `message` gibi
   alanlar)
3. **Başlıklar:** `Retry-After` var mı? `Location` var mı?
4. **Kendi isteğin:** adres, yöntem, başlıklar, gövde belgeyle uyuşuyor mu?

## Örnek 1

```text
HTTP/1.1 401 Unauthorized
Content-Type: application/json

{"error": "missing api key"}
```

Anahtar gönderilmemiş. Belgede anahtarın hangi başlığa yazılacağına bak
(Bölüm 08).

## Örnek 2

```text
HTTP/1.1 404 Not Found
Content-Type: application/json

{"error": "book 9999 not found"}
```

Adres doğru, kayıt yok. Kimliği (9999) nereden aldığına bak.

## Örnek 3

```text
HTTP/1.1 405 Method Not Allowed
Allow: GET, POST
```

Bu adreste kullandığın yöntem geçerli değil. `Allow` başlığı geçerli
olanları listeliyor: belki `PUT` yerine `POST` gerekiyordu.

## Örnek 4

```text
HTTP/1.1 429 Too Many Requests
Retry-After: 30
```

İstek doğru, yalnızca çok sık. 30 saniye bekle, aynısını gönder.

## Örnek 5

```text
HTTP/1.1 503 Service Unavailable
Retry-After: 120

{"error": "maintenance"}
```

Sunucu bakımda. Senin yapacağın bir şey yok; iki dakika sonra yeniden dene.

## Yapma

- Hata yanıtının gövdesini veri sanıp işlemeye devam etme. Önce kod.
- `4xx` aldığın isteği değiştirmeden döngüde tekrar tekrar gönderme; hep
  aynı hatayı alırsın ve sunucu seni `429` ile durdurabilir.
