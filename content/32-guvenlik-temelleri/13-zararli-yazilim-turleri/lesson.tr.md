# Zararlı Yazılım Türleri

**Zararlı yazılım** (malware, malicious software), sahibinin isteği
dışında bir bilgisayara zarar vermek, onu kontrol etmek ya da ondan bilgi
çalmak için yazılmış programdır. Bu bölüm türleri **tanımayı**, nasıl
girdiklerini ve onlara karşı nasıl savunulduğunu anlatıyor. Zararlı kod
yazmıyoruz ve incelemiyoruz; buradaki bütün örnekler savunma tarafının
küçük araçlarıdır ve zararsız metinler üzerinde çalışır.

## Türler

Zararlı yazılımlar **nasıl yayıldıklarına** ve **ne yaptıklarına** göre
adlandırılır. Bir program birden fazla türün özelliğini taşıyabilir.

| Tür | Nasıl yayılır / ne yapar? |
|---|---|
| **Virüs** (virus) | Başka bir dosyaya ya da programa eklenir; o dosya çalıştırılınca çalışır ve kendini başka dosyalara kopyalar. Kullanıcının bir şeyi açmasına ihtiyaç duyar. |
| **Solucan** (worm) | Kimsenin bir şey açmasını beklemeden, ağdaki açıkları kullanarak bilgisayardan bilgisayara **kendi kendine** yayılır. |
| **Truva atı** (trojan) | Yararlı bir program gibi görünür (ücretsiz oyun, "sürücü güncelleyici"); kullanıcı kendisi kurar, arkada başka iş yapar. Kendi kendine yayılmaz. |
| **Fidye yazılımı** (ransomware) | Dosyaları şifreler ve açmak için para ister; çoğu zaman bir kopyasını da çalıp yayımlamakla tehdit eder. |
| **Casus yazılım** (spyware) | Gizlice bilgi toplar: gezilen siteler, belgeler, konum. |
| **Tuş kaydedici** (keylogger) | Basılan tuşları kaydeder; parolaları ele geçirmek için. |
| **Reklam yazılımı** (adware) | İstenmeyen reklam gösterir; çoğu zaman başka programlarla birlikte gelir. |
| **Rootkit** | Varlığını işletim sisteminden ve güvenlik araçlarından **gizlemek** için derinlere yerleşir. |
| **Arka kapı** (backdoor) | Saldırganın normal kimlik doğrulamayı atlayıp sonradan geri gelebilmesi için bırakılmış gizli yol. |
| **Bot ve bot ağı** (bot, botnet) | Uzaktan komut alan ele geçirilmiş bilgisayar; binlercesi birlikte hizmet engelleme ya da istenmeyen e-posta için kullanılır. |
| **Kripto madencisi** (cryptojacking) | Bilgisayarın işlemcisini sahibinin haberi olmadan kripto para üretmek için kullanır. |
| **Dosyasız zararlı** (fileless malware) | Diske dosya bırakmadan, sistemde zaten bulunan araçlar üzerinden bellekte çalışır; bu yüzden dosya taraması onu görmez. |

Virüs ile solucan arasındaki fark sınavlarda sık sorulur: **virüs bir
taşıyıcıya ve bir kullanıcıya**, **solucan ikisine de ihtiyaç duymaz**.
Truva atı ise yayılma değil **aldatma** yoluyla girer.

## Nasıl girerler?

- **E-posta ekleri ve bağlantıları** (Sosyal Mühendislik bölümü).
- **Sahte indirmeler:** "ücretsiz" sürümler, sahte güncelleme uyarıları.
- **Yamalanmamış açıklar:** solucanlar ve otomatik saldırılar bunlarla
  yayılır (Tehdit, Açık ve Risk bölümündeki eski CVE'ler).
- **Taşınabilir bellekler:** USB, harici diskler.
- **Tedarik zinciri** (supply chain): güvendiğin bir programın ya da
  kütüphanenin kendisi ele geçirilir; güncellemeyle birlikte zararlı kod da
  gelir. Sistem Güvenliği modülünde ayrıntısıyla.
- **Zayıf ya da çalınmış parolalarla** uzaktan erişim hizmetleri.

## Nasıl tespit edilir?

İki temel yaklaşım var.

**İmza tabanlı tespit** (signature-based detection): bilinen zararlı
dosyaların özetleri (hash) bir listede tutulur; taranan dosyanın özeti
listede varsa yakalanır. Hızlı ve yanılgısı azdır. Zayıflığı şu:

```python
import hashlib


def sha(data):
    return hashlib.sha256(data).hexdigest()


known_bad = {sha(b"TOY-SAMPLE-A"), sha(b"TOY-SAMPLE-B")}
files = {"report.pdf": b"quarterly numbers",
         "tool.exe": b"TOY-SAMPLE-A",
         "tool2.exe": b"TOY-SAMPLE-A!"}
for name, data in files.items():
    print(name, "match" if sha(data) in known_bad else "no match")
```

```text
report.pdf no match
tool.exe match
tool2.exe no match
```

Buradaki "dosyalar" yalnızca zararsız metinler. `tool2.exe`, bilinen
örnekten **tek bir bayt** farklı; özeti tamamen değiştiği için imza listesi
onu tanımadı. Gerçek zararlı yazılımlar da her bulaşmada kendini biraz
değiştirerek imzadan kaçar. İmza listesi yeni çıkan bir türü de hiç
tanımaz.

**Davranış tabanlı tespit** (behaviour-based detection): dosyanın
kendisine değil **ne yaptığına** bakılır. Fidye yazılımı, kısa sürede çok
sayıda dosyayı okuyup şifrelenmiş hâlleriyle değiştirir; yedekleme
programı da çok dosya yazar ama uzantıları değiştirmez:

```python
events = {"backup.exe": {"files_written": 4000, "extensions_changed": 0},
          "unknown.exe": {"files_written": 3800, "extensions_changed": 3700},
          "editor.exe": {"files_written": 12, "extensions_changed": 0}}
for name, e in events.items():
    ratio = e["extensions_changed"] / e["files_written"]
    alarm = e["files_written"] > 1000 and ratio > 0.5
    print(f"{name:<12} {ratio:.2f}", "suspicious" if alarm else "ok")
```

```text
backup.exe   0.00 ok
unknown.exe  0.97 suspicious
editor.exe   0.00 ok
```

Davranış tespiti yeni türleri de yakalayabilir, ama **yanlış alarm**
(false positive) üretmeye daha yatkındır: dosyalarının uzantısını toplu
değiştiren meşru bir program da işaretlenebilir. Gerçek araçlar iki
yaklaşımı birlikte kullanır.

Bir saldırının izine **tehlike göstergesi** (indicator of compromise, IOC)
denir: bilinen zararlı bir dosyanın özeti, bağlantı kurulan şüpheli bir
alan adı, beklenmeyen bir hizmet. Olay müdahalesinde kayıtlar bu
göstergelere göre taranır (Sistem Güvenliği modülü).

## Savunma

Zararlı yazılıma karşı tek bir ürün yetmez; önceki bölümlerdeki ilkelerin
hepsi burada birleşir:

- **Güncelleme:** yamalanmış bir açık, ondan yayılan solucanı durdurur.
- **En az yetki:** yönetici olmayan bir hesapla açılan zararlı yazılım
  sistemin derinlerine yerleşemez.
- **Uygulama izin listesi** (application allowlisting): yalnızca onaylı
  programların çalışmasına izin vermek; varsayılan olarak reddet.
- **E-posta ve web süzgeçleri**, kullanıcı eğitimi.
- **Ağ bölümleme:** bir bilgisayara giren solucan bütün ağa yayılamasın.
- **Yedek:** fidye yazılımının en güçlü cevabı.

## 3-2-1 yedek kuralı

Fidye yazılımı yalnızca dosyaları değil, ulaşabildiği **yedekleri** de
şifrelemeye çalışır. Bu yüzden yedeğin nasıl tutulduğu en az varlığı kadar
önemlidir. Yaygın kural **3-2-1**: verinin en az **3** kopyası (asıl veri
dahil), en az **2** farklı ortamda, en az **1** tanesi başka bir yerde.
Bugün buna bir şart daha eklenir: en az bir kopya **bağlantısız** ya da
**değiştirilemez** olmalı, ki ağdaki zararlı yazılım ona ulaşamasın.

```python
copies = [{"media": "laptop", "offsite": False, "offline": False},
          {"media": "usb-disk", "offsite": False, "offline": True},
          {"media": "cloud", "offsite": True, "offline": False}]
print("3 copies:", len(copies) >= 3)
print("2 media:", len({c["media"] for c in copies}) >= 2)
print("1 offsite:", any(c["offsite"] for c in copies))
print("1 offline:", any(c["offline"] for c in copies))
```

```text
3 copies: True
2 media: True
1 offsite: True
1 offline: True
```

Yedeğin bir de **denenmiş** olması gerekir: hiç geri yüklenmemiş bir yedeğin
çalıştığı ancak felaket günü anlaşılır, ki bu çok geçtir.

## Fidye istenirse

Kurumların çoğu fidye ödememeyi önerir: ödemek dosyaların geri geleceğini
garanti etmez, saldırganı yeniden saldırmaya teşvik eder ve bazı ülkelerde
hukuki sorun doğurur. Doğru sıra: etkilenen bilgisayarları ağdan ayır,
olay müdahale planını başlat, temiz yedekten geri yükle, nasıl girildiğini
bul ve o kapıyı kapat.

## Özet

- Zararlı yazılım türleri yayılma ve davranışa göre adlandırılır: virüs
  taşıyıcı ister, solucan kendi kendine yayılır, truva atı aldatır, fidye
  yazılımı şifreler, rootkit gizlenir.
- Giriş yolları: e-posta, sahte indirme, yamalanmamış açık, USB, tedarik
  zinciri, zayıf uzaktan erişim.
- **İmza tabanlı** tespit hızlı ama tek bayt farkla kandırılır; **davranış
  tabanlı** tespit yeniyi yakalar ama yanlış alarm verebilir.
- Savunma: güncelleme, en az yetki, izin listesi, süzgeç, eğitim, ağ
  bölümleme, yedek.
- Yedekte **3-2-1** ve en az bir bağlantısız kopya; yedek düzenli olarak
  geri yüklenip denenir.
