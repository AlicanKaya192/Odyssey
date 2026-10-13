`ticket_tokens(text)` should use the lesson's `TOKEN` pattern, in this order:

1. email: `[\w.+-]+@\w+\.\w+`
2. money: `\$\d+(?:\.\d+)?`
3. order number: `[A-Z]+-\d+`
4. word: `\w+(?:'\w+)?`
5. single punctuation: `[^\w\s]`

Build the pattern once with `re.compile(..., re.VERBOSE)`; the function
should return `TOKEN.findall(text)`.

**Expected output:**

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
