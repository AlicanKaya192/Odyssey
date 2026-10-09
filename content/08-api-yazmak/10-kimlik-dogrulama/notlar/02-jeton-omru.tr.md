Bir jeton sonsuza kadar geçerli olmamalı. Çalınırsa çalan kişi onu
istediği kadar kullanır.

## Çıkış (logout)

Sunucu jetonu unutursa jeton geçersiz olur:

```python
@app.post("/logout", status_code=204)
def logout(cred: Annotated[HTTPAuthorizationCredentials, Depends(bearer)]):
    tokens.pop(cred.credentials, None)
```

Bundan sonra aynı jetonla `GET /me` → `401 Invalid token`.

## Süresi dolan jeton

Jetonun yanında oluşturulduğu zamanı sakla, kullanırken yaşına bak:

```python
import time

TOKEN_SECONDS = 3600
tokens = {}          # jeton -> {"user": ..., "created": ...}


def current_user(cred: Annotated[HTTPAuthorizationCredentials, Depends(bearer)]):
    info = tokens.get(cred.credentials)
    if info is None or time.time() - info["created"] > TOKEN_SECONDS:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return info["user"]
```

İstemci `401` alınca yeniden giriş yapar.

## Bellekteki jetonlar

Bu bölümdeki `tokens` sözlüğü sunucu belleğinde: sunucu yeniden başlarsa
herkes çıkış yapmış olur. Gerçek bir uygulamada jetonlar veritabanında
tutulur ya da JWT gibi sunucunun saklamadığı imzalı jetonlar kullanılır.

## İstemci tarafı (API Kullanmak modülünden)

```python
r = requests.post(f"{BASE}/token", json={"username": "ada", "password": "..."})
token = r.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}
requests.get(f"{BASE}/me", headers=headers)
```

`/docs` sayfasında **Authorize** düğmesine jetonu yapıştırınca sayfa da
bütün isteklere bu başlığı ekliyor.
