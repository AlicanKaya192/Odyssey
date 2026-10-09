Write the function `is_balanced(text)` **with a stack**: it returns `True` if
the `()`, `[]`, `{}` brackets in the text open and close properly, `False`
otherwise. Characters that are not brackets do not matter.

Do not forget three cases: the stack may be **empty** when a closing bracket
arrives, the top bracket may be of the **wrong kind**, and brackets may be
**left open** at the end.

**Expected output:**

```
(a[b]{c}) True
(a[b)] False
(( False
)( False
 True
```
