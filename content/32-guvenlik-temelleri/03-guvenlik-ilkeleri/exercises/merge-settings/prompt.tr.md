Bir programın güvenli varsayılan ayarları `defaults` sözlüğünde.
Kullanıcı kendi ayarlarını `user` sözlüğüyle veriyor.

`merge_settings(defaults, user)` **yeni** bir sözlük döndürsün:

- `defaults`'un bütün anahtarlarıyla başlasın,
- `user`'daki değer yalnızca anahtar `defaults`'ta **varsa** uygulansın;
  bilinmeyen anahtarlar atılsın,
- `defaults` sözlüğünün kendisi değişmesin.

**Beklenen çıktı:**

```
debug True
tls True
password_min 12
defaults debug: False
```
