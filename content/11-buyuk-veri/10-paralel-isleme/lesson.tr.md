# Paralel İşleme

Bilgisayarının işlemcisinde birden çok **çekirdek** var; her biri ayrı bir
iş yapabiliyor. Bu bilgisayarda kaç tane olduğunu Python söylüyor:

```python
import os
print(os.cpu_count())
```

```text
24
```

Ama yazdığın Python kodu varsayılan olarak bunlardan **yalnızca birini**
kullanıyor. Paralel işleme, işi birbirinden bağımsız parçalara bölüp
parçaları **aynı anda** farklı çekirdeklerde çalıştırmak demek. Bu bölümde
bunun nasıl yapıldığını, ne zaman gerçekten hızlandırdığını ve ne zaman
tersine yavaşlattığını ölçerek göreceğiz. İkinci kısım en az birincisi kadar
önemli.

## Süreç ve iş parçacığı

Bir işi aynı anda yaptırmanın iki yolu var:

<figure class="fig">
  <div class="versus">
    <div><h4>Süreç (process)</h4><p>Ayrı bir Python, kendi belleği<br>Veri kopyalanarak gider<br>GIL'den etkilenmez<br>Başlatması pahalı</p></div>
    <div><h4>İş parçacığı (thread)</h4><p>Aynı süreçte, ortak bellek<br>Veri kopyalanmaz<br>GIL yüzünden Python kodu sırayla<br>Başlatması ucuz</p></div>
  </div>
  <figcaption>Saf Python hesabı için süreç; beklemek ve NumPy işi için iş parçacığı.</figcaption>
</figure>

- **Süreç** (*process*): ayrı bir program gibi çalışan, kendi belleği olan
  bir Python. Süreçler birbirinin değişkenlerini göremiyor; veri bir
  süreçten ötekine **kopyalanarak** gidiyor.
- **İş parçacığı** (*thread*): aynı sürecin içinde, aynı belleği paylaşan
  bir iş kolu. Veri kopyalanmıyor ama aşağıdaki kilit yüzünden Python kodu
  aynı anda çalışamıyor.

## GIL: Python'un kilidi

Python'un (CPython'un) içinde **GIL** (*Global Interpreter Lock*, genel
yorumlayıcı kilidi) adında bir kilit var: bir süreçte aynı anda **yalnızca
bir** iş parçacığı Python kodu çalıştırabiliyor. Dört iş parçacığı açsan da
saf Python hesabı sırayla yapılıyor.

İki istisna var; bu iki durumda iş parçacığı kilidi bırakıyor:

1. **Beklerken:** dosya okurken, ağdan cevap beklerken, `time.sleep` sırasında.
2. **NumPy ve pandas'ın içinde:** büyük dizi hesapları C dilinde yapılıyor ve
   o sırada kilit bırakılıyor.

Bu yüzden kural basit: **saf Python hesabı için süreç, bekleme ve NumPy işi
için iş parçacığı.**

## `concurrent.futures`

Python'un standart kütüphanesindeki `concurrent.futures` iki yolu da aynı
biçimde kullandırıyor: `ProcessPoolExecutor` (süreç havuzu) ve
`ThreadPoolExecutor` (iş parçacığı havuzu). İkisinin de `map` yöntemi bir
fonksiyonu bir listedeki her öğeye uygulayıp sonuçları **aynı sırayla**
veriyor.

Saf Python ağırlıklı bir iş: 0 ile 400 000 arasındaki asal sayıları saymak.
Aralığı sekiz parçaya bölüp üç yolla deneyelim:

```python
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

def count_primes(bounds):
    start, stop = bounds
    count = 0
    for n in range(start, stop):
        if n < 2:
            continue
        d = 2
        while d * d <= n:
            if n % d == 0:
                break
            d += 1
        else:
            count += 1
    return count

if __name__ == "__main__":
    parts = [(i * 50_000, (i + 1) * 50_000) for i in range(8)]
    with ProcessPoolExecutor(max_workers=4) as ex:
        total = sum(ex.map(count_primes, parts))
    print(total)
```

Bu bilgisayarda (iki denemenin hızlısı):

| Yol | Sonuç | Süre |
|---|---|---|
| Sıralı (`map`) | 33 860 | 1,09 sn |
| 4 iş parçacığı | 33 860 | 1,12 sn |
| 4 süreç | 33 860 | 0,50 sn |

- İş parçacıkları hiç hızlandırmadı: GIL yüzünden asal sayma yine sırayla
  yapıldı.
- Dört süreç işi yarıdan fazla kısalttı. Dört kat değil, çünkü süreçleri
  başlatmanın da bir bedeli var (birazdan).
- Üçünün sonucu aynı: paralel çalıştırmak **cevabı değiştirmemeli**. Bunu
  her zaman denetle.

## `if __name__ == "__main__":` neden şart?

Windows'ta yeni bir süreç, programını **baştan çalıştırarak** başlıyor. Kod
dosyanın en dış düzeyinde havuz kuruyorsa, her yeni süreç de bir havuz
kurmaya çalışıyor; o da yeni süreçler başlatıyor… Odyssey'de bu korumasız kod
zaman aşımına uğradı.

```python
if __name__ == "__main__":
    # havuzu yalnızca ana program kursun
    ...
```

`__name__` ana programda `"__main__"`, yardımcı süreçlerin içinde başka bir
değer. Bu satırın altındaki kod yalnızca bir kez, ana programda çalışıyor.
Yardımcı süreçler yalnızca fonksiyonların **tanımını** okuyor. Bu yüzden
süreçlere verdiğin fonksiyon da (`count_primes`) dosyanın en dış düzeyinde
tanımlanmalı.

## Beklemek için iş parçacıkları

Bir API'den on sayfa çekmek ya da on dosya indirmek gibi işlerde zamanın
çoğu **beklemekle** geçiyor. Bekleyen iş parçacığı kilidi bıraktığı için
burada iş parçacıkları çok etkili. Her biri 0,2 saniye bekleyen on iş:

```python
import time
from concurrent.futures import ThreadPoolExecutor

def wait(i):
    time.sleep(0.2)
    return i

with ThreadPoolExecutor(max_workers=10) as ex:
    result = list(ex.map(wait, range(10)))
```

Sıralı 2,01 saniye, on iş parçacığıyla 0,21 saniye: on beklemenin hepsi aynı
anda yapıldı.

NumPy'nin büyük hesapları da kilidi bırakıyor: 600 × 600'lük sekiz matris
hesabı sıralı 0,23 saniye, dört iş parçacığıyla 0,06 saniye sürdü.

## Paralelliğin bedeli

Süreç başlatmak, ona veri göndermek, sonucu geri almak bedava değil. İş
küçükse bu bedel kazancı yutuyor.

**Çok küçük işler.** On bin sayının karesini almak:

| Yol | Süre |
|---|---|
| Sıralı | 0,0009 sn |
| 4 süreç, her sayı ayrı | 1,78 sn |
| 4 süreç, `chunksize=2_500` | 0,20 sn |

Her sayı ayrı ayrı bir sürece gönderilince iş iki bin kat yavaşladı.
`chunksize` sayıları 2 500'lük gruplar hâlinde göndererek gidip gelmeyi
azaltıyor, ama sıralı hesabın yine çok gerisinde.

**pandas tablosu göndermek.** İki milyon siparişi sekiz parçaya bölüp şehir
başına ciroyu dört süreçle hesapladım:

| Yol | Süre |
|---|---|
| Sıralı, tek tablo | 0,09 sn |
| 4 süreç, parçalar süreçlere gönderiliyor | 1,14 sn |
| Sıralı, 8 Parquet dosyası | 0,27 sn |
| 4 süreç, her süreç kendi dosyasını okuyor | 0,82 sn |

Paralel yol **on iki kat yavaş** kaldı. Sebepleri:

1. pandas'ın gruplaması zaten çok hızlı (C dilinde); bölünecek ağır bir iş
   yok.
2. Her parça sürece **kopyalanarak** gidiyor.
3. Windows'ta her yeni süreç pandas'ı yeniden yüklüyor; bu bilgisayarda
   yalnızca `import pandas` yarım saniyeyi buluyor (0,53–0,69 sn).

Ders şu: paralel işleme **ağır ve bağımsız** işler içindir. Her parçanın işi
saniyeler sürmüyorsa çoğu zaman tek çekirdek daha hızlı.

## Amdahl yasası

Bir programın her parçası paralel olamaz: veriyi bölmek, sonuçları
birleştirmek, dosyayı açmak sırayla yapılıyor. **Amdahl yasası** paralel
yapılamayan kısmın hızlanmaya bir tavan koyduğunu söylüyor:

```text
hızlanma = 1 / ((1 − p) + p / n)
```

`p` işin paralel yapılabilen oranı, `n` çekirdek sayısı.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>%50 paralel</span><span>4 çekirdek: 1,6 kat · 24 çekirdek: 1,92 kat · sonsuz: 2 kat</span></div>
    <div class="anat-row"><span>%90 paralel</span><span>4 çekirdek: 3,08 kat · 24 çekirdek: 7,27 kat · sonsuz: 10 kat</span></div>
    <div class="anat-row"><span>%99 paralel</span><span>4 çekirdek: 3,88 kat · 24 çekirdek: 19,51 kat · sonsuz: 100 kat</span></div>
  </div>
  <figcaption>Sıralı kalan kısım ne kadar küçükse tavan o kadar yüksek. Tavan 1 / (1 − p).</figcaption>
</figure>

İşin yüzde 90'ı paralel olsa bile 24 çekirdek ancak 7,27 kat hızlandırıyor;
sonsuz çekirdek de 10 katı geçemiyor. Sıralı kalan yüzde 10 her şeyi
belirliyor.

## Ne zaman paralel?

1. **İş ağır mı?** Her parça en az birkaç saniye sürmüyorsa önce başka
   yollara bak (doğru türler, Parquet, DuckDB).
2. **Parçalar bağımsız mı?** Birinin sonucu ötekine lazımsa paralel olmaz.
3. **Ne tür iş?** Saf Python hesabı → süreç. Bekleme (ağ, disk) → iş
   parçacığı. NumPy ağırlıklı → iş parçacığı.
4. **Sonuç aynı mı?** Sıralı çözümle karşılaştır.

Çoğu zaman en kolay paralellik, **işi kendisi bölen bir araç** kullanmak:
DuckDB bütün çekirdekleri zaten kullanıyor (Bölüm 7). Bir sonraki bölümdeki
dask da pandas işini parçalara bölüp çekirdeklere kendisi dağıtıyor.

## Özet

- `os.cpu_count()` çekirdek sayısını veriyor; Python kodu varsayılan olarak
  birini kullanıyor.
- Süreç ayrı bellekli bir Python, iş parçacığı aynı süreçte ortak bellekli
  bir iş kolu.
- GIL yüzünden iş parçacıkları saf Python hesabını hızlandırmıyor; bekleme
  ve NumPy işlerinde hızlandırıyor.
- `ProcessPoolExecutor` / `ThreadPoolExecutor` ve `map`; sonuç sırası
  korunuyor.
- Süreç kullanan kod `if __name__ == "__main__":` altında olmalı; yoksa
  Windows'ta her süreç yeni süreçler başlatıyor.
- Paralelliğin bedeli var: küçük işlerde ve veri gönderilen pandas
  işlerinde sıralıdan yavaş kaldı.
- Amdahl: sıralı kalan kısım hızlanmaya tavan koyuyor.
