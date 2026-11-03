`keystream` hazır. `items` her biri `[nonce_hex, data_hex]` olan bir
liste; hepsi aynı `key_hex` ile şifrelenecek. `encrypt_all(key_hex, items)`
her öğe için bir sonuç döndürsün:

- nonce **daha önce bu çağrıda kullanılmışsa** `"nonce reused"`,
- değilse veriyi akış şifresiyle şifreleyip şifreli metni onaltılık ver ve
  nonce'u kullanılmış say.

Nonce'u tekrar eden öğe şifrelenmez; önceki dersin tekrar-anahtar
hatasını önlüyoruz.

**Beklenen çıktı:**

```
65
14
nonce reused
```
