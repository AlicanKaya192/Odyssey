`apply_umask(base, umask)` programın istediği izinden (`base`) umask'taki
bitleri **kaldırsın**. Başlangıç kodu çıkarma yapıyor: `0o666 - 0o022`
tesadüfen doğru çıkar ama `0o666 - 0o077` `0o600` vermez. Bit işlemiyle
yaz: `base & ~umask`.

**Beklenen çıktı:**

```
0o644
0o600
0o750
```
