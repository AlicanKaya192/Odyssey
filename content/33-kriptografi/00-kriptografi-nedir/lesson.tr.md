# Kriptografi Nedir?

**Kriptografi** (cryptography), bilgiyi onu görmemesi ya da değiştirmemesi
gereken kişilere karşı **matematikle** koruma bilimidir. Güvenlik
Temelleri modülünde bazı araçlarını kullandık: parolaları tuzlu özetle
sakladık (Parolaları Saklamak), jetonu HMAC ile imzaladık (Kimlik Yönetimi ve
Tek Oturum). Bu modül o araçların içini açıyor: ne yaptıklarını, nasıl
çalıştıklarını ve en çok nerede yanlış kullanıldıklarını.

## Temel kelimeler

| Terim | Anlamı |
|---|---|
| **Düz metin** (plaintext) | Korunacak asıl mesaj |
| **Şifreli metin** (ciphertext) | Şifrelemeden sonra çıkan, okunamayan metin |
| **Şifreleme** (encryption) | Düz metni anahtarla şifreli metne çevirmek |
| **Şifre çözme** (decryption) | Şifreli metni anahtarla geri çevirmek |
| **Anahtar** (key) | İşlemi kişiye özel yapan gizli değer |
| **Algoritma** (cipher) | Şifreleme ve çözme kuralı |

<figure class="fig"><div class="flow">
  <span class="node">Düz metin</span><span class="arrow">→</span>
  <span class="node acc">Şifrele (anahtar)</span><span class="arrow">→</span>
  <span class="node">Şifreli metin</span><span class="arrow">→</span>
  <span class="node acc">Çöz (anahtar)</span><span class="arrow">→</span>
  <span class="node ok">Düz metin</span>
</div><figcaption>Algoritma herkesçe bilinir; yalnızca anahtar gizlidir.</figcaption></figure>

## Kodlama, özet, şifreleme: üç farklı şey

Bu üç kelime çok karıştırılır ve karıştırılması gerçek açıklara yol açar.

**Kodlama** (encoding) veriyi başka bir biçimde yazmaktır; anahtar yoktur,
herkes geri çevirir. Base64 bunun en yaygın örneği:

```python
import base64

message = "meet at noon"
encoded = base64.b64encode(message.encode()).decode()
print(encoded)
print(base64.b64decode(encoded).decode())
```

```text
bWVldCBhdCBub29u
meet at noon
```

İkinci satırı üretmek için hiçbir sır gerekmedi. Kimlik Yönetimi
bölümündeki jetonun gövdesini de böyle anahtarsız okumuştuk. Base64
"şifrelenmiş" görünür ama gizlilik sağlamaz.

**Özet** (hash) her uzunluktaki veriden sabit uzunlukta bir parmak izi
üretir ve **geri döndürülemez**:

```python
import hashlib

for text in ["meet at noon", "meet at noon!"]:
    digest = hashlib.sha256(text.encode()).hexdigest()
    print(digest[:16], len(digest))
```

```text
50a8d1d0939b05a7 64
994f34a2a5f4b73d 64
```

Tek bir ünlem bütün özeti değiştirdi, uzunluk ise hep 64 onaltılık hane
(256 bit) kaldı. Özetten mesajı geri almanın bir yolu yok; bu yüzden
parolalar özetle saklanır, şifrelenmez.

**Şifreleme** ise **anahtarla** geri çevrilebilir: anahtarı bilen okur,
bilmeyen okuyamaz.

| | Anahtar? | Geri döner mi? | Ne için? |
|---|---|---|---|
| Kodlama | Yok | Herkes için | Veriyi taşımak (e-posta, URL) |
| Özet | Yok | Hayır | Parmak izi, parola saklama |
| Şifreleme | Var | Yalnızca anahtarla | Gizlilik |

## Kriptografi neyi sağlar?

Güvenlik Nedir? CIA Üçlüsü bölümündeki CIA üçlüsü ve yanındaki kavramlar burada
araçlarla eşleşir:

| Amaç | Araç | Bu modülde |
|---|---|---|
| **Gizlilik** | Şifreleme | Simetrik Şifreleme, RSA |
| **Bütünlük** | Özet, HMAC | Özet Fonksiyonları, HMAC |
| **Kimlik doğruluğu** | HMAC, dijital imza | HMAC, Dijital İmza |
| **İnkâr edilemezlik** | Dijital imza | Dijital İmza |

Kriptografi **erişilebilirliği** sağlamaz: tersine, anahtarı kaybeden kendi
verisine de ulaşamaz.

## İki aile: simetrik ve asimetrik

- **Simetrik** (symmetric): şifreleyen ve çözen **aynı** anahtarı kullanır.
  Hızlıdır; sorun anahtarı karşı tarafa güvenle ulaştırmaktır.
- **Asimetrik** (asymmetric) ya da açık anahtarlı: bir **açık anahtar**
  (herkese verilir) ve bir **özel anahtar** (yalnızca sahibinde) vardır.
  Yavaştır ama anahtarı paylaşma sorununu çözer.

Gerçek sistemler ikisini birlikte kullanır: asimetrik yöntemle bir
simetrik anahtar üzerinde anlaşılır, veri o anahtarla şifrelenir. Modülün
sonundaki TLS El Sıkışması bölümü tam olarak bunu anlatıyor.

## Kerckhoffs ilkesi

19. yüzyılda Auguste Kerckhoffs şunu yazdı: bir şifreleme sistemi,
anahtar dışındaki her şeyi düşmanın eline geçse bile güvenli kalmalıdır.
Bu, Güvenlik İlkeleri bölümündeki **açık tasarım** ilkesinin kendisidir.
Algoritma gizli tutulursa bir gün sızar ve o gün bütün sistem çöker;
anahtar sızarsa yalnızca o anahtar değiştirilir.

Bu yüzden güvenilen algoritmalar yayımlanmış, yıllarca herkesin saldırısına
açık kalmış olanlardır. Güvenlik yalnızca **anahtarın** gizliliğine ve
anahtar sayısının büyüklüğüne dayanır.

## Anahtar ne kadar uzun olmalı?

`n` bitlik bir anahtarın `2ⁿ` olası değeri var. Saldırgan her birini
denerse (**kaba kuvvet**, brute force) ne kadar sürer? Saniyede bir
trilyon deneme yapabildiğini varsayalım:

```python
SECONDS_PER_YEAR = 365 * 24 * 3600
rate = 10**12  # a trillion guesses per second

for bits in [40, 56, 80, 128]:
    years = 2**bits / rate / SECONDS_PER_YEAR
    print(f"{bits:>3} bits: {years:.2e} years")
```

```text
 40 bits: 3.49e-08 years
 56 bits: 2.28e-03 years
 80 bits: 3.83e+04 years
128 bits: 1.08e+19 years
```

40 bit yaklaşık bir saniye, 56 bit bir günden kısa sürüyor; 128 bit ise
evrenin yaşının (yaklaşık 1,4 × 10¹⁰ yıl) yüz milyonlarca katı. Her ek bit
süreyi iki katına çıkarıyor. Bugün simetrik anahtarlar için 128 bit
alt sınır kabul edilir.

## Kendi kriptonu yazma

Bu modülde birçok şeyi sıfırdan, küçük oyuncak örneklerle yazacağız,
çünkü içini görmek yanlış kullanımı anlamanın en iyi yolu. Ama gerçek bir
uygulamada **kendi şifreleme algoritmanı ya da protokolünü yazmazsın**:
denenmiş bir kütüphanenin yüksek düzeyli işlevini kullanırsın. Uzmanların
yazdığı algoritmalarda bile yıllar sonra açık bulunuyor; kriptografide
hatalar sessizdir, program çalışmaya devam eder ve kimse fark etmez.

## Özet

- Kriptografi gizlilik, bütünlük, kimlik doğruluğu ve inkâr edilemezlik
  sağlar; erişilebilirlik sağlamaz.
- **Kodlama** anahtarsız ve geri döner, **özet** geri dönmez, **şifreleme**
  yalnızca anahtarla geri döner. Base64 şifreleme değildir.
- **Simetrik** tek anahtar, **asimetrik** açık ve özel anahtar; gerçek
  sistemler ikisini birlikte kullanır.
- **Kerckhoffs ilkesi:** algoritma açık, yalnızca anahtar gizli.
- Her ek bit kaba kuvvet süresini iki katına çıkarır; 128 bit bugünkü alt
  sınır.
- Gerçek uygulamada kendi kriptonu yazmazsın.
