Paket `nonce + cipher + tag` biçiminde onaltılık bir metin: nonce
**8 bayt**, etiket **32 bayt**, arası şifreli metin (uzunluğu değişir).
`split_box(box_hex)` paketi `[nonce_hex, cipher_hex, tag_hex]` listesine
bölsün. 1 bayt onaltılık metinde 2 karakterdir: nonce ilk 16, etiket son
64 karakter.

**Beklenen çıktı:**

```
1111111111111111
aabbcc
32 byte tag
```
