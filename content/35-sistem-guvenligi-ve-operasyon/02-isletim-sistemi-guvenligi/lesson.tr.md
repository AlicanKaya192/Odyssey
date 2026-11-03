# İşletim Sistemi Güvenliği

İşletim sistemi bilgisayardaki her şeyin hakemidir: hangi programın hangi
dosyayı açabileceğine, hangi belleğe dokunabileceğine, ağa çıkıp
çıkamayacağına o karar verir. Bir saldırgan için işletim sistemini ele
geçirmek her şeyi ele geçirmek demektir; savunan için de işletim sistemini
doğru kurmak, üzerindeki her programı korumak demektir.

Bu bölüm işletim sisteminin güvenliği nasıl sağladığını ve bir sistemi
nasıl **sıkılaştırdığımızı** (hardening) anlatıyor. Kodlar yine oyuncak
modeller: gerçek sistem ayarlarına dokunmuyor, yalnızca sözlüklerle aynı
mantığı kuruyor.

## Çekirdek ve kullanıcı kipi

İşlemci iki kipte çalışır. **Çekirdek kipi** (kernel mode) her şeye
erişebilir: tüm bellek, tüm donanım. **Kullanıcı kipi** (user mode) ise
kısıtlıdır. Uygulamalar (tarayıcı, oyun, senin Python programın) kullanıcı
kipinde çalışır ve bir dosyayı açmak gibi ayrıcalıklı bir iş için
çekirdekten **istekte bulunur**. Bu isteğe **sistem çağrısı** (system call)
denir. Çekirdek her isteği denetler ve izin verir ya da reddeder.

<figure class="fig"><div class="versus">
  <div><h4>Kullanıcı kipi</h4>Uygulamalar burada çalışır. Donanıma ve başka programların belleğine doğrudan erişemez; her ayrıcalıklı iş için <b>sistem çağrısı</b> yapar.</div>
  <div><h4>Çekirdek kipi</h4>İşletim sisteminin çekirdeği burada çalışır. Her şeye erişir ve her sistem çağrısını <b>denetler</b>: kim istiyor, buna izni var mı?</div>
</div><figcaption>Sınır, kullanıcı kipindeki bir hatanın bütün sistemi ele geçirmesini engeller.</figcaption></figure>

Bu ayrımı küçük bir modelle görelim. Her rolün yapabileceği işlemler bir
kümede; "çekirdek" isteği kümeye bakarak karşılıyor:

```python
POLICY = {
    "user": {"read_own_file", "open_window"},
    "admin": {"read_own_file", "open_window", "install_driver", "change_time"},
}


def syscall(role, operation):
    if operation in POLICY.get(role, set()):
        return "allowed"
    return "denied"


print(syscall("user", "open_window"))
print(syscall("user", "install_driver"))
print(syscall("admin", "install_driver"))
print(syscall("guest", "open_window"))
```

```text
allowed
denied
allowed
denied
```

Sıradan kullanıcı pencere açabildi ama sürücü kuramadı; yönetici
kurabildi. Politikada hiç olmayan `guest` rolü hiçbir şey yapamadı: listede
olmayan **reddedilir**. Bu, Güvenlik İlkeleri bölümündeki **varsayılan
olarak reddet** (default deny) ilkesinin işletim sistemindeki karşılığıdır.

## Süreç yalıtımı

Çalışan her programa **süreç** (process) denir. İşletim sistemi her
sürece kendi bellek alanını verir ve bir sürecin ötekinin belleğini
okumasını engeller. Tarayıcıdaki oturum çerezi, aynı anda açık bir oyunun
erişemeyeceği bir yerde durur:

```python
memory = {
    "browser": {"cookie": "abc123"},
    "game": {"score": 4200},
}


def read(process, owner, key):
    if process != owner:
        return "access denied"
    return memory[owner][key]


print(read("browser", "browser", "cookie"))
print(read("game", "browser", "cookie"))
```

```text
abc123
access denied
```

Tarayıcı kendi çerezini okudu; oyunun aynı isteği reddedildi. Gerçek
sistemlerde bu denetimi donanım (bellek yönetim birimi) ve çekirdek birlikte
yapar. Yalıtım sayesinde bir programdaki hata ya da zararlı bir eklenti,
öteki programların verisine kendiliğinden ulaşamaz. Tarayıcıların her
sekmeyi ayrı bir süreçte çalıştırması (**kum havuzu**, sandbox) bu fikrin
bir adım ötesidir.

## Hesaplar ve en az yetki

İşletim sistemindeki her süreç bir **hesap** adına çalışır ve o hesabın
yetkilerini taşır. Yönetici hesabıyla (Linux'ta `root`, Windows'ta
Administrator) çalışan bir program her şeyi yapabilir; aynı programdaki
bir hata da her şeyi yapabilir. Bu yüzden:

- Günlük iş **standart** bir hesapla yapılır; yönetici yetkisi yalnızca
  gerektiği an ve gerektiği iş için istenir (Linux'ta `sudo`, Windows'ta
  Kullanıcı Hesabı Denetimi onayı).
- Hizmetler kendi kısıtlı hesaplarıyla çalışır, yönetici olarak değil.
- Kullanılmayan hesaplar (misafir hesabı, eski çalışanların hesapları)
  kapatılır.

Bu, En Az Yetki ve Görev Ayrılığı bölümündeki ilkenin işletim sistemine
uygulanmasıdır.

## Güncellemeler: sürüm karşılaştırma tuzağı

Bilinen açıkların çoğu, düzeltmesi zaten yayınlanmış ama **yüklenmemiş**
sistemlerde kullanılır. Güncelleme denetimi bu yüzden temel bir güvenlik
işidir. Bunu yapan bir betik, kurulu sürümü açığın düzeltildiği sürümle
karşılaştırır. Ama sürümleri metin olarak karşılaştırmak yanlış sonuç
verir:

```python
print("2.4.10" < "2.4.9")


def version(text):
    return tuple(int(part) for part in text.split("."))


print(version("2.4.10") < version("2.4.9"))
print(version("2.4.10"))
```

```text
True
False
(2, 4, 10)
```

Metin karşılaştırması karakter karakter yapılır ve `"1"` `"9"`'dan önce
geldiği için `2.4.10` `2.4.9`'dan küçük sanılır. Bu hatayla yazılmış bir
denetim, `2.4.10` kurulu bir sistemi "eski" sanabilir ya da daha kötüsü,
eski bir sürümü "güncel" sayabilir. Doğrusu sürümü sayılardan oluşan bir
demete çevirmektir: demetler sayı sayı karşılaştırılır ve `10 > 9` olur.

## Sistemi sıkılaştırmak

**Sıkılaştırma** (hardening), bir sistemin varsayılan kurulumunu daha
güvenli hâle getirmektir: gereksiz olanı kapatmak, gerekli korumaları
açmak. Bunu her bilgisayarda elle yapmak yerine kurallar bir listeye
yazılır ve sistemin yapılandırması o listeye göre denetlenir:

```python
CONFIG = {
    "auto_update": False,
    "firewall": True,
    "guest_account": True,
    "admin_daily_use": True,
    "disk_encryption": False,
}
RULES = [
    ("auto_update", True, "turn on automatic updates"),
    ("firewall", True, "turn on the firewall"),
    ("guest_account", False, "disable the guest account"),
    ("admin_daily_use", False, "use a standard account daily"),
    ("disk_encryption", True, "encrypt the disk"),
]
for key, wanted, advice in RULES:
    if CONFIG.get(key) != wanted:
        print("-", advice)
```

```text
- turn on automatic updates
- disable the guest account
- use a standard account daily
- encrypt the disk
```

Beş kuraldan 4 tanesi tutmadı; yalnızca güvenlik duvarı
istendiği gibi. Kurumlarda bu listeler **güvenlik taban çizgisi**
(security baseline) olarak yazılır ve her bilgisayar düzenli aralıklarla
bunlara göre denetlenir.

| Sıkılaştırma adımı | Neden? |
|---|---|
| Otomatik güncellemeleri aç | Bilinen açıklar kapanır |
| Kullanılmayan hizmetleri kapat | Saldırı yüzeyi küçülür |
| Misafir ve eski hesapları kapat | Kimsenin izlemediği giriş kapısı kalmaz |
| Günlük işi standart hesapla yap | Bir hata yönetici yetkisi kazanmaz |
| Diski şifrele | Çalınan cihazdaki veri okunamaz |
| Güvenlik duvarını aç | Gereksiz bağlantılar engellenir |

Gereksiz her hizmet, Saldırı Yüzeyi bölümünde gördüğümüz gibi fazladan bir
kapıdır: kullanılmıyorsa da açıkları vardır ve güncellenmesi unutulur.

## Özet

- İşletim sistemi **hakemdir**: uygulamalar kullanıcı kipinde çalışır,
  ayrıcalıklı işler için **sistem çağrısı** yapar, çekirdek denetler.
- Politikada olmayan **reddedilir** (varsayılan olarak reddet).
- **Süreç yalıtımı:** her süreç kendi belleğini görür; bir programın hatası
  ötekinin verisine ulaşmaz.
- Günlük iş **standart hesapla**; yönetici yetkisi yalnızca gerektiğinde.
- Sürümler metin olarak değil **sayı demeti** olarak karşılaştırılır.
- **Sıkılaştırma:** gereksizi kapat, korumaları aç, yapılandırmayı bir
  taban çizgisine göre düzenli denetle.
