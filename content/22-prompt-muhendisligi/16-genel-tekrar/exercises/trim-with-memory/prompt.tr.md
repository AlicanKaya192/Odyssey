`trim_history(messages, keep, facts)` sistem mesajlarını korusun, onların
arkasına `facts` boş değilse bir bellek mesajı koysun (`system` rolünde
`"Known facts: "` + anahtar sırasıyla `"anahtar: değer"` parçaları `"; "`
ile) ve sistem dışındaki mesajlardan yalnızca son `keep` tanesini eklesin.

**Beklenen çıktı:**

```
system | Be brief.
system | Known facts: order: ORD-48213
assistant | On 2026-10-09.
user | Thanks!
```
