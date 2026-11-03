# Dosya İzinleri

İşletim Sistemi Güvenliği bölümünde çekirdeğin her isteği denetlediğini
gördük. En sık sorulan soru da şu: **bu kullanıcı bu dosyayı okuyabilir,
değiştirebilir ya da çalıştırabilir mi?** Cevabı dosya izinleri verir.
Yanlış bir izin en güçlü şifrelemeyi de boşa çıkarabilir: herkesin
okuyabildiği bir anahtar dosyası, anahtarın hiç gizli olmaması demektir.

Bu bölüm Linux ve macOS'taki **Unix izin modelini** anlatıyor; Windows'un
farklı modeline sonda kısaca değineceğiz. Kodlar yine oyuncak: gerçek
dosyalara dokunmuyor, izinleri sayılar ve sözlüklerle hesaplıyor.

## Üç sınıf, üç izin

Her dosyanın bir **sahibi** (owner) ve bir **grubu** (group) vardır.
Dosyaya erişmek isteyen herkes üç sınıftan birine düşer:

- **Sahip** (user, `u`): dosyanın sahibi olan kullanıcı.
- **Grup** (group, `g`): dosyanın grubundaki kullanıcılar.
- **Diğerleri** (other, `o`): geri kalan herkes.

Her sınıf için üç izin vardır: **okuma** (`r`, read), **yazma** (`w`,
write) ve **çalıştırma** (`x`, execute). Klasörlerde `x`, klasörün içine
girebilmek demektir. Toplam dokuz izin, `rwxr-xr--` gibi dokuz harflik bir
dizeyle yazılır: ilk üç harf sahibin, sonraki üç grubun, son üç diğerlerinin.

## Sayıyla yazmak: sekizlik izinler

Her harf bir bittir: `r` = 4, `w` = 2, `x` = 1. Bir sınıfın izni bunların
toplamıdır: `rwx` = 7, `r-x` = 5, `r--` = 4. Üç sınıfın rakamı yan yana
yazılınca **sekizlik** (octal) izin çıkar: `755`, `644`, `600`. Python'da
sekizlik sayı `0o` ile yazılır ve standart kütüphanedeki `stat.filemode`
bir sayıyı `ls -l`'deki gibi bir dizeye çevirir:

```python
import stat

for mode in [0o755, 0o644, 0o600, 0o777]:
    print(oct(mode), stat.filemode(stat.S_IFREG | mode))
```

```text
0o755 -rwxr-xr-x
0o644 -rw-r--r--
0o600 -rw-------
0o777 -rwxrwxrwx
```

Baştaki `-` sıradan bir dosya olduğunu gösterir (klasörde `d`). Aynı
çeviriyi kendimiz de yapabiliriz: her sınıfın üç bitini sırayla kaydırıp
okuruz.

```python
def to_string(mode):
    letters = ""
    for shift in (6, 3, 0):
        bits = (mode >> shift) & 7
        letters += "r" if bits & 4 else "-"
        letters += "w" if bits & 2 else "-"
        letters += "x" if bits & 1 else "-"
    return letters


print(to_string(0o750))
print(0o750, 7 * 64 + 5 * 8 + 0)
```

```text
rwxr-x---
488 488
```

`750` sahibe her şeyi, gruba okuma ve çalıştırmayı veriyor, diğerlerine
hiçbir şey vermiyor. Sekizlik sayının ondalık değeri 488: her
rakam 8'in bir kuvvetiyle çarpılır (`7 × 64 + 5 × 8 + 0`).

| İzin | Dize | Ne için? |
|---|---|---|
| `755` | `rwxr-xr-x` | Programlar, herkesin girebileceği klasörler |
| `644` | `rw-r--r--` | Herkesin okuyabileceği sıradan dosyalar |
| `600` | `rw-------` | Gizli dosyalar: anahtarlar, parola dosyaları |
| `700` | `rwx------` | Yalnızca sahibin girebileceği klasörler |
| `777` | `rwxrwxrwx` | Herkes her şeyi yapar: neredeyse her zaman yanlış |

## Hangi sınıf? Yalnızca biri

Unix izinlerinin en çok yanlış anlaşılan kuralı: sistem erişen kişi için
**tek bir sınıf** seçer ve yalnızca o sınıfın bitlerine bakar. Sahipse
sahip bitleri; değilse ve gruptaysa grup bitleri; ikisi de değilse
diğerleri. Sınıflar **toplanmaz**.

<figure class="fig"><div class="flow">
  <span class="node">İstek</span><span class="arrow">→</span>
  <span class="node acc">Sahip mi?</span><span class="arrow">→</span>
  <span class="node acc">Grupta mı?</span><span class="arrow">→</span>
  <span class="node">Diğerleri</span><span class="arrow">→</span>
  <span class="node ok">O sınıfın bitleri</span>
</div><figcaption>İlk eşleşen sınıf seçilir; öteki sınıfların bitlerine hiç bakılmaz.</figcaption></figure>

```python
def can(file, user, groups, action):
    bit = {"r": 4, "w": 2, "x": 1}[action]
    if user == file["owner"]:
        bits = (file["mode"] >> 6) & 7
    elif file["group"] in groups:
        bits = (file["mode"] >> 3) & 7
    else:
        bits = file["mode"] & 7
    return bool(bits & bit)


report = {"owner": "ada", "group": "staff", "mode": 0o640}
print(can(report, "ada", ["staff"], "w"))
print(can(report, "bob", ["staff"], "r"))
print(can(report, "bob", ["staff"], "w"))
print(can(report, "eve", ["guests"], "r"))
```

```text
True
True
False
False
```

`640` izinli raporu sahibi `ada` yazabiliyor; gruptaki `bob` yalnızca
okuyabiliyor; gruba girmeyen `eve` hiçbir şey yapamıyor. Bu kural ters
yönde de işler: izni `077` olan bir dosyayı sahibi **okuyamaz**, gruptakiler
ve diğerleri okuyabilir. Sahiplik ayrıcalık değil, yalnızca hangi üç bite
bakılacağını belirleyen şeydir.

## Yeni dosyanın izni: umask

Bir program yeni bir dosya açtığında izni nereden gelir? Program genellikle
dosyalar için `666`, klasörler için `777` ister; işletim sistemi bundan
**umask** denen maskedeki bitleri çıkarır:

```python
for umask in [0o022, 0o077]:
    file_mode = 0o666 & ~umask
    dir_mode = 0o777 & ~umask
    print(oct(umask), oct(file_mode), oct(dir_mode))
```

```text
0o22 0o644 0o755
0o77 0o600 0o700
```

Yaygın umask `022`, grup ve diğerlerinden yazma iznini kaldırır: dosyalar
`644`, klasörler `755` olur. Yalnızca sahibin erişmesi gereken yerlerde
(bir kullanıcının ev klasörü, bir hizmetin gizli verisi) `077` kullanılır:
dosyalar `600`, klasörler `700`. Umask izinleri yalnızca **kaldırır**,
hiçbir zaman eklemez.

## İzinleri denetlemek

İzin hataları iki yerde toplanır: **herkesin yazabildiği** dosyalar ve
**gizli olması gereken ama başkalarının okuyabildiği** dosyalar. İkisi de
izin sayısındaki bitlere bakarak bulunur:

```python
FILES = [
    {"path": "/srv/app/config.ini", "mode": 0o666},
    {"path": "/srv/app/run.sh", "mode": 0o755},
    {"path": "/home/ada/.ssh/id_key", "mode": 0o644},
]
for f in FILES:
    if f["mode"] & 0o002:
        print(f["path"], "world-writable")
    if f["path"].endswith("_key") and f["mode"] & 0o077:
        print(f["path"], "key readable by others")
```

```text
/srv/app/config.ini world-writable
/home/ada/.ssh/id_key key readable by others
```

Yapılandırma dosyasını herkes değiştirebilir: biri programın ayarlarını
bozabilir ya da onu başka bir yere yönlendirebilir. Anahtar dosyasını ise
herkes okuyabilir: anahtar artık gizli değildir. Program dosyası `755` ile
olması gerektiği gibi. Birçok program bu yüzden izni geniş bir anahtar
dosyasını kullanmayı **reddeder**; doğru davranış budur.

## Özel bitler ve Windows

- **setuid / setgid:** program, çalıştıranın değil **dosya sahibinin**
  (ya da grubunun) yetkisiyle çalışır. Parola değiştirme gibi işler için
  gereklidir, ama sahibi yönetici olan her setuid program, bir sonraki
  bölümün konusu olan yetki yükseltmenin potansiyel kapısıdır; sayıları az
  tutulur ve düzenli denetlenir.
- **Yapışkan bit** (sticky bit): herkesin yazabildiği bir klasörde (`/tmp`
  gibi) herkesin yalnızca **kendi** dosyasını silmesine izin verir.
- **Windows** dokuz bit yerine **erişim denetim listeleri** (ACL) kullanır:
  her dosya için "şu kullanıcı ya da grup, şu izinler" satırlarından oluşan
  bir liste. Model daha ayrıntılıdır ama ilke aynıdır: en az yetki,
  gizli dosyayı yalnızca sahibine aç.

## Özet

- Üç sınıf (**sahip**, **grup**, **diğerleri**), üç izin (**r**, **w**,
  **x**); `r` = 4, `w` = 2, `x` = 1.
- Sekizlik izin: `755` programlar, `644` sıradan dosyalar, `600` gizli
  dosyalar; `777` neredeyse her zaman yanlış.
- Erişende **tek sınıf** seçilir; sınıflar toplanmaz.
- **umask** yeni dosyanın izninden bit **kaldırır**: `022` → `644` / `755`,
  `077` → `600` / `700`.
- Denetlenecek iki şey: herkesin yazabildiği dosyalar ve başkalarının
  okuyabildiği gizli dosyalar.
