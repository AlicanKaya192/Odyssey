# XSS: Siteler Arası Betik

SQL Enjeksiyonu bölümünde kullanıcının verisi **veritabanında** kod gibi
yorumlanıyordu. XSS'te (cross-site scripting, siteler arası betik) aynı
hata **tarayıcıda** olur: sitenin sayfaya koyduğu kullanıcı metni HTML ya
da JavaScript olarak yorumlanır ve başka bir kullanıcının tarayıcısında,
o sitenin yetkisiyle çalışır. Bu bölüm açığın nasıl oluştuğunu küçük bir
oyuncak örnekte gösteriyor, ardından savunmalarını sırayla kuruyor:
bağlama uygun çıktı kodlama, otomatik kodlayan şablonlar, güvenli
bağlantılar ve içerik güvenliği politikası (CSP). Örneklerde HTML yalnızca
Python metni olarak üretiliyor; hiçbir tarayıcı açılmıyor.

## Sorun: metin HTML'e dönüşüyor

Bir blog, yorumları sayfaya olduğu gibi yazıyor:

```python
comment = "Nice post! <b>bold</b> <script>showPopup()</script>"
page = f"<p>{comment}</p>"
print(page)
```

```text
<p>Nice post! <b>bold</b> <script>showPopup()</script></p>
```

Tarayıcı bu sayfayı açtığında `<b>` etiketini kalın yazı olarak çizer,
`<script>` etiketinin içini de **çalıştırır**. Buradaki `showPopup()`
hayalî bir fonksiyon; ama aynı yere yazılan gerçek bir betik, sayfayı
açan herkesin tarayıcısında o sitenin bir parçası gibi çalışır: sayfanın
içeriğini okuyabilir, kullanıcı adına istek gönderebilir, `HttpOnly`
olmayan çerezlere erişebilir (Oturum ve Çerez bölümü). Yorumu yazan
kullanıcı, sayfayı okuyan **başka** kullanıcılara kod çalıştırmış olur.

## Üç tür

<figure class="fig anat">
  <div class="anat-row"><span><b>Kalıcı</b> (stored)</span><span>Kötü metin veritabanına kaydedilir (yorum, profil adı) ve sayfayı açan herkese sunulur. En geniş etkili tür.</span></div>
  <div class="anat-row"><span><b>Yansıtılan</b> (reflected)</span><span>Metin istekten gelir (arama kutusu, adres parametresi) ve aynı cevapta sayfaya geri yazılır. Kurbanın hazırlanmış bir bağlantıya tıklaması gerekir.</span></div>
  <div class="anat-row"><span><b>DOM tabanlı</b></span><span>Sunucu hiç karışmaz; sayfanın kendi JavaScript kodu adresten ya da başka bir kaynaktan aldığı metni sayfaya HTML olarak yazar.</span></div>
  <figcaption>Üçünün kök nedeni aynı: güvenilmeyen metin, kodlanmadan HTML'e ya da betiğe giriyor.</figcaption>
</figure>

## Birinci savunma: çıktı kodlama

Çözüm, metni sayfaya yazarken HTML için anlamı olan karakterleri
**zararsız karşılıklarına** çevirmektir: `<` yerine `&lt;`, `>` yerine
`&gt;`, `&` yerine `&amp;`, tırnaklar yerine `&quot;` ve `&#x27;`.
Tarayıcı bunları ekranda yine `<` ve `>` olarak gösterir ama etiket olarak
okumaz. Python'da bunu `html.escape` yapar:

```python
import html

comment = "Nice post! <b>bold</b> <script>showPopup()</script>"
print(f"<p>{html.escape(comment)}</p>")
print(html.escape('He said "hi" & left'))
```

```text
<p>Nice post! &lt;b&gt;bold&lt;/b&gt; &lt;script&gt;showPopup()&lt;/script&gt;</p>
He said &quot;hi&quot; &amp; left
```

Yorum artık sayfada yazıldığı gibi görünür; hiçbir etiketi çalışmaz.
`&` işaretinin de çevrildiğine dikkat: aksi hâlde `&lt;` yazan bir kişinin
metni ekranda `<` olarak çıkardı.

Bu, OWASP Top 10 bölümündeki enjeksiyon kuralının HTML karşılığıdır:
SQL'de **parametre**, HTML'de **çıktı kodlama**. İkisinde de veri,
verinin gittiği dilin kurallarına göre işaretlenir ve kod olamaz.

## Bağlam önemlidir

Doğru kodlama, metnin sayfada **nereye** gittiğine bağlıdır. Aynı değer
farklı yerlerde farklı işlem ister:

<figure class="fig anat">
  <div class="anat-row"><span>HTML gövdesi</span><span><code>&lt;p&gt;...&lt;/p&gt;</code> içi: HTML kodlama (<code>html.escape</code>).</span></div>
  <div class="anat-row"><span>Öznitelik değeri</span><span><code>title="..."</code> içi: tırnaklar da kodlanır ve değer her zaman tırnak içinde yazılır.</span></div>
  <div class="anat-row"><span>Bağlantı adresi</span><span><code>href="..."</code> içi: HTML kodlamaya ek olarak <b>şema</b> denetlenir; yalnızca <code>http</code> ve <code>https</code>.</span></div>
  <div class="anat-row"><span>Betik içi</span><span><code>&lt;script&gt;</code> bloğunun içine kullanıcı verisi yazılmaz; gerekiyorsa veri ayrı bir yerden (ör. bir öznitelikten) okunur.</span></div>
  <figcaption>Tek bir "kaçış" fonksiyonu her bağlamı korumaz; bağlama uygun kodlama gerekir.</figcaption>
</figure>

Bağlantı adresi en sık atlanan bağlamdır. HTML kodlama tırnakları
etkisizleştirir ama adresin **şemasına** dokunmaz; `javascript:` ile
başlayan bir adres tıklanınca betik çalıştırır. Bu yüzden adres bir
ayrıştırıcıyla parçalanır ve şeması bir izin listesiyle denetlenir (HTTP
ve HTTPS bölümündeki `urlsplit`):

```python
import html
from urllib.parse import urlsplit


def safe_link(url, label):
    if urlsplit(url).scheme not in ("http", "https"):
        return html.escape(label)
    return f'<a href="{html.escape(url)}">{html.escape(label)}</a>'


print(safe_link("https://example.com/a?x=1&y=2", "docs"))
print(safe_link("javascript:showPopup()", "click"))
print(safe_link('https://example.com/" title="x', "quote"))
```

```text
<a href="https://example.com/a?x=1&amp;y=2">docs</a>
click
<a href="https://example.com/&quot; title=&quot;x">quote</a>
```

İlk adres geçerli bir bağlantı oldu (`&` kodlandı). İkincisinin şeması
izin listesinde olmadığı için bağlantı hiç üretilmedi, yalnızca metin
kaldı. Üçüncüsündeki tırnak kodlandığı için `href` değerinden taşıp yeni
bir öznitelik açamadı.

## İkinci savunma: otomatik kodlayan şablon

Elle `html.escape` çağırmak, **bir kez** unutulduğunda açık bırakır. Bu
yüzden gerçek uygulamalar HTML'i, değerleri **varsayılan olarak**
kodlayan şablon motorlarıyla üretir. Fikri küçük bir fonksiyonla
gösterelim:

```python
import html
from string import Template


def render(template, **values):
    safe = {k: html.escape(str(v)) for k, v in values.items()}
    return Template(template).substitute(safe)


print(render("<p>Hello, $name!</p>", name="<i>Ada</i>"))
```

```text
<p>Hello, &lt;i&gt;Ada&lt;/i&gt;!</p>
```

Şablona giren her değer kodlandı; geliştiricinin hatırlaması gerekmedi.
Şablon motorlarında kodlamayı **kapatan** işaretler (bir değeri "güvenli"
ya da "ham" diye işaretlemek) dikkatle kullanılır; XSS açıklarının çoğu
bu kapıların yanlış yerde açılmasından çıkar. Kullanıcının biçimli metin
(kalın, bağlantı) yazabilmesi gerekiyorsa kendi düzenli ifadeni yazmak
yerine, izin verilen etiketleri bir listeyle sınırlayan, bakımı süren bir
temizleme kütüphanesi kullanılır.

## Üçüncü savunma: içerik güvenliği politikası (CSP)

Kodlamada bir yer gözden kaçarsa ne olur? **CSP** (Content Security
Policy) tarayıcıya, sayfada **hangi betiklerin çalışabileceğini** söyleyen
bir cevap başlığıdır. Örneğin yalnızca sitenin kendi dosyalarından gelen
betiklere izin verilir ve sayfanın içine gömülmüş betikler çalışmaz:

```python
def parse_csp(header):
    policy = {}
    for part in header.split(";"):
        words = part.split()
        if words:
            policy[words[0].lower()] = words[1:]
    return policy


csp = parse_csp("default-src 'self'; script-src 'self'; object-src 'none'")
print(csp["script-src"])
print("'unsafe-inline'" in csp["script-src"])
```

```text
["'self'"]
False
```

`script-src 'self'` yalnızca aynı siteden yüklenen betik dosyalarına izin
verir; sayfaya bir şekilde sızmış `<script>...</script>` bloğu
çalışmaz. `'unsafe-inline'` eklenirse bu koruma ortadan kalkar; adı da
bunu söylüyor. CSP kodlamanın **yerine** değil, gözden kaçan bir hataya
karşı **ikinci katmandır** (CORS ve Güvenlik Başlıkları bölümü).

## Zararı sınırlamak

- Oturum çerezi **`HttpOnly`**: sızan bir betik çerezi okuyamaz (yine de
  kullanıcı adına istek gönderebilir; bu yüzden asıl çözüm kodlamadır).
- **Girdi doğrulama:** yaş alanı sayı, kullanıcı adı yalnızca belirli
  karakterler (Girdi Doğrulama bölümü). Kodlamanın yanında bir katman.
- Önemli işlemlerde (parola değişimi) parola yeniden sorulur; sızan bir
  betik bunu tek başına yapamaz.

## Özet

- **XSS:** güvenilmeyen metin kodlanmadan sayfaya yazılınca tarayıcıda
  kod olarak çalışır; sayfayı açan başka kullanıcıları etkiler.
- Türler: **kalıcı**, **yansıtılan**, **DOM tabanlı**; kök neden aynı.
- Birinci savunma **çıktı kodlama**: `html.escape` ile `< > & " '`
  karakterleri zararsız karşılıklarına çevrilir.
- Kodlama **bağlama göre** seçilir; bağlantı adresinde şema da denetlenir
  (yalnızca `http`, `https`).
- **Otomatik kodlayan şablonlar** unutmayı önler; kodlamayı kapatan
  işaretler dikkatle kullanılır.
- **CSP** gömülü betikleri durdurur; `'unsafe-inline'` korumayı kaldırır.
- `HttpOnly` çerez ve girdi doğrulama zararı sınırlar, kodlamanın yerini
  tutmaz.
