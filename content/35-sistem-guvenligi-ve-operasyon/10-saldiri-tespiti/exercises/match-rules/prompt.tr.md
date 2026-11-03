`rules` kural adı → düzenli ifade metni. `match_rules(lines, rules)` her
satırı her kurala karşı `re.search` ile denesin ve eşleşmeler için
`"<satir no>: <kural>"` döndürsün; satırlar 1'den sayılır, aynı satırda
kurallar ada göre abece sırasıyla. Başlangıç kodu kalıbı düz metin gibi
arıyor; düzenli ifade olarak denenmeli.

**Beklenen çıktı:**

```
2: path traversal
3: path traversal
3: script tag
```
