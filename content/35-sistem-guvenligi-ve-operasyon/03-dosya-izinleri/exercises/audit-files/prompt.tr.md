Her dosya bir sözlük: `path`, `mode`, `secret` (sır içeriyor mu).
`audit_files(files)` bulguları satır satır döndürsün, yola göre abece
sırasıyla:

- `mode & 0o002` ise `"<yol>: world-writable"`,
- `secret` doğruysa ve `mode & 0o077` ise `"<yol>: secret exposed"`.

Bir dosyada ikisi birden varsa önce `world-writable`.

**Beklenen çıktı:**

```
/home/ada/.env: secret exposed
/srv/app/config.ini: world-writable
/tmp/notes.txt: world-writable
/tmp/notes.txt: secret exposed
```
