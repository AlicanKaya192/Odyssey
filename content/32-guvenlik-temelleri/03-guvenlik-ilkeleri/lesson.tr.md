# Güvenlik İlkeleri

Araçlar her yıl değişir; yeni diller, yeni bulut hizmetleri, yeni saldırı
türleri çıkar. Ama iyi korunan sistemlerin arkasındaki fikirler yarım
yüzyıldır neredeyse aynı. Bunların çoğu 1975'te yazılmış klasik bir
makalede listelenmişti ve bugün de güvenlik incelemelerinin ilk sorularıdır.
Bu bölüm o **güvenlik ilkelerini** (security principles) görüyor; her
birinin ne dediğini, neden işe yaradığını ve kodda nasıl göründüğünü.

## En az yetki

**En az yetki** (least privilege): her kullanıcı, her program ve her
hizmet işini yapmaya **yetecek kadar** yetkiyle çalışır, fazlasıyla değil.
Not girmek için yazılmış bir program öğrenci kayıtlarını silemez; rapor
okuyan bir çalışan raporları değiştiremez.

Neden işe yarar? Bir hesap ele geçirildiğinde ya da bir program hata
yaptığında zarar, o hesabın yetkisiyle sınırlı kalır. Her şeyi yapabilen tek
bir yönetici hesabı, tek bir hatada her şeyi kaybettirir. Bu ilkenin kendi
bölümü var (En Az Yetki ve Görev Ayrılığı).

## Varsayılan olarak reddet

**Güvenli varsayılan** (fail-safe defaults): erişim kararı **izin listesi**
(allowlist) üzerinden verilir. Açıkça izin verilmeyen her şey reddedilir.
Tersi, **engel listesidir** (blocklist): yasaklananlar yazılır, gerisi
serbest. Engel listesinin sorunu, aklına gelmeyeni yasaklayamamandır.

Bir dosya yükleme sayfasının uzantı denetimiyle görelim:

```python
blocked = {"exe", "bat"}
allowed = {"pdf", "png", "jpg"}
for name in ["report.pdf", "tool.exe", "script.ps1", "photo.png"]:
    ext = name.rsplit(".", 1)[-1]
    print(f"{name:<11}", "blocklist:", ext not in blocked, "allowlist:", ext in allowed)
```

```text
report.pdf  blocklist: True allowlist: True
tool.exe    blocklist: False allowlist: False
script.ps1  blocklist: True allowlist: False
photo.png   blocklist: True allowlist: True
```

`script.ps1` engel listesinden geçti, çünkü listeyi yazan kişi bu uzantıyı
düşünmemişti. İzin listesi onu kendiliğinden reddetti. İzin listesinde
unutulan bir şey ise yalnızca bir kullanıcının şikâyetine yol açar
("PNG yükleyemiyorum"); engel listesinde unutulan şey bir açığa.

Bununla akraba bir fikir **varsayılan olarak güvenli** (secure by default):
bir ürün kutudan çıktığı hâliyle güvenli olmalı. Kullanıcı hiçbir ayara
dokunmazsa hata ayıklama kapalı, parola zorunlu, şifreleme açık olmalıdır.

## Güvenli başarısızlık

Programlar hata verir: dosya bulunamaz, ağ kopar, beklenmeyen bir değer
gelir. **Güvenli başarısızlık** (fail securely), bir şey ters gittiğinde
sistemin **kapalı** kalmasıdır: emin olamıyorsan izin verme. Bir izin
denetiminin hata durumunda ne döndürdüğüne bak:

```python
def can_open_bad(user, acl):
    try:
        return acl[user] == "allow"
    except KeyError:
        return True


def can_open_good(user, acl):
    try:
        return acl[user] == "allow"
    except KeyError:
        return False


acl = {"ada": "allow", "alan": "deny"}
for user in ["ada", "alan", "mallory"]:
    print(user, can_open_bad(user, acl), can_open_good(user, acl))
```

```text
ada True True
alan False False
mallory True False
```

Listede hiç olmayan `mallory`, kötü sürümde içeri girdi. Hata "açık"
başarısız oldu (fail open). Kapılarda bunun tersi bazen istenir (yangında
kapılar kilitli kalmasın), ama veriye erişimde kural kapalı kalmaktır.

## Derinlemesine savunma

**Derinlemesine savunma** (defence in depth): tek bir önleme güvenme,
birbirinin arkasında **birden fazla katman** kur. Bir kale düşün: hendek,
sur, kapı, iç kale. Saldırgan birini aşsa da ötekiler onu durdurabilir.

Her katmanın aşılma olasılığı yazılırsa, katmanlar birbirinden bağımsız
olduğu sürece hepsini aşma olasılığı bunların çarpımıdır:

```python
layers = {"firewall": 0.3, "patching": 0.2, "mfa": 0.1}
chance = 1.0
for name, passes in layers.items():
    chance *= passes
    print(f"after {name:<9} {chance:.3f}")
```

```text
after firewall  0.300
after patching  0.060
after mfa       0.006
```

Tek başına her katman zayıf görünüyor (biri her üç saldırıdan birini
geçiriyor), ama üçü birlikte bin saldırıdan ancak altısını geçiriyor.
Önemli koşul **bağımsızlık**: üç katman da aynı parolaya dayanıyorsa o
parola çalınınca hepsi birden düşer ve çarpım hesabı geçersiz olur.
Katmanların farklı türden olması (teknik, idari, fiziksel) bu yüzden
önemlidir.

## Tam aracılık

**Tam aracılık** (complete mediation): her erişim **her seferinde**
denetlenir. Bir kez verilen izni hatırlayıp sonra hiç sormamak, izin geri
alındığında sorun çıkarır:

```python
permissions = {"ada": {"read", "write"}}
cached = set(permissions["ada"])
permissions["ada"].discard("write")
print("cached answer:", "write" in cached)
print("checked now:", "write" in permissions["ada"])
```

```text
cached answer: True
checked now: False
```

Ada'nın yazma yetkisi alındı, ama yetkiyi bir kez okuyup saklayan kod hâlâ
"yazabilir" diyor. İşten ayrılan birinin açık oturumu ya da süresi
dolmayan bir erişim jetonu tam olarak bu sorundur.

## Açık tasarım

**Açık tasarım** (open design): güvenlik, sistemin **nasıl çalıştığının
gizli kalmasına** dayanmamalı; yalnızca anahtarların gizli kalmasına
dayanmalı. Kilit tasarımı herkesçe bilinir, anahtar senin cebindedir. Bu
fikir kriptografide **Kerckhoffs ilkesi** olarak bilinir.

Tasarımı gizleyerek korunmaya **gizlilik yoluyla güvenlik** (security
through obscurity) denir ve tek başına zayıftır: kod sızar, eski bir
çalışan anlatır, biri programı inceler. Gizlemek ek bir katman olabilir,
ama asıl katman olamaz.

## Basitlik

**Basitlik** (economy of mechanism): güvenlik mekanizması olabildiğince
küçük ve basit olmalı. Her satır bir hata fırsatıdır ve karmaşık bir
sistemi incelemek zordur. Yüz satırlık bir izin denetimi bin satırlıktan
daha kolay doğrulanır.

## Görev ayrılığı

**Yetki ayrılığı** (separation of privilege): önemli bir iş tek bir
kişinin ya da tek bir koşulun eline bırakılmaz. Bankadaki kasa iki ayrı
anahtarla açılır; büyük bir ödemeyi bir kişi hazırlar, başka biri onaylar.
Tek bir hesabın ele geçirilmesi ya da tek bir kişinin kötü niyeti yetmez.
İki adımlı giriş (bir sonraki bölüm) aynı fikrin kimlik doğrulamadaki
hâlidir.

## Kullanılabilirlik

**Psikolojik kabul edilebilirlik** (psychological acceptability): güvenlik
önlemi insanların işini gereksiz yere zorlaştırmamalı. Zorlaştırırsa
insanlar onu atlatmanın yolunu bulur: parolayı ekrana yapıştırır, kapıyı
takozla açık tutar. İyi önlem, doğru davranışı en kolay davranış hâline
getirir.

## Özet

<figure class="fig anat">
  <div class="anat-row"><span>En az yetki</span><span>İşe yetecek kadar yetki, fazlası değil.</span></div>
  <div class="anat-row"><span>Varsayılan olarak reddet</span><span>İzin listesi; söylenmeyen her şey yasak.</span></div>
  <div class="anat-row"><span>Güvenli başarısızlık</span><span>Hata olunca kapalı kal.</span></div>
  <div class="anat-row"><span>Derinlemesine savunma</span><span>Birbirinden bağımsız birkaç katman.</span></div>
  <div class="anat-row"><span>Tam aracılık</span><span>Her erişimi her seferinde denetle.</span></div>
  <div class="anat-row"><span>Açık tasarım</span><span>Gizli olan anahtar, tasarım değil.</span></div>
  <div class="anat-row"><span>Basitlik</span><span>Küçük mekanizma, az hata.</span></div>
  <div class="anat-row"><span>Görev ayrılığı</span><span>Önemli iş için iki el.</span></div>
  <div class="anat-row"><span>Kullanılabilirlik</span><span>Doğru davranış en kolayı olsun.</span></div>
  <figcaption>Bir sistemi incelerken her ilkeyi tek tek sor: burada uygulanıyor mu?</figcaption>
</figure>
