# Genel Tekrar

API 1'in sonuna geldin. "API nedir?" sorusuyla başladın; şimdi bir API'den
sayfa sayfa, hatalara ve hız sınırına dayanıklı biçimde veri çekip temiz bir
veri setine dökebiliyorsun. Bu bölüm yolu baştan sona bir kez daha yürüyor:
her durakta en önemli fikir ve en çok kullanacağın kod.

<figure class="fig">
  <div class="flow">
    <span class="node">Temeller<br><small>00–05</small></span><span class="arrow">→</span>
    <span class="node">requests<br><small>06–09</small></span><span class="arrow">→</span>
    <span class="node">Dayanıklı<br><small>10–12</small></span><span class="arrow">→</span>
    <span class="node">REST<br><small>13–14</small></span><span class="arrow">→</span>
    <span class="node acc">Veri hattı<br><small>15</small></span>
  </div>
  <figcaption>API 1'in yolu: kavramdan, gerçek bir veri setini güvenilir biçimde çeken bir programa.</figcaption>
</figure>

## 1. Kavramlar (Bölüm 00)

API, bir programın başka programlara açtığı kapı. Soran **istemci**,
cevaplayan **sunucu**; her konuşma bir **istek** ve bir **yanıt**. Uç nokta
API'nin tek bir kapısı; belge onun menüsü.

## 2. Adres (Bölüm 01)

```text
https://api.example.com:8443/v1/books/42?author=Austen#notes
şema     ana makine      port yol         sorgu dizesi  parça
```

Yol **neyi**, sorgu dizesi **nasıl** istediğini söyler; parça sunucuya
gitmez. `localhost` kendi bilgisayarın.

## 3. İstek ve yanıt (Bölüm 02–03)

İstek: istek satırı (yöntem, hedef, sürüm) + başlıklar + boş satır + gövde.
Yanıt: durum satırı + başlıklar + boş satır + gövde.

| Kod | Anlam | Yapılacak |
|---|---|---|
| `2xx` | Başarı | Gövdeyi kullan |
| `4xx` | Senin hatan | İsteği düzelt (`429` hariç) |
| `429` | Çok sık | `Retry-After` kadar bekle |
| `5xx` | Sunucunun sorunu | Bekleyip yeniden dene |

## 4. JSON ve tablo (Bölüm 04–05)

`json.loads` metinden Python'a, `json.dumps` tersine. İç içe yanıtı tabloya
dökmenin beş adımı: zarfı aç, sütunları seç, iç içeyi düzleştir, listelere
karar ver, türleri düzelt.

## 5. requests (Bölüm 06–09)

```python
import requests

r = requests.get(url, params={...}, headers={...}, timeout=10)
r.status_code, r.headers["Content-Type"], r.json(), r.url
r.raise_for_status()

requests.post(url, json=veri, headers=AUTH)        # 201 + Location
requests.patch(url, json={"price": 8.99}, headers=AUTH)
requests.delete(url, headers=AUTH)                 # 204
```

Kimlik: `X-API-Key` başlığı, `Authorization: Bearer <jeton>` ya da
`auth=(ad, şifre)`. `401` tanınmıyorsun, `403` iznin yok. Anahtar koda değil
ortam değişkenine.

## 6. Dayanıklılık (Bölüm 10–12)

- **Sayfalama:** sayfa numarası, `next` bağlantısı, ofset + sınır, imleç.
  Döngünün açık bir durma koşulu ve güvenlik sınırı olsun.
- **Hatalar:** her isteğe `timeout`; `Timeout` ve `ConnectionError`'ı yakala;
  yalnızca geçici hataları ve tekrarlanabilir istekleri yeniden dene; üstel
  geri çekilme.
- **Hız sınırı:** `429`'da bekle; daha iyisi istekleri aralıklı gönder.

## 7. Tasarım ve araçlar (Bölüm 13–14)

REST: kaynaklar ve adresleri, adreste isim / yöntemde eylem, yöntem ve kod
sözleşmesi, durumsuzluk, bağlantılar. Araçlar: tarayıcı ve Ağ sekmesi, curl,
Swagger UI / OpenAPI, Postman, Bruno.

## 8. Veri hattı (Bölüm 15)

**Çek → sakla → düzleştir → denetle → yaz.** Ham yanıtı önbelleğe al,
yazmadan önce denetle, güncellemeyi artımlı yap, hattın iki kez çalışınca
aynı sonucu versin.

## Bütün parçalar bir arada

Bu kısa program, patikanın neredeyse bütün fikirlerini kullanıyor:

```python
import os
import time
import requests

BASE = "http://api.odyssey.test"
token = os.environ.get("LIBRARY_TOKEN", "letmein")
session = requests.Session()
session.headers.update({"Authorization": "Bearer " + token})

def get(path, params=None):
    for attempt in range(4):
        try:
            r = session.get(BASE + path, params=params, timeout=10)
        except (requests.Timeout, requests.ConnectionError):
            time.sleep(2 ** attempt)
            continue
        if r.status_code == 429:
            time.sleep(int(r.headers.get("Retry-After", 1)))
            continue
        if r.status_code >= 500:
            time.sleep(2 ** attempt)
            continue
        r.raise_for_status()
        return r.json()
    raise RuntimeError("giving up on " + path)

books, url_params = [], {"tag": "scifi", "per_page": 20, "page": 1}
while True:
    body = get("/books", url_params)
    books.extend(body["data"])
    if not body["links"]["next"]:
        break
    url_params["page"] += 1
print(len(books), "science fiction books")
```

Satır satır okuyabiliyorsan, bu patikanın amacına ulaştın.

## Sırada ne var?

API 2'de masanın öbür tarafına geçeceksin: FastAPI ile **kendi** API'ni
yazacak, uç noktalar tanımlayacak, gelen veriyi doğrulayacak, kimlik
isteyecek, belgeni `/docs`'ta göreceksin. Bu patikada istemci olarak
öğrendiğin her kural (yöntemler, kodlar, REST tasarımı), orada sunucu olarak
uygulayacağın kurallar.
