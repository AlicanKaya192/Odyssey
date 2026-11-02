# Sosyal Mühendislik

Şimdiye kadar konuştuğumuz önlemlerin hepsi bir kapıyı kilitliyordu:
parolalar, MFA, yetkiler. **Sosyal mühendislik** (social engineering)
kilidi kırmaya uğraşmaz; kapıyı açması için **içerideki birini ikna
eder**. Teknik açık yerine insanın güvenini, yardımseverliğini ya da
telaşını kullanır. Saldırı yüzeyinin insan tarafı budur.

Bu bölümün amacı bu saldırıları **tanımak ve durdurmak**. Başkalarına
sahte e-posta göndermek, izinsiz "deneme" bile olsa, hem etik değildir
hem de suçtur; kurumlar oltalama tatbikatını yalnızca yazılı izinle ve
çalışanları korumak için yapar.

## Neden işe yarar?

Sosyal mühendislik, insanların karar verirken kullandığı kısa yolları
kullanır. En sık görülen kaldıraçlar:

| Kaldıraç | Mesajda nasıl görünür? |
|---|---|
| **Otorite** (authority) | "Genel müdürden acil talimat" |
| **Aciliyet** (urgency) | "Hesabınız 1 saat içinde kapanacak" |
| **Korku** (fear) | "Hakkınızda şikâyet var, ekteki belgeye bakın" |
| **Merak** (curiosity) | "Maaş zammı listesi ekte" |
| **Yardımseverlik** (helpfulness) | "Sunumum açılmıyor, hemen bakabilir misin?" |
| **Sosyal kanıt** (social proof) | "Ekibin geri kalanı formu doldurdu" |
| **Kıtlık** (scarcity) | "Yalnızca ilk 50 kişiye" |

Hepsinin ortak noktası **düşünmeye zaman bırakmamak**. Bu yüzden en iyi
savunma da en basitidir: dur ve başka bir yoldan doğrula.

## Türleri

- **Oltalama** (phishing): toplu gönderilen sahte e-posta; amaç parola,
  kart bilgisi ya da zararlı bir eki açtırmak.
- **Hedefli oltalama** (spear phishing): tek bir kişiye ya da ekibe göre
  hazırlanmış, adını, işini, yöneticisini bilen mesaj. Daha az ama çok
  daha başarılı.
- **Balina avı** (whaling): üst yöneticileri hedefleyen hedefli oltalama.
- **SMS ile oltalama** (smishing) ve **telefonla oltalama** (vishing):
  aynı fikir, başka kanal. "Bankadan arıyoruz, telefonunuza gelen kodu
  okur musunuz?"
- **Bahane** (pretexting): inandırıcı bir hikâye kurmak. "Bilgi işlemden
  arıyorum, hesabınızı taşıyoruz."
- **İş e-postası dolandırıcılığı** (business email compromise): yönetici ya
  da tedarikçi gibi yazıp ödemeyi başka hesaba yönlendirmek. Çoğu zaman
  ekte zararlı bir şey yoktur, yalnızca yeni bir banka hesap numarası.
- **Yemleme** (baiting): üstünde "maaşlar" yazan bir USB belleği otoparka
  bırakmak.
- **Kuyruğa takılma** (tailgating): kartlı kapıdan, elleri kutu dolu
  biriyle birlikte içeri girmek.
- **Omuz sörfü** (shoulder surfing): parolayı yazarken arkadan bakmak.

## Bağlantı gerçekten nereye gidiyor?

Oltalama e-postalarının çoğu bir bağlantıya tıklatmaya çalışır. Bağlantının
**görünen metni** ile **gittiği adres** farklı olabilir ve adres de
yanıltıcı yazılmış olabilir. Bir adresin gerçekten hangi sunucuya gittiğini
`urllib.parse.urlsplit` söyler:

```python
from urllib.parse import urlsplit


def real_host(url):
    return urlsplit(url).hostname or ""


def belongs_to(url, domain):
    host = real_host(url)
    return host == domain or host.endswith("." + domain)


urls = ["https://login.school.example/reset",
        "https://school.example.account-check.test/login",
        "https://school-example.test/login",
        "https://school.example@evil.test/login"]
for url in urls:
    print(f"{real_host(url):<34}", belongs_to(url, "school.example"))
```

```text
login.school.example               True
school.example.account-check.test  False
school-example.test                False
evil.test                          False
```

Dört adresin dördünde de `school.example` yazıyor, ama yalnızca birincisi
okulun sunucusuna gidiyor:

- İkincide `school.example` yalnızca bir **alt alan adı** (subdomain);
  asıl alan adı sondaki `account-check.test`. Adres **sağdan sola** okunur.
- Üçüncüde nokta yerine tire var; tamamen başka bir alan adı.
- Dördüncüde `@` işaretinden önceki kısım kullanıcı adı sayılır; gidilen
  sunucu `evil.test`.

`belongs_to`'nun `"." + domain` ile bitip bitmediğine bakması önemli:
yalnızca `endswith(domain)` yazsaydık `notschool.example` da okulunmuş gibi
görünürdü.

Bunlara bir de **benzer görünen alan adları** (lookalike domains) eklenir:
`examp1e` (l yerine 1), `rn` ile yazılmış bir `m`, ya da başka alfabeden
aynı görünen harfler. Göz bunları kolayca kaçırır; bu yüzden bağlantıya
tıklamak yerine adresi kendin yazmak ya da yer imini kullanmak daha
güvenlidir.

## Uyarı işaretleri

Tek bir işaret bir e-postayı sahte yapmaz, ama işaretler birikince durup
doğrulamak gerekir. Kurumlar bazen bunu basit bir puanla öğretir:

```python
SIGNS = {"urgent": 2, "asks_password": 3, "link_mismatch": 3,
         "unknown_sender": 1, "attachment": 1}
mail = {"urgent": True, "asks_password": True, "link_mismatch": True,
        "unknown_sender": False, "attachment": False}
score = sum(points for sign, points in SIGNS.items() if mail[sign])
print("score:", score, "-> report it" if score >= 4 else "-> probably fine")
```

```text
score: 8 -> report it
```

Bu puan bir öğretme aracıdır, bir filtre değil: hedefli bir mesajda
işaretlerin hiçbiri olmayabilir. Gerçek kural şu: **parola, kod, ödeme ya
da hesap bilgisi değişikliği isteyen her mesaj başka bir kanaldan
doğrulanır.**

## Savunma

Sosyal mühendisliğe karşı tek bir önlem yetmez; derinlemesine savunma
burada da geçerli:

- **İnsan:** düzenli ve kısa eğitim, gerçek örneklerle. Hata yapanı
  suçlamayan bir kültür: tıkladığını hemen bildiren kişi en değerli
  uyarıyı vermiştir.
- **Süreç:** banka hesabı değişikliği gibi işler, kayıtlı numaradan geri
  aranarak doğrulanır (mesajdaki numaradan değil). Yardım masası parola
  sıfırlamadan önce kimliği doğrular.
- **Teknik:** e-posta filtreleri; gönderenin alan adını doğrulayan e-posta
  kimlik doğrulama kayıtları (SPF, DKIM, DMARC); dışarıdan gelen e-postaya
  "dış gönderen" etiketi; oltalamaya dayanıklı MFA (çalınan parola tek
  başına işe yaramasın).
- **Bildirim:** tek tıkla "oltalama bildir" düğmesi. Bir kişinin bildirdiği
  mesaj, herkesin kutusundan silinebilir.

## Özet

- Sosyal mühendislik kilidi değil insanı hedef alır; otorite, aciliyet,
  korku, merak gibi kaldıraçlarla düşünmeye zaman bırakmaz.
- Türleri: oltalama, hedefli oltalama, balina avı, smishing, vishing,
  bahane, iş e-postası dolandırıcılığı, yemleme, kuyruğa takılma, omuz
  sörfü.
- Bir adres sağdan sola okunur; gerçek sunucuyu `urlsplit(...).hostname`
  söyler. Alan adına ait olmayı `== domain` ya da `endswith("." + domain)`
  ile denetle.
- Kural: hassas bir istek her zaman başka bir kanaldan doğrulanır.
- Savunma insan, süreç ve teknik önlemlerin birlikte çalışmasıdır; hata
  bildirmek ödüllendirilir.
