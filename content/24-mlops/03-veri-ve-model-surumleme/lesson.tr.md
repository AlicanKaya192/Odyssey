# Veri ve Model Sürümleme

Kodun her hâlini Git saklıyor: istediğin commit'e dönebiliyorsun. Peki
geçen ayki veri? Üç hafta önce yayına çıkan model dosyası? Tekrarlanabilir
Eğitim bölümünde bir eğitimin kaydına verinin parmak izini yazdık. Ama
parmak izi tek başına veriyi geri getirmez; yalnızca hangisi olduğunu
söyler. Bu bölümde veriyi ve modeli de kod gibi **sürümlemeyi**
(versioning) öğreniyoruz: her hâlini saklamak, adıyla bulmak ve geri
getirmek.

## Veri dosyaları

Müşteri verisi her ay büyüyor. İlk sürümde 4000, ikincisinde 5000 müşteri
var. İkisini de CSV dosyasına yazıp boylarına ve parmak izlerine bakalım:

```python
import hashlib
from pathlib import Path
from ml_data import write_customers_csv


def file_hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()[:12]


write_customers_csv("customers_v1.csv", 4000)
write_customers_csv("customers_v2.csv", 5000)
for name in ["customers_v1.csv", "customers_v2.csv"]:
    print(name, Path(name).stat().st_size, "bytes", file_hash(name))
```

```text
customers_v1.csv 131847 bytes 2448b83141ea
customers_v2.csv 164798 bytes fd8e64e44454
```

Bu kez parmak izini Python nesnelerinden değil, **dosyanın baytlarından**
hesapladık: diskteki dosya neyse özet de onu anlatıyor. Aynı dosya her
bilgisayarda aynı özeti verir.

## Neden doğrudan Git'e koymuyoruz?

Bu dosyalar küçük, Git'e konabilir. Ama gerçek projelerde veri yüzlerce
megabayt, model dosyaları da büyük: bu bölümün sonunda eğiteceğimiz
rastgele orman tek başına 6,9 MB. Git'te üç sorun çıkıyor:

- **Geçmiş hiç küçülmez.** Git her sürümü saklar. Her hafta yeniden
  eğitilen bir model, yıl sonunda depoya elliden fazla büyük dosya
  ekler; depoyu klonlayan herkes hepsini indirir.
- **Sınırlar var.** GitHub 100 MB'tan büyük dosyayı kabul etmiyor.
- **Fark işe yaramaz.** Git metin dosyasında hangi satırın değiştiğini
  gösterir; model dosyası gibi ikili (binary) bir dosyada "değişti"
  demekten öteye gidemez.

Çözüm, işi ikiye bölmek: büyük dosyalar ayrı bir **depoda** (store)
durur, Git'e yalnızca onları gösteren küçük bir **işaret dosyası**
(pointer file) girer.

## İçerik adresli depo

Depodaki her dosyanın adı, içeriğinin özeti olsun. Buna **içerik
adresli depolama** (content-addressed storage) denir: dosyayı adıyla
değil içeriğiyle bulursun. Aynı içerik her zaman aynı yere düşer.

```python
import json
import shutil

STORE = Path("store")


def put(path):
    digest = hashlib.sha256(Path(path).read_bytes()).hexdigest()
    target = STORE / digest[:2] / digest[2:]
    if not target.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
    pointer = {"path": str(path), "sha256": digest, "size": Path(path).stat().st_size}
    Path(f"{path}.ptr").write_text(json.dumps(pointer, indent=2))
    return digest


put("customers_v1.csv")
print(Path("customers_v1.csv.ptr").read_text())
```

```text
{
  "path": "customers_v1.csv",
  "sha256": "2448b83141eacf2d4a59fe0a808c88c2a2f3c1aba8006c74bd6d58ca77cb8db3",
  "size": 131847
}
```

`put` üç iş yapıyor:

1. Dosyanın tam özetini (64 karakter) hesaplıyor.
2. Dosyayı depoya, özetinden türeyen bir yola kopyalıyor:
   ilk iki karakter klasör, gerisi dosya adı. Tek klasörde binlerce
   dosya birikmesin diye özetler böyle bölünür.
3. Yanına bir işaret dosyası (`.ptr`) yazıyor: hangi dosya, özeti ne,
   kaç bayt.

İşaret dosyası birkaç satırlık bir metin. Git'e o girer; CSV dosyası ise
`.gitignore`'a yazılır. Kodun bir commit'i artık "bu kod, bu veriyle"
demek oluyor.

## Aynı içerik bir kez saklanır

İkinci sürümü de depoya koyalım. Bir de birinci sürümün kopyasını başka
bir adla ekleyelim:

```python
put("customers_v2.csv")
shutil.copyfile("customers_v1.csv", "backup.csv")
put("backup.csv")
pointers = list(Path(".").glob("*.ptr"))
stored = [p for p in STORE.rglob("*") if p.is_file()]
print("pointer files:", len(pointers))
print("files in the store:", len(stored))
```

```text
pointer files: 3
files in the store: 2
```

Üç işaret dosyası var ama depoda iki dosya duruyor. `backup.csv`'nin
içeriği `customers_v1.csv` ile aynı, özeti de aynı; depodaki yer zaten
dolu olduğu için `put` ikinci kez kopyalamadı. Ad değil içerik önemli.
(`glob("*.ptr")` klasördeki `.ptr` dosyalarını, `rglob("*")` alt
klasörler dahil her şeyi listeler.)

## Eski sürümü geri getirmek

İşaret dosyası elimizdeyse veriyi depodan geri getirebiliriz. Getirirken
bir şeyi daha denetleyelim: depodaki dosya bozulmuş olabilir (disk
hatası, yarım kalan kopya). Getirilen baytların özeti işaret
dosyasındakiyle aynı olmalı:

```python
def get(pointer_path):
    pointer = json.loads(Path(pointer_path).read_text())
    digest = pointer["sha256"]
    data = (STORE / digest[:2] / digest[2:]).read_bytes()
    if hashlib.sha256(data).hexdigest() != digest:
        raise ValueError(f"{pointer['path']}: the stored file is damaged")
    Path(pointer["path"]).write_bytes(data)


Path("customers_v1.csv").unlink()
print("deleted:", Path("customers_v1.csv").exists())
get("customers_v1.csv.ptr")
print("restored:", file_hash("customers_v1.csv"))
```

```text
deleted: False
restored: 2448b83141ea
```

Dosyayı sildik, işaret dosyasından geri getirdik: parmak izi baştakiyle
aynı. `unlink` dosyayı silen `Path` metodu. Gerçek projede `get`'i
çağıran, eski bir commit'e dönen kişidir: Git işaret dosyasının eski
hâlini getirir, `get` de verinin eski hâlini.

## İki sürüm arasında ne değişti?

Özet "değişti" der ama neyin değiştiğini söylemez. Verinin her satırında
bir kimlik (`id`) varsa iki sürümü satır satır karşılaştırabiliriz:

```python
import csv


def read_rows(path):
    with open(path, encoding="utf-8") as f:
        return {row["id"]: row for row in csv.DictReader(f)}


old, new = read_rows("customers_v1.csv"), read_rows("customers_v2.csv")
added = [i for i in new if i not in old]
removed = [i for i in old if i not in new]
changed = [i for i in old if i in new and old[i] != new[i]]
print("added:", len(added), "removed:", len(removed), "changed:", len(changed))
print("first new customer:", added[0])
```

```text
added: 1000 removed: 0 changed: 0
first new customer: C00-04001
```

İkinci sürümde 1000 yeni müşteri var; eski müşterilerin hiçbiri silinmemiş
ya da değişmemiş. Bu bilgi bir eğitim kaydının yanında çok değerli:
"model kötüleşti" dendiğinde ilk soru "veride ne değişti?" olur.
Sözlükleri `{row["id"]: row ...}` biçiminde kurmak, bir müşteriyi
kimliğiyle hemen bulmamızı sağlıyor.

## Modeli sürümlemek

Model de bir dosya; aynı depoya girer. Ama model dosyası tek başına
yetmez: hangi veriyle, hangi ayarlarla, hangi kütüphaneyle eğitildiğini
de bilmek isteriz. Modelden geriye doğru verisine ve koduna giden bu
bağa **soy** (lineage) denir:

```python
import pickle
import sklearn
from sklearn.ensemble import RandomForestClassifier
from ml_data import NUMERIC


def load(path):
    rows = read_rows(path).values()
    X = [[float(r[c]) for c in NUMERIC] + [1 if r["plan"] == "pro" else 0] for r in rows]
    y = [int(r["churned"]) for r in rows]
    return X, y


CONFIG = {"n_estimators": 50, "random_state": 0}
model = RandomForestClassifier(**CONFIG).fit(*load("customers_v2.csv"))
Path("model.pkl").write_bytes(pickle.dumps(model))
data_pointer = json.loads(Path("customers_v2.csv.ptr").read_text())
lineage = {
    "model": put("model.pkl")[:12],
    "data": data_pointer["sha256"][:12],
    "config": CONFIG,
    "scikit-learn": sklearn.__version__,
}
print(json.dumps(lineage, indent=2))
```

```text
{
  "model": "dd0ba2458f51",
  "data": "fd8e64e44454",
  "config": {
    "n_estimators": 50,
    "random_state": 0
  },
  "scikit-learn": "1.9.1"
}
```

CSV'den okunan her değer metin olduğu için `float` ve `int` ile sayıya
çevriliyor. `RandomForestClassifier(**CONFIG)` sözlüğü parametrelere
açıyor: `n_estimators=50, random_state=0` yazmakla aynı.

Soy kaydı modelin kimliğini (dosyasının özeti) verisinin kimliğine
bağlıyor. Altı ay sonra "bu model hangi veriyle eğitildi?" sorusunun
cevabı burada; veri de depoda, `get` ile geri gelir.

## Aynı eğitim, aynı dosya

Tekrarlanabilir Eğitim bölümünde iki modelin aynı tahminleri verdiğini
sınamıştık. Model dosyalarının özetine bakarak daha da sıkı bir sınama
yapabiliriz:

```python
again = RandomForestClassifier(**CONFIG).fit(*load("customers_v2.csv"))
print("same file:", pickle.dumps(again) == Path("model.pkl").read_bytes())
```

```text
same file: True
```

Aynı veri, aynı ayarlar, aynı tohum: 6,9 MB'lık dosya bayt
bayt aynı. Bu her kütüphanede ve her ortamda garanti değil (başka bir
sürüm ya da başka bir işlemci farklı bayt üretebilir); bu yüzden asıl
sınama tahminlerin karşılaştırılmasıdır. Ama dosyalar aynı çıkıyorsa
depo aynı modeli ikinci kez saklamaz.

Model dosyası için bir uyarı: `pickle` ile kaydedilen dosya açılırken
içindeki kod çalışabilir. Yalnızca kendi ürettiğin ya da güvendiğin bir
kaynaktan gelen model dosyasını aç.

## Gerçek araçlar

Bu bölümde yazdığımız küçük depo, gerçek araçların fikrinin aynısı:

- **Git LFS** (Large File Storage): büyük dosyaları Git'in dışında
  saklayıp depoya işaret dosyası koyan bir Git eklentisi.
- **DVC** (Data Version Control): veri ve modeller için işaret
  dosyaları (`.dvc`) yazar; dosyaların kendisini bir klasöre ya da bulut
  depolamaya gönderir. Özet, boyut ve yol, bizim `.ptr` dosyamızdaki gibi.

Hangi araç kullanılırsa kullanılsın kural aynı: büyük dosya ayrı bir
depoda, Git'te yalnızca onu gösteren küçük bir metin.

## Özet

- Veri ve model de kod gibi **sürümlenir**: her hâli saklanır, geri
  getirilebilir.
- Büyük dosyalar Git'e girmez: geçmiş büyür, GitHub 100 MB'tan büyük
  dosyayı kabul etmez, ikili dosyada fark işe yaramaz.
- **İçerik adresli depoda** dosyanın adı içeriğinin özetidir. Aynı içerik
  bir kez saklanır.
- Git'e küçük bir **işaret dosyası** girer: yol, özet, boyut.
- Geri getirirken özeti yeniden hesapla; uyuşmazsa dosya bozuktur.
- Kimlik sütunu olan iki sürüm satır satır karşılaştırılabilir:
  eklenen, silinen, değişen.
- **Soy** kaydı modeli verisine, ayarlarına ve ortamına bağlar.
