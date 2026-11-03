`risky_calls(lines)` C kaynak satırlarında boy bilmeden yazan
fonksiyonların çağrılarını bulsun: `gets`, `strcpy`, `strcat`,
`sprintf`. Her bulgu `"<satır no>: <ad>"` biçiminde (satırlar 1'den
sayılır), satır sırasıyla, aynı satırda soldan sağa. `fgets` ya da
`snprintf` gibi güvenli karşılıklar **yakalanmamalı**: düzenli ifadede
kelime sınırı (`\b`) ve ardından `(` kullan.

**Beklenen çıktı:**

```
3: strcpy
5: gets
5: strcat
```
