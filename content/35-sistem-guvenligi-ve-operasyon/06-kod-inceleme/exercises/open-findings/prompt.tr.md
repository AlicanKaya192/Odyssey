Her bulgu `[satir, ileti]`; `lines` kaynağın satırları (satır 1 =
`lines[0]`). Bir bulgu ancak satırında **gerekçeli** bir işaret varsa
kapanır: `"# nosec: "` ve ardından boş olmayan bir gerekçe. Yalnızca
`# nosec` yazmak yetmez. `open_findings(findings, lines)` açık kalan
bulguları `"<satir>: <ileti>"` olarak, satıra göre sıralı döndürsün.

**Beklenen çıktı:**

```
2: eval
3: eval
```
