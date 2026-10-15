# Gizli Değerler ve Güvenlik

Hattımız şimdiye kadar yalnızca kendi içinde çalıştı: kodu çekti, test
etti, paketledi. Bir sonraki adım dışarıyla konuşmak: paketi bir depoya
yüklemek, bir sunucuya dağıtmak, bir servise rapor göndermek. Bunların
hepsi bir **şifre** ya da **anahtar** ister. Bu bölümde iki şeyi
görüyoruz: hattın bu anahtarları nasıl güvenle kullandığı ve hattın
kendisinin nasıl bir saldırı kapısına dönüşebildiği.

## Anahtar neden koda yazılmaz?

Bir servisin kullanıcıyı tanımak için verdiği gizli metne **API anahtarı**
(API key) denir. Anahtarı bilen, o servise sizin adınıza istek atabilir.
En kolay yol onu koda yazmaktır ve en tehlikelisi de budur:

- Depoyu gören herkes anahtarı görür. Açık bir depoda bu, bütün internet
  demek.
- Satırı sonradan silmek yetmez. Git eski commit'leri saklar; anahtar
  **geçmişte** durmaya devam eder.

İkinci maddeyi küçük bir modelle görelim. Bir dosyanın üç sürümünü liste
olarak tutuyoruz (her biri bir commit); anahtar ilk sürümde yazılmış,
ikincide silinmiş:

```python
import re

API_KEY = re.compile(r"apikey_[A-Za-z0-9]{20}")

history = [
    'URL = "https://api.example.com"\nKEY = "apikey_7Hq2Lm9Xc4Vb8Nz1Rt5W"\n',
    'URL = "https://api.example.com"\nKEY = os.environ["KEY"]\n',
    'URL = "https://api.example.com/v2"\nKEY = os.environ["KEY"]\n',
]

print("today:  ", bool(API_KEY.search(history[-1])))
for number, version in enumerate(history, start=1):
    if API_KEY.search(version):
        print("commit", number, "still has the key")
```

```text
today:   False
commit 1 still has the key
```

Bugünkü dosyada anahtar yok, ama birinci commit'e bakan onu bulur.
Gerçek araçlar (GitHub'ın gizli değer taraması gibi) tam olarak bunu
yapar: bilinen anahtar biçimlerini bütün geçmişte arar. Bu yüzden kural
şudur: **bir anahtar bir kez depoya girdiyse sızmış sayılır.** Silmek
değil, servisten **yenisini alıp eskisini iptal etmek** (rotation)
gerekir.

## GitHub'da gizli değer

Anahtarın yeri depo değil, GitHub'ın **gizli değer** (secret) kasasıdır:
deponun **Settings › Secrets and variables › Actions** sayfasında bir ad
ve değer girilir. Değer şifrelenip saklanır; bir kez kaydedildikten sonra
sayfada bile gösterilmez, yalnızca değiştirilebilir. Adlarda harf, rakam
ve alt çizgi olur; rakamla ya da `GITHUB_` ile başlayamaz.

İş akışında değere `${{ secrets.AD }}` ile ulaşılır. Değer en iyi bir
ortam değişkeni olarak (`env:`) yalnızca onu isteyen adıma verilir:

```yaml
name: Report

on:
  push:
    branches: [main]

jobs:
  report:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.13"
      - run: python send_report.py
        env:
          REPORT_API_KEY: ${{ secrets.REPORT_API_KEY }}
```

Python tarafında kod anahtarı ortamdan okur, kendisi hiçbir şey bilmez:
`os.environ["REPORT_API_KEY"]`. Aynı kod bilgisayarınızda kendi
anahtarınızla, hatta kasadaki anahtarla çalışır.

Gizli olmayan ayarlar (bir adres, bir bölge adı) için aynı sayfada
**değişken** (variable) vardır: `${{ vars.AD }}`. Değişken kayıtlarda
açıkça görünür; şifre ona konmaz.

## Kayıtta maskeleme

Bir adım gizli değeri yanlışlıkla yazdırırsa GitHub kayıtta onu `***`
ile değiştirir. Bu güzel bir emniyet kemeri, ama nasıl çalıştığını
bilmek gerekir: kayıttaki metinde değerin **birebir aynısını** arar.
Basitleştirilmiş bir modelle:

```python
import base64


def mask(line, secrets):
    for secret in secrets:
        line = line.replace(secret, "***")
    return line


secret = "s3cr3t-Token-42"
print(mask("Connecting with s3cr3t-Token-42", [secret]))

encoded = base64.b64encode(secret.encode()).decode()
print(mask("Header: " + encoded, [secret]))
```

```text
Connecting with ***
Header: czNjcjN0LVRva2VuLTQy
```

Değer birebir yazılınca gizlendi. Ama aynı değer base64'e çevrilince
(bir adım onu bir başlığa koymak için dönüştürmüş olabilir) artık başka
bir metin ve olduğu gibi kayda düştü. Base64 bir şifre değildir; kaydı
gören herkes onu geri çevirebilir. Buradan iki kural çıkar:

- Gizli değeri **yazdırmayın**, maskelemeye güvenip "nasılsa gizlenir"
  demeyin.
- Bir adım değerden yeni bir gizli değer türetiyorsa onu maskelenecekler
  listesine kendisi ekler: `echo "::add-mask::$TOKEN"`.

## Fork'tan gelen PR

Açık bir depoda herkes deponun kopyasını (fork) alıp PR açabilir. O PR'ın
kodu sizin hattınızda çalışır. Eğer gizli değerler ona verilseydi, kötü
niyetli biri iş akışına "anahtarı bir yere gönder" adımı ekleyip PR
açardı. Bu yüzden GitHub **fork'tan gelen PR'larda gizli değerleri
vermez**: `${{ secrets.AD }}` boş gelir. Yalnızca birazdan göreceğimiz
`GITHUB_TOKEN` gelir, o da yalnızca okuma yetkisiyle.

Bunun sonucu: gizli değer isteyen adımlar (dağıtım, yayın) PR'da değil,
`main`'e gönderimde ya da etiket gelince çalışır. PR'da yalnızca test ve
kontroller koşar.

## `GITHUB_TOKEN` ve izinler

Her çalışmaya GitHub kendiliğinden geçici bir anahtar verir:
`GITHUB_TOKEN`. Hat onunla depoya bir şey yazabilir (etiket, sürüm, PR
yorumu). Çalışma bitince geçerliliği biter. Ne yapabileceği **izinlerle**
(`permissions:`) belirlenir; varsayılan izinler deponun ayarına göre
geniş olabilir.

Güvenliğin temel ilkesi burada da geçerli: **en az yetki** (least
privilege). Her iş yalnızca gerçekten gerektiği kadar izin alır. Hatta
çalışan bir eylem ele geçirilirse zararı izinler kadardır.

```yaml
name: Release

on:
  push:
    tags: ["v*"]

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python -m pytest
  release:
    needs: test
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4
      - run: gh release create "$GITHUB_REF_NAME" --generate-notes
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

- En üstteki `permissions:` bütün işlerin varsayılanıdır: yalnızca okuma.
- `release` işi kendi `permissions:` bloğuyla bunu ezer: sürüm açmak için
  `contents: write` ister. `test` işi okumada kalır.
- `permissions:` yazılınca **listede olmayan bütün izinler kapanır**
  (`none`). İzin eklemek bilinçli bir iştir.

<figure class="fig anat">
  <div class="anat-row"><span><code>contents</code></span><span>Depodaki dosyalar, etiketler, sürümler.</span></div>
  <div class="anat-row"><span><code>pull-requests</code></span><span>PR'a yorum yazmak, etiket koymak.</span></div>
  <div class="anat-row"><span><code>packages</code></span><span>GitHub'ın paket ve imaj deposu.</span></div>
  <div class="anat-row"><span><code>id-token</code></span><span>Buluta şifresiz giriş için kısa ömürlü kimlik.</span></div>
</figure>

Her biri `read`, `write` ya da `none` alır.

## Eylemler başkasının kodudur

`uses: actions/checkout@v4` yazdığınızda başka bir deponun kodunu, sizin
izinlerinizle ve gizli değerlerinize erişebilen bir makinede
çalıştırırsınız. `@v4` bir **etikettir** ve etiket taşınabilir: eylemin
sahibi (ya da onun hesabını ele geçiren biri) `v4`'ü bambaşka bir
commit'e çevirebilir ve hattınız bir sonraki çalışmada o kodu çalıştırır.

Bunun iki önlemi var:

- Güvendiğiniz kaynaklardan eylem kullanın (GitHub'ın kendi `actions/`
  eylemleri, bilinen kuruluşlar).
- Kritik hatlarda eylemi etiketle değil, **commit kimliğiyle** sabitleyin:
  `actions/checkout@` ardından 40 karakterlik commit kimliği, satır
  sonunda yorum olarak hangi sürüm olduğu (`# v4`). Commit kimliği
  değiştirilemez. Güncellemeyi elle ya da Dependabot gibi bir araçla
  yaparsınız.

## Kod enjeksiyonu

`${{ ... }}` ifadeleri kabuk çalışmadan **önce** metnin içine yazılır.
İfadenin değeri bir PR başlığı, bir dal adı ya da bir yorum gibi
**dışarıdan gelen** bir metinse, onu yazan kişi komutun bir parçasını
yazmış olur. Bir PR başlığının komuta nasıl karıştığını görelim. Komutun
kaç parçaya ayrıldığını Python'un `shlex` modülüyle sayıyoruz (`;` kabukta
iki komutu ayırır):

```python
import shlex


def commands(line):
    tokens = list(shlex.shlex(line, posix=True, punctuation_chars=True))
    return tokens.count(";") + 1


unsafe = 'echo "PR title is ${{ github.event.pull_request.title }}"'
title = 'Fix typo"; echo leaked=$API_KEY; echo "'
rendered = unsafe.replace("${{ github.event.pull_request.title }}", title)
print(rendered)
print("commands:", commands(rendered))

safe = 'echo "PR title is $TITLE"'
print(safe)
print("commands:", commands(safe))
```

```text
echo "PR title is Fix typo"; echo leaked=$API_KEY; echo ""
commands: 3
echo "PR title is $TITLE"
commands: 1
```

Başlıktaki tırnak, `echo`'nun metnini kapattı ve ardından gelen her şey
ayrı bir komut oldu: PR'ı açan kişi hattınızda istediği komutu
çalıştırabilir. Güvenli yazımda başlık bir **ortam değişkenine** konur ve
komut yalnızca değişkenin adını içerir. Kabuk değişkenin değerini
yerleştirirken onu yeniden komut olarak okumaz; içinde ne olursa olsun
tek bir metindir:

```yaml
      - run: echo "PR title is $TITLE"
        env:
          TITLE: ${{ github.event.pull_request.title }}
```

Kural: dışarıdan gelen bir değer `run:` satırına `${{ }}` ile doğrudan
yazılmaz; önce `env:`'e konur.

## Sırada

Anahtarları güvenle tutmayı ve izinleri daraltmayı gördük. Onuncu bölümde
paketi bir sürüm numarasıyla yayınlıyoruz: etiket gelince çalışan,
`contents: write` izniyle sürüm açan ve gizli değerle paketi yükleyen
bir hat.

## Özet

- Anahtar koda yazılmaz; yazıldıysa silmek yetmez, git geçmişi saklar.
  Sızan anahtar iptal edilip yenisi alınır.
- Gizli değer deponun kasasında durur, `${{ secrets.AD }}` ile
  okunur ve `env:` ile yalnızca isteyen adıma verilir. Gizli olmayan
  ayar `${{ vars.AD }}`.
- Kayıtta maskeleme yalnızca birebir değeri gizler; dönüştürülmüş değer
  sızar. Gizli değer yazdırılmaz.
- Fork'tan gelen PR'larda gizli değer yoktur.
- `GITHUB_TOKEN` her çalışmanın geçici anahtarıdır; `permissions:` ile en
  az yetki verilir. Üstte okuma, gereken işte yazma.
- Eylem başkasının kodudur; kritik hatta commit kimliğiyle sabitlenir.
- Dışarıdan gelen metin `run:`'a doğrudan yazılmaz; `env:` üzerinden
  verilir.
