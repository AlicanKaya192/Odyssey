`eval_postfix(tokens)` fonksiyonunu **yığınla** yaz: postfix ifadeyi
hesaplasın. Belirteçler tam sayı metinleri ve `+`, `-`, `*` işlemcileri.

- `["3", "4", "+", "2", "*"]` → `14`
- `["8", "2", "-"]` → `6`

Sayıyı `int(token)` ile yığına koy. İşlemcide **önce sağdaki** işleneni al:
`right = stack.pop()`, sonra `left = stack.pop()`.

**Beklenen çıktı:**

```
14
6
14
```
