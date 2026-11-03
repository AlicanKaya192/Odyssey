`unpinned(lines)` bir `requirements.txt`'nin satırlarında **tam sürümle
sabitlenmemiş** (`==` içermeyen) paketlerin adlarını, satır sırasıyla
döndürsün. Boş satırlar ve yorumlar (`#`'ten sonrası) atlanır. Ad, ilk
`<`, `>`, `=`, `!`, `~`, boşluk, `;` ya da `[` karakterine kadar olan
kısımdır: `re.split(r"[<>=!~ ;\[]", line)[0]`.

**Beklenen çıktı:**

```
['pandas', 'flask', 'httpkit']
```
