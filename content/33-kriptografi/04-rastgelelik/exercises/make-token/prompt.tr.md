`make_token(length, alphabet)` alfabedeki karakterlerden `length`
karakterlik rastgele bir jeton üretsin. Karakterleri `secrets.choice` ile
seç.

Jetonun değeri her çalıştırmada değiştiği için alttaki kod değerleri değil
**özellikleri** yazdırıyor: uzunluk, alfabe, 100 jetonun hepsinin farklı
olması ve son satırda tohumun etkisi. Başlangıç kodundaki `random.choices`
aynı tohumla aynı jetonu veriyor; `secrets` ise tohumdan etkilenmez.

**Beklenen çıktı:**

```
lengths ok: True
alphabet ok: True
all different: True
seed has no effect: True
```
