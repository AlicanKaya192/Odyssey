Hat her adımın çıkış koduna bakıyor. İki fonksiyon yaz:

`step_status(code)`:

- `0` → `"green"`
- `1` → `"red: tests failed"`
- `5` → `"red: no tests"`
- başka her sayı → `"red: error"`

`pipeline_status(codes)`: adımların çıkış kodları sırayla bir listede. Hepsi `0` ise `"green"`. Değilse ilk sıfır olmayan adımda dur ve şunu döndür (adımlar 1'den sayılır):

- `"red at step 2 (red: tests failed)"`

**Beklenen çıktı:**

```
green
red: tests failed
red: no tests
red: error
green
red at step 2 (red: tests failed)
red at step 3 (red: no tests)
```
