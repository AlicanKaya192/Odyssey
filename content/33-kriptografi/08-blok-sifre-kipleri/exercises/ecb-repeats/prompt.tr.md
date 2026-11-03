ECB kipinde aynı düz metin bloğu aynı şifreli bloğu verir. Bir şifreli
metinde tekrar eden 16 baytlık bloklar, ECB kullanıldığının işaretidir.
`count_repeats(cipher_hex)` onaltılık şifreli metni **16 baytlık**
bloklara bölsün ve daha önce görülmüş bir bloğun kaç kez tekrar ettiğini
döndürsün. Dikkat: 16 bayt, onaltılık metinde **32 karakter** eder.

**Beklenen çıktı:**

```
2
0
0
```
