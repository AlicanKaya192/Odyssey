# Bellek Güvenliği ve Arabellek Taşması

Bir program çalışırken verisini bellekte tutar: bir ad, bir sayı, bir
dosyanın içeriği. Bu veriler bellekte **yan yana** durur. Bir değişkene
ayrılan alanın dışına yazmak, hemen yanındaki başka bir değişkeni sessizce
bozar. Buna **bellek güvenliği hatası** (memory safety bug) denir ve
yıllardır en ciddi güvenlik açıklarının başında gelir.

Bu bölüm bu hataların nasıl oluştuğunu Python'da kurduğumuz **oyuncak bir
bellekle** gösteriyor: gerçek belleğe dokunmuyoruz, yalnızca bir
`bytearray` üzerinde aynı mantığı izliyoruz. Amaç hatayı tanımak ve önlemeyi
öğrenmek.

## Arabellek nedir?

**Arabellek** (buffer), belirli sayıda bayt için ayrılmış bir bellek
alanıdır. C gibi dillerde `char name[8];` yazınca bellekte tam 8 baytlık
bir yer ayrılır. Bu alana 8 bayttan fazlasını yazmaya çalışınca ne olacağı
dile bağlıdır.

Python her yazmada sınırı denetler. Alanın dışına yazmak bir hata ile
durur:

```python
buffer = bytearray(8)
print(len(buffer))
try:
    buffer[8] = 65
except IndexError as error:
    print("IndexError:", error)
```

```text
8
IndexError: bytearray index out of range
```

8 baytlık arabelleğin son geçerli sırası `7`'dir; `8`'e yazmak engellendi.
Bu denetime **sınır denetimi** (bounds checking) denir. C ve C++ bu
denetimi kendiliğinden yapmaz: yazma işlemi alanın dışına taşar ve yanındaki
veriyi bozar. Buna **arabellek taşması** (buffer overflow) denir.

## Taşmayı oyuncak bellekte görmek

C'nin davranışını taklit etmek için 12 baytlık bir bellek kuralım. İlk 8
bayt kullanıcının adı, son 4 bayt kullanıcının rolü olsun:

| Bayt | 0–7 | 8–11 |
|---|---|---|
| Alan | `name` (8 bayt) | `role` (4 bayt) |

Sınırı denetlemeyen bir kopyalama fonksiyonu, verinin uzunluğu ne olursa
olsun hepsini yazar:

```python
memory = bytearray(12)
memory[8:12] = b"USER"


def unsafe_copy(memory, start, data):
    for i, byte in enumerate(data):
        memory[start + i] = byte


unsafe_copy(memory, 0, b"alice")
print("name:", bytes(memory[0:8]))
print("role:", bytes(memory[8:12]))
unsafe_copy(memory, 0, b"Bartholomew!")
print("name:", bytes(memory[0:8]))
print("role:", bytes(memory[8:12]))
```

```text
name: b'alice\x00\x00\x00'
role: b'USER'
name: b'Bartholo'
role: b'mew!'
```

`alice` 5 bayt; alana sığdı, kalan 3 bayt sıfır kaldı. `Bartholomew!` ise
12 bayt: ilk 8'i ad alanına, kalan 4 bayt rolün
üstüne yazıldı. Rol artık `USER` değil, adın kuyruğu. Program hiçbir hata
vermedi; yalnızca yanlış bir rolle çalışmaya devam etti.

Bu, sorunun özü: taşma **sessizdir**. Gerçek programlarda taşan veri
rolü, bir sayacı, bir işaretçiyi ya da programın bir sonra nereye
gideceğini tutan bilgiyi bozabilir. Dışarıdan gelen veri (bir ağ paketi,
bir dosya, bir form alanı) bu taşmayı tetikleyebiliyorsa, saldırgan
programın davranışını değiştirebilir. Bu yüzden taşma bir **güvenlik**
hatasıdır, yalnızca bir yazılım hatası değil.

## Önlem: yazmadan önce ölç

Düzeltme basit: kopyalamadan önce verinin alana sığıp sığmadığına bak.

```python
def safe_copy(memory, start, size, data):
    if len(data) > size:
        return False
    memory[start:start + len(data)] = data
    return True


memory = bytearray(12)
memory[8:12] = b"USER"
print(safe_copy(memory, 0, 8, b"alice"))
print(safe_copy(memory, 0, 8, b"Bartholomew!"))
print("role:", bytes(memory[8:12]))
```

```text
True
False
role: b'USER'
```

Uzun ad reddedildi ve rol yerinde kaldı. Uzun veriyi reddetmek ya da
alana sığacak kadarını almak (kırpmak) iki geçerli seçenektir; hangisinin
doğru olduğu işe bağlıdır. Yanlış olan tek şey, ölçmeden yazmaktır.

C'de bu yüzden bazı standart fonksiyonlar tehlikeli sayılır: `gets`,
`strcpy`, `strcat` ve `sprintf` hedef alanın boyunu bilmeden yazar.
Yerlerine boyu da alan `fgets`, `strncpy` / `strlcpy`, `strncat` ve
`snprintf` kullanılır. Kod incelemesinde (Kod İnceleme ve Statik Analiz
bölümü) bu adlar ilk aranan şeylerdendir.

## Bir eksik, bir fazla: off-by-one

Taşmanın en sinsi hâli **bir fazla** yazmaktır. Döngünün sınırını `<=` ile
yazmak (ya da `range(size + 1)`) alanın hemen bitişiğindeki tek baytı
bozar:

```python
size = 8
written = []
for i in range(size + 1):
    written.append(i)
print(len(written), "bytes written into", size)
print("last index:", written[-1])
```

```text
9 bytes written into 8
last index: 8
```

8 baytlık alana 9 bayt yazıldı; son sıra `8`, yani alanın
dışı. Tek bayt küçük görünür, ama o bayt bir metnin sonunu gösteren sıfır
ya da bir uzunluk alanının parçası olabilir. C'deki metinler sonlarındaki
sıfır baytla biter; 8 harflik bir ad için **9** bayt gerekir. Bu tek bayt
unutulunca da aynı hata doğar.

## Tam sayı taşması: boyut hesabı yanlış çıkınca

Bazen sorun kopyalamada değil, **alanın boyunu hesaplarken** başlar. C'de
sayılar sabit genişliktedir; 8 bitlik bir sayı en çok 255 tutar ve
fazlası başa sarar (`n & 0xFF` bunu taklit eder):

```python
def size_8bit(n):
    return n & 0xFF


header = 200
body = 100
print("real size:", header + body)
print("8-bit size:", size_8bit(header + body))
```

```text
real size: 300
8-bit size: 44
```

300 bayt gereken veri için yalnızca 44 baytlık bir
alan ayrılır; ardından gelen kopyalama 300 baytın hepsini yazar ve
taşma olur. Bu yüzden boyut hesabı da sınır denetiminin parçasıdır:
toplamadan ya da çarpmadan **önce** sonucun sığıp sığmayacağına bakılır.

## Bellek hatalarının ailesi

| Hata | Ne olur? |
|---|---|
| **Arabellek taşması** | Alanın sonundan öteye yazılır, komşu veri bozulur |
| **Aşırı okuma** (out-of-bounds read) | Alanın dışından okunur, başka verinin içeriği sızar |
| **Off-by-one** | Sınır bir eksik ya da bir fazla hesaplanır |
| **Tam sayı taşması** | Boyut hesabı başa sarar, ayrılan alan küçük kalır |
| **Serbest bırakıldıktan sonra kullanım** (use-after-free) | Geri verilmiş bellek hâlâ kullanılır |
| **Çift serbest bırakma** (double free) | Aynı bellek iki kez geri verilir |

Hepsinin ortak noktası: program, kendisine ait olmayan ya da artık geçerli
olmayan bir bellek alanına dokunur.

## Bellek güvenli diller

<figure class="fig"><div class="versus">
  <div><h4>Bellek güvenli olmayan (C, C++)</h4>Hız ve donanıma yakınlık sağlar. Sınır denetimi ve belleğin ne zaman geri verileceği <b>programcıya</b> kalır. Bir unutma, sessiz bir taşma demektir.</div>
  <div><h4>Bellek güvenli (Python, Rust, Go, Java)</h4>Dil her erişimi denetler ya da belleğin ömrünü kendisi yönetir. Taşma <b>hata olarak durur</b>, komşu veriyi bozmaz.</div>
</div><figcaption>Bellek güvenli dil bu hata ailesinin büyük kısmını baştan ortadan kaldırır.</figcaption></figure>

Python'da yazdığın kod bu hataların çoğundan korunur, ama tamamen değil:
Python'un kendisi ve kullandığın birçok kütüphane (NumPy gibi) C ile
yazılmıştır. O C kodundaki bir taşma, Python programını da etkiler. Rust
ise bellek güvenliğini derleme anında denetler ve bunu C kadar hızlı
yapar; Rust patikası bunu ayrıntısıyla anlatıyor.

Bir sonraki bölüm, bellek güvenli olmayan programları korumak için
işletim sistemlerinin ve derleyicilerin eklediği katmanları anlatıyor:
ASLR, DEP ve kanarya.

## Özet

- Arabellek, sabit boyutlu bir bellek alanıdır; dışına yazmak **arabellek
  taşması**dır ve komşu veriyi **sessizce** bozar.
- Python her yazmada **sınır denetimi** yapar; C ve C++ yapmaz.
- Önlem: yazmadan önce **ölç**; uzun veriyi reddet ya da kırp.
- `gets`, `strcpy`, `strcat`, `sprintf` boy bilmeden yazar; boyu alan
  karşılıkları kullanılır.
- **Off-by-one** ve **tam sayı taşması** da aynı sonuca götürür: alan
  sanıldığından küçüktür.
- **Bellek güvenli diller** bu hata ailesinin çoğunu baştan engeller.
