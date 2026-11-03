# Girdi Doğrulama ve Çıktı Kodlama

SQL Enjeksiyonu ve XSS bölümleri aynı hatanın iki yüzünü gösterdi: veri,
gittiği yerde kod gibi yorumlandı. İki bölümde de asıl savunma **çıkışta**
idi (parametre, çıktı kodlama) ve girdi doğrulama "yanında bir katman"
olarak geçti. Bu bölüm o katmanı kendi başına ele alıyor: girdi nasıl
doğrulanır, hangi tuzaklar vardır (düzenli ifadenin yanlış kullanımı, aynı
görünen farklı metinler, dosya yolları, komut satırı) ve doğrulama ile
kodlama nasıl birlikte çalışır.

<figure class="fig"><div class="versus">
  <div><h4>Girdi doğrulama</h4>Veri <b>içeri girerken</b>: beklenen tür, uzunluk, aralık ve biçimde mi? Değilse reddedilir. Verinin <b>anlamını</b> denetler.</div>
  <div><h4>Çıktı kodlama</h4>Veri <b>bir yere yazılırken</b>: o yerin (HTML, SQL, URL, komut) kurallarına göre işaretlenir. Verinin <b>kod olmasını</b> engeller.</div>
</div><figcaption>İkisi birbirinin yerini tutmaz: geçerli bir ad da (<code>O'Brien</code>) SQL'i bozabilir.</figcaption></figure>

## İzin listesiyle doğrulamak

Doğrulamanın en sağlam biçimi **izin listesidir**: neyin geçerli olduğunu
tarif et, gerisini reddet. "Tehlikeli karakterleri" sayan bir kara liste
hep bir şeyi unutur (Güvenlik İlkeleri bölümündeki varsayılan ret).

```python
import re

COUNTRIES = {"TR", "DE", "US"}


def validate(form):
    errors = []
    if not re.fullmatch(r"[a-z0-9_]{3,20}", form.get("username", "")):
        errors.append("username")
    age = form.get("age", "")
    if not re.fullmatch(r"[0-9]{1,3}", age) or not 13 <= int(age) <= 120:
        errors.append("age")
    if form.get("country") not in COUNTRIES:
        errors.append("country")
    return errors


print(validate({"username": "ada_1", "age": "34", "country": "TR"}))
print(validate({"username": "Ada!", "age": "-5", "country": "XX"}))
print(validate({"username": "ada", "age": "999"}))
```

```text
[]
['username', 'age', 'country']
['age', 'country']
```

Her alan için üç soru soruldu: **tür** (sayı mı), **biçim** (yalnızca izin
verilen karakterler, belirli uzunlukta) ve **aralık ya da küme** (13–120
arası, bilinen ülkelerden biri). Eksik alan da hata sayıldı. Doğrulama
**sunucuda** yapılır; tarayıcıdaki doğrulama yalnızca kullanıcıya hızlı
geri bildirimdir, çünkü istek tarayıcı olmadan da yazılabilir (HTTP ve
HTTPS bölümü).

## Düzenli ifade tuzağı: match ile fullmatch

Biçim denetiminde düzenli ifadenin **bütün** metne uyması gerekir.
`re.match` yalnızca başına bakar; `$` işareti de sondaki bir satır sonunu
hoş görür:

```python
import re

for name in ["ada", "ada\n", "ada; x"]:
    loose = bool(re.match(r"^[a-z0-9_]{3,20}$", name))
    strict = bool(re.fullmatch(r"[a-z0-9_]{3,20}", name))
    print(f"{name!r:<10} match={loose!s:<5} fullmatch={strict}")
```

```text
'ada'      match=True  fullmatch=True
'ada\n'    match=True  fullmatch=False
'ada; x'   match=False fullmatch=False
```

`^...$` ile yazılmış ve "doğru" görünen desen, sonunda satır sonu olan
adı kabul etti. `re.fullmatch` metnin tamamını ister ve onu reddetti.
Doğrulamada `fullmatch` kullanılır. Düzenli ifadelerde bir başka tuzak da
iç içe tekrarlı desenlerin (`(a+)+` gibi) bazı girdilerde çok uzun
çalışmasıdır; bu bir hizmet engelleme açığına dönüşebilir. Desen basit,
girdinin uzunluğu sınırlı tutulur.

## Önce kanonik biçim

Aynı görünen iki metin bilgisayar için farklı olabilir: büyük/küçük harf,
sondaki boşluk, ya da Unicode'un "tam genişlikli" harfleri gibi başka
karakterlerle yazılmış biçimler. `admin` adı yasaklıysa ama karşılaştırma
ham metinle yapılıyorsa, aynı görünen başka bir yazım içeri sızar. Bu
yüzden metin önce **kanonik** (tek, standart) biçime çevrilir, sonra
doğrulanır ve karşılaştırılır:

```python
import unicodedata

for name in ["admin", "Admin", "ａｄｍｉｎ", "admin "]:
    canon = unicodedata.normalize("NFKC", name).strip().casefold()
    print(f"{name!r:<9} -> {canon!r:<8} {canon == 'admin'}")
```

```text
'admin'   -> 'admin'  True
'Admin'   -> 'admin'  True
'ａｄｍｉｎ'   -> 'admin'  True
'admin '  -> 'admin'  True
```

Dört farklı yazımın hepsi aynı kanonik biçime indi. `NFKC` Unicode'un
"uyumlu" karakterlerini sıradan karşılıklarına çevirir, `casefold` harf
büyüklüğünü kaldırır (Türkçedeki `İ`/`ı` gibi dile özgü durumları bilmez;
onlar ayrıca düşünülür).
Sıra önemlidir: **önce kanonik biçim, sonra doğrulama**; tersi yapılırsa
doğrulanan ile kullanılan metin farklı olur.

## Dosya yolları

Kullanıcının verdiği bir dosya adı bir klasöre eklenirken `..` (üst klasör)
ya da mutlak bir yol, sonucu klasörün **dışına** çıkarabilir. Buna **yol
geçişi** (path traversal) denir. Savunma: yolu birleştir, **normalleştir**
ve sonucun hâlâ izin verilen klasörün içinde olduğunu denetle:

```python
import posixpath

BASE = "/srv/app/uploads"


def safe_path(name):
    full = posixpath.normpath(posixpath.join(BASE, name))
    return full if full.startswith(BASE + "/") else None


for name in ["cat.png", "2026/cat.png", "../settings.ini", "/srv/app/settings.ini"]:
    print(f"{name:<22} {safe_path(name)}")
```

```text
cat.png                /srv/app/uploads/cat.png
2026/cat.png           /srv/app/uploads/2026/cat.png
../settings.ini        None
/srv/app/settings.ini  None
```

Alt klasördeki dosyaya izin verildi; üst klasöre çıkan ve mutlak yol
veren adlar reddedildi. Denetimdeki `BASE + "/"` önemlidir: yalnızca
`BASE` ile başlamak, `/srv/app/uploads-old` gibi komşu bir klasörü de
kabul ederdi. Daha da iyisi, kullanıcının dosya adını hiç kullanmamaktır:
dosya rastgele bir adla saklanır, kullanıcının verdiği ad yalnızca bir
etiket olarak veritabanında tutulur.

## Bir değer, birçok kodlama

Doğrulamadan geçen bir değer bile her yere aynı biçimde yazılamaz. Aynı
metnin üç farklı bağlamdaki kodlanmış hâli:

```python
import html
import json
from urllib.parse import quote

value = 'Tom & "Jerry" <3'
print(html.escape(value))
print(quote(value, safe=""))
print(json.dumps(value))
```

```text
Tom &amp; &quot;Jerry&quot; &lt;3
Tom%20%26%20%22Jerry%22%20%3C3
"Tom & \"Jerry\" <3"
```

HTML'de `&amp;` ve `&lt;`, adres parametresinde `%26` ve `%3C`, JSON'da
kaçışlı tırnak. Her bağlamın kendi kodlayıcısı vardır ve kodlama, veri o
bağlama **yazılırken** yapılır (XSS bölümündeki kural).

## Komut satırı

Kullanıcının verdiği bir değeri bir **kabuk komutuna** metin olarak
eklemek, SQL enjeksiyonunun komut satırındaki karşılığıdır. Kabukta `;`
gibi işaretler yeni bir komut başlatır. Aşağıda hiçbir komut çalışmıyor;
yalnızca kabuğun metni nasıl parçalara ayıracağı gösteriliyor:

```python
import shlex

name = "report.txt; echo hi"
print(shlex.split("wc -l " + name))
print(["wc", "-l", name])
print("wc -l " + shlex.quote(name))
```

```text
['wc', '-l', 'report.txt;', 'echo', 'hi']
['wc', '-l', 'report.txt; echo hi']
wc -l 'report.txt; echo hi'
```

Metin olarak birleştirilen komutta `;` ayrı bir parça oldu ve ardından
ikinci bir komut (`echo hi`) geldi. Argüman **listesi** biçiminde ise ad
tek bir argüman olarak kaldı; program kabuksuz çalıştırılırsa bu değer
hiçbir zaman komut olmaz. Kural SQL'deki gibidir: komut metinle
kurulmaz, argümanlar ayrı verilir; kabuk gerçekten gerekiyorsa her değer
`shlex.quote` ile kaçılır. En iyisi ise mümkünse dış komut çalıştırmak
yerine aynı işi yapan bir kütüphane fonksiyonu kullanmaktır.

## Özet

- **Girdi doğrulama** anlamı denetler, **çıktı kodlama** verinin kod
  olmasını engeller; biri ötekinin yerini tutmaz.
- Doğrulama **izin listesiyle** ve **sunucuda** yapılır: tür, biçim,
  uzunluk, aralık ya da küme; eksik alan da hatadır.
- Düzenli ifadede **`re.fullmatch`**; `re.match` ve `$` sondaki satır
  sonunu kaçırır. Desen basit, girdi uzunluğu sınırlı.
- Metin önce **kanonik biçime** (NFKC, `strip`, `casefold`) çevrilir, sonra
  doğrulanır.
- **Dosya yolu** normalleştirilir ve izin verilen klasörün içinde mi
  denetlenir; en iyisi kullanıcının adını dosya adı yapmamaktır.
- Her bağlamın kendi **kodlayıcısı**: HTML, URL, JSON.
- **Komut** metinle kurulmaz; argüman listesi, gerekirse `shlex.quote`.
