`cookie_header(name, value, max_age)` şu biçimde bir `Set-Cookie`
değeri döndürsün (parçalar `"; "` ile ayrılır):
`name=value; Max-Age=N; Path=/; Secure; HttpOnly; SameSite=Lax`.

**Beklenen çıktı:**

```
session=abc123
Max-Age=3600
Path=/
Secure
HttpOnly
SameSite=Lax
```
