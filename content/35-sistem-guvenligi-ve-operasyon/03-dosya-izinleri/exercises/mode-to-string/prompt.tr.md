`mode_to_string(mode)` bir izin sayısını (`0o750` gibi) dokuz harflik
dizeye çevirsin: `"rwxr-x---"`. Sahip, grup ve diğerleri sırasıyla; her
sınıfta `r` (4), `w` (2), `x` (1) bitine bak, yoksa `-` yaz.
`stat.filemode` kullanma: amaç bitleri kendin okumak.

**Beklenen çıktı:**

```
0o755 rwxr-xr-x
0o640 rw-r-----
0o600 rw-------
0o7 ------rwx
```
