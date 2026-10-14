`render_latest(templates, name, values)` `templates[name]` içindeki
sürümlerden (anahtarlar `"1"`, `"2"`, `"10"` gibi metin) **sayı olarak**
en büyüğünü seçsin ve onu `str.format(**values)` ile doldursun. Döndür:
`[sürüm numarası (int), metin]`. Şablon adı yoksa `[0, ""]`.

**Beklenen çıktı:**

```
10
Pick one category: Hi
[0, '']
```
