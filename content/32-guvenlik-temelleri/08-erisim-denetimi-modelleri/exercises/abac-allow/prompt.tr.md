`abac_allow(subject, resource, action, hour)` hastanenin kuralını uygulasın,
kuralları bu sırayla dene:

1. Kaydın `sensitivity` değeri `"high"` ve öznenin `mfa` değeri `False`
   ise → `False` (hassas kayda iki adımlı giriş şart).
2. `role` `"doctor"` ise → bölümler (`dept`) aynıysa `True`.
3. `role` `"nurse"` ise → bölümler aynı, eylem `"read"` ve `7 <= hour < 19`
   ise `True`.
4. Öteki her durum → `False`.

Başlangıç kodu dersteki kural; ilk maddeyi bilmiyor.

**Beklenen çıktı:**

```
True True
True False
```
