Giriş ve `current_user` hazır; `roles` sözlüğünde `ada` yönetici, `alan`
üye.

**Yapman gerekenler:**

1. `require_admin`: `current_user`'a bağımlı; rol `admin` değilse `403`
   (`"Admins only"`).
2. `GET /admin/users` → kullanıcı adlarının sıralı listesi; yalnızca
   yönetici.

- jetonsuz → `401`
- `alan`'ın jetonu → `403`
- `ada`'nın jetonu → `["ada", "alan"]`
