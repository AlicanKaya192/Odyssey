# CI/CD Nedir

Bir programı yazmak işin yarısı. Öbür yarısı, yazdığın her değişikliğin
programı bozmadığından emin olmak ve programı kullanıcıya ulaştırmak. Bu
patikanın ilk modülü o ikinci yarıyı anlatıyor: her değişiklikte
kendiliğinden çalışan, kodu test eden, denetleyen, paketleyen ve
yayınlayan bir **hat** kurmak. Bu bölümde hattın ne olduğunu, neden
gerektiğini ve hangi parçalardan oluştuğunu görüyoruz; ilk iş akışı
dosyanı da yazıyorsun.

## "Bende çalışıyordu"

Üç kişilik bir ekip düşün. Herkes kendi bilgisayarında, kendi dalında
(Git patikasındaki **branch**) çalışıyor. İki hafta sonra işleri ana dalda
birleştiriyorlar ve şunlar oluyor:

- Ayşe'nin değiştirdiği fonksiyonu Mert'in kodu eski hâliyle çağırıyor.
  İkisi de kendi bilgisayarında testleri geçirmişti.
- Selin yeni bir paket kurmuş ama `requirements.txt`'e yazmayı unutmuş.
  Program yalnızca onun bilgisayarında çalışıyor.
- Sürüm çıkarmak için yazılması gereken on komut var. Biri bir adımı
  atlıyor ve kullanıcıya testi hiç çalıştırılmamış bir sürüm gidiyor.

Bu sorunların hiçbiri kötü programcılıktan gelmiyor. Hepsinin ortak
nedeni şu: **birleştirme seyrek, denetim elle ve herkesin bilgisayarı
farklı.** Hata ne kadar geç bulunursa o kadar pahalı oluyor, çünkü iki
hafta sonra "bunu hangi değişiklik bozdu" sorusunun cevabı yüzlerce
satırın içinde kayboluyor.

## Sürekli entegrasyon (CI)

**Entegrasyon** (integration), herkesin yaptığı değişikliği ortak koda
katmak, yani birleştirmek demek. **Sürekli entegrasyon** (continuous
integration, kısaca **CI**) bu işi seyrek ve büyük parçalar hâlinde
değil, sık ve küçük parçalar hâlinde yapmak demek. Ama CI'ı asıl CI yapan
şey ikinci yarısı: **her değişiklik geldiğinde kod kendiliğinden kurulur
ve test edilir.**

Yani CI iki alışkanlıktan oluşuyor:

1. Değişikliği küçük tut ve sık birleştir (günde birkaç kez).
2. Her birleştirmede bir makine kodu **temiz bir ortamda** sıfırdan kursun
   ve bütün testleri çalıştırsın. Sonuç birkaç dakika içinde gelsin.

"Temiz ortam" önemli: test, senin bilgisayarında değil, hiçbir şeyin
önceden kurulu olmadığı bir makinede çalışıyor. Selin'in unuttuğu paket
orada yok, test hemen düşüyor ve sorun daha birleştirme günü gelmeden
görünüyor.

## Sürekli teslim ve sürekli dağıtım (CD)

**CD** kısaltması iki farklı şeyin adı olarak kullanılıyor, o yüzden
ikisini ayıralım:

- **Sürekli teslim** (continuous delivery): testleri geçen her değişiklik
  kendiliğinden **yayına hazır bir pakete** dönüşür. Yayınlamak tek bir
  düğmeye basmak kadar kolaydır, ama düğmeye bir insan basar.
- **Sürekli dağıtım** (continuous deployment): düğme de yoktur. Testleri
  geçen her değişiklik kendiliğinden kullanıcıya ulaşır.

<figure class="fig versus">
  <div class="no"><h4>Elle yayın</h4>Adımlar bir belgede ya da birinin aklında. Biri atlanabilir. Sürüm seyrek ve büyük çıkar; bozulduğunda neyin bozduğunu bulmak zordur.</div>
  <div class="ok"><h4>CI/CD hattı</h4>Adımlar bir dosyada yazılı ve her seferinde aynı sırayla çalışır. Sürüm sık ve küçük çıkar; düşen adım hangi değişikliğin sorunlu olduğunu hemen söyler.</div>
  <figcaption>Fark kodun kendisinde değil, kodun yolculuğunda.</figcaption>
</figure>

Hangisini seçeceğin işin riskine bağlı. Bir web sitesi günde birkaç kez
kendiliğinden güncellenebilir; bir bankanın ödeme sistemi ya da
kullanıcının bilgisayarına kurulan bir program çoğu zaman bir insanın son
onayıyla yayınlanır. Odyssey'in kendisi ikinci türden: yeni bir sürüm
etiketi gönderilince bir iş akışı içeriği denetliyor, programı derliyor
ve kurulum dosyasını hazırlıyor, ama sürümü yayınlama kararını yine bir
insan veriyor. Bu sürekli teslim.

## Hat: aşamalar ve kapılar

Kodun yolculuğundaki adımların sıralı listesine **hat** (pipeline) denir.
Tipik bir Python projesinin hattı şöyle görünür:

<figure class="fig">
  <div class="flow">
    <span class="node">Kur</span>
    <span class="arrow">→</span>
    <span class="node">Denetle</span>
    <span class="arrow">→</span>
    <span class="node acc">Test et</span>
    <span class="arrow">→</span>
    <span class="node">Paketle</span>
    <span class="arrow">→</span>
    <span class="node">Yayınla</span>
  </div>
  <figcaption>Her aşama bir kapı: düşerse sonraki aşamalar çalışmaz.</figcaption>
</figure>

- **Kur:** kodu indir, Python'u ve bağımlılıkları kur.
- **Denetle:** kodun biçimine ve sık yapılan hatalara bak (kalite kapıları
  bölümünde).
- **Test et:** otomatik testleri çalıştır (bir sonraki bölüm).
- **Paketle:** kullanıcıya gidecek dosyayı üret.
- **Yayınla:** paketi kullanıcıya ulaştır.

Hattın en önemli kuralı: **bir aşama düşerse hat orada durur.** Testi
geçmeyen kod paketlenmez, paketlenmeyen kod yayınlanmaz. Buna **hızlı
düşmek** (fail fast) denir: sorunu olabildiğince erken ve ucuz yerde
yakalamak. Bu yüzden hızlı aşamalar (biçim denetimi birkaç saniye sürer)
yavaş olanların (uzun testler, derleme) önüne konur.

Bu kuralı Python'da küçük bir taklitle görelim. Her aşama bir fonksiyon;
`True` dönerse geçti, `False` dönerse düştü:

```python
def install():
    print("install: ok")
    return True


def lint():
    print("lint: ok")
    return True


def test():
    print("test: 1 of 12 tests failed")
    return False


def package():
    print("package: ok")
    return True


pipeline = [("install", install), ("lint", lint), ("test", test), ("package", package)]

passed = True
for name, stage in pipeline:
    if not stage():
        print("pipeline stopped at:", name)
        passed = False
        break
if passed:
    print("pipeline passed")
```

```text
install: ok
lint: ok
test: 1 of 12 tests failed
pipeline stopped at: test
```

`package` hiç çalışmadı: test düştüğü anda hat durdu. Gerçek bir CI
servisinde de olan bu. Ekranda düşen aşama kırmızıyla işaretlenir ve
değişikliği gönderen kişiye haber gider.

Bir hattın sonucu iki kelimeyle anılır: geçtiyse **yeşil** (green build),
düştüyse **kırmızı** (red build). Ekiplerin en önemli kuralı da buradan
çıkar: **ana dal kırmızıysa önce o düzeltilir**, üstüne yeni iş eklenmez.

## Hattı kim çalıştırıyor?

Hattı bir **CI servisi** çalıştırıyor. Bu patikada GitHub'ın servisi olan
**GitHub Actions**'ı kullanıyoruz, çünkü kodun zaten GitHub'da duruyor
(Git patikası) ve dünyada en çok kullanılanlardan biri. Fikirler başka
servislerde de aynı; yalnızca dosyanın yazımı değişiyor.

Birkaç terim:

- **İş akışı** (workflow): hattı tarif eden dosya. Deponun içinde,
  `.github/workflows/` klasöründe duran bir YAML dosyası (Docker
  patikasındaki `compose.yaml` ile aynı yazım dili).
- **Tetikleyici** (trigger): iş akışını başlatan olay. Örneğin "biri
  `push` yaptığında".
- **İş** (job): aynı makinede çalışan adımlar grubu.
- **Adım** (step): tek bir komut ya da hazır bir eylem.
- **Çalıştırıcı** (runner): işi çalıştıran makine. Her çalıştırmada
  sıfırdan açılan temiz bir sanal bilgisayar; iş bitince silinir.

## İlk iş akışı dosyası

En küçük işe yarar iş akışı şöyle bir şey:

```yaml
name: CI

on: push

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.13"
      - run: pip install -r requirements.txt
      - run: python -m pytest
```

Satır satır:

<figure class="fig anat">
  <div class="anat-row"><span><code>name: CI</code></span><span>İş akışının adı; GitHub'daki listede böyle görünür.</span></div>
  <div class="anat-row"><span><code>on: push</code></span><span>Tetikleyici: depoya her <code>push</code> yapıldığında çalış.</span></div>
  <div class="anat-row"><span><code>jobs:</code></span><span>İşlerin listesi. Burada tek iş var: <code>test</code>.</span></div>
  <div class="anat-row"><span><code>runs-on</code></span><span>İşin çalışacağı makine: Ubuntu Linux'un en son sürümü.</span></div>
  <div class="anat-row"><span><code>steps:</code></span><span>Sırayla çalışan adımlar. Her adım <code>-</code> ile başlar.</span></div>
  <div class="anat-row"><span><code>uses:</code></span><span>Hazır bir eylem kullan. <code>actions/checkout@v4</code> deponun kodunu makineye indirir; <code>@v4</code> eylemin sürümü.</span></div>
  <div class="anat-row"><span><code>with:</code></span><span>Eyleme verilen ayarlar: hangi Python sürümü kurulacak.</span></div>
  <div class="anat-row"><span><code>run:</code></span><span>Bir komut çalıştır, tıpkı terminalde yazar gibi.</span></div>
</figure>

Makine temiz olduğu için ilk adım her zaman kodu indirmek: çalıştırıcıda
deponun kodu kendiliğinden bulunmuyor. Bunu unutmak en sık yapılan
hatalardan biri; sonraki adımlar boş bir klasörde çalışır ve
`requirements.txt` bulunamaz.

Dosyanın her parçasını İş Akışı Dosyasının Anatomisi bölümünde tek tek
açacağız. Şimdilik yapıyı tanıman yeterli: **ne zaman** (`on`), **nerede**
(`runs-on`), **ne** (`steps`).

## Bu modülde nasıl çalışacağız

Odyssey çevrimdışı çalışıyor ve gerçek bir CI servisine bağlanmıyor. Bu
yüzden iki tür alıştırma var:

- **İş akışı alıştırmaları:** `.github/workflows/ci.yml` dosyasını
  yazıyorsun. Dosya çalıştırılmıyor; GitHub'ın kurallarına göre
  **denetleniyor**: yapı doğru mu (her işin `runs-on`'u var mı, eylemlerin
  sürümü yazılmış mı), istenen tetikleyici, adım ve sıra var mı. Denetim
  GitHub'ın reddedeceği hataları yakalar, ama dosyanın gerçek bir
  makinede ne yapacağını ölçemez. Gerçek denemeyi kendi deponda
  yapabilirsin: dosyayı GitHub'a gönderdiğin anda çalışır.
- **Python alıştırmaları:** testler ve hattın içinde çalışan kod
  gerçekten çalıştırılıyor; buradaki her sonuç ölçülmüş sonuç.

## Özet

- **CI:** değişiklikleri sık birleştir, her birleştirmede kod temiz bir
  makinede kendiliğinden kurulsun ve test edilsin.
- **Sürekli teslim:** testi geçen her değişiklik yayına hazır pakete
  dönüşür, yayını insan başlatır. **Sürekli dağıtım:** yayın da
  kendiliğinden.
- **Hat** aşamalardan oluşur; bir aşama düşerse hat durur. Hızlı aşamalar
  öne konur (hızlı düşmek).
- GitHub Actions'ta hat bir **iş akışı** dosyasıyla tarif edilir: `on`
  (ne zaman), `jobs` → `runs-on` (nerede), `steps` (ne).
