`merge_state(required, runs)` fonksiyonunu yaz. `required` zorunlu kontrol adları; `runs` gelen sonuçlar, eskiden yeniye, her biri `[ad, durum]`. Bir kontrol yeniden çalıştırılabilir: **her adın son sonucu** geçerli.

- Zorunlulardan birinin son durumu `"failure"` ise: `"blocked by AD"` (listede ilk düşen).
- Değilse, zorunlulardan birinin son durumu `"success"` ya da `"skipped"` değilse (hiç gelmemişse de): `"waiting for AD"` (listede ilk).
- Hepsi tamamsa: `"ready"`.

**Beklenen çıktı:**

```
waiting for test (3.12)
ready
blocked by test (3.13)
```
