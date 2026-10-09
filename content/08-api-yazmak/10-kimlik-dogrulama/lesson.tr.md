# Kimlik Doğrulama

Şimdiye kadar yazdığın her uç noktayı adresi bilen herkes çağırabiliyordu.
Gerçek bir API'de bazı işler yalnızca **belli kişilere** açık olmalı:
kendi notlarını okumak, kayıt silmek, yönetici sayfası. Bu bölümde iki
soruyu cevaplıyorsun:

- **Kimlik doğrulama** (authentication): *Sen kimsin?* Bilmiyorsam `401`.
- **Yetkilendirme** (authorization): *Bunu yapmaya iznin var mı?* Yoksa `403`.

API Kullanmak modülünde istemci olarak anahtar ve jeton göndermiştin; şimdi onları
**denetleyen** tarafı yazıyorsun.

## 1. API anahtarı

En basit yol: her istemciye gizli bir anahtar verirsin, istemci onu her
istekte bir başlıkta gönderir.

```python
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import APIKeyHeader

app = FastAPI()
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
KEYS = {"k-123": "ada"}


def require_api_key(key: Annotated[str | None, Depends(api_key_header)]):
    if key not in KEYS:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return KEYS[key]


@app.get("/reports")
def reports(owner: Annotated[str, Depends(require_api_key)]):
    return {"owner": owner}
```

- `APIKeyHeader(name="X-API-Key")`: başlığı okuyan hazır bir bağımlılık.
  Önceki bölümdeki `Header()` ile aynı işi yapıyor; farkı `/docs`'a
  "bu API anahtar istiyor" diye yazması (sayfada **Authorize** düğmesi
  çıkıyor).
- `auto_error=False`: başlık yoksa `None` versin, hata mesajını biz
  yazalım.

```text
GET /reports                      401 {"detail": "Invalid API key"}
GET /reports  (X-API-Key: k-123)  200 {"owner": "ada"}
```

Anahtarı **sorguya** koyma (`?key=k-123`): adresler sunucu günlüklerine,
tarayıcı geçmişine yazılır. Başlık daha güvenli.

## 2. Şifreler: asla düz saklanmaz

Kullanıcı adı ve şifreyle giriş yapılacaksa sunucu şifreyi bir yerde
tutmalı. **Düz metin olarak değil**: veritabanı bir gün sızarsa bütün
şifreler gider (insanlar aynı şifreyi başka yerlerde de kullanır).

Bunun yerine şifrenin **özeti** (hash) saklanır: geri çevrilemeyen bir
dönüşüm. Giriş sırasında gelen şifrenin özeti alınıp saklananla
karşılaştırılır.

```python
import hashlib
import hmac


def hash_password(password: str, salt: bytes) -> str:
    return hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100_000).hex()


SALT = b"fixed-salt-for-demo"
users = {"ada": {"hash": hash_password("lovelace", SALT)}}


def check_password(username: str, password: str) -> bool:
    user = users.get(username)
    if user is None:
        return False
    return hmac.compare_digest(user["hash"], hash_password(password, SALT))
```

- `pbkdf2_hmac(..., 100_000)`: özeti **kasıtlı olarak yavaş** hesaplıyor
  (100 000 tur). Doğru şifreyi bilen için fark edilmez; milyonlarca şifre
  deneyen saldırgan için çok yavaş. Sonuç 64 karakterlik bir metin.
- **Tuz** (salt): özetten önce şifreye eklenen rastgele bayt. Aynı şifreli
  iki kullanıcının özetleri farklı olur. Gerçekte her kullanıcıya ayrı tuz
  verilir (`secrets.token_bytes(16)`) ve özetin yanında saklanır; burada
  kısalık için tek tuz.
- `hmac.compare_digest`: iki metni karşılaştırırken süresi metinlerin
  nerede ayrıldığına bağlı olmuyor; saldırgan süreyi ölçüp ipucu alamıyor.

Gerçek projelerde bu iş için `bcrypt` ya da `argon2` gibi kütüphaneler
kullanılır; fikir aynı.

## 3. Jeton: bir kez giriş, sonra jeton

Her istekte şifre göndermek iyi değil. Bunun yerine istemci **bir kez**
giriş yapar ve karşılığında bir **jeton** (token) alır; sonraki isteklerde
jetonu gönderir.

```python
import secrets
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

bearer = HTTPBearer()
tokens = {}


class Login(BaseModel):
    username: str
    password: str


@app.post("/token")
def login(form: Login):
    if not check_password(form.username, form.password):
        raise HTTPException(status_code=401, detail="Wrong username or password")
    token = secrets.token_hex(16)
    tokens[token] = form.username
    return {"access_token": token, "token_type": "bearer"}


def current_user(cred: Annotated[HTTPAuthorizationCredentials, Depends(bearer)]):
    if cred.credentials not in tokens:
        raise HTTPException(status_code=401, detail="Invalid token")
    return tokens[cred.credentials]


@app.get("/me")
def me(user: Annotated[str, Depends(current_user)]):
    return {"user": user}
```

- `secrets.token_hex(16)`: tahmin edilemeyen 32 karakterlik rastgele
  metin. `random` modülü bu iş için **kullanılmaz**; tahmin edilebilir.
- `HTTPBearer()`: `Authorization: Bearer <jeton>` başlığını okuyan hazır
  bağımlılık. `cred.credentials` jetonun kendisi.
- `tokens` sözlüğü hangi jetonun kime ait olduğunu tutuyor.

<figure class="fig">
  <div class="flow">
    <span class="node">POST /token<br><small>kullanıcı adı + şifre</small></span><span class="arrow">→</span>
    <span class="node acc">jeton<br><small>301f1864…</small></span><span class="arrow">→</span>
    <span class="node">GET /me<br><small>Authorization: Bearer 301f…</small></span><span class="arrow">→</span>
    <span class="node ok">{"user": "ada"}</span>
  </div>
  <figcaption>Şifre yalnızca bir kez gidiyor; sonraki her istek jetonla. Sunucu jetonun kime ait olduğunu <code>tokens</code> sözlüğünden buluyor.</figcaption>
</figure>

Ölçtüğümüz akış:

```text
POST /token {"username": "ada", "password": "nope"}      401
POST /token {"username": "ada", "password": "lovelace"}  200
            {"access_token": "301f1864...", "token_type": "bearer"}
GET /me  (başlık yok)                  401 {"detail": "Not authenticated"}
GET /me  (Authorization: Bearer zzz)   401 {"detail": "Invalid token"}
GET /me  (Authorization: Bearer 301f…) 200 {"user": "ada"}
```

Başlık hiç yoksa `HTTPBearer` kendisi `401` veriyor ve cevaba
`WWW-Authenticate: Bearer` başlığını ekliyor (ölçtük).

## 4. Yetki: 401 değil 403

Kim olduğunu bildikten sonra izni denetlemek ayrı bir bağımlılık:

```python
roles = {"ada": "admin", "alan": "member"}


def require_admin(user: Annotated[str, Depends(current_user)]):
    if roles.get(user) != "admin":
        raise HTTPException(status_code=403, detail="Admins only")
    return user
```

`current_user` → `require_admin` zinciri: önce kim (`401`), sonra izin
(`403`). Önceki bölümdeki bağımlılık zincirinin tam olarak bu iş için
olduğunu şimdi görüyorsun.

## Bilmen gereken iki şey daha

- **HTTPS.** Anahtar, şifre ve jeton başlıkta **açık metin** gidiyor.
  Gerçek sunucuda adres `https://` olmalı; yoksa aradaki herkes okur.
  Bilgisayarındaki deneme sunucusu (`127.0.0.1`) dışarı çıkmadığı için
  sorun değil.
- **JWT.** Burada jetonlar sunucunun belleğinde (`tokens`). Yaygın bir
  başka yol JWT: içinde kullanıcı adı ve son kullanma tarihi olan, sunucunun
  **imzaladığı** jeton; sunucu bir şey saklamadan imzayı denetler. Ayrı bir
  paket (`PyJWT`) ister; mantık bu bölümdekinin aynısı.

## Özet

- `401` kim olduğunu bilmiyorum, `403` biliyorum ama izin yok.
- API anahtarı başlıkta: `APIKeyHeader(name="X-API-Key")`.
- Şifre asla düz değil: tuzlu, yavaş özet (`pbkdf2_hmac`), karşılaştırma
  `hmac.compare_digest`.
- Giriş → `secrets.token_hex` ile jeton → `Authorization: Bearer` →
  `HTTPBearer` + `current_user` bağımlılığı.
- İzin ayrı bir bağımlılık, `current_user`'a bağlı.
