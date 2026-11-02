# Genel Tekrar

Bu modül güvenliğin temel dilini kurdu: neyi koruduğumuzu, neye karşı
koruduğumuzu, kimin neye erişebileceğine nasıl karar verildiğini ve bütün
bunların bir kurumda nasıl yönetildiğini. Bu bölüm hepsini bir arada
görüyor; sonunda 40 karışık soru ve birden çok bölümü birleştiren beş
alıştırma var.

## Modülün haritası

| Konu | Ana fikir |
|---|---|
| **CIA üçlüsü** | Gizlilik, bütünlük, erişilebilirlik; her olay en az birini bozar. |
| **Tehdit, açık, risk** | Tehdit bir açığı kullanınca varlık zarar görür; risk = olasılık × etki. CVE açığın adı, CVSS ağırlığı. |
| **Risk değerlendirme** | Nitel 1–5 ölçek ya da parayla (SLE = AV × EF, ALE = SLE × ARO). Dört cevap: azalt, aktar, kabul et, kaçın. |
| **Güvenlik ilkeleri** | En az yetki, varsayılan ret, güvenli başarısızlık, derinlemesine savunma, tam aracılık, açık tasarım, basitlik, görev ayrılığı. |
| **Kimlik doğrulama** | Bilinen, sahip olunan, olunan; çok faktör farklı türlerden. TOTP zamandan kod üretir. |
| **Parolalar** | Güç = entropi (uzunluk × log₂ alfabe); uzunluk karmaşıklıktan çok kazandırır. |
| **Parola saklama** | Ne düz metin ne şifreleme: tuzlu ve yavaş özet (PBKDF2 gibi), sabit süreli karşılaştırma. |
| **Yetkilendirme** | Özne, eylem, nesne; karar sunucuda; yatay ve dikey yetki aşımı. |
| **Erişim modelleri** | DAC sahibi, MAC kural, RBAC rol, ABAC özellik ile karar verir. |
| **En az yetki** | Yetki birikmesi, kullanılmayan yetki, süreli yetki, görev ayrılığı. |
| **Tehdit modelleme** | Veri akış şeması, güven sınırları, STRIDE. |
| **Saldırı yüzeyi** | Envanter, giriş noktalarını tartmak, kullanılmayanı kapatmak. |
| **Sosyal mühendislik** | Güven, telaş ve otoriteyi kullanır; alan adının gerçek sahibine bakılır; savunma süreçtir. |
| **Zararlı yazılım** | Türler yayılma ve davranışa göre; imza ve davranış tabanlı tespit; 3-2-1 yedek. |
| **Kimlik yönetimi** | JML, öksüz hesap, SSO, IdP ve SP; jetonda önce imza, sonra iddialar. |
| **Politika ve standartlar** | Politika → standart → prosedür → kılavuz; veri sınıfları; ISO/IEC 27001, NIST CSF; uyumluluk güvenlik değildir. |

## Bir isteğin yolu

Modülün parçalarının çoğu tek bir isteğin yolunda buluşur:

<figure class="fig"><div class="flow">
  <span class="node">İstek</span><span class="arrow">→</span>
  <span class="node acc">Kimlik doğrulama</span><span class="arrow">→</span>
  <span class="node acc">Yetkilendirme</span><span class="arrow">→</span>
  <span class="node">Kayıt</span><span class="arrow">→</span>
  <span class="node ok">Cevap</span>
</div><figcaption>Önce "kimsin?", sonra "buna iznin var mı?", her durumda kayda geçir.</figcaption></figure>

Aşağıdaki küçük program bunu baştan sona yapıyor: parolayı tuzlu ve yavaş
özetle denetliyor (Parola Saklama), rolüne göre izin veriyor (Erişim
Denetimi Modelleri), bilmediği her şeyi reddediyor (Güvenlik İlkeleri) ve
her denemeyi kayda yazıyor.

```python
import hashlib
import hmac

SALT = b"fixed-salt-for-the-lesson"


def hash_password(password):
    return hashlib.pbkdf2_hmac("sha256", password.encode(), SALT, 100_000).hex()


users = {"ada": {"hash": hash_password("blue-river-42"), "role": "editor"}}
roles = {"viewer": {"read"}, "editor": {"read", "write"}}
log = []


def request(user, password, action):
    record = users.get(user)
    known = record["hash"] if record else ""
    if not hmac.compare_digest(known, hash_password(password)):
        result = "denied: authentication"
    elif action not in roles[record["role"]]:
        result = "denied: authorization"
    else:
        result = "allowed"
    log.append(f"{user} {action} {result}")
    return result


print(request("ada", "blue-river-42", "write"))
print(request("ada", "wrong", "write"))
print(request("ada", "blue-river-42", "delete"))
print(request("zeynep", "x", "read"))
print(len(log), "log lines")
```

```text
allowed
denied: authentication
denied: authorization
denied: authentication
4 log lines
```

Küçük ayrıntılara dikkat: bilinmeyen kullanıcı için de parola özeti
hesaplanıyor, böylece cevap süresi "böyle bir kullanıcı var mı?" sorusunu
ele vermiyor. Kimlik doğrulama hatasında hangi parçanın (ad mı parola mı)
yanlış olduğu söylenmiyor. `delete` hiçbir rolde olmadığı için kendiliğinden
reddediliyor: izin yazılmadıysa yoktur. Gerçek bir sistemde tuz her
kullanıcıya ayrı ve rastgele olur; burada sonuç her çalıştırmada aynı
çıksın diye sabit.

## Sık karışan çiftler

| Çift | Fark |
|---|---|
| Kimlik doğrulama / yetkilendirme | "Kimsin?" / "Buna iznin var mı?" |
| Tehdit / açık | Zarar verebilecek şey / onun kullandığı zayıflık |
| Özet / şifreleme | Geri döndürülemez / anahtarla geri açılır |
| Gizlilik / bütünlük | Yetkisiz kimse okumasın / yetkisiz kimse değiştirmesin |
| ACL / yetenek listesi | Nesnenin listesi / öznenin listesi |
| Bell-LaPadula / Biba | Gizliliği korur / bütünlüğü korur |
| Virüs / solucan | Taşıyıcı ve kullanıcı ister / kendi kendine yayılır |
| İmza / davranış tabanlı tespit | Bilineni hızlı bulur / yeniyi yakalar, yanlış alarm verebilir |
| OAuth 2.0 / OpenID Connect | Yetki devri / kimlik |
| Politika / standart | Ne ve neden / ölçülebilir kural |
| Uyumluluk / güvenlik | Kutular işaretli / kontroller her gün çalışıyor |

## Buradan sonra

Bu modül kavramları kurdu. Patikanın sonraki modülleri bunların üstüne
çıkıyor: **Kriptografi** özetin, şifrelemenin ve imzanın içini açıyor;
**Ağ ve Web Güvenliği** isteklerin ağda nasıl korunduğunu ve web
uygulamalarının sık açıklarını; **Sistem Güvenliği ve Operasyon** ise
sistemlerin sertleştirilmesini, kayıtların izlenmesini ve olay müdahalesini
anlatıyor.

## Özet

- Güvenlik bir varlığı belirli tehditlere karşı, riske göre korumaktır;
  CIA neyin bozulduğunu, risk ne kadar önemli olduğunu söyler.
- Kararlar ilkelere dayanır: en az yetki, varsayılan ret, derinlemesine
  savunma, görev ayrılığı.
- Bir isteğin yolu: kimlik doğrulama → yetkilendirme → kayıt.
- İnsanlar, zararlı yazılımlar ve hesaplar da saldırı yüzeyinin parçasıdır.
- Hepsi yazılı politikalar ve standartlarla yönetilir; ama ölçülen şey
  kutular değil, kontrollerin gerçekten çalışmasıdır.
