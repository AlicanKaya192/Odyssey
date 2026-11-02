`make_password(length)` harf ve rakamlardan oluşan rastgele bir parola
üretsin; parola **en az bir küçük harf, bir büyük harf ve bir rakam**
içermeli.

- Karakterleri `secrets.choice` ile seç; `random` modülü tahmin
  edilebilir, tohum (`seed`) ise her çalıştırmada aynı parolaları üretir.
- Üretilen parola üç türü içermiyorsa at ve yeniden üret.

Alttaki kod 50 parola üretip özelliklerini yazdırıyor; parolaların
kendisini değil.

**Beklenen çıktı:**

```
lengths ok: True
classes ok: True
unique: 50
```
