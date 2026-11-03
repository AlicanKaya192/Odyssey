`string_to_mode(text)` dokuz harflik bir izin dizesini (`"rwxr-x---"`)
sayıya çevirsin: `0o750`, yani `488`. Her harf bir bittir; harf `-` değilse
o bit açıktır. Dizenin ilk harfi en yüksek bittir (`0o400`), son harfi en
düşük (`0o001`).

**Beklenen çıktı:**

```
rwxr-xr-x 0o755
rw-r----- 0o640
rw------- 0o600
--------- 0o0
```
