`ticket_tokens(text)` dersteki `TOKEN` desenini kullansın; sırasıyla:

1. e-posta: `[\w.+-]+@\w+\.\w+`
2. para: `\$\d+(?:\.\d+)?`
3. sipariş numarası: `[A-Z]+-\d+`
4. kelime: `\w+(?:'\w+)?`
5. tek noktalama: `[^\w\s]`

Deseni `re.compile(..., re.VERBOSE)` ile bir kez kur, fonksiyon
`TOKEN.findall(text)` döndürsün.

**Beklenen çıktı:**

```
24 []
25 ['ben52@example.com']
18 ['ORD-65149']
18 ['jo11@example.com', 'ORD-34877']
29 ['ORD-27246']
25 ['ORD-86146']
17 ['ORD-15317']
36 ['ORD-25113', '$233.00']
```
