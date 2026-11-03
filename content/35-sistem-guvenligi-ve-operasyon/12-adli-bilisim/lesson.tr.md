# Adli Bilişim Temelleri

Olay Müdahalesi bölümünde sınırlama yaparken bir kural koyduk: makine
kapatılmaz, silinmez; üzerindeki iz korunur. O izlerin incelenmesine
**adli bilişim** (digital forensics) denir: dijital kanıtı toplamak,
korumak, incelemek ve bulguları başkalarının da doğrulayabileceği biçimde
raporlamak.

Adli bilişimin ilk kuralı tekniğe değil güvenilirliğe dairdir: bir kanıt,
toplandığı andan rapora kadar **değişmediği kanıtlanabiliyorsa**
değerlidir. Bu bölümdeki bütün "kanıtlar" sahte: birkaç baytlık metinler,
uydurma dosya kayıtları. Gerçek bir diske ya da sisteme dokunan kod yok.

## Kanıtın özeti

Kanıt toplanınca hemen **özeti** alınır ve kayda geçer (Özet Fonksiyonları
bölümü). İnceleme kanıtın kendisi üzerinde değil, bir **kopyası** üzerinde
yapılır; ileride biri "kanıt değişti mi?" diye sorarsa özet yeniden
hesaplanır:

```python
import hashlib

evidence = b"disk image of pc-bob (toy)"
recorded = hashlib.sha256(evidence).hexdigest()
print(recorded[:16])

copy = bytes(evidence)
print(hashlib.sha256(copy).hexdigest() == recorded)
changed = evidence.replace(b"bob", b"eve")
print(hashlib.sha256(changed).hexdigest() == recorded)
```

```text
1f27ccdc5b39f4f7
True
False
```

Kopyanın özeti kayıtla aynı: inceleme kopyada yapılabilir. Tek bir kelime
değişince özet tutmadı. Gerçek incelemelerde disk, kopyalanırken ona hiçbir
şey yazılmasını engelleyen bir **yazma engelleyici** (write blocker)
üzerinden okunur.

## Gözetim zinciri

Kanıtın kimin elinde, ne zaman, ne için bulunduğu kesintisiz bir kayıtla
belgelenir; buna **gözetim zinciri** (chain of custody) denir. Her teslimde
veren ve alan yazılır; bir halka eksikse "o arada kanıta ne oldu?"
sorusunun cevabı yoktur:

```python
CUSTODY = [
    ("2026-11-01 02:40", "responder-ada", "lab-locker", "collected, sha256 recorded"),
    ("2026-11-01 09:15", "lab-locker", "analyst-eve", "copy made for analysis"),
    ("2026-11-02 17:00", "analyst-joe", "lab-locker", "returned"),
]
holder = CUSTODY[0][1]
for when, giver, taker, note in CUSTODY:
    if giver != holder:
        print("gap before", when, ": expected", holder, "but got", giver)
    holder = taker
print("last holder:", holder)
```

```text
gap before 2026-11-02 17:00 : expected analyst-eve but got analyst-joe
last holder: lab-locker
```

Kanıt `analyst-eve`'ye verilmiş ama geri getiren `analyst-joe`. Arada
kanıtın el değiştirdiğine dair kayıt yok; bu boşluk, mahkemede ya da bir
iç soruşturmada bulguların değerini düşürebilir.

## Toplama sırası: uçuculuk

Bazı izler çok çabuk kaybolur. Bilgisayar kapanınca bellekteki her şey
silinir; disk kalır, yedekler daha da uzun kalır. Kanıt bu yüzden **en
uçucudan en kalıcıya** doğru toplanır:

```python
SOURCES = [
    ("backup tapes", 5),
    ("memory (RAM)", 1),
    ("disk", 4),
    ("network connections", 2),
    ("running processes", 2),
    ("temporary files", 3),
]
for name, volatility in sorted(SOURCES, key=lambda s: (s[1], s[0])):
    print(volatility, name)
```

```text
1 memory (RAM)
2 network connections
2 running processes
3 temporary files
4 disk
5 backup tapes
```

Bellek ve açık bağlantılar ilk sırada: makineyi kapatmak tam da bunları
yok eder. Olay Müdahalesi bölümündeki "kapatma, ağdan ayır" kuralının
nedeni budur.

## Dosya ne diyor, içi ne diyor?

Bir dosyanın uzantısı yalnızca adının parçasıdır ve kolayca
değiştirilebilir. Dosyanın **gerçek türü** ilk baytlarından anlaşılır;
bunlara **dosya imzası** ya da **sihirli sayılar** (magic bytes) denir.
Uzantısı türüyle uyuşmayan dosya incelemede dikkat çeker:

```python
SIGNATURES = {b"%PDF": "pdf", b"\x89PNG": "png", b"PK\x03\x04": "zip"}
FILES = {
    "report.pdf": b"%PDF-1.7 ...",
    "photo.png": b"PK\x03\x04 ...",
    "notes.txt": b"meeting at noon",
}
for name, data in FILES.items():
    kind = next((k for sig, k in SIGNATURES.items() if data.startswith(sig)), "unknown")
    ext = name.rsplit(".", 1)[1]
    flag = "" if kind in (ext, "unknown") else "  <- mismatch"
    print(f"{name:<11} {kind}{flag}")
```

```text
report.pdf  pdf
photo.png   zip  <- mismatch
notes.txt   unknown
```

`photo.png` adını taşıyan dosya aslında bir zip arşivi: bir şeyi gözden
saklamak için yapılmış olabilir. Metin dosyalarının sabit bir imzası
yoktur; bu yüzden `unknown` uyuşmazlık sayılmadı.

## Dosya zamanları ve zaman çizelgesi

Dosya sistemleri her dosya için birkaç zaman tutar: son **değiştirilme**
(modified), son **erişim** (accessed) ve oluşturma ya da meta veri
değişikliği. Bu zamanlar, Olay Müdahalesi bölümündeki zaman çizelgesinin
bir başka kaynağıdır:

```python
RECORDS = [
    ("/tmp/x.zip", "created", "02:17:40"),
    ("/srv/data/customers.csv", "accessed", "02:19:58"),
    ("/tmp/x.zip", "modified", "02:20:03"),
    ("/home/bob/.bash_history", "modified", "02:21:10"),
]
for path, kind, time in sorted(RECORDS, key=lambda r: r[2]):
    print(time, f"{kind:<8}", path)
```

```text
02:17:40 created  /tmp/x.zip
02:19:58 accessed /srv/data/customers.csv
02:20:03 modified /tmp/x.zip
02:21:10 modified /home/bob/.bash_history
```

Müşteri dosyası okunduktan birkaç saniye sonra geçici klasördeki arşiv
değişti: dışa aktarılan verinin paketlendiğini düşündüren bir sıra. Ama
dosya zamanları **kesin kanıt değildir**: değiştirilebilirler ve
yorumlanmaları dosya sistemine bağlıdır. Bulgular bu yüzden birden çok
bağımsız kaynakla (ağ kayıtları, uygulama kayıtları) doğrulanır.

## Rapor

İncelemenin sonunda bir **rapor** yazılır: ne toplandı, özetleri neydi,
hangi araç ve yöntem kullanıldı, ne bulundu ve ne **bulunmadı**. Rapor
yalnızca kanıtların gösterdiğini söyler, tahmini kanıt gibi anlatmaz ve
başka bir uzmanın aynı adımları izleyip aynı sonuca varabileceği kadar
ayrıntılıdır.

## Özet

- **Adli bilişim:** dijital kanıtı toplamak, korumak, incelemek,
  doğrulanabilir biçimde raporlamak.
- Kanıt toplanınca **özeti** kaydedilir; inceleme **kopya** üzerinde
  yapılır.
- **Gözetim zinciri** her el değiştirmeyi kesintisiz belgeler.
- Toplama **en uçucudan** başlar: bellek, bağlantılar, süreçler, sonra disk.
- Dosyanın gerçek türü **imzasından** anlaşılır, uzantısından değil.
- Dosya zamanları yararlı ama kesin değildir; bulgular birden çok kaynakla
  doğrulanır.
