`encrypt_block` hazır: Feistel ağı, 4 tur. `decrypt_block(key_hex,
block_hex)` şifreli bloğu geri çevirsin ve onaltılık döndürsün. Turlar
**ters sırayla** uygulanır ve her turda `mixed`, `right` ile
`round_fn(key, i, left)`'in XOR'udur; ardından `left, right = mixed,
left`.

**Beklenen çıktı:**

```
6fcb9dd4b0ccbb92
True
b'exactly16bytes!!'
```
